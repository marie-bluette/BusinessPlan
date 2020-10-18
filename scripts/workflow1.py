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
                          main_geographic_area=Europe,
                          name='Italy')
USA = bp.GeographicArea(market_size=1200000000, market_maturity=10, market_access_cost=0.828, market_penetration=0.001,
                        percentage_profit_center=0.000011, percentage_cost_center=0.00000224, sale_annual_package=72000,
                        support_annual_package=55000, hiring_cost=13000, main_geographic_area=America, name='USA')
Canada = bp.GeographicArea(market_size=1300000000, market_maturity=9, market_access_cost=0.846,
                           market_penetration=0.001, percentage_profit_center=0.0000115,
                           percentage_cost_center=0.00000224, sale_annual_package=64800, support_annual_package=54000,
                           hiring_cost=11000, main_geographic_area=America, name='Canada')
China = bp.GeographicArea(market_size=2500000000, market_maturity=10, market_access_cost=0.72, market_penetration=0.001,
                          percentage_profit_center=0.000007, percentage_cost_center=0.0000011,
                          sale_annual_package=30000, support_annual_package=27500, hiring_cost=7000,
                          main_geographic_area=Asia,
                          name='China')
Japan = bp.GeographicArea(market_size=900000000, market_maturity=4, market_access_cost=0.99, market_penetration=0.001,
                          percentage_profit_center=0.000011, percentage_cost_center=0.00000224,
                          sale_annual_package=72000, support_annual_package=55000, hiring_cost=13000,
                          main_geographic_area=Asia, name='Japan')

block_generator = wf.InstanciateModel(bp.MainRevenueGenerator, name='MainRevenueGenerator')
method_generate = wf.ModelMethod(bp.MainRevenueGenerator, 'decision_tree', name='generate')
block_optimizer = wf.InstanciateModel(bp.MainRevenueOptimizer, name='MainRevenueOptimizer')
method_minimize = wf.ModelMethod(bp.MainRevenueOptimizer, 'minimize', name='minimize')

parallel_plot_block = wf.ParallelPlot(['last_margin', 'cumulative_cost', 'cumulative_revenue',
                                       'last_revenue', 'strategy_txt', 'revenue_txt'])

blocks = []

blocks.extend([block_generator, method_generate, block_optimizer, method_minimize,
               parallel_plot_block])

pipes = [wf.Pipe(block_generator.outputs[0], method_generate.inputs[0]),
         wf.Pipe(method_generate.outputs[0], method_minimize.inputs[1]),
         wf.Pipe(block_optimizer.outputs[0], method_minimize.inputs[0]),
         wf.Pipe(method_minimize.outputs[0], parallel_plot_block.inputs[0])]

workflow = wf.Workflow(blocks, pipes, method_minimize.outputs[0], name='Generation')

workflow.plot_jointjs()

input_values = {workflow.index(block_generator.inputs[0]): [France, Germany, Italy, USA, Canada, China, Japan],
                workflow.index(method_generate.inputs[1]): 2020,
                workflow.index(method_generate.inputs[2]): 2023,

                workflow.index(method_minimize.inputs[2]): 1e6,
                workflow.index(method_minimize.inputs[3]): 5,
                workflow.index(method_minimize.inputs[4]): 0.01,
                workflow.index(method_minimize.inputs[5]): 1,
                workflow.index(method_minimize.inputs[6]): 2e8,
                workflow.index(method_minimize.inputs[7]): 5e6, }

workflow_run = workflow.run(input_values)

# c = Client(api_url='https://api.platform-dev.dessia.tech')
c = Client(api_url='https://api.ibm.dessia.tech')
r = c.create_object_from_python_object(workflow_run)
