# 漏斗图 (Funnel Plot)

## 概述

漏斗图是元分析中检测发表偏倚的标准工具。X轴=效应量,Y轴=标准误(或样本量)。小样本研究散布在底部,大样本研究集中在顶部。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 元分析发表偏倚检测 |
| 数据 | 每个研究的效应量+SE |

## R 代码

```r
library(metafor)
res <- rma(yi=yi, sei=sei, data=dat)
funnel(res, main="Funnel Plot")
# Egger's regression test
regtest(res)
```

## 解读

- 对称漏斗 → 无发表偏倚
- 不对称(左下角空白) → 小样本阴性结果可能未发表
- Egger检验 p<.05 → 显著不对称

## 关键参数

| 参数 | 作用 |
|------|------|
| `main` | 标题 |
| `level` | 漏斗边界置信水平 |
