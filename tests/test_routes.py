"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from random import randint
from unittest import TestCase
from unittest.mock import MagicMock, patch
from tests.factories import ShopcartFactory, ItemFactory
from service.routes import app
from service.models import Shopcart, db
from service.common import status  # HTTP Status Codes

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/shopcarts"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestShopcartServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Shopcart.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_shopcarts(self, count):
        """ Factory method to create shopcarts in bulk """
        shopcarts = []
        for _ in range(count):
            shopcart = ShopcartFactory()
            resp = self.client.post(BASE_URL, json=shopcart.serialize())
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test Shopcart"
            )
            new_shopcart = resp.get_json()
            shopcart.id = new_shopcart["id"]
            shopcarts.append(shopcart)
        return shopcarts

    def _create_items(self, count):
        """Factory method to create items in bulk"""
        items = []
        for _ in range(count):
            item = ItemFactory()
            items.append(item)

        return items


    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_shopcart(self):
        """It should Create a new Shopcart"""
        shopcart = ShopcartFactory()
        resp = self.client.post(
            BASE_URL, json=shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["customer_id"], shopcart.customer_id, "customer_id does not match")
  

        # Check that the location header was correct by getting it
        resp = self.client.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["customer_id"], shopcart.customer_id, "customer_id does not match")

    def test_get_account(self):
        """It should Read a single Shopcart"""
        # get the id of a Shopcart
        shopcart = self._create_shopcarts(1)[0]
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], shopcart.id)
        resp = self.client.get(f"{BASE_URL}/123456", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_shopcart(self):
        """It should Delete a shopcart with a specific ID"""
        shopcart = self._create_shopcarts(1)[0]
        resp = self.client.delete(
            f"{BASE_URL}/{shopcart.id}"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.client.delete(
            f"{BASE_URL}/{shopcart.id}"
        ) 
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_all_shopcarts(self):
        """It should List all existing shopcarts."""
        shopcarts = [sc.serialize() for sc in self._create_shopcarts(5)]
        resp = self.client.get(
            f"{BASE_URL}"
        )
        resp_dict = resp.get_json()

        self.assertEqual(resp_dict["shopcarts"], shopcarts)

    def test_reset_shopcart(self):
        """It should reset a shopcart (clear all items)."""
        shopcart = self._create_shopcarts(1)[0]
        shopcart.items = self._create_items(randint(0, 10))
        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}/reset"
        )
        resp_dict = resp.get_json()
        
        # check if the list of items is cleared
        self.assertEqual(len(resp_dict["items"]), 0)

        # check if the rest of the shopcart info remains the same
        cleared_shopcart = shopcart
        cleared_shopcart.items.clear()
        self.assertEqual(resp_dict, cleared_shopcart.serialize())

        # check if the function behaves given that the shopcart does not exist
        shopcart_id = shopcart.id
        resp = self.client.delete(
            f"{BASE_URL}/{shopcart.id}"
        )
        resp = self.client.put(
            f"{BASE_URL}/{shopcart_id}/reset"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
