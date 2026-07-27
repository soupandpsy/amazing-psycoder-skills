# 可靠变化指数 (Reliable Change Index / RCI)

## 概述

RCI 用一个明确的测量误差模型判断个体前后变化是否大于该模型预期的误差。它是一种常见指标，但结论依赖信度来源、标准误公式、练习效应和参照样本；不能单独证明治疗因果效应或临床意义。

**典型场景**: 治疗后焦虑分数从25降到18,7分的变化是真的改善还是测量误差?

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计类型 | 单组前后测设计（重复测量） |
| 因变量类型 | 连续变量（如量表得分、生理指标） |
| 样本要求 | 每个个体需有完整的前测和后测分数；需已知量表信度（Cronbach's α 或重测信度） |
| 关键假设 | 所选标准误/信度模型适用；前后测误差相关、回归均值、练习效应和量表测量不变性已处理或明确作为限制 |

## 公式

RCI = (X_post - X_pre) / S_diff

经典 Jacobson–Truax 形式可写为 S_diff = √(2 × SE²), SE = SD × √(1-r)。这里的 `r` 必须是适合该用途和参照总体的信度估计；Cronbach's α 并不自动等同于重测误差模型。若考虑前后误差相关或练习效应，应使用相应公式/规范样本模型。

## 判断标准

- 在预先选定的双侧 95% 误差模型下，常用临界值是 |RCI| > 1.96；不同置信水平应使用对应临界值。
- “可靠变化”与“跨越临床界值”是不同条件；临床界值必须有目标人群和测量依据。

## R代码

```r
RCI <- (post_score - pre_score) / sqrt(2 * (SD_pooled * sqrt(1 - alpha))^2)
```

## 报告

> RCI analysis examined individual pre-post changes in anxiety. Of 30 patients, 18 (60%) showed reliable improvement (RCI< -1.96), 10 (33%) showed no reliable change, and 2 (7%) showed reliable deterioration (RCI>1.96).

### APA 7th 报告格式

**方法部分 (Method)**

> Individual-level change was evaluated using the reliable change index (RCI; Jacobson & Truax, 1991). The standard error of measurement was computed as *SE* = *SD* × √(1 − α), where *SD* is the pooled baseline standard deviation and α is the internal consistency (Cronbach's α) of the Beck Anxiety Inventory (BAI) in the current sample (α = .88). The standard error of the difference was then derived as *S*<sub>diff</sub> = √(2 × *SE*²). Participants were classified as reliably improved (RCI < −1.96), reliably deteriorated (RCI > 1.96), or showing no reliable change (|RCI| ≤ 1.96) based on the 95% confidence interval.

**结果部分 (Results)**

> Reliable change index analysis examined whether individual pre- to posttreatment changes on the BAI exceeded the prespecified measurement-error model. The standard error of the difference was *S*<sub>diff</sub> = 4.14, corresponding to a 95% critical difference of ±8.11 BAI points. Among 30 completers, 18 (60.0%) showed reliable improvement, 10 (33.3%) no reliable change, and 2 (6.7%) reliable deterioration. Of the 18 reliably improved patients, 14 (77.8%) also crossed the independently justified clinical cutoff. These classifications are descriptive of completers and do not by themselves identify a treatment effect.

**参考文献部分 (Reference)**

> Jacobson, N. S., & Truax, P. (1991). Clinical significance: A statistical approach to defining meaningful change in psychotherapy research. *Journal of Consulting and Clinical Psychology*, *59*(1), 12–19. https://doi.org/10.1037/0022-006X.59.1.12
