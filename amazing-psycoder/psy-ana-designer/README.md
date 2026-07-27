# psy-ana-designer

> v1.4.0 | 从科学问题、estimand、数据生成过程和观测层级设计分析；确认语言/精确版本/依赖策略后输出 `analysis_config.yaml` v1.2，不生成代码。

## 证据驱动工作流

| Phase | 产物 | Gate |
|------|------|------|
| 1. 问题 | confirmatory/exploratory 角色、primary/secondary、estimand | 主要主张与操作化明确；不是每个记录字段都强造问题 |
| 2. 数据 | 实际 schema、ID/项目/会话、观测层级、缺失与抽样结构 | 依赖结构和变量类型可验证 |
| 3. 方法 | selected method、公式、诊断、真正可行的替代方案 | 方法回答 estimand 且表示层级；用户只能在可行方案中选择 |
| 4. 细节 | 排除/缺失/变换 provenance、multiplicity、估计/区间、图表、敏感性 | 无通用 RT/缺失/正态性阈值；规则有依据且预先声明 |
| 5. 审查 | 完整 Decision Registry + 保存的 config 路径 | `validate_analysis.py` 零错误，用户确认后交给 Coder |

## 方法选择原则

- 先确定目标量和观测单位，再选 likelihood/link、固定效应、随机/相关结构；不要从“最熟悉的检验”倒推问题。
- trial/event 级重复数据必须表示被试、项目、会话等相关性。普通独立观测 Logit 不是随机效应 GLMM；GEE、GLMM、贝叶斯层级模型或有依据的聚合回答不同 estimand。
- 二元、计数、有序、比例和生存结局按其支持集与生成过程建模。Beta 回归通常用于连续开区间 `(0,1)`，不是任意准确率表格。
- SSRT 按 stop-signal 任务共识流程设计并保存必要输入；它不是普通 Cox/log-rank 生存问题。
- confirmatory 分析不能用焦点结局反复试阈值/模型后再当作预先方案。必要的数据驱动选择应标为 exploratory、使用 blinded/pilot 数据，或预定义决策/敏感性规则。
- 只有两个以上方法都真正可行且选择会影响结论时，才展开完整比较；不要制造陪跑 Candidate A/B。
- seed 只约束实际随机步骤，还需记录包、硬件/并行和采样设置；seed 不保证跨环境数值完全相同。

## 参考资源路由

`methods/` 与 `plots/` 是候选卡片，不是自动处方，也不覆盖 [SKILL.md](SKILL.md)、config schema、平台实现限制或 Reviewer 结论。方法卡中的代码/经验阈值必须结合当前问题、软件版本和领域依据复核。

| Need | Start here |
|------|------------|
| 连续重复数据 | [linear mixed model](methods/linear-mixed-model.md), [crossed random effects](methods/crossed-random-effects.md), [GEE](methods/gee.md) |
| 二元/计数/有序 | [logistic mixed model](methods/logistic-mixed-model.md), [Poisson/NB](methods/poisson-regression.md), [ordinal logistic](methods/ordinal-logistic.md) |
| RT 分布/机制 | [Gamma mixed](methods/gamma-mixed-model.md), [ex-Gaussian](methods/exgaussian.md), [DDM](methods/drift-diffusion.md) |
| 测量/纵向/预测 | [reliability](methods/reliability.md), [growth curve](methods/growth-curve.md), [cross-validation](methods/cross-validation.md) |
| 缺失/稳健性 | [multiple imputation](methods/multiple-imputation.md), [robust methods](methods/robust-methods.md), [bootstrap](methods/bootstrap.md) |
| 图表 | 用目标估计和数据层级选 `plots/`；显示个体/项目结构与不确定性，避免只画均值柱状图 |

完整规则见 [SKILL.md](SKILL.md) 与 [config schema](references/config-schema.md)。
