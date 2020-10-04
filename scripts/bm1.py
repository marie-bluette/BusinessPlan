
import business_plan as bp

ga1 = bp.GeographicArea(market_size = 100,
                        market_maturity = 1,
                        market_access_cost = 0.01,
                        market_penetration= 0.004,
                        percentage_profit_center = 0.01,
                        percentage_cost_center = 0.001,
                        sale_annual_package = 100000,
                        support_annual_package = 40000,
                        hiring_cost = 10000,
                        name = 'France')

rev1 = bp.Evolution({2019: 1e3, 2020: 1e3*1.2, 2021: 1e3*1.4, 2022: 1e3*1.6})
od1 = bp.OperatingDivision(revenue=rev1, geographic_area=ga1)
sales, supports = od1.generate_employees()

