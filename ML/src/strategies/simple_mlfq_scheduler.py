# strategies/simple_mlfq_scheduler.py
from strategies.base_strategy import BaseSchedulingStrategy

class SimpleMLFQScheduler(BaseSchedulingStrategy):
    """Simple priority-based scheduler."""
    
    def solve(self):
        """Basic priority-based scheduling."""
        print("Simple MLFQ: Processing trains by priority")
        
        # Group trains by priority
        priority_groups = {'high': [], 'medium': [], 'low': []}
        for train in self.data['trains']:
            priority_groups[train['priority']].append(train)
        
        # Schedule in priority order
        current_time = 0
        for priority in ['high', 'medium', 'low']:
            for train in priority_groups[priority]:
                # Use fastest route
                travel_time = min(train['travel_times'])
                route_idx = train['travel_times'].index(travel_time)
                route = self.data['routes'][route_idx]
                
                end_time = current_time + travel_time
                can_schedule = end_time <= self.data['horizon']
                
                self.full_schedule.append({
                    'train_id': train['id'],
                    'route_selected': route if can_schedule else 'N/A',
                    'start_time': current_time if can_schedule else None,
                    'end_time': end_time if can_schedule else None,
                    'travel_time': travel_time,
                    'completion_status': can_schedule
                })
                
                if can_schedule:
                    current_time = end_time + self.data['headway']
        
        print(f"MLFQ completed: {sum(1 for t in self.full_schedule if t['completion_status'])} trains scheduled")
        return self.get_results()