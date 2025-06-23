from abc import ABC, abstractmethod


class Constraint(ABC):

    def __init__(self, name, description, scope, constraint_type, parameters):
        """Initialize a constraint."""
        self.name = name
        self.description = description
        self.scope = scope
        self.constraint_type = constraint_type
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
    


t = InventoryConstraint(
    name="Max Inventory Constraint",
    description="Ensure inventory does not exceed maximum levels.",
    scope="product",
    parameters={"max_inventory": 200},
    min_inventory=500
)

print(t.min_inventory)
print(t.evaluate(100))  # Should return False since 600 > 500