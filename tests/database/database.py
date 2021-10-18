from typing import Dict
from models.supplier import Supplier
import logging

logger = logging.getLogger(__name__)


class Database:
    '''
    Database defines access to application storage.
    Currently, this is simply in memory storage
    '''

    def __init__(self):
        '''
        Creates an instance of the Database class
        '''
        logging.info("initializing database")
        self._suppliers = {}

    def create_supplier(self, supplier: Supplier) -> Supplier:
        '''
        Inserts a new supplier into the database.
        The newly inserted supplier will be returned with the id
        appropriately set
        ----------
        supplier: Supplier
            A supplier object representing the record to insert
        '''
        logging.info("inserting supplier into database")
        new_id = len(self._suppliers) + 1
        supplier.id = new_id
        self._suppliers[new_id] = supplier
        return supplier

    @property
    def get_suppliers(self) -> Dict[int, Supplier]:
        return self._suppliers

