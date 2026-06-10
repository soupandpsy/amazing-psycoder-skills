# 显著性标注 (Significance Annotation)

## 概述

在图表上添加统计检验结果(p值、显著性星号),使图表自带统计结论。常用`ggsignif`或`ggpubr`包。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 任何需要标注显著性的图表 |
| 标注 | p值 或 星号(*), 比较括号 |

## R 代码

```r
library(ggsignif)
ggplot(data, aes(x=condition, y=rt)) +
  geom_boxplot() +
  geom_signif(comparisons=list(c("congruent","incongruent")),
              map_signif_level=TRUE,  # 自动星号
              test="t.test", test.args=list(paired=TRUE)) +
  labs(title="Stroop Effect") + theme_minimal()

# 手动指定p值
geom_signif(comparisons=list(c("A","B")),
            annotations="p = .003",
            y_position=550)
```

## 星号惯例

| p值 | 星号 |
|-----|------|
| < .001 | *** |
| < .01 | ** |
| < .05 | * |
| ≥ .05 | ns |

## 关键参数

| 参数 | 作用 |
|------|------|
| `comparisons` | 比较对的列表 |
| `map_signif_level` | TRUE=自动星号, FALSE=手动p值 |
| `test` | 检验方法(t.test/wilcox.test) |
| `y_position` | 括号的Y坐标位置 |

## 解读

| p值 | 星号 |
|-----|------|
| <.001| *** |
| <.01 | ** |
| <.05 | * |
| ≥.05| ns |

## 注意事项

多个比较时注意括号位置避免重叠。被试内设计用paired=TRUE。
