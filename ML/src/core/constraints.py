"""
Constraint definitions for train movement optimization.
"""

from ortools.sat.python import cp_model
import numpy as np

class MovementConstraints:
    """Defines and applies constraints to the train movement optimization model."""
    
    def __init__(self, model, variables, infrastructure, timetable):
        """
        Initialize constraints.
        
        Args:
            model: CP-SAT model instance
            variables: TrainMovementVariables instance
            infrastructure: Dictionary containing infrastructure details
            timetable: Dictionary containing train timetable data
        """
        self.model = model
        self.vars = variables
        self.infra = infrastructure
        self.timetable = timetable
        
    def apply_safety_constraints(self):
        """Apply safety constraints (no two trains on same track section at same time)."""
        print("Applying safety constraints...")
        
        # For each track section and each time step, ensure at most one train occupies it
        for section in self.infra['sections']:
            for t in range(self.vars.time_horizon):
                trains_in_section = []
                for train_id in self.vars.train_ids:
                    # Check if this train occupies the section at time t
                    occupies = self.vars.occupancy[train_id][section['id']][t]
                    trains_in_section.append(occupies)
                
                # Add constraint: at most one train can be in this section at time t
                if trains_in_section:
                    self.model.AddAtMostOne(trains_in_section)
    
    def apply_headway_constraints(self):
        """Apply minimum headway constraints between trains."""
        print("Applying headway constraints...")
        
        min_headway = self.infra.get('min_headway_time', 3)  # default 3 minutes
        
        for section in self.infra['sections']:
            section_id = section['id']
            for train1_id in self.vars.train_ids:
                for train2_id in self.vars.train_ids:
                    if train1_id >= train2_id:
                        continue  # avoid duplicate constraints
                    
                    # For each time step, ensure proper headway
                    for t in range(self.vars.time_horizon - min_headway):
                        # If train1 occupies section at time t, train2 cannot occupy
                        # same section until time t + min_headway
                        train1_occupies = self.vars.occupancy[train1_id][section_id][t]
                        for delta in range(1, min_headway + 1):
                            if t + delta < self.vars.time_horizon:
                                train2_occupies = self.vars.occupancy[train2_id][section_id][t + delta]
                                # Implication: if train1 occupies, then train2 cannot occupy within headway
                                self.model.AddImplication(train1_occupies, train2_occupies.Not())
    
    def apply_junction_constraints(self):
        """Apply constraints for junctions and conflicting routes."""
        print("Applying junction constraints...")
        
        for junction in self.infra.get('junctions', []):
            conflicting_routes = junction.get('conflicting_routes', [])
            
            for route1, route2 in conflicting_routes:
                for t in range(self.vars.time_horizon):
                    # Count how many trains are using each conflicting route
                    trains_on_route1 = []
                    trains_on_route2 = []
                    
                    for train_id in self.vars.train_ids:
                        # Check if train is on route1 at time t
                        on_route1 = self.model.NewBoolVar(f'train_{train_id}_on_{route1}_at_{t}')
                        # This would need to be defined based on actual route variables
                        trains_on_route1.append(on_route1)
                        
                        # Check if train is on route2 at time t
                        on_route2 = self.model.NewBoolVar(f'train_{train_id}_on_{route2}_at_{t}')
                        trains_on_route2.append(on_route2)
                    
                    # At most one route can be active at a time
                    route1_active = self.model.NewBoolVar(f'{route1}_active_at_{t}')
                    self.model.Add(sum(trains_on_route1) >= 1).OnlyEnforceIf(route1_active)
                    self.model.Add(sum(trains_on_route1) == 0).OnlyEnforceIf(route1_active.Not())
                    
                    route2_active = self.model.NewBoolVar(f'{route2}_active_at_{t}')
                    self.model.Add(sum(trains_on_route2) >= 1).OnlyEnforceIf(route2_active)
                    self.model.Add(sum(trains_on_route2) == 0).OnlyEnforceIf(route2_active.Not())
                    
                    # Conflicting routes cannot be active simultaneously
                    self.model.AddAtMostOne([route1_active, route2_active])
    
    def apply_travel_time_constraints(self):
        """Apply constraints related to minimum travel times between sections."""
        print("Applying travel time constraints...")
        
        for train_id in self.vars.train_ids:
            train_data = self.timetable['trains'][train_id]
            train_type = train_data['type']
            
            # Get minimum travel times for this train type
            min_travel_times = self.infra['min_travel_times'].get(train_type, {})
            
            # For each consecutive section pair in the train's route
            route = train_data['route']
            for i in range(len(route) - 1):
                current_section = route[i]
                next_section = route[i + 1]
                
                min_time = min_travel_times.get(f"{current_section}-{next_section}", 2)  # default 2 minutes
                
                # For each time t, if train is in current_section at time t,
                # it cannot be in next_section before time t + min_time
                for t in range(self.vars.time_horizon - min_time):
                    in_current = self.vars.occupancy[train_id][current_section][t]
                    for early_arrival in range(1, min_time):
                        if t + early_arrival < self.vars.time_horizon:
                            in_next_early = self.vars.occupancy[train_id][next_section][t + early_arrival]
                            self.model.AddImplication(in_current, in_next_early.Not())
    
    def apply_all_constraints(self):
        """Apply all constraints to the model."""
        self.apply_safety_constraints()
        self.apply_headway_constraints()
        self.apply_junction_constraints()
        self.apply_travel_time_constraints()
        print("All constraints applied successfully.")