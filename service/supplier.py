'''
This file defines the model for Supplier
'''

import json
import logging
from typing import List, Set, Union
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from werkzeug.exceptions import NotFound
from service.supplier_exception \
    import DuplicateProduct, MissingInfo, WrongArgType, \
    UserDefinedIdError, OutOfRange


db = SQLAlchemy()
logger = logging.getLogger("flask.app")


def init_db(app):
    """Initialies the SQLAlchemy app"""
    Supplier.init_db(app)


class Supplier(db.Model):
    '''
    Supplier model that encapsulates
    necessary info about a supplier
    '''
    app: Flask = None
    __tablename__ = "supplier"
    __table_args__ = (
        db.CheckConstraint('NOT(email IS NULL AND address IS NULL)'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    email = db.Column(db.String(63), nullable=True)
    address = db.Column(db.String(63), nullable=True)
    products = db.Column(ARRAY(db.Integer), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.id is not None:
            raise UserDefinedIdError("User cannot set the value of id")
        self._check_name(self.name)
        self._check_email(self.email)
        self._check_address(self.address)
        self._check_product_ids(self.products)

        self.products = sorted(set(self.products))

        if self.email is None and self.address is None:
            raise MissingInfo("At least one contact method "
                              "(email or address) is required")

    # def __repr__(self):
    #     return "<Supplier %r, id=%s>" % (self.name, self.id)

    def __eq__(self, other):
        if not isinstance(other, Supplier):
            return False

        return self.id == other.id and \
            self.name == other.name and \
            self.email == other.email and \
            self.address == other.address and \
            self.products == other.products

    ##################################################
    # CLASS METHODS
    ##################################################
    @classmethod
    def init_db(cls, app: Flask):
        """Initializes the database session
        :param app: the Flask app
        :type data: Flask
        """
        logger.info("Initializing database")
        cls.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def list(cls) -> List["Supplier"]:
        """List all suppliers"""
        return Supplier.query.all()

    @classmethod
    def find_all(cls, supplier_info: dict) -> List["Supplier"]:
        """Finds a Supplier by it's ID
        :param supplier_id: the id of the Supplier to find
        :type supplier_id: int
        :return: an instance with the supplier_id,
                 or 404_NOT_FOUND if not found
        :rtype: Supplier
        """
        if isinstance(supplier_info, int):
            supplier_info = {'id': supplier_info}
        useless_info = []
        for k, v in supplier_info.items():
            if v is None:
                useless_info.append(k)
            elif k == 'products':
                supplier_info[k] = sorted(supplier_info[k])
        for k in useless_info:
            supplier_info.pop(k)
        # logger.info("Processing lookup or 404 for id %s ...",
        #             supplier_info['id'])  # may not have ID,
        #                                   # need other way to log
        ret = Supplier.query.filter_by(**supplier_info).all()
        if len(ret) == 0:
            raise NotFound("No results found")
        return ret

    @classmethod
    def find_first(cls, supplier_info: dict) -> "Supplier":
        """Finds a Supplier by it's ID
        :param supplier_id: the id of the Supplier to find
        :type supplier_id: int
        :return: an instance with the supplier_id,
                 or 404_NOT_FOUND if not found
        :rtype: Supplier
        """
        try:
            return Supplier.find_all(supplier_info)[0]
        except NotFound:
            raise NotFound(
                "Supplier with provided fields not found: {}".format(supplier_info))

    ##################################################
    # STATIC METHODS
    ##################################################
    @staticmethod
    def deserialize_from_dict(data: dict) -> "Supplier":
        """
        Deserializes a supplier from a dictionary
        Args:
            data (dict): A dictionary containing the supplier data
        """
        if not isinstance(data, dict):
            raise WrongArgType("<class 'dict'> expected for data, "
                               "got %s" % type(data))
        id = data["id"] if "id" in data else None
        name = data["name"] if "name" in data else None
        email = data["email"] if "email" in data else None
        address = data["address"] if "address" in data else None
        products = data["products"] if "products" in data else None
        supplier = Supplier(id=id,
                            name=name,
                            email=email,
                            address=address,
                            products=products)
        return supplier

    @staticmethod
    def deserialize_from_json(data: str) -> "Supplier":
        """
        Deserializes a supplier from a dictionary
        Args:
            data (str): A json-formatted string
        """
        if not isinstance(data, str):
            raise WrongArgType("<class 'str'> expected for data, "
                               "got %s" % type(data))
        dictionary = json.loads(data)
        return Supplier.deserialize_from_dict(dictionary)

    ##################################################
    # PUBLIC INSTANCE METHODS
    ##################################################
    def create(self):
        """
        Creates a supplier to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()

    def update(self, data: dict) -> "Supplier":
        """
        Updates self with data in dict
        Saves changes to the database
        """
        self.name = data["name"] if "name" in data else self.name
        self.email = data["email"] if "email" in data else self.email
        self.address = data["address"] if "address" in data else self.address
        self.products = data["products"] if "products" in data\
                                            else self.products

        self._check_name(self.name)
        self._check_email(self.email)
        self._check_address(self.address)
        self._check_product_ids(self.products)

        self.products = sorted(set(self.products))

        if self.email is None and self.address is None:
            raise MissingInfo("At least one contact method "
                              "(email or address) is required")
        db.session.commit()
        return self

    def delete(self) -> None:
        """
        Deletes a supplier by its id in database
        """
        db.session.delete(self)
        db.session.commit()

    def add_products(self, products: Union[List[int], Set[int]]) -> "Supplier":
        """
        Adds the list of suppliers to self and commits to database.
        Returns self
        """
        self._check_product_ids(products)
        current_products = self.products or []
        duplicates = set(current_products).intersection(set(products))

        if len(duplicates) != 0:
            raise DuplicateProduct(
                "Duplicated products: {}".format(duplicates))

        new_products = list(current_products) + list(products)
        return self.update({
            "products": new_products
        })

    def serialize_to_dict(self) -> dict:
        """Serializes a supplier into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "products": self.products,
        }

    def serialize_to_json(self) -> str:
        '''convert the supplier to JSON formatted string'''
        return json.dumps(self.serialize_to_dict(), indent=4)

    ##################################################
    # PRIVATE INSTANCE METHODS
    ##################################################
    def _check_name(self, name: str) -> None:
        '''check the type of name'''
        if name is None:
            raise MissingInfo("Supplier name is required")
        elif not isinstance(name, str):
            raise WrongArgType("class<'str'> expected for supplier name, "
                               "got %s" % type(name))

    def _check_email(self, email: str) -> None:
        '''check the type of email'''
        # email format parser may needed
        if email is not None and not isinstance(email, str):
            raise WrongArgType("<class 'str'> expected for email, "
                               "got %s" % type(email))

    def _check_address(self, address: str) -> None:
        '''check the type of address'''
        if address is not None and not isinstance(address, str):
            raise WrongArgType("<class 'str'> expected for address, "
                               "got %s" % type(address))

    def _check_product_id(self, product_id: int) -> None:
        '''check the type of product'''
        if not isinstance(product_id, int):
            raise WrongArgType("class<'int'> expected for product ID, "
                               "got %s" % type(product_id))
        elif (product_id <= 0 or product_id >= 1e15):
            raise OutOfRange("Product id is not within range (0, 1e15), "
                             "got %s" % id)
        # also need to check if product id is in db

    def _check_product_ids(self, product_ids:
                           Union[List[int], Set[int]]) -> None:
        '''check the type of product ids'''
        if product_ids is None:
            product_ids = []
            self.products = product_ids
            return
        elif not isinstance(product_ids, (List, Set)):
            raise WrongArgType("class<'List'> or class<'Set'> expected "
                               "for product ids, got %s" % type(product_ids))
        for id in product_ids:
            self._check_product_id(id)
