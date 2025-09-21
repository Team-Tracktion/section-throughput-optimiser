# strategies/simple_mlfq_scheduler.py
from .base_strategy import BaseSchedulingStrategy

class SimpleMLFQScheduler(BaseSchedulingStrategy):
    """Fixed MLFQ scheduler without schedule conflicts."""
    
    def solve(self):
        """Conflict-free priority-based scheduling."""
        # Group trains by priority
        priority_groups = {'high': [], 'medium': [], 'low': []}
        for train in self.data['trains']:
            priority_groups[train['priority']].append(train)
        
        # Track used time slots to prevent conflicts
        used_time_slots = {}
        current_time = 0
        
        for priority in ['high', 'medium', 'low']:
            for train in priority_groups[priority]:
                # Use fastest available route
                travel_time = min(train['travel_times'])
                fastest_route_idx = train['travel_times'].index(travel_time)
                route = self.data['routes'][fastest_route_idx]
                
                # Find the next available time slot for this route
                if route in used_time_slots:
                    current_time = max(current_time, used_time_slots[route] + self.data['headway'])
                
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
                    # Update the next available time for this route
                    used_time_slots[route] = end_time
                    current_time = end_time + self.data['headway']
        
        return self.get_results()