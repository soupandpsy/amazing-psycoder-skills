# 弦图 (Chord Diagram)

## 概述

弦图展示节点之间的流向和关系。外环=节点,内弦=流向,弦宽=流量大小。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 组间流向/转换关系 |
| 数据 | 方阵(从→到的流量) |

## R 代码

```r
library(circlize)
chordDiagram(mat, transparency=0.5,
             annotationTrack="grid",
             preAllocateTracks=list(track.height=0.1))
circos.track(track.index=1, panel.fun=function(x,y) {
  circos.text(CELL_META$xcenter, CELL_META$ylim[1],
              CELL_META$sector.index, facing="clockwise",
              adj=c(-0.1,0.5), cex=0.8)
}, bg.border=NA)
```

## vs 网络图 vs Sankey

- 弦图=圆形流向图,适合方阵数据
- 网络图=节点+边,适合无向关系
- Sankey(冲积图)=线性流向,适合阶段转换

## 关键参数

| 参数 | 作用 |
|------|------|
| `transparency` | 弦透明度(0-1) |
| `annotationTrack` | 外环标签样式 |
| `grid.col` | 扇区颜色 |
