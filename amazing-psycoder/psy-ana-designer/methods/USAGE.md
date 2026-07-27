# Method Card Usage Contract

Read this file before any individual method card.

Method cards are candidate reminders, not self-validating prescriptions. Their examples may use older package APIs, simplified formulas, conventional cutoffs, or deterministic `set.seed()` boilerplate. They never override the confirmed estimand, observation hierarchy, config schema, current official package documentation, Coder platform spec, or Reviewer verdict.

When using a card:

1. State the target estimand, outcome support/unit, observation level, assignment/sampling structure, and all dependence units.
2. Separate mathematical assumptions from diagnostics; a failed omnibus normality test does not mechanically select a nonparametric method.
3. Treat effect-size, fit-index, sample-size, event-count, and diagnostic cutoffs as context-dependent claims requiring a source/justification, not universal gates.
4. Verify the current package/API and whether the implementation actually supports the required random effects, links, covariance, weights, censoring, or missing-data mechanism.
5. Add a seed only for stochastic computation and record environment/parallel/sampling controls.
6. Compare only genuinely viable alternatives. Record why excluded methods cannot answer the same estimand or represent the design.
7. Do not copy code from a card into the final script; Coder re-implements the confirmed method from its pinned platform spec/mapping.

Known hard exclusions: ordinary survival analysis is not an SSRT estimator; plain `statsmodels.Logit()` is not a repeated-measures GLMM; beta regression is not a substitute for binomial successes/denominators; acquisition code should save raw inputs rather than compute final paradigm scores.
