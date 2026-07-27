<div align="center">

# 🧠 Amazing PsyCoder 💻

> Helping psychology researchers focus more on research questions, not code.

[![Version](https://img.shields.io/badge/version-v1.4.0-2563eb.svg)](../amazing-psycoder/SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Codex](https://img.shields.io/badge/Codex-Skill-green)](https://github.com/openai/codex)
[![Hermes](https://img.shields.io/badge/Hermes-Skill-orange)](https://github.com/NousResearch/hermes-agent)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-red)](https://github.com/openclaw/openclaw)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-standard-333)](https://agentskills.io)
[![Stars](https://img.shields.io/github/stars/soupandpsy/amazing-psycoder-skills?style=social)](https://github.com/soupandpsy/amazing-psycoder-skills)

[**简体中文**](../README.md) · [**繁體中文**](README_ZH-HANT.md) · [**English**](README_EN.md) · [**日本語**](README_JA.md) · [**Deutsch**](README_DE.md) · [**Français**](README_FR.md)

<br>

[📖 Why](#-why) · [👥 Who It's For](#-who-its-for) · [⚡ Install](#-install) · [🚀 Quick Start](#-quick-start) · [🧪 Experiment Programming](#-experiment-programming) · [📊 Data Analysis](#-data-analysis) · [🎬 Demo](#-demo) · [📂 File Structure](#-file-structure)

</div>

<br>


---

## 📖 Why

<h3 align="center">🔍 Common Challenges from Study Design to Data Analysis</h3>

🔬 Turning a research idea into an experiment that can collect data often requires Python, JavaScript, or MATLAB.<br>
📦 Existing laboratory code may stop working when the environment changes, while its dependencies and core logic can be difficult to maintain.<br>
📊 When statistical methods are chosen mainly by convention, it can be difficult to explain how they match the research question, outcome type, and data structure.<br>
🔁 Without recorded software versions and dependencies, an analysis may be difficult to reproduce on another computer.<br>
✂️ When experiment design and analysis planning are disconnected, researchers may discover after data collection that the design cannot support the intended analysis.

<h3 align="center">🧱 Two Main Challenges in Conducting Research</h3>

**First: experiment programming.** Testing a hypothesis requires translating the design into a program. PsychoPy Builder may not be flexible enough for some complex designs; Coder requires Python, jsPsych requires JavaScript and timeline logic, and Psychtoolbox requires MATLAB and knowledge of display synchronization. RT onset, key mapping, and data recovery after interruption all need explicit decisions and careful checks.

**Second: data analysis.** Analysis planning should ideally begin before data collection and be implemented against the observed data structure afterwards. Should a within-subject design use a paired t-test or a mixed model? How should near-ceiling accuracy be modeled? Why is a particular method appropriate? Can the result be reproduced on another computer? These questions depend on the research aim, data hierarchy, and software environment.

These challenges involve not only programming, but also study design, statistical inference, data management, and reproducibility.

<h3 align="center">✨ How Amazing PsyCoder Helps</h3>

You can begin with an experiment idea, an existing design, or current data. Amazing PsyCoder then helps you confirm research rules, generate code, and check for problems step by step. When needed, you still provide configurations, data descriptions, exclusion sources, and execution records. AI output alone is never treated as “ready for data collection” or “ready for publication”: experiments require a target-machine test run, and analyses must actually run with their outputs reviewed.

Amazing PsyCoder contains 7 skills—1 entry skill and 6 specialist skills—and follows the [agentskills.io](https://agentskills.io) open standard. It can be installed in four AI agents: Claude Code, Codex, Hermes, and OpenClaw.

So you can give the time back to the research itself.

---

## 👥 Who It's For

- 🎓 Psychology undergrads and grad students writing (or about to write) experiment code
- 🧠 Researchers running cognitive, behavioral, or social psychology experiments
- 😵‍💫 Researchers who repeatedly encounter RT, randomization, or condition-table problems and want systematic checks for common risks
- 📊 Anyone who's collected data and isn't sure which statistical method to use — and wants a structured analysis plan
- 🐍 PsychoPy · 🌐 jsPsych · 🧮 Psychtoolbox / MATLAB users

---

## ⚡ Install

Use the repository installer. It checks all 7 skills before changing the destination and restores the previous files if an installation fails.

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
```

**Claude Code**

```bash
./install.sh claude
```

Use `/amazing-psycoder` after installation. Default destination: `${CLAUDE_CONFIG_DIR:-~/.claude}/skills`.

**Codex**

```bash
./install.sh codex
```

Use `$amazing-psycoder` after installation. Default destination: `~/.agents/skills`.

**Hermes**

```bash
./install.sh hermes
```

Use `/amazing-psycoder` after installation. Default destination: `~/.hermes/skills`.

**OpenClaw**

```bash
./install.sh openclaw
```

Describe your task after installation and let the OpenClaw agent match the skill. Default destination: `~/.openclaw/skills`.

<details>
<summary><b>Project install, custom directories, and installation checks</b></summary>

<br>

```bash
./install.sh --scope project --project-dir /path/to/repo claude
./install.sh --scope project --project-dir /path/to/repo codex
./install.sh --scope project --project-dir /path/to/workspace openclaw
./install.sh --check codex
```

Hermes currently has no stable project-level skill directory, so its installer supports user scope only. See [`PLATFORMS.md`](../amazing-psycoder/PLATFORMS.md).

</details>

---

## 🚀 Quick Start

After installation, invoke Amazing PsyCoder in the relevant AI agent and describe what you want to do:

> "I want a Stroop task, red/green/blue, key-press response" → auto-enters experiment design

> "Analyze my Stroop data — is there an RT difference between congruent and incongruent?" → auto-enters analysis design

> "Review this experiment code, especially RT onset and data saving" → auto-enters code review

You normally do not need to choose a specialist skill. The entry skill selects design, code generation, or review from the request. If it cannot determine whether you want to build an experiment or analyze data, it asks for clarification.

---

## 🧪 Experiment Programming

From idea to experiment code that is ready for a test run: three steps — design, generate, review.

### Skills

| # | Skill | What It Does | Key Details |
|---|------|--------|---------|
| ① | **Design Orchestration** `psy-exp-designer` | Turns experiment ideas into complete design specifications | 5-phase progressive confirmation. Phase 2 generates trial-window timeline diagrams — per-screen duration, keys, RT onset at a glance. 5 hard gates. 38 paradigm references |
| ② | **Code Generation** `psy-exp-coder` | Generates runnable code from design specs | 4-layer priority architecture. A 10-item quality gate checks timing, response handling, saving, cleanup, dependencies, and other blocking risks before delivery |
| ③ | **Code Review** `psy-exp-reviewer` | Checks code against the confirmed design | Without recorded test runs on the real collection machine, it will not claim the experiment is ready for data collection |

### Platforms

| Platform | Strengths |
|------|------|
| 🐍 **[PsychoPy](https://psychopy.org/)** | Python experiments on lab computers; timing still needs validation on the target machine |
| 🌐 **[jsPsych](https://www.jspsych.org/)** | Browser and online experiments; test on the actual browser and participant devices |
| 🧮 **[Psychtoolbox](https://psychtoolbox.org/)** | MATLAB/Octave experiments with detailed display and device control; synchronization and hardware calibration remain necessary |

### Experiment Design References

**38 experiment-design references**, each organized with unified meta-logic: When to use → Core logic → Must confirm → Don't assume → Trial window timeline → Condition table → Data analysis → Variants & references.

These references help define an experiment. They do **not** mean 38 × 3 generators have already been verified on real machines across all three platforms.

| Category | Paradigms |
|------|------|
| 🎯 **Attention & Inhibitory Control** | Stroop · Eriksen Flanker · Simon · Go/No-go · Stop-signal · ANT · Posner Cuing · Visual Search · Dot-probe · Navon · CPT · Antisaccade |
| 🧠 **Memory & Working Memory** | N-back · Sternberg · Corsi Blocks · Change Detection · Drag and Drop |
| 🔄 **Executive Function & Cognitive Flexibility** | Task Switching · WCST · Choice RT |
| 👥 **Social Cognition & Emotion** | Cyberball · Climate Reflection · Phone a Friend · Rating · Priming · IAT · EAST |
| 💰 **Decision Making & Reward** | BART · Delay Discounting · Rating to Choice · Ultimatum Game |
| 👁️ **Perception & Psychophysics** | Psychophysics Staircase · Multisensory Nature · Mental Rotation |
| 🌱 **Development & Individual Differences** | Children Flanker · Bilingual Stroop · Numerical Stroop · Writing Distraction |

---

## 📊 Data Analysis

Analysis can be planned before data collection and implemented further once data are available: design the analysis plan, generate the code, and review the executed results.

### Skills

| # | Skill | What It Does | Key Details |
|---|------|--------|---------|
| ④ | **Analysis Design** `psy-ana-designer` | Starts from your scientific question, designs a complete analysis plan | 5-phase progressive confirmation. Phase 2 confirms file organization and the participant/stimulus/session hierarchy. Phase 3 compares viable alternatives on the dimensions that matter for this decision; the full 12-dimension matrix is reserved for genuinely competitive or high-impact choices |
| ⑤ | **Analysis Coding** `psy-ana-coder` | Generates reproducible scripts from the analysis plan | Phase 0 validates config → confirms R/Python → 12-step script generation. 10-item quality gate. R: tidyverse/lme4/ggplot2. Python: pandas/statsmodels/seaborn. Fully config-driven |
| ⑥ | **Analysis Audit** `psy-ana-reviewer` | Separates static code review from executed-result review | Static review can reach `ready_for_execution` only. `ready_for_publication` additionally requires a successful clean run plus reviewed logs, tables, figures, dependency record, and environment |

### Analysis Languages and Environments

| Language and environment | Strengths |
|------|------|
| 📊 **[R](https://www.r-project.org/)** | Statistical modeling and academic reporting, with tools such as lme4, ggplot2, Quarto, and R Markdown |
| 🐍 **[Python](https://www.python.org/)** | General data processing, statistical analysis, visualization, and Jupyter workflows |

### Analysis Methods

**60 method references and 48 chart references** help identify candidates; they are not automatic prescriptions. Compare viable choices on the factors that can change the decision. Use the full 12-dimension comparison only when alternatives are genuinely close or the choice has major consequences.

| Category | Method Examples |
|------|------|
| **Mean Comparison** | Paired/independent t-test, within/between/mixed ANOVA, ANCOVA, MANOVA |
| **Mixed Models** | Linear mixed models (LMM), logistic mixed models (GLMM), Gamma GLMM, crossed random effects |
| **Mediation & Moderation** | Mediation analysis, moderation analysis, moderated mediation, structural equation modeling |
| **Regression & Longitudinal** | Multiple regression, quantile regression, growth curves, cross-lagged panel, time series |
| **Correlation & Classification** | Pearson/Spearman correlation, repeated measures correlation, chi-square, canonical correlation |
| **Nonparametric & Robust** | Wilcoxon, Friedman, permutation tests, bootstrap, robust regression |
| **Bayesian** | Bayesian t-test, Bayesian ANOVA, Bayesian mixed models |
| **Measurement & Psychometrics** | Reliability (α/ω/ICC), exploratory/confirmatory factor analysis, multidimensional scaling |
| **Signal Detection & Diagnostics** | d', ROC curves, psychometric functions |
| **RT & Decision Modeling** | Ex-Gaussian distribution, drift diffusion model (DDM) |
| **Meta-analysis & Power** | Meta-analysis, power analysis, equivalence testing |
| **Specialized Methods** | Multiple imputation, LASSO/Ridge, network analysis, cluster analysis, latent class analysis |

---

## 🎬 Demo

### 🧪 Experiment · PsychoPy Stroop

> "I want a Stroop task, red/green/blue text, key-press to judge ink color, 50:50 congruent:incongruent, 2 blocks of 60 trials each"

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
                   │          +           │  →   │     Red "green"      │  →   │                      │
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
                   Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Blocks
                   2 blocks × 60 trials · Feedback in practice block only
                   Gate 3 ✅

Amazing PsyCoder ❯ 🟢 Phase 5/5 · Final Review
                   ┌──────────────────────────────────────────────┐
                   │ Design Decision Registry                     │
                   │ Paradigm Stroop · Platform PsychoPy  ← user  │
                   │ Keys f/j/k · Congruent:Incongruent 50:50 ← user│
                   │ ITI 400-800ms random               ← user    │
                   │ Trial timeline 4 windows           ← convention│
                   └──────────────────────────────────────────────┘
                   Gate 5 ✅ All confirmed → Route to code generation

User             ❯ Generate.

Amazing PsyCoder ❯ ✅ stroop_task.py + README.md generated
                   Params at top · CJK font configured · Incremental save
                   → Auto-routing to audit

Amazing PsyCoder ❯ 🔍 Static code review found no blocking issue.
                   The experiment is ready for a test run, not yet for data collection.
                   Run startup/exit, short-session, data-integrity, and interruption-
                   recovery checks on the real collection machine.

User             ❯ Those checks passed on the collection machine. Here are the logs and data files.

Amazing PsyCoder ❯ 🔍 Runtime evidence and saved data reviewed.
                   Readiness: ready_for_collection
                   Data collection can begin.
```

### 📊 Analysis · R Stroop

> "Analyze my Stroop data — is there a significant RT difference between congruent and incongruent conditions?"

```
User             ❯ Analyze my Stroop data — RT difference congruent vs incongruent?

Amazing PsyCoder ❯ 🟢 Phase 1/5 · Understand experiment & scientific question
                   Please provide experiment config or describe the design

User             ❯ Within-subject, IV: condition (congruent/incongruent), DV: rt+acc. 30 subjects

Amazing PsyCoder ❯ 🟢 Phase 2/5 · Understand data structure
                   How is your data stored? One file per subject or combined?

User             ❯ One CSV per subject, named sub-001_stroop.csv
                   Columns: subject_id, stimulus, condition, rt, acc, trial

Amazing PsyCoder ❯ Are the stimuli unique to each subject, or does the same set
                   appear for multiple subjects?

User             ❯ All subjects see the same 60 color-word combinations, with
                   repeated trials within each subject.

Amazing PsyCoder ❯ Confirmed: observations repeat within both subject and stimulus.
                   Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 3/5 · Define the estimand, then choose the method
                   Primary estimand: the population-average RT contrast,
                   incongruent minus congruent.

                   Proposed RT model:
                   rt ~ condition + (1 + condition | subject_id) + (1 | stimulus)

                   Accuracy can be a supplementary binomial mixed model.
                   A paired t-test is a simpler alternative, but it answers the
                   question at an aggregated subject-mean level.
                   If the random-effects structure cannot be estimated reliably,
                   follow a predeclared simplification order and report diagnostics.

User             ❯ Confirm the estimand, formula, and subject/stimulus hierarchy.
                   Use the mixed model for RT and accuracy as supplementary.

Amazing PsyCoder ❯ Gate 3 ✅ Estimand, formula, hierarchy, and alternatives confirmed

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Cleaning rules, runtime, and outputs
                   Please provide RT, missing-data, and participant-exclusion rules
                   from the task protocol or preregistration. No fixed threshold or
                   SD rule will be inserted without a source and confirmation.

User             ❯ The preregistration says: the primary RT analysis uses correct
                   trials with non-missing RT only; no fixed RT bounds, SD trimming,
                   or automatic participant exclusion. Add a log-RT sensitivity
                   analysis. The lab uses R 4.4.1, renv.lock, and R Markdown.

Amazing PsyCoder ❯ 🟢 Phase 5/5 · Final Review
                   ┌──────────────────────────────────────────────┐
                   │ Analysis Decision Registry                   │
                   │ Question: congruent vs incongruent RT ← user │
                   │ Formula: subject slope + stimulus intercept   │
                   │ Cleaning: preregistered rules + audit log     │
                   │ Runtime: R 4.4.1 + renv.lock          ← user  │
                   │ Outputs: contrast, interval, diagnostics, plots│
                   └──────────────────────────────────────────────┘
                   Gate 5 ✅ Save analysis_config.yaml → Route to code gen

User             ❯ Generate.

Amazing PsyCoder ❯ ✅ analysis.R + report.Rmd + renv.lock generated
                   Dependency versions recorded · static review completed

Amazing PsyCoder ❯ 🔍 Readiness: ready_for_execution
                   The code is ready to run, but the results are not yet ready to report.

User             ❯ It ran in a clean environment. Here are the log, tables, plots, and versions.

Amazing PsyCoder ❯ 🔍 Execution outputs reviewed.
                   Readiness: ready_for_publication
```

---

## 📂 File Structure

```text
amazing-psycoder-skills/
├── amazing-psycoder/                  ← Main entry point (v1.4.0)
│   ├── SKILL.md                       ← Routing and global rules
│   ├── PLATFORMS.md · install.sh      ← Platform notes and installer
│   ├── STANDALONE.md                  ← Direct use inside an agent
│   ├── PSYCODER_STUDIO.md             ← Website integration
│   ├── runtime/                       ← Website contracts and capability scope
│   ├── scripts/ · tests/              ← Automated checks
│   ├── requirements-dev.txt           ← Pinned validation dependencies
│   │
│   │   # 🧪 Experiment Programming
│   ├── psy-exp-designer/              ← ① Experiment design (5 phases + 38 design references)
│   ├── psy-exp-coder/                 ← ② Experiment code generation (PsychoPy/jsPsych/Psychtoolbox)
│   └── psy-exp-reviewer/              ← ③ Experiment code review
│   │
│   │   # 📊 Data Analysis
│   ├── psy-ana-designer/              ← ④ Analysis design (60 method + 48 chart references)
│   ├── psy-ana-coder/                 ← ⑤ Analysis code generation (R/Python)
│   └── psy-ana-reviewer/              ← ⑥ Analysis code and output review
│
├── docs/                              ← Translated READMEs (TW/EN/JP/DE/FR)
├── .github/                           ← Automated checks
└── README.md                          ← Simplified Chinese project page
```

---

<div align="center">

💡 Have ideas or suggestions? Reach out at [tangdingyi04@outlook.com](mailto:tangdingyi04@outlook.com)<br>
🪄 Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
