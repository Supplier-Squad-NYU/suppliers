"""
Supplier Store Service

Paths:
------
GET /suppliers - Returns a list all of the Suppliers
GET /suppliers/{id} - Returns the Supplier with a given id number
POST /suppliers - creates a new Supplier record in the database
PUT /suppliers/{id} - updates a Supplier record in the database
DELETE /suppliers/{id} - deletes a Supplier record in the database
"""

import json
from typing import Tuple
from flask import jsonify, Response, request, make_response
from werkzeug.exceptions import abort, BadRequest, NotFound
from service import status, app
from service.supplier import Supplier


######################################################################
# Application Routes
######################################################################
@app.route("/")
def index() -> Tuple[Response, int]:
    """ Return a message about the service """
    app.logger.info("Request for Index page")
    return app.send_static_file("index.html")


@app.route("/api/suppliers", methods=["POST"])
def create_supplier() -> Tuple[Response, int]:
    """ Create a supplier and return the supplier as a dict """
    check_content_type_is_json()
    request_body = request.json
    app.logger.info("request body: {}".format(request_body))

    if "name" not in request_body:
        raise BadRequest("missing name")

    new_supplier = Supplier.deserialize_from_dict(request_body)
    new_supplier.create()
    message = new_supplier.serialize_to_dict()

    app.logger.info("created new supplier with id {}".format(new_supplier.id))

    return make_response(jsonify(message), status.HTTP_201_CREATED)


@app.route("/api/suppliers/<int:supplier_id>", methods=["GET"])
def get_supplier(supplier_id) -> Tuple[Response, int]:
    """ Read a supplier and return the supplier as a dict """
    app.logger.info('Reads a supplier with id: {}'.format(supplier_id))
    supplier_info = {'id': supplier_id}
    supplier = Supplier.find_first(supplier_info)
    app.logger.info("Returning suppliers: %s", supplier.name)
    message = supplier.serialize_to_dict()
    return make_response(jsonify(message), status.HTTP_200_OK)


@app.route("/api/suppliers", methods=["GET"])
def get_supplier_by_attribute() -> Tuple[Response, int]:
    """ Reads suppliers satisfying required attributes
        and returns the suppliers as a dict """
    supplier_info = {}
    try:
        supplier_info['id'] = int(request.args.get('id'))
    except TypeError:
        supplier_info['id'] = None
    supplier_info['name'] = request.args.get('name')
    supplier_info['email'] = request.args.get('email')
    supplier_info['address'] = request.args.get('address')
    supplier_info['products'] = None
    try:
        supplier_info['products'] =\
            [int(x) for x in request.args.get('products').split(',')]
    except AttributeError:
        supplier_info['products'] = None

    if not any(supplier_info.values()):
        suppliers = Supplier.list()
        app.logger.info("List all {} suppliers".format(len(suppliers)))
    else:
        suppliers = Supplier.find_all(supplier_info)
        app.logger.info('Reads a supplier with {}'.
                        format(json.dumps(supplier_info)))

    message = {}
    for supplier in suppliers:
        message[supplier.id] = supplier.serialize_to_dict()
    app.logger.info("Returning supplier(s): {}".
                    format(", ".join(s.name for s in suppliers)))
    return make_response(jsonify(message), status.HTTP_200_OK)


@app.route("/api/suppliers/<int:supplier_id>", methods=["PUT"])
def update_supplier(supplier_id: int) -> Tuple[Response, int]:
    """
    Updates a supplier with the provided supplier id
    Returns the updated supplier
    """
    check_content_type_is_json()
    request_body = request.json
    app.logger.info("request body: {}".format(request_body))
    supplier_info = {'id': supplier_id}
    supplier = Supplier.find_first(supplier_info)
    supplier.update(request_body)
    message = supplier.serialize_to_dict()

    return make_response(jsonify(message), status.HTTP_200_OK)


@app.route("/api/suppliers/<int:supplier_id>/products", methods=["POST"])
def add_product(supplier_id: int) -> Tuple[Response, int]:
    """
    Adds the provided list of products to a supplier
    Returns the updated supplier
    """
    check_content_type_is_json()
    request_body = request.json
    app.logger.info("request body: {}".format(request_body))

    supplier = Supplier.find_first({'id': supplier_id})
    try:
        supplier.add_products(request_body["products"])
        message = supplier.serialize_to_dict()
        return make_response(jsonify(message), status.HTTP_200_OK)
    except KeyError:
        raise BadRequest("products not provided")


@app.route("/api/suppliers/<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id: int) -> Tuple[Response, int]:
    """
    Deletes a supplier with the provided supplier id
    Returns the deleted supplier if the supplier exists
    """
    app.logger.info("delete supplier with id {}".format(supplier_id))

    try:
        supplier = Supplier.find_first(supplier_id)
        supplier.delete()
        app.logger.info(
            "Supplier with id {} has been deleted.".format(supplier_id))
    except NotFound:
        app.logger.info(
            "Supplier with id {} does not exist.".format(supplier_id))
    finally:
        return make_response(jsonify({}), status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type_is_json():
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == "application/json":
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format("application/json"),
    )
