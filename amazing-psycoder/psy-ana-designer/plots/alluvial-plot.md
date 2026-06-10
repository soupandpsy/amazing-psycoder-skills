# 冲积图 (Alluvial/Sankey Plot)

## 概述

冲积图展示分类数据在多个时间点或阶段之间的流动变化。适合纵向追踪中的类别转换。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 纵向分类数据(诊断变化、阶段转换) |
| 变量 | 2-4个分类时间点 |

## R 代码

```r
library(ggalluvial)
ggplot(data, aes(axis1=time1, axis2=time2, axis3=time3,
                 y=count)) +
  geom_alluvium(aes(fill=time1), width=0.3) +
  geom_stratum(width=0.3, fill="grey90", color="grey40") +
  geom_text(stat="stratum", aes(label=after_stat(stratum))) +
  scale_x_discrete(limits=c("Time1","Time2","Time3")) +
  labs(title="Diagnostic Category Changes", y="Count") +
  theme_minimal()
```

## 解读

- 流带宽度=类别转换人数
- 流带颜色一致=大多数人在同一类别
- 流带分散=类别转换多
- 窄带→少数人发生该转换

## 关键参数

| 参数 | 作用 |
|------|------|
| `aes(axis1,axis2,...)` | 各时间点的分类变量 |
| `fill` | 流带颜色映射 |
| `width` | 流带和柱体的宽度(0.1-0.4) |
