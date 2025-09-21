"""
Energy-efficient strategy for train movement optimization.
"""

from ortools.sat.python import cp_model

class EnergyEfficientStrategy:
    """Optimization strategy focused on minimizing energy consumption."""
    
    def __init__(self, model, variables, infrastructure, timetable, time_horizon):
        """
        Initialize energy-efficient strategy.
        
        Args:
            model: CP-SAT model instance
            variables: TrainMovementVariables instance
            infrastructure: Dictionary containing infrastructure details
            timetable: Dictionary containing train timetable data
            time_horizon: Time horizon for optimization in minutes
        """
        self.model = model
        self.vars = variables
        self.infra = infrastructure
        self.timetable = timetable
        self.time_horizon = time_horizon
        
    def set_objective(self):
        """Set the objective function to minimize energy consumption."""
        print("Setting energy-efficient objective...")
        
        total_energy = 0
        
        for train_id in self.vars.train_ids:
            train_data = self.timetable['trains'][train_id]
            train_type = train_data['type']
            route = train_data['route']
            
            # Energy consumption factors by train type
            energy_factors = {
                'express': 1.0,
                'passenger': 0.8, 
                'freight': 1.2
            }
            base_energy = energy_factors.get(train_type, 1.0)
            
            # Calculate energy consumption for each section
            for i in range(len(route) - 1):
                current_section = route[i]
                next_section = route[i + 1]
                
                # Energy depends on section length and train type
                section_length = next(self.infra['sections']['id'] == current_section, None)['length']
                section_energy = base_energy * section_length
                
                # Add energy for each time step the train spends moving between sections
                for t in range(self.time_horizon - 1):
                    # If train leaves current section at time t, add energy
                    leaves_at_t = self.model.NewBoolVar(f'leaves_{train_id}_{current_section}_at_{t}')
                    
                    # Train leaves current section at time t if it's there at t but not at t+1
                    at_t = self.vars.occupancy[train_id][current_section][t]
                    at_t1 = self.vars.occupancy[train_id][current_section][t + 1]
                    self.model.Add(leaves_at_t == 1).OnlyEnforceIf([at_t, at_t1.Not()])
                    self.model.Add(leaves_at_t == 0).OnlyEnforceIf(at_t.Not())
                    self.model.Add(leaves_at_t == 0).OnlyEnforceIf(at_t1)
                    
                    # Add to total energy
                    total_energy += section_energy * leaves_at_t
        
        # Minimize total energy consumption
        self.model.Minimize(total_energy)
        print("Energy-efficient objective set.")