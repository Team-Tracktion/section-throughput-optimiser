"""
Simulation module for testing optimization results.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime, timedelta

class Simulation:
    """Simulates and visualizes train movements based on optimization results."""
    
    def __init__(self, results_file, infrastructure_file):
        """
        Initialize simulation.
        
        Args:
            results_file: Path to optimization results JSON file
            infrastructure_file: Path to infrastructure JSON file
        """
        with open(results_file, 'r') as f:
            self.results = json.load(f)
        
        with open(infrastructure_file, 'r') as f:
            self.infrastructure = json.load(f)
        
        # Extract section order for visualization
        self.section_order = [section['id'] for section in self.infrastructure['sections']]
    
    def visualize_schedule(self, output_file=None):
        """
        Create a Gantt chart visualization of the train schedule.
        
        Args:
            output_file: Path to save the visualization (if None, display interactively)
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Colors for different train types
        colors = {
            'express': 'red',
            'passenger': 'blue',
            'freight': 'green'
        }
        
        # Plot each train's schedule
        y_ticks = []
        y_labels = []
        
        for i, (train_id, train_data) in enumerate(self.results.items()):
            y_pos = i
            y_ticks.append(y_pos)
            y_labels.append(train_id)
            
            for schedule_item in train_data['schedule']:
                section = schedule_item['section']
                start = schedule_item['entry_time']
                duration = schedule_item['duration']
                
                # Find x position based on section order
                x_pos = self.section_order.index(section) * 20  # Scale for visibility
                
                # Create rectangle for this occupancy
                rect = patches.Rectangle(
                    (x_pos, y_pos - 0.4), 15, 0.8,
                    linewidth=1, edgecolor='black', 
                    facecolor=colors.get(train_data['type'], 'gray'),
                    alpha=0.7
                )
                ax.add_patch(rect)
                
                # Add text with time info
                ax.text(x_pos + 7.5, y_pos, f"{start}-{start+duration}", 
                       ha='center', va='center', fontsize=8)
        
        # Set up axes
        ax.set_xlabel('Track Sections')
        ax.set_ylabel('Trains')
        ax.set_title('Train Schedule Visualization')
        
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        
        ax.set_xticks([i * 20 for i in range(len(self.section_order))])
        ax.set_xticklabels(self.section_order)
        
        ax.grid(True, alpha=0.3)
        
        # Add legend
        legend_patches = [
            patches.Patch(color=color, label=train_type)
            for train_type, color in colors.items()
        ]
        ax.legend(handles=legend_patches, loc='upper right')
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300)
            print(f"Visualization saved to {output_file}")
        else:
            plt.show()
    
    def calculate_statistics(self):
        """Calculate and display statistics about the solution."""
        total_delay = 0
        delayed_trains = 0
        train_types = {}
        
        for train_id, train_data in self.results.items():
            delay = train_data['delay']
            total_delay += delay
            
            if delay > 0:
                delayed_trains += 1
            
            train_type = train_data['type']
            if train_type not in train_types:
                train_types[train_type] = {'count': 0, 'total_delay': 0}
            
            train_types[train_type]['count'] += 1
            train_types[train_type]['total_delay'] += delay
        
        print("=== SOLUTION STATISTICS ===")
        print(f"Total delay: {total_delay} minutes")
        print(f"Delayed trains: {delayed_trains}/{len(self.results)} ({delayed_trains/len(self.results)*100:.1f}%)")
        print(f"Average delay: {total_delay/len(self.results):.1f} minutes")
        
        print("\nDelay by train type:")
        for train_type, stats in train_types.items():
            avg_delay = stats['total_delay'] / stats['count'] if stats['count'] > 0 else 0
            print(f"  {train_type}: {stats['total_delay']} min total, {avg_delay:.1f} min avg per train")
    
    def simulate_movements(self, speed=1.0):
        """
        Simulate train movements in real-time (for demonstration).
        
        Args:
            speed: Simulation speed multiplier (1.0 = real-time)
        """
        print("Starting simulation...")
        
        # Find the maximum time in the schedule
        max_time = 0
        for train_data in self.results.values():
            for schedule_item in train_data['schedule']:
                max_time = max(max_time, schedule_item['exit_time'])
        
        # Simulate each time step
        for current_time in range(max_time + 1):
            print(f"\nTime: {current_time} minutes")
            print("=" * 40)
            
            # Check each section for trains
            for section_id in self.section_order:
                trains_in_section = []
                
                for train_id, train_data in self.results.items():
                    for schedule_item in train_data['schedule']:
                        if (schedule_item['section'] == section_id and 
                            schedule_item['entry_time'] <= current_time <= schedule_item['exit_time']):
                            trains_in_section.append(train_id)
                
                if trains_in_section:
                    print(f"Section {section_id}: {', '.join(trains_in_section)}")
                else:
                    print(f"Section {section_id}: Empty")
            
            # Simple animation - wait before next time step
            import time
            time.sleep(1.0 / speed)