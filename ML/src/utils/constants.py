"""
Constants for the IRIS system.
"""

# Train type priorities (higher number = higher priority)
TRAIN_PRIORITIES = {
    'express': 3,
    'passenger': 2, 
    'freight': 1,
    'maintenance': 0
}

# Default optimization parameters
DEFAULT_PARAMS = {
    'time_horizon': 60,
    'time_limit': 30,
    'strategy': 'delay_minimization'
}

# Section types
SECTION_TYPES = {
    'main': 'Main line',
    'loop': 'Looping line',
    'siding': 'Siding',
    'yard': 'Yard',
    'platform': 'Platform'
}

# Optimization status codes
STATUS_CODES = {
    0: 'OPTIMAL',
    1: 'FEASIBLE',
    2: 'INFEASIBLE',
    3: 'UNBOUNDED',
    4: 'ABNORMAL',
    5: 'MODEL_INVALID',
    6: 'UNKNOWN'
}