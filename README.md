<div align="center">

# Amazing PsyCoder

> 心理学人的米奇妙妙屋：从实验设计到程序编写一步到位！🎉

</div>

## 📖 为什么做这个项目

心理学实验编程的痛点，做过的人都懂：

- **学习成本高** — PsychoPy 的 Builder 和 Coder 该用哪个？Psychtoolbox 的 `Screen('Flip')` 为什么要在 `vbl + (waitframes - 0.5) * ifi` 时刻翻页？光是搞清楚 API 就要花几周。
- **设计时漏细节** — 试次窗口长什么样？反应时从哪个窗口开始算？按键映射是什么？漏一个细节，实验逻辑就崩。
- **切换平台困难** — 实验室的 PsychoPy 代码想在 Pavlovia 上线跑？从 Python 翻译成 JavaScript，所有 API 都要重写。
- **写代码时踩坑** — `time.sleep()` 阻塞了 Escape 键，被试按啥都没反应。中文刺激没配字体，屏幕上一堆 □□□。这些坑每个初学者都必踩一次。
- **代码报错不知道怎么改** — 报了一屏红字，不知道该看哪一行。搜了半天 StackOverflow，发现别人的问题跟自己的完全不一样。
- **改参数要找半天** — 想把注视点从 500ms 改成 800ms，翻了 300 行代码才找到那个藏在循环里的魔数。
- **代码过了自己这关仍不安心** — 跑起来了，但 RT 到底测得准不准？数据保存方式对不对？万一被试做一半崩了，之前的数据还在不在？
- **别人看不懂你的代码** — 接手师兄的代码，变量名叫 `x1`、`x2`、`tmp`，没有注释，不知道从哪开始改。

每个实验室都有踩过这些坑的师兄师姐，但他们的经验很少被系统化地沉淀下来。Amazing PsyCoder 把这些经验编码进了 Claude Code 的三个强制技能里——不是给你一份代码模板自己改，而是像一位坐在你旁边的实验编程老手，一步步确认设计、生成代码、审计质量。

## 🎯 我们做了什么

- **🔴 设计编排层**（psych-experiment-programming）—— 5 阶段渐进式确认，试次窗口时间线画清楚才放行，不猜任何实验细节
- **🟡 代码生成层**（psych-experiment-coder）—— 4 层优先级架构生成代码，9 项质量门自动检查，`time.sleep()` 和 `KbCheck` 测 RT 直接拒绝
- **🟢 审计层**（psych-experiment-code-reviewer）—— 烟雾测试、数据完整性验证、范式特定失败模式检查，输出 `ready_for_collection` 才准收数据

三步全部强制，不可跳过。**未经审计的代码不交付。**

## ✨ 特点

- 🔬 **帮你避开常见坑**：写实验代码最容易犯的错——`time.sleep()` 阻塞按键、`KbCheck` 测不准反应时——系统直接拒绝，不让你踩
- 🚀 **拿来就能用**：生成的代码不需要再改这改那，打开就能跑。想要调参数？全部放在文件最上面，不用翻代码
- 🌏 **中文无法显示**：显示中文指导语最怕被试看到一堆 □□□，系统会自动检测并配置中文字体
- 🧪 **崩溃不丢数据**：每个试次结束立刻存盘。就算实验崩了，已经收完的试次数据都还在
- 🎛️ **一个系统，三个平台**：不管你们实验室用 PsychoPy、jsPsych 还是 MATLAB 的 Psychtoolbox，都能生成对应的代码

**不要在实验代码调试上浪费时间，把精力留给真正的科研。**

---

## 📑 目录

- [安装](#安装)
- [快速开始](#快速开始)
- [三个技能](#三个技能)
- [平台支持](#平台支持)
- [范式覆盖](#范式覆盖)
- [文件结构](#文件结构)

---

## 安装

在 Claude Code 中输入：

```
Install Amazing PsyCoder for me: https://github.com/<your-username>/AmazingPsyCoderSkills
```

Claude Code 会自动 clone 仓库、把 4 个技能注册到 `~/.claude/skills/`。完成后输入 `/amazing-psycoder` 即可启动。

<details>
<summary>手动安装</summary>

```bash
git clone https://github.com/<your-username>/AmazingPsyCoderSkills /tmp/AmazingPsyCoderSkills
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

- **[PsychoPy](https://psychopy.org/)** — 本地实验，精确 RT 计时（USB HID 硬件时间戳）
- **[jsPsych](https://www.jspsych.org/v7/)** — 在线实验，浏览器端部署
- **[Psychtoolbox](http://psychtoolbox.org/)** — MATLAB 实验室，GPU 级帧精确控制

每个平台均配备完整的代码生成体系。

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

