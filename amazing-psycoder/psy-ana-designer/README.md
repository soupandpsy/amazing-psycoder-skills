# psy-ana-designer

> v1.3 | 读实验 config → 5 阶段渐进确认 → 分析 config YAML。不生成代码。amazing-psycoder 子技能。

## 工作流

| Phase | 内容 | Gate 通过条件 |
|------|------|-------------|
| 1. 理解实验 | 读 config,提取 IV/DV/设计,确认科学问题 | 每个 DV 有明确科学问题 |
| 2. 理解数据 | 确认列名、格式、设计矩阵 | 变量映射表+设计类型确认 |
| 3. 匹配方法 | 确认数据特点 → 12维度比较 A vs B → 用户选择 | 方法已选+附比较理由+多重比较确认 |
| 4. 分析细节 | 清洗标准、缺失策略、效应量、图表类型 | 全部确认,默认值标 ⚠️ |
| 5. 最终审查 | 分析决策注册表全量展示,用户逐项确认 | Gate 5 通过 → 路由到 coder |

**核心机制**: 分析决策注册表(来源追踪) · 12维度方法比较 · 阶段决策清单 · 默认项⚠️标记

## 分析方法库

60 个方法，designer 在 Phase 3 根据实验设计自动匹配候选，按 12 维度比较 A vs B。

### 基础组间比较

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [配对t检验](methods/paired-t-test.md)（Paired t-test）| Stroop一致vs不一致RT | 连续 · 被试内 · 2组 | 差值正态→t;非正态→Wilcoxon |
| [独立t检验](methods/independent-t-test.md)（Independent t-test）| 实验组vs对照组 | 连续 · 被试间 · 2组 | 默认Welch(不假设方差齐) |
| [被试内ANOVA](methods/oneway-anova-within.md)（One-way RM ANOVA）| 3种难度RT比较 | 连续 · 被试内 · 3+组 | 球对称→GG校正;事后必校正 |
| [被试间ANOVA](methods/oneway-anova-between.md)（One-way ANOVA）| 3年龄组Stroop比较 | 连续 · 被试间 · 3+组 | 方差齐→常规;不齐→Welch |

### 进阶模型

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [线性混合模型](methods/linear-mixed-model.md)（Linear Mixed Model）| 被试内RT,需利用全部试次 | 连续 · 被试内/混合 | **推荐首选**:全试次+随机效应,效力>ANOVA |
| [逻辑混合模型](methods/logistic-mixed-model.md)（Logistic GLMM）| 准确率分析,天花板/地板时 | 二分类 · 被试内 | **天花板时强制用**:ANOVA方差压缩致假阳性 |
| [Gamma混合模型](methods/gamma-mixed-model.md)（Gamma GLMM）| RT严重右偏,对数转换无效 | 连续(右偏) · 被试内 | 自然处理偏态,乘法效应(RT比率) |
| [两因素被试内ANOVA](methods/factorial-anova-within.md)（Two-way RM ANOVA）| 2×2 Stroop(一致×SOA) | 连续 · 被试内 · 2因素 | 交互显著→简单效应;lmer替代更灵活 |
| [混合ANOVA](methods/mixed-anova.md)（Mixed ANOVA）| 组别(被试间)×条件(被试内) | 连续 · 混合设计 | 组×条件交互是核心 |
| [交叉随机效应](methods/crossed-random-effects.md)（Crossed Random Effects）| 被试×刺激双随机(语言/面孔) | 连续 · 被试+项目 | 心理语言学标准;避免假阳性膨胀 |
| [广义估计方程](methods/gee.md)（GEE）| 需总体平均效应,非个体预测 | 连续/二分类 · 被试内 | 混合模型替代;glmer不收敛时备选 |

### 相关与分类

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [Pearson/Spearman相关](methods/correlation.md)（Correlation）| RT与年龄的关联 | 连续×连续 | r=0.1小/0.3中/0.5大;被试内需用rmcorr |
| [重复测量相关](methods/rmcorr.md)（rmcorr）| 每人60试次,RT×trial的关联 | 连续×连续 · 被试内 | ANCOVA消除被试间差异 |
| [卡方检验](methods/chi-square.md)（Chi-square Test）| 两条件错误类型分布 | 分类×分类 | 期望频数<5→Fisher精确检验 |
| [McNemar检验](methods/mcnemar-test.md)（McNemar's Test）| 治疗前后诊断变化 | 配对二分类 | 检验变化方向是否对称 |
| [典型相关](methods/canonical-correlation.md)（Canonical Correlation）| 3认知×4问卷整体关联 | 多DV×多IV | 两组变量整体相关,非逐对 |

### 专项方法

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [信号检测论d'](methods/signal-detection-dprime.md)（Signal Detection d'）| Go/No-go分离辨别力与偏向 | 二分类 · Hit/FA | d'=z(H)-z(F);准确率混淆辨别力和偏向 |
| [非参数检验](methods/nonparametric.md)（Nonparametric）| 严重非正态且转换无效 | 连续 | Wilcoxon/Mann-Whitney/Friedman/Kruskal-Wallis |
| [贝叶斯t检验](methods/bayesian-t-test.md)（Bayesian t-test）| 需量化无差异证据 | 连续 | BF10>3=H1支持,BF10<1/3=H0支持 |
| [贝叶斯ANOVA](methods/bayesian-anova.md)（Bayesian ANOVA）| 替代传统ANOVA | 连续 | 小样本可用;支持序贯分析 |
| [稳健方法](methods/robust-methods.md)（Robust Methods）| 含异常值但不能排除 | 连续 | 截尾均值/Winsorized/Yuen's t |
| [置换检验](methods/permutation-test.md)（Permutation Test）| n<20不能假设正态 | 连续 | 随机打乱标签→精确p值 |
| [等效性检验](methods/equivalence-test.md)（TOST）| 证明A和B无差异 | 连续 | 两次单侧t检验;Δ=最小有意义效应 |

### 中介/调节/多层

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [中介分析](methods/mediation.md)（Mediation）| 焦虑→注意偏向→Stroop | 连续 | Bootstrap CI不跨0→中介显著;需n≥100 |
| [调节分析](methods/moderation.md)（Moderation）| 社会支持缓解压力→表现 | 连续 | X×W交互显著→简单斜率±1SD |
| [有调节的中介](methods/moderated-mediation.md)（Moderated Mediation）| 中介路径在WM高低组差异 | 连续 | Index of ModMed的Bootstrap CI |
| [多水平模型](methods/multilevel-modeling.md)（Multilevel）| 学生(Level1)嵌套班级(Level2) | 连续 | ICC>0.05→需多水平;组均值中心化 |
| [结构方程模型](methods/structural-equation-modeling.md)（SEM）| 执行功能(潜变量)中介年龄→Stroop | 连续/潜变量 | CFI>.95,RMSEA<.06;测量+结构 |

### 回归/协方差/纵向

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [多元回归](methods/multiple-regression.md)（Multiple Regression）| 年龄+教育+焦虑预测Stroop | 连续 | 层次回归;ΔR²;VIF<5 |
| [协方差分析](methods/ancova.md)（ANCOVA）| 控制前测比较两训练方法 | 连续 + 协变量 | 回归斜率同质性是关键假设 |
| [增长曲线](methods/growth-curve.md)（Growth Curve）| 5次追踪N-back练习效应 | 连续 · 纵向≥3点 | 固定=平均变化率;随机=个体差异 |
| [交叉滞后面板](methods/cross-lagged-panel.md)（CLPM）| 焦虑⇆睡眠3波追踪 | 连续 · 纵向≥3波 | RI-CLPM分离被试间/内 |
| [时间序列](methods/time-series.md)（ARIMA）| 30天日焦虑评分趋势 | 连续 · 密集纵向 | p,d,q;中断时间序列检验干预 |
| [分位数回归](methods/quantile-regression.md)（Quantile Regression）| Stroop效应在快慢反应上不同? | 连续 | 效应在τ=.25,.50,.75的变化 |

### 测量与量表

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [因子分析](methods/factor-analysis.md)（Factor Analysis）| 20题焦虑量表→3因子 | 连续 · 量表 | EFA:KMO>.6;CFA:CFI>.95,RMSEA<.06 |
| [信度分析](methods/reliability.md)（Reliability）| 量表内部一致性 | 连续 · 分类 | Cronbach's α>.7;推荐报告McDonald's ω |
| [多维标度法](methods/mds.md)（MDS）| 8种情绪相似性→2D空间 | 距离矩阵 | Stress<0.1好;valence×arousal |
| [潜在类别/剖面](methods/latent-class.md)（LCA/LPA）| 焦虑+抑郁+压力→3亚型 | 连续 · 分类 | BIC最低;Entropy>.8;以人为中心 |

### 元分析/效力/Bootstrap

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [效力分析](methods/power-analysis.md)（Power Analysis）| 需要多少被试检测d=0.5? | — | α=.05,power=.80;混合模型用simr |
| [Bootstrap](methods/bootstrap.md)（Bootstrap）| 效应量CI,中介间接效应 | 任意 | 重采样≥5000;被试内重采样被试 |
| [元分析](methods/meta-analysis.md)（Meta-analysis）| 15个Stroop研究整合 | 效应量 | 随机效应默认;I²>50%→异质性 |
| [交叉验证](methods/cross-validation.md)（Cross-validation）| 评估预测模型泛化 | 任意 | k=5/10;被试级分折;最终全数据重拟合 |

### RT与决策建模

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [Ex-Gaussian分布](methods/exgaussian.md)（Ex-Gaussian）| ADHD的τ(注意lapse)高于对照 | RT · 试次级 | μ=决策速度,σ=稳定性,τ=极端慢反应 |
| [漂移扩散模型](methods/drift-diffusion.md)（DDM）| Stroop效应改变v还是a? | RT+准确率 | v=信息积累速度,a=反应阈值,t0=非决策 |
| [心理测量函数](methods/psychometric-function.md)（Psychometric）| 阶梯法估计对比度阈值 | 二分类 | Logistic/Weibull;75%正确=阈值 |

### 临床与诊断

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [ROC分析](methods/roc-analysis.md)（ROC）| 焦虑分数诊断准确率 | 二分类 · 患病/健康 | AUC:0.7可接受/0.8好/0.9优秀 |
| [可靠变化指数](methods/reliable-change-index.md)（RCI）| 治疗后焦虑降7分=真改善? | 连续 · 前后测 | RCI>1.96=可靠变化;跨阈值=临床显著 |
| [Bland-Altman分析](methods/bland-altman.md)（Bland-Altman）| 手动vs自动RT编码一致性 | 连续 · 两方法 | Bias±1.96SD=95%一致限 |
| [Cox回归](methods/cox-regression.md)（Cox Regression）| Stop-signal抑制成功影响因素 | 时间-事件+删失 | HR>1=事件快;比例风险假设 |
| [Log-Rank检验](methods/logrank-survdiff.md)（Log-rank Test）| ADHD vs对照抑制曲线 | 时间-事件+删失 | 非参数;Kaplan-Meier |

### 专项数据与高级方法

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [有序逻辑回归](methods/ordinal-logistic.md)（Ordinal Logistic）| Likert评分(1-7)的条件效应 | 有序分类 | 不假设等距,只假设顺序;OR解释 |
| [Beta回归](methods/beta-regression.md)（Beta Regression）| 条件间注意力分配比例 | 比例 · 0-1 | 自然处理异方差;优于arcsine |
| [Poisson/负二项回归](methods/poisson-regression.md)（Poisson/NB）| 每条件错误次数 | 计数 | 负二项默认(过度离散);零膨胀 |
| [多元方差分析](methods/manova.md)（MANOVA）| RT+准确率+变异性同时检验 | 多DV(连续) | DV相关时效力>多个ANOVA |
| [聚类分析](methods/cluster-analysis.md)（Cluster）| RT/acc/问卷→高效/谨慎两类 | 连续 · 标准化 | 肘部法/轮廓系数;kmeans/LCA |
| [网络分析](methods/network-analysis.md)（Network）| 20症状中哪些处于中心 | 连续 · 症状 | EBICglasso;Strength中心性;CS>.25 |
| [LASSO/Ridge](methods/lasso-ridge.md)（LASSO/Ridge）| 50题中选最佳Stroop预测子集 | 连续 · 高维 | LASSO→选变量;CV选λ;传统回归估计 |
| [多重插补](methods/multiple-imputation.md)（MICE）| 20%被试缺失部分试次 | 含缺失 | m=5-20;Rubin's rules;优于成列删除 |
| [Box-Cox变换](methods/boxcox.md)（Box-Cox）| 找到最优正态化λ | 连续 · 非正态 | λ=0→log;λ=0.5→sqrt |
| [Dunnett/Games-Howell](methods/dunnett-games-howell.md)（Dunnett/Games-Howell）| 只与对照比;方差不齐+n不等 | 连续 | Dunnett效力高;Games-Howell不齐 |

### 选择流程

```
DV 类型？
  ├── 连续 (RT/分数)
  │     ├── 被试内 → 2组[t-test/lmer] / 3+组[ANOVA/lmer] / 非正态[Nonparametric] / 右偏[Gamma]
  │     ├── 被试间 → 2组[Ind-t] / 3+组[ANOVA]
  │     └── 混合 → [Mixed ANOVA]
  ├── 二分类 (正确/错误)
  │     ├── 天花板/地板? → **强制glmer**
  │     └── 否 → glmer推荐, ANOVA可接受(标注)
  ├── 分类 → 卡方检验
  ├── 有序分类(Likert) → 有序逻辑回归
  ├── 两个连续变量 → 相关 / rmcorr(被试内)
  ├── 计数(错误次数) → Poisson/NB
  ├── 比例(准确率%) → Beta回归
  ├── 时间-事件(Stop-signal) → Cox/Log-Rank
  └── 机制检验(中介/调节) → Mediation/Moderation
```

## 图表类型库

48 个图表类型，按 [R Graph Gallery](https://r-graph-gallery.com) 分类。图表选择元逻辑已整合至 [SKILL.md](SKILL.md) Phase 4。

### 分布 (Distribution)

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [直方图](plots/histogram.md)（Histogram）| 单变量分布,bins控制粒度 | 连续 | 对称=正态,右尾=偏态,双峰=混合 |
| [密度图](plots/density-plot.md)（Density）| 平滑分布曲线比较 | 连续 | 重叠=相似,分离=差异大 |
| [箱线图+散点](plots/boxplot-jitter.md)（Boxplot+Jitter）| 被试间/多组四分位+个体 | 连续 · 多组 | 中位线距=效应,散点=个体差异 |
| [小提琴图](plots/violin-standalone.md)（Violin）| 密度形状,比箱线多一层信息 | 连续 · 多组 | 鼓包=多峰,一端鼓=偏态 |
| [雨云图](plots/raincloud.md)（Raincloud）| 被试内两组首选 | 连续 · 被试内 | 小提琴+箱线+散点三合一 |
| [山脊图](plots/ridgeline.md)（Ridgeline）| 3+组密度堆叠,纵向多时点 | 连续 · 多组 | 峰移位=变化,变宽=变异增大 |
| [蜜蜂群图](plots/beeswarm.md)（Beeswarm）| 个体点不重叠,10-200观测 | 连续 | cex控制间距,priority控制排列 |

### 相关 (Correlation)

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [散点图+回归](plots/scatter-regression.md)（Scatter）| 两连续变量+拟合线 | 连续×连续 | 点均匀=线性,漏斗形=异方差 |
| [相关椭圆图](plots/correlation-ellipse.md)（Ellipse）| 置信椭圆+散点 | 连续×连续 | 窄长=强相关,近圆=弱相关 |
| [边缘分布图](plots/marginal-distribution.md)（Marginal）| 散点+X/Y轴密度 | 连续×连续 | 一张图看关系+各自分布 |
| [相关热图](plots/correlation-heatmap.md)（Heatmap）| 多变量相关矩阵 | 连续(4+) | 颜色深浅=相关强度,对角=1 |
| [相关图](plots/correlogram.md)（Correlogram）| 两两散点+相关+分布 | 连续(3-8) | 上三角=系数,下三角=散点 |
| [气泡图](plots/bubble-chart.md)（Bubble）| 散点+size=第三维 | 连续×3 | scale_size_range控制大小范围 |
| [六边形分箱图](plots/hexbin.md)（Hexbin）| 超大样本>5000点 | 连续×连续 | 颜色=密度,无重叠问题 |
| [连接散点图](plots/connected-scatter.md)（Connected）| 时间轨迹+两变量 | 连续×时间 | path保持顺序,arrow示方向 |

### 排序 (Ranking)

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [条形图](plots/bar-chart.md)（Bar）| 被试间均值+误差 | 连续 · 被试间 | ⚠️被试内不推荐,隐藏个体差异 |
| [棒棒糖图](plots/lollipop.md)（Lollipop）| 条形图轻量替代 | 连续 | 线段+圆点,最少墨水 |
| [Cleveland点图](plots/cleveland-dot.md)（Dot）| 多组排序>5组 | 连续 | 比条形图更精准 |
| [环形条形图](plots/circular-barplot.md)（Circular）| 大量类别>10,醒目 | 连续 | ⚠️角度难精确比较 |
| [华夫图](plots/waffle-chart.md)（Waffle）| 方格比例展示 | 分类 | 1方格=1固定单位,直观 |
| [平行坐标图](plots/parallel-coordinates.md)（Parallel）| 高维个体模式 | 连续(4+) | 线束分离=组间差异 |
| [雷达图](plots/radar-chart.md)（Radar）| 多变量剖面 | 连续(3-10) | 面积大=整体高,某轴突出=强项 |

### 演化 (Evolution)

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [折线图](plots/line-plot.md)（Line）| 基础时间序列 | 连续×时间 | 上升/下降趋势一目了然 |
| [时间序列图](plots/time-series-plot.md)（Time Series）| 纵向追踪/EMA,个体+均值 | 连续×时间 | 灰色个体线+红色均值 |
| [个体连线图](plots/individual-lines.md)（Spaghetti）| 被试内两时点连线 | 连续 · 被试内 | 斜率一致=效应稳健 |
| [哑铃图](plots/dumbbell.md)（Dumbbell）| 前后测多项目对比 | 连续 · 前后 | 线长=变化幅度 |
| [斜率图](plots/slope-chart.md)（Slope）| 大量个体两时点快速对比 | 连续 · 两时点 | 陡升/陡降=大幅变化 |
| [冲积图](plots/alluvial-plot.md)（Alluvial）| 纵向分类转换 | 分类·时间 | 流带宽=人数多,分散=转换多 |
| [甘特图](plots/gantt-chart.md)（Gantt）| 实验流程时间线 | 时间 | 条形=任务时长,重叠=并行 |

### 组成 (Part of a Whole)

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [环形图](plots/donut-chart.md)（Donut）| 少量类别比例 | 分类 | ⚠️人眼不擅长比较弧长 |
| [堆叠面积图](plots/stacked-area.md)（Stacked Area）| 时间+组成比例 | 分类×时间 | stack=绝对量,fill=比例 |
| [流图](plots/streamgraph.md)（Streamgraph）| 堆叠面积变体 | 分类×时间 | 中心对称,适合趋势非精确值 |
| [树图](plots/treemap.md)（Treemap）| 层次比例,嵌套矩形 | 分类 | 面积=数值,适合>5类 |
| [马赛克图](plots/mosaic-plot.md)（Mosaic）| 分类交叉表 | 分类×分类 | 蓝=多于期望,红=少于期望 |
| [Upset图](plots/upset-plot.md)（UpSet）| 多集合交集 | 多分类组合 | 韦恩图现代替代,适合>3集合 |

### 特殊 (Special)

| 名称 | 典型场景 | 数据类型 | 核心 |
|------|---------|---------|------|
| [QQ图](plots/qq-plot.md)（QQ Plot）| 正态性视觉检验 | 连续 | 点贴对角线=正态,两端翘=重尾 |
| [交互作用图](plots/interaction-plot.md)（Interaction）| 两因素交互 | 连续 · 两因素 | 线不平行=交互存在 |
| [显著性标注](plots/significance-annotation.md)（Signif）| 图表上标注p值/星号 | — | ggsignif自动星号或手动p值 |
| [森林图](plots/forest-plot.md)（Forest）| 元分析效应量+CI | 效应量+CI | 线跨0=不显著,菱形=合并效应 |
| [漏斗图](plots/funnel-plot.md)（Funnel）| 发表偏倚检测 | 效应量+SE | 不对称=小样本阴性结果缺失 |
| [ROC曲线](plots/roc-curve.md)（ROC）| 二分类判别 | 二分类+预测 | AUC>0.8=好,0.5=随机 |
| [Kaplan-Meier](plots/kaplan-meier.md)（KM Curve）| 生存/事件时间 | 时间-事件 | 曲线陡降=事件早,分离=组间差 |
| [Bland-Altman](plots/bland-altman-plot.md)（BA Plot）| 方法一致性 | 连续(两方法) | Bias±1.96SD=95%一致限 |
| [双标图](plots/biplot.md)（Biplot）| PCA/因子分析 | 连续(多变量) | 同向箭头=正相关,反向=负相关 |
| [网络图](plots/network-graph.md)（Network）| 心理网络,偏相关 | 连续(多变量) | 粗边=强相关,中心节点=高中心性 |
| [弦图](plots/chord-diagram.md)（Chord）| 方阵流向 | 方阵 | 弦宽=流量,外环=总量 |
| [树状图](plots/dendrogram.md)（Dendrogram）| 层次聚类 | 距离矩阵 | 低处合并=相似,横切线定类数 |
| [词云](plots/wordcloud.md)（Word Cloud）| 文本频率 | 文本 | 字号=频率,适合定性展示 |

## 关键文件

| 文件 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | 完整工作流规范 |
| [methods/](methods/) | 60 个分析方法 |
| [plots/](plots/) | 48 个图表类型 + 元逻辑 |