# psy-ana-reviewer — 分析代码审计层

> **版本**: v1.3 | **角色**: 对分析脚本进行统计正确性和可重复性审计，输出问题分级报告 + 就绪标签。不修改代码。amazing-psycoder 子技能。

## 一句话说明

输入分析脚本 + 数据，审计统计方法是否正确、结果是否可重复，标注就绪状态。

## 4 种审查模式

| 模式 | 输入 | 最大标签 |
|------|------|---------|
| `analysis-audit` | 完整分析脚本 + 数据 | `ready_for_publication` |
| `plan-review` | 分析 config YAML | `analysis_plan_ready` |
| `triage-only` | 研究问题描述 | 缺失信息清单 |
| `blocked` | 输入不足 | 说明需要什么 |

## 就绪标签

| 标签 | 含义 |
|------|------|
| `ready_for_publication` | 零 Critical + 零 Major |
| `ready_after_minor_fixes` | 仅 Minor 问题 |
| `not_ready` | 存在 Critical 或 Major |
| `analysis_plan_ready` | 分析设计完成，可生成代码 |

## 严重性分级

| 级别 | 定义 |
|------|------|
| **Critical** | 结果无效，必须修复 |
| **Major** | 降低可重复性，发表前修复 |
| **Minor** | 不影响正确性，方便时修复 |

## 审计维度

### 统计正确性
- 模型匹配设计类型（被试内→paired/lmer，被试间→ind t/aov）
- 随机效应结构合理
- 效应量类型正确
- 多重比较已校正

### 可重复性
- seed 已设
- sessionInfo / pip freeze 输出
- 排除日志完整（每步数量+原因）
- 无硬编码路径

### 假设检验
- 正态性已验证，违规有备选
- 方差齐性已验证（被试间）
- 球对称已验证（被试内>2水平）

### 图表质量
- 误差线已定义（SE/CI）
- 个体数据可见（被试内设计）
- 坐标轴标签清晰

## 平台反模式清单

每平台独立维护：

| 平台 | 检查清单 |
|------|---------|
| R | [r/checklist/README.md](r/checklist/README.md) — 12项Quality Gate + 9项反模式grep |
| Python | [python/checklist/README.md](python/checklist/README.md) — 12项Quality Gate + 9项反模式grep |

## 输出格式

```
## 审计模式: analysis-audit
## 就绪标签: ready_for_publication / not_ready
## Critical Issues: (如有)
## Major Issues: (如有)
## Minor Issues: (如有)
## 总体判断: 1-2句总结
```

## 关键文件

| 文件 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | 完整审计工作流规范 |
| [r/checklist/README.md](r/checklist/README.md) | R 平台独立审计清单（12项Gate + grep模式） |
| [python/checklist/README.md](python/checklist/README.md) | Python 平台独立审计清单（12项Gate + grep模式） |
| [../psy-ana-coder/r/spec/README.md](../psy-ana-coder/r/spec/README.md) | Coder R API规范 + 15项反模式（参考） |
| [../psy-ana-coder/python/spec/README.md](../psy-ana-coder/python/spec/README.md) | Coder Python API规范 + 12项反模式（参考） |
