# strategies/global_state_manager.py
class GlobalStateManager:
    """Manages global state across all scheduling phases."""
    
    def __init__(self, network_data):
        self.network_data = network_data
        self.route_occupancy = {route: [] for route in network_data['routes']}
        self.scheduled_trains = set()
        
    def can_schedule_train(self, train_id, route, start_time, travel_time):
        """Check if a train can be scheduled without headway violations."""
        end_time = start_time + travel_time
        
        # Check against all existing scheduled trains on this route
        for occupied_start, occupied_end in self.route_occupancy[route]:
            # Check headway constraints in both directions
            if (abs(start_time - occupied_end) < self.network_data['headway'] or 
                abs(occupied_start - end_time) < self.network_data['headway']):
                return False
        return True
    
    def schedule_train(self, train_id, route, start_time, end_time):
        """Schedule a train and update global state."""
        self.route_occupancy[route].append((start_time, end_time))
        self.scheduled_trains.add(train_id)
        # Keep occupancy list sorted for efficient checking
        self.route_occupancy[route].sort(key=lambda x: x[0])
    
    def get_earliest_available_time(self, route, travel_time):
        """Get the earliest available time slot for a route."""
        if not self.route_occupancy[route]:
            return 0
        
        # Check gaps between existing schedules
        last_end = 0
        for start, end in self.route_occupancy[route]:
            gap = start - last_end
            if gap >= travel_time + self.network_data['headway']:
                return last_end + self.network_data['headway']
            last_end = end + self.network_data['headway']
        
        return last_end + self.network_data['headway']
    
    def verify_zero_violations(self):
        """Verify that there are zero headway violations."""
        violations = 0
        for route in self.network_data['routes']:
            schedules = self.route_occupancy[route]
            schedules.sort(key=lambda x: x[0])
            
            for i in range(1, len(schedules)):
                prev_end = schedules[i-1][1]
                curr_start = schedules[i][0]
                if curr_start - prev_end < self.network_data['headway']:
                    violations += 1
        
        return violations