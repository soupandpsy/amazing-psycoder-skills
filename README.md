# Amazing PsyCoder Skills

> 从实验构想到可运行代码，三板斧一步到位。

Three Claude Code skills forming a mandatory sequential chain that converts psychological experiment ideas into audited, production-quality code across PsychoPy, jsPsych, and Psychtoolbox.

```
用户描述实验 / User describes experiment
       │
       ▼
  ① psych-experiment-programming      设计层 · 5 阶段确认
       │
       ▼
  ② psych-experiment-coder            代码层 · 自动生成 + 质量闸
       │
       ▼
  ③ psych-experiment-code-reviewer    审计层 · 强制通过才能收数据
```

---

## Quick Start

在 Claude Code 中输入：

```
/amazing-psycoder
```

然后描述你的实验，例如："我要做一个情绪 Stroop 实验，中文情绪词用红绿蓝三色呈现，按键反应"

AI 会依次引导你完成设计确认 → 代码生成 → 代码审计。

---

## 三个技能

| 技能 | 输入 | 输出 | 强制？ |
|------|------|------|--------|
| **psych-experiment-programming** | 自然语言实验描述 | config YAML + 条件表 | ✅ |
| **psych-experiment-coder** | config YAML | 可运行代码 + README | ✅ |
| **psych-experiment-code-reviewer** | 实验代码 | 审计报告 + 就绪标签 | ✅ |

**三步都不能跳过。** 没有 Reviewer 审计通过的代码不算完成。

---

## 核心红线

- **设计确认后才能生成代码** — 试次窗口时间线未确认绝不写代码
- **反模式零容忍** — `time.sleep()`, `event.getKeys(maxWait=)`, `KbCheck` 测 RT 一律禁止
- **中文必须有字体** — 缺失中文字体路径会导致文字无法渲染（□□□）
- **增量保存** — 每试次即时写入，崩溃不丢失数据
- **生成后必须审计** — 数据采集前的最后一道闸门

详细红线与设计原则见 [amazing-psycoder/SKILL.md](amazing-psycoder/SKILL.md)。

---

## 支持平台

| 平台 | 4 层代码生成 | 范式参考 |
|------|-------------|----------|
| **PsychoPy** (2024.x+, Python 3.10+) | 全满，自动生成 | 27 个 |
| **jsPsych** (7.x, JavaScript) | 全满，自动生成 | 25 个 |
| **Psychtoolbox** (MATLAB) | 全满，手动参考 | 5 个 + 82 个 demo |

---

## 范式覆盖

**核心 14 个**（完整设计+代码参考）：Go/No-go · Navon · Priming · Stroop · Eriksen Flanker · Simon · Rating · Stop-signal · IAT · N-back · Dot-probe · Visual Search · Task Switching · EAST

**扩展 24 个**（设计参考）：Antisaccade · ANT · BART · Bilingual Stroop · Change Detection · Choice RT · CPT · Corsi Blocks · Cyberball · Delay Discounting · Mental Rotation · Posner Cuing · Sternberg · WCST 等

---

## 文件结构

```
AmazingPsyCoderSkills/
├── amazing-psycoder/SKILL.md               ← 入口技能（给 AI 看）
├── psych-experiment-programming/            ← ① 设计编排层
│   ├── SKILL.md
│   ├── paradigms/                           ← 38 个范式参考文件
│   └── references/                          ← 设计规范（config-schema, timing 等）
├── psych-experiment-coder/                  ← ② 代码生成层
│   ├── SKILL.md
│   ├── psychopy/{spec,mapping,paradigm,demo}/
│   ├── jspsych/{spec,mapping,paradigm,demo}/
│   └── psychtoolbox/{spec,mapping,paradigm,demo}/
└── psych-experiment-code-reviewer/          ← ③ 审计层
    └── SKILL.md
```

---

## 版本

v1.0 — 2026-05-30
