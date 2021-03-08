from dessia_common import DessiaObject
from CatalogItem import CatalogItem


class Catalog(DessiaObject):
    _standalone_in_db = False
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = ['name']
    _non_data_hash_attributes = ['name']

    def __init__(self, items: list[CatalogItem]):
        DessiaObject.__init__(self, items=items)
        self.items = items

    @staticmethod
    def factory(catalog_specifications: list[dict]):
        items = []
        for item in catalog_specifications:
            items.append(CatalogItem(
                item['name'],
                item['unit_price'],
                item['unit_cost'],
                item['unit_name']
            ))
        return Catalog(items)

