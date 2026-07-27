# psy-ana-coder — 分析代码生成层

> **版本**: v1.4.0 | 从已确认的分析 config 生成 R/Python 脚本；不重新发明研究问题或统计方法。

## 输入与输出

- 输入：通过 `scripts/validate_analysis.py` 的 `analysis_config.yaml`，其中包含已确认的语言/精确版本/依赖策略、问题角色、estimand、观测层级、selected method、公式、清洗/缺失策略和输出契约。
- 输出：配置驱动的 `.R`/`.py`、可选 `.Rmd`/`.qmd`/`.ipynb`、结果目录与 `analysis-run.json` 执行清单。
- 静态生成和审查最多标记 `ready_for_execution`；只有 clean run 与结果审查后才能评估 `ready_for_publication`。

## 生成结构

1. 读取 config，校验 schema、ID、列类型、单位和数据层级。
2. 捕获环境；仅为声明的 stochastic 步骤设置 seed/后端控制。
3. 导入数据并保存 source-row、缺失、排除和变换 provenance。
4. 生成与 estimand/层级一致的描述统计、模型、诊断和敏感性分析。
5. 保存目标效应估计、不确定性、必要的 multiplicity 结果与图表。
6. 写入执行状态、输入/config 哈希、输出清单、警告和环境信息。

Python 的普通 `statsmodels.Logit()` 不是随机效应 GLMM；重复二元结果需按已确认方案使用适当的 GLMM/GEE/贝叶斯层级实现。R 与 Python 无需强行产生数值完全相同的实现，但都必须忠实于同一 estimand 和证据契约。

完整规则见 [SKILL.md](SKILL.md)、[R spec](r/spec/README.md)、[Python spec](python/spec/README.md) 与对应 mapping/checklist。
