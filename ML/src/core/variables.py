"""
Variable definitions for train movement optimization.
"""

from ortools.sat.python import cp_model

class TrainMovementVariables:
    """Manages decision variables for train movement optimization."""
    
    def __init__(self, model, infrastructure, timetable, time_horizon):
        """
        Initialize variables manager.
        
        Args:
            model: CP-SAT model instance
            infrastructure: Dictionary containing infrastructure details
            timetable: Dictionary containing train timetable data
            time_horizon: Time horizon for optimization in minutes
        """
        self.model = model
        self.infra = infrastructure
        self.timetable = timetable
        self.time_horizon = time_horizon
        
        # Extract train IDs
        self.train_ids = list(timetable['trains'].keys())
        
        # Variables storage
        self.occupancy = {}  # occupancy[train_id][section_id][time] = BoolVar
        self.departure_times = {}  # departure_times[train_id][section_id] = IntVar
        
    def create_variables(self):
        """Create all decision variables for the model."""
        print("Creating decision variables...")
        
        # Create occupancy variables: for each train, each section, each time step
        self.occupancy = {}
        
        for train_id in self.train_ids:
            train_data = self.timetable['trains'][train_id]
            self.occupancy[train_id] = {}
            
            # Only create variables for sections in the train's route
            for section_id in train_data['route']:
                self.occupancy[train_id][section_id] = [
                    self.model.NewBoolVar(f'occ_{train_id}_{section_id}_{t}')
                    for t in range(self.time_horizon)
                ]
        
        # Create departure time variables for each train from each section
        self.departure_times = {}
        
        for train_id in self.train_ids:
            train_data = self.timetable['trains'][train_id]
            self.departure_times[train_id] = {}
            
            for section_id in train_data['route']:
                # Departure time from this section (when the train stops occupying it)
                self.departure_times[train_id][section_id] = self.model.NewIntVar(
                    0, self.time_horizon, f'dep_{train_id}_{section_id}'
                )
                
                # Link departure time to occupancy variables
                for t in range(self.time_horizon):
                    # If train occupies section at time t but not at time t+1, then departure_time = t
                    if t < self.time_horizon - 1:
                        occupies_t = self.occupancy[train_id][section_id][t]
                        occupies_t1 = self.occupancy[train_id][section_id][t + 1]
                        
                        # If occupies at t but not at t+1, then departure time = t
                        self.model.Add(self.departure_times[train_id][section_id] == t).OnlyEnforceIf(
                            [occupies_t, occupies_t1.Not()])
        
        print(f"Created variables for {len(self.train_ids)} trains across {self._count_sections()} sections")
    
    def _count_sections(self):
        """Count total number of section variables created."""
        count = 0
        for train_id in self.occupancy:
            count += len(self.occupancy[train_id])
        return count