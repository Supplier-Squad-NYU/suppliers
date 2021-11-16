"""
Test cases for Supplier Model
Test cases can be run with:
    nosetests
    coverage report -m
While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_suppliers.py:TestSupplierModel
"""
import os
import unittest
from werkzeug.exceptions import NotFound
from service.supplier import Supplier, db
from .factories import SupplierFactory
from service import app
import logging
from service.supplier_exception \
    import MissingInfo, OutOfRange, WrongArgType,\
    UserDefinedIdError, DuplicateProduct

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  S U P P L I E R   M O D E L   T E S T   C A S E S
######################################################################
class TestSupplierModel(unittest.TestCase):
    """Test Cases for Supplier Model"""
    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Supplier.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def supplier_repr(self):
        supplier = Supplier(name='foo', address="USA")
        supplier.create()
        self.assertEqual(repr(supplier), "<Supplier foo, id=1>")

    def test_construct_a_supplier(self):
        """Create a supplier and assert that it exists"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com")
        self.assertTrue(supplier is not None)
        self.assertEqual(supplier.id, None)
        self.assertEqual(supplier.name, "Tom")
        self.assertEqual(supplier.email, "Tom@gmail.com")
        self.assertEqual(supplier.address, None)
        self.assertEqual(supplier.products, [])
        supplier = Supplier(name="Apple",
                            email="abc@apple.com",
                            products=[1, 2, 3])
        self.assertEqual(supplier.name, "Apple")
        self.assertEqual(supplier.email, "abc@apple.com")
        self.assertEqual(supplier.products, [1, 2, 3])

    def test_construct_supplier_with_insufficient_info(self):
        '''construct a supplier with insufficient info'''
        self.assertRaises(MissingInfo, Supplier, name="Tom", products=[1, 2])
        self.assertRaises(MissingInfo, Supplier, name=None, address="US")

    def test_construct_supplier_with_wrong_type_input(self):
        '''construct a supplier with input of wrong type'''
        self.assertRaises(WrongArgType, Supplier, name=1, address="US")
        self.assertRaises(WrongArgType, Supplier, name="Tom", address=1)
        self.assertRaises(WrongArgType, Supplier, name="foo", email=1)
        self.assertRaises(WrongArgType, Supplier, name="foo",
                          email="abc", products=["d"])
        self.assertRaises(WrongArgType, Supplier, name="foo",
                          email="abc", products=1)

    def test_construct_supplier_with_invalid_product_id(self):
        self.assertRaises(OutOfRange, Supplier, name="foo",
                          email="abc", products=[-2])

    def test_construct_supplier_with_user_defined_id(self):
        '''construct a supplier with user defined id'''
        self.assertRaises(UserDefinedIdError, Supplier,
                          id=2, name="Tom", address="US")

    def test_serialization_to_dict(self):
        """Convert a supplier object to a dict object"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[1, 5])
        output = supplier.serialize_to_dict()
        self.assertTrue(isinstance(output, dict))
        self.assertEqual(output["name"], "Tom")
        self.assertEqual(output["email"], "Tom@gmail.com")
        self.assertEqual(output["products"], [1, 5])

    def test_deserialization_from_dict(self):
        """Convert a dict object to a supplier object"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[1, 5])
        dictionary = supplier.serialize_to_dict()
        other = Supplier.deserialize_from_dict(dictionary)
        self.assertEqual(supplier, other)

    def test_deserialize_from_dict_missing_data(self):
        """Test deserialization from dict of a supplier with missing data"""
        data = {"address": "USA"}
        self.assertRaises(MissingInfo,
                          Supplier.deserialize_from_dict, data=data)

    def test_deserialize_from_dict_bad_data(self):
        """Test deserialization from dict of bad data"""
        data = "this is not a dictionary"
        self.assertRaises(WrongArgType,
                          Supplier.deserialize_from_dict, data=data)

    def test_deserialize_from_json_missing_data(self):
        """Test deserialization from json of a supplier with missing data"""
        json_data = "{\"name\":\"Tom\"}"
        self.assertRaises(MissingInfo,
                          Supplier.deserialize_from_json, data=json_data)

    def test_deserialize_from_json_bad_data(self):
        """Test deserialization from json of a supplier with bad data"""
        json_data = [1, 2, 3]
        self.assertRaises(WrongArgType,
                          Supplier.deserialize_from_json, data=json_data)

    def test_json_converter(self):
        """Convert a supplier object to JSON string and vice versas"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[1, 5])
        json_output = supplier.serialize_to_json()
        other = Supplier.deserialize_from_json(json_output)
        self.assertEqual(supplier, other)
        pass

    def test_create_suppliers(self):
        """Create a supplier and add it to the database"""
        suppliers = Supplier.list()
        self.assertEqual(suppliers, [])

        supplier = Supplier(name="Ken",
                            email="Ken@gmail.com", products=set([2, 4]))
        self.assertEqual(supplier.id, None)
        supplier.create()
        self.assertEqual(supplier.id, 1)
        suppliers = Supplier.list()
        self.assertEqual(len(suppliers), 1)

        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[11])
        self.assertEqual(supplier.id, None)
        supplier.create()
        self.assertEqual(supplier.id, 2)
        suppliers = Supplier.list()
        self.assertEqual(len(suppliers), 2)

    def test_find_single_supplier(self):
        """Find a Supplier by ID"""
        suppliers = SupplierFactory.create_batch(3)
        for supplier in suppliers:
            supplier.create()
        logging.debug(suppliers)
        # make sure they got saved
        self.assertEqual(len(Supplier.list()), 3)
        # find the 2nd supplier in the list
        supplier = Supplier.find_first({'id': suppliers[1].id})
        self.assertIsNot(supplier, None)
        self.assertEqual(supplier.id, suppliers[1].id)
        self.assertEqual(supplier.name, suppliers[1].name)
        self.assertEqual(supplier.email, suppliers[1].email)
        self.assertEqual(supplier.products, suppliers[1].products)

    def test_find_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Supplier.find_first, {'id': 0})

    def test_update_supplier(self):
        """
        Creates a Supplier and Update the supplier
        """
        supplier = Supplier(name="Ken",
                            email="Ken@gmail.com", products=set([2, 4]))
        supplier.create()
        supplier.update({
            "name": "Super Ken",
            "address": "super ken home"
        })
        updated_supplier = Supplier.find_first({'id': supplier.id})
        self.assertEqual(updated_supplier.name, "Super Ken")
        self.assertEqual(updated_supplier.address, "super ken home")
        self.assertEqual(updated_supplier.email, "Ken@gmail.com")

    def test_update_supplier_missing_email(self):
        """
        Update the supplier with missing data should raise exception
        """
        supplier = Supplier(name="Ken",
                            email="Ken@gmail.com", products=set([2, 4]))
        supplier.create()
        update_json = {
            "name": "Super Ken",
            "email": None
        }
        self.assertRaises(MissingInfo, supplier.update, update_json)

    def test_add_product(self):
        """
        Create a supplier and add to the product list
        """
        supplier = Supplier(name="Ken",
                            email="Ken@gmail.com", products=set([2, 4]))
        supplier.create()
        supplier.add_products([1, 3])
        updated_supplier = Supplier.find_first({'id': supplier.id})
        self.assertEqual(updated_supplier.products, sorted([2, 4, 1, 3]))
        supplier.add_products(set([5, 6]))
        updated_supplier = Supplier.find_first({'id': supplier.id})
        self.assertEqual(updated_supplier.products, sorted([2, 4, 1, 3, 5, 6]))

    def test_add_product_duplicate(self):
        """
        Create a supplier and add duplicate products.
        Assert DuplicateProduct is raised
        """
        supplier = Supplier(name="Ken",
                            email="Ken@gmail.com", products=set([2, 4]))
        supplier.create()
        self.assertRaises(DuplicateProduct, supplier.add_products, [2, 4])

    def test_add_product_none_existed(self):
        """
        Create a supplier without any products and add to it
        """
        supplier = Supplier(name="Ken",
                            email="Ken@gmail.com")
        supplier.create()
        supplier.add_products([1, 3])
        updated_supplier = Supplier.find_first(supplier.id)
        self.assertEqual(updated_supplier.products, [1, 3])

    def test_delete_supplier(self):
        """
        Creates a Supplier
        Delete the supplier
        """
        supplier = Supplier(name="Ken",
                            email="Ken@gmail.com", products=set([2, 4]))
        supplier.create()

        # Test it can be found before deletion
        supplier_to_be_deleted = Supplier.find_first(supplier.id)
        self.assertEqual(supplier_to_be_deleted.name, "Ken")
        self.assertEqual(supplier_to_be_deleted.email, "Ken@gmail.com")

        # Test it cannot be found after deletion
        supplier.delete()
        self.assertRaises(NotFound, Supplier.find_first, 0)
