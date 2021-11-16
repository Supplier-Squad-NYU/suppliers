import os
import logging
import unittest


from service import status
from service.supplier import db, init_db
from service.routes import app
from .factories import SupplierFactory

# Disable all but ciritcal errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/api/suppliers"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   C A S E S
######################################################################


class TestSupplierServer(unittest.TestCase):
    """Supplier Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def _create_suppliers(self, count):
        """Factory method to create suppliers in bulk"""
        suppliers = []
        for _ in range(count):
            test_supplier = SupplierFactory()
            resp = self.app.post(
                BASE_URL, json=test_supplier.serialize_to_dict(),
                content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(resp.status_code,
                             status.HTTP_201_CREATED,
                             "Could not create test supplier")
            new_supplier = resp.get_json()
            test_supplier.id = new_supplier["id"]
            suppliers.append(test_supplier)
        return suppliers

    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_supplier(self):
        """Create a new Supplier for testing"""
        test_supplier = {
            "name": "TOM",
            "email": "a0",
            "address": "asd",
            "products": [102, 123],
        }
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Check the data is correct
        resp_supplier = resp.get_json()
        self.assertEqual(resp_supplier["name"],
                         test_supplier["name"],
                         "Names do not match")
        self.assertEqual(resp_supplier["email"],
                         test_supplier["email"],
                         "Email do not match")
        self.assertEqual(resp_supplier["address"],
                         test_supplier["address"],
                         "Address does not match")
        self.assertEqual(resp_supplier["products"],
                         test_supplier["products"],
                         "Products does not match")

    def test_create_supplier_without_name(self):
        """Create a Supplier with no name"""
        test_supplier = {
            "email": "a0@purdue.edu",
            "address": "asd",
            "products": [102, 123],
        }
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_supplier_without_content_type(self):
        """Create a Supplier with no content type"""
        resp = self.app.post(BASE_URL)
        self.assertEqual(resp.status_code,
                         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_get_supplier(self):
        """Get a single Supplier"""
        # first create a new Supplier
        test_supplier = self._create_suppliers(1)[0]
        # read the Supplier based on id
        resp = self.app.get("{}/{}".format(BASE_URL, test_supplier.id),
                            content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"],
                         test_supplier.name, "Name does not match")
        self.assertEqual(data["email"],
                         test_supplier.email, "Email does not match")
        self.assertEqual(data["address"],
                         test_supplier.address, "Address does not match")
        self.assertEqual(data["products"],
                         test_supplier.products, "Products does not match")

    def test_get_supplier_not_found(self):
        """Get a Supplier thats not found"""
        resp = self.app.get("{}/0".format(BASE_URL))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_supplier_invalid_arguments(self):
        """ Create a Supplier with a user supplied id and invalid address """
        test_supplier = {
            "email": "test@nyu.edu",
            "address": 177013,
            "name": "omg",
            "id": 2
        }
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_supplier_happy_path(self):
        """ Create a supplier and update it """

        # Create supplier
        test_supplier = {
            "name": "TOM",
            "email": "a0",
            "address": "asd",
            "products": [102, 123],
        }
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Update the fields
        test_supplier = {
            "email": "test@nyu.edu",
            "address": "omg",
        }
        logging.debug(test_supplier)
        resp = self.app.put("{}/{}".format(BASE_URL, resp.json["id"]),
                            json=test_supplier,
                            content_type=CONTENT_TYPE_JSON)
        resp = self.app.get("{}/1".format(BASE_URL))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        body = resp.json
        self.assertEqual(body["email"], "test@nyu.edu")
        self.assertEqual(body["address"], "omg")
        # Verify that the other fields have not changed
        self.assertEqual(body["name"], "TOM")
        self.assertEqual(body["products"], [102, 123])

    def test_update_supplier_does_not_exist(self):
        """ Update a supplier which does not exist """
        test_supplier = {
            "email": "test@nyu.edu",
            "address": "omg",
        }
        logging.debug(test_supplier)
        resp = self.app.put("{}/{}".format(BASE_URL, 0),
                            json=test_supplier,
                            content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_multiple_suppliers(self):
        """Get multiple suppliers with given attributes"""
        test_supplier = self._create_suppliers(3)

        test_supplier = {
            "name": "Hutao",
            "products": [2, 1, 4],
        }

        self.app.put("{}/{}".format(BASE_URL, 1),
                     json=test_supplier,
                     content_type=CONTENT_TYPE_JSON)
        self.app.put("{}/{}".format(BASE_URL, 2),
                     json=test_supplier,
                     content_type=CONTENT_TYPE_JSON)

        resp = self.app.get("{}?products=4,2,1&name=Hutao".format(BASE_URL))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data['1']['name'],
                         test_supplier['name'],
                         "Name does not match")
        self.assertEqual(data['1']["products"],
                         sorted(test_supplier['products']),
                         "Products does not match")
        self.assertEqual(data['2']['name'],
                         test_supplier['name'],
                         "Name does not match")
        self.assertEqual(data['2']["products"],
                         sorted(test_supplier['products']),
                         "Products does not match")

    def test_get_all_suppliers(self):
        """Get all suppliers"""
        self._create_suppliers(3)
        resp = self.app.get(BASE_URL)
        data = resp.get_json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 3)

    def test_all_suppliers_even_with_invalid_attributes(self):
        """Get all suppliers even with invalid attributes"""
        self._create_suppliers(3)
        resp = self.app.get("{}?country=inatsuma".format(BASE_URL))
        data = resp.get_json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 3)

    def test_get_multiple_suppliers_not_existed_attributes(self):
        """Get multiple suppliers with not exited attributes"""
        self._create_suppliers(3)
        resp = self.app.get("{}?products=1,2,3&name=Hutao".format(BASE_URL))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_product_to_supplier_happy_path(self):
        """ Tests that adding a product to a supplier works """

        # Create supplier
        test_supplier = {
            "name": "TOM",
            "email": "a0",
            "address": "asd",
            "products": [102, 123],
        }
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        to_add_products = {
            "products": [145, 1776]
        }

        # Add to the products list using the action endpoint
        resp = self.app.post(
            "{}/{}/products".format(BASE_URL, resp.json["id"]),
            json=to_add_products,
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        body = resp.json
        self.assertEqual(body["products"], [102, 123, 145, 1776])

    def test_add_product_to_supplier_duplicate_products_should_fail(self):
        """ Tests that adding a duplicate product to a supplier fails"""

        # Create supplier
        test_supplier = {
            "name": "TOM",
            "email": "a0",
            "address": "asd",
            "products": [102, 123],
        }
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        to_add_products = {
            "products": [145, 123]
        }

        # Add to the products list using the action endpoint
        resp = self.app.post(
            "{}/{}/products".format(BASE_URL, resp.json["id"]),
            json=to_add_products,
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_product_to_supplier_no_products(self):
        """ Tests that adding an empty product fails"""

        # Create supplier
        test_supplier = {
            "name": "TOM",
            "email": "a0",
            "address": "asd",
            "products": [102, 123],
        }
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        to_add_products = {
        }

        # Add to the products list using the action endpoint
        resp = self.app.post(
            "{}/{}/products".format(BASE_URL, resp.json["id"]),
            json=to_add_products,
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_product_to_supplier_does_not_exist(self):
        """ Tests that adding to a non-existent supplier fails"""

        to_add_products = {
            "products": [145, 123]
        }

        # Add to the products list using the action endpoint
        resp = self.app.post(
            "{}/{}/products".format(BASE_URL, 0),
            json=to_add_products,
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_supplier_does_not_exist(self):
        """
        Delete a supplier which does not exist
        """
        resp = self.app.delete("{}/0".format(BASE_URL))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_supplier_successful_case(self):
        """
        Delete a supplier that exists
        """

        # first create a new Supplier
        test_supplier = self._create_suppliers(1)[0]

        # verify that the test_supplier can be found before deletion
        resp = self.app.get(
            "{}/{}".format(BASE_URL, test_supplier.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_supplier.name, "Name does not match")
        self.assertEqual(data["email"], test_supplier.email, "Email does not match")
        self.assertEqual(data["address"], test_supplier.address, "Address does not match")
        self.assertEqual(data["products"], test_supplier.products, "Products does not match")

        # Delete supplier
        resp = self.app.delete("{}/{}".format(BASE_URL,test_supplier.id))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # verify that it has been deleted and cannot be found
        resp = self.app.get("{}/{}".format(BASE_URL, test_supplier.id))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        # verify that it has been deleted and it still returns 204
        resp = self.app.delete("{}/{}".format(BASE_URL,test_supplier.id))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
