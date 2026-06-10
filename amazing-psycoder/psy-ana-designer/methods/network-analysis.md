# 心理网络分析 (Network Analysis)

## 概述

网络分析将心理症状/行为建模为相互连接的节点网络,而非潜变量的外在表现。在精神病理学中广泛应用。

**典型场景**: 20个焦虑症状中哪些处于网络中心(最有影响力); 症状网络在治疗前后如何变化。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计类型 | 横截面设计为主;也可用于纵向数据(多时间点网络比较或时变网络) |
| 因变量类型 | 连续变量(症状评分、问卷条目得分、行为频率等) |
| 样本要求 | 被试数 > 节点数(变量数);通常 N ≥ 100 以保证网络稳定性;若节点数较多,建议 N ≥ 节点数×3 |
| 关键假设 | 观测变量满足多元正态性(高斯图模型);网络具有稀疏性(多数偏相关系数接近0,可经EBICglasso正则化处理);边仅反映条件依赖关系而非因果关系 |

## 核心概念

| 概念 | 含义 |
|------|------|
| 节点 | 观测变量(症状/行为/问卷条目) |
| 边 | 偏相关系数(控制所有其他节点) |
| 中心性 | 节点在网络中的重要性 |
| 稀疏化 | 去除弱边(EBICglasso / 阈值) |

## 中心性指标

| 指标 | 含义 |
|------|------|
| Strength | 该节点与其他节点的连接强度 |
| Betweenness | 该节点位于多少最短路径上(桥梁) |
| Closeness | 该节点与其他节点的平均距离 |

## R代码

```r
library(qgraph); library(bootnet)
network <- estimateNetwork(data, default="EBICglasso")
plot(network)
# 中心性
centralityPlot(network)
# Bootstrap稳定性
boot <- bootnet(network, nBoots=1000)
plot(boot, statistics="strength")
```

## 报告

### 简要报告

> A Gaussian graphical network estimated the anxiety symptom network (EBICglasso). "Worry" showed the highest strength centrality, suggesting it may be a promising intervention target. The network was stable (CS-coefficient=0.44).

### APA 7th 格式完整报告

**方法 (Method)**

> A Gaussian graphical model was estimated using the graphical LASSO (Least Absolute Shrinkage and Selection Operator) with Extended Bayesian Information Criterion (EBICglasso; tuning parameter γ = 0.5) for model selection (Epskamp & Fried, 2018). The network comprised 20 nodes representing individual anxiety symptoms from the Beck Anxiety Inventory (BAI). Edges represent regularized partial correlations between symptom pairs after conditioning on all other symptoms in the network.

**结果 (Results)**

> The estimated network is presented in Figure 1. Node strength centrality was calculated as the sum of absolute edge weights connected to each node. Bootstrap stability analysis with 1,000 iterations was conducted using the *bootnet* package (Epskamp et al., 2018) to evaluate the accuracy of edge weights and the stability of centrality indices. The correlation-stability (CS) coefficient for strength centrality was 0.44, exceeding the recommended threshold of 0.25 (indicating adequate stability). The node "Worry" (BAI item 1) exhibited the highest strength centrality (S = 1.24), suggesting it has the strongest direct connections to other symptoms in the network. "Fatigue" (BAI item 13; S = 1.08) and "Restlessness" (BAI item 3; S = 0.97) showed the next highest strength values, indicating these symptoms also occupy central positions in the anxiety symptom network.

## 注意事项

- 中心性的可解释性取决于网络的稳定性(CS-coefficient>0.25)
- 边≠因果关系——只是条件依赖
- 变量数>被试数时需谨慎——考虑正则化
