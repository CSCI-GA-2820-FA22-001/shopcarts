"""
My Service

Describe what your service does here
"""

from flask import jsonify, request
from flask_restx import Resource, fields, reqparse
from .common import status  # HTTP Status Codes
from service.models import Shopcart, Item

# Import Flask application
from . import app, api


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return app.send_static_file("index.html")


item_model = api.model('Item', {
    'id': fields.Integer(required=True, description='The id of the item'),
    'shopcart_id': fields.Integer(required=True, description='The id of the shopcart that contains the item'),
    'name': fields.String(required=True, description='The name of the item'),
    'price': fields.Float(required=True, description='The price of the item'),
    'quantity': fields.Integer(required=True, description='The quantity of the item'),
    'color': fields.String(required=True, description='The color of the item'),
})

# Define the model so that the docs reflect what can be sent
create_shopcart_model = api.model('Shopcart', {
    'customer_id': fields.Integer(required=True, description='The customer id of the Shopcart'),
    'items': fields.List(fields.Nested(item_model), required=True, description='The item list of the Shopcart'),
    },
)

shopcart_model = api.inherit(
    'ShopcartModel',
    create_shopcart_model,
    {
        'id': fields.Integer(
            readOnly=True, description='The unique id assigned internally by service'
        ),
    }
)

shopcart_args = reqparse.RequestParser()
shopcart_args.add_argument('shopcart_id', type=int, location='args', required=False, help='List Shopcarts by shopcart id')
shopcart_args.add_argument('customer_id', type=int, location='args', required=False, help='List Shopcarts by customer id')


######################################################################
#  PATH: /shopcarts
######################################################################
@api.route('/shopcarts', strict_slashes=False)
class ShopcartCollection(Resource):
    """ Handles all interactions with collections of Shopcarts """
    ######################################################################
    # CREATE A SHOPCART
    ######################################################################
    @api.doc('create_shopcarts')
    @api.response(415, 'The posted data was not valid')
    @api.expect(create_shopcart_model)
    @api.marshal_with(shopcart_model, code=201)
    def post(self):
        """
        Creates a shopcart
        This endpoint will create a shopcart based the data in the body that is posted
        """
        app.logger.info("Request to create a Shopcart")
        check_content_type("application/json")

        # Create the account
        shopcart = Shopcart()
        shopcart.deserialize(api.payload)
        shopcart.create()

        # Create a message to return
        message = shopcart.serialize()
        location_url = api.url_for(
            ShopcartResource, shopcart_id=shopcart.id, _external=True)

        return message, status.HTTP_201_CREATED, {"Location": location_url}

    ######################################################################
    # LIST ALL SHOPCARTS
    ######################################################################
    @api.doc('list_shopcarts')
    @api.expect(shopcart_args, validate=True)
    @api.response(404, 'No shopcart found')
    @api.marshal_list_with(shopcart_model)
    def get(self):
        """
        List all shopcarts.
        Returns a JSON that contains all shopcarts under the key 'shopcarts'.
        """
        shopcarts = []

        args = shopcart_args.parse_args()
        arg_shopcart_id = args['shopcart_id']
        arg_customer_id = args['customer_id']

        if arg_shopcart_id and arg_customer_id:
            shopcarts = Shopcart.find_by_shopcart_id_and_customer_id(arg_shopcart_id, arg_customer_id)
            app.logger.info(f"Retrieved shopcarts with specific id: {shopcarts}")
        elif arg_shopcart_id:
            shopcarts = Shopcart.find_by_shopcart_id(arg_shopcart_id)
            app.logger.info(f"Retrieved shopcarts with specific id: {shopcarts}")
        elif arg_customer_id:
            shopcarts = Shopcart.find_by_customer_id(arg_customer_id)
            app.logger.info(f"Retrieved shopcarts with specific customer_id: {shopcarts}")
        else:
            shopcarts = Shopcart.all()
            app.logger.info(f"Retrieved shopcarts: {shopcarts}")

        results = [shopcart.serialize() for shopcart in shopcarts]
        return results, status.HTTP_200_OK


######################################################################
#  PATH: /shopcarts/<shopcart_id>
######################################################################
@api.route('/shopcarts/<int:shopcart_id>', strict_slashes=False)
@api.param('shopcart_id', 'The Shopcart identifier')
class ShopcartResource(Resource):
    """
    ShopcartResource class

    Allows the manipulation of a single Shopcart
    GET /shopcarts/<shopcart_id> - Returns a Shopcart with the id
    PUT /shopcarts/<shopcart_id>} - Update a Shopcart with the id
    DELETE /shopcarts/<shopcart_id> -  Deletes a Shopcart with the id
    """
    ######################################################################
    # READ A SHOPCART
    ######################################################################
    @api.doc('get_shopcarts')
    @api.response(404, 'Shopcart not found')
    @api.marshal_with(shopcart_model)
    def get(self, shopcart_id):
        """
        Retrieve a single Shopcart

        This endpoint will return a Shopcart based on it's id
        """
        app.logger.info("Request for Shopcart with id: %s", shopcart_id)

        shopcart = Shopcart.find(shopcart_id)
        if not shopcart:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Shopcart with id '{shopcart_id}' could not be found.",
            )
        return shopcart.serialize(), status.HTTP_200_OK

    ######################################################################
    # DELETE A SHOPCART
    ######################################################################
    @api.doc('delete_shopcarts')
    @api.response(204, 'Shopcart deleted')
    def delete(self, shopcart_id):
        """
        Delete a single Shopcart.
        This endpoint deletes a shopcart with a specific shopcart ID.
        If no such shopcart exists, return HTTP_204_NO_CONTENT.
        """
        app.logger.info("Deleting Shopcart with id: %d", shopcart_id)

        shopcart = Shopcart.find(shopcart_id)
        if shopcart:
            for item in shopcart.items:
                item.delete()
            shopcart.delete()

        return '', status.HTTP_204_NO_CONTENT

    ######################################################################
    # UPDATE A SHOPCART
    ######################################################################
    @api.doc('update_shopcarts')
    @api.response(404, 'Shopcart not found')
    @api.response(400, 'The posted data was not valid')
    @api.response(415, 'The posted data was not valid')
    @api.expect(shopcart_model)
    @api.marshal_with(shopcart_model)
    def put(self, shopcart_id):
        """
        Update a shopcart with JSON request.
        Returns a 400 Error if the shopcart ID and URL does not match.
        Returns a 200 OK with the updated content if the operation is successful.
        """
        app.logger.info("Updating Shopcart with id: %d", shopcart_id)

        check_content_type("application/json")

        data = api.payload
        if data["id"] != shopcart_id:
            abort(
                status.HTTP_400_BAD_REQUEST,
                f"Shopcart ID in JSON ({data['id']}) does not match the one in the request URL {shopcart_id}."
            )

        shopcart = Shopcart.find(shopcart_id)
        if not shopcart:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Shopcart with id '{shopcart_id}' could not be found."
            )
        shopcart.deserialize(data)
        shopcart.update()
        return shopcart.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /shopcarts/<shopcart_id>/items
######################################################################
@api.route('/shopcarts/<int:shopcart_id>/items', strict_slashes=False)
@api.param('shopcart_id', 'The shopcart identifier')
class ItemCollection(Resource):
    """ Handles all interactions with collections of items """
    ######################################################################
    # READ ITEMS FROM A SHOPCART
    ######################################################################
    @api.doc('get_items')
    @api.response(404, 'items not found')
    def get(self, shopcart_id):
        """
        List all items in a Shopcart

        This endpoint will return a Item list based on the Shopcart id
        """
        app.logger.info("Request for items in Shopcart with id: %s", shopcart_id)

        shopcart = Shopcart.find(shopcart_id)
        if not shopcart:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Shopcart with id '{shopcart_id}' could not be found.",
            )
        items = {"items": []}
        for item in shopcart.items:
            items["items"].append(item.serialize())
        return items, status.HTTP_200_OK

    ######################################################################
    # ADD AN ITEM TO SHOPCART
    ######################################################################
    @api.doc('create_items')
    @api.response(400, 'The posted data was not valid')
    @api.response(415, 'The posted data was not valid')
    @api.expect(item_model)
    @api.marshal_with(item_model, code=201)
    def post(self, shopcart_id):
        """ Add an item to shopcart """
        app.logger.info(
            "Request to add an item to shopcart with id: %s", shopcart_id)
        check_content_type("application/json")
        shopcart = Shopcart.find(shopcart_id)
        if not shopcart:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Shopcart with id '{shopcart_id}' could not be found.",
            )
        # temp_item is the data in request
        temp_item = api.payload
        item = Item.find(temp_item["id"])
        if item:
            item.quantity += temp_item["quantity"]
        else:
            item = Item()
            temp_item["shopcart_id"] = shopcart_id
            item.deserialize(temp_item)
            shopcart.items.append(item)
        shopcart.update()
        message = item.serialize()
        location_url = api.url_for(
            ShopcartResource, shopcart_id=shopcart.id, _external=True)
        app.logger.info(
            "Item with ID [%s] has been added to the shopcart with ID [%s]", item.id, shopcart_id)
        return message, status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /shopcarts/<shopcart_id>/items/<item_id>
######################################################################
@api.route('/shopcarts/<int:shopcart_id>/items/<int:item_id>', strict_slashes=False)
@api.param('shopcart_id', 'The Shopcart identifier')
@api.param('item_id', 'The Item identifier')
class ItemResource(Resource):
    """
    ItemResource class

    Allows the manipulation of a single Item
    GET /shopcarts/<shopcart_id>/items/<item_id> - Returns an Item with the id
    PUT /shopcarts/<shopcart_id>/items/<item_id> - Update an Item with the id
    DELETE /shopcarts/<shopcart_id>/items/<item_id> -  Deletes an Item with the id
    """
    ######################################################################
    # READ AN ITEM FROM A SHOPCART
    ######################################################################
    @api.doc('get_items')
    @api.response(404, 'Item not found')
    @api.marshal_with(item_model)
    def get(self, shopcart_id, item_id):
        """
        Read an item from a shopcart.
        Returns JSON of the item if it exists and the shopcart exists.
        Returns a 404 Error if either of the item or the shopcart does not exist.
        """
        app.logger.info("Reading Item %d from Shopcart %d", item_id, shopcart_id)

        shopcart = Shopcart.find(shopcart_id)
        if not shopcart:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Shopcart with id '{shopcart_id}' could not be found."
            )

        app.logger.info("item_id: %d, shopcart id: %d", item_id, shopcart_id)
        for item in shopcart.items:
            if item.id == item_id:
                return item.serialize(), status.HTTP_200_OK

        return "Item not found", status.HTTP_404_NOT_FOUND

    ######################################################################
    # DELETE AN ITEM FROM SHOPCART
    ######################################################################
    @api.doc('delete_items')
    @api.response(204, 'Item deleted')
    @api.response(404, 'Item not found')
    def delete(self, shopcart_id, item_id):
        """ Delete an item from shopcart """
        app.logger.info(
            "Request to delete an item with ID [%s] from shopcart with ID [%s]", item_id, shopcart_id)
        item = Item.find(item_id)
        if not item:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Item with id '{item_id}' could not be found.",
            )
        item.delete()
        return '', status.HTTP_204_NO_CONTENT

    ######################################################################
    # UPDATE AN ITEM IN SHOPCART
    ######################################################################
    @api.doc('update_items')
    @api.response(404, 'Shopcart not found')
    @api.response(400, 'The posted Item data was not valid')
    @api.response(415, 'The posted data was not valid')
    @api.expect(item_model)
    @api.marshal_with(shopcart_model)
    def put(self, shopcart_id, item_id):
        """
        Update an item{item_id} in a certain shopcart{shopcart_id}.
        This endpoint will update an item based on the shopcart_id and item_id argument in the url
        """
        app.logger.info("Request to update an item")
        check_content_type("application/json")

        req = api.payload
        if not "quantity" in req.keys() and not "price" in req.keys():
            abort(status.HTTP_400_BAD_REQUEST, "Must have either quantity or price.")
        quantity = None
        price = None
        if "quantity" in req.keys():
            if not isinstance(req["quantity"], int) or req["quantity"] <= 0:
                abort(status.HTTP_400_BAD_REQUEST, "Invalid quantity.")
            else:
                quantity = req["quantity"]
        if "price" in req.keys():
            if (not isinstance(req["price"], int)
                    and not isinstance(req["price"], float)) or req["price"] < 0:
                abort(status.HTTP_400_BAD_REQUEST, "Invalid price.")
            else:
                price = req["price"]

        # Make sure the shopcart exists
        shopcart = Shopcart.find(shopcart_id)
        if not shopcart:
            abort(status.HTTP_404_NOT_FOUND, f"Shopcart with id {shopcart_id} was not found.")
        item_index = -1
        # Make sure the item exists
        for i, item in enumerate(shopcart.items):
            if item.id == item_id:
                item_index = i
                # Now proceed to update
                if quantity:
                    item.quantity = quantity
                    app.logger.info(f"item {item_id}'s quantity is changed to {quantity}")
                if price is not None and price >= 0:
                    item.price = price
                    app.logger.info(f"item {item_id}'s price is changed to {price}")
                shopcart.update()
                return shopcart.serialize(), status.HTTP_200_OK

        if item_index == -1:
            abort(status.HTTP_404_NOT_FOUND, f"item with id {item_id} was not found.")

######################################################################
# Health Endpoint for Kubernete
######################################################################
@app.route("/health", methods=["GET"])
def check_health():
    """ The health endpoint for Kubernetes """
    return jsonify(status="OK"), status.HTTP_200_OK

######################################################################
#  PATH: /shopcarts/<shopcart_id>/reset
######################################################################
@api.route('/shopcarts/<int:shopcart_id>/reset', strict_slashes=False)
@api.param('shopcart_id', 'The Shopcart identifier')
class ShopcartReset(Resource):
    ##########å############################################################
    # RESET A SHOPCART
    ######################################################################
    @api.doc('reset_shopcarts')
    @api.response(404, 'Shopcart not found')
    @api.expect(shopcart_model)
    @api.marshal_with(shopcart_model)
    def put(self, shopcart_id):
        """
        Reset a shopcart.
        Returns a 404 Error if the shopcart does not exist.
        Returns a 200 OK with the updated content if the operation is successful.
        """
        app.logger.info("Resetting Shopcart with id: %d", shopcart_id)

        shopcart = Shopcart.find(shopcart_id)
        if not shopcart:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Shopcart with id '{shopcart_id}' could not be found."
            )
        shopcart.items.clear()
        shopcart.update()
        return shopcart.serialize(), status.HTTP_200_OK

######################################################################
#  PATH: /shopcarts/<shopcart_id>/checkout
######################################################################
@api.route('/shopcarts/<int:shopcart_id>/checkout', strict_slashes=False)
@api.param('shopcart_id', 'The Shopcart identifier')
class ShopcartCheckout(Resource):
    ######################################################################
    # CHECKOUT ITEMS FROM A SHOPCART
    ######################################################################
    @api.doc('checkout_items')
    @api.response(404, 'shopcart or item could not be found')
    @api.response(403, 'item does not belong to this shopcart')
    @api.expect(shopcart_model)
    def post(self, shopcart_id):
        """
        Checkout selected items in a shopcart.
        Returns JSON of a list of selected items; remove these items from shopcart.
        Returns a 404 Error if any item is not in the item list of the shopcart.
        Returns a 404 Error if the shopcart does not exist.
        """
        app.logger.info("Checking out items from Shopcart %d", shopcart_id)

        shopcart = Shopcart.find(shopcart_id)
        if not shopcart:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Shopcart with id '{shopcart_id}' could not be found."
            )
        
        items_to_checkout = api.payload["items"]
        for item in items_to_checkout:
            item_looked_up = Item.find(item["id"])
            if not item_looked_up:
                abort(
                    status.HTTP_404_NOT_FOUND,
                    f"item with id {item['id']} could not be found."
                )
            elif item_looked_up.shopcart_id != shopcart_id:
                abort(
                    status.HTTP_403_FORBIDDEN,
                    f"item with id {item['id']} does not belong to shopcart"
                    + f" with id {shopcart_id}."
                )
            else:
                item_looked_up.delete()

        return api.payload, status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Shopcart.init_db(app)

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )

def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)
