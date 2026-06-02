<div align="center">

# 🧠 Amazing PsyCoder 💻

> 从实验构想到生产级代码，设计 → 生成 → 审计，三步强制交付。🪄

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Stars](https://img.shields.io/github/stars/soupandpsy/AmazingPsyCoderSkills?style=social)](https://github.com/soupandpsy/AmazingPsyCoderSkills)

[**简体中文**](README.md) · [**繁體中文**](README_ZH-HANT.md) · [**English**](README_EN.md) · [**日本語**](README_JA.md) · [**Deutsch**](README_DE.md) · [**Français**](README_FR.md)

<br>

[📖 为什么](#-为什么做这个项目) · [⚡ 安装](#-安装) · [🚀 快速开始](#-快速开始) · [🎬 Demo](#-demo) · [✨ 特点](#-特点) · [👥 适合谁](#-适合这些人)

</div>

<br>

<table>
<tr><td align="left">

⏱️ &nbsp;RT 到底从哪一屏开始算？计时起点标错，整批反应时数据白收。<br>
⌨️ &nbsp;按键映射有没有写反？被试按对了，代码判错了。<br>
🚦 &nbsp;No-go 不按键怎么算正确？该按不按、不该按按了，规则不清。<br>
💾 &nbsp;程序崩了数据还在不在？跑完才保存，崩了全丢。<br>
🔤 &nbsp;中文指导语变成 □□□ — 没配字体，被试看到的全是乱码。<br>
😇 &nbsp;代码能跑，但真的能正式采集吗？RT 是否准确、逻辑是否正确、数据是否可靠——没有系统性的保障。

</td></tr>
</table>

### ✨ Amazing PsyCoder 解决的就是这些。

不是给你一份代码模板自己改，而是像一位坐在你旁边的实验编程老手——**先帮你理清设计 → 再生成代码 → 最后做采集前审查**。

三步全部强制，不可跳过。**未经审计的代码不交付。**

---

## 📖 为什么做这个项目

每个实验室都有踩过这些坑的师兄师姐，但他们的经验很少被系统化地沉淀下来。PsychoPy 的 Builder 和 Coder 该用哪个？jsPsych 的 timeline 变量怎么传？Psychtoolbox 的 `Screen('Flip')` 为什么要在 `vbl + (waitframes - 0.5) * ifi` 时刻翻页？

光搞清楚 API 就要花几周。

Amazing PsyCoder 把这些经验编码进了 Claude Code 的三个强制技能里——设计编排（5 阶段确认）、代码生成（统一流水线 + 9 项质量门）、代码审计（烟雾测试协议）。不管你的实验室用 PsychoPy、jsPsych 还是 Psychtoolbox，同一套流程生成对应代码。

---

## 🎯 三个技能

| 技能 | 做什么 | 关键输出 |
|------|--------|---------|
| 1️⃣ **设计编排** `psych-experiment-programming` | 5 阶段渐进式确认：试次时间线 → 反应规则 → 条件表 → block 结构 → 最终确认 | config YAML + 条件表 |
| 2️⃣ **代码生成** `psych-experiment-coder` | 4 层优先级架构生成代码，9 项质量门自动检查。`time.sleep()` / `KbCheck` 测 RT 直接拒绝 | 可运行代码 + README |
| 3️⃣ **代码审计** `psych-experiment-code-reviewer` | 烟雾测试 + 数据完整性验证 + 范式失败模式检查。RT 起点、按键映射、数据安全逐项审查 | 审计报告 + 就绪标签 |

---

## ⚡ 安装

在 Claude Code 中输入以下指令，系统会自动完成安装：

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/AmazingPsyCoderSkills
```

Claude Code 会自动 clone 仓库，把技能文件注册到 `~/.claude/skills/`。完成后输入 `/amazing-psycoder` 即可启动。

<details>
<summary><b>🛠️ 手动安装</b></summary>

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

## 🚀 快速开始

在 Claude Code 中输入 `/amazing-psycoder`，然后描述你的实验：

> "我要做一个 Stroop 任务，红绿蓝三色，按键反应，2 个 block 各 60 个试次"

系统自动路由到编排器，引导完成 5 阶段设计。设计过程中，系统会生成试次窗口时间线图：

```
┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐
│ 注视点    │ →  │ 刺激呈现  │ →  │ 空屏等待  │ →  │ 反馈      │
│ +         │    │ 红色"绿"  │    │           │    │ 正确!     │
│ 500ms     │    │ 2000ms    │    │ 500ms     │    │ 1000ms    │
│           │    │ ← 按键    │    │           │    │           │
└───────────┘    └───────────┘    └───────────┘    └───────────┘
                  RT 计时起点
```

确认时间线后，指定目标平台。输出可直接运行的平台文件（`.py` / `.js` / `.m`）和实验说明 README。

---

## 🎬 Demo

### 🐍 PsychoPy — Stroop 任务

> "我要做一个 Stroop，红绿蓝三色文字，按键判断墨色，50:50 一致不一致，2 block 各 60 试次"

```
用户             ❯ 我要做一个 Stroop 任务

Amazing PsyCoder ❯ 🟢 Phase 1/5 · 诊断
                   范式 Stroop · 确认使用 PsychoPy？

用户             ❯ 对，PsychoPy。

Amazing PsyCoder ❯ 🟢 Phase 2/5 · 试次窗口 + 反应规则（最关键）
                   墨色红绿蓝 → f=红 j=绿 k=蓝。试次时间线：
                   ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐
                   │ 注视点    │ →  │ 刺激呈现  │ →  │ 空屏等待  │ →  │ 反馈      │
                   │ +         │    │ 红色"绿"  │    │           │    │ 正确!     │
                   │ 500ms     │    │ 2000ms    │    │ 500ms     │    │ 1000ms    │
                   │ 无反应    │    │ ← RT起点  │    │ 无反应    │    │ 无反应    │
                   └───────────┘    └───────────┘    └───────────┘    └───────────┘
                                       RT 计时起点
                   Gate 1 ✅ 窗口完整、反应映射已确认

用户             ❯ 时间线和按键没问题。ITI 400-800ms 随机。

Amazing PsyCoder ❯ 🟢 Phase 3/5 · 条件表
                   一致:不一致 = 60:60 → 120 试次条件表已生成
                   Gate 2 ✅ 条件列已填入

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Block 结构
                   2 blocks × 60 trials · 反馈仅练习 block
                   Gate 3 ✅ Config 零 [MISSING]

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
                   参数置顶 · CJK 字体已配置 · 增量保存
                   → 自动路由至代码审计

Amazing PsyCoder ❯ 🔍 审计通过 · 就绪标签：ready_for_collection
                   可开始数据采集。
```
---

## ✨ 特点

| 特点 | 说明 |
|------|------|
| 🔬 **常见坑自动拦截** | `time.sleep()`、`KbCheck` 测 RT——系统直接拒绝，不让你踩 |
| 🚀 **打开就能跑** | 所有参数置顶在文件开头，想调不用翻代码 |
| 🌏 **中文不出方框** | 自动检测中文并配置字体，被试看到的是字不是 □□□ |
| 🧪 **崩溃不丢数据** | 每个试次结束立刻存盘，崩了已收的数据全在 |
| 🎛️ **一个系统，三个平台** | 不管用 PsychoPy、jsPsych 还是 Psychtoolbox，同一套流程 |

**少一点玄学调试，少一点凌晨崩溃，多一点正式采集前的安全感。🧪✨**

---

## 📦 平台支持

| 平台 | 版本 | 定位 | 范式 | Demo |
|------|------|------|:--:|:--:|
| 🐍 **[PsychoPy](https://psychopy.org/)** | 2024.x+ | 本地实验室，USB HID 硬件时间戳 | 27 | 45 |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | 7.x | 在线实验，浏览器端部署 | 25 | 23 |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | 3.0.21+ | GPU 级帧精确控制 | 5 | 100 |

---

## 👥 适合这些人

- 👶 不太会写代码，但必须搞定实验程序
- 🎓 正在写或将要写实验代码的本科生、研究生
- 🧠 做认知、行为、社会心理实验的研究者
- 🐍 PsychoPy 本地实验 · 🌐 jsPsych 在线实验 · 🧮 Psychtoolbox / MATLAB
- 😵‍💫 在 RT、随机化、条件表上反复踩过坑，希望实验代码有质量保障

---

## 📦 范式覆盖

**38 个范式**：14 个核心（完整设计规范）+ 24 个扩展（参考描述）

| 类型 | 范式 |
|------|------|
| **核心** | Go/No-go · Navon · Priming · Stroop · Eriksen Flanker · Simon · Rating · Stop-signal · IAT · N-back · Dot-probe · Visual Search · Task Switching · EAST |
| **扩展** | Antisaccade · ANT · BART · Bilingual Stroop · Change Detection · Choice RT · CPT · Corsi Blocks · Cyberball · Delay Discounting · Mental Rotation · Posner Cuing · Sternberg · WCST 等 |

---

## 📂 文件结构

```
AmazingPsyCoderSkills/
├── amazing-psycoder/                  ← 编排器（系统入口）
├── psych-experiment-programming/      ← ① 设计层（5 阶段工作流 + 38 范式）
├── psych-experiment-coder/            ← ② 代码生成层
│   ├── psychopy/
│   ├── jspsych/
│   └── psychtoolbox/
└── psych-experiment-code-reviewer/    ← ③ 审计层（5 模式 + 烟雾测试）
```

---

<div align="center">

Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
