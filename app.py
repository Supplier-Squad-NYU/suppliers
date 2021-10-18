import os
import logging
from typing import Tuple
from flask import Flask, jsonify, Response, request
from models.supplier import Supplier
from exceptions.supplier_exception import WrongArgType, MissingContactInfo
from database.database import Database

######################################################################
# Get bindings from the environment
######################################################################
DEBUG = os.getenv("DEBUG", "False") == "True"
PORT = os.getenv("PORT", "5000")


######################################################################
# Create Flask application
######################################################################
app = Flask(__name__)
if DEBUG:
    app.logger.setLevel(logging.DEBUG)
else:
    app.logger.setLevel(logging.INFO)


######################################################################
# Storage for Suppliers
######################################################################
suppliers = {}
database = Database()


######################################################################
# Application Routes
######################################################################
@app.route("/")
def index() -> Tuple[Response, int]:
    """ Returns a message about the service """
    app.logger.info("Request for Index page")
    return (
        jsonify(
            name="Supplier"
        ),
        200,
    )


@app.route("/supplier", methods=["PUT"])
def create_supplier() -> Tuple[Response, int]:
    """ Creates a supplier and returns the ID """
    request_body = request.json
    app.logger.info("request body: {}".format(request_body))
    if request_body is None:
        app.logger.info("bad request")
        return error_response("no request body", 400)
    if "name" not in request_body:
        return error_response("missing name", 400)
    new_name = request_body["name"]
    if "email" in request_body:
        email = request_body["email"]
    else:
        email = ""
    if "address" in request_body:
        address = request_body["address"]
    else:
        address = ""
    try:
        new_supplier = Supplier(
            name=new_name,
            email=email,
            address=address
        )
        created_supplier = database.create_supplier(new_supplier)
        app.logger.info(
            "created new supplier with id {}".format(created_supplier.id))
    except (MissingContactInfo, WrongArgType) as e:
        return error_response(str(e), 400)
    return jsonify(id=created_supplier.id), 200

@app.route("/supplier/<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id) -> Tuple[Response, int]:
    """Deletes a supplier"""
    app.logger.info("Deletes a supplier with id: {}".format(supplier_id))
    """Here I use the find() function implemented by Iris directly."""
    supplier = database.find(supplier_id)
    if not supplier:
        missing_msg = "Supplier with id: {} was not found".format(supplier_id)
        app.logger.info(missing_msg)
        return error_response(missing_msg, 400)
    supplier.delete()
    deleted_msg = "Supplier with id: {} was deleted".format(supplier_id)
    app.logger.info(deleted_msg)
    return Response(deleted_msg), 200

@app.route("/suppliers", methods=["GET"])
def list_all_suppliers() -> Tuple[Response, int]:
    """List all suppliers"""
    app.logger.info("List all suppliers")
    suppliers = database.get_suppliers()
    if suppliers:
        for id, supplier in suppliers:
            supplier_name = supplier.name
            supplier_email = supplier.email
            supplier_address = supplier.address
            supplier_products = supplier.products

            app.logger.info("Supplier information:" + "\nid: " + str(id) + 
            "\nname: " + supplier_name + "\nemail: " + supplier_email +
            "\naddress: " + supplier_address)
        return Response("All suppliers are listed above"), 200        
    else:
        empty_msg = "There are no suppliers"
        app.logger.info(empty_msg)
        return Response(empty_msg), 200

######################################################################
#   Convenience functions
######################################################################


def error_response(msg: str, error_code: int) -> Tuple[Response, int]:
    return jsonify(
        error=msg
    ), error_code


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    app.logger.info("*" * 70)
    app.logger.info("   Seleton Flask For Supplier   ".center(70, "*"))
    app.logger.info("*" * 70)
    app.run(host="0.0.0.0", port=int(PORT), debug=DEBUG)
