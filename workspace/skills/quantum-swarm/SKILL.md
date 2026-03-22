---
name: quantum-swarm
description: Quantum-inspired swarm intelligence for distributed AI agent coordination. Use when: (1) spawning multiple parallel agents for complex tasks, (2) coordinating agent swarms with entanglement patterns, (3) solving problems with quantum superposition (try multiple approaches simultaneously), (4) probabilistic task routing through quantum tunneling, (5) emergent problem-solving through swarm collaboration. Triggers on: "quantum swarm", "agent swarm", "parallel agents", "multi-agent coordination", "swarm intelligence", "量子蜂群".
metadata:
  {
    "openclaw": { "emoji": "⚛️", "homepage": "https://github.com/openclaw/openclaw" },
  }
---

# Quantum Swarm Intelligence

Quantum Swarm combines quantum computing principles with agent swarm intelligence for distributed AI task solving.

## Core Principles

### Superposition
Multiple agents explore different solution paths simultaneously, collapsing into optimal outcomes upon evaluation.

### Entanglement
Agent pairs remain synchronized through shared state, enabling coordinated behavior across distributed tasks.

### Tunneling
Agents can "tunnel" through local minima by probabilistically jumping to unexplored solution spaces.

### Interference
Parallel agent results interfere constructively (synergies) or destructively (conflicts), yielding refined outcomes.

## Execution Model

Use `sessions_spawn` for all quantum swarm operations:

```bash
# Spawn entangled agent pairs
sessions_spawn count:2 entangled:true prompt:"Explore {variant} of the solution"

# Superposition: multiple approaches in parallel
sessions_spawn count:3 superposition:true prompt:"Approach: {approach}"

# Tunneling: probabilistic exploration
sessions_spawn count:5 tunneling:true prompt:"Find solutions, then jump to unexplored areas"
```

## Swarm Patterns

### Pattern 1: Exploration Swarm

For discovering solution spaces:

```
1. Spawn N agents in superposition state
2. Each explores a different branch
3. Results interfere to reveal optimal path
4. Collapse into focused agents for execution
```

### Pattern 2: Verification Swarm

For validating solutions from multiple angles:

```
1. Original agent produces solution
2. Spawn entangled verification agents
3. Each verifies with different criteria
4. Conflicts trigger tunneling to new solutions
```

### Pattern 3: Factory Swarm

For parallel task execution (inspired by Gas Town):

```
1. Mayor receives task, creates convoy
2. Divide into beads (work units)
3. Spawn polecat agents for each bead
4. Witness monitors swarm health
5. Refinery merges results
```

## State Synchronization

Maintain entangled state through shared resources:

| State Type | Mechanism | Use Case |
|------------|-----------|----------|
| File-based | `.swarm/state.json` | Cross-agent coordination |
| Git-backed | `convoys/` directory | Persistent work tracking |
| In-memory | Session context | Ephemeral synchronization |

## Quality Levels

| Level | Agents | Reviews | Time Cost |
|-------|--------|---------|-----------|
| Standard | 1-3 | Self-review | 1x |
| Shiny | 3-5 | 2-pass review | 2x |
| Chrome | 5-10 | 5-pass review | 3x |

## Swarm Health Monitoring

Monitor entropy levels across the swarm:

- **High entropy**: Agents exploring too divergently → increase interference
- **Low entropy**: Agents stuck in local minima → trigger tunneling
- **Collapse**: Sufficient convergence achieved → terminate swarm

## Best Practices

1. **Size swarms appropriately**: More agents = more coordination overhead
2. **Use entanglement sparingly**: Synchronization has costs
3. **Set collapse thresholds**: Don't run swarms indefinitely
4. **Preserve diversity**: Avoid premature convergence
5. **Handle interference**: Conflicts should trigger resolution

For detailed patterns and examples, see `references/patterns.md`.
