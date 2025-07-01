from abc import ABC, abstractmethod
'''This module defines the base class for constraints and a specific inventory constraint.
It provides a structure for creating and evaluating constraints in a supply planning model.
Constraints cover areas such as

1. Capacity Constraints
Production capacity: Max output per time period per resource.

Storage capacity: Limits on inventory at warehouses or distribution centers.

Transportation capacity: Limits on truck/container availability or shipping volume.

2. Material Constraints
Availability of components or raw materials.

Lead times for procurement and delivery.

production conversion factors (e.g., yield rates).

3. Inventory Constraints
Minimum/maximum inventory levels.

Safety stock requirements.

Shelf-life or expiry dates (for perishables).

4. Demand Fulfillment Constraints
Customer service levels (fill rate, OTIF).

Order prioritization or allocation rules.

5. Scheduling Constraints
Setup/changeover times and costs.

Shift patterns, working hours, or maintenance windows.

6. Financial Constraints
Budget limits for production, procurement, or logistics.

Cost minimization or profit maximization objectives.

7. Policy Constraints
Make-to-order vs. make-to-stock policies.

Fixed production lot sizes.

Supplier contracts (e.g., MOQ, quotas).'''

class Constraint(ABC):

    def __init__(self, name, description, scope, constraint_type, start_date, end_date=None, parameters=None):
        """Initialize a constraint."""
        self.name = name
        self.description = description
        self.scope = scope
        self.constraint_type = constraint_type
        self.start_date = start_date
        self.end_date = end_date
        if parameters is None:
            parameters = {}
        self.parameters = parameters

    @abstractmethod
    def evaluate(self, data):
        """Evaluate the constraint against the model."""
        pass


class InventoryConstraint(Constraint):
    def __init__(self, name, description, scope, parameters,min_inventory=0):
        """Initialize a inventory constraint."""
        super().__init__(name, description, scope, 'inventory', parameters)
        self.min_inventory = min_inventory

    def evaluate(self, inventory_level):
        """Evaluate the inventory constraint."""
        # Example evaluation logic
        return inventory_level >= self.min_inventory
    
class CapacityConstraint(Constraint):
    def __init__(self, name, description, scope, parameters, max_capacity=0):
        """Initialize a capacity constraint."""
        super().__init__(name, description, scope, 'capacity', parameters)
        self.max_capacity = max_capacity

    def evaluate(self, production_level):
        """Evaluate the capacity constraint."""
        # Example evaluation logic
        return production_level <= self.max_capacity
    

    
# Example instantiation of an IncentoryConstraint

t = InventoryConstraint(
    name="Max Inventory Constraint",
    description="Ensure inventory does not exceed maximum levels.",
    scope="product",
    parameters={"max_inventory": 200},
    min_inventory=500
)

#


# Example usage
print(t.min_inventory)
print(t.evaluate(100))  # Should return False since 600 > 500