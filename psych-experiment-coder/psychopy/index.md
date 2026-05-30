# PsychoPy — Platform Index

> **状态**: Full auto code generation | **范式**: 27 | **Demo**: 45 `.py`

## Quick links

| Layer | Path | Content |
|-------|------|---------|
| L1 Spec | [spec/README.md](spec/README.md) | Canonical Code Skeleton + 19 anti-patterns + API spec |
| L2 Mapping | [mapping/README.md](mapping/README.md) | Config→code mapping, 3 window modes, 3-version comparison |
| L3 Paradigms | [paradigms/](paradigms/) | 27 paradigm reference files |
| L4 Demos | [demo/_raw/](demo/_raw/) | 45 Pavlovia-exported `.py` files |

## Mandatory API quick reference

| Category | Use | Never |
|----------|-----|-------|
| Keyboard | `keyboard.Keyboard(backend='ptb')` | `event.getKeys(maxWait=)` |
| RT source | `key.rt` | `kb.clock.getTime()` |
| RT onset | `win.callOnFlip(kb.clock.reset)` | manual `clock.reset()` before flip |
| Timing | `CountdownTimer` | `time.sleep()` / `core.wait()` |
| Data save | `try/finally` + per-trial flush | save only at end |
| Escape | check in every loop | no escape handler |

## Paradigm quick list

Stroop · Go/No-go · Eriksen Flanker · Simon · N-back · Dot-probe · Visual Search · Task Switching · Stop-signal · IAT · Priming · Rating · Navon · Antisaccade · Change Detection · Choice RT · Cyberball · Delay Discounting · Mental Rotation · Multisensory Nature · Numerical Stroop · Phone a Friend · Psychophysics Staircase · Sternberg · Ultimatum Game · WCST · Writing Distraction
