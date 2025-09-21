from ortools.sat.python import cp_model

def create_objective(model, data, variables):
    """Create the objective function for the railway scheduling problem."""
    T = variables['T']
    x = variables['x']
    flow = variables['flow']
    
    objective_terms = []
    
    # Throughput maximization (weighted by priority)
    for i, train in enumerate(data['trains']):
        weight = 100 if train['priority'] == 'high' else 1
        objective_terms.append(weight * flow[i])
    
    # Delay minimization
    alpha = data['alpha']
    for i, train in enumerate(data['trains']):
        delay = T[i] - train['scheduled_time']
        objective_terms.append(-alpha * delay)
    
    # Diversion cost minimization
    beta = data['beta']
    for i in range(len(data['trains'])):
        for r in range(len(data['routes'])):
            if r > 0:  # Assume index 0 is main route, others are diversions
                cost = data['diversion_costs'][r]
                objective_terms.append(-beta * cost * x[i][r])
    
    # Maximize the objective function
    model.Maximize(sum(objective_terms))
    
    return model