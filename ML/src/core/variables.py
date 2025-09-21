from ortools.sat.python import cp_model

def create_variables(model, data):
    """Create decision variables for the railway scheduling problem."""
    num_trains = len(data['trains'])
    num_routes = len(data['routes'])
    
    # Start time variables
    T = [model.NewIntVar(0, data['horizon'], f'T_{i}') for i in range(num_trains)]
    
    # Route choice variables (one-hot encoded)
    x = []
    for i in range(num_trains):
        route_vars = []
        for r in range(num_routes):
            route_vars.append(model.NewBoolVar(f'x_{i}_{r}'))
        x.append(route_vars)
    
    # Flow completion variables
    flow = [model.NewBoolVar(f'flow_{i}') for i in range(num_trains)]
    
    # Sequencing variables (for conflict resolution)
    p = {}
    for i in range(num_trains):
        for j in range(i + 1, num_trains):
            p[i, j] = model.NewBoolVar(f'p_{i}_{j}')
            p[j, i] = model.NewBoolVar(f'p_{j}_{i}')
    
    return {
        'T': T,
        'x': x,
        'flow': flow,
        'p': p
    }