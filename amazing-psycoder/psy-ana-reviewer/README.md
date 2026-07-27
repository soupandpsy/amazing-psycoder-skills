# psy-ana-reviewer — 分析审计层

> **版本**: v1.4.0 | 审计分析设计、脚本或已执行结果；不直接修改代码。

## 审查模式与证据上限

| 模式 | 最低输入 | 最大标签 |
|------|----------|---------|
| `plan-review` | `analysis_config.yaml` | `analysis_plan_ready` |
| `analysis-audit` | config + 完整脚本 + 数据 schema | `ready_for_execution` |
| `result-audit` | 上述材料 + clean execution log + 生成的表/图 + 环境信息 | `ready_for_publication` |
| `triage-only` | 研究问题/错误描述 | 缺失信息与风险清单 |
| `blocked` | 无法判断范围或缺少关键输入 | `blocked` |

静态审查通过只表示脚本可以进入执行验证，不能证明结果正确或可发表。`ready_for_publication` 必须有成功执行和结果审查证据。

## 核心审计

- 研究问题、estimand、观测层级与模型公式一致；重复测量、项目和会话依赖未被忽略。
- 变量类型与似然/链接函数匹配；重复二元数据不能把普通 `statsmodels.Logit()` 标成 GLMM。
- 排除、缺失、变换和派生变量均有来源、理由、计数与敏感性策略。
- 诊断针对实际模型；不机械要求所有模型做 Shapiro 检验。
- 每个实质性结论由目标效应估计与不确定性支持，而非仅报告 p 值或 R²。
- 随机种子只在随机过程存在时要求；始终记录包/运行环境和输入输出清单。
- 结果审查核对执行日志、样本流转、表图数值、警告/收敛、方向和单位。

## 严重性

| 级别 | 判定依据 |
|------|----------|
| **Critical** | 会改变主要结论、使用错误数据/模型，或结果无法追溯 |
| **Major** | 可能实质影响估计/不确定性/重复性，发表前必须解决 |
| **Minor** | 不改变实质结论的清晰度、维护性或文档问题 |

## 最小输出

报告必须包含：审查模式、审查范围、证据状态、就绪标签、按严重性分组且带文件/稳定定位的发现、每项修复路径，以及仍未验证的事项。

完整工作流见 [SKILL.md](SKILL.md)；平台清单见 [R checklist](r/checklist/README.md) 与 [Python checklist](python/checklist/README.md)。
