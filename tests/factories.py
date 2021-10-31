"""
Test Factory to make fake objects for testing
"""
import numpy as np
import factory
from factory.fuzzy import FuzzyChoice
from service.supplier import Supplier


class SupplierFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:
        model = Supplier

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    email = str(name) + "@gmail.com"
    address = FuzzyChoice(
        choices=["New York", "Chicago", "Los Angeles", "San Francisco"])
    products = list(np.random.permutation(np.arange(1, 101))[:3])