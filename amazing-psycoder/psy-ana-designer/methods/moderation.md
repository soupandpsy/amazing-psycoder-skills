# 调节分析 (Moderation Analysis)

## 概述

调节分析检验第三个变量(W)是否改变X和Y之间关系的**强度或方向**。相当于"交互效应"。

**典型场景**: 压力(X)对任务表现(Y)的影响是否被社会支持(W)缓冲。社会支持是调节变量。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究问题 | 检验第三个变量是否改变X→Y关系的**强度**或**方向** |
| 自变量 (X) | 连续变量（也可以是分类变量） |
| 因变量 (Y) | 连续变量 |
| 调节变量 (W) | 连续变量或分类变量（如性别、实验条件） |
| 样本量 | N ≥ 100（检测中等交互效应）；每组/水平至少 50 |
| 核心假设 | 线性关系、残差独立性与正态性、方差齐性、无多重共线性 |
| 数据预处理 | 连续自变量和调节变量建议**中心化**后再计算乘积项 |
| 交互项显著性 | X×W 交互项显著是调节效应成立的前提 |

## 模型

```
        W (调节变量)
        │
X ──────→ Y
        
X×W ────→ Y  (交互项是关键)
```

- **交互项显著** → W调节X→Y的关系
- 交互项不显著 → W不调节

## 简单斜率分析 (Simple Slopes)

交互显著后必须做简单斜率:
- 在W的高值(+1SD)上: X对Y的效应?
- 在W的均值上: X对Y的效应?
- 在W的低值(-1SD)上: X对Y的效应?

## R代码

```r
library(interactions)
model <- lm(Y ~ X * W, data=data)  # X*W = X + W + X:W
summary(model)

# 简单斜率
sim_slopes(model, pred=X, modx=W)
interact_plot(model, pred=X, modx=W)
```

## 连续调节变量的可视化

Johnson-Neyman图: 显示X的效应在W的哪个区间显著。比±1SD的传统方法更精确。

## 报告格式

> A moderation analysis examined whether social support (W) moderated the effect of stress (X) on performance (Y). The interaction was significant, b=-0.25, t(96)=-3.12, p=.002. Simple slopes revealed that stress reduced performance under low support (b=-0.45, p<.001) but not under high support (b=-0.05, p=.42).

## 报告格式 (APA 7th)

调节分析采用层次回归（hierarchical multiple regression）检验 [W] 是否调节 [X] 与 [Y] 之间的关系。所有连续预测变量均已中心化处理以降低多重共线性。整体模型显著，*F*([df1], [df2]) = [F], *p* = [p], *R*² = [R²]。

[X] 与 [W] 的交互项显著，*b* = [b], *SE* = [SE], 95% CI [[LL], [UL]], *t*([df]) = [t], *p* = [p], Δ*R*² = [ΔR²]，表明 [W] 显著调节了 [X] 对 [Y] 的效应。

简单斜率分析（Aiken & West, 1991）显示：
- 低 [W] (-1 *SD*) 条件下，[X] 对 [Y] 的效应 [显著/不显著]，*b* = [b], *t*([df]) = [t], *p* = [p]；
- 均值 [W] 条件下，[X] 对 [Y] 的效应 [显著/不显著]，*b* = [b], *t*([df]) = [t], *p* = [p]；
- 高 [W] (+1 *SD*) 条件下，[X] 对 [Y] 的效应 [显著/不显著]，*b* = [b], *t*([df]) = [t], *p* = [p]。

上述结果表明，随着 [W] 的升高，[X] 对 [Y] 的效应 [增强/减弱/方向反转]。图 [X] 展示了调节效应的交互图与简单斜率。

## 常见错误

- ❌ 不做简单斜率直接报告"调节显著"——无法说明效应方向
- ❌ 连续变量未中心化就做乘积——导致多重共线性
- ❌ 交互不显著还强行做简单斜率
