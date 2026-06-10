# 等效性检验 (Equivalence Testing / TOST)

## 概述

等效性检验翻转传统假设检验的逻辑:零假设是"效应足够大(≥Δ)",备择假设是"效应可忽略(<Δ)"。用于**证明**两组没有有意义的差异。

**典型场景**: 证明新方法和旧方法效果相同; 证明两个实验版本没有差异。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计类型 | 两组独立样本或配对样本设计 |
| 因变量类型 | 连续变量（如反应时、正确率、量表得分） |
| 样本量要求 | 每组 ≥ 30（独立样本）；总对数 ≥ 30（配对样本）；样本量过小时等效边界需放宽 |
| 关键假设 | 1) 数据服从正态分布（或大样本下近似正态）；2) 两组方差齐性（独立样本 t 检验时）；3) 等效边界 Δ 需在研究前基于领域知识预先设定（非数据驱动） |
| 等效边界设定参考 | 最小有意义效应量：Cohen's d = ±0.3（小效应）或 ±0.5（中等效应），具体根据研究领域惯例确定 |

## TOST 逻辑

1. 设定等效边界 Δ(最小有意义效应,如 d=0.3)
2. 做两次单侧t检验:
   - H0a: 效应 ≥ +Δ → p1
   - H0b: 效应 ≤ -Δ → p2
3. p = max(p1, p2)。p<.05 → 等效

## 何时用

- 想证明"没有差异"
- 比较新旧方法(只需证明不比旧的差)
- 检验版间差异(实验版本A vs B)
- 操纵检验(确认IV操纵不影响无关变量)

## vs 传统检验

传统检验p>.05 = "不拒绝H0" ≠ "H0成立"。等效性检验正面确证"效应<Δ"。

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
