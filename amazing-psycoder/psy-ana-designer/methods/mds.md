# 多维标度法 (Multidimensional Scaling / MDS)

## 概述

MDS将高维相似性/距离数据降维到2D/3D空间,可视化对象间的"心理距离"。

**典型场景**: 8种情绪的相似性判断→2D情绪空间(valence × arousal); 面孔的知觉相似性→"面孔空间"。

## 何时使用

| 条件 | 要求 |
|------|------|
| 数据类型 | 距离矩阵或相似性矩阵 (n × n) |
| 测量水平 | Metric MDS需等距/等比数据; Non-metric MDS仅需顺序数据 |
| 样本要求 | 单个距离矩阵即可; INDSCAL需多个被试的矩阵 (建议≥10) |
| 关键假设 | Metric MDS: 距离满足三角不等式; Non-metric MDS: 单调变换下保持秩次关系 |
| 维度数 | k < n-1, 通常k=2或3以便可视化 |
| 适用情境 | 探索刺激空间结构、检验维度理论、品牌感知定位、心理距离可视化 |

## 类型

| 方法 | 输入 | 输出 |
|------|------|------|
| Metric MDS | 距离矩阵 | 坐标 |
| Non-metric MDS | 排序(相似度) | 坐标(保持秩次) |
| INDSCAL | 多个被试的距离矩阵 | 公共空间+个体权重 |

## R代码

```r
# 从相似性矩阵到2D坐标
fit <- cmdscale(dist_matrix, k=2)
plot(fit, type="n"); text(fit, labels=names)

# Non-metric MDS
library(MASS)
fit <- isoMDS(dist_matrix, k=2)
```

## 报告

APA 7th格式报告示例:

> 采用非计量多维标度法(Non-metric MDS)对8种情绪词的相似性评分矩阵进行分析。二维解的Stress值为0.06,表明模型拟合良好(Stress < 0.10)。维度1解释为"愉悦度"(Valence: 高负荷端为"快乐""满足",低负荷端为"愤怒""悲伤"),维度2解释为"唤醒度"(Arousal: 高负荷端为"愤怒""恐惧",低负荷端为"平静""困倦")。二维构形图呈现环状结构,与Russell(1980)的情绪环状模型一致。

**报告要素**: ①MDS类型(Metric / Non-metric / INDSCAL) ②距离/相似性输入与数据来源 ③解的维度和Stress值 ④各维度的命名、解释依据与典型刺激坐标 ⑤结果与理论预期或前人研究的对比。

## 评估

Stress值: <0.05优秀, <0.1好, <0.2尚可, >0.2差。

