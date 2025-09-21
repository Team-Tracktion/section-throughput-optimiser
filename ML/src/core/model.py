"""
Main optimization model for train movement scheduling.
"""

from ortools.sat.python import cp_model
from .variables import TrainMovementVariables
from .constraints import MovementConstraints
from .objective import ObjectiveFunction

class OptimizationModel:
    """Main optimization model for train movement scheduling."""
    
    def __init__(self, infrastructure, timetable, time_horizon=60):
        """
        Initialize the optimization model.
        
        Args:
            infrastructure: Dictionary containing infrastructure details
            timetable: Dictionary containing train timetable data
            time_horizon: Time horizon for optimization in minutes
        """
        self.model = cp_model.CpModel()
        self.infra = infrastructure
        self.timetable = timetable
        self.time_horizon = time_horizon
        
        # Initialize variables, constraints, and objective
        self.variables = TrainMovementVariables(self.model, infrastructure, timetable, time_horizon)
        self.constraints = MovementConstraints(self.model, self.variables, infrastructure, timetable)
        self.objective = ObjectiveFunction(self.model, self.variables, timetable)
        
        # Build the model
        self._build_model()
    
    def _build_model(self):
        """Build the complete optimization model."""
        print("Building optimization model...")
        
        # Create variables
        self.variables.create_variables()
        
        # Apply constraints
        self.constraints.apply_all_constraints()
        
        # Set objective
        self.objective.set_objective()
        
        print("Model built successfully.")
    
    def solve(self, time_limit=30):
        """
        Solve the optimization model.
        
        Args:
            time_limit: Maximum time to spend solving in seconds
            
        Returns:
            Dictionary containing the solution if found, None otherwise
        """
        print(f"Solving model (time limit: {time_limit}s)...")
        
        # Create solver and solve
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit
        solver.parameters.num_search_workers = 8  # Use multiple cores
        
        status = solver.Solve(self.model)
        
        # Check solution status
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            print("Solution found!")
            return self._extract_solution(solver)
        else:
            print(f"No solution found. Status: {solver.StatusName(status)}")
            return None
    
    def _extract_solution(self, solver):
        """
        Extract solution from the solver.
        
        Args:
            solver: CP-SAT solver instance with solution
            
        Returns:
            Dictionary containing the solution
        """
        solution = {}
        
        for train_id in self.variables.train_ids:
            train_solution = {
                'id': train_id,
                'type': self.timetable['trains'][train_id]['type'],
                'priority': self.timetable['trains'][train_id]['priority'],
                'schedule': [],
                'total_delay': 0
            }
            
            # Find arrival time at destination
            dest_section = self.timetable['trains'][train_id]['route'][-1]
            for t in range(self.time_horizon):
                if solver.Value(self.variables.occupancy[train_id][dest_section][t]):
                    arrival_time = t
                    break
            else:
                arrival_time = self.time_horizon  # Didn't reach destination
            
            scheduled_arrival = self.timetable['trains'][train_id]['scheduled_arrival']
            train_solution['actual_arrival'] = arrival_time
            train_solution['scheduled_arrival'] = scheduled_arrival
            train_solution['delay'] = max(0, arrival_time - scheduled_arrival)
            train_solution['total_delay'] = train_solution['delay']
            
            # Record occupancy for each section
            for section_id in self.variables.occupancy[train_id]:
                entry_time = None
                exit_time = None
                
                for t in range(self.time_horizon):
                    if solver.Value(self.variables.occupancy[train_id][section_id][t]):
                        if entry_time is None:
                            entry_time = t
                        exit_time = t
                
                if entry_time is not None:
                    train_solution['schedule'].append({
                        'section': section_id,
                        'entry_time': entry_time,
                        'exit_time': exit_time,
                        'duration': exit_time - entry_time + 1
                    })
            
            solution[train_id] = train_solution
        
        return solution