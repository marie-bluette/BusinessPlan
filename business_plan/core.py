
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
        if year < self.hiring_year or year > self.exit_year:
            return 0
        else:
            return self.salary + self.general_expenses

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
        return evolutions

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

    def generate_costs(self):
        years = list(self.revenue.evolutions.keys())

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
        revenue = Evolution()
        for operating_division in self.operating_divisions:
            revenue += operating_division.revenue
        return revenue
