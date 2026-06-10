# psy-exp-designer — 实验设计编排层

> **版本**: v1.3 | **角色**: 你将实验想法告诉它，它逐步确认每个设计细节，产出完整的设计决策注册表和 config YAML。amazing-psycoder 子技能。

## 一句话说明

输入实验想法（中/英文），输出完整 config YAML + 设计决策注册表，经用户最终确认后路由到代码生成。

## 5阶段工作流

```
Phase 1: Assess      → 收集已有信息（范式、平台、操作系统/字体）
Phase 2: Windows     → 定义 Trial + 反应规则（最关键 — 窗口序列+按键映射+准确性规则）
Phase 3: Conditions  → 定义 trial 序列（条件表生成/验证，刺激文件）
Phase 4: Blocks      → 定义 block 结构和循环（练习/正式/休息/反馈）
Phase 5: Validate    → 验证 + 全量设计审查 → 路由至代码生成
```

每阶段结束必须**展示决策清单**，用户确认后才推进。

## 5道门禁

| Gate | 检查内容 |
|------|---------|
| Gate 1 | Phase 2 完成后：窗口序列无 `[MISSING]`，按键映射已确认 |
| Gate 2 | Phase 3 完成后：条件文件列名与窗口 `{column}` 一致 |
| Gate 3 | Phase 4 完成后：config 无 `[MISSING]`，所有 section 完整 |
| Gate 4 | Phase 5 技术验证：9条 schema 规则全部通过 |
| Gate 5 | **最终设计审查**：全量决策注册表展示，用户逐项确认 ⚠️ 默认项 |

## 核心机制

- **Design Decision Registry**: 跨阶段追踪所有设计决策，标记来源（用户确认/范式惯例/自动推断）
- **Phase Decision Checklist**: 每阶段输出决策清单，用户确认后推进
- **`[MISSING]` / `[ASSUMED]` 标记**: 缺值标记为 `[MISSING]`，默认值标记为 `[ASSUMED]`，均在 Gate 5 审查
- **Must-Confirm 跨阶段分配**: 范式文件的 Must-Confirm 项分配到对应阶段提问

## 范式覆盖

**38个范式**: 14核心（完整 Must-Confirm + 条件列定义）+ 24扩展（参考描述）

覆盖: Go/No-go、Navon、Priming、Stroop、Eriksen Flanker、Simon、Rating、Stop-signal、IAT、N-back、Dot-probe、Visual Search、Task Switching、EAST 及更多

详见 [paradigms/](paradigms/) 目录。

## 关键文件

| 文件 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | 完整工作流规范（Claude 读取） |
| [paradigms/](paradigms/) | 38个范式规范文件 |
| [references/config-schema.md](references/config-schema.md) | Config YAML schema + 9条验证规则 |
| [references/condition-file-generation.md](references/condition-file-generation.md) | 条件文件生成工具 |
| [references/data-recording.md](references/data-recording.md) | 数据输出列定义规范 |
| [references/randomization.md](references/randomization.md) | 随机化与平衡规范 |
| [references/timing.md](references/timing.md) | 计时与RT测量规范 |

## 使用示例

```
用户: "我想做一个点探测实验，情绪面孔配对（愤怒-中性），500ms呈现后探针出现，按f/j判断探针位置"

系统:
  Phase 1 → 识别范式(dot-probe)，确认平台(PsychoPy)，确认OS(macOS)，加载范式Must-Confirm
  Phase 2 → 构建窗口: Fixation(500ms) → FacePair(500ms) → Probe(until key, f/j)
             按键映射: f=左, j=右  |  rt_onset: Probe (split模式)
             准确性: key==correct_response
             → 展示Phase 2决策清单，user确认
  Phase 3 → 条件表: 情绪(愤怒/中性)×探针位置(左/右)×一致性(一致/不一致)
             → 展示Phase 3决策清单
  ... → 最终Gate 5全量审查 → 路由至代码生成
```
