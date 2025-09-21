# strategies/advanced_hybrid_scheduler.py
from strategies.hybrid_scheduler import HybridScheduler
import time

class AdvancedHybridScheduler(HybridScheduler):
    """Advanced hybrid scheduler with strict headway enforcement."""
    
    def __init__(self, data):
        super().__init__(data)
        # Track last end time for each route to enforce headway
        self.route_last_end = {route: 0 for route in self.data['routes']}
        
    def solve(self):
        """Advanced scheduling with strict headway enforcement."""
        print("Using Advanced Hybrid approach with strict headway enforcement")
        
        # Enhanced MLFQ with headway enforcement
        print("Phase 1: Advanced MLFQ with Headway Enforcement")
        mlfq_results = self._advanced_mlfq()
        
        # Get scheduled trains
        scheduled_ids = {t['train_id'] for t in mlfq_results['schedule'] if t.get('completion_status', False)}
        
        # Identify unscheduled trains
        unscheduled_trains = [t for t in self.data['trains'] if t['id'] not in scheduled_ids]
        
        if unscheduled_trains:
            print(f"Phase 2: Advanced Rolling Horizon for {len(unscheduled_trains)} remaining trains")
            
            # Enhanced Rolling Horizon with headway enforcement
            remaining_data = {
                'trains': unscheduled_trains,
                'routes': self.data['routes'],
                'headway': self.data['headway'],
                'horizon': self.data['horizon']
            }
            
            # Use advanced rolling horizon
            rh_results = self._advanced_rolling_horizon(remaining_data)
            
            # Combine results
            self.full_schedule = mlfq_results['schedule'] + rh_results['schedule']
        else:
            self.full_schedule = mlfq_results['schedule']
            print("All trains scheduled by Advanced MLFQ")
        
        return self.get_results()
    
    def _advanced_mlfq(self):
        """MLFQ with strict headway enforcement."""
        # Group trains by priority
        priority_groups = {'high': [], 'medium': [], 'low': []}
        for train in self.data['trains']:
            priority_groups[train['priority']].append(train)
        
        # Schedule in priority order with headway enforcement
        for priority in ['high', 'medium', 'low']:
            for train in priority_groups[priority]:
                # Try all routes to find the best available slot
                best_route = None
                best_start_time = float('inf')
                best_travel_time = float('inf')
                
                for i, travel_time in enumerate(train['travel_times']):
                    route = self.data['routes'][i]
                    # Calculate earliest possible start time for this route
                    earliest_start = self.route_last_end[route] + self.data['headway']
                    end_time = earliest_start + travel_time
                    
                    # Check if this route is feasible and better than current best
                    if (end_time <= self.data['horizon'] and 
                        earliest_start < best_start_time):
                        best_route = route
                        best_start_time = earliest_start
                        best_travel_time = travel_time
                
                # Schedule the train if a feasible route was found
                if best_route:
                    end_time = best_start_time + best_travel_time
                    self.full_schedule.append({
                        'train_id': train['id'],
                        'route_selected': best_route,
                        'start_time': best_start_time,
                        'end_time': end_time,
                        'travel_time': best_travel_time,
                        'completion_status': True
                    })
                    # Update the last end time for this route
                    self.route_last_end[best_route] = end_time
        
        return self.get_results()
    
    def _advanced_rolling_horizon(self, data):
        """Advanced rolling horizon with headway enforcement."""
        # Implementation would go here
        # For now, use the parent class implementation
        return super().solve()