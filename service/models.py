"""
Models for shopcart

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase:
    """Base class added persistent methods"""

    def __init__(self):
        self.id = None  # pylint: disable=invalid-name

    def create(self):
        """
        Creates a item/shopcart to the database
        """
        logger.info("Creating shopcart")
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a item/shopcart to the database
        """
        logger.info("Updating shopcart")
        db.session.commit()

    def delete(self):
        """Removes a Shopcart from the data store"""
        logger.info("Deleting shopcart")
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the records in the database"""
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a record by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)


######################################################################
#  I T E M   M O D E L
######################################################################
class Item(db.Model, PersistentBase):

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    shopcart_id = db.Column(db.Integer, db.ForeignKey("shopcart.id"), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(16))


    def __repr__(self):
        return f"<Item {self.name} id=[{self.id}] shopcart[{self.shopcart_id}]>"

    def serialize(self):
        """ Serializes a Item into a dictionary """
        return {"id": self.id, "shopcart_id": self.shopcart_id, "name": self.name, "price": self.price, "quantity": self.quantity, "color": self.color}

    def deserialize(self, data):
        """
        Deserializes a Item from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id = data["id"]
            self.shopcart_id = data["shopcart_id"]
            self.name = data["name"]
            self.price = data["price"]
            self.quantity = data["quantity"]
            self.color = data["color"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Item: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained bad or no data - "
                "Error message: " + error.args[0]
            )
        return self

    @classmethod
    def find_by_name(cls, name):
        """Returns all YourResourceModels with the given name

        Args:
            name (string): the name of the YourResourceModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

######################################################################
#  S H O P C A R T   M O D E L
######################################################################
class Shopcart(db.Model, PersistentBase):

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    items = db.relationship("Item", backref="shopcart", passive_deletes=True)


    def __repr__(self):
        return f"<Shopcart {self.id} customer {self.customer_id}>"

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        shopcart =  {"id": self.id, "customer_id": self.customer_id, "items": []}
        for item in self.items:
            shopcart["items"].append(item.serialize())
        return shopcart

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.customer_id = data["customer_id"]
            items_list = data.get("items")
            for json_item in items_list:
                item = Item()
                item.deserialize(json_item)
                self.items.append(item)
        except KeyError as error:
            raise DataValidationError(
                "Invalid Shopcart: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Shopcart: body of request contained bad or no data - "
                "Error message: " + error.args[0]
            )
        return self

