"""
Test cases for Shopcart Model

"""
import os
import logging
import unittest
from service.models import Shopcart, Item, DataValidationError, db
from tests.factories import ShopcartFactory, ItemFactory
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  S H O P C A R T   M O D E L   T E S T   C A S E S
######################################################################


class TestShopcart(unittest.TestCase):
    """ Test Cases for Shopcart Model """

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

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_XXXX(self):
        """ It should always be true """
        self.assertTrue(True)

    def test_create_a_shopcart(self):
        """It should Create a Shopcart and assert that it exists """
        fake_shopcart = ShopcartFactory()
        shopcart = Shopcart(
            id=fake_shopcart.id,
            customer_id=fake_shopcart.customer_id,
        )
        self.assertIsNotNone(shopcart)
        self.assertEqual(shopcart.id, fake_shopcart.id)
        self.assertEqual(shopcart.customer_id, fake_shopcart.customer_id)

    def test_add_a_shopcart(self):
        """It should Create an shopcart and add it to the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = ShopcartFactory()
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

    def test_read_shopcart(self):
        """It should Read an shopcart"""
        shopcart = ShopcartFactory()
        shopcart.create()

        # Read it back
        found_shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(found_shopcart.id, shopcart.id)
        self.assertEqual(found_shopcart.customer_id, shopcart.customer_id)
        self.assertEqual(found_shopcart.items, [])

    def test_update_shopcart(self):
        """It should Update an shopcart"""
        shopcart = ShopcartFactory(customer_id=1111)
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        self.assertEqual(shopcart.customer_id, 1111)

        # Fetch it back
        shopcart = Shopcart.find(shopcart.id)
        shopcart.customer_id = 1234
        shopcart.update()

        # Fetch it back again
        shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(shopcart.customer_id, 1234)

    def test_delete_an_shopcart(self):
        """It should Delete an shopcart from the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = ShopcartFactory()
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)
        shopcart = shopcarts[0]
        shopcart.delete()
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 0)

    def test_list_all_shopcarts(self):
        """It should List all Shopcarts in the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        for shopcart in ShopcartFactory.create_batch(5):
            shopcart.create()
        # Assert that there are not 5 shopcarts in the database
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 5)
        
    def test_serialize_an_shopcart(self):
        """It should Serialize an shopcart"""
        shopcart = ShopcartFactory()
        item = ItemFactory()
        shopcart.items.append(item)
        serial_shopcart = shopcart.serialize()
        self.assertEqual(serial_shopcart["id"], shopcart.id)
        self.assertEqual(serial_shopcart["customer_id"], shopcart.customer_id)
        self.assertEqual(len(serial_shopcart["items"]), 1)
        items = serial_shopcart["items"]
        self.assertEqual(items[0]["id"], item.id)
        self.assertEqual(items[0]["shopcart_id"], item.shopcart_id)
        self.assertEqual(items[0]["name"], item.name)
        self.assertEqual(items[0]["price"], item.price)
        self.assertEqual(items[0]["quantity"], item.quantity)
        self.assertEqual(items[0]["color"], item.color)

    def test_deserialize_an_shopcart(self):
        """It should Deserialize an shopcart"""
        shopcart = ShopcartFactory()
        shopcart.items.append(ItemFactory())
        shopcart.create()
        serial_shopcart = shopcart.serialize()
        new_shopcart = Shopcart()
        new_shopcart.deserialize(serial_shopcart)
        self.assertEqual(new_shopcart.customer_id, shopcart.customer_id)

    def test_deserialize_with_key_error(self):
        """It should not Deserialize an shopcart with a KeyError"""
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize an shopcart with a TypeError"""
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, [])

    def test_deserialize_item_key_error(self):
        """It should not Deserialize an item with a KeyError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_item_type_error(self):
        """It should not Deserialize an item with a TypeError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])

    def test_add_shopcart_item(self):
        """It should Create an shopcart with an item and add it to the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = ShopcartFactory()
        item = ItemFactory(shopcart=shopcart)
        shopcart.items.append(item)
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        new_shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(new_shopcart.items[0].name, item.name)

        item2 = ItemFactory(shopcart=shopcart)
        shopcart.items.append(item2)
        shopcart.update()

        new_shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(len(new_shopcart.items), 2)
        self.assertEqual(new_shopcart.items[1].name, item2.name)

    def test_update_shopcart_item(self):
        """It should Update an shopcarts item"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])

        shopcart = ShopcartFactory()
        item = ItemFactory(shopcart=shopcart)
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        # Fetch it back
        shopcart = Shopcart.find(shopcart.id)
        old_item = shopcart.items[0]
        print("%r", old_item)
        self.assertEqual(old_item.quantity, item.quantity)
        # Change the quantity
        old_item.quantity = 111
        shopcart.update()

        # Fetch it back again
        shopcart = Shopcart.find(shopcart.id)
        item = shopcart.items[0]
        self.assertEqual(item.quantity, 111)

    def test_delete_shopcart_item(self):
        """It should Delete an shopcarts item"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])

        shopcart = ShopcartFactory()
        item = ItemFactory(shopcart=shopcart)
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        # Fetch it back
        shopcart = Shopcart.find(shopcart.id)
        item = shopcart.items[0]
        item.delete()
        shopcart.update()

        # Fetch it back again
        shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(len(shopcart.items), 0)

    def test_find_by_shopcart_id_and_customer_id(self):
        """It should Find Shopcarts by shopcart_id and customer_id"""
        shopcart = ShopcartFactory()
        shopcart.create()

        same_shopcart = Shopcart.find_by_shopcart_id_and_customer_id(shopcart.id, shopcart.customer_id)[0]
        self.assertEqual(shopcart.id, same_shopcart.id)
        self.assertEqual(shopcart.customer_id, same_shopcart.customer_id)

    def test_find_by_shopcart_id(self):
        """It should Find Shopcarts by shopcart_id"""
        shopcart = ShopcartFactory()
        shopcart.create()

        same_shopcart = Shopcart.find_by_shopcart_id(shopcart.id)[0]
        self.assertEqual(shopcart.id, same_shopcart.id)

    def test_find_by_customer_id(self):
        """It should Find Shopcarts by customer_id"""
        shopcart = ShopcartFactory()
        shopcart.create()

        same_shopcart = Shopcart.find_by_customer_id(shopcart.customer_id)[0]
        self.assertEqual(shopcart.customer_id, same_shopcart.customer_id)
