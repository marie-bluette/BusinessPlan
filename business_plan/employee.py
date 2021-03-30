from dessia_common import DessiaObject
from typing import TypeVar, List, Dict
from itertools import product, permutations
from scipy.optimize import fsolve, minimize
import random
from dectree import DecisionTree
import math
import numpy as npy
from business_plan.core import Evolution


class Employee(DessiaObject):
    _standalone_in_db = True
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


class SubEmployee(DessiaObject):
    _standalone_in_db = True
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = ['name']
    _non_data_hash_attributes = ['name']

    def __init__(self, employee: Employee,
                 number: int,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.number = number
        self.employee = employee


class EmployeeNeedRule(DessiaObject):
    _standalone_in_db = True
    _eq_is_data_eq = True
    _non_serializable_attributes = []
    _non_data_eq_attributes = ['name']
    _non_data_hash_attributes = ['name']

    def __init__(self, if_employee: Employee,
                 number_greater_than: int,
                 then_employee: List[SubEmployee],
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

    def __init__(self, sub_employees: List[SubEmployee],
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.sub_employees = sub_employees

    @classmethod
    def generate(cls, employee_need_rules: List[EmployeeNeedRule], sub_employees: List[SubEmployee]):
        dict_sub_employees = {}
        for sub_employee in sub_employees:
            employee = sub_employee.employee
            number = sub_employee.number
            if employee in dict_sub_employees:
                dict_sub_employees[employee] += number
            else:
                dict_sub_employees[employee] = number
        new_sub_employees = {}
        for employee, number_employee in dict_sub_employees.items():
            for employee_need_rule in employee_need_rules:
                if isinstance(employee, employee_need_rule.if_employee):
                    if number_employee >= employee_need_rule.number_greater_than:
                        new_employees = employee_need_rule.then_employee
                        for new_employee in new_employees:
                            if new_employee.employee in new_sub_employees:
                                new_sub_employees[new_employee.employee] += new_employee.number
                            else:
                                new_sub_employees[new_employee.employee] = new_employee.number
        dict_sub_employees.update(new_sub_employees)
        new_sub_employees = [SubEmployee(k, v) for k, v in dict_sub_employees.items()]
        return cls(new_sub_employees)


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
