# 多重插补 (Multiple Imputation / MICE)

## 概述

多重插补是在可辩护的缺失机制和兼容插补模型下处理缺失数据的候选方法。创建多个插补数据集、分别分析并按相应合并规则传播插补不确定性；它不是所有缺失问题的自动默认方案。

**典型场景**: 20%被试在某些试次缺失RT; 某些被试未完成全部问卷; 纵向研究中被试流失。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 实验设计、准实验设计、纵向研究、问卷研究等含缺失数据的各类设计均适用 |
| 因变量类型 | 连续变量（RT、得分等，最常见）、二分类变量、有序分类变量、计数变量 |
| 信息要求 | 根据样本结构、缺失模式/比例、变量支持集、插补模型复杂度与 Monte Carlo 误差设计；不使用固定“完整案例×变量数”或 50% 门槛代替诊断 |
| 关键假设 | **MAR**（Missing at Random，随机缺失）：缺失仅依赖于已观测数据，不依赖于缺失值本身；**插补模型需包含分析模型中所有变量**（包括交互项和因变量）；可引入辅助变量提高插补精度 |

## 为什么不是成列删除

- 成列删除: 丢弃任何含缺失的行 → 偏差(如果缺失非随机) + 效力损失
- 均值插补: 低估标准误 → 假阳性膨胀
- 多重插补: 在插补/分析模型兼容且缺失假设可辩护时传播插补不确定性；不能保证无偏

## MICE 流程

1. 通过 Monte Carlo 误差/稳定性诊断选择足够的插补数据集数量，而不是固定套用 `m=5-20`
2. 每个数据集独立分析
3. Rubin's rules 合并结果(估计+SE+CI)

## R代码

```r
library(mice)
imp <- mice(data, m=10, method="pmm", seed=2024)
fit <- with(imp, lmer(rt ~ condition + (1|subject)))
pool(fit)
```

## 报告

### 简要示例

> Missing data (12% of trials) were handled with multiple imputation (m=10, MICE). Pooled results showed a significant condition effect, b=45.2, 95%CI [38.1,52.3], p<.001. Sensitivity analysis with listwise deletion yielded consistent results (b=43.8).

### APA 7th 完整报告格式

> Missing data were handled using multiple imputation by chained equations under a prespecified MAR assumption justified from the data-collection process and observed predictors of missingness. The imputation model included all analysis-model terms plus declared auxiliary variables, respected variable supports and the multilevel structure, and was checked with trace/distribution/convergence diagnostics. The number of imputations was selected to make Monte Carlo error acceptably small. Estimates and uncertainty were pooled using rules compatible with the fitted analysis, and sensitivity analyses examined departures from the MAR assumption. Little's MCAR test was not used to claim MAR, because a non-significant MCAR test does not establish that mechanism.
