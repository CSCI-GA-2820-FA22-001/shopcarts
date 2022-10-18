"""
My Service

Describe what your service does here
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from .common import status  # HTTP Status Codes
from service.models import Shopcart, Item, DataValidationError

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )

######################################################################
# CREATE A SHOPCART
######################################################################


@app.route("/shopcarts", methods=["POST"])
def create_shopcarts():
    """
    Creates a shopcart
    This endpoint will create a shopcart based the data in the body that is posted
    """
    app.logger.info("Request to create a Shopcart")
    check_content_type("application/json")

    # Create the account
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    shopcart.create()

    # Create a message to return
    message = shopcart.serialize()
    location_url = url_for(
        "get_shopcarts", shopcart_id=shopcart.id, _external=True)

    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# READ A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["GET"])
def get_shopcarts(shopcart_id):
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
    return make_response(jsonify(shopcart.serialize()), status.HTTP_200_OK)

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

######################################################################
# ADD AN ITEM TO SHOPCART
######################################################################


@app.route("/shopcarts/<int:shopcart_id>/items", methods=["POST"])
def add_an_item_to_shopcart(shopcart_id):
    """ Add an item to shopcart """
    app.logger.info(
        "Request to add an item to shopcart with id: %s", shopcart_id)
    check_content_type("application/json")
    item = Item()
    item.deserialize(request.get_json())
    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{shopcart_id}' could not be found.",
        )
    item.shopcart_id = shopcart_id
    shopcart.items.append(item)
    message = shopcart.serialize()
    location_url = url_for(
        "get_shopcarts", shopcart_id=shopcart.id, _external=True)
    app.logger.info(
        "Item with ID [%s] has been added to the shopcart with ID [%s]", item.id, shopcart_id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}

#############################################################s#########
# DELETE AN ITEM FROM SHOPCART
######################################################################


@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods=["DELETE"])
def delete_an_item_from_shopcart(shopcart_id, item_id):
    """ Delete an item from shopcart """
    app.logger.info(
        "Request to delete an item with ID [%s] from shopcart with ID [%s]", item_id, shopcart_id)
    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{shopcart_id}' could not be found.",
        )
    item_index = -1
    for i, item in enumerate(shopcart.items):
        if item.id == item_id:
            item_index = i
    if item_index == -1:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Item with id '{item_id}' could not be found.",
        )
    message = shopcart.items[item_index].serialize()
    del shopcart.items[item_index]
    location_url = url_for(
        "get_shopcarts", shopcart_id=shopcart_id, _external=True)
    app.logger.info(
        "Item with ID [%s] has been deleted from the shopcart with ID [%s]", item_id, shopcart_id)
    return jsonify(message), status.HTTP_204_NO_CONTENT, {"Location": location_url}
