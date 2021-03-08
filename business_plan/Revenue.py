

from business_plan import Catalog


class Revenue:

    def __init__(self, catalog: Catalog, quantities: list):
        self.catalog = catalog
        self.quantities = quantities

    # Todo: use numpy
    # Todo: UT
    def cumulated_revenues(self):
        revenues = 0
        print(self.catalog.items)
        for index in range(0, len(self.catalog.items)):
            for quantity in self.quantities[index]:
                revenues = revenues + self.catalog.items[index].revenue(quantity)
        return revenues

    # Todo: use numpy
    # Todo: UT
    def last_year_revenues(self):
        revenues = 0
        for index in range(0, len(self.catalog.items)):
            quantity = self.quantities[index][-1]
            revenues = revenues + self.catalog.items[index].revenue(quantity)
        return revenues


