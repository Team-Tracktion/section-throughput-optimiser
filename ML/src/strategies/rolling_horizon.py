# strategies/rolling_horizon.py
from strategies.base_strategy import BaseSchedulingStrategy
from core.model import RailwayScheduler

class RollingHorizonScheduler(BaseSchedulingStrategy):
    """Rolling Horizon scheduler."""
    
    def __init__(self, data, window_size=6, overlap=1, time_limit_per_window=2.0):
        super().__init__(data)
        self.window_size = window_size
        self.overlap = overlap
        self.time_limit_per_window = time_limit_per_window
    
    def solve(self):
        """Rolling horizon implementation."""
        print(f"Rolling Horizon: Window size={self.window_size}, Overlap={self.overlap}")
        
        all_trains = self.data['trains']
        start_idx = 0
        
        while start_idx < len(all_trains):
            end_idx = min(start_idx + self.window_size, len(all_trains))
            window_trains = all_trains[start_idx:end_idx]
            
            # Solve window
            window_schedule = self._solve_window(window_trains)
            self.full_schedule.extend(window_schedule)
            
            start_idx += (self.window_size - self.overlap)
        
        print(f"Rolling Horizon completed: {len(self.full_schedule)} trains processed")
        return self.get_results()
    
    def _solve_window(self, trains):
        """Solve a single window."""
        window_data = {
            'trains': trains,
            'routes': self.data['routes'],
            'headway': self.data['headway'],
            'horizon': self.data['horizon']
        }
        
        try:
            scheduler = RailwayScheduler(window_data)
            scheduler.build_model()
            results = scheduler.solve(
                time_limit_minutes=self.time_limit_per_window,
                verbose=False
            )
            
            if results['status'] in [2, 4]:  # Feasible or optimal
                formatted = []
                for i, train_result in enumerate(results['schedule']):
                    if train_result['completed']:
                        train_config = trains[i]
                        travel_time = train_config['travel_times'][self.data['routes'].index(train_result['route'])]
                        formatted.append({
                            'train_id': train_config['id'],
                            'route_selected': train_result['route'],
                            'start_time': train_result['start_time'],
                            'end_time': train_result['start_time'] + travel_time,
                            'travel_time': travel_time,
                            'completion_status': True
                        })
                return formatted
                
        except:
            pass
        
        # Fallback: simple scheduling
        schedule = []
        current_time = 0
        
        for train in trains:
            travel_time = min(train['travel_times'])
            end_time = current_time + travel_time
            can_schedule = end_time <= self.data['horizon']
            
            schedule.append({
                'train_id': train['id'],
                'route_selected': self.data['routes'][train['travel_times'].index(travel_time)] if can_schedule else 'N/A',
                'start_time': current_time if can_schedule else None,
                'end_time': end_time if can_schedule else None,
                'travel_time': travel_time,
                'completion_status': can_schedule
            })
            
            if can_schedule:
                current_time = end_time + self.data['headway']
        
        return schedule