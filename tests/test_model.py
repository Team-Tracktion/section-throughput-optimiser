"""
Test cases for the main optimization model.
"""

import unittest
import json
import os
from core.model import OptimizationModel

class TestOptimizationModel(unittest.TestCase):
    """Test cases for OptimizationModel class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a simple test configuration
        self.infrastructure = {
            'sections': [
                {'id': 's1', 'length': 5, 'capacity': 1},
                {'id': 's2', 'length': 8, 'capacity': 1}
            ],
            'junctions': [],
            'min_travel_times': {
                'express': {'s1-s2': 3},
                'passenger': {'s1-s2': 4},
                'freight': {'s1-s2': 6}
            },
            'min_headway_time': 3
        }
        
        self.timetable = {
            'trains': {
                'train1': {
                    'type': 'express',
                    'priority': 3,
                    'route': ['s1', 's2'],
                    'scheduled_arrival': 20
                }
            }
        }
    
    def test_model_initialization(self):
        """Test that the model initializes correctly."""
        model = OptimizationModel(self.infrastructure, self.timetable, 30)
        
        self.assertIsNotNone(model.model)
        self.assertIsNotNone(model.variables)
        self.assertIsNotNone(model.constraints)
        self.assertIsNotNone(model.objective)
    
    def test_model_solving(self):
        """Test that the model can solve a simple problem."""
        model = OptimizationModel(self.infrastructure, self.timetable, 30)
        solution = model.solve(time_limit=5)  # Short time limit for test
        
        # For such a simple problem, we should get a solution
        self.assertIsNotNone(solution)

if __name__ == '__main__':
    unittest.main()