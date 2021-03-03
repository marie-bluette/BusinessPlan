from Revenue import Revenue
from Catalog import Catalog

TIMELINE = [
    2021, 2022, 2023, 2024, 2025
]

CATALOG_SPECIFICATIONS = [
    {'name': 'Integration Lump Sum', 'unit_price': 50000, 'unit_cost': 45000, 'unit_name': 'per project'},
    {'name': 'Monthly Licence Cost', 'unit_price': 10000, 'unit_cost': 0, 'unit_name': 'per month'},
    {'name': 'Services', 'unit_price': 850, 'unit_cost': 600, 'unit_name': 'per md'},
]

# quantity of each item per year
QUANTITY = [
    {5, 10, 20, 50, 200},
    {60, 120, 240, 1200, 4800},
    {100, 500, 3000, 10000, 50000},
]

if __name__ == '__main__':
    catalog = Catalog(CATALOG_SPECIFICATIONS)
    Revenue = Revenue(catalog, QUANTITY)

    print('Creating the catalog')
    print('Cumulated Revenues: ' + str(Revenue.cumulated_revenues()))
