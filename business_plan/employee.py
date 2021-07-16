from dessia_common import DessiaObject
from typing import TypeVar, List, Dict, Union
from itertools import product, permutations
from scipy.optimize import fsolve, minimize
import random
from dectree import DecisionTree
import math
import numpy as npy
from business_plan.core import Evolution


class Employee(DessiaObject):
    _standalone_in_db = False
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = ['name']
    _non_data_hash_attributes = ['name']

    def __init__(self, profit_center: bool = False,
                 salary: float = None,
                 general_expenses: float = 0,
                 hiring_year: float = None,
                 exit_year: float = None,
                 name: str = ''):

        DessiaObject.__init__(self, name=name)
        self.exit_year = exit_year
        self.hiring_year = hiring_year
        self.general_expenses = general_expenses
        self.salary = salary
        self.profit_center = profit_center

    def cost(self, year):
        if self.exit_year is None:
            last_year = year + 1
        if year < self.hiring_year or year > last_year:
            return 0
        else:
            return self.salary + self.general_expenses

    def _cost_evolution(self, last_year):
        salary_evolution = {}
        if self.exit_year is not None:
            last_year = min(last_year, self.exit_year)
        for i in range(int(last_year - self.hiring_year) + 1):
            salary_evolution[self.hiring_year + i] = self.cost(self.hiring_year + i)
        return Evolution(salary_evolution)


class Sale(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float = None, name: str = ''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=True, hiring_year=hiring_year, name=name)


class Support(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float = None, name: str = ''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=False, hiring_year=hiring_year, name=name)


class Developer(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float = None, name: str = ''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=False, hiring_year=hiring_year, name=name)


class Manager(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float = None, name: str = ''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=False, hiring_year=hiring_year, name=name)


class EmployeeNeedRule(DessiaObject):
    _standalone_in_db = True
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = ['name']
    _non_data_hash_attributes = ['name']

    def __init__(self, if_employee: Employee,
                 number_greater_than: int,
                 then_employee: List[Union[Sale, Support, Developer, Manager]],
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.then_employee = then_employee
        self.number_greater_than = number_greater_than
        self.if_employee = if_employee


class Team(DessiaObject):
    _standalone_in_db = True
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = ['name']
    _non_data_hash_attributes = ['name']

    def __init__(self, employees: List[Union[Sale, Support, Developer, Manager]],
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.employees = employees

    @classmethod
    def generate(cls, employee_need_rules: List[EmployeeNeedRule], employees: List[Union[Sale, Support, Developer, Manager]]):
        dict_employees = {}
        for employee in employees:
            if employee.__class__ in dict_employees:
                dict_employees[employee.__class__] += 1
            else:
                dict_employees[employee.__class__] = 1
        dict_new_employees = {}
        print(dict_employees)
        for employee_class, number_employee in dict_employees.items():
            for employee_need_rule in employee_need_rules:
                if isinstance(employee_need_rule.if_employee, employee_class):
                    print('ok')
                    if number_employee >= employee_need_rule.number_greater_than:
                        new_employees = employee_need_rule.then_employee
                        for new_employee in new_employees:
                            if new_employee.__class__ in dict_new_employees:
                                dict_new_employees[new_employee.__class__] += 1
                            else:
                                dict_new_employees[new_employee.__class__] = 1

        update_employees = employees
        for employee_class, number_employee in dict_new_employees.items():
            print(employee_class)
            if str(employee_class) == str(Sale.__class__):
                update_employees.extend([Sale(40000, 10000) for i in range(number_employee)])
            if str(employee_class) == str(Support.__class__):
                update_employees.extend([Support(40000, 10000) for i in range(number_employee)])
            if str(employee_class) == str(Developer.__class__):
                update_employees.extend([Developer(40000, 10000) for i in range(number_employee)])
        return cls(update_employees)


# class TeamRule(DessiaObject):
#     _standalone_in_db = True
#     _eq_is_data_eq = True
#     _non_serializable_attributes = []
#     _non_data_eq_attributes = ['name']
#     _non_data_hash_attributes = ['name']
#
#     def __init__(self, if_employee: Employee,
#                  number_greater_than: int,
#                  then_employee: List[SubEmployee],
#                  name: str = ''):
#         DessiaObject.__init__(self, name=name)
#         self.then_employee = then_employee
#         self.number_greater_than = number_greater_than
#         self.if_employee = if_employee
#
#
# class Departement(DessiaObject):
#     _standalone_in_db = True
#     _eq_is_data_eq = True
#     _non_serializable_attributes = []
#     _non_data_eq_attributes = ['name']
#     _non_data_hash_attributes = ['name']
#
#     def __init__(self, teams: List[Team],
#                  team_rules: List[TeamRule],
#                  name: str = ''):
#         DessiaObject.__init__(self, name=name)
#         self.team_rules = team_rules
#         self.teams = teams
#
#     @classmethod
#     def generate(cls, team_rules: List[TeamRule], sub_employees: List[SubEmployee]):
