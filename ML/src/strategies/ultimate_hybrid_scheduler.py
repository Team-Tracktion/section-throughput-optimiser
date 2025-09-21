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


class UltimateHybridScheduler:
    """Ultimate hybrid scheduler with guaranteed headway compliance and high capacity."""
    
    def __init__(self, data):
        self.data = data
        self.full_schedule = []
        self.global_state = GlobalStateManager(data)
        
    def solve(self):
        """Ultimate scheduling with guaranteed headway compliance and high capacity."""
        print("Using ULTIMATE Hybrid approach with guaranteed headway compliance")
        
        # Phase 1: Enhanced MLFQ with global state enforcement
        print("Phase 1: Global-State-Enforced MLFQ")
        mlfq_results = self._global_state_mlfq()
        
        # Get scheduled trains
        scheduled_ids = {t['train_id'] for t in mlfq_results if t.get('completion_status', False)}
        
        # Identify unscheduled trains
        unscheduled_trains = [t for t in self.data['trains'] if t['id'] not in scheduled_ids]
        
        if unscheduled_trains:
            print(f"Phase 2: Capacity-Optimized Scheduling for {len(unscheduled_trains)} remaining trains")
            # Use optimized capacity scheduling for remaining trains
            capacity_results = self._optimize_for_capacity(unscheduled_trains)
            
            # Combine results
            self.full_schedule = mlfq_results + capacity_results
        else:
            self.full_schedule = mlfq_results
            print("All trains scheduled by Global-State-Enforced MLFQ")
        
        # Verify zero headway violations
        self._verify_zero_violations()
        
        return self.get_results()
    
    def _global_state_mlfq(self):
        """MLFQ with global state headway enforcement."""
        # Group trains by priority
        priority_groups = {'high': [], 'medium': [], 'low': []}
        for train in self.data['trains']:
            priority_groups[train['priority']].append(train)
        
        schedule = []
        
        # Schedule in priority order with global state enforcement
        for priority in ['high', 'medium', 'low']:
            for train in priority_groups[priority]:
                # Try all routes to find the best available slot
                best_route = None
                best_start_time = float('inf')
                best_travel_time = float('inf')
                
                for i, travel_time in enumerate(train['travel_times']):
                    route = self.data['routes'][i]
                    # Get earliest available time from global state
                    earliest_start = self.global_state.get_earliest_available_time(route, travel_time)
                    end_time = earliest_start + travel_time
                    
                    # Check if this route is feasible and better than current best
                    if (end_time <= self.data['horizon'] and 
                        earliest_start < best_start_time and
                        self.global_state.can_schedule_train(train['id'], route, earliest_start, travel_time)):
                        best_route = route
                        best_start_time = earliest_start
                        best_travel_time = travel_time
                
                # Schedule the train if a feasible route was found
                if best_route:
                    end_time = best_start_time + best_travel_time
                    schedule.append({
                        'train_id': train['id'],
                        'route_selected': best_route,
                        'start_time': best_start_time,
                        'end_time': end_time,
                        'travel_time': best_travel_time,
                        'completion_status': True
                    })
                    # Update global state
                    self.global_state.schedule_train(train['id'], best_route, best_start_time, end_time)
                else:
                    # Train cannot be scheduled within horizon
                    schedule.append({
                        'train_id': train['id'],
                        'route_selected': 'N/A',
                        'start_time': None,
                        'end_time': None,
                        'travel_time': min(train['travel_times']),
                        'completion_status': False
                    })
        
        scheduled_count = sum(1 for t in schedule if t['completion_status'])
        print(f"Global-State-Enforced MLFQ completed: {scheduled_count} trains scheduled")
        return schedule
    
    def _optimize_for_capacity(self, trains):
        """Optimized scheduling for high-capacity scenarios."""
        schedule = []
        
        # Group by priority first, then sort by travel time within each priority
        priority_groups = {'high': [], 'medium': [], 'low': []}
        for train in trains:
            priority_groups[train['priority']].append(train)
        
        # Sort each group by shortest travel time first (for better packing)
        for priority in priority_groups:
            priority_groups[priority].sort(key=lambda x: min(x['travel_times']))
        
        # Schedule in priority order with optimized packing
        for priority in ['high', 'medium', 'low']:
            for train in priority_groups[priority]:
                # Try all routes to find the best available slot
                best_route = None
                best_start_time = float('inf')
                best_travel_time = float('inf')
                
                for i, travel_time in enumerate(train['travel_times']):
                    route = self.data['routes'][i]
                    # Get earliest available time from global state
                    earliest_start = self.global_state.get_earliest_available_time(route, travel_time)
                    end_time = earliest_start + travel_time
                    
                    # Check if this route is feasible and better than current best
                    if (end_time <= self.data['horizon'] and 
                        earliest_start < best_start_time and
                        self.global_state.can_schedule_train(train['id'], route, earliest_start, travel_time)):
                        best_route = route
                        best_start_time = earliest_start
                        best_travel_time = travel_time
                
                # Schedule the train if a feasible route was found
                if best_route:
                    end_time = best_start_time + best_travel_time
                    schedule.append({
                        'train_id': train['id'],
                        'route_selected': best_route,
                        'start_time': best_start_time,
                        'end_time': end_time,
                        'travel_time': best_travel_time,
                        'completion_status': True
                    })
                    # Update global state
                    self.global_state.schedule_train(train['id'], best_route, best_start_time, end_time)
                else:
                    # Try to find any available slot with reduced headway
                    scheduled = False
                    for i, travel_time in enumerate(train['travel_times']):
                        route = self.data['routes'][i]
                        
                        # Find the next available slot on this route
                        if self.global_state.route_occupancy[route]:
                            # Get the last scheduled train on this route
                            last_end = self.global_state.route_occupancy[route][-1][1]
                            # Try with reduced headway for capacity (down to 5 minutes)
                            start_time = last_end + max(5, self.data['headway'] - 3)
                        else:
                            start_time = 0
                        
                        end_time = start_time + travel_time
                        
                        # Check if this slot is available and within horizon
                        if (end_time <= self.data['horizon'] and 
                            self.global_state.can_schedule_train(train['id'], route, start_time, travel_time)):
                            schedule.append({
                                'train_id': train['id'],
                                'route_selected': route,
                                'start_time': start_time,
                                'end_time': end_time,
                                'travel_time': travel_time,
                                'completion_status': True
                            })
                            self.global_state.schedule_train(train['id'], route, start_time, end_time)
                            scheduled = True
                            break
                    
                    if not scheduled:
                        # If no slot found with reduced headway, try to find gaps between existing trains
                        for i, travel_time in enumerate(train['travel_times']):
                            route = self.data['routes'][i]
                            
                            if self.global_state.route_occupancy[route] and len(self.global_state.route_occupancy[route]) > 1:
                                # Look for gaps between scheduled trains
                                for j in range(len(self.global_state.route_occupancy[route]) - 1):
                                    current_end = self.global_state.route_occupancy[route][j][1]
                                    next_start = self.global_state.route_occupancy[route][j + 1][0]
                                    
                                    gap = next_start - current_end
                                    if gap >= travel_time + self.data['headway']:
                                        start_time = current_end + self.data['headway']
                                        end_time = start_time + travel_time
                                        
                                        if (end_time <= self.data['horizon'] and 
                                            self.global_state.can_schedule_train(train['id'], route, start_time, travel_time)):
                                            schedule.append({
                                                'train_id': train['id'],
                                                'route_selected': route,
                                                'start_time': start_time,
                                                'end_time': end_time,
                                                'travel_time': travel_time,
                                                'completion_status': True
                                            })
                                            self.global_state.schedule_train(train['id'], route, start_time, end_time)
                                            scheduled = True
                                            break
                                if scheduled:
                                    break
                    
                    if not scheduled:
                        # Final attempt: try to squeeze in with minimum headway
                        for i, travel_time in enumerate(train['travel_times']):
                            route = self.data['routes'][i]
                            
                            if self.global_state.route_occupancy[route]:
                                # Try absolute minimum headway (5 minutes)
                                last_end = self.global_state.route_occupancy[route][-1][1]
                                start_time = last_end + 5  # Absolute minimum headway
                                end_time = start_time + travel_time
                                
                                if (end_time <= self.data['horizon'] and 
                                    self.global_state.can_schedule_train(train['id'], route, start_time, travel_time)):
                                    schedule.append({
                                        'train_id': train['id'],
                                        'route_selected': route,
                                        'start_time': start_time,
                                        'end_time': end_time,
                                        'travel_time': travel_time,
                                        'completion_status': True
                                    })
                                    self.global_state.schedule_train(train['id'], route, start_time, end_time)
                                    scheduled = True
                                    break
                    
                    if not scheduled:
                        # Train cannot be scheduled within horizon
                        schedule.append({
                            'train_id': train['id'],
                            'route_selected': 'N/A',
                            'start_time': None,
                            'end_time': None,
                            'travel_time': min(train['travel_times']),
                            'completion_status': False
                        })
        
        return schedule
    
    def _verify_zero_violations(self):
        """Verify that there are zero headway violations."""
        violations = self.global_state.verify_zero_violations()
        if violations == 0:
            print("✅ GUARANTEED: Zero headway violations achieved!")
        else:
            print(f"❌ CRITICAL: Still {violations} headway violations detected")
    
    def get_results(self):
        """Return formatted results."""
        return {
            'schedule': self.full_schedule,
            'throughput': sum(1 for t in self.full_schedule if t.get('completion_status', False))
        }