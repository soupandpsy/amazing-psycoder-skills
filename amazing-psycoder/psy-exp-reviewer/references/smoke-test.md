# Experiment Smoke Test

Run this test on the target machine before collecting real data. Adapt the launch and force-quit commands to the detected platform and operating system.

## Test 1: Launch and clean exit

1. Run the exact experiment launch command with subject ID `smoke_launch`.
2. Verify the window opens at the intended display, resolution, and fullscreen setting.
3. Verify instructions and CJK text render correctly and the console shows no errors.
4. Press Escape during an active screen and verify display, cursor, audio, priority, and hardware handles are restored.

## Test 2: Full run-through

1. Run with subject ID `smoke_full` using a shortened but structurally complete condition set.
2. Complete instructions and practice; verify key mapping and feedback.
3. Complete every block type and transition, including rest/debrief screens.
4. Verify the final screen and normal exit path.

## Test 3: Data output

1. Open the produced data file.
2. Verify one row per completed trial and the expected row count.
3. Verify every required column, numeric RT for responses, correct timeout/no-response coding, accuracy coding, condition identity, block/trial indices, and subject ID.
4. Compare at least three trial responses against what happened on screen.
5. Verify condition counts and task-relevant correct-key mapping against the confirmed spec.

## Test 4: Incremental-save recovery

1. Run with subject ID `smoke_crash`.
2. Force-quit after approximately ten trials using an OS-appropriate method.
3. PsychoPy/PTB: reopen the data file. jsPsych: inspect the configured server/IndexedDB/localStorage checkpoint and exercise its recovery/export path.
4. Verify all completed trials survived with no partial/corrupt row; end-only in-memory data or end-only `localSave` fails this test.
5. Relaunch with a new subject ID and verify the previous file/checkpoint is not overwritten.

## Test 5: Edge cases

1. Press disallowed keys; verify they are ignored and not recorded as valid responses.
2. Press a response before onset; verify the keyboard buffer prevents contamination.
3. Allow a response deadline to expire; verify timeout coding.
4. Test the first and last trial of each block and any no-go/catch/stop condition.
5. If hardware/audio is used, verify trigger/audio onset and cleanup with the actual device.

Do not infer that a smoke test passed from code inspection. For each test, write a `RuntimeEvidence` record defined in `review-report-schema.md`: test ID, exact target environment, observed timestamp, command/procedure, concrete observations, and paths to inspected logs/data/screenshots/notes. The Reviewer must resolve and inspect those paths (or clearly label inaccessible user-attested evidence as insufficient for a collection-ready verdict); it must not fabricate evidence or convert a planned test into `passed`.

## Pre-first-subject checklist

- [ ] All five smoke tests passed on the target machine.
- [ ] Monitor resolution, refresh rate, scaling, and calibration are correct.
- [ ] Audio volume and response device were tested at the participant position.
- [ ] Hardware triggers were checked with the receiving device, when applicable.
- [ ] Data directory is writable and filenames cannot overwrite prior participants.
- [ ] jsPsych durable checkpoint storage and recovery/export were tested when applicable.
- [ ] Backup/recovery procedure is documented.
- [ ] Experimenter knows the normal and emergency quit procedures.
- [ ] Participant briefing, consent, withdrawal, and debrief procedures are ready.
