# Analysis Method Comparison Examples

Use these as formatting examples, not as automatic recommendations. Re-evaluate all dimensions against the user's actual design and data.

## Paired t-test vs linear mixed model for RT

| Dimension | Paired t-test | Linear mixed model |
|-----------|---------------|--------------------|
| Statistical unit | One aggregate per subject/condition | Trial-level observations with random effects |
| Data utilization | Aggregates trials | Retains valid trials |
| Assumptions | Difference scores approximately normal | Residual/model assumptions; random-effects adequacy |
| Outliers | Aggregates can be sensitive | Still requires diagnostics and robust sensitivity checks |
| Interpretability | Familiar mean difference and Cohen's d | Fixed effects plus random-effects explanation |
| Extensibility | Limited | Adds covariates and interactions naturally |
| Computation | Simple | Requires convergence and singular-fit checks |

Recommendation pattern: prefer the t-test for a simple, pre-specified two-condition contrast when aggregation is justified; prefer a mixed model when trial-level variation or additional predictors matter. Do not claim that retaining more rows automatically increases valid power.

## ANOVA vs logistic mixed model for accuracy

| Dimension | ANOVA on proportions | Logistic mixed model |
|-----------|----------------------|----------------------|
| Outcome scale | Treats bounded proportions as continuous | Models binary trials on the logit scale |
| Ceiling/floor behavior | Can violate normality and equal-variance assumptions | Respects probability bounds |
| Data utilization | Usually aggregates trials | Retains trial-level responses |
| Interpretation | Percentage-point differences | Log-odds or odds ratios; marginal probabilities can aid interpretation |
| Complexity | Familiar and simple | Requires random-effects and convergence checks |

Recommendation pattern: prefer a binomial mixed model for trial-level accuracy, especially near ceiling/floor or with unequal trial counts. If using ANOVA on proportions, justify aggregation and verify assumptions.
