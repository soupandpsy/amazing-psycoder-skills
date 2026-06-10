# 雷达图 (Radar/Spider Chart)

## 概述

雷达图在多个轴上展示多变量数据,每个轴代表一个变量。适合展示个体或群体的多维度剖面。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 多变量剖面比较(如3+认知任务的标准化分数) |
| 变量 | 3-10个连续,需标准化到同一尺度 |

## R 代码

```r
library(fmsb)
# 数据需包含max/min行定义轴范围
radar_data <- rbind(rep(1,5), rep(0,5), profile_data)
radarchart(radar_data, axistype=1,
           pcol=rgb(0.2,0.5,0.5,0.9), pfcol=rgb(0.2,0.5,0.5,0.3),
           plwd=2, cglcol="grey", cglty=1, axislabcol="grey",
           caxislabels=seq(0,1,0.25), cglwd=0.8, vlcex=0.8)
```

## 解读

- 多边形面积大=整体表现好
- 某轴突出=该维度强
- 两组多边形重叠少=组间剖面差异大
- 需标准化变量到同一尺度(如Z-score)

## 注意

- >10个变量时图形拥挤,难解读
- 轴顺序影响视觉印象
- 不适合展示绝对量(用平行坐标替代)
