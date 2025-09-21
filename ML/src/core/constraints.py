from ortools.sat.python import cp_model

def add_constraints(model, data, variables):
    """Add all constraints to the model."""
    num_trains = len(data['trains'])
    num_routes = len(data['routes'])
    T = variables['T']
    x = variables['x']
    flow = variables['flow']
    p = variables['p']
    
    # 1. Each train takes exactly one route
    for i in range(num_trains):
        model.Add(sum(x[i][r] for r in range(num_routes)) == 1)
    
    # 2. Conflict-free scheduling with headway constraints
    for i in range(num_trains):
        for j in range(i + 1, num_trains):
            # Only one sequencing direction can be true
            model.Add(p[i, j] + p[j, i] == 1)
            
            # Headway constraint enforcement
            for r in range(num_routes):
                # If both trains use same route, enforce headway
                both_same_route = model.NewBoolVar(f'both_same_route_{i}_{j}_{r}')
                model.Add(x[i][r] + x[j][r] == 2).OnlyEnforceIf(both_same_route)
                model.Add(x[i][r] + x[j][r] != 2).OnlyEnforceIf(both_same_route.Not())
                
                # Apply headway constraint based on sequencing
                travel_time_i = data['trains'][i]['travel_times'][r]
                travel_time_j = data['trains'][j]['travel_times'][r]
                headway = data['headway']
                
                model.Add(T[i] + travel_time_i + headway <= T[j]).OnlyEnforceIf([p[i, j], both_same_route])
                model.Add(T[j] + travel_time_j + headway <= T[i]).OnlyEnforceIf([p[j, i], both_same_route])
    
    # 3. Time horizon enforcement
    for i in range(num_trains):
        for r in range(num_routes):
            travel_time = data['trains'][i]['travel_times'][r]
            model.Add(T[i] + travel_time <= data['horizon']).OnlyEnforceIf(x[i][r])
    
    # 4. Priority enforcement (high-priority trains must run)
    for i in range(num_trains):
        if data['trains'][i]['priority'] == 'high':
            model.Add(flow[i] == 1)
    
    # 5. Human input adjustments
    for adjustment in data.get('human_adjustments', []):
        train_idx = adjustment['train_index']
        
        if 'fixed_route' in adjustment:
            route_idx = data['routes'].index(adjustment['fixed_route'])
            model.Add(x[train_idx][route_idx] == 1)
        
        if 'fixed_start_time' in adjustment:
            model.Add(T[train_idx] == adjustment['fixed_start_time'])
    
    return model