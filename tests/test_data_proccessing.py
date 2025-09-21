"""
Test cases for data processing utilities.
"""

import unittest
import json
import tempfile
import os

from data_processing import DataProcessor

class TestDataProcessing(unittest.TestCase):
    """Test cases for DataProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary files for testing
        self.temp_infra = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_timetable = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        
        # Write sample data to temporary files
        infra_data = {
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
        
        timetable_data = {
            'trains': {
                'train1': {
                    'type': 'express',
                    'priority': 3,
                    'route': ['s1', 's2'],
                    'scheduled_arrival': 20
                }
            }
        }
        
        json.dump(infra_data, self.temp_infra)
        json.dump(timetable_data, self.temp_timetable)
        
        self.temp_infra.close()
        self.temp_timetable.close()
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.temp_infra.name)
        os.unlink(self.temp_timetable.name)
    
    def test_data_loading(self):
        """Test that data is loaded correctly from files."""
        processor = DataProcessor(self.temp_infra.name, self.temp_timetable.name)
        infrastructure, timetable = processor.load_data()
        
        self.assertIn('sections', infrastructure)
        self.assertIn('trains', timetable)
        self.assertEqual(len(infrastructure['sections']), 2)
        self.assertEqual(len(timetable['trains']), 1)
    
    def test_data_validation(self):
        """Test that data validation works correctly."""
        processor = DataProcessor(self.temp_infra.name, self.temp_timetable.name)
        
        # This should not raise an exception
        infrastructure, timetable = processor.load_data()
        
        # Test with invalid data (missing required key)
        invalid_infra = infrastructure.copy()
        del invalid_infra['sections']
        
        with self.assertRaises(ValueError):
            processor._validate_data(invalid_infra, timetable)
    
    def test_test_data_generation(self):
        """Test that test data generation works correctly."""
        processor = DataProcessor(None, None)
        infrastructure, timetable = processor.generate_test_data(num_trains=3)
        
        self.assertIn('sections', infrastructure)
        self.assertIn('trains', timetable)
        self.assertEqual(len(timetable['trains']), 3)

if __name__ == '__main__':
    unittest.main()