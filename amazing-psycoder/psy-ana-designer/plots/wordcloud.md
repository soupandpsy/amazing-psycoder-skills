# 词云 (Word Cloud)

## 概述

词云用字体大小表示词频,快速展示文本数据中最重要的词汇。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 文本数据频率展示 |
| 用途 | 定性摘要,非精确分析 |

## R 代码

```r
library(wordcloud2)
wordcloud2(data=word_freq, size=0.5, shape="circle",
           color="random-dark", backgroundColor="white")
```

## 关键参数

| 参数 | 作用 |
|------|------|
| `size` | 字体大小缩放 |
| `shape` | 形状(circle/cardioid/diamond) |
| `color` | 配色(random-dark/random-light) |
| `backgroundColor` | 背景色 |

## 解读

- 字号大=高频词
- 中心位置=更突出
- 配色区分词类

## 注意事项

不适合精确分析(人眼不擅长比较面积)。推荐只用于定性展示。中文需先分词(jieba包)。
