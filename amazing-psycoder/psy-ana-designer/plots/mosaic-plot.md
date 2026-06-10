# 马赛克图 (Mosaic Plot)

## 概述

马赛克图用矩形面积表示分类变量交叉表的频数。矩形越大=该组合越多。适合展示两个或多个分类变量的关系。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 2-3个分类变量的交叉表 |
| 优势 | 面积直观展示频数,标准残差着色 |

## R 代码

```r
library(vcd)
mosaic(~ condition + error_type, data=data,
       shade=TRUE, legend=TRUE,
       labeling_args=list(set_varnames=c(condition="Condition",
                                          error_type="Error Type")))
```

## 解读

- 矩形面积=该组合的观测数
- 蓝色=观测>期望(正残差)
- 红色=观测<期望(负残差)
- 颜色越深=偏离期望越远

## 关键参数

| 参数 | 作用 |
|------|------|
| `shade=TRUE` | 残差着色(蓝=多于期望,红=少于) |
| `legend=TRUE` | 显示残差图例 |
