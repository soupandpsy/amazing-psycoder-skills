# 置换检验 (Permutation Test)

## 概述

置换检验是非参数方法的一种,通过随机打乱数据标签来构建零分布的抽样分布,不假设任何理论分布。

**典型场景**: 小样本被试内设计(n<15)且怀疑正态性假设不可靠; 使用非标准统计量时没有现成的参数检验。

## 何时使用

| 条件 | 要求 |
|------|------|
| 实验设计类型 | 被试内设计、被试间设计均可，尤其适合被试内配对设计 |
| 因变量类型 | 连续变量（如反应时、正确率、评分） |
| 样本量要求 | 小样本（n < 20），尤其 n < 15 时参数检验正态性假设难以验证 |
| 关键假设 | 零假设下观测值的可交换性（exchangeability）；不依赖正态性或任何理论分布 |
| 统计量类型 | 可使用任意自定义统计量（均值差、中位数差、trimmed mean 等），不限于标准检验统计量 |

## 优势

- 不假设分布
- 适用于任何自定义统计量
- 小样本下更可靠
- 精确p值(非渐近)

## R代码

```r
# 简单置换: 配对设计
observed_diff <- mean(condA - condB)
n_perms <- 10000
perm_diffs <- replicate(n_perms, {
  sign_flip <- sample(c(-1,1), length(condA), replace=TRUE)
  mean((condA - condB) * sign_flip)
})
p_value <- mean(abs(perm_diffs) >= abs(observed_diff))
```

## 何时用

- n < 20 且不能假设正态
- 使用非标准统计量(如中位数差)
- 作为补充: 报告置换p值和参数p值,两者一致→结论稳健

## 报告

APA 7th 格式报告示例（被试内配对设计，10,000次置换）：

> 采用置换检验（10,000次置换）比较条件A（*M* = 350 ms, *SD* = 45 ms）与条件B（*M* = 320 ms, *SD* = 40 ms）的反应时差异。结果显示条件A的反应时显著高于条件B，*p* = .023（置换检验，双尾）。观测到的均值差为 30 ms，95% CI [10, 50]（基于 bootstrap 百分位法）。

英文对照：

> A permutation test (10,000 permutations) was conducted to compare reaction times between Condition A (*M* = 350 ms, *SD* = 45 ms) and Condition B (*M* = 320 ms, *SD* = 40 ms). Results indicated that reaction times in Condition A were significantly higher than in Condition B, *p* = .023 (permutation test, two-tailed). The observed mean difference was 30 ms, 95% CI [10, 50] (based on bootstrap percentile method).

报告要点：
- 明确说明置换次数（如 10,000 次）
- 报告观测到的效应量和置换 *p* 值
- 注明单尾/双尾
- 若使用 bootstrap 计算置信区间，应说明方法
- 建议同时报告参数检验结果作为参照，两者一致则结论更稳健

## 局限

- 计算密集(n=10000时需几秒)
- 不能直接给CI(需bootstrap)

