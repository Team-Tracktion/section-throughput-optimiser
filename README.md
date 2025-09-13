# Railway Scheduling Project Summary

## Project Goal

* Develop a **dynamic, human-in-the-loop railway scheduler**.
* Maximize **section throughput**, minimize **delays**, handle **track diversions**.
* Respect **train priorities** and **operational constraints**.

## Key Challenges

1. Conflicts on shared track sections.
2. Headway and safety constraints.
3. Trade-offs between diversions, delays, and throughput.
4. Real-time adjustments based on **human input**.
5. Scalability for multiple trains and sections.

## Problem Formulation

### Decision Variables

* `T_i`: Start time of train i at a section.
* `x_{i,r}`: Route choice (main or diversion).
* `flow_i`: Indicator if train completes within planning horizon.
* `p_{ij}`: Sequencing between conflicting trains.

### Objective Function

```math
max \sum_i w_i \cdot flow_i - \alpha \sum_i (T_i - T_i^{sched}) - \beta \sum_i \sum_r c_r \cdot x_{i,r}
```

* Weighted throughput minus **delay penalties** and **diversion costs**.
* `w_i` = train priority.
* `α` = delay weight.
* `β` = diversion penalty.

### Constraints

1. Each train takes exactly **one route**: `\sum_r x_{i,r} = 1`
2. **Conflict-free** section scheduling using pairwise sequencing and headway constraints.
3. **Time horizon** enforcement — trains must finish within planning horizon.
4. **Priority enforcement** for high-priority trains.
5. **Human input adjustments** — fixed routes or start times for operator-selected trains.

## Implementation Status

* **Python-based CP-SAT model** using Google OR-Tools.
* Supports **3–10 trains** with main/diversion route options.
* Includes:

  * Weighted throughput optimization
  * Conflict-free section scheduling
  * Headway and safety constraints
  * Human-in-the-loop adjustments (fixed routes/start times)
* Flexible for extension to multiple sections and rolling horizon.

## Git Workflow

* One `main` branch: stable production-ready code.
* One `dev-<username>` branch per contributor.
* Pull requests from `dev-<username>` → `main` after review and testing.
* Commit messages in imperative mood; small, atomic commits.

## Next Steps

1. Extend model to **multi-section networks**.
2. Implement **rolling horizon scheduling** for real-time updates.
3. Integrate **visualization (Gantt charts)** to display schedules and human adjustments.
4. Optimize for **larger numbers of trains (20–50+)** using hybrid MILP + heuristics approach.
5. Refine **human-in-the-loop interface** for dynamic rescheduling.
