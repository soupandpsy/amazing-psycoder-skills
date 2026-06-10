# psy-exp-reviewer — 代码审计层

> **版本**: v1.3 | **角色**: 对实验代码进行质量审计，输出问题分级报告 + 就绪状态标签。不修改代码。amazing-psycoder 子技能。

## 一句话说明

输入实验代码（或 config / 实验方案），输出审计报告（Critical/Major/Minor 分级 + 修改建议 + 就绪标签）。

## 审计流程

```
输入 (代码 / config / 方案描述)
    │
    ▼
1. 检测模式 (code-audit / config-audit / implementation-plan-review / triage-only / blocked)
    │
    ▼
2. [code-audit] 检测平台 → 加载 coder spec
    │
    ▼
3. 运行 Quality Gate（9 项最低门槛）
    │
    ▼
4. 逐项审计（实验逻辑 → 计时 → 响应 → 随机化 → 刺激 → 数据 → 退出 → 就绪）
    │
    ▼
5. 分级（Critical > Major > Minor）→ 输出报告 + 就绪标签
```

## 5 种审查模式

| 模式 | 输入 | 能判断什么 |
|------|------|-----------|
| **code-audit** | 完整实验代码 | 代码级就绪状态（`ready_for_collection`） |
| **config-audit** | Config YAML / trial timeline | 设计级就绪状态（`pre_code_ready`） |
| **implementation-plan-review** | 伪代码 / 架构计划 | 架构风险 |
| **triage-only** | 自然语言实验描述 | 缺失信息清单 |
| **blocked** | 无有效输入 | 告知需要什么 |

## 平台感知（code-audit）

审计时自动检测平台并加载对应的 coder spec：

| 检测签名 | 平台 | 加载的规范 |
|----------|------|-----------|
| `from psychopy import` / `visual.Window` / `keyboard.Keyboard` | PsychoPy | `../psy-exp-coder/psychopy/spec/README.md` |
| `initJsPsych` / `jsPsych.run` / `jsPsychHtmlKeyboardResponse` | jsPsych | `../psy-exp-coder/jspsych/spec/README.md` |
| `PsychImaging` / `Screen('Flip'` / `KbQueueCreate` / `sca` | Psychtoolbox | `../psy-exp-coder/psychtoolbox/spec/README.md` |

## 审计维度

每次 code-audit 覆盖 9 个维度：

| # | 维度 | 核心检查 |
|---|------|---------|
| 0 | Quality Gate | 9 项最低门槛（任何失败 = Critical） |
| 1 | 实验逻辑 | 窗口序列、正确性规则、条件结构 |
| 2 | 计时与 RT | 平台特定 RT 源、帧精确 timing、反模式 |
| 3 | 响应收集 | 按键验证、超时、多键、Escape、no-go |
| 4 | 随机化 | 种子、比例、counterbalancing、约束 |
| 5 | 刺激 | 预加载、字体、文件验证、注视点 |
| 6 | 数据保存 | 增量、列完整性、崩溃恢复、文件名 |
| 7 | 紧急退出 | Escape 覆盖、数据留存、资源清理 |
| 8 | 采集就绪 | 参数可编辑性、README 完整性、硬件校准 |

## 就绪状态标签

| 标签 | 含义 |
|------|------|
| `ready_for_collection` | 零 Critical + 零 Major（仅 code-audit 可达） |
| `ready_after_minor_fixes` | 零 Critical + 零 Major；有 Minor（仅 code-audit 可达） |
| `not_ready_for_collection` | 有 Critical 或 Major 问题 |
| `pre_code_ready` | Config 完整，可开始写代码（仅 config-audit 可达） |
| `needs_experiment_info` | 关键设计信息缺失 |
| `blocked` | 输入不足，无法审查 |

## 关键文件

- [SKILL.md](SKILL.md) — 完整审计规范（5 种模式 + 平台感知检查表 + 输出格式）
