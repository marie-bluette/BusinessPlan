
from dessia_api_client import Client
import business_plan as bp
from dessia_common import workflow as wf
import volmdlr as vm
import math

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

ga4 = bp.GeographicArea(market_size = 90,
                        market_maturity = 2,
                        market_access_cost = 0.001,
                        market_penetration= 0.0004,
                        percentage_profit_center = 0.000004,
                        percentage_cost_center = 0.0000006,
                        sale_annual_package = 140000,
                        support_annual_package = 75000,
                        hiring_cost = 26000,
                        name = 'USA')

block_generator = wf.InstanciateModel(bp.MainRevenueGenerator, name='MainRevenueGenerator')
method_generate = wf.ModelMethod(bp.MainRevenueGenerator, 'generate', name='generate')
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

input_values = {workflow.index(block_generator.inputs[0]): [ga1, ga2, ga3],
                workflow.index(method_generate.inputs[1]): 2020,
                workflow.index(method_generate.inputs[2]): 2024,

                workflow.index(method_minimize.inputs[2]): 1e6,
                workflow.index(method_minimize.inputs[3]): 5,
                workflow.index(method_minimize.inputs[4]): 0.01,
                workflow.index(method_minimize.inputs[5]): 1,
                workflow.index(method_minimize.inputs[6]): 2e8,
                workflow.index(method_minimize.inputs[7]): 5e6,}

workflow_run = workflow.run(input_values)

# c = Client(api_url='https://api.platform-dev.dessia.tech')
# c = Client(api_url='https://api.ibm.dessia.tech')
# r = c.create_object_from_python_object(workflow_run)