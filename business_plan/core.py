
from dessia_common import DessiaObject
from typing import TypeVar, List, Dict


class Employee(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, profit_center: bool=False,
                 salary: float=None,
                 general_expenses: float=0,

                 name:str=''):

        DessiaObject.__init__(self, name=name)
        self.general_expenses = general_expenses
        self.salary = salary
        self.profit_center = profit_center

class Revenue(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, revenues: Dict[int, float],
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.revenues = revenues

    def __add__(self, other_revenue):
        year1

class MainDivision(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, asset_improve: float,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.asset_improve = asset_improve

class GeographicArea(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, market_size: float,
                 market_maturity: float,
                 market_access_cost: float,
                 market_penetration: float,
                 percentage_profit_center: float,
                 percentage_cost_center: float,
                 name:str=''):
        DessiaObject.__init__(self, name=name)
        self.percentage_cost_center = percentage_cost_center
        self.percentage_profit_center = percentage_profit_center
        self.market_penetration = market_penetration
        self.market_access_cost = market_access_cost
        self.market_maturity = market_maturity
        self.market_size = market_size

class OperatingDivision(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, geographic_area: GeographicArea,
                 revenue: Revenue,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.revenue = revenue
        self.geographic_area = geographic_area

class MainRevenue(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, operating_divisions: List[OperatingDivision],
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.operating_divisions = operating_divisions

    def revenue(self):
        revenue = Revenue(0, 0)
        for operating_division in self.operating_divisions:
            revenue += operating_division.revenue
        return revenue
