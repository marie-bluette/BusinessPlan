

from business_plan import Catalog


class Revenue:

    def __init__(self, catalog: Catalog, quantities: list):
        self.catalog = catalog
        self.quantities = quantities

    def cumulated_revenues(self):
        revenues = 0
        for index in range(0, len(self.catalog.catalog_items)):
            for quantity in self.quantities[index]:
                revenues = revenues + self.catalog.catalog_items[index].revenue(quantity)
        return revenues

    def last_year_revenues(self):
        revenues = 0
        for index in range(0, len(self.catalog.catalog_items)):
            quantity = self.quantities[index][-1]
            revenues = revenues + self.catalog.catalog_items[index].revenue(quantity)
        return revenues


