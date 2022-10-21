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
    location_url = url_for("get_shopcarts", shopcart_id=shopcart.id, _external=True)

    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# READ A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items", methods=["GET"])
def list_shopcart_items(shopcart_id):
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
    return (items, status.HTTP_200_OK)

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
# DELETE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["DELETE"])
def delete_shopcart(shopcart_id):
    """
    Delete a single Shopcart.
    This endpoint deletes a shopcart with a specific shopcart ID.
    If no such shopcart exists, return not found.
    """
    app.logger.info("Deleting Shopcart with id: %d", shopcart_id)
    
    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{shopcart_id}' could not be found."
        )

    shopcart.delete()
    return {}, status.HTTP_204_NO_CONTENT


######################################################################
# LIST ALL SHOPCARTS
######################################################################
@app.route("/shopcarts", methods=["GET"])
def list_all_shopcarts():
    """
    List all shopcarts.
    Returns a JSON that contains all shopcarts under the key 'shopcarts'.
    """
    shopcart = Shopcart()
    shopcarts = {"shopcarts": []}
    for sc in shopcart.all():
        shopcarts["shopcarts"].append(sc.serialize())
    app.logger.info(f"Retrieved shopcarts: {shopcarts}")

    return shopcarts, status.HTTP_200_OK


######################################################################
# UPDATE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["PUT"])
def update_shopcart(shopcart_id):
    """
    Update a shopcart with JSON request.
    Returns a 400 Error if the shopcart ID and URL does not match.
    Returns a 200 OK with the updated content if the operation is successful.
    """
    app.logger.info("Updating Shopcart with id: %d", shopcart_id)
    check_content_type("application/json")

    data = request.get_json()
    if data["id"] != shopcart_id:
        abort(
            status.HTTP_400_BAD_REQUEST,
            f"Shopcart ID in JSON ({data['id']}) does not match",
            f"the one in the request URL {shopcart_id}."
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
# RESET A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/reset", methods=["PUT"])
def reset_shopcart(shopcart_id):
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
