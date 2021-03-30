from dessia_common import DessiaObject
from typing import TypeVar, List, Dict
from itertools import product, permutations
from scipy.optimize import fsolve, minimize
import random
from dectree import DecisionTree
import math
import numpy as npy


class PricingFamily(DessiaObject):
    _standalone_in_db = True
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = []
    _non_data_hash_attributes = []

    def __init__(self, name: str = ''):
        DessiaObject.__init__(self, name=name)


class RecurringRevenue(DessiaObject):
    _standalone_in_db = True
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = ['name']
    _non_data_hash_attributes = ['name']

    def __init__(self, revenue_per_month: float,
                 pricing_family: PricingFamily,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.pricing_family = pricing_family
        self.revenue_per_month = revenue_per_month


class PackageFamily(DessiaObject):
    _standalone_in_db = True
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = []
    _non_data_hash_attributes = []

    def __init__(self, name: str = ''):
        DessiaObject.__init__(self, name=name)


class SubPackage(DessiaObject):
    _standalone_in_db = True
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = ['name']
    _non_data_hash_attributes = ['name']

    def __init__(self, recurring_revenue: RecurringRevenue,
                 number: int,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.recurring_revenue = recurring_revenue
        self.number = number


class Package(DessiaObject):
    _standalone_in_db = True
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = ['name']
    _non_data_hash_attributes = ['name']

    def __init__(self, sub_packages: List[SubPackage],
                 package_family: PackageFamily,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.package_family = package_family
        self.sub_packages = sub_packages
