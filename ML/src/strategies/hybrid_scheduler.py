# strategies/hybrid_scheduler.py
from strategies.simple_mlfq_scheduler import SimpleMLFQScheduler
from strategies.rolling_horizon import RollingHorizonScheduler

class HybridScheduler(SimpleMLFQScheduler):
    """Hybrid scheduler combining MLFQ and Rolling Horizon."""
    
    def __init__(self, data):
        super().__init__(data)
        
    def solve(self):
        """Hybrid scheduling implementation."""
        print("Using Hybrid approach: MLFQ + Rolling Horizon")
        
        # Phase 1: Simple MLFQ
        print("Phase 1: Simple MLFQ Scheduling")
        mlfq_results = super().solve()
        
        # Get scheduled trains
        scheduled_ids = {t['train_id'] for t in mlfq_results['schedule'] if t.get('completion_status', False)}
        
        # Identify unscheduled trains
        unscheduled_trains = [t for t in self.data['trains'] if t['id'] not in scheduled_ids]
        
        if unscheduled_trains:
            print(f"Phase 2: Rolling Horizon for {len(unscheduled_trains)} remaining trains")
            
            # Phase 2: Rolling Horizon
            remaining_data = {
                'trains': unscheduled_trains,
                'routes': self.data['routes'],
                'headway': self.data['headway'],
                'horizon': self.data['horizon']
            }
            
            rh_scheduler = RollingHorizonScheduler(
                remaining_data,
                window_size=min(6, len(unscheduled_trains)),
                overlap=1,
                time_limit_per_window=2.0
            )
            rh_results = rh_scheduler.solve()
            
            # Combine results
            self.full_schedule = mlfq_results['schedule'] + rh_results['schedule']
        else:
            self.full_schedule = mlfq_results['schedule']
            print("All trains scheduled by MLFQ")
        
        return self.get_results()