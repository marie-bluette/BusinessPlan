
import business_plan as bp

ga1 = bp.GeographicArea(market_size = 120,
                        market_maturity = 2,
                        market_access_cost = 0.001,
                        market_penetration= 0.0004,
                        percentage_profit_center = 0.000005,
                        percentage_cost_center = 0.0000005,
                        sale_annual_package = 130000,
                        support_annual_package = 60000,
                        hiring_cost = 20000,
                        name = 'France')
rev1 = bp.Evolution({2019: 1e6, 2020: 1e6, 2021: 1e6, 2022: 1e6, 2023: 1e6, 2024: 1e6, 2025: 1e6})
od1 = bp.OperatingDivision(revenue=rev1, geographic_area=ga1)
sales, supports = od1.generate_employees()

ga2 = bp.GeographicArea(market_size = 130,
                        market_maturity = 2,
                        market_access_cost = 0.001,
                        market_penetration= 0.0004,
                        percentage_profit_center = 0.000005,
                        percentage_cost_center = 0.0000005,
                        sale_annual_package = 130000,
                        support_annual_package = 60000,
                        hiring_cost = 20000,
                        name = 'Germany')
rev2 = bp.Evolution({2020: 1e6, 2021: 1e6, 2022: 1e6, 2023: 1e6, 2024: 1e6, 2025: 1e6})
od2 = bp.OperatingDivision(revenue=rev2, geographic_area=ga2)

mr1 = bp.MainRevenue(operating_divisions=[od1, od2])
mro1 = bp.MainRevenueOptimizer(main_revenue=mr1)
for i in range(100):
    sol, x_out = mro1.minimize(initial_revenue_max=1e6, increase_revenue_max=5,
                        margin_min=0.01, margin_max=1, cumulative_cost_max=2e8,
                        revenue_obj=5e6)
    if sol is not None:
        print(sol)
        print(x_out)
        print('ineq', mro1.constraint(x_out,margin_min=0.01, margin_max=1, cumulative_cost_max=2e8, revenue_obj=5e6))
        print('fonc', mro1.functional(x_out, margin_min=0.01, margin_max=1, cumulative_cost_max=2e8, revenue_obj=5e6))
        print(len(sol.operating_divisions[0].sales)+len(sol.operating_divisions[0].supports), len(sol.operating_divisions[1].sales)+len(sol.operating_divisions[1].supports))