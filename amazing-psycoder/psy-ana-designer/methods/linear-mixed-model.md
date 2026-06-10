# 线性混合模型 (Linear Mixed Model / lmer)

## 概述

线性混合模型（LMM）是被试内设计的**推荐首选方法**。相比传统t检验/ANOVA，它能利用全部试次数据（非均值化），自然处理不平衡设计和缺失数据，同时建模被试间随机变异。

**典型场景**：Stroop/Flanker/GoNoGo等被试内设计的RT分析。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 被试内或混合设计 |
| DV | 连续变量 |
| 数据要求 | 试次级数据（非已聚合），残差近似正态 |
| 优势 | 利用全部试次、处理不平衡、易扩展协变量 |

## 为什么优于t检验/ANOVA

| 维度 | t检验/ANOVA | LMM |
|------|-----------|-----|
| 数据利用 | 均值化→丢失试次间变异 | 全部试次参与建模 |
| 统计效力 | 低(被试数=数据点数) | 高(被试数×试次数) |
| 不平衡设计 | 困难 | 自动处理 |
| 协变量 | 需重新分析 | 公式加+即可 |
| 缺失数据 | 需排除被试 | FIML自动利用已有数据 |

## 随机效应结构

**推荐: (1+condition|subject)** — 随机截距+随机斜率。每个被试有自己的基线RT和条件效应。

收敛问题降级方案：
1. (1|subject)+(0+condition|subject) — 去掉相关性
2. (1|subject) — 仅随机截距
3. 换优化器: `lmerControl(optimizer="bobyqa")`

## 效应量

| 指标 | 公式 | 含义 |
|------|------|------|
| Marginal R² | 固定效应解释的方差比例 | 条件效应的独立贡献 |
| Conditional R² | 固定+随机效应解释的方差比例 | 整体模型拟合 |

## 报告格式

> A linear mixed model with condition as fixed effect and random intercepts and slopes by subject was fit. Condition significantly predicted RT, b=45.2, SE=8.3, t(29.0)=5.44, p<.001. Marginal R²=.18, Conditional R²=.72.

## 常见错误
- ❌ 只加随机截距(1|subject)不做随机斜率——当条件效应在被试间有差异时,假阳性膨胀
- ❌ 不检查收敛——奇异拟合时需降级
- ❌ 用lme4原生的p值——需lmerTest或car::Anova获取p值
- ❌ 用summary(model)$r.squared——不存在,用performance::r2()

## R 代码

```r
# 随机截距+随机斜率(推荐)
model <- lmer(rt ~ condition + (1 + condition | subject_id),
              data = data_rt, control = lmerControl(optimizer = "bobyqa"))
summary(model)

# 随机截距仅(收敛失败降级)
model <- lmer(rt ~ condition + (1 | subject_id), data = data_rt)
```
