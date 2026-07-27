# Psychtoolbox — Platform Index

> **Status**: Reference-complete, manual generation | **范式**: 5 | **Demo**: 100 `.md` (_raw/)

## Quick links

| Layer | Path | Content |
|-------|------|---------|
| L1 Spec | [spec/README.md](spec/README.md) | Canonical Code Skeleton + 18 anti-patterns + API reference |
| L2 Mapping | [mapping/README.md](mapping/README.md) | 12-step template + 3 frame-loop patterns + config→MATLAB |
| L3 Paradigms | [paradigms/](paradigms/) | 5 paradigm reference files |
| L4 Demos | [demo/_raw/](demo/_raw/) | 100 `.md` by category (getting-started, drawing, animated, textures, text, 3D-VR, other) |

## Mandatory API quick reference

| Category | Use | Never |
|----------|-----|-------|
| Keyboard | `KbQueueCreate` + `KbQueueCheck` | `KbCheck` / `KbWait` for RT |
| RT onset | `VBLTimestamp` = `Screen('Flip')` return | `GetSecs` |
| RT calc | `(min(firstPress) - stimOnset) * 1000` | `secs - tStimFlip` |
| Timing | `vbl + (waitframes-0.5)*ifi` | `WaitSecs()` for trial timing |
| Data save | `fopen/fprintf/fclose` incremental | workspace matrix |
| Cleanup | `try/catch/sca/Priority(0)/ShowCursor` | bare `sca` |

## Paradigm quick list

Stroop · Posner Cuing · Orientation Threshold · Likert Scale · Slider
