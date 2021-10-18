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
from models.supplier import Supplier, db
from models import app
import logging
from exceptions.supplier_exception import MissingInfo, WrongArgType
# from exceptions.supplier_exception import MissingContactInfo

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
    def test_construct_a_supplier(self):
        """Create a supplier and assert that it exists"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com")
        self.assertTrue(supplier is not None)
        self.assertEqual(supplier.id, None)
        self.assertEqual(supplier.name, "Tom")
        self.assertEqual(supplier.email, "Tom@gmail.com")
        self.assertEqual(supplier.address, None)
        self.assertEqual(supplier.products, None)
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

    def test_serialization(self):
        """Convert a supplier object to a dict object"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[1, 5])
        output = supplier.to_dict()
        another = Supplier.serialize(supplier)
        self.assertEqual(output, another)
        self.assertTrue(isinstance(output, dict))
        self.assertEqual(output["name"], "Tom")
        self.assertEqual(output["email"], "Tom@gmail.com")
        self.assertEqual(output["products"], [1, 5])

    def test_deserialization_from_dict(self):
        """Convert a dict object to supplier object"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[1, 5])
        dictionary = Supplier.serialize(supplier)
        other = Supplier.deserialize_from_dict(dictionary)
        self.assertEqual(supplier, other)

    def test_json_converter(self):
        """Convert a supplier object to JSON string and vice versas"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[1, 5])
        json_output = supplier.to_json()
        other = Supplier.deserialize_from_json(json_output)
        self.assertEqual(supplier, other)
        pass

    def test_create_suppliers(self):
        """Create a supplier and add it to the database"""
        suppliers = Supplier.all()
        self.assertEqual(suppliers, [])

        supplier = Supplier(name="Ken", email="Ken@gmail.com", products=[2, 4])
        self.assertEqual(supplier.id, None)
        supplier.create()
        self.assertEqual(supplier.id, 1)
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 1)

        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[11])
        self.assertEqual(supplier.id, None)
        supplier.create()
        self.assertEqual(supplier.id, 2)
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 2)

    '''
    def test_update_a_supplier(self):
        """Update a supplier"""
        supplier = supplierFactory()
        logging.debug(supplier)
        supplier.create()
        logging.debug(supplier)
        self.assertEqual(supplier.id, 1)
        # Change it an save it
        supplier.category = "k9"
        original_id = supplier.id
        supplier.update()
        self.assertEqual(supplier.id, original_id)
        self.assertEqual(supplier.category, "k9")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        suppliers = supplier.all()
        self.assertEqual(len(suppliers), 1)
        self.assertEqual(suppliers[0].id, 1)
        self.assertEqual(suppliers[0].category, "k9")

    def test_delete_a_supplier(self):
        """Delete a supplier"""
        supplier = supplierFactory()
        supplier.create()
        self.assertEqual(len(supplier.all()), 1)
        # delete the supplier and make sure it isn't in the database
        supplier.delete()
        self.assertEqual(len(supplier.all()), 0)

    def test_serialize_a_supplier(self):
        """Test serialization of a supplier"""
        supplier = supplierFactory()
        data = supplier.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], supplier.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], supplier.name)
        self.assertIn("category", data)
        self.assertEqual(data["category"], supplier.category)
        self.assertIn("available", data)
        self.assertEqual(data["available"], supplier.available)
        self.assertIn("gender", data)
        self.assertEqual(data["gender"], supplier.gender.name)

    def test_deserialize_a_supplier(self):
        """Test deserialization of a supplier"""
        data = {
            "id": 1,
            "name": "kitty",
            "category": "cat",
            "available": True,
            "gender": "Female",
        }
        supplier = supplier()
        supplier.deserialize(data)
        self.assertNotEqual(supplier, None)
        self.assertEqual(supplier.id, None)
        self.assertEqual(supplier.name, "kitty")
        self.assertEqual(supplier.category, "cat")
        self.assertEqual(supplier.available, True)
        self.assertEqual(supplier.gender, Gender.Female)

    def test_deserialize_missing_data(self):
        """Test deserialization of a supplier with missing data"""
        data = {"id": 1, "name": "kitty", "category": "cat"}
        supplier = supplier()
        self.assertRaises(DataValidationError, supplier.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        supplier = supplier()
        self.assertRaises(DataValidationError, supplier.deserialize, data)

    def test_deserialize_bad_available(self):
        """ Test deserialization of bad available attribute """
        test_supplier = supplierFactory()
        data = test_supplier.serialize()
        data["available"] = "true"
        supplier = supplier()
        self.assertRaises(DataValidationError, supplier.deserialize, data)

    def test_deserialize_bad_gender(self):
        """ Test deserialization of bad gender attribute """
        test_supplier = supplierFactory()
        data = test_supplier.serialize()
        data["gender"] = "male" # wrong case
        supplier = supplier()
        self.assertRaises(DataValidationError, supplier.deserialize, data)
    '''
