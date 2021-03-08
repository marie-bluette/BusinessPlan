from Revenue import Revenue
from Catalog import Catalog

# Todo: consolidate all classes in one file

# Timeline
TIMELINE = [
    2021, 2022, 2023, 2024, 2025
]

# Items specifications
# Todo: remove implicit objects
CATALOG_SPECIFICATIONS = [
    {'name': 'Integration Lump Sum', 'unit_price': 50000, 'unit_cost': 45000, 'unit_name': 'per project'},
    {'name': 'Monthly Licence Cost', 'unit_price': 10000, 'unit_cost': 0, 'unit_name': 'per month'},
    {'name': 'Services', 'unit_price': 850, 'unit_cost': 600, 'unit_name': 'per md'},
]

# Quantity of each item per year
# Todo: remove implicit objects
# Todo: see new model for quantities
QUANTITY = [
    {5, 10, 20, 50, 200},
    {60, 120, 240, 1200, 4800},
    {100, 500, 3000, 10000, 50000},
]

if __name__ == '__main__':
    catalog = Catalog.factory(CATALOG_SPECIFICATIONS)
    revenue = Revenue(catalog, QUANTITY)
    print('Cumulated revenues: ' + str(revenue.cumulated_revenues()))
