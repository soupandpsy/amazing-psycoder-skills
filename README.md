<div align="center">

# 🧠 Amazing PsyCoder 💻

> 让心理学研究者更专注于研究问题，而不是代码。

[![Version](https://img.shields.io/badge/version-v1.4.0-2563eb.svg)](amazing-psycoder/SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Codex](https://img.shields.io/badge/Codex-Skill-green)](https://github.com/openai/codex)
[![Hermes](https://img.shields.io/badge/Hermes-Skill-orange)](https://github.com/NousResearch/hermes-agent)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-red)](https://github.com/openclaw/openclaw)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-standard-333)](https://agentskills.io)
[![Stars](https://img.shields.io/github/stars/soupandpsy/amazing-psycoder-skills?style=social)](https://github.com/soupandpsy/amazing-psycoder-skills)

[**简体中文**](README.md) · [**繁體中文**](docs/README_ZH-HANT.md) · [**English**](docs/README_EN.md) · [**日本語**](docs/README_JA.md) · [**Deutsch**](docs/README_DE.md) · [**Français**](docs/README_FR.md)

<br>

[📖 为什么](#-为什么做这个项目) · [👥 适合谁](#-适合这些人) · [⚡ 安装](#-安装) · [🚀 快速开始](#-快速开始) · [🧪 实验编程](#-实验编程) · [📊 数据分析](#-数据分析) · [📂 文件结构](#-文件结构)

</div>

<br>

## 📖 为什么做这个项目

<h3 align="center">🔍 心理学研究从设计到分析的常见困难</h3>

🔬 研究想法要转化为可用于收集数据的实验程序，研究者往往还需要掌握 Python、JavaScript 或 MATLAB。<br>
📦 实验室已有代码可能因运行环境变化而无法使用，依赖关系和核心逻辑也常常难以维护。<br>
📊 如果统计方法主要依照惯例选择，研究者可能难以说明方法与研究问题、变量类型和数据结构之间的关系。<br>
🔁 如果没有记录软件版本和依赖环境，分析结果可能难以在其他电脑上复现。<br>
✂️ 如果实验设计与分析计划彼此脱节，可能在数据收集后才发现现有设计无法支持原定分析。

<h3 align="center">🧱 研究进行中的两类主要困难</h3>

**第一类：实验编程。** 为了检验一个假设，需要把实验设计转化为程序。PsychoPy Builder 在部分复杂设计中可能不够灵活，使用 Coder 需要 Python；jsPsych 需要 JavaScript 和时间线逻辑；Psychtoolbox 需要 MATLAB 和显示同步知识。反应时从哪个画面开始计算、按键如何映射、程序中断后怎样保留数据，都需要明确设计并逐项检查。

**第二类：数据分析。** 分析方案最好在数据收集前就开始规划，并在获得数据后根据实际结构落实。被试内设计应使用配对 t 检验还是混合模型？正确率接近上限时应如何建模？为什么选择这个方法？换一台电脑后能否复现相同结果？这些问题需要结合研究目标、数据层级和软件环境回答。

这些困难不仅涉及编程，也涉及实验设计、统计推断、数据管理和研究复现。

<h3 align="center">✨ Amazing PsyCoder 如何提供帮助</h3>

你可以先描述实验想法、已有设计或现有数据。Amazing PsyCoder 会逐步协助你确认研究规则、生成代码并检查问题；在需要时，你仍需提供配置、数据说明、排除依据和运行记录。系统不会仅凭 AI 输出就宣称“可以收数据”或“可以发表”：实验仍要在正式电脑上试跑，分析也必须真正运行并检查结果。

Amazing PsyCoder 由 7 个 Skill 组成——1 个总入口加 6 个专业 Skill。它遵循 [agentskills.io](https://agentskills.io) 开放标准，可安装到 Claude Code、Codex、Hermes 和 OpenClaw 这四个 AI Agent 中。

**把时间还给研究本身。**

---

## 👥 适合这些人

- 🎓 正在或准备写实验代码的心理学本科生、研究生
- 🧠 做认知、行为、社会心理实验的研究者
- 😵‍💫 经常遇到反应时、随机化或条件表问题，希望系统化检查常见风险
- 📊 收完数据不确定该用什么统计方法，希望有系统化分析方案
- 🐍 PsychoPy · 🌐 jsPsych · 🧮 Psychtoolbox / MATLAB 用户

如果只是问一个 API、改一行普通代码或了解一个统计概念，直接提问即可，不需要启动完整流程。

---

## ⚡ 安装

推荐使用仓库自带的安装脚本。它会先检查全部 7 个 Skill；如果中途失败，会恢复原来的文件。

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
```

**Claude Code**

```bash
./install.sh claude
```

安装后使用 `/amazing-psycoder`。默认安装到 `${CLAUDE_CONFIG_DIR:-~/.claude}/skills`。

**Codex**

```bash
./install.sh codex
```

安装后使用 `$amazing-psycoder`。默认安装到 `~/.agents/skills`。

**Hermes**

```bash
./install.sh hermes
```

安装后使用 `/amazing-psycoder`。默认安装到 `~/.hermes/skills`。

**OpenClaw**

```bash
./install.sh openclaw
```

安装后直接描述任务，由 OpenClaw Agent 匹配 Skill。默认安装到 `~/.openclaw/skills`。

<details>
<summary><b>项目级安装、自定义目录和安装检查</b></summary>

<br>

```bash
./install.sh --scope project --project-dir /path/to/repo claude
./install.sh --scope project --project-dir /path/to/repo codex
./install.sh --scope project --project-dir /path/to/workspace openclaw
./install.sh --check codex
```

Hermes 当前没有稳定的项目级目录，因此只提供用户级安装。更多说明见
[`PLATFORMS.md`](amazing-psycoder/PLATFORMS.md)。

</details>

---

## 🚀 快速开始

安装后，在对应的 AI Agent 中调用 Amazing PsyCoder，并直接描述你想做什么：

> “我要做一个 Stroop 任务，红绿蓝三色，按键判断墨色” → 自动进入实验设计

> “帮我分析 Stroop 数据，一致和不一致条件的反应时有没有差异” → 自动进入分析设计

> “帮我检查这份实验代码，重点看反应时起点和数据保存” → 自动进入代码检查

通常不需要指定应该使用哪个专业 Skill。总入口会根据任务内容选择设计、代码生成或代码检查；如果请求不足以判断是在设计实验还是分析数据，它会先向你确认。

下面是实验编程和数据分析的详细介绍，每个部分末尾都有完整的交互 Demo。

---

## 🧪 实验编程

从想法到可以开始试跑的实验代码，分三步——设计、生成、检查。

### 技能

| # | 技能 | 功能 |
|---|---|---|
| ① | **设计编排** `psy-exp-designer` | 把实验想法变成完整说明，逐步确认画面、按键、条件、顺序和保存内容 |
| ② | **代码生成** `psy-exp-coder` | 根据已确认设计生成平台代码，并拦截阻塞等待、只在结尾保存等常见问题 |
| ③ | **代码检查** `psy-exp-reviewer` | 检查代码与设计是否一致；没有正式电脑试跑记录时，不会说“可以收数据” |

### 平台

| 平台 | 适合什么 |
|---|---|
| 🐍 **[PsychoPy](https://psychopy.org/)** | 在实验室电脑上运行的 Python 实验；实际计时仍需在目标设备验证 |
| 🌐 **[jsPsych](https://www.jspsych.org/)** | 浏览器或在线实验；需要在实际浏览器和设备上测试 |
| 🧮 **[Psychtoolbox](https://psychtoolbox.org/)** | MATLAB/Octave 实验；适合精细控制显示和设备，但必须做同步与硬件校准 |

### 实验设计参考

**38 个实验设计参考**，每个按统一思路整理：何时使用 → 核心逻辑 → 必须确认 → 不要假设 → 试次画面顺序 → 条件表 → 数据分析 → 变体与参考。

这里的 38 个参考用于帮助你把实验想清楚，**不等于 38 × 3 个已经在三种平台实机验证过的生成器**。

| 类别 | 范式 |
|---|---|
| 🎯 **注意与抑制控制** | Stroop · Eriksen Flanker · Simon · Go/No-go · Stop-signal · ANT · Posner Cuing · Visual Search · Dot-probe · Navon · CPT · Antisaccade |
| 🧠 **记忆与工作记忆** | N-back · Sternberg · Corsi Blocks · Change Detection · Drag and Drop |
| 🔄 **执行功能与认知灵活性** | Task Switching · WCST · Choice RT |
| 👥 **社会认知与情绪** | Cyberball · Climate Reflection · Phone a Friend · Rating · Priming · IAT · EAST |
| 💰 **决策与奖励** | BART · Delay Discounting · Rating to Choice · Ultimatum Game |
| 👁️ **感知与心理物理** | Psychophysics Staircase · Multisensory Nature · Mental Rotation |
| 🌱 **发展与个体差异** | Children Flanker · Bilingual Stroop · Numerical Stroop · Writing Distraction |

### 🎬 Demo：做一个 Stroop 实验

> “我要做一个 Stroop，红绿蓝三色文字，按键判断墨色，50:50 一致不一致，2 个正式 block，每个 60 试次”

```text
用户             ❯ 我要做一个 Stroop 任务

Amazing PsyCoder ❯ 🟢 第 1/5 阶段 · 了解需求
                   确认使用 PsychoPy？

用户             ❯ 对，PsychoPy。

Amazing PsyCoder ❯ 🟢 第 2/5 阶段 · 试次画面和反应规则
                   墨色红绿蓝 → f=红 j=绿 k=蓝。试次顺序：

                       画面 1: 注视点             画面 2: 刺激呈现            画面 3: 空屏等待
                   ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
                   │                      │      │                      │      │                      │
                   │          +           │  →   │       红色“绿”       │  →   │                      │
                   │                      │      │                      │      │                      │
                   └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
                            500ms                         最长 2000ms                    400–800ms
                            不接收反应                    f / j / k                       不接收反应
                                                        ← 反应时起点

                       画面 4: 练习反馈
                   ┌──────────────────────┐
                   │        正确！         │   仅练习阶段出现
                   └──────────────────────┘
                            1000ms

                   ✅ 画面顺序和按键已确认

用户             ❯ 时间线和按键没问题。空屏 400–800ms 随机。

Amazing PsyCoder ❯ 🟢 第 3/5 阶段 · 条件表
                   一致:不一致 = 60:60，共 120 个正式试次。✅

Amazing PsyCoder ❯ 🟢 第 4/5 阶段 · Block 结构
                   练习阶段有反馈；2 个正式 block × 60 试次，不提供反馈。✅

Amazing PsyCoder ❯ 🟢 第 5/5 阶段 · 最终确认
                   ┌──────────────────────────────────────────────┐
                   │ 已确认内容                                   │
                   │ 平台 PsychoPy                  ← 用户确认    │
                   │ 按键 f/j/k · 一致:不一致 50:50 ← 用户确认    │
                   │ 空屏 400–800ms 随机            ← 用户确认    │
                   │ 试次顺序和练习反馈              ← 用户确认    │
                   └──────────────────────────────────────────────┘
                   ✅ 可以生成代码

用户             ❯ 生成。

Amazing PsyCoder ❯ ✅ stroop_task.py + README.md 已生成
                   参数集中设置 · 中文字体方案 · 每试次及时保存

Amazing PsyCoder ❯ 🔍 代码检查没有发现必须修的问题
                   现在可以在正式电脑上试跑，但还不能直接开始收数据。
                   请完成：启动退出、短程完整运行、数据完整性和中断恢复检查。

用户             ❯ 已在正式采集电脑完成并保存这些检查记录，全部通过。

Amazing PsyCoder ❯ 🔍 已检查试跑记录和数据文件
                   当前状态：ready_for_collection
                   可以开始正式采集。
```

---

## 📊 数据分析

分析方案既可以在数据收集前规划，也可以在获得数据后进一步落实，分三步——设计分析方案、生成代码、检查运行结果。

### 技能

| # | 技能 | 功能 |
|---|---|---|
| ④ | **分析设计** `psy-ana-designer` | 先明确真正要回答的问题，再结合数据结构选择方法并记录备选方案 |
| ⑤ | **分析代码** `psy-ana-coder` | 生成 R/Python 脚本、报告和软件版本记录 |
| ⑥ | **分析检查** `psy-ana-reviewer` | 区分“代码看起来没问题”和“结果已经实际运行并检查过” |

### 分析语言与环境

| 语言与环境 | 适合什么 |
|---|---|
| 📊 **[R](https://www.r-project.org/)** | 统计建模和学术报告，可按需要使用 lme4、ggplot2、Quarto/R Markdown 等 |
| 🐍 **[Python](https://www.python.org/)** | 通用数据处理、统计分析、可视化和 Jupyter 工作流 |

### 分析方法

**60 个方法参考、48 个图表参考**用于寻找候选方案，不是自动处方。选择方法时先看研究问题、结果变量是什么类型，以及同一被试、刺激或会话中的数据是否彼此相关。

| 类别 | 方法举例 |
|---|---|
| **均值比较** | 配对/独立 t 检验、被试内/间 ANOVA、混合 ANOVA、ANCOVA、MANOVA |
| **混合模型** | 线性混合模型（LMM）、逻辑混合模型（GLMM）、Gamma GLMM、交叉随机效应 |
| **中介调节** | 中介分析、调节分析、有调节的中介、结构方程模型 |
| **回归与纵向** | 多元回归、分位数回归、增长曲线、交叉滞后面板、时间序列 |
| **相关与分类** | Pearson/Spearman 相关、重复测量相关、卡方检验、典型相关 |
| **非参数与稳健方法** | Wilcoxon、Friedman、置换检验、Bootstrap、稳健回归 |
| **贝叶斯** | 贝叶斯 t 检验、贝叶斯 ANOVA、贝叶斯混合模型 |
| **测量与量表** | 信度分析（α/ω/ICC）、探索性/验证性因子分析、多维标度法 |
| **信号检测与诊断** | d'、ROC 曲线、心理测量函数 |
| **反应时与决策建模** | Ex-Gaussian 分布、漂移扩散模型（DDM） |
| **元分析与效力** | 元分析、效力分析、等效性检验 |
| **专项方法** | 多重插补、LASSO/Ridge、网络分析、聚类分析、潜在类别分析 |

### 🎬 Demo：分析一组 Stroop 数据

> “帮我分析 Stroop 数据，一致和不一致条件的反应时有没有差异”

```text
用户             ❯ 帮我分析 Stroop 数据，一致和不一致反应时有没有差异

Amazing PsyCoder ❯ 🟢 第 1/5 阶段 · 了解实验和研究问题
                   请提供实验配置，或者描述实验设计。

用户             ❯ 被试内设计。条件是一致/不一致，结果是反应时和正确率，共 30 个被试。

Amazing PsyCoder ❯ 🟢 第 2/5 阶段 · 了解数据
                   数据怎么存？每个被试一个文件，还是已经合并？

用户             ❯ 每个被试一个 CSV。
                   列是 subject_id, stimulus, condition, rt, acc, trial。

Amazing PsyCoder ❯ 这些 stimulus 是每个被试各自不同，还是同一组刺激会被多人看到？

用户             ❯ 同一组 60 个颜色词组合会被所有被试看到，每个被试都有重复试次。

Amazing PsyCoder ❯ ✅ 已确认：30 个被试，每人一个文件，每行一个试次；
                   数据同时按被试和刺激重复。

Amazing PsyCoder ❯ 🟢 第 3/5 阶段 · 明确要估计什么，再选择方法
                   主要问题定义为：总体上，不一致条件相对一致条件的平均 RT 差异。
                   因为同一被试有很多试次，同一刺激也会被多人看到，
                   不能把所有行当成互不相关。

                   建议：
                   · RT 主分析：
                     rt ~ condition + (1 + condition | subject_id) + (1 | stimulus)
                   · 正确率补充分析：用二项分布混合模型，同时考虑被试和刺激；
                   · 配对 t 检验可作为更简单的备选方案，但它回答的是按被试汇总后的问题。
                   如果随机效应结构无法稳定估计，会记录诊断并按预先写明的顺序简化，
                   不会看到结果后临时换模型。

用户             ❯ 确认这个问题、公式和数据层级。RT 用线性混合模型，
                   正确率作为补充分析。

Amazing PsyCoder ❯ ✅ 方法、公式和数据层级已确认。

Amazing PsyCoder ❯ 🟢 第 4/5 阶段 · 清理规则、运行环境和输出
                   请提供任务说明或预注册中的反应时、缺失和被试排除规则。
                   如果没有依据，不自动套用“150–2000ms”或“±2.5 SD”。
                   每一步会记录删掉多少行，并保留原始数据。

用户             ❯ 预注册规定：RT 主分析只用正确且 RT 非缺失的试次；
                   不做固定 RT 上下限或 ±SD 剔除，也不自动排除被试；
                   另做 log-RT 敏感性分析。实验室环境是 R 4.4.1，
                   依赖用 renv.lock 固定，报告用 R Markdown。

Amazing PsyCoder ❯ 🟢 第 5/5 阶段 · 最终确认
                   ┌──────────────────────────────────────────────┐
                   │ 已确认内容                                   │
                   │ 问题：一致 vs 不一致反应时       ← 用户确认  │
                   │ 公式：被试随机斜率 + 刺激随机截距 ← 用户确认  │
                   │ 清理：按预注册规则并记录每步数量  ← 用户确认  │
                   │ 环境：R 4.4.1 + renv.lock         ← 用户确认  │
                   │ 输出：条件差、区间、诊断和图表    ← 用户确认  │
                   └──────────────────────────────────────────────┘
                   ✅ 保存 analysis_config.yaml，可以生成代码

用户             ❯ 生成。

Amazing PsyCoder ❯ ✅ analysis.R + report.Rmd + renv.lock 已生成
                   已记录软件版本并完成代码检查。

Amazing PsyCoder ❯ 🔍 当前状态：ready_for_execution
                   可以运行，但还不能说结果已经适合写入论文。

用户             ❯ 已在新环境运行，提供运行记录、结果表、图和软件版本。

Amazing PsyCoder ❯ 🔍 已检查运行结果
                   当前状态：ready_for_publication
                   可以进入报告和论文写作阶段。
```

---

## 📂 文件结构

```text
amazing-psycoder-skills/
├── amazing-psycoder/                  ← 总入口（v1.4.0）
│   ├── SKILL.md                       ← 任务分流和全局规则
│   ├── PLATFORMS.md · install.sh      ← 平台说明和安装器
│   ├── STANDALONE.md                  ← 在 Agent 中直接使用
│   ├── PSYCODER_STUDIO.md             ← 网站接入说明
│   ├── runtime/                       ← 网站使用的数据格式和能力范围
│   ├── scripts/ · tests/              ← 自动检查
│   ├── requirements-dev.txt           ← 完整检查所需的软件版本
│   │
│   │   # 🧪 实验编程
│   ├── psy-exp-designer/              ← ① 实验设计（5 阶段 + 38 个设计参考）
│   ├── psy-exp-coder/                 ← ② 实验代码生成（PsychoPy/jsPsych/Psychtoolbox）
│   └── psy-exp-reviewer/              ← ③ 实验代码检查
│   │
│   │   # 📊 数据分析
│   ├── psy-ana-designer/              ← ④ 分析设计（60 个方法参考 + 48 个图表参考）
│   ├── psy-ana-coder/                 ← ⑤ 分析代码生成（R/Python）
│   └── psy-ana-reviewer/              ← ⑥ 分析代码与结果检查
│
├── docs/                              ← 多语言 README（繁/英/日/德/法）
├── .github/                           ← 自动测试
└── README.md                          ← 简体中文项目首页
```

---

<div align="center">

💡 有想法或建议？欢迎来信 [tangdingyi04@outlook.com](mailto:tangdingyi04@outlook.com)<br>
🪄 Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
