# Plot Card Usage Contract

Read this file before any individual plot card. Plot cards are visual-design reminders, not current API specifications or automatic prescriptions.

Choose a figure from the confirmed estimand, observation hierarchy, uncertainty, distribution/support, and intended audience. Preserve subject/item pairing and denominators where relevant; do not hide raw-data structure behind a bar chart or imply independence with unqualified error bars. Define every interval/error bar and avoid dual axes, truncated scales, or decorative encodings that alter interpretation.

Examples in cards may contain simplified data, older package calls, fixed palettes, or categorical claims such as “normal” based on a Q–Q plot. Treat those as provisional. Coder must implement the confirmed figure with the pinned platform spec, accessible colors/fonts, explicit units, saved output, and tests against the actual schema. A figure is not publication evidence until generated from the reviewed execution and checked against its source table/model.
