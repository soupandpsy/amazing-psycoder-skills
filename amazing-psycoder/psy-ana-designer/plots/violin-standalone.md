# 小提琴图 (Violin Plot)

## 概述

小提琴图展示数据分布的密度形状,旋转的核密度曲线=小提琴形状。比箱线图多一层分布信息,能揭示多峰和偏态。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 多组分布比较 |
| 优势 | 展示箱线图隐藏的多峰/偏态 |
| 组数 | 2-8组 |

## R 代码

```r
# 基础小提琴图
ggplot(data, aes(x=condition, y=rt, fill=condition)) +
  geom_violin(trim=FALSE, alpha=0.7) +
  scale_fill_viridis_d() +
  labs(title="RT Distribution by Condition", x="Condition", y="RT (ms)") +
  theme_minimal() +
  theme(legend.position="none")

# 小提琴+箱线图
ggplot(data, aes(x=condition, y=rt, fill=condition)) +
  geom_violin(trim=FALSE, alpha=0.7) +
  geom_boxplot(width=0.15, fill="white", outlier.shape=NA) +
  scale_fill_viridis_d() +
  labs(title="Violin + Boxplot", x="Condition") +
  theme_minimal()

# 小提琴+分位线
ggplot(data, aes(x=condition, y=rt, fill=condition)) +
  geom_violin(trim=FALSE, alpha=0.7,
              draw_quantiles=c(0.25, 0.5, 0.75)) +
  scale_fill_brewer(palette="Set2") +
  labs(title="Violin with Quartiles") +
  theme_minimal()

# 按第二个变量分组的镜像小提琴
ggplot(data, aes(x=condition, y=rt, fill=group)) +
  geom_violin(position=position_dodge(0.8), trim=FALSE, alpha=0.7) +
  scale_fill_brewer(palette="Set2") +
  labs(title="Violin by Condition and Group") +
  theme_minimal()
```

## 关键参数

| 参数 | 作用 | 建议 |
|------|------|------|
| `trim` | TRUE=尾端修剪到数据范围 | FALSE看完整密度 |
| `draw_quantiles` | 在小提琴内画分位线 | c(0.25,0.5,0.75) |
| `adjust` | 密度带宽乘数 | >1更平滑,<1更多细节 |
| `scale` | "area"/"count"/"width" | "count"让样本量不同的小提琴不同宽 |

## 解读

- 小提琴形状对称 → 近似正态
- 小提琴一端鼓 → 偏态
- 两个鼓包 → 双峰
- 两把小提琴不重叠 → 组间差异大
