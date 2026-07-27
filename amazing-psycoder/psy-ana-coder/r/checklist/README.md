# R Analysis Delivery Checklist

1. Config v1.2 passes deterministic validation; selected method/estimand/formula are complete.
2. Declared subject/item/session/site dependence is represented or explicitly justified.
3. Only confirmed cleaning/missingness rules run; exclusions retain row IDs, reasons, counts, and denominators.
4. Seed/backend controls exist when and only when stochastic steps require them.
5. Diagnostics and fallback/sensitivity rules match the estimator; no ceremonial Shapiro gate.
6. Every substantive claim has a focal estimate and uncertainty; R² is not substituted for a contrast.
7. Multiplicity handling matches the family of claims in config.
8. Paths are project-relative/configured; schema/types/levels are fail-fast validated.
9. Declared tables/figures/reports are saved and traceable to config/code.
10. `sessionInfo()`/package lock and execution manifest are saved when run.

Block delivery for unresolved scientific choices, invalid formulas, lost exclusion provenance, or unrepresented dependence. Static pass means ready for execution testing, not publication.
