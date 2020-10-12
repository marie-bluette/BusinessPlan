
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

ga3 = bp.GeographicArea(market_size = 90,
                        market_maturity = 2,
                        market_access_cost = 0.001,
                        market_penetration= 0.0004,
                        percentage_profit_center = 0.000005,
                        percentage_cost_center = 0.0000005,
                        sale_annual_package = 80000,
                        support_annual_package = 40000,
                        hiring_cost = 18000,
                        name = 'Italy')

mrg1 = bp.MainRevenueGenerator([ga1, ga2, ga3])
main_revenues = mrg1.generate(initial_year=2020, last_year=2024)
mro1 = bp.MainRevenueOptimizer()
solutions = mro1.minimize(main_revenues=main_revenues, initial_revenue_max=1e6, increase_revenue_max=5,
                                margin_min=0.01, margin_max=1, cumulative_cost_max=2e8,
                                revenue_obj=5e6)

for sol in solutions:
    print(sol)
