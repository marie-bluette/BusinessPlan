
from dessia_common import DessiaObject
from typing import TypeVar, List, Dict
from itertools import product
from scipy.optimize import fsolve, minimize
import random
from dectree import DecisionTree
import math
import numpy as npy


class Employee(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, profit_center: bool=False,
                 salary: float=None,
                 general_expenses: float=0,
                 hiring_year: float=None,
                 exit_year: float=None,
                 name:str=''):

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

class EmployeeSale(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float=None, name:str=''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=True, hiring_year=hiring_year, name=name)

class EmployeeSupport(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float=None, name:str=''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=False, hiring_year=hiring_year, name=name)

class EmployeeTalker(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float=None, name:str=''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=False, hiring_year=hiring_year, name=name)

class EmployeeMaker(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float=None, name:str=''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=False, hiring_year=hiring_year, name=name)

class Evolution(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, evolutions: Dict[int, float]=None,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        if evolutions is None:
            self.evolutions = {}
        else:
            self.evolutions = evolutions

    def __add__(self, other_evolution):
        year1 = list(self.evolutions.keys())
        year2 = list(other_evolution.evolutions.keys())
        all_year = year1
        for y in year2:
            if y not in all_year:
                all_year.append(y)
        evolutions = {}
        for y in all_year:
            evolutions[y] = 0
            if y in self.evolutions:
                evolutions[y] += self.evolutions[y]
            if y in other_evolution.evolutions:
                evolutions[y] += other_evolution.evolutions[y]
        return Evolution(evolutions=evolutions, name=self.name)

    def min(self):
        return min(list(self.evolutions.keys()))

    def max(self):
        return max(list(self.evolutions.keys()))

    def cumulative(self):
        return sum([e for e in self.evolutions.values()])

    def update(self, evolutions):
        self.evolutions = evolutions

    def cut(self, last_year, copy=False):
        evol = {k:v for k, v in self.evolutions.items() if k <= last_year}
        if copy:
            return Evolution(evol, self.name)
        else:
            self.evolutions = evol

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
                 sale_annual_package: float,
                 support_annual_package: float,
                 hiring_cost: float,
                 name:str=''):
        DessiaObject.__init__(self, name=name)
        self.hiring_cost = hiring_cost
        self.support_annual_package = support_annual_package
        self.sale_annual_package = sale_annual_package
        self.percentage_cost_center = percentage_cost_center
        self.percentage_profit_center = percentage_profit_center
        self.market_penetration = market_penetration
        self.market_access_cost = market_access_cost
        self.market_maturity = market_maturity
        self.market_size = market_size

    def number_sales(self, value_revenue):
        return max(1, int(self.percentage_profit_center*value_revenue))

    def number_supports(self, value_revenue):
        return max(1, int(self.percentage_cost_center*value_revenue))


class OperatingDivision(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, geographic_area: GeographicArea,
                 revenue: Evolution,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.revenue = revenue
        self.geographic_area = geographic_area

        self.sales, self.supports = self.generate_employees()

    def generate_employees(self):
        years = list(self.revenue.evolutions.keys())
        years.sort()
        sales = []
        supports = []
        for y in years:
            value_revenue = self.revenue.evolutions[y]
            ga = self.geographic_area

            number_sales = ga.number_sales(value_revenue)
            number_sales_m = 0
            for s in sales:
                if s.exit_year is None:
                    number_sales_m += 1
            if number_sales_m < number_sales:
                sales.extend([EmployeeSale(salary=ga.sale_annual_package,
                                           general_expenses=0, hiring_year=y) for i in range(number_sales-number_sales_m)])
            elif number_sales_m > number_sales:
                number_exit = number_sales_m - number_sales
                n = 0
                for s in sales:
                    if s.exit_year is None:
                        s.exit_year = y
                        n += 1
                    if n == number_exit:
                        break

            number_support = ga.number_supports(value_revenue)
            number_supports_m = 0
            for s in supports:
                if s.exit_year is None:
                    number_supports_m += 1
            if number_supports_m < number_support:
                supports.extend([EmployeeSupport(salary=ga.support_annual_package,
                                                 general_expenses=0, hiring_year=y) for i in range(number_support-number_supports_m)])
            elif number_supports_m > number_support:
                number_exit = number_supports_m - number_support
                n = 0
                for s in supports:
                    if s.exit_year is None:
                        s.exit_year = y
                        n += 1
                    if n == number_exit:
                        break
        return sales, supports

    def generate_costs(self, last_year):
        costs = Evolution()
        for sale in self.sales:
            costs += sale._cost_evolution(last_year)
        for support in self.supports:
            costs += support._cost_evolution(last_year)
        return costs

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

    def __str__(self):
        last_year = self.last_year()
        costs = self.cost(last_year)
        margin = self.margin(last_year)
        cumulative_cost = self.cumulative_cost(last_year)
        cumulative_revenue = self.revenue(last_year).cumulative()
        last_revenue = self.revenue(last_year).evolutions[last_year]
        output = 'Solution margin:{} investment:{} '.format(margin, cumulative_cost)
        output += ' CumulRevenue:{}'.format(cumulative_revenue)
        output += ' LastRevenue:{}'.format(last_revenue)
        for operating_division in self.operating_divisions:
            name = operating_division.geographic_area.name
            turnover = operating_division.revenue.evolutions[last_year]
            output += name + ' revenues:{}'.format(turnover)
        return output

    def revenue(self, last_year):
        revenue = Evolution()
        for operating_division in self.operating_divisions:
            revenue += operating_division.revenue
        revenue.cut(last_year)
        return revenue

    def cost(self, last_year):
        cost = Evolution()
        for operating_division in self.operating_divisions:
            operating_division.sales, operating_division.supports = operating_division.generate_employees()
            cost += operating_division.generate_costs(last_year)
        return cost

    def margin(self, last_year):
        revenue = self.revenue(last_year)
        cost = self.cost(last_year)
        return (revenue.evolutions[last_year] - cost.evolutions[last_year])/revenue.evolutions[last_year]

    def cumulative_cost(self, last_year):
        cost = self.cost(last_year)
        return cost.cumulative()

    def last_year(self):
        last_year = 0
        for operating_division in self.operating_divisions:
            last_year = max(last_year, operating_division.revenue.max())
        return last_year

class MainRevenueOptimizer(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, main_revenue: MainRevenue,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.main_revenue = main_revenue
        self._x = [0]*2*len(self.main_revenue.operating_divisions)

    def update(self, x):
        if not npy.allclose(npy.array(x), npy.array(self._x)):
            for i, operating_division in enumerate(self.main_revenue.operating_divisions):
                initial_revenue = x[2 * i]
                increase_revenue = x[2 * i + 1]
                initial_year = operating_division.revenue.min()
                final_year = operating_division.revenue.max()
                rev = {}
                for y in range(final_year - initial_year + 1):
                    rev[initial_year + y] = initial_revenue*(1 + increase_revenue)**y
                operating_division.revenue.update(rev)
            self._x = x

    def functional(self, x, margin_min, margin_max, cumulative_cost_max, revenue_obj):
        if not npy.allclose(npy.array(x), npy.array(self._x)):
            self.update(x)
            last_year = self.main_revenue.last_year()
            margin = self.main_revenue.margin(last_year)
            cumulative_cost = self.main_revenue.cumulative_cost(last_year)
            last_revenue = self.main_revenue.revenue(last_year).evolutions[last_year]
            self._margin = margin
            self._cumulative_cost = cumulative_cost
            self._last_revenue = last_revenue
        else:
            margin = self._margin
            cumulative_cost = self._cumulative_cost
            last_revenue = self._last_revenue
        return (last_revenue - revenue_obj)**2

    def constraint(self, x, margin_min, margin_max, cumulative_cost_max, revenue_obj):
        if not npy.allclose(npy.array(x), npy.array(self._x)):
            self.update(x)
            last_year = self.main_revenue.last_year()
            margin = self.main_revenue.margin(last_year)
            cumulative_cost = self.main_revenue.cumulative_cost(last_year)
            last_revenue = self.main_revenue.revenue(last_year).evolutions[last_year]
            self._margin = margin
            self._cumulative_cost = cumulative_cost
            self._last_revenue = last_revenue
        else:
            margin = self._margin
            cumulative_cost = self._cumulative_cost
            last_revenue = self._last_revenue
        ine = [margin - margin_min]
        ine.append(margin_max - margin)
        ine.append(cumulative_cost_max - cumulative_cost)
        ine.append(last_revenue - 0.8*revenue_obj)
        ine.append(1.2*revenue_obj - last_revenue)
        # ine.append(cumulative_cost - cumulative_cost_max*0.8)
        return ine

    def minimize(self, initial_revenue_max, increase_revenue_max,
                 margin_min, margin_max, cumulative_cost_max, revenue_obj):

        data = (margin_min, margin_max, cumulative_cost_max, revenue_obj)
        cons = {'type': 'ineq', 'fun': self.constraint, 'args': data}
        bnds = [[0, initial_revenue_max], [0, increase_revenue_max]]*len(self.main_revenue.operating_divisions)

        f_obj = 0
        x_out = None
        solution = None
        for nb in range(10):
            x0 = []
            for b in bnds:
                x0.append(b[0] + (b[1] - b[0]) * random.random())
            # x0 = [initial_revenue_max, increase_revenue_max]*len(self.main_revenue.operating_divisions)
            res = minimize(self.functional, x0, method='SLSQP', bounds=bnds,
                           constraints=cons, args= data)
            x_opt = res.x
            self._x = [0] * 2 * len(self.main_revenue.operating_divisions)
            self.update(x_opt)
            if min(self.constraint(x_opt, *data)) > -1e-4:
                last_year = self.main_revenue.last_year()
                margin = self.main_revenue.margin(last_year)
                cumulative_cost = self.main_revenue.cumulative_cost(last_year)
                if f_obj < margin:
                    f_obj = margin
                    x_out = x_opt
                    solution = self.main_revenue.copy()
        return solution, x_out

