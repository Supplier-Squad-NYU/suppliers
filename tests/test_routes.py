# from app import app
# import json

# test_app = app.test_client()


# def test_create_happy_path():
#     response = test_app.put('/supplier',
#                             data=json.dumps({
#                                 'name': 'test',
#                                 'email': 'nice'
#                             }), content_type='application/json')
#     assert response is not None
#     assert response.status_code == 200
#     assert response.is_json
#     assert 'id' in response.json


# def test_create_no_contact():
#     response = test_app.put('/supplier',
#                             data=json.dumps({
#                                 'name': 'test',
#                             }), content_type='application/json')
#     assert response is not None
#     assert response.status_code == 400
#     assert response.is_json
#     assert 'error' in response.json


# def test_create_incorrect_data_type():
#     response = test_app.put('/supplier',
#                             data=json.dumps({
#                                 'name': 177013,
#                             }), content_type='application/json')
#     assert response is not None
#     assert response.status_code == 400
#     assert response.is_json
#     assert 'error' in response.json

import os
import logging
import unittest

# from unittest.mock import MagicMock, patch
#from urllib.parse import quote_plus
from service import status  # HTTP Status Codes
from service.supplier import db, init_db
from service.routes import app

# Disable all but ciritcal errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/suppliers"
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
