"""
Throughput maximization strategy for train movement optimization.
"""

from ortools.sat.python import cp_model

class ThroughputMaximizationStrategy:
    """Optimization strategy focused on maximizing section throughput."""
    
    def __init__(self, model, variables, infrastructure, time_horizon):
        """
        Initialize throughput maximization strategy.
        
        Args:
            model: CP-SAT model instance
            variables: TrainMovementVariables instance
            infrastructure: Dictionary containing infrastructure details
            time_horizon: Time horizon for optimization in minutes
        """
        self.model = model
        self.vars = variables
        self.infra = infrastructure
        self.time_horizon = time_horizon
        
    def set_objective(self):
        """Set the objective function to maximize throughput."""
        print("Setting throughput maximization objective...")
        
        # Maximize the number of trains that complete their journey within time horizon
        trains_completed = []
        
        for train_id in self.vars.train_ids:
            dest_section = self.vars.timetable['trains'][train_id]['route'][-1]
            
            # Check if train reaches destination by end of time horizon
            reaches_destination = self.model.NewBoolVar(f'reaches_dest_{train_id}')
            
            # Train reaches destination if it occupies the destination section at any time
            dest_occupancy = self.vars.occupancy[train_id][dest_section]
            self.model.AddMaxEquality(reaches_destination, dest_occupancy)
            
            trains_completed.append(reaches_destination)
        
        # Maximize the number of trains that complete their journey
        self.model.Maximize(sum(trains_completed))
        print("Throughput maximization objective set.")