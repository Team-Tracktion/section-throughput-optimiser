"""
Test cases for variable definitions.
"""

import unittest
from ortools.sat.python import cp_model

from core.variables import TrainMovementVariables

class TestVariables(unittest.TestCase):
    """Test cases for TrainMovementVariables class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = cp_model.CpModel()
        
        # Mock infrastructure and timetable data
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
    
    def test_variable_creation(self):
        """Test that variables are created correctly."""
        variables = TrainMovementVariables(self.model, self.infrastructure, self.timetable, 30)
        variables.create_variables()
        
        # Check that occupancy variables were created
        self.assertIn('train1', variables.occupancy)
        self.assertIn('s1', variables.occupancy['train1'])
        self.assertIn('s2', variables.occupancy['train1'])
        
        # Check that departure time variables were created
        self.assertIn('train1', variables.departure_times)
        self.assertIn('s1', variables.departure_times['train1'])
        self.assertIn('s2', variables.departure_times['train1'])

if __name__ == '__main__':
    unittest.main()