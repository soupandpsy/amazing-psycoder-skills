# 独立 t 检验 (Independent Samples t-test)

## 概述

独立 t 检验用于比较两组独立样本的均值差异。在心理学中用于被试间设计。

**典型场景**：实验组 vs 控制组、A组 vs B组（不同被试）、不同人群比较。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 被试间 (between-subjects) |
| 条件数 | 恰好 2 个 |
| DV | 连续变量 |
| 数据要求 | 每组数据近似正态，方差齐或不齐 |

## 假设与检验

1. **独立性**：两组被试互相独立
2. **抽样分布/异常值**：结合设计、样本量、图形和影响诊断评估均值差推断是否稳健；分组 Shapiro p 值不是自动换方法的开关
3. **方差模型**：在分析计划中预先声明 Student 或 Welch；不要先用 Levene p 值再数据驱动选择检验

**Welch t-test 是默认推荐**：不假设方差齐性，自由度校正。大多数情况下 Welch 比 Student's t 更安全。

## 效应估计

优先报告原始均值差和置信区间；需要跨量表比较时再报告与方差模型一致的标准化均值差及区间。`d=.2/.5/.8` 不是跨构念通用的实质大小界线。

## R 代码

```r
# 独立 t 检验 - 完整分析流程

# 示例数据：实验组 vs 控制组
exp_group  <- c(88, 92, 85, 90, 87, 93, 89, 91, 86, 94, 90, 88)
ctrl_group <- c(78, 80, 82, 79, 81, 77, 83, 80, 78, 82, 79, 81)
n_exp  <- length(exp_group)
n_ctrl <- length(ctrl_group)

# 描述统计
cat(sprintf("实验组: M = %.2f, SD = %.2f, n = %d\n",
  mean(exp_group), sd(exp_group), n_exp))
cat(sprintf("控制组: M = %.2f, SD = %.2f, n = %d\n",
  mean(ctrl_group), sd(ctrl_group), n_ctrl))

# 1. 按预先声明的方差模型执行 Welch t 检验
t_result <- t.test(exp_group, ctrl_group, var.equal = FALSE)
cat(sprintf("\nWelch t-test:\n  t(%.2f) = %.3f, p = %.4f\n",
  t_result$parameter, t_result$statistic, t_result$p.value))
cat(sprintf("  均值差 = %.3f, 95%% CI [%.3f, %.3f]\n",
  t_result$estimate[1] - t_result$estimate[2],
  t_result$conf.int[1], t_result$conf.int[2]))

# 如 config 声明标准化估计，另用与目标总体和方差模型一致的标准化量及 CI。
```

## APA 7th 报告格式

> A Welch independent-samples t-test estimated a 70-ms mean difference between the experimental group (M=520, SD=95) and control group (M=450, SD=80), 95% CI [26, 114], t(approximately 57 df)=3.15, p=.003. Any standardized estimate should name its denominator and interval separately.

## 备选方法
- **Mann-Whitney U**: 当目标是分布/秩概率且其假设与设计相符；它不是“Shapiro 显著后的均值检验替代品”
- **Welch's ANOVA**: 三组+
