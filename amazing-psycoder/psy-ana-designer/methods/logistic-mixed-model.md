# 逻辑混合模型 (Logistic Mixed Model / glmer)

## 概述

逻辑混合模型用于二分类因变量（正确/错误、是/否）。在心理学中主要用于**准确率分析**，尤其当数据接近天花板或地板时。

## 何时使用

| 条件 | 要求 |
|------|------|
| DV | 二分类 (0/1, 正确/错误) |
| 设计 | 被试内,需建模随机效应 |
| **必须用** | 任何条件准确率 >90% 或 <10% |

## 为什么不能用ANOVA做准确率

- 比例数据天然非正态（被约束在0-1之间）
- 接近天花板(~95%)时方差被严重压缩→ANOVA假阳性飙升
- 每个试次是0/1数据,逻辑模型直接建模概率,不是近似
- 方法学期刊(Psychonomic Bulletin & Review等)明确推荐

## 模型公式

```r
glmer(acc ~ condition + (1+condition|subject), 
      data=data, family=binomial,
      control=glmerControl(optimizer="bobyqa"))
```

## 效应量: Odds Ratio

OR = exp(fixef(model))。OR>1=概率增加, OR<1=概率降低。例如OR=1.5表示条件B下正确概率比条件A高50%。

## 当准确率在70-90%之间时

两个方法都可接受,但glmer更安全:
- 如果期刊对方法要求严格→glmer
- 如果领域惯例仍是ANOVA→用ANOVA但标注"比例数据,接近正态假设边界"

## 报告示例

> A logistic mixed model examined accuracy across conditions. The odds of correct response were significantly higher in congruent (95%) vs incongruent (88%) condition, OR=2.35, z=4.12, p<.001.
