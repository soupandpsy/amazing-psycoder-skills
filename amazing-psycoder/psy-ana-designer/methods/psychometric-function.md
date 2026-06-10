# 心理测量函数拟合

## 概述

心理测量函数描述刺激强度与检测/辨别概率的关系,用于估计**阈值**(75%正确对应的刺激强度)。是心理物理法的核心。

**典型场景**: 阶梯法中,拟合logistic/Weibull函数估计对比度阈值; 自适应阶梯(1-up-2-down等)收敛到70.7%正确。

## 何时使用

| 条件 | 要求 |
|------|------|
| 实验设计类型 | 心理物理法(阶梯法、恒定刺激法、自适应阶梯); 被试内或被试间设计均可 |
| 因变量类型 | 二分类变量(正确/错误、检测到/未检测到)或比例数据 |
| 样本量要求 | 每条件≥40试次(推荐); 每参与者通常需100–200试次以确保阈值稳定 |
| 关键假设 | (1)刺激强度与正确率呈单调递增关系; (2)试次间独立; (3)无显著疲劳或练习效应; (4)猜测率(lapse rate)可控或可在模型中参数化 |

## 常用函数

| 函数 | 参数 | 特点 |
|------|------|------|
| Logistic | α(阈值), β(斜率) | 最常用 |
| Weibull | α, β | 视觉心理物理 |
| Cumulative Gaussian | μ(阈值), σ(SD) | 信号检测框架 |

## R代码

```r
library(quickpsy)
fit <- quickpsy(data, x=stimulus_intensity, k=correct, n=total_trials,
                grouping=.(condition), fun=logistic_fun)
plot(fit)
# 提取阈值
fit$thresholds
```

## 报告

**APA 7th 格式报告示例**:

> Psychometric functions were fitted using a logistic function to estimate the contrast threshold at 75% correct for each condition. The congruent condition showed a significantly lower contrast threshold (α = 0.12, 95% CI [0.09, 0.15]) compared to the incongruent condition (α = 0.18, 95% CI [0.14, 0.22]), t(19) = 3.45, p = .003, Cohen's d = 0.77. The slope parameter did not differ between conditions (β_congruent = 1.12, β_incongruent = 1.08, p = .62). Goodness-of-fit was assessed by visual inspection of observed versus predicted proportions and the deviance statistic, which indicated acceptable fit (D = 12.34, p = .42).

> Psychometric functions (logistic) estimated the contrast threshold at 75% correct. The congruent condition showed a lower threshold (0.12) than incongruent (0.18), indicating better perceptual sensitivity.

**报告要点**: (1)说明拟合函数类型(logistic/Weibull等); (2)报告阈值与置信区间; (3)报告斜率(如相关); (4)报告拟合优度指标; (5)如有多条件,报告条件间比较的统计量。

## 注意事项

- 阶梯法的阈值估计依赖阶梯规则(如1-up-2-down→70.7%)
- 太少试次导致阈值估计不稳定(每条件>40试次推荐)
- 检查拟合优度: 预测-观测对比图
