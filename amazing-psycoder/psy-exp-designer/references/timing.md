# Timing and Response Standard

Applies to all experiments, regardless of platform or paradigm.

## RT Measurement

Reaction time must use the confirmed response event and a recorded software onset reference tied to the relevant flip/audio/device event, not the moment code reaches `draw()`. When physical onset accuracy matters, the collection hardware must be measured; a software timestamp alone is not proof of photons or sound at the participant.

### Platform-specific RT methods

| Platform | Method |
|----------|--------|
| PsychoPy | Reset the keyboard clock with `win.callOnFlip(kb.clock.reset)` and use the selected backend's `key.rt` for key-down tasks; release/duration tasks use their declared event fields |
| Psychtoolbox | Use the `Screen('Flip')` VBL timestamp as the visual reference and the relevant `KbQueue` event timestamp such as `firstPress`; RT is event timestamp minus onset reference |
| jsPsych | Use the selected plugin's documented `data.rt`/event fields; pin core/plugin/browser targets and test the deployed device rather than assuming physical-onset accuracy |

### RT edge cases

- **Anticipatory rule**: Derive the threshold/rule from the task, device, protocol, and literature. Retain the raw event and flag it; exclusions belong to the confirmed analysis plan.
- **Timeout**: Keep RT truly missing (`null`/empty/NA), set `response_status: timeout`, and code accuracy from the confirmed task rule. Never use numeric missing sentinels such as `-1` or `-999`.
- **Multiple events**: Apply the confirmed event-selection rule. For a first-response task, preserve the first eligible event and optionally record later events in a linked event table.
- **No-go correct rejection**: RT is expected to be empty. Do not mark as error.

## Response Deadlines

- **Fixed deadline**: Same deadline for all trials (e.g., 2000ms)
- **Adaptive deadline**: Deadline adjusts based on running performance (implement with caution — complicates analysis)
- **Self-paced**: No externally imposed deadline; valid for instructions/ratings and for designs where self-paced latency is itself a declared measure. It must not arise accidentally from a missing deadline.

## Timing Types

### Wall-clock blocking (not a visual-onset guarantee)
This call blocks concurrent event handling and is not an implementation pattern for an interactive visual interval:
```python
core.wait(0.5)  # 500ms, but blocks event loop
```

### Frame-based timing
Duration is measured in screen refresh cycles (frames):
```python
for _ in range(FRAMES):
    stim.draw()
    win.flip()
```
Used for brief presentations where frame synchronization matters. Convert frames using the measured refresh interval of the target display; do not assume 60 Hz.

### Flip-based timing
Combine drawing and presentation:
```python
stim.draw()
win.callOnFlip(kb.clearEvents)
win.flip()
timer = core.CountdownTimer(duration)
while timer.getTime() > 0:
    if kb.getKeys(keyList=['escape'], waitRelease=False):
        save_and_quit()
```
Used when Escape must remain responsive during the interval.

## Response Collection

- Provide a documented abort action that remains reachable during every active response/timing loop; it may be separate from the scored response set
- Clear keyboard buffer before each trial's response window
- Prefer platform-native keyboard handling (PsychoPy: `keyboard.Keyboard`, jsPsych: plugin response parameters)
- Never block the event loop with `event.waitKeys()` or `event.getKeys(maxWait=...)`

## ITI and Jitter

- **Fixed ITI**: Same interval between all trials — predictable, may induce rhythmic responding
- **Variable ITI**: A confirmed seeded distribution may reduce temporal predictability; record the realized duration and do not claim it eliminates rhythmic responding
- **Exponential ITI**: Long-tailed distribution — commonly used in fMRI designs
