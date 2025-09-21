# Heuristic-Prioritized Limited Horizon Optimization (H-PLHO)

## Overview
**H-PLHO** is a hybrid algorithm for **real-time optimization** in complex scheduling domains such as **railway traffic management**.  
It efficiently resolves conflicts by combining **fast heuristics** with **targeted mathematical optimization**, decomposing large problems into manageable sub-problems.

---

## Core Principles

- **Decomposition**: Uses a rolling horizon (e.g., 30-minute windows) to break down the problem spatially and temporally.  
- **Heuristic Triaging**: Applies priority rules to resolve most conflicts instantly (e.g., passenger over freight, more delayed trains first).  
- **Targeted Optimization**: Solves small optimization models only for complex conflict clusters.  

---

## Methodology

### Heuristic Module
- Applies rules based on train priority, delay, and schedule.  

### Optimization Module
- Solves localized **MILP/CP** models to minimize weighted delay in clusters.  

---

## Algorithm Steps

1. **Conflict Detection**  
   Project train movements and identify conflicts.  

2. **Heuristic Filtering**  
   Resolve clear conflicts using priority rules.  

3. **Cluster Identification**  
   Group unresolved conflicts into clusters.  

4. **Mini-Optimization**  
   Solve a small optimization model per cluster.  

5. **Execution & Roll**  
   Implement the plan and repeat for the next horizon.  

---

## Mathematical Formulation

**Objective**: Minimize total weighted delay  

\[
\text{Minimize } Z = \sum_{t \in T} w_t \cdot D^{\text{total}}_t
\]

### Variables
- **Precedence binaries**: \( x_{i,j} \)  
- **Total delay**: \( D^{\text{total}}_t \)  

### Constraints
- Precedence  
- Headway  
- Resource occupation  
- Delay calculation  

---

## Applications

- Real-time **railway dispatching and signaling**  
- **Delay management** and recovery  
- **Network resilience** during disruptions  
- Also applicable to:
  - **Air traffic control**  
  - **Manufacturing scheduling**  
  - **Logistics planning**  

---

## Advantages

- High computational efficiency  
- Scalable to large networks  
- Maintains solution quality  
- Explainable decisions  

---

## Limitations

- May miss long-term optimal solutions  
- Relies on heuristic quality  
- Requires accurate cluster identification  
- Higher implementation complexity  

---
