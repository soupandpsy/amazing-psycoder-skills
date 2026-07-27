# Randomization and Counterbalancing Contract

Randomization is a design decision, not a universal shuffle. Confirm whether the goal is unpredictable presentation, balance across positions, constrained sequences, adaptive sampling, or an intentionally fixed/calibration order.

## Supported Strategies

- **Random**: shuffle the declared multiset without sequence constraints.
- **Constrained/pseudorandom**: construct or search for an order satisfying explicit constraints. Use bounded attempts and fail loudly if infeasible; never run an unbounded re-shuffle loop.
- **Blocked/stratified**: preserve declared balance within sub-blocks or strata, then randomize only allowed positions.
- **Counterbalanced**: assign participants/sessions to precomputed orders (full permutation, Latin/Williams square, or a declared subset).
- **Fixed**: use a predeclared order when scientifically justified; it is not limited to practice but its order effects must be accepted or controlled.
- **Adaptive**: log every realized state/value and the inputs that drove the update.

## Seed Strategy

For stochastic ordering, config must declare `seed_scope` (`per_session`, `per_subject`, or intentionally `fixed`), a resolvable seed, and `record_resolved_seed: true`. A fixed seed gives every run the same pseudorandom order; use it only with a recorded justification.

Prefer a versioned, stable derivation over language-runtime defaults. For example, hash `task_version + pseudonymous_subject_id + session_id`, convert part of the digest to an integer, and record both the derivation version and resolved seed. Avoid Python's process-salted `hash()` and do not assume the same seed yields identical sequences across languages/library versions.

For counterbalance assignment, a stable digest modulo the number of precomputed cells is auditable, but monitor realized enrollment counts and define handling for exclusions/replacements. Do not confuse counterbalance-cell assignment with within-cell trial randomization.

## Validation

After constructing the realized order:

1. Verify the exact declared trial multiset and condition counts.
2. Verify every sequence constraint and report infeasibility explicitly.
3. Verify sequence boundaries and counterbalance/adaptive state transitions.
4. Save the resolved seed or complete realized order with subject/session/task version.
5. Test that different intended scopes vary and intentionally fixed scopes reproduce.
