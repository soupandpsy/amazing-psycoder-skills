<div align="center">

# 🧠 Amazing PsyCoder 💻

> Making the coding barrier in psychology research disappear completely.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
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

<table>
<tr><td align="center">

🔬 &nbsp;An idea won't become a data-collection-ready experiment until you learn Python, JavaScript, or MATLAB first.<br>
📦 &nbsp;The lab's legacy code crashes on a different machine — nobody can explain the dependencies, nobody dares touch the logic.<br>
📊 &nbsp;Statistical methods chosen by habit — "everyone uses ANOVA" — until a reviewer's question sends you back to square one.<br>
🔁 &nbsp;Results only reproducible on your machine; change the environment or random seed and the conclusions might flip.<br>
✂️ &nbsp;Experiment builders and data analysts are often different people — you collect data only to realize the design never accounted for how it'd be analyzed.<br>
📝 &nbsp;A journal asks for a reproducibility statement, but the code was never audited, never documented, never independently verified.

</td></tr>
</table>

<div align="center">

### ✨ Amazing PsyCoder solves exactly these.

You don't need to know Python. You don't need to know statistics. You just need to bring your ideas and your data — it walks you through confirming the design step by step, generates the code, and audits the result. What you get runs right out of the box, and the analysis holds up to reviewer scrutiny.

</div>

---

## 📖 Why

For a psychology researcher, two things eat up the most time between having an idea and actually collecting data and getting results.

**First: experiment programming.** To test a hypothesis, you first have to code the experiment. PsychoPy's Builder isn't flexible enough; Coder means learning Python. jsPsych means learning JavaScript and timeline logic. Psychtoolbox means learning MATLAB and frame synchronization. Just figuring out "which screen does RT start from," "how do I not map the keys backwards," and "how do I save data so a crash doesn't wipe everything" can take weeks. The distance between an idea in your head and a working experiment often takes longer than designing the experiment itself.

**Second: data analysis.** Data's collected — now what statistical method? Within-subject design: paired t-test or mixed model? Accuracy near ceiling — is ANOVA still valid? When a reviewer asks "why this method," what do you say? If someone runs your code on a different machine, will they get the same result?

These aren't skill problems. They're tool problems. Writing code and running analyses should make research smoother, not be the thing that stalls you.

Amazing PsyCoder encodes hard-won experience in experiment programming and data analysis into 7 skills — 1 orchestrator plus 6 sub-skills, following the agentskills.io open standard, supporting Claude Code / Codex / Hermes / OpenClaw.

So you can give the time back to the research itself.

---

## 👥 Who It's For

- 🎓 Psychology undergrads and grad students writing (or about to write) experiment code
- 🧠 Researchers running cognitive, behavioral, or social psychology experiments
- 😵‍💫 Anyone who's tripped over RT timing, randomization, and condition tables one too many times — and wants systematic quality assurance
- 📊 Anyone who's collected data and isn't sure which statistical method to use — and wants a structured analysis plan
- 📝 Anyone preparing a manuscript and wanting an independent reproducibility audit before submission
- 🐍 PsychoPy · 🌐 jsPsych · 🧮 Psychtoolbox / MATLAB users

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
<summary><b>Terminal install (all platforms)</b></summary>

<br>

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
./install.sh           # auto-detects platform and installs
# or specify: ./install.sh claude | codex | hermes | openclaw
```

</details>

---

## 🚀 Quick Start

After installation, type `/amazing-psycoder` and describe what you want to do:

> "I want a Stroop task, red/green/blue, key-press response" → auto-enters experiment design

> "Analyze my Stroop data — is there an RT difference between congruent and incongruent?" → auto-enters analysis design

No need to specify which skill to use — the orchestrator automatically determines it based on your needs. From there, the skill guides you step by step: confirm the design, choose methods, generate code, audit checks. You just answer its questions.

---

## 🧪 Experiment Programming

From idea to data-collection-ready experiment code: three steps — design, generate, audit.

### Skills

| # | Skill | What It Does | Key Details |
|---|------|--------|---------|
| ① | **Design Orchestration** `psy-exp-designer` | Turns experiment ideas into complete design specifications | 5-phase progressive confirmation. Phase 2 generates trial-window timeline diagrams — per-screen duration, keys, RT onset at a glance. 5 hard gates. 38 paradigm references |
| ② | **Code Generation** `psy-exp-coder` | Generates runnable code from design specs | 4-layer priority architecture. 9-item quality gate auto-blocks: `time.sleep()`, `KbCheck` for RT rejected on sight. 12-step code template, parameters at the top |
| ③ | **Code Audit** `psy-exp-reviewer` | The last checkpoint before data collection | 5 review modes. Smoke test protocol. Paradigm failure-mode checks. Failures get a fix path. Readiness label: `ready_for_collection` |

### Platforms

| Platform | Strengths |
|------|------|
| 🐍 **[PsychoPy](https://psychopy.org/)** | Python ecosystem, USB HID hardware timestamps, millisecond RT precision. Go-to for local-lab experiments |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | JavaScript ecosystem, runs in the browser, zero install. Go-to for online experiments |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | MATLAB ecosystem, GPU-level frame-precise control. Go-to when timing precision is everything |

### Paradigm Coverage

**38 paradigms**, each organized with unified meta-logic: When to use → Core logic → Must confirm → Don't assume → Trial window timeline → Condition table → Data analysis → Variants & references.

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

Once data is collected: three steps — design the analysis plan, generate the code, audit for reproducibility.

### Skills

| # | Skill | What It Does | Key Details |
|---|------|--------|---------|
| ④ | **Analysis Design** `psy-ana-designer` | Starts from your scientific question, designs a complete analysis plan | 5-phase progressive confirmation. Phase 2 confirms data file organization (multi-file/single-file, naming, CSV/Excel/TSV). Phase 3 uses 12-dimension comparison to pick the best method. Config YAML as single source of truth |
| ⑤ | **Analysis Coding** `psy-ana-coder` | Generates reproducible scripts from the analysis plan | Phase 0 validates config → confirms R/Python → 12-step script generation. 10-item quality gate. R: tidyverse/lme4/ggplot2. Python: pandas/statsmodels/seaborn. Fully config-driven |
| ⑥ | **Analysis Audit** `psy-ana-reviewer` | The last checkpoint before publication | 4 review modes. Intake protocol auto-detection. Statistical correctness + reproducibility + assumption checks. R/Python dual-platform anti-pattern detection. Failures get a fix path. Readiness label: `ready_for_publication` |

### Platforms

| Platform | Strengths |
|------|------|
| 📊 **[R](https://www.r-project.org/)** | The statistical computing standard. tidyverse + lme4 + ggplot2 + RMarkdown. Academic publishing's first choice |
| 🐍 **[Python](https://www.python.org/)** | General-purpose scientific computing. pandas + statsmodels + seaborn + Jupyter. Reproducible analysis |

### Analysis Methods

**60 analysis methods, 48 chart types**. Every method choice goes through 12-dimension comparison: statistical power · false positive control · data utilization · outlier sensitivity · assumption robustness · interpretability · domain acceptance · effect size comparability · reproducibility · extensibility · sample size constraints · computational feasibility.

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

Amazing PsyCoder ❯ 🔍 Audit passed · Readiness: ready_for_collection
                   Safe to start data collection.
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
                   Columns: subject_id, condition, rt, acc, trial

Amazing PsyCoder ❯ Confirmed: 30 subjects × 1 file each. Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 3/5 · Data characteristics + match methods (core phase)
                   Is RT right-skewed? Accuracy near ceiling?

User             ❯ RT somewhat right-skewed, accuracy around 95%

Amazing PsyCoder ❯ Accuracy near ceiling → glmer(binomial) for acc analysis
                   For RT, 12-dimension comparison A vs B:

                   ┌────────────┬─────────────────┬─────────────────┐
                   │ Dimension  │ A: Paired t-test │ B: Linear Mixed  │
                   ├────────────┼─────────────────┼─────────────────┤
                   │ Power      │ 30 pts (subj avg)│ 1800 pts (all)  │
                   │ Data use   │ 1 pt per subject │ All trials used │
                   │ Extensible │ Covariate = redo │ Add + to formula│
                   │ Intuitive  │ d=0.5 universal  │ Random effects  │
                   └────────────┴─────────────────┴─────────────────┘

                   Prioritize power + extensibility → choose B. Simplicity → choose A.

User             ❯ Choose B

Amazing PsyCoder ❯ Gate 3 ✅ Method selected (with 12-dimension rationale)

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Analysis details
                   Cleaning: RT 150-2000ms · correct trials only · exclude subj acc<60%
                   · ±2.5 SD trial exclusion · Plots: raincloud + individual lines ⚠️

User             ❯ Confirm

Amazing PsyCoder ❯ 🟢 Phase 5/5 · Final Review
                   ┌──────────────────────────────────────────────┐
                   │ Analysis Decision Registry                   │
                   │ Question: congruent vs incongruent RT ← user │
                   │ Method: lmer (user chose B)         ← user   │
                   │ RT 150-2000ms · subj acc<60%        ← default⚠️│
                   │ Plots: raincloud + indiv lines      ← default⚠️│
                   └──────────────────────────────────────────────┘
                   Gate 5 ✅ Save analysis_config.yaml → Route to code gen

User             ❯ Generate.

Amazing PsyCoder ❯ ✅ analysis.R + report.Rmd generated
                   Config-driven · 10 quality gates · 12-step script structure
                   → Auto-routing to audit

Amazing PsyCoder ❯ 🔍 Audit passed · Readiness: ready_for_publication
```

---

## 📂 File Structure

```
amazing-psycoder-skills/
├── amazing-psycoder/                  ← Orchestrator (system entry point, v1.3)
│   ├── SKILL.md · PLATFORMS.md · install.sh
│   │
│   │   # 🧪 Experiment Programming
│   ├── psy-exp-designer/              ← ① Experiment design (5 phases + 38 paradigms + 9 reference files)
│   ├── psy-exp-coder/                 ← ② Experiment code generation (PsychoPy/jsPsych/Psychtoolbox)
│   └── psy-exp-reviewer/              ← ③ Experiment audit (5 modes + smoke test + recovery loop)
│   │
│   │   # 📊 Data Analysis
│   ├── psy-ana-designer/              ← ④ Analysis design (5 phases + 60 methods + 48 charts)
│   ├── psy-ana-coder/                 ← ⑤ Analysis code generation (R/Python dual-platform)
│   └── psy-ana-reviewer/              ← ⑥ Analysis audit (4 modes + intake protocol + recovery loop)
│
├── docs/                              ← Multi-language READMEs (CN/TW/EN/JP/DE/FR)
└── README.md
```

---

<div align="center">

💡 Have ideas or suggestions? Reach out at [tangdingyi04@outlook.com](mailto:tangdingyi04@outlook.com)<br>
🪄 Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
