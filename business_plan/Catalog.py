from dessia_common import DessiaObject
from CatalogItem import CatalogItem


class Catalog(DessiaObject):
    _standalone_in_db = False
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = ['name']
    _non_data_hash_attributes = ['name']

    def __init__(self, catalog_specifications: list):
        DessiaObject.__init__(self, catalog_specifications=catalog_specifications)
        self.catalog_items = []
        for catalog_specification in catalog_specifications:
            catalog_item = CatalogItem(
                catalog_specification['name'],
                catalog_specification['unit_price'],
                catalog_specification['unit_cost'],
                catalog_specification['unit_name']
            )
            self.catalog_items.append(catalog_item)
