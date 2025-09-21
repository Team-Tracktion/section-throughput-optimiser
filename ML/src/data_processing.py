"""
Data processing utilities for IRIS system.
"""

import json
import pandas as pd
from datetime import datetime, timedelta

class DataProcessor:
    """Processes and prepares data for the optimization model."""
    
    def __init__(self, infrastructure_file, timetable_file):
        """
        Initialize data processor.
        
        Args:
            infrastructure_file: Path to infrastructure JSON file
            timetable_file: Path to timetable JSON file
        """
        self.infra_file = infrastructure_file
        self.timetable_file = timetable_file
        
    def load_data(self):
        """Load and validate data from files."""
        with open(self.infra_file, 'r') as f:
            infrastructure = json.load(f)
        
        with open(self.timetable_file, 'r') as f:
            timetable = json.load(f)
        
        return self._validate_data(infrastructure, timetable)
    
    def _validate_data(self, infrastructure, timetable):
        """
        Validate infrastructure and timetable data.
        
        Args:
            infrastructure: Infrastructure data dictionary
            timetable: Timetable data dictionary
            
        Returns:
            Tuple of (validated_infrastructure, validated_timetable)
        """
        # Validate infrastructure
        required_infra_keys = ['sections', 'junctions', 'min_travel_times']
        for key in required_infra_keys:
            if key not in infrastructure:
                raise ValueError(f"Missing required infrastructure key: {key}")
        
        # Validate timetable
        if 'trains' not in timetable:
            raise ValueError("Missing 'trains' key in timetable")
        
        for train_id, train_data in timetable['trains'].items():
            required_train_keys = ['type', 'priority', 'route', 'scheduled_arrival']
            for key in required_train_keys:
                if key not in train_data:
                    raise ValueError(f"Train {train_id} missing required key: {key}")
            
            # Validate that all sections in route exist in infrastructure
            for section_id in train_data['route']:
                if not any(s['id'] == section_id for s in infrastructure['sections']):
                    raise ValueError(f"Section {section_id} in train {train_id} route not found in infrastructure")
        
        return infrastructure, timetable
    
    def generate_test_data(self, num_trains=5, time_horizon=60):
        """
        Generate test data for demonstration purposes.
        
        Args:
            num_trains: Number of trains to generate
            time_horizon: Time horizon for optimization
            
        Returns:
            Tuple of (infrastructure, timetable)
        """
        # Simple infrastructure with 5 sections
        infrastructure = {
            "sections": [
                {"id": "s1", "length": 5, "capacity": 1},
                {"id": "s2", "length": 8, "capacity": 1},
                {"id": "s3", "length": 6, "capacity": 1},
                {"id": "s4", "length": 7, "capacity": 1},
                {"id": "s5", "length": 4, "capacity": 1}
            ],
            "junctions": [
                {
                    "id": "j1",
                    "conflicting_routes": [["s1-s2", "s3-s4"]]
                }
            ],
            "min_travel_times": {
                "express": {"s1-s2": 3, "s2-s3": 4, "s3-s4": 3, "s4-s5": 2},
                "passenger": {"s1-s2": 4, "s2-s3": 5, "s3-s4": 4, "s4-s5": 3},
                "freight": {"s1-s2": 6, "s2-s3": 7, "s3-s4": 6, "s4-s5": 4}
            },
            "min_headway_time": 3
        }
        
        # Generate trains
        train_types = ['express', 'passenger', 'freight']
        priorities = {'express': 3, 'passenger': 2, 'freight': 1}
        
        timetable = {"trains": {}}
        
        for i in range(num_trains):
            train_type = train_types[i % len(train_types)]
            train_id = f"train_{i+1}_{train_type}"
            
            # Simple route through all sections
            route = ["s1", "s2", "s3", "s4", "s5"]
            
            # Scheduled arrival based on train type and random offset
            base_time = 20 if train_type == 'express' else 30 if train_type == 'passenger' else 40
            scheduled_arrival = base_time + (i * 5) % 20
            
            timetable['trains'][train_id] = {
                "type": train_type,
                "priority": priorities[train_type],
                "route": route,
                "scheduled_arrival": scheduled_arrival
            }
        
        return infrastructure, timetable
    
    def save_data(self, infrastructure, timetable, output_file):
        """
        Save processed data to a JSON file.
        
        Args:
            infrastructure: Infrastructure data
            timetable: Timetable data
            output_file: Path to output JSON file
        """
        data = {
            "infrastructure": infrastructure,
            "timetable": timetable,
            "generated_at": datetime.now().isoformat()
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Data saved to {output_file}")