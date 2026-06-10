# Stop-Signal — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [stop-signal](../../../psy-exp-designer/paradigms/stop-signal.md)
> **Status**: **CONFIG-DRIVEN** — no Pavlovia demo code found. Code generated from config YAML using the patterns below.

## Experiment Logic

On each trial, participants respond to a "go" stimulus. On a subset of trials (typically 25%), a "stop" signal appears after a variable delay (SSD), instructing them to withhold their response. The SSD is dynamically adjusted via a staircase to find the delay at which participants successfully inhibit 50% of the time. SSRT (stop-signal reaction time) is the primary measure.

## Trial Window Sequence

```
Fixation (500ms) → Go Stimulus (until response/stop) → [Stop Signal after SSD] → Feedback → ITI
```

The stop signal (auditory tone or visual cue) appears SSD ms after go stimulus onset. If stop signal appears, participant must withhold. If no stop signal, respond normally.

## Implementation Pattern

### Step 1: SSD Staircase Algorithm (Critical)

This is the most algorithmically complex paradigm in the system. The SSD must be tracked independently per staircase (if multiple) and adjusted trial-by-trial.

```python
# === SSD Staircase State ===
# Two independent trackers: one per staircase (if counterbalanced by condition)
ssd_trackers = {
    'staircase_1': {'ssd': INITIAL_SSD, 'direction': None},
    'staircase_2': {'ssd': INITIAL_SSD, 'direction': None},
}

SSD_STEP = 50       # ms — step size for SSD adjustment
SSD_MIN = 50        # ms — floor
SSD_MAX = 800       # ms — ceiling
STOP_PROBABILITY = 0.25  # proportion of trials with stop signal

def update_ssd(tracker, inhibited):
    """
    Staircase rule: after a stop trial:
    - If participant successfully inhibited → increase SSD by STEP (make it harder next time)
    - If participant failed to inhibit → decrease SSD by STEP (make it easier next time)
    
    This converges SSD toward the delay where p(inhibit) ≈ 0.5
    """
    if inhibited:
        tracker['ssd'] = min(tracker['ssd'] + SSD_STEP, SSD_MAX)
    else:
        tracker['ssd'] = max(tracker['ssd'] - SSD_STEP, SSD_MIN)
    return tracker['ssd']
```

### Step 2: Per-Trial Logic

```python
for trial in trials:
    # 1. Fixation
    show_fixation(FIXATION_DURATION)
    
    # 2. Determine if this is a stop trial
    is_stop_trial = random.random() < STOP_PROBABILITY
    tracker = get_tracker_for_trial(trial)
    
    # 3. Present go stimulus and start response window
    go_stim.draw()
    win.callOnFlip(kb.clock.reset)
    win.callOnFlip(kb.clearEvents)
    win.flip()
    
    go_stim_onset = core.getTime()
    stop_signal_presented = False
    response = None
    rt = None
    inhibited = False
    stop_rt = None  # for failed stops: RT relative to stop signal
    
    # 4. Timed response loop
    timer = core.CountdownTimer(DEADLINE / 1000.0)
    while timer.getTime() > 0:
        now = core.getTime()
        elapsed = (now - go_stim_onset) * 1000  # ms since go stimulus
        
        # 4a. Check if stop signal should fire
        if is_stop_trial and not stop_signal_presented and elapsed >= tracker['ssd']:
            present_stop_signal()  # play tone or flash visual stop cue
            stop_signal_presented = True
            stop_signal_time = now
        
        # 4b. Poll keyboard
        keys = kb.getKeys(keyList=GO_KEYS + ['escape'], waitRelease=False, clear=False)
        if keys:
            if keys[0].name == 'escape':
                save_and_quit()
            response = keys[0].name
            rt = keys[0].rt * 1000  # ms from go stimulus onset
            
            # On stop trials: response = failed inhibition
            if is_stop_trial:
                inhibited = False
                stop_rt = (now - stop_signal_time) * 1000 if stop_signal_presented else None
            break
    
    # 5. After response window
    if is_stop_trial and response is None:
        inhibited = True  # successfully withheld
    
    # 6. Update SSD (only on stop trials, per staircase)
    if is_stop_trial:
        update_ssd(tracker, inhibited)
    
    # 7. Save trial data
    save_trial_data(trial, is_stop_trial, tracker['ssd'], response, rt, inhibited, stop_rt)
```

### Step 3: Stop Signal Presentation

```python
def present_stop_signal():
    """Present auditory or visual stop signal."""
    if STOP_SIGNAL_TYPE == 'auditory':
        # Play a tone (750Hz, 100ms)
        stop_tone.play()
    elif STOP_SIGNAL_TYPE == 'visual':
        # Change fixation color or show a visual cue
        stop_cue.draw()
        win.flip()

# Preload stop signal stimulus
stop_tone = sound.Sound(STOP_SIGNAL_FILE) if STOP_SIGNAL_TYPE == 'auditory' else None
stop_cue = visual.TextStim(win, text='STOP', color='red', height=40) if STOP_SIGNAL_TYPE == 'visual' else None
```

### Step 4: SSRT Estimation (Post-Experiment)

```python
def estimate_ssrt(go_rts, ssd_mean, p_inhibit):
    """
    Integration method (Logan & Cowan, 1984):
    SSRT = mean_go_RT(at nth percentile) - mean_SSD
    where n = p(inhibit) × 100
    
    Example: if p(inhibit) = 0.48, find the 48th percentile of go RT distribution,
    subtract mean SSD from it.
    """
    nth_rt = np.percentile(go_rts, p_inhibit * 100)
    ssrt = nth_rt - ssd_mean
    return ssrt
```

### Key Edge Cases

- **Independent vs hierarchical tracking**: Independent = separate SSD per condition/stimulus. Hierarchical = one master SSD that all conditions inherit from. The config `paradigm_config.ssd_tracking` determines which.
- **SSD bounds**: Never let SSD go below 50ms (physically impossible to stop) or above the go deadline (trivial to stop). Clamp at boundaries.
- **Go trial RT monitoring**: Track mean go RT. If go RT drifts, SSD staircase may need context — a very slow responder may inhibit easily at long SSDs, inflating SSRT estimate.
- **Stop signal delay jitter**: Some implementations add ±25ms jitter to SSD to prevent participants from anticipating the exact stop timing.
- **Failed stop RT**: When a participant responds on a stop trial, the RT relative to the stop signal (not go stimulus) is meaningful for SSRT distribution analysis.

## Data Output Columns

Base columns + `is_stop_trial`, `ssd`, `inhibited` (1/0), `stop_rt` (RT from stop signal on failed stops, None otherwise), `staircase_id`
