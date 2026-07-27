# psy-exp-reviewer — 实验审计与证据门

> **版本**: v1.4.0 | **角色**: 审计实验设计、配置、实现和运行证据；不直接修改代码。

## 核心原则

Reviewer 不把“看起来正确”当成“可以采集”。证据按以下顺序升级：

```text
design_confirmed
  → static_review_passed
  → runtime_or_execution_passed
  → ready_for_collection
```

静态代码审计只能发现可见风险；`ready_for_collection` 还必须有目标机器上的实测 smoke-test 证据，包括启动、刺激呈现、响应、数据保存、中断恢复和正常退出。所有审计都应报告输入范围、未验证事项和证据文件路径。

## 审查模式

| 模式 | 最低输入 | 最大结论 |
|------|----------|----------|
| `code-audit` | 代码 + config；如需最终就绪标签还要 smoke-test 证据 | 无运行证据时为 `not_ready_for_collection`；证据充分时可为 `ready_for_collection` |
| `config-audit` | Config YAML / trial timeline | `pre_code_ready` |
| `implementation-plan-review` | 伪代码 / 架构计划 | 仅架构风险与待确认项 |
| `triage-only` | 自然语言实验描述 | 缺失信息与设计风险 |
| `blocked` | 无可审查输入 | 明确所需输入 |

## 审计范围

- 设计忠实度：窗口、条件、计分、反应映射与 config 一致。
- 计时与响应：RT 原点、响应事件、超时、多键和退出逻辑明确。
- 随机化：seed scope、解析后的 seed、比例、约束和 counterbalancing 可复现。
- 刺激与运行环境：资源、字体、版本、依赖和目标设备策略明确。
- 数据语义：语义化 trial-summary；重复的试次内事件写入关联 event table；缺失 RT 不用数值哨兵。
- 持久化与恢复：增量保存、唯一标识、重复运行防护、中断测试和资源清理。
- 运行证据：在声明的目标环境中实际观察，而不是由静态检查推断。

## 平台感知

`code-audit` 根据实现加载相应规范：

| 平台签名 | 规范 |
|----------|------|
| PsychoPy (`from psychopy import`, `visual.Window`) | `../psy-exp-coder/psychopy/spec/README.md` |
| jsPsych (`initJsPsych`, `jsPsych.run`) | `../psy-exp-coder/jspsych/spec/README.md` |
| Psychtoolbox (`PsychImaging`, `Screen('Flip'`) | `../psy-exp-coder/psychtoolbox/spec/README.md` |

## 严重度与标签

严重度按对数据有效性、参与者安全、数据丢失和结论正确性的实际影响分级，而不是按固定问题数量分级。

| 标签 | 证据要求 |
|------|----------|
| `ready_for_collection` | 零 Critical/Major，且目标机器 smoke test 已通过并被审查 |
| `not_ready_for_collection` | 存在 Critical/Major，或所需运行证据缺失/失败 |
| `pre_code_ready` | 配置完整，只代表可以进入代码生成 |
| `needs_experiment_info` | 关键设计信息缺失 |
| `blocked` | 输入不足，无法形成相应结论 |

完整协议、检查表和输出格式见 [SKILL.md](SKILL.md)。
