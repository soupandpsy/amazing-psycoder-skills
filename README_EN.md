<div align="center">

# 🧠 Amazing PsyCoder 💻

> From experiment idea to production-ready code. Design → Generate → Audit, three mandatory steps. 🪄

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Stars](https://img.shields.io/github/stars/soupandpsy/AmazingPsyCoderSkills?style=social)](https://github.com/soupandpsy/AmazingPsyCoderSkills)

[**简体中文**](README.md) · [**繁體中文**](README_ZH-HANT.md) · [**English**](README_EN.md) · [**日本語**](README_JA.md) · [**Deutsch**](README_DE.md) · [**Français**](README_FR.md)

<br>

[📖 Why](#-why-this-project-exists) · [⚡ Install](#-install) · [🚀 Quick Start](#-quick-start) · [🎬 Demo](#-demo) · [✨ Features](#-features) · [👥 Who It's For](#-who-its-for)

</div>

<br>

<table>
<tr><td align="left">

⏱️ &nbsp;Which screen does RT start from? Get the onset wrong, every reading is garbage.<br>
⌨️ &nbsp;Did you map the keys backwards? The participant presses correctly, the code scores it wrong.<br>
🚦 &nbsp;How is No-go "correct" even defined? When pressing is wrong and not-pressing is right.<br>
💾 &nbsp;Does the data survive a crash? Save-only-at-the-end means crash = everything lost.<br>
🔤 &nbsp;Chinese instructions render as □□□ — no CJK font configured, participants see garbled text.<br>
😇 &nbsp;It runs, but is it really ready for data collection? RT accuracy, logical correctness, data reliability — no systematic guarantee.

</td></tr>
</table>

### ✨ Amazing PsyCoder solves exactly these.

Not a code template you tweak yourself — more like a seasoned experiment-programming veteran sitting beside you. **Clarify your design → Generate the code → Audit before collection.**

Three mandatory steps. No skipping. **No code is delivered without passing review.**

---

## 📖 Why This Project Exists

Every lab has seniors who've stepped on every one of these mines, but that knowledge rarely gets passed down systematically. PsychoPy Builder or Coder? How do jsPsych timeline variables work? Why does `Screen('Flip')` need `vbl + (waitframes - 0.5) * ifi`?

Just figuring out the APIs takes weeks.

Amazing PsyCoder encodes these lessons into three mandatory Claude Code skills — design orchestration (5-phase confirmation), code generation (unified pipeline + 9-item quality gate), and code audit (smoke test protocol). Whether your lab uses PsychoPy, jsPsych, or Psychtoolbox, the same pipeline generates platform-appropriate code.

---

## 🎯 The Three Skills

| Skill | Role | Key Output |
|-------|------|-----------|
| 1️⃣ **Design** `psych-experiment-programming` | 5-phase progressive confirmation: trial timeline → response rules → condition table → block structure → final review | config YAML + condition tables |
| 2️⃣ **Code Gen** `psych-experiment-coder` | 4-layer priority architecture, 9-item quality gate. `time.sleep()` / `KbCheck` for RT rejected outright | runnable code + README |
| 3️⃣ **Audit** `psych-experiment-code-reviewer` | Smoke tests + data integrity checks + paradigm failure mode scans. RT onset, key mapping, data safety — item by item | audit report + readiness label |

---

## ⚡ Install

In Claude Code, enter the following instruction and the system will install automatically:

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/AmazingPsyCoderSkills
```

Claude Code will clone the repo and register all 4 skills into `~/.claude/skills/`. Once done, type `/amazing-psycoder` to launch.

<details>
<summary><b>🛠️ Manual install</b></summary>

<br>

```bash
git clone https://github.com/soupandpsy/AmazingPsyCoderSkills /tmp/AmazingPsyCoderSkills
cp -r /tmp/AmazingPsyCoderSkills/amazing-psycoder ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/psych-experiment-programming ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/psych-experiment-coder ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/psych-experiment-code-reviewer ~/.claude/skills/
```

</details>

---

## 🚀 Quick Start

In Claude Code, type `/amazing-psycoder` and describe your experiment:

> "I want a Stroop task, red/green/blue text, key-press response, 2 blocks of 60 trials each"

The system routes you to the orchestrator for the 5-phase design. During the process, it generates a trial window timeline:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Fixation  │ →  │ Stimulus  │ →  │ Blank     │ →  │ Feedback  │
│ +         │    │ Red "绿"  │    │           │    │ Correct!  │
│ 500ms     │    │ 2000ms    │    │ 500ms     │    │ 1000ms    │
│           │    │ ← press   │    │           │    │           │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                    RT onset
```

After confirming the timeline, choose your platform. Outputs a runnable file (`.py` / `.js` / `.m`) and an experiment README.

---

## 🎬 Demo

### 🐍 PsychoPy — Stroop Task

> "I want a Stroop task, red/green/blue text, judge ink color, 50:50 congruent:incongruent, 2 blocks × 60 trials"

```
User             ❯ I want a Stroop task

Amazing PsyCoder ❯ Let me confirm a few things first:
                   1. Three ink colors → three keys: f=red, j=green, k=blue. OK?
                   2. 50:50 congruent:incongruent. OK?
                   3. Fixation 500ms, stimulus max 2000ms, feedback 500ms,
                      ITI 600-900ms random. Use these defaults?

User             ❯ First two are fine. ITI should be 400-800ms.

Amazing PsyCoder ❯ Updated. Trial timeline:
                   ┌───────────────────────────────────────────────┐
                   │ Fixation(500ms) → Stimulus(2000ms/keypress)   │
                   │ → Feedback(500ms) → ITI(400-800ms)            │
                   └───────────────────────────────────────────────┘
                   All confirmed? Generate code?

User             ❯ Generate.

Amazing PsyCoder ❯ ✅ Code generated: stroop_task.py + README.md
                   Parameters at top, FONT_CONFIG set, incremental save on.
                   Run audit?

User             ❯ Audit.

Amazing PsyCoder ❯ 🔍 Audit passed. Readiness: ready_for_collection
                   Safe to start data collection.
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔬 **Common pitfalls blocked** | `time.sleep()`, `KbCheck` for RT — rejected before you even see them |
| 🚀 **Runnable out of the box** | Every editable parameter at the top of the file — no hunting |
| 🌏 **CJK text just works** | Auto-detects Chinese text, configures fonts — no □□□ |
| 🧪 **Crash-proof data** | Every trial saved to disk immediately — crash won't lose collected data |
| 🎛️ **One system, three platforms** | Same pipeline, whether you use PsychoPy, jsPsych, or Psychtoolbox |

**Less debugging at midnight, more confidence before you collect. 🧪✨**

---

## 📦 Platform Support

| Platform | Version | Use Case | Paradigms | Demos |
|----------|---------|----------|:--:|:--:|
| 🐍 **[PsychoPy](https://psychopy.org/)** | 2024.x+ | Local lab, USB HID hardware timestamps | 27 | 45 |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | 7.x | Online experiments, browser deployment | 25 | 23 |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | 3.0.21+ | GPU-level frame-precise control | 5 | 100 |

---

## 👥 Who It's For

- 👶 Don't really know how to code, but still have to ship an experiment
- 🎓 Undergrads and grad students writing (or about to write) experiment code
- 🧠 Researchers running cognitive, behavioral, or social psychology experiments
- 🐍 PsychoPy for local · 🌐 jsPsych for online · 🧮 Psychtoolbox / MATLAB
- 😵‍💫 Hit the same RT, randomization, and condition table pitfalls before — looking for systematic quality assurance

---

## 📦 Paradigm Coverage

**38 paradigms**: 14 core (full design specs) + 24 extended (reference descriptions)

| Type | Paradigms |
|------|-----------|
| **Core** | Go/No-go · Navon · Priming · Stroop · Eriksen Flanker · Simon · Rating · Stop-signal · IAT · N-back · Dot-probe · Visual Search · Task Switching · EAST |
| **Extended** | Antisaccade · ANT · BART · Bilingual Stroop · Change Detection · Choice RT · CPT · Corsi Blocks · Cyberball · Delay Discounting · Mental Rotation · Posner Cuing · Sternberg · WCST, and more |

---

## 📂 File Structure

```
AmazingPsyCoderSkills/
├── amazing-psycoder/                  ← Orchestrator (entry point)
├── psych-experiment-programming/      ← ① Design layer (5-phase workflow + 38 paradigms)
├── psych-experiment-coder/            ← ② Code generation layer
│   ├── psychopy/
│   ├── jspsych/
│   └── psychtoolbox/
└── psych-experiment-code-reviewer/    ← ③ Audit layer (5 modes + smoke testing)
```

---

<div align="center">

Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
