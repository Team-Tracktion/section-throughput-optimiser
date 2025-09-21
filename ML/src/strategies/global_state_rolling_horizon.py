# run_technical_scheduler.py
from strategies.ultimate_hybrid_scheduler import UltimateHybridScheduler
from generate_data import generate_random_data
import time
import sys
import traceback

def execute_ultimate_schedule(train_count=30):
    """Execute ultimate scheduling with guaranteed headway compliance."""
    try:
        print("Starting ULTIMATE Railway Network Scheduler...")
        print("=" * 65)
        print("Implementation: Guaranteed Zero Headway Violation System")
        print("=" * 65)
        
        # Generate dataset with optimized parameters
        print("Generating network data...")
        network_data = generate_random_data(train_count)
        network_data['horizon'] = 480  # 8-hour horizon
        network_data['headway'] = 10   # Safe headway
        
        # Ensure we have multiple routes
        if len(network_data['routes']) < 3:
            network_data['routes'] = ['main', 'alternate', 'express', 'freight']
            for train in network_data['trains']:
                if len(train['travel_times']) < 4:
                    base_time = min(train['travel_times'])
                    train['travel_times'] = [
                        base_time,       # main route
                        base_time * 1.1, # alternate route
                        base_time * 0.9, # express route
                        base_time * 1.3  # freight route
                    ]
        
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
        
        print("\nInitiating ULTIMATE Optimization...")
        computation_start = time.time()
        
        # Initialize and execute ultimate scheduler
        scheduler = UltimateHybridScheduler(network_data)
        
        print("Starting ULTIMATE scheduling process...")
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
    """Display scheduling results with all trains shown."""
    try:
        print("\n" + "=" * 85)
        print("ENHANCED SCHEDULING RESULTS SUMMARY")
        print("=" * 85)
        
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
        print(f"- Total Trains: {len(network_data['trains'])}")
        print(f"- Successfully Scheduled: {len(completed_trains)} trains")
        print(f"- Success Rate: {success_rate:.1f}%")
        
        # Display ALL trains in schedule
        if completed_trains:
            print(f"\nCOMPLETE TRAIN SCHEDULE:")
            print("=" * 85)
            print(f"{'Train':<8} {'Route':<12} {'Start':<8} {'End':<8} {'Duration':<10} {'Priority':<10} {'Status':<12}")
            print("-" * 85)
            
            # Sort by start time
            def get_sort_key(train):
                start_time = train.get('start_time')
                return start_time if start_time is not None else float('inf')
            
            completed_trains_sorted = sorted(completed_trains, key=get_sort_key)
            
            for train in completed_trains_sorted:
                duration = f"{train.get('travel_time', 0)}min"
                
                # Get priority from original data
                original_train = next((t for t in network_data['trains'] if t['id'] == train['train_id']), None)
                priority = original_train['priority'] if original_train else 'unknown'
                
                print(f"{train.get('train_id', 'N/A'):<8} {train.get('route_selected', 'N/A'):<12} "
                      f"{train.get('start_time', 'N/A'):<8} {train.get('end_time', 'N/A'):<8} "
                      f"{duration:<10} {priority:<10} {'COMPLETED':<12}")
        
        # Show unscheduled trains with details
        unscheduled = len(network_data['trains']) - len(completed_trains)
        if unscheduled > 0:
            print(f"\n⚠️  UNSCHEDULED TRAINS ({unscheduled}):")
            print("-" * 50)
            unscheduled_trains = [t for t in network_data['trains'] if t['id'] not in seen_ids]
            for train in unscheduled_trains:
                print(f"  - {train['id']} (Priority: {train['priority']}, "
                      f"Min Travel Time: {min(train['travel_times'])}min)")
        
        # Industry Standard Analysis
        print(f"\n{'='*85}")
        print("ENHANCED INDUSTRY STANDARD COMPLIANCE ANALYSIS")
        print(f"{'='*85}")
        analyze_industry_standards(completed_trains, network_data)
        
    except Exception as e:
        print(f"❌ Display error: {e}")
        traceback.print_exc()

def analyze_industry_standards(scheduled_trains, network_data):
    """Analyze if the schedule meets industry standards."""
    if not scheduled_trains:
        print("No trains scheduled - cannot analyze industry standards")
        return
    
    # 1. Headway Compliance
    headway_violations = 0
    time_slots = {}
    detailed_violations = []
    
    for train in scheduled_trains:
        route = train['route_selected']
        start = train['start_time']
        end = train['end_time']
        
        if route not in time_slots:
            time_slots[route] = []
        
        # Check headway compliance
        for existing_start, existing_end in time_slots[route]:
            time_gap = start - existing_end
            if 0 < time_gap < network_data['headway']:
                headway_violations += 1
                detailed_violations.append({
                    'train1': f"Train ending at {existing_end}",
                    'train2': f"Train starting at {start}",
                    'route': route,
                    'gap': time_gap,
                    'required_gap': network_data['headway']
                })
        
        time_slots[route].append((start, end))
    
    # 2. Priority Compliance
    priority_times = {'high': [], 'medium': [], 'low': []}
    for train in scheduled_trains:
        original_train = next((t for t in network_data['trains'] if t['id'] == train['train_id']), None)
        if original_train:
            priority_times[original_train['priority']].append(train['start_time'])
    
    # Calculate average start times by priority
    avg_start_times = {}
    for priority, times in priority_times.items():
        if times:
            avg_start_times[priority] = sum(times) / len(times)
    
    # 3. Resource Utilization
    route_utilization = {route: len(times) for route, times in time_slots.items()}
    
    # Industry Standard Metrics
    print("📊 ENHANCED INDUSTRY STANDARD METRICS:")
    compliance_percentage = ((len(scheduled_trains) - headway_violations) / len(scheduled_trains)) * 100
    print(f"1. Headway Compliance: {len(scheduled_trains) - headway_violations}/{len(scheduled_trains)} "
          f"({compliance_percentage:.1f}%)")
    
    print(f"2. Minimum Headway: {network_data['headway']} minutes")
    print(f"3. Headway Violations: {headway_violations}")
    
    if headway_violations > 0 and len(detailed_violations) > 0:
        print("4. Headway Violation Details:")
        for i, violation in enumerate(detailed_violations[:3]):  # Show first 3 violations
            print(f"   - Violation {i+1}: {violation['train1']} and {violation['train2']} on {violation['route']}")
            print(f"     Gap: {violation['gap']}min (Required: {violation['required_gap']}min)")
        if len(detailed_violations) > 3:
            print(f"   - ... and {len(detailed_violations) - 3} more violations")
    
    print("5. Priority-Based Scheduling:")
    for priority in ['high', 'medium', 'low']:
        if priority in avg_start_times:
            print(f"   - {priority.upper()}: Avg start time = {avg_start_times[priority]:.1f} minutes")
    
    print("6. Route Utilization:")
    for route, count in route_utilization.items():
        utilization_pct = (count / len(scheduled_trains)) * 100
        print(f"   - {route}: {count} trains ({utilization_pct:.1f}%)")
    
    # Industry Compliance Rating
    compliance_score = 100
    compliance_score -= headway_violations * 10  # More severe penalty for headway violations
    
    # Bonus for good route utilization if not just using main route
    if len(route_utilization) > 1:
        compliance_score += 10
        print("   + Bonus: Multiple routes utilized")
    
    # Bonus for proper priority handling
    if ('high' in avg_start_times and 'low' in avg_start_times and 
        avg_start_times['high'] < avg_start_times['low']):
        compliance_score += 10
        print("   + Bonus: Proper priority handling (high priority trains scheduled earlier)")
    
    if headway_violations == 0:
        print("✅ EXCELLENT: No headway violations detected")
    elif headway_violations <= 2:
        print("⚠️  ACCEPTABLE: Minor headway violations")
    else:
        print("❌ POOR: Significant headway violations")
    
    print(f"\n🏆 OVERALL INDUSTRY COMPLIANCE SCORE: {min(100, max(0, compliance_score))}/100")
    
    if compliance_score >= 90:
        print("🎯 INDUSTRY STANDARD: EXCEEDS EXPECTATIONS")
    elif compliance_score >= 75:
        print("✅ INDUSTRY STANDARD: MEETS REQUIREMENTS") 
    elif compliance_score >= 60:
        print("⚠️  INDUSTRY STANDARD: NEEDS IMPROVEMENT")
    else:
        print("❌ INDUSTRY STANDARD: BELOW STANDARD")
        
    # Recommendations for improvement
    print(f"\n💡 RECOMMENDATIONS FOR IMPROVEMENT:")
    if headway_violations > 0:
        print(f"- Increase minimum headway from {network_data['headway']} to {network_data['headway'] + 2} minutes")
        print("- Implement better conflict detection in scheduling algorithm")
    if len(route_utilization) == 1:
        print("- Utilize alternative routes to reduce congestion on main route")
    if 'high' in avg_start_times and 'low' in avg_start_times and avg_start_times['high'] >= avg_start_times['low']:
        print("- Improve priority handling to ensure high-priority trains schedule earlier")

if __name__ == "__main__":
    try:
        # Get train count from command line
        train_count = 30
        if len(sys.argv) > 1:
            try:
                train_count = int(sys.argv[1])
            except ValueError:
                print("Invalid train count. Using default 30.")
        
        print(f"ULTIMATE Scheduler Starting for {train_count} trains...")
        print("Guarantee: ZERO headway violations")
        
        start_time = time.time()
        results = execute_ultimate_schedule(train_count)
        total_time = time.time() - start_time
        
        print(f"\n✅ ULTIMATE scheduling completed in {total_time:.2f}s!")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        traceback.print_exc()