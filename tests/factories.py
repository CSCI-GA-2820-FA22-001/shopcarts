import factory
from factory.fuzzy import FuzzyChoice
from service.models import Shopcart, Item

class ItemFactory(factory.Factory):
    """ Creates fake items  """

    class Meta:
        model = Item

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["laptop", "monitor", "desk", "mouse","pc"])
    quantity = FuzzyChoice(choices=[2,3,5,8,1])
    price = FuzzyChoice(choices=[10,15.46,17.51,199999.2,663,2183])
    color = FuzzyChoice(choices=["red", "yellow", "green"])

class ShopcartFactory(factory.Factory):
    """ Creates fake Shopcarts """

    class Meta:
        model = Shopcart

    customer_id = FuzzyChoice(choices=[1, 5, 15, 20, 35, 68])