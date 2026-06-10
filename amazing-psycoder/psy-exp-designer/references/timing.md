# Timing and Response Standard

Applies to all experiments, regardless of platform or paradigm.

## RT Measurement

Reaction time must be measured from **stimulus onset** (the moment the stimulus appears on screen), not from when the code reaches the `draw()` call.

### Platform-specific RT methods

| Platform | Method |
|----------|--------|
| PsychoPy | `win.callOnFlip(kb.clock.reset)` — reset keyboard clock on screen refresh |
| Psychtoolbox | `Screen('Flip')` returns flip timestamp; subtract from `GetSecs()` at response |
| jsPsych | `trial.data.rt` is automatically measured from stimulus onset |

### RT edge cases

- **Anticipatory (RT < 100ms)**: Record but flag. Exclude from analysis unless paradigm expects fast responses (e.g., masked priming).
- **Timeout (RT = null)**: Code as `-1` accuracy, empty RT. Do not record 0.
- **Multiple keys**: Record the first key and its RT. Later keys may be recorded in a separate `extra_keys` field.
- **No-go correct rejection**: RT is expected to be empty. Do not mark as error.

## Response Deadlines

- **Fixed deadline**: Same deadline for all trials (e.g., 2000ms)
- **Adaptive deadline**: Deadline adjusts based on running performance (implement with caution — complicates analysis)
- **Self-paced**: No deadline — participant presses a key to advance (use for instructions or subjective ratings, never for RT tasks)

## Timing Types

### Absolute timing
Duration is fixed regardless of screen refresh rate:
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
Used for brief presentations (masked priming) where frame accuracy matters. At 60Hz: 1 frame = ~16.7ms, 2 frames = ~33.3ms, 3 frames = ~50ms.

### Flip-based timing
Combine drawing and presentation:
```python
stim.draw()
win.flip()
timer = core.CountdownTimer(duration)
while timer.getTime() > 0:
    if 'escape' in event.getKeys():
        quit()
```
Used when Escape must remain responsive during the interval.

## Response Collection

- Always collect responses with Escape in the allowed key list
- Clear keyboard buffer before each trial's response window
- Prefer platform-native keyboard handling (PsychoPy: `keyboard.Keyboard`, jsPsych: plugin response parameters)
- Never block the event loop with `event.waitKeys()` or `event.getKeys(maxWait=...)`

## ITI and Jitter

- **Fixed ITI**: Same interval between all trials — predictable, may induce rhythmic responding
- **Variable ITI**: Random interval (e.g., 500-800ms uniform) — prevents rhythmic responding
- **Exponential ITI**: Long-tailed distribution — commonly used in fMRI designs
