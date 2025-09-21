"""
IRIS - Intelligent Railway Integration System

A decision-support system for optimizing train movements in real-time.
"""

__version__ = "0.1.0"
__author__ = "IRIS Development Team"
__license__ = "Apache 2.0"

from .core import OptimizationModel, TrainMovementVariables, MovementConstraints, ObjectiveFunction
from .data_processing import DataProcessor
from .simulation import Simulation

__all__ = [
    'OptimizationModel',
    'TrainMovementVariables', 
    'MovementConstraints',
    'ObjectiveFunction',
    'DataProcessor',
    'Simulation'
]