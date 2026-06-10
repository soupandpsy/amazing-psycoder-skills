# Randomization Standard

Applies to all experiments, regardless of platform or paradigm.

## Trial Order

### Within-block randomizations

- **Full random**: Shuffle all trials in the block. No constraints. Fastest to implement.
- **Pseudorandom**: Shuffle with constraints (e.g., no more than 3 consecutive same-condition trials). Implement by re-shuffling until constraint is met, or use a constraint-based algorithm.
- **Blocked**: Group trials by condition, randomize within each sub-block. Used when conditions must be evenly distributed.
- **Fixed**: Predefined order, same for all subjects. Only acceptable for practice blocks or calibration.

### Between-block randomizations

- **Same order, re-randomized**: Each block gets its own independent randomization of the same condition set.
- **Counterbalanced across subjects**: Each subject gets one of N predetermined orders. Use a condition file or subject-ID-based assignment.
- **Latin square**: For N conditions, N subjects each see a different order. Reduces order effects in within-subjects designs.

## Counterbalancing

For within-subjects designs where order effects matter:

1. **Across subjects**: Each subject assigned to one counterbalance order at startup
2. **Within subject**: Each subject experiences all counterbalance orders across blocks
3. **Full permutation**: Use all N! possible orders (feasible only for small N)
4. **Latin square**: Use N orders, each condition appears once per position

Implementation:
```python
# Example: assign counterbalance order by subject ID
import random
random.seed(subject_id)
order = random.choice(['order_a', 'order_b'])
```

## Constraints

Common constraints to implement:

- **No more than N consecutive same-condition trials**: Re-shuffle until constraint met
- **No condition repetitions on critical trials**: Exclude from randomization
- **Equal condition count per block**: Required by design; verify after randomization
- **Go/No-go consecutive limit**: Typically max 1-2 no-go trials in a row

## Seed Management

- Always set `random.seed()` for reproducibility
- Seed can be based on subject ID, or use a fixed seed and save the state
- Document the seed in data output or a separate log file

## Validation

After generating trial order, verify:
1. All conditions appear the expected number of times
2. No constraint violations
3. Block transitions are at correct trial indices
4. Counterbalance order is correctly assigned
