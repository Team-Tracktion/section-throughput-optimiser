# File: optimized_model.py
from ortools.sat.python import cp_model
import time

class OptimizedRailwayScheduler:
    def __init__(self, data):
        self.data = data
        self.model = cp_model.CpModel()
        self.variables = None
        self.solver = cp_model.CpSolver()
        
    def build_model(self):
        """Build model with optimizations."""
        # ... [same as before but with these optimizations]:
        
        # Enable solver optimizations
        self.solver.parameters.num_search_workers = 8  # Use multiple cores
        self.solver.parameters.log_search_progress = True
        
    def solve(self, time_limit_minutes=5):
        """Solve with time limit."""
        self.solver.parameters.max_time_in_seconds = time_limit_minutes * 60
        
        start_time = time.time()
        status = self.solver.Solve(self.model)
        end_time = time.time()
        
        print(f"Solver ran for {end_time - start_time:.2f} seconds")
        
        # ... [rest same as before]