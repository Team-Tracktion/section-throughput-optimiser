from core.model import RailwayScheduler
from generate_data import generate_random_data
import json
import yaml

def load_config():
    """Load configuration from YAML file."""
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {
            'default_time_limit': 10,
            'max_trains': 30,
            'horizon_multiplier': 8
        }

def run_scheduler(num_trains=None, time_limit=None, data_file=None):
    """Run scheduler with configurable parameters."""
    config = load_config()
    
    if data_file:
        with open(data_file, 'r') as f:
            data = json.load(f)
    else:
        num_trains = num_trains or config.get('max_trains', 20)
        data = generate_random_data(num_trains)
        # Adjust horizon based on train count
        data['horizon'] = num_trains * config.get('horizon_multiplier', 8)
    
    time_limit = time_limit or config.get('default_time_limit', 10)
    
    print(f"🚆 Running CP-SAT Scheduler")
    print(f"Trains: {len(data['trains'])} | Time limit: {time_limit} min | Horizon: {data['horizon']} min")
    
    scheduler = RailwayScheduler(data)
    scheduler.build_model()
    results = scheduler.solve(time_limit_minutes=time_limit)
    
    display_results(results, data)
    return results

def display_results(results, data):
    """Display results in a formatted way."""
    print("\n" + "="*60)
    
    if results['status'] == 4:
        print("✅ OPTIMAL SOLUTION FOUND!")
    elif results['status'] == 2:
        print("⚠️ FEASIBLE SOLUTION FOUND (may not be optimal)")
    else:
        print("❌ NO SOLUTION FOUND")
        return
    
    print(f"Objective value: {results['objective_value']}")
    print(f"Throughput: {results['throughput']}/{len(data['trains'])} trains")
    print(f"Solve time: {results['solve_time']:.2f} seconds")
    
    # Route usage statistics
    route_usage = {route: 0 for route in data['routes']}
    for train in results['schedule']:
        if train['completed'] and train['route']:
            route_usage[train['route']] += 1
    
    print(f"\nRoute usage:")
    for route, count in route_usage.items():
        print(f"  {route}: {count} trains")
    
    # Show sample schedule
    print(f"\nSample schedule (first 10 trains):")
    for train in results['schedule'][:10]:
        status = "✅" if train['completed'] else "❌"
        print(f"{status} {train['train_id']}: Start at {train['start_time']}, Route: {train['route']}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Railway Scheduler CP-SAT')
    parser.add_argument('--trains', type=int, help='Number of trains')
    parser.add_argument('--time', type=int, help='Time limit in minutes')
    parser.add_argument('--file', type=str, help='Input data file')
    
    args = parser.parse_args()
    run_scheduler(args.trains, args.time, args.file)