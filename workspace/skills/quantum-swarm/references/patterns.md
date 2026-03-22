# Quantum Swarm Patterns

## Pattern Catalog

### 1. Factory Swarm (Gas Town Inspired)

Factory Swarm implements industrialized parallel task execution:

```
                    ┌─────────────┐
                    │   MAYOR     │ ← User interface
                    │  (Overseer) │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌────────┐  ┌─────────┐  ┌─────────┐
         │ WITCH  │  │ WITCH   │  │ WITCH   │ ← Health monitors
         │ (Rig1) │  │ (Rig2)  │  │ (Rig3)  │
         └───┬────┘  └────┬────┘  └────┬────┘
             │            │            │
        ┌────┴────┐  ┌─────┴────┐  ┌────┴────┐
        │Polecats │  │Polecats  │  │Polecats │ ← Worker agents
        │ (N=max) │  │ (N=max)  │  │ (N=max) │
        └────┬────┘  └────┬─────┘  └────┬────┘
             │            │            │
             └────────────┼────────────┘
                          ▼
                    ┌──────────┐
                    │ REFINERY │ ← Merge queue
                    └────┬─────┘
                         ▼
                    ┌──────────┐
                    │   LAND   │ ← Convoy complete
                    └──────────┘
```

#### Execution Flow

```markdown
1. MAYOR: Receive task, create convoy, spawn beads
2. WITCH: Monitor polecat health, nudge stuck agents
3. POLECATS: Execute beads in parallel, submit MRs
4. REFINERY: Merge MRs intelligently, handle conflicts
5. LAND: Archive convoy, notify completion
```

#### State Files

```
.swarm/
├── convoys/
│   ├── active/{convoy-id}.json
│   └── archive/{convoy-id}.json
├── hooks/{agent-name}.json      # Work assignments
├── mail/{agent-name}/           # Inter-agent messages
└── state.json                   # Swarm state
```

### 2. Exploration Swarm

For discovering solutions in large search spaces:

```bash
# Phase 1: Superposition - spawn explorers
sessions_spawn count:5 superposition:true \
  prompt:"Explore {branch} of the solution space"

# Phase 2: Interference - combine results
# Analyze overlap and divergence

# Phase 3: Collapse - focus on best paths
sessions_spawn count:1 collapse:true \
  prompt:"Refine {best_branch} based on all findings"
```

### 3. Verification Swarm

For validating solutions:

```bash
# Spawn verification agents with different criteria
sessions_spawn count:3 entangled:true \
  prompt:"Verify {solution} against criteria: {criteria}"
```

### 4. Quantum Tunneling

Probabilistic escape from local minima:

```bash
# When stuck, spawn tunnel agents
sessions_spawn count:3 tunneling:true \
  prompt:"Jump to unexplored regions, ignore {stuck_area}"
```

## Implementation Examples

### Example 1: Code Feature Implementation

```markdown
Task: "Add user authentication to the app"

1. MAYOR receives task
2. Create convoy: "auth-feature"
3. Divide into beads:
   - bead-001: Design auth flow
   - bead-002: Implement login
   - bead-003: Implement registration
   - bead-004: Add session management
   - bead-005: Write tests
4. Spawn 3 polecats (chrome quality)
5. WITCH monitors health
6. REFINERY merges branches
7. LAND convoy
```

### Example 2: Bug Fix with Verification

```markdown
Bug: "API returns 500 on edge case X"

1. EXPLORER: Reproduce and identify root cause
2. EXPLORER: Propose fix
3. SPAWN verification swarm:
   - Agent A: Test the fix
   - Agent B: Check similar edge cases
   - Agent C: Review security implications
4. If conflicts: TUNNEL to alternative approaches
5. MERGE verified fix
```

## Entanglement Patterns

### Pair Entanglement

Two agents share state bidirectionally:

```bash
sessions_spawn count:2 entangled:pair \
  prompt:"Work on {aspect}, sync state with paired agent"
```

### Ring Entanglement

N agents in a logical ring:

```
Agent 1 ↔ Agent 2 ↔ Agent 3 ↔ Agent 1
```

### Broadcast Entanglement

One agent broadcasts to N listeners:

```bash
sessions_spawn count:1 broadcast:true \
  prompt:"Announce findings to all"
```

## Collapse Conditions

Define when swarm should terminate:

| Condition | Trigger | Action |
|-----------|---------|--------|
| Convergence | >80% agents agree | Collapse to consensus |
| Exhaustion | All paths explored | Return best result |
| Timeout | Max iterations reached | Return partial solution |
| Quality | Quality threshold met | Early termination |

## Anti-Patterns

### Premature Collapse
Don't collapse before sufficient exploration.

### Superposition Overhead
Too many agents = coordination costs exceed benefits.

### Tunneling Addiction
Don't tunnel constantly; explore first.

### Ghost Entanglement
Don't entangle agents that don't need coordination.
