import random
import json

def generate_random_data(num_trains):
    """Generate random data for railway scheduling problem."""
    
    # Define priorities and their weights
    priorities = ['high', 'medium', 'low']
    priority_distribution = [0.2, 0.3, 0.5]  # 20% high, 30% medium, 50% low
    
    # Define routes and their costs
    routes = ['main', 'diversion1', 'diversion2', 'diversion3']
    diversion_costs = [0, 15, 25, 35]  # Costs for each route
    
    # Generate trains
    trains = []
    for i in range(1, num_trains + 1):
        priority = random.choices(priorities, weights=priority_distribution)[0]
        
        # Base travel times (main route)
        base_travel_time = random.randint(20, 60)
        
        # Travel times for different routes (diversions take longer)
        travel_times = [
            base_travel_time,  # main route
            base_travel_time + random.randint(5, 15),  # diversion1
            base_travel_time + random.randint(10, 25),  # diversion2
            base_travel_time + random.randint(15, 35)   # diversion3
        ]
        
        # Scheduled time (spread out over 2 hours)
        scheduled_time = random.randint(0, 120)
        
        trains.append({
            'id': f'T{i:02d}',
            'priority': priority,
            'scheduled_time': scheduled_time,
            'travel_times': travel_times
        })
    
    # Create the complete data structure
    data = {
        'trains': trains,
        'routes': routes,
        'diversion_costs': diversion_costs,
        'headway': 5,  # 5 minutes headway between trains
        'horizon': 240,  # 4-hour planning horizon
        'alpha': 1.0,   # Delay weight
        'beta': 2.0,    # Diversion penalty
        'human_adjustments': []  # No human adjustments initially
    }
    
    return data


def save_data(data, filename='large_dataset.json'):
    """Save data to JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

def load_data(filename='large_dataset.json'):
    """Load data from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    # Generate and save data for 25 trains
    data = generate_random_data(25)
    save_data(data, '25_trains_dataset.json')
    
    # Print summary
    print(f"Generated data for {len(data['trains'])} trains")
    print(f"Routes available: {data['routes']}")
    print(f"Diversion costs: {data['diversion_costs']}")
    
    # Count trains by priority
    priority_count = {'high': 0, 'medium': 0, 'low': 0}
    for train in data['trains']:
        priority_count[train['priority']] += 1
    
    print(f"\nTrain priorities:")
    for priority, count in priority_count.items():
        print(f"  {priority}: {count} trains")
    
    print(f"\nPlanning horizon: {data['horizon']} minutes")
    print(f"Headway: {data['headway']} minutes")