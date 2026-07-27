# Data Recording Contract

**Output**: a durable trial-summary table for every experiment, plus a linked event table when a trial can contain repeated responses, clicks, gaze samples, state transitions, or other one-to-many events.

The schema is semantic rather than paradigm-blind: fields that do not apply are omitted or documented as missing. Never force a rating, free-text task, passive-viewing trial, or adaptive procedure into a keypress-only schema.

## Trial-Summary Requirements

Every row must support these roles, although projects may use different documented column names:

| Role | Required content |
|------|------------------|
| Participant/session identity | Pseudonymous `subject_id` and, when repeat sessions are possible, `session_id` |
| Trial identity | Unique trial identifier plus sequence/run/trial indices that reconstruct order |
| Design identity | Condition/trial type and stimulus or item identifier needed to reconstruct the manipulation |
| Exposure | Whether the trial started/completed/aborted and the realized stimulus/timing values, including adaptive values |
| Response | Recorded response value/type when applicable; missing must not be confused with a real response |
| Timing | Declared RT field and unit when RT is an outcome, with its onset/event definitions; no plausible numeric sentinel for missing RT |
| Scoring | Correct answer and accuracy only when the task defines them; scoring convention documented |
| Provenance | Experiment/config version and sufficient timestamp/order information to trace the run |

Also record paradigm-specific fields needed by the confirmed analysis: for example SSD and stop success, target/lure status, IAT block role, probe side, counterbalance cell, or item identity. The experiment code should acquire these inputs; derived scientific scores such as SSRT, D-score, d-prime, or bias scores belong in the analysis pipeline.

## Repeated Event Table

Use a second table when one trial can emit multiple events. Each row includes `subject_id`, `session_id` when applicable, `trial_id`, an event sequence number, event type/value, and a timestamp relative to a documented origin. The foreign key to the trial-summary row must be validated.

## Response and Missingness Rules

- Store a separate response status such as `responded`, `timeout`, `correct_rejection`, `aborted`, or `device_error` when these states are scientifically distinct.
- RT is missing for a timeout or valid no-response; never encode missing RT as `0`, `-1`, or `-999`.
- Accuracy may be `1`/`0` only when correctness is defined. A go-trial timeout may be scored `0` if omission is incorrect; a no-go withholding may be scored `1`. Keep the response status separate so these cases remain distinguishable.
- Preserve raw response/timing fields. Recode exclusions and derived scores in analysis with an auditable log.

## Persistence Rules

1. Create a durable checkpoint after every completed trial. For browser tasks, choose a configured server, IndexedDB, or a tested device-local store according to payload, quota, privacy, and recovery requirements; an in-memory jsPsych object is not a checkpoint. `localStorage` qualifies only as a bounded, device-local checkpoint after quota/failure/recovery testing and is not a remote backup.
2. Flush/commit the checkpoint before starting the next trial when feasible, and document any bounded-loss tradeoff.
3. Route normal completion, Escape/abort, and runtime exceptions through cleanup that closes files/devices and preserves completed rows.
4. Use collision-resistant filenames or storage keys containing pseudonymous participant/session identity and task/version metadata.
5. Use a documented machine-readable encoding and delimiter (UTF-8 CSV is acceptable); quote/escape free text correctly.

## Verification

Before collection, inspect at least one normal run, one timeout/no-response case, one incorrect response, and one interrupted run. Confirm unique trial IDs, declared columns/types/units, design reconstruction, event-table linkage, response-status distinctions, and recovery of all committed trials.
