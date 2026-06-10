# 重复测量相关 (Repeated Measures Correlation / rmcorr)

## 概述

rmcorr 用于计算被试内重复测量数据中两个变量的相关,解决了普通Pearson r在处理每个被试多行数据时的独立性违反问题。

**典型场景**: RT与trial序号的被试内关联, 每个trial的刺激强度与RT的关联。

## 何时使用

| 条件 | 要求 |
|------|------|
| 实验设计类型 | 被试内设计 (within-subject design)，每个被试在多个条件下重复测量 |
| 因变量类型 | 两个变量均为连续变量 (continuous) |
| 自变量类型 | 连续变量 (continuous) 或可视为连续的离散变量 |
| 最低样本量 | 每个被试至少 2 次重复测量；总被试数建议 ≥ 20，总观测数建议 ≥ 60 |
| 数据层级 | 两水平嵌套数据：重复测量 (Level 1) 嵌套于被试 (Level 2) |
| 核心假设 | (1) 线性关系：两变量在被试内呈线性关系；(2) 残差正态性；(3) 方差齐性 (homoscedasticity)；(4) 各被试的斜率方向一致（rmcorr 估计共同斜率，不适用于被试间方向相反的情况） |
| 不适用情形 | 被试间斜率方向不一致（应使用混合模型或个体回归）；数据有非线性趋势；两个变量中任一为分类变量 |

## 为什么不能用普通Pearson r

被试内数据(每人60个trial):
- Pearson r 把 30人×60=1800行当成独立观测 → 假阳性膨胀
- 均值化(每被试一个r)→丢失被试内信息
- rmcorr: 用ANCOVA去除被试间差异,只分析被试内的共变

## R代码

```r
library(rmcorr)
rmcorr(participant = subject_id, measure1 = rt, measure2 = trial_number, dataset = data)
```

## 输出

- r_rm: 重复测量相关系数(解释同Pearson r)
- p值
- 95% CI
- 个体拟合线图(ggplot)

## 报告格式 (APA 7th)

**中文报告模板**：

> 采用重复测量相关 (repeated measures correlation, rmcorr) 检验反应时 (RT) 与试次序号 (trial number) 的被试内关联。结果表明两者存在显著的负相关，*r*~rm~(1428) = -.28, *p* < .001, 95% CI [-.33, -.23]，说明随实验进程推进，被试的反应时逐渐下降。

**英文报告模板**：

> A repeated measures correlation (rmcorr) was conducted to examine the within-subject association between reaction time (RT) and trial number. The results revealed a significant negative correlation, *r*~rm~(1428) = -.28, *p* < .001, 95% CI [-.33, -.23], indicating that RT decreased as the experiment progressed.

**报告要点**：
- 报告 *r*~rm~ 值、自由度（总观测数 − 被试数）、*p* 值和 95% 置信区间。
- 自由度计算公式：*df* = *N* − *k*，其中 *N* 为总观测行数，*k* 为被试数。
- 效应量解释：|*r*~rm~| ≈ .10 为小效应，≈ .30 为中等效应，≈ .50 为大效应（与 Pearson *r* 相同）。
