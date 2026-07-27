# R Analysis Platform Contract

Use this reference only after analysis config v1.2 passes validation. The config owns scientific choices; this file owns safe R implementation patterns.

## Canonical Structure

Keep these evidence-producing stages, but adapt their internal structure to the selected method:

1. Read config and record input/config hashes.
2. Load only required packages; capture versions.
3. Set seed/backend controls only when `model.stochastic: true`.
4. Import data through relative/configured paths and validate schema, types, levels, uniqueness, and denominators.
5. Apply only confirmed cleaning/missingness rules; retain immutable row IDs and a reason-coded exclusion log.
6. Produce sample-flow and descriptive summaries at the declared observation/clustering levels.
7. Fit `questions[].selected_method` to its declared estimand and formula.
8. Run estimator-appropriate diagnostics and prespecified fallback/sensitivity rules.
9. Report focal estimates, uncertainty, multiplicity handling, and claim-supporting tables/figures.
10. Save outputs plus `sessionInfo()` and an execution manifest.

Do not require all stages to use one fixed function or order. A paired test, GLMM, SSRT estimator, and Bayesian model need different diagnostics.

## Core Guard Pattern

```r
config <- yaml::read_yaml("analysis_config.yaml")
stopifnot(config$version == "1.2")
project_root <- fs::path_abs(getwd())

project_path <- function(value) {
  candidate <- fs::path_abs(value, start = project_root)
  relative <- fs::path_rel(candidate, start = project_root)
  if (relative == ".." || grepl("^\\.\\.[/\\\\]", relative)) {
    stop("Path escapes project root: ", value)
  }
  candidate
}

running_r <- paste(R.version$major, R.version$minor, sep = ".")
if (!identical(running_r, as.character(config$runtime$language_version))) {
  stop("R ", config$runtime$language_version, " required; running ", running_r)
}

dependency_path <- project_path(config$runtime$dependency_file)
if (!file.exists(dependency_path)) {
  stop("Declared dependency artifact is missing: ", dependency_path)
}

if (isTRUE(config$model$stochastic)) {
  stopifnot(!is.null(config$model$seed))
  set.seed(config$model$seed)
}

read_one <- function(path, file_format, options) {
  encoding <- if (is.null(options$encoding)) "UTF-8" else options$encoding
  switch(
    file_format,
    csv = readr::read_csv(path, locale = readr::locale(encoding = encoding), show_col_types = FALSE),
    tsv = readr::read_tsv(path, locale = readr::locale(encoding = encoding), show_col_types = FALSE),
    txt = readr::read_delim(path, delim = options$delimiter, locale = readr::locale(encoding = encoding), show_col_types = FALSE),
    xlsx = readxl::read_excel(path, sheet = options$sheet),
    parquet = arrow::read_parquet(path, as_data_frame = TRUE),
    json = tibble::as_tibble(jsonlite::fromJSON(path, flatten = TRUE)),
    stop("Unsupported file format: ", file_format)
  )
}

experiment <- config$experiment
data_path <- project_path(experiment$data_path)
loader_options <- experiment$loader_options
if (is.null(loader_options)) loader_options <- list()
if (isTRUE(experiment$multi_file)) {
  glob_pattern <- gsub("\\{[A-Za-z_][A-Za-z0-9_]*\\}", "*", experiment$file_pattern)
  input_files <- sort(Sys.glob(fs::path(data_path, glob_pattern)))
} else {
  input_files <- data_path
}
input_files <- input_files[file.exists(input_files) & !dir.exists(input_files)]
if (!length(input_files)) stop("No input files matched the confirmed analysis config")

frames <- lapply(input_files, function(input_file) {
  frame <- read_one(input_file, tolower(experiment$file_format), loader_options)
  frame$.source_file <- fs::path_rel(input_file, start = project_root)
  frame$.source_file_row <- seq_len(nrow(frame))
  frame
})
data_raw <- dplyr::bind_rows(frames)

required <- unique(c(
  config$experiment$id_columns$subject,
  unlist(lapply(config$design$ivs, `[[`, "name")),
  unlist(lapply(config$design$dvs, `[[`, "name"))
))
missing <- setdiff(required, names(data_raw))
if (length(missing)) stop("Missing columns: ", paste(missing, collapse = ", "))

data_work <- dplyr::mutate(data_raw, .source_row = dplyr::row_number())
exclusion_log <- tibble::tibble(.source_row = integer(), rule = character(), reason = character())
# Apply only config$cleaning rules here; never insert generic RT/accuracy/SD cutoffs.

# Fit the exact confirmed method/formula. Validate subject/item/session dependence first.
# Save tidy estimates, uncertainty, diagnostics, and prespecified sensitivity results.

output_dir <- project_path(config$output$save_path)
fs::dir_create(output_dir, recurse = TRUE)
writeLines(capture.output(sessionInfo()), fs::path(output_dir, "session-info.txt"))
```

## Method/API Guidance

| Need | Preferred R implementation |
|------|----------------------------|
| Paired/Welch contrast | `stats::t.test()` with explicit pairing/`var.equal = FALSE` |
| Repeated-measures ANOVA | `afex::aov_ez()` with declared factors and correction |
| Linear mixed model | `lme4::lmer()` / `lmerTest`, design-derived random structure |
| Binary/count GLMM | `lme4::glmer()` with appropriate family; check convergence/dispersion |
| Estimated contrasts | `emmeans` with declared scale and multiplicity rule |
| Focal effects | `effectsize`, `emmeans`, transformed coefficients, or bootstrap CI as appropriate |
| SSRT | Prespecified integration-method implementation with omission/replacement diagnostics |
| Environment | exact R-version check + `sessionInfo()` + declared `renv.lock` |

## Blocking Anti-Patterns

- Selecting a model or cleaning threshold because the config is incomplete.
- Overwriting raw data or losing source-row identity during exclusions.
- Treating Shapiro p > .05 as proof of normality or running it ceremonially per condition.
- Using ordinary ANOVA on trial-level binary outcomes without an explicitly justified aggregated estimand.
- Ignoring declared item/session/site dependence.
- Replacing the focal mixed-model contrast with marginal/conditional R².
- Choosing Type III sums of squares solely because the design is unbalanced.
- Using absolute user-specific paths, `setwd()`, end-only unsaved results, or missing environment capture.
- Treating `multi_file` as one file, silently choosing the first workbook sheet, or ignoring declared loader options.
- Declaring dependency locking without generating `runtime.dependency_file`, or allowing the lock and clean-run package snapshot to disagree.
- Comparing sensitivity analyses only by whether p crosses .05.

## Delivery Evidence

Static generation yields `ready_for_execution` at most. When an R runtime is available, execute through `tryCatch`/`on.exit` so both success and failure save a manifest with command/timestamps/exit status, config/code/`renv.lock`/input SHA-256 values available at that point, warnings/error trace, package snapshot, and generated artifacts plus hashes. Result audit must reject post-run hash drift.
