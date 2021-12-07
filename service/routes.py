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
from flask import Response, request
from werkzeug.exceptions import abort, BadRequest
from flask_restx import Api, Resource, fields, reqparse
from service import status, app
from service.supplier import Supplier
from service.supplier_exception \
    import DuplicateProduct, MissingInfo, WrongArgType, \
    UserDefinedIdError, OutOfRange, InvalidFormat

BASE_URL = "/suppliers"


######################################################################
# Application Routes
######################################################################
@app.route("/")
def index() -> Tuple[Response, int]:
    """ Return a message about the service """
    app.logger.info("Request for Index page")
    return make_response(jsonify("Welcome to Supplier Service"), status.HTTP_200_OK)


@app.route("/api")
def index_api() -> Tuple[Response, int]:
    """ Return a message about the service """
    app.logger.info("Request for Index page")
    return app.send_static_file("index.html")

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Suppliers REST API Service',
          description='This is the Supplier service server.',
          default='suppliers',
          default_label='Supplier service operations',
          doc='/apidocs',  # default also could use doc='/apidocs/'
          prefix='/api'
         )


products_list = api.model('Products', {
    'products': fields.String(required=True, description='The products the Supplier provides')
})

# Define the model so that the docs reflect what can be sent
create_model = api.model('Supplier',
    {
        'name': fields.String(required=True,
                              description='The name of the Supplier'),
        'email': fields.String(required=True,
                               description='The email of the Supplier'),
        'address': fields.String(required=True,
                                 description='The address of the Supplier'),
        'products': fields.String(required=True, description='The products the Supplier provides')
    }
)

supplier_model = api.inherit(
    'SupplierModel',
    create_model,
    {
        'id': fields.String(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)


# query string arguments
supplier_args = reqparse.RequestParser()
supplier_args.add_argument('name', type=str, required=False, help='List Suppliers by name')
supplier_args.add_argument('email', type=str, required=False, help='List Suppliers by email')
supplier_args.add_argument('address', type=str, required=False, help='List Suppliers by address')
supplier_args.add_argument('products', type=str, required=False, help='List Suppliers by products')

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(InvalidFormat)
def request_invalidformat_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': '400 BAD REQUEST',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(DuplicateProduct)
def request_duplicateproduct_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': '400 BAD REQUEST',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(MissingInfo)
def request_missinginfo_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': '400 BAD REQUEST',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(WrongArgType)
def request_wrongargtype_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': '400 BAD REQUEST',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(UserDefinedIdError)
def request_userdefinedIderror_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': '400 BAD REQUEST',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(OutOfRange)
def request_outofrange_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': '400 BAD REQUEST',
        'message': message
    }, status.HTTP_400_BAD_REQUEST


######################################################################
#  PATH: /suppliers/{id}
######################################################################
@api.route(BASE_URL+'/<supplier_id>')
@api.param('supplier_id', 'The Supplier identifier')
class SupplierResource(Resource):
    """
    SupplierResource class

    Allows the manipulation of a single Supplier
    GET /suppliers/{id} - Returns a supplier with the id
    PUT /suppliers/{id} - Update a supplier with the id
    DELETE /suppliers/{id} -  Deletes a supplier with the id
    """

    #------------------------------------------------------------------
    # RETRIEVE A SUPPLIER
    #------------------------------------------------------------------
    @api.doc('get_suppliers')
    @api.response(404, 'Supplier Not Found')
    @api.response(400, 'Bad ID Type')
    @api.response(200, '')
    @api.marshal_with(supplier_model)
    def get(self, supplier_id) -> Tuple[Response, int]:
        """ Read a supplier and return the supplier as a dict """
        app.logger.info('Reads a supplier with id: {}'.format(supplier_id))
        supplier_info = {'id': supplier_id}
        supplier_id = convert_id_to_int(supplier_id)
        supplier = Supplier.find_first(supplier_info)
        app.logger.info("Returning suppliers: %s", supplier.name)
        message = supplier.serialize_to_dict()
        return message, status.HTTP_200_OK

    #------------------------------------------------------------------
    # UPDATE AN EXISTING SUPPLIER
    #------------------------------------------------------------------
    @api.doc('update_suppliers')
    @api.response(404, 'Supplier Not Found')
    @api.response(400, 'Invalid Attributes')
    @api.response(200, '')
    @api.expect(supplier_model)
    @api.marshal_with(supplier_model)
    def put(self, supplier_id: int) -> Tuple[Response, int]:
        """
        Updates a supplier with the provided supplier id
        Returns the updated supplier
        """
        supplier_id = convert_id_to_int(supplier_id)
        check_content_type_is_json()
        request_body = api.payload
        app.logger.info("request body: {}".format(request_body))
        supplier_info = {'id': supplier_id}
        supplier = Supplier.find_first(supplier_info)
        supplier.update(request_body)
        message = supplier.serialize_to_dict()

        return message, status.HTTP_200_OK

    #------------------------------------------------------------------
    # DELETE A SUPPLIER
    #------------------------------------------------------------------
    @api.doc('delete_suppliers')
    @api.response(204, '')
    @api.response(404, 'Supplier Already Not In DB')
    @api.response(400, 'Bad ID Type')
    def delete(self, supplier_id: int) -> Tuple[Response, int]:
        """
        Deletes a supplier with the provided supplier id
        Returns the deleted supplier if the supplier exists
        """
        supplier_id = convert_id_to_int(supplier_id)
        app.logger.info("delete supplier with id {}".format(supplier_id))
        supplier = Supplier.find_first(supplier_id)
        supplier.delete()
        app.logger.info(
            "Supplier with id {} has been deleted.".format(supplier_id))
        return {}, status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /suppliers
######################################################################
@api.route(BASE_URL, strict_slashes=False)
class SupplierCollection(Resource):
    """ Handles all interactions with collections of Suppliers """
    #------------------------------------------------------------------
    # LIST SUPPLIERS BY ATTRIBUTES
    #------------------------------------------------------------------
    @api.doc('list_suppliers_by_attributes')
    @api.expect(supplier_args, validate=True)
    @api.response(200, '')
    @api.response(404, 'Supplier Not Found')
    @api.response(400, 'Invalid Attributes')
    @api.marshal_list_with(supplier_model)
    def get(self) -> Tuple[Response, int]:
        """ Reads suppliers satisfying required attributes
            and returns the suppliers as a dict """
        supplier_info = {}
        try:
            supplier_info['id'] = request.args.get('id')
            if supplier_info['id'] is not None:
                supplier_info['id'] = int(supplier_info['id'])
        except ValueError:
            raise BadRequest('400 BAD REQUEST. Wrong ID type')
        supplier_info['name'] = request.args.get('name')
        supplier_info['email'] = request.args.get('email')
        supplier_info['address'] = request.args.get('address')
        supplier_info['products'] = None
        try:
            supplier_info['products'] = request.args.get('products')
            if supplier_info['products'] is not None:
                supplier_info['products'] =\
                    [int(x) for x in supplier_info['products'].split(',')]
        except ValueError:
            raise BadRequest('400 BAD REQUEST. Wrong Products type')
        if not any(supplier_info.values()):
            suppliers = Supplier.list()
            app.logger.info("List all {} suppliers".format(len(suppliers)))
        else:
            suppliers = Supplier.find_all(supplier_info)
            app.logger.info('Reads a supplier with {}'.
                            format(json.dumps(supplier_info)))
        message = [supplier.serialize_to_dict() for supplier in suppliers]
        app.logger.info("Returning supplier(s): {}".
                        format(", ".join(s.name for s in suppliers)))
        return message, status.HTTP_200_OK


    #------------------------------------------------------------------
    # ADD A NEW SUPPLIER
    #------------------------------------------------------------------
    @api.doc('create_suppliers')
    @api.response(201, '')
    @api.response(400, 'Invalid Attributes')
    @api.expect(create_model)
    @api.marshal_with(supplier_model, code=201)
    def post(self) -> Tuple[Response, int]:
        """ Create a supplier and return the supplier as a dict """
        check_content_type_is_json()
        request_body = api.payload
        app.logger.info("request body: {}".format(request_body))

        new_supplier = Supplier.deserialize_from_dict(request_body)
        new_supplier.create()
        message = new_supplier.serialize_to_dict()
        app.logger.info("created new supplier with id {}".format(new_supplier.id))
        return message, status.HTTP_201_CREATED

######################################################################
#  PATH: /suppliers/{id}/products
######################################################################
@api.route(BASE_URL + '/<int:supplier_id>/products')
@api.param('supplier_id', 'The Supplier identifier')
@api.expect(products_list)
class AddProductsResource(Resource):
    """ Add products to a Supplier """
    @api.doc('add_products_to_suppliers')
    @api.response(200, '')
    @api.response(404, 'Supplier Not Found')
    @api.response(400, 'Invalid products')
    def post(self, supplier_id: int) -> Tuple[Response, int]:
        """
        Adds the provided list of products to a supplier
        Returns the updated supplier
        """
        check_content_type_is_json()
        request_body = api.payload
        app.logger.info("request body: {}".format(request_body))
        supplier = Supplier.find_first({'id': supplier_id})
        try:
            supplier.add_products(request_body["products"])
            message = supplier.serialize_to_dict()
            message['products'] = '['+', '.join(str(i) for i in message['products'])+']'
            return message, status.HTTP_200_OK
        except KeyError:
            raise BadRequest("400 BAD REQUEST: products not provided")


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

def convert_id_to_int(supplier_id):
    try:
        return int(supplier_id)
    except ValueError:
        raise BadRequest("400 BAD REQUEST: id must be int")
