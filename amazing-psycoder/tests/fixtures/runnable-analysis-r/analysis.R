args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (!length(file_arg)) stop("Run this fixture with Rscript")
project_root <- normalizePath(dirname(sub("^--file=", "", file_arg[[1]])), mustWork = TRUE)
config_path <- file.path(project_root, "config.yaml")
config <- yaml::read_yaml(config_path)
iso_time <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%OS6Z", tz = "UTC")
started_at <- iso_time()

project_path <- function(value) {
  candidate <- normalizePath(file.path(project_root, value), mustWork = FALSE)
  relative <- substring(candidate, nchar(project_root) + 2L)
  if (identical(candidate, project_root) || startsWith(relative, "..")) {
    stop("Path escapes project root: ", value)
  }
  candidate
}

output_dir <- project_path(config$output$save_path)
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
execution_log <- file.path(output_dir, config$output$execution_log)
dependency_file <- project_path(config$runtime$dependency_file)
input_files <- character()

file_hash <- function(path) {
  digest::digest(file = path, algo = "sha256", serialize = FALSE)
}

running_r <- paste(R.version$major, R.version$minor, sep = ".")

write_failure <- function(error) {
  failure <- list(
    command = "Rscript analysis.R",
    started_at = started_at,
    ended_at = iso_time(),
    exit_status = 1L,
    config_sha256 = file_hash(config_path),
    code_sha256 = file_hash(file.path(project_root, "analysis.R")),
    dependency_sha256 = if (file.exists(dependency_file)) file_hash(dependency_file) else NULL,
    input_sha256 = setNames(lapply(input_files[file.exists(input_files)], file_hash), sub(paste0("^", project_root, "/"), "", input_files[file.exists(input_files)])),
    outputs_sha256 = list(),
    warnings = list(),
    environment = list(r = running_r, dependency_file = config$runtime$dependency_file),
    error = conditionMessage(error)
  )
  jsonlite::write_json(failure, execution_log, auto_unbox = TRUE, pretty = TRUE, null = "null")
}

main <- function() {
  if (!identical(running_r, as.character(config$runtime$language_version))) {
    stop("running R version does not match config.runtime.language_version")
  }
  if (!file.exists(dependency_file)) stop("declared renv.lock is missing")

  lock <- jsonlite::read_json(dependency_file, simplifyVector = FALSE)
  used_packages <- c("digest", "jsonlite", "yaml")
  for (package in used_packages) {
    locked <- lock$Packages[[package]]$Version
    installed <- as.character(utils::packageVersion(package))
    if (!identical(installed, locked)) stop("installed ", package, " does not match renv.lock")
  }

  data_path <- project_path(config$experiment$data_path)
  input_files <<- data_path
  data_raw <- utils::read.csv(data_path, stringsAsFactors = FALSE)
  required_columns <- c("subject_id", "condition", "rt")
  missing_columns <- setdiff(required_columns, names(data_raw))
  if (length(missing_columns)) stop("Missing required columns: ", paste(missing_columns, collapse = ", "))
  if (!setequal(unique(data_raw$condition), c("control", "experimental"))) stop("Condition levels do not match config")

  data_raw$source_row <- seq_len(nrow(data_raw))
  reason <- rep(NA_character_, nrow(data_raw))
  reason[is.na(data_raw$rt)] <- "missing_rt"
  reason[!is.na(data_raw$rt) & data_raw$rt < config$cleaning$rt_lower] <- "rt_below_confirmed_bound"
  reason[!is.na(data_raw$rt) & data_raw$rt > config$cleaning$rt_upper] <- "rt_above_confirmed_bound"
  exclusion_log <- data_raw[!is.na(reason), c("source_row", "subject_id", "condition", "rt"), drop = FALSE]
  exclusion_log$reason <- reason[!is.na(reason)]
  analysis_data <- data_raw[is.na(reason), , drop = FALSE]

  control <- analysis_data[analysis_data$condition == "control", c("subject_id", "rt")]
  experimental <- analysis_data[analysis_data$condition == "experimental", c("subject_id", "rt")]
  names(control)[2] <- "control"
  names(experimental)[2] <- "experimental"
  paired <- merge(control, experimental, by = "subject_id", all = FALSE)
  if (!nrow(paired)) stop("No complete subject pairs remain")
  differences <- paired$experimental - paired$control

  captured_warnings <- character()
  test <- withCallingHandlers(
    stats::t.test(paired$experimental, paired$control, paired = TRUE),
    warning = function(w) {
      captured_warnings <<- c(captured_warnings, conditionMessage(w))
      invokeRestart("muffleWarning")
    }
  )
  confidence <- unname(test$conf.int)
  result <- data.frame(
    n_pairs = nrow(paired),
    estimate = mean(differences),
    std_error = stats::sd(differences) / sqrt(length(differences)),
    CI_low = confidence[[1]],
    CI_high = confidence[[2]],
    t = unname(test$statistic),
    p_value = test$p.value
  )
  descriptive <- stats::aggregate(rt ~ condition, data = analysis_data, FUN = function(x) c(n = length(x), mean = mean(x), sd = stats::sd(x), median = stats::median(x)))
  diagnostics <- list(n_pairs = nrow(paired), all_finite = all(is.finite(differences)), difference_sd = stats::sd(differences))
  environment <- list(
    r = running_r,
    dependency_file = config$runtime$dependency_file,
    packages = setNames(lapply(used_packages, function(package) as.character(utils::packageVersion(package))), used_packages),
    sessionInfo = capture.output(utils::sessionInfo())
  )

  utils::write.csv(result, file.path(output_dir, "paired-contrast.csv"), row.names = FALSE)
  utils::write.csv(descriptive, file.path(output_dir, "descriptive-statistics.csv"), row.names = FALSE)
  utils::write.csv(exclusion_log, file.path(output_dir, "exclusion-log.csv"), row.names = FALSE)
  jsonlite::write_json(diagnostics, file.path(output_dir, "model-diagnostics.json"), auto_unbox = TRUE, pretty = TRUE)
  jsonlite::write_json(environment, file.path(output_dir, "environment.json"), auto_unbox = TRUE, pretty = TRUE)
  writeLines(c(
    "---", "title: \"Paired RT analysis\"", "output: html_document", "---", "",
    "The hashed CSV and JSON artifacts in this directory are produced by `analysis.R`."
  ), file.path(output_dir, "report.Rmd"))

  output_names <- c("paired-contrast.csv", "descriptive-statistics.csv", "exclusion-log.csv", "model-diagnostics.json", "environment.json", "report.Rmd")
  success <- list(
    command = "Rscript analysis.R",
    started_at = started_at,
    ended_at = iso_time(),
    exit_status = 0L,
    config_sha256 = file_hash(config_path),
    code_sha256 = file_hash(file.path(project_root, "analysis.R")),
    dependency_sha256 = file_hash(dependency_file),
    input_sha256 = setNames(lapply(input_files, file_hash), sub(paste0("^", project_root, "/"), "", input_files)),
    outputs_sha256 = setNames(lapply(file.path(output_dir, output_names), file_hash), output_names),
    warnings = as.list(captured_warnings),
    environment = environment,
    error = NULL
  )
  jsonlite::write_json(success, execution_log, auto_unbox = TRUE, pretty = TRUE, null = "null")
}

tryCatch(main(), error = function(error) {
  write_failure(error)
  stop(error)
})
