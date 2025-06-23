class AdvancedSupplyPlanningModel:
    def __init__(self):
        """Initialize the advanced supply chain optimization model."""
        self.model = pulp.LpProblem("Advanced_Supply_Chain_Optimization", pulp.LpMinimize)
        self.periods = []
        self.products = []
        self.facilities = []
        self.variables = {}
        self.scenario_results = {}

    # [Previous methods remain the same]

    def get_results(self):
        """
        Extract detailed optimization results with comprehensive metrics.
        Returns a dictionary of DataFrames for different optimization aspects.
        """
        results = {
            'production': [],
            'inventory': [],
            'transportation': [],
            'workforce': [],
            'financial_summary': {}
        }

        # Production Results
        for f in self.facilities:
            for p in self.products:
                for t in self.periods:
                    results['production'].append({
                        'facility': f,
                        'product': p,
                        'period': t,
                        'quantity': self.variables['production'][f, p, t].value(),
                        'setup': self.variables['setup'][f, p, t].value()
                    })

        # Inventory Results
        for f in self.facilities:
            for p in self.products:
                for t in self.periods:
                    results['inventory'].append({
                        'facility': f,
                        'product': p,
                        'period': t,
                        'inventory': self.variables['inventory'][f, p, t].value(),
                        'backlog': self.variables['backlog'][f, p, t].value()
                    })

        # Transportation Results
        for f1 in self.facilities:
            for f2 in self.facilities:
                for p in self.products:
                    for t in self.periods:
                        if f1 != f2:
                            transport_qty = self.variables['transport'][f1, f2, p, t].value()
                            if transport_qty > 0:
                                results['transportation'].append({
                                    'from_facility': f1,
                                    'to_facility': f2,
                                    'product': p,
                                    'period': t,
                                    'quantity': transport_qty
                                })

        # Workforce Results
        for f in self.facilities:
            for t in self.periods:
                results['workforce'].append({
                    'facility': f,
                    'period': t,
                    'skilled_workforce': self.variables['workforce'][f, 'skilled', t].value(),
                    'unskilled_workforce': self.variables['workforce'][f, 'unskilled', t].value(),
                    'overtime': self.variables['overtime'][f, t].value()
                })

        # Convert to DataFrames
        results['production_df'] = pd.DataFrame(results['production'])
        results['inventory_df'] = pd.DataFrame(results['inventory'])
        results['transportation_df'] = pd.DataFrame(results['transportation'])
        results['workforce_df'] = pd.DataFrame(results['workforce'])

        return results

    def generate_scenario_comparison(self, scenarios):
        """
        Run multiple scenarios and provide comprehensive comparison.
        
        Args:
            scenarios (dict): Dictionary of scenario configurations
        
        Returns:
            dict: Comparison results for each scenario
        """
        comparison_results = {}

        for scenario_name, scenario_config in scenarios.items():
            # Reset the model
            self.__init__()

            # Configure scenario
            self.add_facilities(scenario_config.get('facilities', ['Factory1']))
            self.add_products(scenario_config.get('products', ['ProductA']))
            self.add_periods(scenario_config.get('periods', list(range(4))))

            # Setup variables
            self.setup_variables(scenario_config.get('initial_inventory'))

            # Add constraints and objective function based on scenario
            self.add_demand_satisfaction_constraints(scenario_config['demand'])
            self.add_workforce_constraints(scenario_config['workforce_params'])
            
            if 'material_requirements' in scenario_config:
                self.add_material_requirements_constraints(scenario_config['material_requirements'])

            self.set_objective_function(scenario_config['cost_parameters'])

            # Solve and store results
            solve_status = self.solve()
            results = self.get_results()
            
            comparison_results[scenario_name] = {
                'status': solve_status,
                'results': results
            }

        return comparison_results

    def visualization_suite(self, results):
        """
        Create comprehensive visualizations for supply chain analysis.
        
        Args:
            results (dict): Results from get_results() method
        
        Returns:
            dict: Matplotlib figure objects
        """
        figures = {}

        # Production Overview
        plt.figure(figsize=(15, 10))
        plt.subplot(2, 2, 1)
        prod_df = results['production_df']
        prod_pivot = prod_df.pivot_table(
            index='period', 
            columns=['facility', 'product'], 
            values='quantity', 
            aggfunc='sum'
        )
        prod_pivot.plot(kind='bar', ax=plt.gca())
        plt.title('Production Quantities by Facility and Product')
        plt.xlabel('Period')
        plt.ylabel('Quantity')
        plt.tight_layout()
        figures['production_overview'] = plt.gcf()

        # Inventory Analysis
        plt.figure(figsize=(15, 10))
        inv_df = results['inventory_df']
        inv_pivot = inv_df.pivot_table(
            index='period', 
            columns=['facility', 'product'], 
            values='inventory', 
            aggfunc='sum'
        )
        inv_pivot.plot(kind='line', marker='o')
        plt.title('Inventory Levels by Facility and Product')
        plt.xlabel('Period')
        plt.ylabel('Inventory')
        plt.tight_layout()
        figures['inventory_analysis'] = plt.gcf()

        # Transportation Heatmap
        plt.figure(figsize=(12, 8))
        trans_df = results['transportation_df']
        trans_pivot = trans_df.pivot_table(
            index=['from_facility', 'to_facility'], 
            columns='product', 
            values='quantity', 
            aggfunc='sum'
        )
        sns.heatmap(trans_pivot, annot=True, cmap='YlGnBu')
        plt.title('Inter-Facility Transportation')
        plt.tight_layout()
        figures['transportation_heatmap'] = plt.gcf()

        # Workforce Composition
        plt.figure(figsize=(15, 10))
        workforce_df = results['workforce_df']
        workforce_pivot = workforce_df.pivot_table(
            index='facility', 
            columns='period', 
            values=['skilled_workforce', 'unskilled_workforce'], 
            aggfunc='sum'
        )
        workforce_pivot.plot(kind='bar', stacked=True)
        plt.title('Workforce Composition by Facility')
        plt.xlabel('Facility')
        plt.ylabel('Number of Workers')
        plt.tight_layout()
        figures['workforce_composition'] = plt.gcf()

        return figures


# method to create a comprehensive scenario for demonstration
def create_comprehensive_scenario():
    """
    Generate a comprehensive sample scenario for demonstration.
    """
    scenarios = {
        'Base_Scenario': {
            'facilities': ['Factory1', 'Factory2', 'Warehouse1'],
            'products': ['ProductA', 'ProductB'],
            'periods': list(range(6)),
            'initial_inventory': {
                'Factory1': {'ProductA': 100, 'ProductB': 50},
                'Factory2': {'ProductA': 75, 'ProductB': 25},
                'Warehouse1': {'ProductA': 50, 'ProductB': 30}
            },
            'demand': {
                'ProductA': {0: 120, 1: 140, 2: 160, 3: 130, 4: 110, 5: 150},
                'ProductB': {0: 80, 1: 90, 2: 110, 3: 100, 4: 85, 5: 95}
            },
            'workforce_params': {
                'min_skilled': 10,
                'max_hire': 5,
                'skill_mix_ratio': 0.4
            },
            'material_requirements': {
                'Raw_Material_A': {
                    'ProductA': 2,
                    'ProductB': 1,
                    'capacity': 500
                }
            },
            'cost_parameters': {
                'production_cost': {
                    'Factory1': {'ProductA': 10, 'ProductB': 12},
                    'Factory2': {'ProductA': 11, 'ProductB': 13}
                },
                'setup_cost': {
                    'Factory1': {'ProductA': 500, 'ProductB': 600},
                    'Factory2': {'ProductA': 550, 'ProductB': 650}
                },
                'transport_cost': {
                    'Factory1': {'Factory2': 5, 'Warehouse1': 3},
                    'Factory2': {'Factory1': 5, 'Warehouse1': 4}
                },
                'inventory_cost': {
                    'Factory1': {'ProductA': 2, 'ProductB': 2},
                    'Factory2': {'ProductA': 3, 'ProductB': 3}
                },
                'backlog_cost': {
                    'Factory1': {'ProductA': 20, 'ProductB': 20},
                    'Factory2': {'ProductA': 22, 'ProductB': 22}
                },
                'workforce_cost': {
                    'Factory1': {'skilled': 50, 'unskilled': 30},
                    'Factory2': {'skilled': 55, 'unskilled': 35}
                },
                'hire_cost': 1000,
                'fire_cost': 1500
            }
        },
        # Additional scenarios can be added here for comparison
    }

    model = AdvancedSupplyPlanningModel()
    return model.generate_scenario_comparison(scenarios)