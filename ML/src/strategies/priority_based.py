"""
Priority-based strategy for train movement optimization.
"""

from ortools.sat.python import cp_model
from .utils.constants import TRAIN_PRIORITIES

class PriorityBasedStrategy:
    """Optimization strategy focused on prioritizing higher priority trains."""
    
    def __init__(self, model, variables, timetable, time_horizon):
        """
        Initialize priority-based strategy.
        
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
        """Set the objective function to prioritize higher priority trains."""
        print("Setting priority-based objective...")
        
        # Create a score for each train based on priority and progress
        total_score = 0
        
        for train_id in self.vars.train_ids:
            train_data = self.timetable['trains'][train_id]
            priority = train_data['priority']
            route = train_data['route']
            
            # Score based on how far the train progresses in its route
            for i, section_id in enumerate(route):
                section_progress = i / len(route)  # Normalized progress (0 to 1)
                
                # For each time step, if train is in this section, add to score
                for t in range(self.time_horizon):
                    # Score = priority * progress * (1 - normalized time)
                    time_factor = 1 - (t / self.time_horizon)  # Earlier is better
                    score = priority * section_progress * time_factor
                    
                    # Add to total score if train occupies this section at this time
                    occupancy = self.vars.occupancy[train_id][section_id][t]
                    total_score += score * occupancy
        
        # Maximize the total priority-weighted progress score
        self.model.Maximize(total_score)
        print("Priority-based objective set.")