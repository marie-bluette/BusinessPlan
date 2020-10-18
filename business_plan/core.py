from dessia_common import DessiaObject
from typing import TypeVar, List, Dict
from itertools import product, permutations
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


class EmployeeSale(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float = None, name: str = ''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=True, hiring_year=hiring_year, name=name)


class EmployeeSupport(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float = None, name: str = ''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=False, hiring_year=hiring_year, name=name)


class EmployeeTalker(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float = None, name: str = ''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=False, hiring_year=hiring_year, name=name)


class EmployeeMaker(Employee):
    def __init__(self, salary: float,
                 general_expenses: float, hiring_year: float = None, name: str = ''):
        Employee.__init__(self, salary=salary, general_expenses=general_expenses,
                          profit_center=False, hiring_year=hiring_year, name=name)


class Evolution(DessiaObject):
    _standalone_in_db = False
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, evolutions: Dict[str, float] = None,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        if evolutions is None:
            self.evolutions = {}
        else:
            self.evolutions = evolutions

    def __add__(self, other_evolution):
        year1 = [int(y) for y in self.evolutions.keys()]
        year2 = [int(y) for y in other_evolution.evolutions.keys()]
        all_year = year1
        for y in year2:
            if y not in all_year:
                all_year.append(y)
        evolutions = {}
        for y in all_year:
            evolutions[str(y)] = 0
            if str(y) in self.evolutions:
                evolutions[str(y)] += self.evolutions[str(y)]
            if str(y) in other_evolution.evolutions:
                evolutions[str(y)] += other_evolution.evolutions[str(y)]
        return Evolution(evolutions=evolutions, name=self.name)

    def __mul__(self, other):
        output = {}
        for k, v in self.evolutions.items():
            output[k] = v * other
        return Evolution(output)

    def min(self):
        return min([int(y) for y in self.evolutions.keys()])

    def max(self):
        return max([int(y) for y in self.evolutions.keys()])

    def cumulative(self):
        return sum([e for e in self.evolutions.values()])

    def update(self, evolutions):
        self.evolutions = evolutions

    def cut(self, last_year, copy=False):
        evol = {k: v for k, v in self.evolutions.items() if int(k) <= int(last_year)}
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


class MainGeographicArea(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, europe: bool = False,
                 asia: bool = False,
                 america: bool = False,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.america = america
        self.asia = asia
        self.europe = europe

    def extract_geographic_area(self, geographic_areas):
        ga = []
        for geographic_area in geographic_areas:
            if geographic_area.main_geographic_area.europe and self.europe:
                ga.append(geographic_area)
            if geographic_area.main_geographic_area.asia and self.asia:
                ga.append(geographic_area)
            if geographic_area.main_geographic_area.america and self.america:
                ga.append(geographic_area)
        return ga


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
                 main_geographic_area: MainGeographicArea,
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.main_geographic_area = main_geographic_area
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
        return max(1, int(self.percentage_profit_center * value_revenue))

    def number_supports(self, value_revenue):
        return max(1, int(self.percentage_cost_center * value_revenue))


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
        self.sale_employe = EmployeeSale(salary=geographic_area.sale_annual_package, general_expenses=0)
        self.support_employe = EmployeeSupport(salary=geographic_area.support_annual_package, general_expenses=0)
        self.evolution_sales, self.evolution_supports = Evolution(), Evolution()

    @classmethod
    def genere_operating_division(cls, geographic_area, initial_year, last_year):
        revenue = Evolution({str(k + initial_year): 1 for k in range(last_year - initial_year)})
        return cls(geographic_area, revenue)

    def update_employees(self):
        years = list(self.revenue.evolutions.keys())
        years.sort()
        evolution_sales = {}
        evolution_supports = {}
        for y in years:
            value_revenue = self.revenue.evolutions[y]
            ga = self.geographic_area
            number_sales = ga.number_sales(value_revenue)
            evolution_sales[y] = number_sales
            number_support = ga.number_supports(value_revenue)
            evolution_supports[y] = number_support
        self.evolution_sales.evolutions = evolution_sales
        self.evolution_supports.evolutions = evolution_supports

    def generate_costs(self, last_year):
        self.update_employees()
        costs = self.evolution_sales * self.sale_employe.salary
        costs += self.evolution_supports * self.support_employe.salary
        return costs


class MainRevenue(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    def __init__(self, operating_divisions: List[OperatingDivision],
                 last_margin: float = None, cumulative_cost: float = None, cumulative_revenue: float = None,
                 last_revenue: float = None, strategy_txt: str = '', revenue_txt: str = '',
                 name: str = ''):

        DessiaObject.__init__(self, name=name)
        self.operating_divisions = operating_divisions

        if last_margin is None and cumulative_cost is None and cumulative_revenue is None and last_revenue is None and strategy_txt is None and revenue_txt is None:
            self.update()
        else:
            self.last_margin, self.cumulative_cost, self.cumulative_revenue, self.last_revenue, self.strategy_txt, self.revenue_txt = last_margin, cumulative_cost, cumulative_revenue, last_revenue, strategy_txt, revenue_txt

    def update(self):
        last_year = self.last_year()
        last_margin = self.margin(last_year)
        cumulative_cost = self._cumulative_cost(last_year)
        cumulative_revenue = self.revenue(last_year).cumulative()
        last_revenue = self.revenue(last_year).evolutions[last_year]
        strategy_txt = ''
        for operating_division in self.operating_divisions:
            name = operating_division.geographic_area.name
            start_year = operating_division.revenue.min()
            strategy_txt += ' ' + name + ':' + str(start_year)
        revenue_txt = ''
        for operating_division in self.operating_divisions:
            name = operating_division.geographic_area.name
            turnover = operating_division.revenue.evolutions[last_year]
            revenue_txt += ' ' + name + ':' + str(turnover)
        self.last_margin, self.cumulative_cost, self.cumulative_revenue, self.last_revenue, self.strategy_txt, self.revenue_txt = last_margin, cumulative_cost, cumulative_revenue, last_revenue, strategy_txt, revenue_txt

    def __str__(self):
        last_year = self.last_year()
        costs = self.cost(last_year)
        margin = self.margin(last_year)
        cumulative_cost = self._cumulative_cost(last_year)
        cumulative_revenue = self.revenue(last_year).cumulative()
        last_revenue = self.revenue(last_year).evolutions[last_year]
        output = 'Solution margin:{} investment:{} '.format(margin, cumulative_cost) + '\n'
        for operating_division in self.operating_divisions:
            name = operating_division.geographic_area.name
            start_year = operating_division.revenue.min()
            output += ' ' + name + ' start year:{}'.format(start_year) + '\n'
        output += ' CumulRevenue:{}'.format(cumulative_revenue) + '\n'
        output += ' LastRevenue:{}'.format(last_revenue) + '\n'
        for operating_division in self.operating_divisions:
            name = operating_division.geographic_area.name
            turnover = operating_division.revenue.evolutions[last_year]
            output += ' ' + name + ' revenues:{}'.format(turnover) + '\n'
        return output

    def to_csv(self, max_country=None):
        if max_country is None:
            max_country = len(self.operating_divisions)
        title = ''
        datas = ''
        last_year = self.last_year()
        costs = self.cost(last_year)
        margin = self.margin(last_year)
        title += 'margin'
        datas += str(margin)
        cumulative_cost = self._cumulative_cost(last_year)
        title += ',cumulative_cost'
        datas += ',' + str(cumulative_cost)
        cumulative_revenue = self.revenue(last_year).cumulative()
        last_revenue = self.revenue(last_year).evolutions[last_year]
        for operating_division in self.operating_divisions:
            name = operating_division.geographic_area.name
            start_year = operating_division.revenue.min()
            title += ',name, start_year'
            datas += ',' + name + ',' + str(start_year)
        for i in range(max_country - len(self.operating_divisions)):
            title += ',name, start_year'
            datas += ',' + ','
        title += ',cumulative_revenue'
        datas += ',' + str(cumulative_revenue)
        title += ',last_revenue'
        datas += ',' + str(last_revenue)
        for operating_division in self.operating_divisions:
            name = operating_division.geographic_area.name
            turnover = operating_division.revenue.evolutions[last_year]
            title += ',name, turnover_last_year'
            datas += ',' + name + ',' + str(turnover)
        for i in range(max_country - len(self.operating_divisions)):
            title += ',name, turnover_last_year'
            datas += ',' + ','
        return title, datas

    def revenue(self, last_year):
        revenue = Evolution()
        for operating_division in self.operating_divisions:
            revenue += operating_division.revenue
        revenue.cut(last_year)
        return revenue

    def cost(self, last_year):
        cost = Evolution()
        for operating_division in self.operating_divisions:
            cost += operating_division.generate_costs(last_year)
        return cost

    def margin(self, last_year):
        revenue = self.revenue(last_year)
        cost = self.cost(last_year)
        return (revenue.evolutions[last_year] - cost.evolutions[last_year]) / revenue.evolutions[last_year]

    def _cumulative_cost(self, last_year):
        cost = self.cost(last_year)
        return cost.cumulative()

    def last_year(self):
        last_year = 0
        for operating_division in self.operating_divisions:
            last_year = max(last_year, int(operating_division.revenue.max()))
        return str(last_year)


class MainRevenueOptimizer(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    _dessia_methods = ['minimize']

    def __init__(self, name: str = ''):
        DessiaObject.__init__(self, name=name)

    def minimize(self, main_revenues: List[MainRevenue], initial_revenue_max: float, increase_revenue_max: float,
                 margin_min: float, margin_max: float, cumulative_cost_max: float, revenue_obj: float) -> List[
        MainRevenue]:
        solutions = []
        for main_revenue in main_revenues:
            self._x = [0] * 2 * len(main_revenue.operating_divisions)
            solution = self.minimize_elem(main_revenue, initial_revenue_max, increase_revenue_max,
                                          margin_min, margin_max, cumulative_cost_max, revenue_obj)
            if solution is not None:
                solutions.append(solution)
        return solutions

    def update(self, x, main_revenue):
        if not npy.allclose(npy.array(x), npy.array(self._x)):
            for i, operating_division in enumerate(main_revenue.operating_divisions):
                initial_revenue = x[2 * i]
                increase_revenue = x[2 * i + 1]
                initial_year = operating_division.revenue.min()
                final_year = operating_division.revenue.max()
                rev = {}
                for y in range(final_year - initial_year + 1):
                    rev[str(initial_year + y)] = initial_revenue * (1 + increase_revenue) ** y
                operating_division.revenue.update(rev)
            self._x = x

    def functional(self, x, main_revenue, margin_min, margin_max, cumulative_cost_max, revenue_obj):
        if not npy.allclose(npy.array(x), npy.array(self._x)):
            self.update(x, main_revenue)
            last_year = main_revenue.last_year()
            margin = main_revenue.margin(last_year)
            cumulative_cost = main_revenue._cumulative_cost(last_year)
            last_revenue = main_revenue.revenue(last_year).evolutions[last_year]
            self._margin = margin
            self._cumulative_cost = cumulative_cost
            self._last_revenue = last_revenue
        else:
            margin = self._margin
            cumulative_cost = self._cumulative_cost
            last_revenue = self._last_revenue
        return (last_revenue - revenue_obj) ** 2

    def constraint(self, x, main_revenue, margin_min, margin_max, cumulative_cost_max, revenue_obj):
        if not npy.allclose(npy.array(x), npy.array(self._x)):
            self.update(x, main_revenue)
            last_year = main_revenue.last_year()
            margin = main_revenue.margin(last_year)
            cumulative_cost = main_revenue._cumulative_cost(last_year)
            last_revenue = main_revenue.revenue(last_year).evolutions[last_year]
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
        ine.append(last_revenue - 0.95 * revenue_obj)
        ine.append(1.05 * revenue_obj - last_revenue)
        # ine.append(cumulative_cost - cumulative_cost_max*0.8)
        return ine

    def minimize_elem(self, main_revenue, initial_revenue_max, increase_revenue_max,
                      margin_min, margin_max, cumulative_cost_max, revenue_obj):

        data = (main_revenue, margin_min, margin_max, cumulative_cost_max, revenue_obj)
        cons = {'type': 'ineq', 'fun': self.constraint, 'args': data}
        bnds = [[0, initial_revenue_max], [0, increase_revenue_max]] * len(main_revenue.operating_divisions)

        f_obj = 0
        x_out = None
        solution = None
        for nb in range(10):
            x0 = []
            for b in bnds:
                x0.append(b[0] + (b[1] - b[0]) * random.random())
            # x0 = [initial_revenue_max, increase_revenue_max]*len(self.main_revenue.operating_divisions)
            res = minimize(self.functional, x0, method='SLSQP', bounds=bnds,
                           constraints=cons, args=data)
            x_opt = res.x
            self._x = [0] * 2 * len(main_revenue.operating_divisions)
            self.update(x_opt, main_revenue)
            if min(self.constraint(x_opt, *data)) > -1e-4:
                last_year = main_revenue.last_year()
                margin = main_revenue.margin(last_year)
                cumulative_cost = main_revenue._cumulative_cost(last_year)
                if f_obj < margin:
                    f_obj = margin
                    x_out = x_opt
                    solution = main_revenue.copy()
                    solution.update()
        return solution


class MainRevenueGenerator(DessiaObject):
    _standalone_in_db = True
    _generic_eq = True
    _non_serializable_attributes = []
    _non_eq_attributes = ['name']
    _non_hash_attributes = ['name']

    _dessia_methods = ['generate']

    def __init__(self, geographic_areas: List[GeographicArea],
                 name: str = ''):
        DessiaObject.__init__(self, name=name)
        self.geographic_areas = geographic_areas

    def extract_main_geographic_area(self):
        main_geographic_areas = []
        for geographic_area in self.geographic_areas:
            if geographic_area.main_geographic_area not in main_geographic_areas:
                main_geographic_areas.append(geographic_area.main_geographic_area)
        return main_geographic_areas

    def generate(self, initial_year: int, last_year: int) -> List[MainRevenue]:
        main_revenues = []
        for number_geographic_area in range(len(self.geographic_areas)):
            for geographic_areas in permutations(self.geographic_areas, number_geographic_area + 1):

                if len(geographic_areas) > 0:
                    for indice_years in product(range(last_year - initial_year), repeat=len(geographic_areas) - 1):
                        operating_divisions = []
                        operating_divisions.append(OperatingDivision.genere_operating_division(geographic_areas[0],
                                                                                               initial_year, last_year))
                        for i, geographic_area in enumerate(geographic_areas[1:]):
                            operating_divisions.append(OperatingDivision.genere_operating_division(geographic_area,
                                                                                                   initial_year +
                                                                                                   indice_years[i],
                                                                                                   last_year))
                        main_revenue = MainRevenue(operating_divisions)
                        main_revenues.append(main_revenue)
        return main_revenues

    def decision_tree(self, initial_year: int, last_year: int) -> List[MainRevenue]:
        main_geographic_areas = self.extract_main_geographic_area()
        number_main_area = len(main_geographic_areas)
        number_years = last_year - initial_year - 1
        dt = DecisionTree()
        # point 0 : number main area
        # point 1 : indice main area
        # point 2 : year start main area
        main_revenues = []
        while not dt.finished:
            valid = True
            if dt.current_depth == 0:
                dt.SetCurrentNodeNumberPossibilities(number_main_area)
            if dt.current_depth > 0:
                nb_main_area = dt.current_node[0]
                list_position = [2 * i + 1 for i in range(nb_main_area)]
                if (dt.current_depth + 1) % 2 == 0:
                    dt.SetCurrentNodeNumberPossibilities(number_main_area)
                elif (dt.current_depth + 2) % 2 == 0:
                    dt.SetCurrentNodeNumberPossibilities(number_years)
                if dt.current_depth == 2 * (nb_main_area + 1) + 1:
                    dt.SetCurrentNodeNumberPossibilities(0)
            if dt.current_depth > 0 and (dt.current_depth + 1) % 2 == 0:
                nb = int((dt.current_depth - 1) / 2.)
                list_area = [dt.current_node[2 * i + 1] for i in range(nb)]
                list_year = [dt.current_node[2 * i + 2] for i in range(nb)]
                if len(set(list_area)) != len(list_area):
                    valid = False
            if valid and dt.current_depth > 0:
                nb = int((dt.current_depth - 1) / 2.)
                list_area = [dt.current_node[2 * i + 1] for i in range(nb)]
                list_year = [dt.current_node[2 * i + 2] for i in range(nb)]

                if dt.current_depth == 2 * (nb_main_area + 1) + 1:
                    if 0 not in list_year:
                        valid = False
                    elif sorted(list_area) != list_area:  # isomorphism slection
                        valid = False
                    else:
                        sols = []
                        for ind_area, ind_year in zip(list_area, list_year):
                            sols.append(self.decision_tree_geographic_area(main_geographic_areas[ind_area],
                                                                           initial_year + ind_year, last_year))
                        for operating_divisions in product(*sols):
                            ods = [o[0] for o in operating_divisions]
                            main_revenue = MainRevenue(ods)
                            main_revenues.append(main_revenue)
            dt.NextNode(valid)
        return main_revenues

    def decision_tree_geographic_area(self, main_area: MainGeographicArea, initial_year: int, last_year: int) -> List[
        List[OperatingDivision]]:
        geographic_areas = main_area.extract_geographic_area(self.geographic_areas)
        number_area = len(geographic_areas)
        number_years = last_year - initial_year - 1
        dt = DecisionTree()
        # point 0 : number geographic area
        # point 1 : indice geographic area
        # point 2 : year start geographic area
        solutions = []
        while not dt.finished:
            valid = True
            if dt.current_depth == 0:
                dt.SetCurrentNodeNumberPossibilities(number_area)
            if dt.current_depth > 0:
                nb_area = dt.current_node[0]
                list_position = [2 * i + 1 for i in range(nb_area)]
                if (dt.current_depth + 1) % 2 == 0:
                    dt.SetCurrentNodeNumberPossibilities(number_area)
                elif (dt.current_depth + 2) % 2 == 0:
                    dt.SetCurrentNodeNumberPossibilities(number_years)
                if dt.current_depth == 2 * (nb_area + 1) + 1:
                    dt.SetCurrentNodeNumberPossibilities(0)
            if dt.current_depth > 0 and (dt.current_depth + 1) % 2 == 0:
                nb = int((dt.current_depth - 1) / 2.)
                list_area = [dt.current_node[2 * i + 1] for i in range(nb)]
                if len(set(list_area)) != len(list_area):
                    valid = False
            if valid and dt.current_depth > 0:
                if dt.current_depth == 2 * (nb_area + 1) + 1:
                    nb = int((dt.current_depth - 1) / 2.)
                    list_area = [dt.current_node[2 * i + 1] for i in range(nb)]
                    list_year = [dt.current_node[2 * i + 2] for i in range(nb)]

                    if dt.current_depth == 2 * (nb_area + 1) + 1:
                        if 0 not in list_year:
                            valid = False
                        elif sorted(list_area) != list_area:  # isomorphism slection
                            valid = False
                        else:
                            operating_divisions = []
                            operating_divisions.append(
                                OperatingDivision.genere_operating_division(geographic_areas[list_area[0]],
                                                                            initial_year + list_year[0],
                                                                            last_year))
                            for i, indice in enumerate(list_area[1:]):
                                operating_divisions.append(
                                    OperatingDivision.genere_operating_division(geographic_areas[indice],
                                                                                initial_year +
                                                                                list_year[i + 1],
                                                                                last_year))
                            solutions.append(operating_divisions)
            dt.NextNode(valid)
        return solutions
