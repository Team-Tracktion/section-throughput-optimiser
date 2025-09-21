# strategies/base_strategy.py
from abc import ABC, abstractmethod

class BaseSchedulingStrategy(ABC):
    """Base class for scheduling strategies."""
    
    def __init__(self, data):
        self.data = data
        self.full_schedule = []
    
    @abstractmethod
    def solve(self):
        """Solve the scheduling problem."""
        pass
    
    def get_results(self):
        """Return formatted results."""
        return {
            'schedule': self.full_schedule,
            'throughput': sum(1 for t in self.full_schedule if t.get('completion_status', False))
        }