# psy-exp-coder — 实验代码生成/修改/调试层

> **版本**: v1.4.0 | 从已确认的 config 生成平台代码，或对现有代码做范围明确的修改/调试。静态通过不等于可采集。

## 三种模式

- `generate`：需要 Designer Gate 5、保存的 config/条件表，以及 `validate_experiment.py` 零错误。
- `modify`：读取现有代码和可用 config，保持未授权的设计语义不变。
- `debug`：先定位可复现根因，再做最小修复并重跑相关验证。

## 生成原则

1. 读取 config 的 `runtime`，固定 framework/core/plugin/dependency 版本；不使用未记录的 `latest`。
2. 从目标平台 L1 spec 复制骨架，按 L2 mapping 映射 config。
3. L3 只提供范式逻辑。Pavlovia/PsychoJS/jsPsych 6/旧 PsychoPy 代码块均视为隔离来源，不能复制 API。
4. 只生成 config 声明的 instruction、practice、窗口、反馈和事件；不套用万能 trial 模板。
5. 生成语义化 trial-summary；重复 trial 内事件使用关联 event table。采集端保留原始字段，不计算 SSRT、D-score、d-prime、bias score 或执行分析排除。
6. 每 trial 形成耐久 checkpoint，所有完成/中止/异常路径进入清理。
7. 运行平台语法检查、`validate_experiment.py --code`、Quality Gate 和 Reviewer 静态审查。

## 平台入口

| 平台 | 入口 | 关键限制 |
|------|------|----------|
| PsychoPy | [psychopy/README.md](psychopy/README.md) | 后端与时序必须按目标版本/机器验证 |
| jsPsych | [jspsych/README.md](jspsych/README.md) | 当前目标为 config 固定的 jsPsych 8.x；PsychoJS 是独立 runtime |
| Psychtoolbox | [psychtoolbox/README.md](psychtoolbox/README.md) | MATLAB/Octave/PTB 版本、许可和目标硬件须在运行前确认 |

## 交付证据

交付代码、条件/刺激、依赖清单、README、静态验证报告和 smoke-test 协议。零静态错误最多进入目标机测试；只有 Reviewer 审查过实际 smoke-test 证据后，才能给出 `ready_for_collection`。

完整工作流见 [SKILL.md](SKILL.md)。
