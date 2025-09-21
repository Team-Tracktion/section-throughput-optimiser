"""
Delay minimization strategy for train movement optimization.
"""

from ortools.sat.python import cp_model
from .utils.constants import TRAIN_PRIORITIES

class DelayMinimizationStrategy:
    """Optimization strategy focused on minimizing total weighted delay."""
    
    def __init__(self, model, variables, timetable, time_horizon):
        """
        Initialize delay minimization strategy.
        
        Args:
            model: CP-SAT model instance
            variables: TrainMovementVariables instance
            timetable: Dictionary containing train timetable data
            time_horizon: Time horizon for optimization in minutes
        """
        self.model = model
        self.vars = variables
        self.timetable = timetable
        self.time_horizon = time_horizon
        
    def set_objective(self):
        """Set the objective function to minimize total weighted delay."""
        print("Setting delay minimization objective...")
        
        total_delay = 0
        
        for train_id in self.vars.train_ids:
            train_data = self.timetable['trains'][train_id]
            priority = train_data['priority']
            scheduled_arrival = train_data['scheduled_arrival']
            
            # The actual arrival time is the first time the train occupies its destination section
            dest_section = train_data['route'][-1]
            
            # Create a variable for arrival time
            arrival_time = self.model.NewIntVar(0, self.time_horizon, f'arrival_time_{train_id}')
            
            # Link arrival_time to occupancy variables
            occupancy_vars = self.vars.occupancy[train_id][dest_section]
            for t in range(self.time_horizon):
                # If train occupies destination at time t, then arrival_time <= t
                self.model.Add(arrival_time <= t).OnlyEnforceIf(occupancy_vars[t])
                # And arrival_time should be the first time it arrives
                if t > 0:
                    # If it wasn't there at t-1 but is there at t, then arrival_time >= t
                    was_occupied = occupancy_vars[t-1]
                    is_occupied = occupancy_vars[t]
                    self.model.Add(arrival_time >= t).OnlyEnforceIf([is_occupied, was_occupied.Not()])
            
            # Calculate delay (max(0, arrival_time - scheduled_arrival))
            delay = self.model.NewIntVar(0, self.time_horizon, f'delay_{train_id}')
            self.model.Add(delay >= arrival_time - scheduled_arrival)
            self.model.Add(delay >= 0)
            
            # Add to total delay with priority weighting
            # Higher priority trains have higher weight (more important to minimize their delay)
            weight = 10 * priority  # Adjust weighting as needed
            weighted_delay = delay * weight
            total_delay += weighted_delay
        
        # Set the objective to minimize total weighted delay
        self.model.Minimize(total_delay)
        print("Delay minimization objective set.")