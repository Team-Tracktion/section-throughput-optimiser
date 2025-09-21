# run_technical_scheduler.py
from strategies.hybrid_scheduler import HybridScheduler
from generate_data import generate_random_data
import time
import sys
import traceback

def execute_hybrid_schedule(train_count=30):
    """Execute hybrid MLFQ + Rolling Horizon scheduling."""
    try:
        print("Starting Railway Network Hybrid Scheduler...")
        print("=" * 60)
        
        # Generate dataset
        print("Generating network data...")
        network_data = generate_random_data(train_count)
        network_data['horizon'] = 300
        
        print(f"Network Configuration:")
        print(f"- Total Trains: {train_count}")
        print(f"- Available Routes: {len(network_data['routes'])}")
        print(f"- Planning Horizon: {network_data['horizon']} minutes")
        print(f"- Minimum Headway: {network_data['headway']} minutes")
        
        # Priority distribution
        high_priority = sum(1 for train in network_data['trains'] if train['priority'] == 'high')
        medium_priority = sum(1 for train in network_data['trains'] if train['priority'] == 'medium')
        low_priority = train_count - high_priority - medium_priority
        
        print(f"\nTrain Priority Distribution:")
        print(f"- High Priority: {high_priority} trains")
        print(f"- Medium Priority: {medium_priority} trains") 
        print(f"- Low Priority: {low_priority} trains")
        
        print("\nInitiating Hybrid Optimization...")
        computation_start = time.time()
        
        # Initialize and execute hybrid scheduler
        scheduler = HybridScheduler(network_data)
        
        print("Starting hybrid MLFQ + Rolling Horizon process...")
        scheduling_results = scheduler.solve()
        computation_time = time.time() - computation_start
        
        # Display results
        display_hybrid_results(scheduling_results, network_data, computation_time)
        
        return scheduling_results
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return {'schedule': [], 'throughput': 0}

def display_hybrid_results(results, network_data, comp_time):
    """Display scheduling results."""
    try:
        print("\n" + "=" * 70)
        print("SCHEDULING RESULTS SUMMARY")
        print("=" * 70)
        
        # Count completed trains
        completed_trains = []
        seen_ids = set()
        
        if 'schedule' in results:
            for t in results['schedule']:
                if (t.get('completion_status', False) and 
                    'train_id' in t and 
                    t['train_id'] not in seen_ids):
                    completed_trains.append(t)
                    seen_ids.add(t['train_id'])
        
        success_rate = (len(completed_trains) / len(network_data['trains'])) * 100
        success_rate = min(success_rate, 100.0)
        
        print(f"Performance Metrics:")
        print(f"- Solve Time: {comp_time:.2f}s")
        print(f"- Trains: {len(network_data['trains'])}")
        print(f"- Success: {len(completed_trains)}/{len(network_data['trains'])} ({success_rate:.1f}%)")
        
        # Display schedule
        if completed_trains:
            print(f"\nTRAIN SCHEDULE:")
            print("=" * 70)
            print(f"{'Train':<6} {'Route':<10} {'Start':<6} {'End':<6} {'Dur':<4} {'Status':<10}")
            print("-" * 70)
            
            # Sort by start time
            def get_sort_key(train):
                start_time = train.get('start_time')
                return start_time if start_time is not None else float('inf')
            
            completed_trains_sorted = sorted(completed_trains, key=get_sort_key)
            
            for train in completed_trains_sorted[:10]:  # Show first 10 only
                duration = f"{train.get('travel_time', 0)}m"
                print(f"{train.get('train_id', 'N/A'):<6} {train.get('route_selected', 'N/A'):<10} "
                      f"{train.get('start_time', 'N/A'):<6} {train.get('end_time', 'N/A'):<6} "
                      f"{duration:<4} {'COMPLETED':<10}")
            
            if len(completed_trains) > 10:
                print(f"... and {len(completed_trains) - 10} more trains")
        
        # Show unscheduled trains
        unscheduled = len(network_data['trains']) - len(completed_trains)
        if unscheduled > 0:
            print(f"\n⚠️  {unscheduled} trains could not be scheduled")
            
    except Exception as e:
        print(f"❌ Display error: {e}")

if __name__ == "__main__":
    try:
        # Get train count from command line
        train_count = 30
        if len(sys.argv) > 1:
            try:
                train_count = int(sys.argv[1])
            except ValueError:
                print("Invalid train count. Using default 30.")
        
        print(f"Hybrid Scheduler Starting for {train_count} trains...")
        
        # Simple timeout check
        start_time = time.time()
        timeout_seconds = 300
        
        results = execute_hybrid_schedule(train_count)
        
        if time.time() - start_time > timeout_seconds:
            print("⏰ Scheduling took too long, but completed")
        
        print("\n✅ Scheduling completed!")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        traceback.print_exc()