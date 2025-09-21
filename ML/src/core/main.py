"""
Main entry point for the IRIS optimization system.
"""

import argparse
import json
from datetime import datetime

from .model import OptimizationModel
from .variables import TrainMovementVariables
from .constraints import MovementConstraints
from .objective import ObjectiveFunction

def load_config(config_path):
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    """Main function to run the IRIS optimization system."""
    parser = argparse.ArgumentParser(description='IRIS - Intelligent Railway Integration System')
    parser.add_argument('--config', type=str, required=True, help='Path to configuration JSON file')
    parser.add_argument('--output', type=str, default='results.json', help='Path to output results file')
    parser.add_argument('--time-horizon', type=int, default=60, help='Time horizon for optimization (minutes)')
    
    args = parser.parse_args()
    
    # Load configuration
    print(f"Loading configuration from {args.config}...")
    config = load_config(args.config)
    
    # Extract infrastructure and timetable data
    infrastructure = config['infrastructure']
    timetable = config['timetable']
    
    # Initialize and run optimization model
    print("Initializing optimization model...")
    start_time = datetime.now()
    
    model = OptimizationModel(infrastructure, timetable, args.time_horizon)
    solution = model.solve()
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"Optimization completed in {duration:.2f} seconds")
    
    if solution:
        print("Solution found!")
        
        # Save results
        with open(args.output, 'w') as f:
            json.dump(solution, f, indent=2)
        
        print(f"Results saved to {args.output}")
        
        # Print summary
        total_delay = sum(train['total_delay'] for train in solution.values())
        print(f"Total delay minimized: {total_delay} minutes")
        print(f"Number of trains scheduled: {len(solution)}")
    else:
        print("No solution found within given constraints.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())