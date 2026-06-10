# 多重插补 (Multiple Imputation / MICE)

## 概述

多重插补是处理缺失数据的**推荐标准方法**。创建多个(通常m=5-20)完整数据集,分别分析后合并结果,正确反映缺失数据引入的不确定性。

**典型场景**: 20%被试在某些试次缺失RT; 某些被试未完成全部问卷; 纵向研究中被试流失。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 实验设计、准实验设计、纵向研究、问卷研究等含缺失数据的各类设计均适用 |
| 因变量类型 | 连续变量（RT、得分等，最常见）、二分类变量、有序分类变量、计数变量 |
| 样本量要求 | 至少需有部分完整观测案例（完整案例数 ≥ 变量数 × 5）；缺失比例单变量不宜超过 50% |
| 关键假设 | **MAR**（Missing at Random，随机缺失）：缺失仅依赖于已观测数据，不依赖于缺失值本身；**插补模型需包含分析模型中所有变量**（包括交互项和因变量）；可引入辅助变量提高插补精度 |

## 为什么不是成列删除

- 成列删除: 丢弃任何含缺失的行 → 偏差(如果缺失非随机) + 效力损失
- 均值插补: 低估标准误 → 假阳性膨胀
- 多重插补: 正确反映不确定性 → 无偏估计

## MICE 流程

1. 创建 m 个插补数据集 (m=5-20)
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

> Missing data were handled using multiple imputation by chained equations (MICE; van Buuren & Groothuis-Oudshoorn, 2011). The overall proportion of missing data was 12%, primarily from incomplete experimental trials and occasional questionnaire non-response. Little's (1988) MCAR test was not significant, χ²(45) = 52.3, p = .213, consistent with a missing-at-random (MAR) mechanism. Ten imputed datasets (m = 10) were generated via predictive mean matching (PMM) with 50 iterations per dataset. All analysis model variables (condition, baseline scores, age, gender) were included in the imputation model, along with auxiliary variables (trial order, session number) to improve imputation quality. Parameter estimates were pooled across imputed datasets using Rubin's (1987) rules. Pooled results indicated a significant effect of condition, b = 45.2, 95% CI [38.1, 52.3], t(152.4) = 12.6, p < .001, Cohen's d = 0.68. A sensitivity analysis using listwise deletion yielded substantively identical results (b = 43.8, 95% CI [36.2, 51.4]), supporting the robustness of the findings.
