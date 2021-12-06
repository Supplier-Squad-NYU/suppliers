"""
Test Factory to make fake objects for testing
"""
import random
import factory
from factory.fuzzy import FuzzyChoice
from service.supplier import Supplier


class SupplierFactory(factory.Factory):
    """Creates fake suppliers that you don't have to feed"""

    class Meta:
        model = Supplier

    id = None  # factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    email = str(name)[1:-1].replace(" ", "") + "@gmail.com"
    address = FuzzyChoice(
        choices=["New York", "Chicago", "Los Angeles", "San Francisco"])
    products = random.sample(range(1, 101), 3)
