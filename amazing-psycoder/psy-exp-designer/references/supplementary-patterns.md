# Supplementary Experiment Patterns

Load this reference only when the experiment includes questionnaires, scales, participant-facing scores, or debrief feedback.

## Questionnaire and demographic sequences

Insert a questionnaire sequence between the main sequence design and final validation. Reuse the window → condition → sequence model.

- Represent a demographic item as one form/window with an explicit response type and validation rule.
- Represent a multi-item scale as one trial per item, driven by condition columns such as `scale_name`, `item_id`, `item_text`, and `reverse_scored`.
- Record the raw response, item identifier, scale identifier, and presentation order on every item trial.
- Confirm required/optional status, response range, missing-response handling, and whether back-navigation is allowed.
- Do not infer sensitive demographic questions; include only fields required by the study protocol and ethics approval.

## Reverse scoring and scale computation

Keep raw responses unchanged. Compute derived scores separately using the confirmed scale range:

```text
reverse_score = minimum + maximum - raw_response
```

Record the scoring key, included items, missing-item policy, and minimum completion rate in the config. Do not present a scale score to participants unless the protocol explicitly requires and ethically supports it.

## Debrief and participant-facing feedback

Use a `debrief` sequence after formal trials and before the final exit screen.

- Always provide the approved study debrief text and a clean exit path.
- Show task performance or scale feedback only when explicitly requested in the study protocol.
- Separate participant-facing feedback from research-grade analysis; label preliminary summaries clearly.
- Avoid diagnostic or clinical interpretations unless the instrument and protocol explicitly authorize them.
- Save any derived feedback values with the formula/version used, without overwriting raw trial data.

## Validation additions

- Verify every questionnaire condition column exists.
- Verify allowed response values and validation messages.
- Verify reverse-scored item identifiers against the scoring key.
- Verify privacy-sensitive fields are excluded from logs and filenames.
- Verify participants can complete, skip, or withdraw exactly as the protocol specifies.
