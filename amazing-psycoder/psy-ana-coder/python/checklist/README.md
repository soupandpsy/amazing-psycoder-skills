# Python Analysis Delivery Checklist

1. Config v1.2 passes deterministic validation; selected method/estimand/formula are complete.
2. Chosen Python estimator really supports the declared outcome family and dependence; plain `Logit()` is not GLMM.
3. Only confirmed cleaning/missingness rules run; exclusions retain source-row IDs, reasons, counts, and denominators.
4. Seed/backend controls exist when and only when stochastic steps require them.
5. Diagnostics and fallback/sensitivity rules match the estimator; no universal Shapiro gate.
6. Every substantive claim has a focal estimate and uncertainty.
7. Multiplicity handling matches the confirmed family of claims.
8. `pathlib`/config paths and fail-fast schema/type/level checks are present.
9. Declared tables/figures/reports are saved and traceable.
10. Python/platform/package snapshot and `analysis-run.json` are saved when run.

Block delivery for unresolved choices, unsupported estimators, invalid formulas, lost exclusion provenance, or ignored dependence. Static pass means ready for execution testing, not publication.
