# Ex-Gaussian 分布拟合

## 概述

Ex-Gaussian（指数修正高斯）是描述右偏 RT 分布的一种候选分布，常用参数对应高斯位置/尺度与指数尾部尺度。参数是分布描述，不应在没有过程模型或外部证据时直接命名为“决策速度”“稳定性”或“注意 lapse”，也不是所有 RT 问题的黄金标准。

**典型场景**: ADHD研究中,高τ值(更多的极端慢反应)是核心行为标记,而μ和σ可能与对照组无差异。

## 何时使用

| 条件 | 要求 |
|------|------|
| 实验设计 | 被试间或被试内设计;需至少两组或两个条件进行比较 |
| 因变量类型 | 反应时(RT),连续正数变量,单位通常为毫秒 |
| 样本信息 | 由层级结构、尾部信息、效应大小和估计器决定；用参数恢复/设计模拟评估，不设通用试次数/被试数门槛 |
| 关键检查 | 分布支持与任务 RT 相容；与 lognormal/shifted-lognormal/过程模型等候选做预测检查；核验收敛、参数恢复和对预先声明清理规则的敏感性，不自动加入固定 RT/SD 剔除 |

## 三个参数

| 参数 | 心理学解释 | 典型值(ms) |
|------|-----------|----------|
| μ (mu) | 高斯成分的位置参数；心理过程解释需额外证据 | 由任务/单位/模型估计 |
| σ (sigma) | 高斯成分的尺度参数 | 由任务/单位/模型估计 |
| τ / beta | 指数成分的尺度/均值参数（名称依实现） | 由任务/单位/模型估计 |

## 为什么用Ex-Gaussian

均值/中位数不能完整描述分布形状；Ex-Gaussian 可把位置、尺度与右尾差异参数化。但不同生成过程可能产生相似参数，分布参数差异不能单独识别“走神”等潜在认知过程。

## R代码

```r
library(brms)
# 仅示意：公式、先验、清理和随机结构必须来自已确认 config。
fit <- brm(
  bf(
    rt ~ condition + (1 + condition | subject_id),
    sigma ~ condition,
    beta ~ condition
  ),
  data = data,
  family = exgaussian(),
  prior = confirmed_priors,
  seed = confirmed_seed
)
summary(fit)
pp_check(fit)
# 还需检查 R-hat/ESS、发散、后验预测与预先声明的候选分布敏感性。
```

## 报告格式 (APA 7th)

**方法部分**:

> Trial-level RTs were modeled with a hierarchical Ex-Gaussian distribution in the pinned `brms` environment. The Gaussian location/scale and exponential-component parameterization followed the documented package version. Cleaning rules were prespecified in the analysis config; no generic fixed-RT or within-cell SD rule was added. The model represented subject/item dependence declared by the design. We reported parameter contrasts with posterior intervals, R-hat/ESS and divergence diagnostics, posterior-predictive checks, and a prespecified comparison with viable alternative RT distributions.

**结果部分**:

> The fitted groups differed primarily in the model's exponential-tail parameter, while location and Gaussian-scale contrasts were smaller and less precise. Posterior-predictive checks showed where the Ex-Gaussian captured or missed each group's RT distribution. These are distributional differences; labeling the tail contrast as attentional lapses or the location contrast as decision speed would require independent process-level evidence.

**表格建议**:

| 参数 | 声明的组间/条件对比 | 区间 | 模型/预测诊断 |
|------|--------------------|------|---------------|
| μ / location | estimate | 95% CrI/CI | R-hat/ESS + posterior predictive fit |
| σ | estimate | 95% CrI/CI | R-hat/ESS + posterior predictive fit |
| beta / exponential scale | estimate | 95% CrI/CI | R-hat/ESS + tail predictive fit |

> *Note.* State the package parameterization and link functions explicitly; `tau` and `beta` names are not interchangeable without checking the implementation. Report participant/trial denominators after cleaning and avoid two-stage individual fitting when the confirmed hierarchical estimand requires joint partial pooling.
