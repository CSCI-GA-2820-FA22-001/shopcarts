"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from random import randint, sample
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

    def _create_items(self, count):
        """ Factory method to create items in bulk """
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
        self.assertEqual(
            new_shopcart["customer_id"], shopcart.customer_id, "customer_id does not match")

        # Check that the location header was correct by getting it
        resp = self.client.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_shopcart = resp.get_json()
        self.assertEqual(
            new_shopcart["customer_id"], shopcart.customer_id, "customer_id does not match")

        resp = self.client.post("/shopcarts", json=shopcart.serialize(), content_type="test/html"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        resp = self.client.post("/shopcarts", json={"name": "not enough data"}, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

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
        resp = self.client.get(f"{BASE_URL}/123456",
                               content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_an_item_from_shopcart(self):
        """It should delete an item from a shopcart"""
        shopcart = self._create_shopcarts(1)[0]
        item = self._create_items(1)[0]
        item.shopcart_id = shopcart.id
        self.client.post(
            f"{BASE_URL}/{shopcart.id}/items", json=item.serialize(), content_type="application/json"
        )
        resp = self.client.delete(f"{BASE_URL}/{shopcart.id}/items/{item.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.client.delete(f"{BASE_URL}/{shopcart.id}/items/{item.id}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_item(self):
        """It should list all items in a Shopcart"""
        # get the id of a Shopcart
        shopcart = self._create_shopcarts(1)[0]
        items = self._create_items(5)
        for item in items:
            shopcart.items.append(item)
        shopcart.create()
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/items"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        for (expect_item, retriveved_item) in zip(shopcart.items, data["items"]):
            self.assertEqual(expect_item.serialize(), retriveved_item)

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

    def test_update_shopcart(self):
        """It should update a shopcart with JSON content"""

        # Create a fictional shopcart and POST it
        shopcart = self._create_shopcarts(1)[0]
        resp = self.client.post(
            BASE_URL, json=shopcart.serialize(), content_type="application/json"
        )

        # Create items and assign them to shopcart.items
        items = self._create_items(randint(1, 5))
        for item in items:
            item.shopcart_id = shopcart.id
        shopcart.items = items

        # Update the Shopcart with JSON from shopcart
        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}",
            json=shopcart.serialize(),
            content_type="application/json"
        )
        # Check if successful
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertDictEqual(resp.get_json(), shopcart.serialize())

        # Update a shopcart with shopcart_id in JSON unmatched
        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id + randint(2,10)}",
            json=shopcart.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Update a non-existing shopcart
        shopcart.id += randint(5, 10)
        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}",
            json=shopcart.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.client.put(
            "/shopcarts", 
            json={"abc": "defg"}, 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_add_an_item_to_shopcart(self):
        """It should add an item to a shopcart"""
        shopcart = self._create_shopcarts(1)[0]
        item = self._create_items(1)[0]
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items", json=item.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_read_item(self):
        """ It should return a JSON of the specified item."""
        # Create a fictional shopcart and POST it
        shopcart = self._create_shopcarts(1)[0]

        # Create items and assign them to shopcart.items
        items = self._create_items(randint(1, 5))
        shopcart.items = items

        resp = self.client.post(
            BASE_URL, json=shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # TODO(allenpthunag): we might need to fix this behaviour
        # `id` in shopcart JSON is ignored, a new id is created
        # current hack is to use the shopcart_id from server response
        shopcart_id = resp.get_json()["id"]
        for item in items:
            item.shopcart_id = shopcart_id

        # try to read an item that we created above
        item_to_read = items[randint(0, len(items) - 1)]
        resp = self.client.get(
            f"{BASE_URL}/{shopcart_id}/items/{item_to_read.id}"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json(), item_to_read.serialize())

        # try to read from a non-existing shopcart
        resp = self.client.get(
            f"{BASE_URL}/{shopcart_id + randint(5, 10)}/items/{item_to_read.id}"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        # try to read a non-existing item
        non_existing_item_id = 0
        for item in items:
            non_existing_item_id += item.id
        resp = self.client.get(
            f"{BASE_URL}/{shopcart_id}/items/{non_existing_item_id}"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_checkout_items(self):
        """ It should return a list of items for checkout, and remove them from the shopcart"""
        # Create a fictional shopcart and POST it
        shopcart = self._create_shopcarts(1)[0]

        # Create items and POST them to the shopcart
        items = self._create_items(randint(5, 10))
        for item in items:
            resp = self.client.post(
                f"{BASE_URL}/{shopcart.id}/items",
                json=item.serialize(),
                content_type="application/json"
            )

        # sample some of the items to be checked out
        items_to_checkout = sample(items, randint(1, 5))

        # prepare a dict to POST
        checkout_dict = {"items": []}
        for item in items_to_checkout:
            checkout_dict["items"].append(item.serialize())

        # try POSTing to a non-existing shopcart
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id + randint(42, 56)}/checkout",
            json=checkout_dict,
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        # try POSTing to a shopcart that does not have these items
        other_shopcart = self._create_shopcarts(1)[0]
        resp = self.client.post(
            f"{BASE_URL}/{other_shopcart.id}/checkout",
            json=checkout_dict,
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # happy path
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/checkout",
            json=checkout_dict,
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json(), checkout_dict)

        # try to checkout the same set of items again
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/checkout",
            json=checkout_dict,
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
