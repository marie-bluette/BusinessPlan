from dessia_api_client import Client
import business_plan as bp
from dessia_common import workflow as wf
import volmdlr as vm
import math

Europe = bp.MainGeographicArea(europe=True)
Asia = bp.MainGeographicArea(asia=True)
America = bp.MainGeographicArea(america=True)

France = bp.GeographicArea(market_size=1100000000, market_maturity=8, market_access_cost=0.99, market_penetration=0.001,
                           percentage_profit_center=0.0000105, percentage_cost_center=0.0000022,
                           sale_annual_package=66000, support_annual_package=47500, hiring_cost=12000,
                           main_geographic_area=Europe, name='France')
Germany = bp.GeographicArea(market_size=1300000000, market_maturity=9, market_access_cost=1.026,
                            market_penetration=0.001, percentage_profit_center=0.0000115,
                            percentage_cost_center=0.00000224, sale_annual_package=64800, support_annual_package=54000,
                            hiring_cost=11000, main_geographic_area=Europe, name='Germany ')
Italy = bp.GeographicArea(market_size=900000000, market_maturity=4, market_access_cost=0.945, market_penetration=0.001,
                          percentage_profit_center=0.0000105, percentage_cost_center=0.0000022,
                          sale_annual_package=66000, support_annual_package=47500, hiring_cost=9000,
                          main_geographic_area=Europe, name='Italy')
USA = bp.GeographicArea(market_size=1200000000, market_maturity=10, market_access_cost=0.828, market_penetration=0.001,
                        percentage_profit_center=0.000011, percentage_cost_center=0.00000224, sale_annual_package=72000,
                        support_annual_package=55000, hiring_cost=13000,
                        main_geographic_area=America, name='USA')
Canada = bp.GeographicArea(market_size=1300000000, market_maturity=9, market_access_cost=0.846,
                           market_penetration=0.001, percentage_profit_center=0.0000115,
                           percentage_cost_center=0.00000224, sale_annual_package=64800, support_annual_package=54000,
                           hiring_cost=11000,
                           main_geographic_area=America, name='Canada')
China = bp.GeographicArea(market_size=2500000000, market_maturity=10, market_access_cost=0.72, market_penetration=0.001,
                          percentage_profit_center=0.000007, percentage_cost_center=0.0000011,
                          sale_annual_package=30000, support_annual_package=27500, hiring_cost=7000,
                          main_geographic_area=Asia, name='China')
Japan = bp.GeographicArea(market_size=900000000, market_maturity=4, market_access_cost=0.99, market_penetration=0.001,
                          percentage_profit_center=0.000011, percentage_cost_center=0.00000224,
                          sale_annual_package=72000, support_annual_package=55000, hiring_cost=13000,
                          main_geographic_area=Asia, name='Japan')

mrg1 = bp.MainRevenueGenerator([France, Germany, Italy, USA, Canada, China, Japan])
main_revenues = mrg1.decision_tree(initial_year=2020, last_year=2023)
print(len(main_revenues))
mro1 = bp.MainRevenueOptimizer()
solutions = mro1.minimize(main_revenues=main_revenues, initial_revenue_max=1e6, increase_revenue_max=5,
                          margin_min=0.01, margin_max=1, cumulative_cost_max=2e8,
                          revenue_obj=5e6)
sols = mro1.sort_solutions(solutions, 50)

# c = Client(api_url='https://api.ibm.dessia.tech')
# r = c.create_object_from_python_object(solutions[0])


file = open('output.csv', 'w')

for i, sol in enumerate(solutions):
    title, datas = sol.to_csv(len(mrg1.geographic_areas))
    if i == 0:
        file.write(title + '\n')
    file.write(datas + '\n')
file.close()
