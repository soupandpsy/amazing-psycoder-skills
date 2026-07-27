# Reviewer — Python 审计清单

先读取已确认的 `analysis_config.yaml`。静态关键词只能辅助定位，不能替代对 estimand、层级和模型语义的审查。

## 证据门

| 检查 | 通过标准 |
|------|----------|
| Config/schema | 脚本读取 config；验证输入列、类型、ID、层级和单位 |
| 数据流转 | 排除/缺失/变换有来源、理由、前后计数和可保存日志 |
| Estimand/model | 公式、family/link 与结局类型、目标 estimand、聚类结构一致 |
| 随机步骤 | 仅 stochastic 步骤要求显式 RNG/seed，并记录采样/并行设置 |
| 诊断 | 检查实际模型需要的收敛、残差、过度离散、影响点或后验诊断 |
| 推断 | 主要结论保存目标估计和不确定性；multiplicity 与 config 一致 |
| 输出/环境 | 表图、样本流转、执行日志和包/解释器版本被保存 |

## 高风险模式（结合上下文判定）

- 用户专属绝对路径、隐式 notebook 状态或未记录的手工数据编辑。
- 重复二元数据使用普通 `statsmodels.Logit/GLM` 却声称实现随机效应；应选支持目标层级的 GLMM、GEE、贝叶斯层级模型或有依据的聚合分析。
- 把独立观测 `ttest_ind`/OLS 用于配对、重复或聚类数据。
- 对所有模型机械做 Shapiro/Levene，或忽略更相关的模型诊断。
- 只报告 p 值/R²，缺少 config 指定的目标估计与区间。
- stochastic 函数没有 RNG 控制；反之，确定性 `scipy.stats` 检验不需要 `random_state`。
- `iterrows()`/`apply()` 仅在其确实造成性能或语义错误时分级，不作为自动失败。

## 结果审查附加项

`result-audit` 必须看到 clean execution log、生成的表图、环境信息和警告/收敛状态，并核对样本流转、估计方向、单位和报告结论。否则最高标签为 `ready_for_execution`。
