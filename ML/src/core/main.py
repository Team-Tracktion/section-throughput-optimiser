from .model import RailwayScheduler

def main():
    """Main function to run the railway scheduler."""
    # Example data structure
    data = {
        'trains': [
            {'id': 'T1', 'priority': 'high', 'scheduled_time': 0, 'travel_times': [30, 40]},
            {'id': 'T2', 'priority': 'low', 'scheduled_time': 5, 'travel_times': [35, 45]},
            {'id': 'T3', 'priority': 'medium', 'scheduled_time': 10, 'travel_times': [25, 35]}
        ],
        'routes': ['main', 'diversion1'],
        'diversion_costs': [0, 10],  # Cost for each route
        'headway': 5,  # Minimum time between trains on same route
        'horizon': 100,  # Planning horizon
        'alpha': 1.0,  # Delay weight
        'beta': 2.0,   # Diversion penalty
        'human_adjustments': []  # Optional human adjustments
    }
    
    # Create and solve the model
    scheduler = RailwayScheduler(data)
    scheduler.build_model()
    results = scheduler.solve()
    
    # Print results
    if results['status'] == 4:  # OPTIMAL
        print("Optimal solution found!")
        print(f"Objective value: {results['objective_value']}")
        print(f"Throughput: {results['throughput']} trains")
        print("\nSchedule:")
        for train in results['schedule']:
            print(f"Train {train['train_id']}: Start at {train['start_time']}, "
                  f"Route: {train['route']}, Completed: {train['completed']}")
    else:
        print("No optimal solution found.")
        print(f"Solver status: {results['status']}")

if __name__ == "__main__":
    main()