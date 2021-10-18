from database.database import Database
from models.supplier import Supplier
database = Database()


def test_create_happy_path():
    supplier = Supplier(name='test', email='test')
    updated_supplier = database.create_supplier(supplier)
    assert updated_supplier.id is not None
