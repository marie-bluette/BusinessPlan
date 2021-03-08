from dessia_common import DessiaObject


class CatalogItem(DessiaObject):
    _standalone_in_db = True

    def __init__(self, name: str, unit_price: float, unit_cost: float,
                 unit_name: str):
        self.name = name
        self.unit_price = unit_price
        self.unit_cost = unit_cost
        self.unit_name = unit_name

    def revenue(self, quantity: float):
        return self.unit_price * quantity

    def cost(self, quantity):
        return self.unit_cost * quantity
