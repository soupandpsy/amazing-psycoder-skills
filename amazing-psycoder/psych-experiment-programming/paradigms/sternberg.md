# Sternberg Memory Scanning Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/sternberg) · reference

## When to Use

User mentions: Sternberg task, memory scanning, short-term memory search, set size effect, 斯滕伯格任务, 记忆扫描. Measures the speed and nature of short-term memory retrieval by varying the number of items held in a memory set and measuring the time to determine whether a probe was present.

## Core Logic

On each trial, participants are shown a memory set of items (typically digits, e.g., "3 7 1") to memorize. After a brief retention interval, a single probe item is presented. Participants respond whether the probe was present in the memory set (yes/no judgment). The critical manipulation is the set size — the number of items in the memory set — which varies from trial to trial (e.g., 1 to 6 items).

Sternberg's (1969) classic finding is that RT increases linearly with set size at approximately 30-40 ms per additional item, and the slope is roughly equal for both positive (probe present) and negative (probe absent) responses. This parallel slope pattern supports a serial, exhaustive search model: the entire memory set is scanned on every trial, even when the probe is found early (self-terminating search would predict shallower slopes for positive trials). The intercept of the RT function estimates encoding + response time, while the slope estimates scanning rate per item.

This implementation uses a precisely timed trial sequence with all items of the memory set shown simultaneously: fixation cross for 1.0 s, memory set display for 1.5 s (digits as a space-separated string, e.g., "3 7 1"), a 2.0 s blank retention interval, then the probe digit appears. The keyboard begins listening at probe onset for frame-accurate RT. Response reminders ("LEFT if it was NOT" / "RIGHT if it WAS") appear after the probe has been on screen briefly. 

Design includes a practice block (with 1.0 s feedback showing "Correct! RT=Nms" or "Oops! That was wrong") followed by the main block (no feedback). Separate condition files (`pracTrials.xlsx`, `mainTrials.xlsx`) each have columns: `numberSet` (memory set string), `target` (probe digit string), and `corrAns` ('left' or 'right').

## Must Confirm

- **Set sizes**: Which memory set sizes to include? (typically 1-6 items)
- **Stimulus type**: Digits, letters, words, or other?
- **Memory set presentation**: Simultaneous (all items at once) or sequential (one at a time)?
- **Timing**: Fixation duration, memory set display duration, retention interval length?
- **Response mapping**: Which keys for "yes/in set" and "no/not in set"?
- **Practice**: Include a practice block with RT feedback before the main task?
- **Trial count**: How many trials per set size per response type (positive/negative)?

## Trial Window Timeline

```text
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ Window 1             │→ │ Window 2             │→ │ Window 3             │→ │ Window 4             │→ │ Window 5             │
│ Fixation             │  │ Memory Set           │  │ Retention Interval   │  │ Probe                │  │ Feedback (practice   │
│ Content: +           │  │ Content: digits      │  │ Content: blank       │  │ Content: digit       │  │ only)                │
│ Duration: 1.0 s      │  │ (e.g., "3 7 1")      │  │ Duration: 2.0 s      │  │ Duration: ≤2.0 s     │  │ Content: correct/    │
│ Response: none       │  │ starts at t=1.2 s    │  │ Response: none       │  │ starts at t=4.7 s    │  │ incorrect + RT       │
│ Data: none           │  │ Duration: 1.5 s      │  │ Data: none           │  │ Response: left/right │  │ Duration: 1.0 s      │
│                      │  │ Response: none       │  │                      │  │ Data: rt, key, acc   │  │ Response: none       │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

## Data Analysis

Plot mean RT as a function of set size, separately for positive and negative trials. Fit linear regression to estimate slope (ms/item) and intercept. Compare slopes between positive and negative responses (serial exhaustive vs. self-terminating). Test whether different populations (e.g., older adults, schizophrenia patients) show steeper slopes (slower scanning) or higher intercepts (slower encoding/response). Also analyze accuracy to ensure ceiling-level performance.

## References

Sternberg, S. (1969). Memory-scanning: Mental processes revealed by reaction-time experiments. *American Scientist, 57*(4), 421–457.
