# 等效性检验 (Equivalence Testing / TOST)

## 概述

等效性检验把零假设设为效应落在预先定义的等效区间之外，用于评估数据是否支持“效应小到在该领域可忽略”。它提供受误差率控制的证据，不是绝对证明两组相同。

**典型场景**: 评估新旧方法或两个实验版本的差异是否落入预先定义的实质等效范围。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计类型 | 两组独立样本或配对样本设计 |
| 因变量类型 | 连续变量（如反应时、正确率、量表得分） |
| 样本量要求 | 由等效边界、目标功效、方差、设计和失访决定；不能因样本少而事后放宽边界 |
| 关键假设 | 与所用估计器一致（配对/独立、方差模型、分布/稳健性）；等效边界必须在看结果前基于领域、测量和决策后果设定 |
| 等效边界设定参考 | 优先使用原始量纲上的最小重要差异或经验证的标准化边界；`d=.3/.5` 不是通用默认值 |

## TOST 逻辑

1. 设定等效边界 Δ(最小有意义效应,如 d=0.3)
2. 做两次单侧t检验:
   - H0a: 效应 ≥ +Δ → p1
   - H0b: 效应 ≤ -Δ → p2
3. p = max(p1, p2)。p<.05 → 等效

## 何时用

- 想检验数据是否支持“差异小于预先定义的重要边界”
- 比较新旧方法的双向等效；若问题仅是“不比旧方法差”，应设计非劣效检验而不是把它称为等效性检验
- 检验版间差异(实验版本A vs B)
- 操纵检验(确认IV操纵不影响无关变量)

## vs 传统检验

传统检验 p>.05 = “未拒绝点零假设”，不等于没有重要差异。只有当等效检验的置信区间/两侧检验都落入预先定义的边界时，数据才支持该边界下的等效结论。

## R代码

```r
library(TOSTER)
tsum_TOST(m1=520, m2=515, sd1=80, sd2=82, n1=30, n2=30,
          low_eqbound_d=-0.3, high_eqbound_d=0.3)
```

## 报告

APA 7th 格式报告范例:

> We conducted a two one-sided test (TOST) equivalence procedure to determine whether the difference between Version A and Version B fell within a pre-specified equivalence bound of d_z = ±0.3, corresponding to a raw mean difference of ±25 ms. The equivalence test was non-significant for the lower bound, t(58) = 1.21, p = .115, and significant for the upper bound, t(58) = -3.45, p < .001. The overall equivalence test was non-significant (p = .115), indicating that we could not reject the null hypothesis of non-equivalence — the observed mean difference of 5 ms (90% CI [-8.6, 18.6]) did not fall entirely within the equivalence bounds. Descriptively, reaction times were similar between Version A (M = 520 ms, SD = 80) and Version B (M = 515 ms, SD = 82), but the confidence interval exceeded the lower equivalence bound, precluding a conclusion of statistical equivalence.

要点:
- 报告等效边界 Δ 及其实质含义（如 d_z 和原始单位）
- 同时报告两个单侧检验的 t 值和 p 值
- 报告等效性检验的整体 p 值（取两个单侧检验 p 值中较大者）
- 报告 90% CI 而非 95% CI（TOST 使用 90% CI，等价于 α = .05 的双侧等效性检验）
- 报告描述统计（M, SD）便于读者评估实际差异大小
