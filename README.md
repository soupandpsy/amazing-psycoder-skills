<div align="center">

# 🧠 Amazing PsyCoder 💻

> 让心理学研究的代码门槛彻底消失。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Codex](https://img.shields.io/badge/Codex-Skill-green)](https://github.com/openai/codex)
[![Hermes](https://img.shields.io/badge/Hermes-Skill-orange)](https://github.com/NousResearch/hermes-agent)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-red)](https://github.com/openclaw/openclaw)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-standard-333)](https://agentskills.io)
[![Stars](https://img.shields.io/github/stars/soupandpsy/amazing-psycoder-skills?style=social)](https://github.com/soupandpsy/amazing-psycoder-skills)

[**简体中文**](README.md) · [**繁體中文**](docs/README_ZH-HANT.md) · [**English**](docs/README_EN.md) · [**日本語**](docs/README_JA.md) · [**Deutsch**](docs/README_DE.md) · [**Français**](docs/README_FR.md)

<br>

[📖 为什么](#为什么做这个项目) · [👥 适合谁](#适合这些人) · [⚡ 安装](#安装) · [🚀 快速开始](#快速开始) · [🧪 实验编程](#实验编程) · [📊 数据分析](#数据分析) · [📂 文件结构](#文件结构)

</div>

<br>

## 📖 为什么做这个项目

<div align="center">

当前心理学研究面临的痛点

🔬 &nbsp;一个 idea 要变成能收数据的实验程序，得先学 Python 或 JavaScript 或 MATLAB。<br>
📦 &nbsp;实验室祖传代码换台电脑就崩，没人说得清依赖、没人改得动逻辑。<br>
📊 &nbsp;统计方法靠习惯选——"大家都用 ANOVA"，审稿人一句质疑就得从头再来。<br>
🔁 &nbsp;分析结果只有自己跑得出来，换个环境换个随机种子结论可能就变了。<br>
✂️ &nbsp;做实验和做分析的经常是两拨人——收完数据才发现设计时根本没想好怎么分析。<br>
📝 &nbsp;投稿被要求提供可重复性声明，但代码没有审计、没有记录、没有人独立验证过。

</div>

一个心理学研究者从有想法到真正开始收数据、出结果，路上有两件事最耗时间。

**第一件：实验编程。** 想验证一个假设，得先把实验写出来。PsychoPy 的 Builder 不够灵活，Coder 要学 Python；jsPsych 要学 JavaScript 和 timeline 逻辑；Psychtoolbox 要学 MATLAB 和帧同步。光是搞清楚"RT 从哪一屏开始算""按键映射怎么不反""数据怎么存崩了不丢"就要花几周。一个 idea 从脑子里到能跑起来，中间耗掉的时间比设计实验本身还长。

**第二件：数据分析。** 数据收回来了，该用什么统计方法？被试内设计用配对 t 还是混合模型？准确率接近天花板 ANOVA 还能用吗？审稿人问"为什么用这个方法"时怎么回答？代码换了台电脑还能不能跑出一样的结果？

这些不是能力问题，是缺少合适的工具。写代码和做分析应该让研究更顺利，不应该成为卡住你的地方。

不需要你会 Python，不需要你懂统计，你只需要把实验想法和数据交给它——它会引导你一步步确认设计、生成代码、完成审计。最终拿到的代码打开就能跑，分析结果期刊审稿人也挑不出毛病。

<div align="center">

Amazing PsyCoder 把实验编程和数据分析的经验编码进了 7 个技能——1 个编排器加 6 个子技能，遵循 agentskills.io 开放标准，支持 Claude Code / Codex / Hermes / OpenClaw。

**把时间还给研究本身。**

</div>

---

## 👥 适合这些人

- 🎓 正在或准备写实验代码的心理学本科生、研究生
- 🧠 做认知、行为、社会心理实验的研究者
- 😵‍💫 在 RT、随机化、条件表上反复踩坑，希望实验代码有质量保障
- 📊 收完数据不确定该用什么统计方法，希望有系统化分析方案
- 📝 投稿前想确认分析可重复——需要独立审计
- 🐍 PsychoPy · 🌐 jsPsych · 🧮 Psychtoolbox / MATLAB 用户

---

## ⚡ 安装

在 AI 对话中直接输入对应平台的命令：

**Claude Code**

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/amazing-psycoder-skills
```

**Codex**

```
$skill-installer
```

输入仓库地址：`https://github.com/soupandpsy/amazing-psycoder-skills`

**Hermes**

```
hermes skills install https://github.com/soupandpsy/amazing-psycoder-skills
```

**OpenClaw**

```
npm i -g clawhub && clawhub install amazing-psycoder
```

安装后输入 `/amazing-psycoder` 即可启动。

<details>
<summary><b>终端安装（所有平台通用）</b></summary>

<br>

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
./install.sh           # 自动检测平台并安装
# 或手动指定: ./install.sh claude | codex | hermes | openclaw
```

</details>

---

## 🚀 快速开始

安装后输入 `/amazing-psycoder`，直接描述你想做什么：

> "我要做一个 Stroop 任务，红绿蓝三色，按键反应" → 自动进入实验设计

> "帮我分析 Stroop 数据，一致和不一致 RT 有没有差异" → 自动进入分析设计

不需要指定用哪个技能——编排器根据你的需求自动判断。之后 skill 会一步步引导你：确认设计、选择方法、生成代码、审计检查。你只需要回答它提出的问题。

下面是实验编程和数据分析的详细介绍，每个部分末尾都有完整的交互 Demo。

---

## 🧪 实验编程

从想法到可采集数据的实验代码，分三步走——设计、生成、审计。

### 技能

| # | 技能 | 功能 |
|---|------|------|
| ① | **设计编排** `psy-exp-designer` | 将实验想法转化为完整设计规范，5 阶段渐进确认，生成试次窗口时间线图 |
| ② | **代码生成** `psy-exp-coder` | 从设计规范生成可运行实验代码，自动拦截 `time.sleep()` 等常见错误 |
| ③ | **代码审计** `psy-exp-reviewer` | 检查 → 修复 → 再检查，直到 0 Critical + 0 Major 才交付 |

### 平台

| 平台 | 特点 |
|------|------|
| 🐍 **[PsychoPy](https://psychopy.org/)** | Python 生态，USB HID 硬件时间戳，毫秒级 RT 精度。本地实验室首选 |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | JavaScript 生态，浏览器即运行，无需安装。在线实验首选 |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | MATLAB 生态，GPU 级帧精确控制。时序精度要求极致时首选 |

### 范式覆盖

**38 个范式**，每个按统一元逻辑整理：何时使用 → 核心逻辑 → 必须确认 → 不要假设 → 试次窗口时间线 → 条件表 → 数据分析 → 变体与参考。

| 类别 | 范式 |
|------|------|
| 🎯 **注意与抑制控制** | Stroop · Eriksen Flanker · Simon · Go/No-go · Stop-signal · ANT · Posner Cuing · Visual Search · Dot-probe · Navon · CPT · Antisaccade |
| 🧠 **记忆与工作记忆** | N-back · Sternberg · Corsi Blocks · Change Detection · Drag and Drop |
| 🔄 **执行功能与认知灵活性** | Task Switching · WCST · Choice RT |
| 👥 **社会认知与情绪** | Cyberball · Climate Reflection · Phone a Friend · Rating · Priming · IAT · EAST |
| 💰 **决策与奖励** | BART · Delay Discounting · Rating to Choice · Ultimatum Game |
| 👁️ **感知与心理物理** | Psychophysics Staircase · Multisensory Nature · Mental Rotation |
| 🌱 **发展与个体差异** | Children Flanker · Bilingual Stroop · Numerical Stroop · Writing Distraction |

### 🎬 Demo：做一个 Stroop 实验

> "我要做一个 Stroop，红绿蓝三色文字，按键判断墨色，50:50 一致不一致，2 block 各 60 试次"

```
用户             ❯ 我要做一个 Stroop 任务

Amazing PsyCoder ❯ 🟢 Phase 1/5 · 诊断
                   范式 Stroop · 确认使用 PsychoPy？

用户             ❯ 对，PsychoPy。

Amazing PsyCoder ❯ 🟢 Phase 2/5 · 试次窗口 + 反应规则（最关键）
                   墨色红绿蓝 → f=红 j=绿 k=蓝。试次时间线：
                       Window 1: 注视点             Window 2: 刺激呈现            Window 3: 空屏等待   
                   ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
                   │                      │      │                      │      │                      │
                   │          +           │  →   │       红色"绿"       │  →   │                      │
                   │                      │      │                      │      │                      │
                   └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
                            500ms                         2000ms                        500ms          
                            无反应                      f / j / k                       无反应         
                                                        ← RT起点                                      

                        Window 4: 反馈     
                   ┌──────────────────────┐
                   │                      │
                   │        正确!         │
                   │                      │
                   └──────────────────────┘
                            1000ms         
                            无反应         
                   Gate 1 ✅ 窗口完整、反应映射已确认

用户             ❯ 时间线和按键没问题。ITI 400-800ms 随机。

Amazing PsyCoder ❯ 🟢 Phase 3/5 · 条件表
                   一致:不一致 = 60:60 → 120 试次条件表已生成。Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Block 结构
                   2 blocks × 60 trials · 反馈仅练习 block。Gate 3 ✅

Amazing PsyCoder ❯ 🟢 Phase 5/5 · 最终审查
                   ┌──────────────────────────────────────────────┐
                   │ 设计决策注册表                               │
                   │ 范式 Stroop · 平台 PsychoPy    ← 用户确认    │
                   │ 按键 f/j/k · 一致:不一致 50:50 ← 用户确认    │
                   │ ITI 400-800ms 随机             ← 用户确认    │
                   │ 试次时间线 4 窗口              ← 范式惯例    │
                   └──────────────────────────────────────────────┘
                   Gate 5 ✅ 全部确认 → 路由至代码生成

用户             ❯ 生成。

Amazing PsyCoder ❯ ✅ stroop_task.py + README.md 已生成
                   参数置顶 · CJK 字体已配置 · 增量保存 → 自动路由至审计

Amazing PsyCoder ❯ 🔍 第 1 轮审计 · 发现 0 个问题
                   审计通过 · 就绪标签：ready_for_collection
                   可开始数据采集。
                   （如有问题，修复后进入第 2 轮，直到通过）
```

---

## 📊 数据分析

数据收回来后，同样分三步走——设计分析方案、生成代码、审计可重复性。

### 技能

| # | 技能 | 功能 |
|---|------|------|
| ④ | **分析设计** `psy-ana-designer` | 从科学问题出发设计分析方案，12 维度比较选择最优统计方法 |
| ⑤ | **分析代码** `psy-ana-coder` | 从分析方案生成 R 或 Python 可重复分析脚本 |
| ⑥ | **分析审计** `psy-ana-reviewer` | 检查 → 修复 → 再检查，直到 0 Critical + 0 Major 才交付 |

### 平台

| 平台 | 特点 |
|------|------|
| 📊 **[R](https://www.r-project.org/)** | 统计计算标准。tidyverse + lme4 + ggplot2 + RMarkdown。学术出版首选 |
| 🐍 **[Python](https://www.python.org/)** | 通用科学计算。pandas + statsmodels + seaborn + Jupyter。可重复分析 |

### 分析方法

**60 种分析方法，48 种图表类型**。每个方法选择经过 12 维度对比：统计效力 · 假阳性控制 · 数据利用率 · 异常值敏感度 · 假设鲁棒性 · 可解释性 · 领域接受度 · 效应量可比性 · 可重复性 · 可扩展性 · 样本量约束 · 计算可实现性。

| 类别 | 方法举例 |
|------|------|
| **均值比较** | 配对/独立 t 检验、被试内/间 ANOVA、混合 ANOVA、ANCOVA、MANOVA |
| **混合模型** | 线性混合模型（LMM）、逻辑混合模型（GLMM）、Gamma GLMM、交叉随机效应 |
| **中介调节** | 中介分析、调节分析、有调节的中介、结构方程模型 |
| **回归与纵向** | 多元回归、分位数回归、增长曲线、交叉滞后面板、时间序列 |
| **相关与分类** | Pearson/Spearman 相关、重复测量相关、卡方检验、典型相关 |
| **非参与稳健** | Wilcoxon、Friedman、置换检验、Bootstrap、稳健回归 |
| **贝叶斯** | 贝叶斯 t 检验、贝叶斯 ANOVA、贝叶斯混合模型 |
| **测量与量表** | 信度分析（α/ω/ICC）、探索性/验证性因子分析、多维标度法 |
| **信号检测与诊断** | d'、ROC 曲线、心理测量函数 |
| **RT 与决策建模** | Ex-Gaussian 分布、漂移扩散模型（DDM） |
| **元分析与效力** | 元分析、效力分析、等效性检验 |
| **专项方法** | 多重插补、LASSO/Ridge、网络分析、聚类分析、潜在类别分析 |

### 🎬 Demo：分析一组 Stroop 数据

> "帮我分析 Stroop 数据，一致和不一致条件的 RT 有没有显著差异"

```
用户             ❯ 帮我分析 Stroop 数据，一致和不一致 RT 有没有差异

Amazing PsyCoder ❯ 🟢 Phase 1/5 · 理解实验与科学问题
                   请提供实验 config 或描述实验设计

用户             ❯ 被试内，IV: condition(一致/不一致)，DV: rt+acc。30 被试

Amazing PsyCoder ❯ 🟢 Phase 2/5 · 理解数据结构
                   数据怎么存的？每被试一个文件还是汇总？

用户             ❯ 每被试一个 CSV，命名 sub-001_stroop.csv
                   列: subject_id, condition, rt, acc, trial

Amazing PsyCoder ❯ 已确认：30 被试 × 每被试 1 文件。Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 3/5 · 数据特点 + 匹配方法（核心阶段）
                   RT 有右偏吗？准确率有没有接近天花板？

用户             ❯ RT 有点右偏，准确率大概 95%

Amazing PsyCoder ❯ 准确率接近天花板 → glmer(binomial) 做 acc 分析
                   对 RT，12 维度比较 A vs B：

                   ┌────────────┬─────────────────┬─────────────────┐
                   │ 维度       │ A: 配对 t 检验   │ B: 线性混合模型  │
                   ├────────────┼─────────────────┼─────────────────┤
                   │ 统计效力   │ 30 点（被试均值）│ 1800 点（全试次）│
                   │ 数据利用率 │ 每被试压缩为 1 点│ 全部试次参与     │
                   │ 可扩展性   │ 加协变量需重做   │ 公式加 + 即可    │
                   │ 可解释性   │ d=0.5 人人懂     │ 需解释随机效应   │
                   └────────────┴─────────────────┴─────────────────┘

                   侧重效力和可扩展 → 选 B。侧重简单 → 选 A。

用户             ❯ 选 B

Amazing PsyCoder ❯ Gate 3 ✅ 方法已选（附 12 维度比较理由）

Amazing PsyCoder ❯ 🟢 Phase 4/5 · 分析细节
                   清洗: RT 150-2000ms · 正确试次 · 被试 acc<60% 排除
                   · ±2.5 SD 试次排除 · 图表: 雨云图+个体连线 ⚠️

用户             ❯ 确认

Amazing PsyCoder ❯ 🟢 Phase 5/5 · 最终审查
                   ┌──────────────────────────────────────────────┐
                   │ 分析决策注册表                               │
                   │ 科学问题: 一致 vs 不一致 RT       ← 用户确认  │
                   │ 方法: lmer (用户选 B)              ← 用户确认  │
                   │ RT 150-2000ms · 被试 acc<60%       ← 默认 ⚠️   │
                   │ 图表: 雨云图 + 个体连线            ← 默认 ⚠️   │
                   └──────────────────────────────────────────────┘
                   Gate 5 ✅ 保存 analysis_config.yaml → 路由至代码生成

用户             ❯ 生成。

Amazing PsyCoder ❯ ✅ analysis.R + report.Rmd 已生成
                   Config 驱动 · 10 项质量门 · 12 步脚本结构 → 路由至审计

Amazing PsyCoder ❯ 🔍 第 1 轮审计 · 发现 0 个问题
                   审计通过 · 就绪标签：ready_for_publication
                   （如有问题，修复后进入第 2 轮，直到通过）
```

---

## 📂 文件结构

```
amazing-psycoder-skills/
├── amazing-psycoder/                  ← 编排器（系统入口，v1.3）
│   ├── SKILL.md · PLATFORMS.md · install.sh
│   │
│   │   # 🧪 实验编程
│   ├── psy-exp-designer/              ← ① 实验设计（5 阶段 + 38 范式 + 9 参考文件）
│   ├── psy-exp-coder/                 ← ② 实验代码生成（PsychoPy/jsPsych/Psychtoolbox）
│   └── psy-exp-reviewer/              ← ③ 实验审计（5 模式 + 烟雾测试 + 恢复循环）
│   │
│   │   # 📊 数据分析
│   ├── psy-ana-designer/              ← ④ 分析设计（5 阶段 + 60 方法 + 48 图表）
│   ├── psy-ana-coder/                 ← ⑤ 分析代码生成（R/Python 双平台）
│   └── psy-ana-reviewer/              ← ⑥ 分析审计（4 模式 + 摄入协议 + 恢复循环）
│
├── docs/                              ← 多语言 README（简/繁/英/日/德/法）
└── README.md
```

---

<div align="center">

💡 有想法或建议？欢迎来信 [tangdingyi04@outlook.com](mailto:tangdingyi04@outlook.com)<br>
🪄 Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
