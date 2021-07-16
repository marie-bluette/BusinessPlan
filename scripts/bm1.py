from dessia_api_client import Client
import business_plan as bp
from dessia_common import workflow as wf
import volmdlr as vm
import math
import business_plan.pricing as pricing
import business_plan.employee as employee


licence_manager = pricing.RecurringRevenue(revenue_per_month = 100, pricing_family = pricing.PricingFamily('manager'))
licence_user = pricing.RecurringRevenue(revenue_per_month = 200, pricing_family = pricing.PricingFamily('user'))
licence_super_user = pricing.RecurringRevenue(revenue_per_month = 500, pricing_family = pricing.PricingFamily('super-user'))

package_family_small = pricing.PackageFamily('small')
package_family_middle = pricing.PackageFamily('middle')
package_family_large = pricing.PackageFamily('large')

package_small = pricing.Package(sub_packages=[pricing.SubPackage(recurring_revenue=licence_manager, number=2),
                                              pricing.SubPackage(recurring_revenue=licence_user, number=1),
                                              pricing.SubPackage(recurring_revenue=licence_super_user, number=1)],
                                package_family=package_family_small)

package_middle = pricing.Package(sub_packages=[pricing.SubPackage(recurring_revenue=licence_manager, number=4),
                                              pricing.SubPackage(recurring_revenue=licence_user, number=3),
                                              pricing.SubPackage(recurring_revenue=licence_super_user, number=1)],
                                package_family=package_family_middle)

package_large = pricing.Package(sub_packages=[pricing.SubPackage(recurring_revenue=licence_manager, number=10),
                                              pricing.SubPackage(recurring_revenue=licence_user, number=8),
                                              pricing.SubPackage(recurring_revenue=licence_super_user, number=3)],
                                package_family=package_family_large)

sale1 = employee.Sale(salary=40000, general_expenses=10000, hiring_year=2020)
sale2 = employee.Sale(salary=50000, general_expenses=10000, hiring_year=2020)
dev1 = employee.Developer(salary=40000, general_expenses=10000, hiring_year=2020)
team1 = employee.Team(employees=[sale1, sale2, dev1])

rule1 = employee.EmployeeNeedRule(if_employee=sale1, number_greater_than=1,
                                  then_employee=[dev1, dev1])
team2 = employee.Team.generate(employee_need_rules=[rule1], employees=[sale1, sale2])

#
# raise
#
# Europe = bp.MainGeographicArea(europe=True)
# Asia = bp.MainGeographicArea(asia=True)
# America = bp.MainGeographicArea(america=True)
#
# France = bp.GeographicArea(market_size=1100000000, market_maturity=8, market_access_cost=0.99, market_penetration=0.001,
#                            percentage_profit_center=0.0000105, percentage_cost_center=0.0000022,
#                            sale_annual_package=66000, support_annual_package=47500, hiring_cost=12000,
#                            main_geographic_area=Europe, name='France')
# Germany = bp.GeographicArea(market_size=1300000000, market_maturity=9, market_access_cost=1.026,
#                             market_penetration=0.001, percentage_profit_center=0.0000115,
#                             percentage_cost_center=0.00000224, sale_annual_package=64800, support_annual_package=54000,
#                             hiring_cost=11000, main_geographic_area=Europe, name='Germany ')
# Italy = bp.GeographicArea(market_size=900000000, market_maturity=4, market_access_cost=0.945, market_penetration=0.001,
#                           percentage_profit_center=0.0000105, percentage_cost_center=0.0000022,
#                           sale_annual_package=66000, support_annual_package=47500, hiring_cost=9000,
#                           main_geographic_area=Europe, name='Italy')
# USA = bp.GeographicArea(market_size=1200000000, market_maturity=10, market_access_cost=0.828, market_penetration=0.001,
#                         percentage_profit_center=0.000011, percentage_cost_center=0.00000224, sale_annual_package=72000,
#                         support_annual_package=55000, hiring_cost=13000,
#                         main_geographic_area=America, name='USA')
# Canada = bp.GeographicArea(market_size=1300000000, market_maturity=9, market_access_cost=0.846,
#                            market_penetration=0.001, percentage_profit_center=0.0000115,
#                            percentage_cost_center=0.00000224, sale_annual_package=64800, support_annual_package=54000,
#                            hiring_cost=11000,
#                            main_geographic_area=America, name='Canada')
# China = bp.GeographicArea(market_size=2500000000, market_maturity=10, market_access_cost=0.72, market_penetration=0.001,
#                           percentage_profit_center=0.000007, percentage_cost_center=0.0000011,
#                           sale_annual_package=30000, support_annual_package=27500, hiring_cost=7000,
#                           main_geographic_area=Asia, name='China')
# Japan = bp.GeographicArea(market_size=900000000, market_maturity=4, market_access_cost=0.99, market_penetration=0.001,
#                           percentage_profit_center=0.000011, percentage_cost_center=0.00000224,
#                           sale_annual_package=72000, support_annual_package=55000, hiring_cost=13000,
#                           main_geographic_area=Asia, name='Japan')
#
# mrg1 = bp.MainRevenueGenerator([France, Germany, Italy, USA, Canada, China, Japan])
# main_revenues = mrg1.decision_tree(initial_year=2020, last_year=2024)
# print(len(main_revenues))
# mro1 = bp.MainRevenueOptimizer()
# solutions = mro1.minimize(main_revenues=main_revenues, initial_revenue_max=1e6, increase_revenue_max=5,
#                           margin_min=0.01, margin_max=1, cumulative_cost_max=2e8,
#                           revenue_obj=5e6)
# sols = mro1.sort_solutions(solutions, 50)
#
# # c = Client(api_url='https://api.ibm.dessia.tech')
# # r = c.create_object_from_python_object(solutions[0])
#
#
# file = open('output.csv', 'w')
#
# for i, sol in enumerate(solutions):
#     title, datas = sol.to_csv(len(mrg1.geographic_areas))
#     if i == 0:
#         file.write(title + '\n')
#     file.write(datas + '\n')
# file.close()
