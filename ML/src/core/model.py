from ortools.sat.python import cp_model
from .variables import create_variables
from .constraints import add_constraints
from .objective import create_objective
import time

class RailwayScheduler:
    def __init__(self, data):
        self.data = data
        self.model = cp_model.CpModel()
        self.variables = None
        self.solver = cp_model.CpSolver()
        
    def build_model(self):
        """Build the complete CP-SAT model with optimizations."""
        self.variables = create_variables(self.model, self.data)
        self.model = add_constraints(self.model, self.data, self.variables)
        self.model = create_objective(self.model, self.data, self.variables)
        return self
    
    def solve(self, time_limit_minutes=10, verbose=True):
        """Solve with configurable time limit and optimizations."""
        # Set solver parameters for better performance
        self.solver.parameters.max_time_in_seconds = time_limit_minutes * 60
        self.solver.parameters.num_search_workers = 8  # Use multiple cores
        self.solver.parameters.log_search_progress = verbose
        
        if verbose:
            print(f"Solving with {len(self.data['trains'])} trains...")
            print(f"Time limit: {time_limit_minutes} minutes")
        
        start_time = time.time()
        status = self.solver.Solve(self.model)
        end_time = time.time()
        
        if verbose:
            print(f"Solver completed in {end_time - start_time:.2f} seconds")
        
        return self._extract_results(status)
    
    def _extract_results(self, status):
        """Extract and format results."""
        results = {
            'status': status,
            'solve_time': self.solver.WallTime(),
            'objective_value': self.solver.ObjectiveValue() if status == cp_model.OPTIMAL else None,
            'schedule': [],
            'throughput': 0
        }
        
        if status in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
            for i, train in enumerate(self.data['trains']):
                start_time = self.solver.Value(self.variables['T'][i])
                route_idx = None
                for r in range(len(self.data['routes'])):
                    if self.solver.Value(self.variables['x'][i][r]):
                        route_idx = r
                        break
                
                results['schedule'].append({
                    'train_id': train['id'],
                    'start_time': start_time,
                    'route': self.data['routes'][route_idx] if route_idx is not None else None,
                    'completed': bool(self.solver.Value(self.variables['flow'][i]))
                })
            
            results['throughput'] = sum(1 for train in results['schedule'] if train['completed'])
        
        return results