# 可靠变化指数 (Reliable Change Index / RCI)

## 概述

RCI判断个体在前后测中的变化是否超出了测量误差的范围——即是"真实变化"还是"随机波动"。临床心理学中判断治疗是否有意义的**标准方法**。

**典型场景**: 治疗后焦虑分数从25降到18,7分的变化是真的改善还是测量误差?

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计类型 | 单组前后测设计（重复测量） |
| 因变量类型 | 连续变量（如量表得分、生理指标） |
| 样本要求 | 每个个体需有完整的前测和后测分数；需已知量表信度（Cronbach's α 或重测信度） |
| 关键假设 | 测量误差服从正态分布；前后测测量误差相互独立；信度估计准确且适用于当前样本 |

## 公式

RCI = (X_post - X_pre) / S_diff

其中 S_diff = √(2 × SE²), SE = SD × √(1-α)。α为信度系数(Cronbach's α)。

## 判断标准

- |RCI| > 1.96 → 可靠变化(p<.05)
- 可靠变化 + 跨越临床阈值 → 临床显著改善

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

> Reliable change index analysis examined whether individual pre- to posttreatment changes on the BAI exceeded measurement error. The standard error of the difference was *S*<sub>diff</sub> = 4.14, corresponding to a 95% CI critical threshold of ±8.11 BAI points. Among 30 completers, 18 (60.0%) showed reliable improvement (RCI < −1.96; mean pre–post change = 13.42, *SD* = 4.87), 10 (33.3%) exhibited no reliable change (|RCI| ≤ 1.96; mean change = 2.10, *SD* = 3.21), and 2 (6.7%) exhibited reliable deterioration (RCI > 1.96; mean change = −9.50, *SD* = 2.12). A chi-square goodness-of-fit test confirmed that the distribution across categories deviated significantly from chance, χ²(2, *N* = 30) = 13.87, *p* < .001. Of the 18 reliably improved patients, 14 (77.8%) also crossed the clinical cutoff (BAI < 16), thereby meeting Jacobson and Truax's (1991) criteria for clinically significant improvement.

**参考文献部分 (Reference)**

> Jacobson, N. S., & Truax, P. (1991). Clinical significance: A statistical approach to defining meaningful change in psychotherapy research. *Journal of Consulting and Clinical Psychology*, *59*(1), 12–19. https://doi.org/10.1037/0022-006X.59.1.12
