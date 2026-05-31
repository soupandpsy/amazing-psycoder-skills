<div align="center">

# 🧠 Amazing PsyCoder 💻

> 心理学人的米奇妙妙屋：先把实验理清楚，再把代码写出来，最后少踩几个坑。🪄

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Stars](https://img.shields.io/github/stars/soupandpsy/AmazingPsyCoderSkills?style=social)](https://github.com/soupandpsy/AmazingPsyCoderSkills)

</div>

**Design ⇒ Generate ⇒ Audit.** Three mandatory skills, one runnable experiment. No skipped steps, no guesswork, no code delivered without review.

---

## 📖 为什么做这个项目

心理学实验编程的痛点，做过的人都懂。程序能跑 🏃 只是第一步，真正的折磨是——它跑起来以后，到底是不是按你的实验逻辑在跑。😵‍💫

- ⏱️ **RT 到底从哪一屏开始算** —— 计时起点标错，整批反应时数据白收
- ⌨️ **按键映射有没有写反** —— f=红还是f=绿？被试按对了代码判错了
- 🚦 **No-go 不按键怎么算正确** —— 该按不按、不该按按了，规则不清
- 🧩 **设计时漏细节** —— 试次窗口长什么样？按键映射是什么？漏一个细节，实验逻辑就崩
- 📊 **条件表和刺激文件对不上** —— 列名拼错、文件路径写错，试次直接跳过
- 🔀 **随机化连续出现同类试次** —— 被试按了一排同一个键，数据废了
- 💾 **程序崩了数据还在不在** —— 跑完才保存，崩了全丢
- 🔤 **中文指导语变成 □□□** —— 没配中文字体，被试看着一堆豆腐块
- 😇 **代码能跑，但真的能正式采集吗** —— 跑起来了，RT 准不准？逻辑对不对？没底

每个实验室都有踩过这些坑的师兄师姐，但他们的经验很少被系统化地沉淀下来。Amazing PsyCoder 把这些经验编码进了 Claude Code 的三个强制技能里——不是给你一份代码模板自己改，而是像一位坐在你旁边的实验编程老手，一步步确认设计、生成代码、审计质量。

## 🎯 我们做了什么

- 1️⃣ **设计编排层**（psych-experiment-programming）—— 先帮你理清实验设计：试次时间线怎么走？block 怎么分？条件表怎么设计？按键规则是什么？正确性怎么算？5 阶段渐进式确认，试次窗口时间线画清楚才放行，不猜任何实验细节
- 2️⃣ **代码生成层**（psych-experiment-coder）—— 再帮你生成实验代码：4 层优先级架构，9 项质量门自动检查，`time.sleep()` 和 `KbCheck` 测 RT 直接拒绝。重点处理 RT 计时、反应收集、刺激呈现、条件文件读取、增量保存、Escape 退出、中文字体
- 3️⃣ **审计层**（psych-experiment-code-reviewer）—— 最后帮你做采集前审查：RT 起点有没有问题？按键映射有没有反？数据保存安不安全？随机化是否合理？烟雾测试 + 数据完整性验证 + 范式特定失败模式检查，输出 `ready_for_collection` 才准收数据

三步全部强制，不可跳过。**未经审计的代码不交付。**

## ✨ 特点

- 🔬 **帮你避开常见坑**：写实验代码最容易犯的错——`time.sleep()` 阻塞按键、`KbCheck` 测不准反应时——系统直接拒绝，不让你踩
- 🚀 **拿来就能用**：生成的代码不需要再改这改那，打开就能跑。想要调参数？全部放在文件最上面，不用翻代码
- 🌏 **中文无法显示**：显示中文指导语最怕被试看到一堆 □□□，系统会自动检测并配置中文字体
- 🧪 **崩溃不丢数据**：每个试次结束立刻存盘。就算实验崩了，已经收完的试次数据都还在
- 🎛️ **一个系统，三个平台**：不管你们实验室用 PsychoPy、jsPsych 还是 MATLAB 的 Psychtoolbox，都能生成对应的代码

**少一点玄学调试，少一点凌晨崩溃，多一点正式采集前的安全感。🧪✨**

---

## 📑 目录

- [安装](#安装)
- [快速开始](#快速开始)
- [三个技能](#三个技能)
- [平台支持](#平台支持)
- [适合这些人](#-适合这些人)
- [范式覆盖](#范式覆盖)
- [文件结构](#文件结构)

---

## 安装

在 Claude Code 中输入：

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/AmazingPsyCoderSkills
```

Claude Code 会自动 clone 仓库、把 4 个技能注册到 `~/.claude/skills/`。完成后输入 `/amazing-psycoder` 即可启动。

<details>
<summary>手动安装</summary>

```bash
git clone https://github.com/soupandpsy/AmazingPsyCoderSkills /tmp/AmazingPsyCoderSkills
cp -r /tmp/AmazingPsyCoderSkills/amazing-psycoder ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/psych-experiment-programming ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/psych-experiment-coder ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/psych-experiment-code-reviewer ~/.claude/skills/
```

</details>

---

## 快速开始

在 Claude Code 中输入：

```
/amazing-psycoder
```

然后描述你的实验：

> "我要做一个 Stroop 任务，红绿蓝三色，按键反应，2 个 block 各 60 个试次"

系统自动路由到编排器，引导完成 5 阶段设计。设计过程中，系统会生成试次窗口时间线图，帮你直观确认每个试次的呈现流程：

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 注视点    │ →  │ 刺激呈现  │ →  │ 空屏等待  │ →  │ 反馈      │
│ +        │    │ 红色"绿"  │    │          │    │ 正确!     │
│ 500ms    │    │ 2000ms   │    │ 500ms    │    │ 1000ms   │
│          │    │ ← 按键   │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                  RT 计时起点
```

确认时间线后，指定目标平台生成对应代码。每个实验输出可直接运行的平台文件（`.py` / `.js` / `.m`）和实验说明 README。

> 💡 **使用说明**：Amazing PsyCoder 是一套 Claude Code Skills，安装到 `.claude/skills/` 目录后，Claude Code 启动时自动加载。在对话中描述实验需求即可触发对应流程，无需记忆复杂 prompt。

---

## 三个技能

- **psych-experiment-programming** — 设计编排层，5 阶段渐进式确认，输出 config YAML + 条件表
- **psych-experiment-coder** — 代码生成层，统一生成流水线 + 4 层优先级架构，输出可运行代码 + README
- **psych-experiment-code-reviewer** — 审计层（最终关卡），5 种审查模式 + 烟雾测试协议，输出审计报告 + 就绪标签

---

## 平台支持

- 🐍 **[PsychoPy](https://psychopy.org/)** — 本地实验，精确 RT 计时（USB HID 硬件时间戳）
- 🌐 **[jsPsych](https://www.jspsych.org/v7/)** — 在线实验，浏览器端部署
- 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** — MATLAB 实验室，GPU 级帧精确控制

每个平台均配备完整的代码生成体系。

---

## 👥 适合这些人

- 👶 不太会写代码，但必须搞定实验程序
- 🎓 正在写或将要写实验代码的本科生、研究生
- 🧠 做认知、行为、社会心理实验的研究者
- 🐍 PsychoPy 本地实验 · 🌐 jsPsych 在线实验 · 🧮 Psychtoolbox / MATLAB
- 😵‍💫 被 RT、随机化、条件表反复背刺过，只想安心收数据

---

## 范式覆盖

**38 个范式**：14 个核心（完整设计规范）+ 24 个扩展（参考描述）。

核心：Go/No-go · Navon · Priming · Stroop · Eriksen Flanker · Simon · Rating · Stop-signal · IAT · N-back · Dot-probe · Visual Search · Task Switching · EAST

扩展：Antisaccade · ANT · BART · Bilingual Stroop · Change Detection · Choice RT · CPT · Corsi Blocks · Cyberball · Delay Discounting · Mental Rotation · Posner Cuing · Sternberg · WCST 等

---

## 文件结构

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

