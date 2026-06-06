<div align="center">

# 🧠 Amazing PsyCoder 💻

> From experiment idea to production-ready code. Design → Generate → Audit, three mandatory steps. 🪄

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Codex](https://img.shields.io/badge/Codex-Skill-green)](https://github.com/openai/codex)
[![Hermes](https://img.shields.io/badge/Hermes-Skill-orange)](https://github.com/NousResearch/hermes-agent)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-red)](https://github.com/openclaw/openclaw)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-standard-333)](https://agentskills.io)
[![Stars](https://img.shields.io/github/stars/soupandpsy/amazing-psycoder-skills?style=social)](https://github.com/soupandpsy/amazing-psycoder-skills)

[**简体中文**](../README.md) · [**繁體中文**](README_ZH-HANT.md) · [**English**](README_EN.md) · [**日本語**](README_JA.md) · [**Deutsch**](README_DE.md) · [**Français**](README_FR.md)

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

Amazing PsyCoder encodes these lessons into three mandatory skills — design orchestration (5-phase confirmation), code generation (unified pipeline + 9-item quality gate), and code audit (smoke test protocol). Whether your lab uses PsychoPy, jsPsych, or Psychtoolbox, the same pipeline generates platform-appropriate code.

---

## 🎯 The Three Skills

| Skill | Role | Key Output |
|-------|------|-----------|
| 1️⃣ **Design** `psych-experiment-programming` | 5-phase progressive confirmation: trial timeline → response rules → condition table → block structure → final review | config YAML + condition tables |
| 2️⃣ **Code Gen** `psych-experiment-coder` | 4-layer priority architecture, 9-item quality gate. `time.sleep()` / `KbCheck` for RT rejected outright | runnable code + README |
| 3️⃣ **Audit** `psych-experiment-code-reviewer` | Smoke tests + data integrity checks + paradigm failure mode scans. RT onset, key mapping, data safety — item by item | audit report + readiness label |

---

## ⚡ Install

Type the command for your platform directly in your AI chat:

**Claude Code**
```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/amazing-psycoder-skills
```

**Codex**
```
$skill-installer
```
Enter repo URL: `https://github.com/soupandpsy/amazing-psycoder-skills`

**Hermes**
```
hermes skills install https://github.com/soupandpsy/amazing-psycoder-skills
```

**OpenClaw**
```
npm i -g clawhub && clawhub install amazing-psycoder
```

Then type `/amazing-psycoder` to launch.

<details>
<summary><b>Other install methods</b></summary>

<br>

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills && cd amazing-psycoder-skills/amazing-psycoder && ./install.sh
```

**Manual copy**:

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills /tmp/amazing-psycoder-skills
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder <skills-dir>/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psych-experiment-{programming,coder,code-reviewer} <skills-dir>/
```

</details>

---

## 🚀 Quick Start

Type `/amazing-psycoder` (or let the agent auto-match the skill) and describe your experiment:

> "I want a Stroop task, red/green/blue text, key-press response, 2 blocks of 60 trials each"

The system routes you to the orchestrator for the 5-phase design. During the process, it generates a trial window timeline:

```
   Window 1: Fixation            Window 2: Stimulus             Window 3: Blank     
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│                      │      │                      │      │                      │
│          +           │  →   │     Red (green)      │  →   │                      │
│                      │      │                      │      │                      │
└──────────────────────┘      └──────────────────────┘      └──────────────────────┘
         500ms                         2000ms                        500ms          
        no resp                       ← press                      no resp         
                                      RT onset                                      

   Window 4: Feedback   
┌──────────────────────┐
│                      │
│       Correct!       │
│                      │
└──────────────────────┘
         1000ms         
        no resp         
```

After confirming the timeline, choose your platform. Outputs a runnable file (`.py` / `.js` / `.m`) and an experiment README.

---

## 🎬 Demo

### 🐍 PsychoPy — Stroop Task

> "I want a Stroop task, red/green/blue text, judge ink color, 50:50 congruent:incongruent, 2 blocks × 60 trials"

```
User             ❯ I want a Stroop task

Amazing PsyCoder ❯ 🟢 Phase 1/5 · Assess
                   Paradigm Stroop · Confirm platform: PsychoPy?

User             ❯ Yes, PsychoPy.

Amazing PsyCoder ❯ 🟢 Phase 2/5 · Trial Windows + Response Rules (most critical)
                   Ink colors → f=red j=green k=blue. Trial timeline:
                      Window 1: Fixation            Window 2: Stimulus             Window 3: Blank     
                   ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
                   │                      │      │                      │      │                      │
                   │          +           │  →   │     Red (green)      │  →   │                      │
                   │                      │      │                      │      │                      │
                   └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
                            500ms                         2000ms                        500ms          
                           no resp                      f / j / k                      no resp         
                                                       ← RT onset                                     

                      Window 4: Feedback   
                   ┌──────────────────────┐
                   │                      │
                   │       Correct!       │
                   │                      │
                   └──────────────────────┘
                            1000ms         
                           no resp         
                   Gate 1 ✅ Windows complete, response mapping confirmed

User             ❯ Timeline and keys look good. ITI 400-800ms random.

Amazing PsyCoder ❯ 🟢 Phase 3/5 · Conditions
                   Congruent:incongruent = 60:60 → 120-trial condition table generated
                   Gate 2 ✅ All columns filled

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Blocks
                   2 blocks × 60 trials · Feedback in practice only
                   Gate 3 ✅ Config has zero [MISSING]

Amazing PsyCoder ❯ 🟢 Phase 5/5 · Final Review
                   ┌───────────────────────────────────────────────────────┐
                   │ Design Decision Registry                              │
                   │ Paradigm Stroop · Platform PsychoPy   ← user          │
                   │ Keys f/j/k · 50:50 congruent          ← user          │
                   │ ITI 400-800ms random                  ← user          │
                   │ Trial timeline 4 windows              ← convention    │
                   └───────────────────────────────────────────────────────┘
                   Gate 5 ✅ All confirmed → Route to code generation

User             ❯ Generate.

Amazing PsyCoder ❯ ✅ stroop_task.py + README.md generated
                   Params at top · CJK font configured · Incremental save
                   → Auto-routing to code audit

Amazing PsyCoder ❯ 🔍 Audit passed · Readiness: ready_for_collection
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
amazing-psycoder-skills/
├── amazing-psycoder/                  ← Orchestrator (entry point)
│   ├── SKILL.md
├── PLATFORMS.md                   ← Platform adapter reference
├── install.sh                     ← Cross-platform installer
│   ├── psych-experiment-programming/  ← ① Design layer (5-phase workflow + 38 paradigms)
│   ├── psych-experiment-coder/        ← ② Code generation layer
│   │   ├── psychopy/
│   │   ├── jspsych/
│   │   └── psychtoolbox/
│   └── psych-experiment-code-reviewer/ ← ③ Audit layer (5 modes + smoke testing)
├── docs/                              ← Multi-language READMEs
└── README.md
```

---

<div align="center">

Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
