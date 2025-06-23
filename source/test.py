import supplyplanningmodel as spm
import matplotlib.pyplot as plt

# Example usage
model = spm.SupplyPlanningModel()

# Define products and periods
products = ['ProductA', 'ProductB']
periods = list(range(4))
model.add_products(products)
model.add_periods(periods)

# Setup initial inventory
initial_inventory = {'ProductA': 100, 'ProductB': 50}
model.setup_variables(initial_inventory)

# Define demand
demand = {
    'ProductA': {0: 120, 1: 140, 2: 160, 3: 130},
    'ProductB': {0: 80, 1: 90, 2: 110, 3: 100}
}
model.add_demand_constraints(demand)

# Production parameters
production_time = {
    'ProductA': 2,  # hours per unit
    'ProductB': 3,  # hours per unit
    'setup': 4      # setup time in hours
}
model.add_capacity_constraints(
    regular_capacity=160,    # regular hours per period
    max_overtime=40,         # maximum overtime hours per period
    production_time=production_time
)

# Minimum production quantities
min_production = {'ProductA': 30, 'ProductB': 25}
model.add_minimum_production_constraints(min_production)

# Maximum inventory levels
max_inventory = {'ProductA': 200, 'ProductB': 150}
model.add_inventory_constraints(max_inventory)

# Define all costs
production_cost = {'ProductA': 10, 'ProductB': 12}
setup_cost = {'ProductA': 500, 'ProductB': 600}
inventory_cost = {'ProductA': 2, 'ProductB': 2}
backlog_cost = {'ProductA': 20, 'ProductB': 20}
overtime_cost = 50  # cost per overtime hour

model.set_objective(
    production_cost=production_cost,
    setup_cost=setup_cost,
    inventory_cost=inventory_cost,
    backlog_cost=backlog_cost,
    overtime_cost=overtime_cost
)

# Solve and get results
status = model.solve()
results = model.get_results()

# Create visualizations
fig = model.visualize_results(results)
plt.show()