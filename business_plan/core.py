
from dessia_common import DessiaObject
from typing import TypeVar, List


class Employee(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, value_creation: float=None,
                 value_improve: float=None,
                 value_sale: float=None,
                 name:str=''):
        self.value_sale = value_sale
        self.value_improve = value_improve
        self.value_creation = value_creation
        DessiaObject.__init__(self, name=name)

class EmployeeMaker(Employee):
    def __init__(self, value_creation: float, name:str=''):
        Employee.__init__(self,value_creation=value_creation, name=name)

class EmployeeSeller(Employee):
    def __init__(self, value_sale: float, name: str = ''):
        Employee.__init__(self, value_sale=value_sale, name=name)

class EmployeeTalker(Employee):
    def __init__(self, value_improve: float, name: str = ''):
        Employee.__init__(self, value_improve=value_improve, name=name)

class EmployeeManager(Employee):
    def __init__(self, name: str = ''):
        Employee.__init__(self, name=name)

class Country(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, market_size: float,
                 market_maturity: float,
                 name:str=''):
        DessiaObject.__init__(self, name=name)
        self.market_maturity = market_maturity
        self.market_size = market_size


