# Python 分析平台 — Reviewer 检查清单

## Quality Gate（交付前必查）

| # | 检查项 | grep 命令 |
|---|--------|----------|
| 1 | seed 已设 | `grep -q "random\.seed\|np\.random\.seed" script.py` |
| 2 | 排除日志 | `grep -q "Exclusion\|排除" script.py` |
| 3 | 正态性检验 | `grep -q "shapiro\|normaltest" script.py` |
| 4 | 效应量 | `grep -q "cohens_d\|compute_effsize\|eta_squared\|anova" script.py` |
| 5 | 多重比较 | `grep -q "multipletests\|pairwise_tukeyhsd\|adjust" script.py` |
| 6 | 环境信息 | `grep -q "sys\.version\|pip freeze\|pkg_resources" script.py` |
| 7 | 无绝对路径 | `! grep -q "/Users/\|/home/\|C:\\\\" script.py` |
| 8 | 图表保存 | `grep -q "savefig" script.py` |
| 9 | 列名校验 | `grep -q "issubset\|columns\|assert.*col" script.py` |
| 10 | 包版本 | `grep -q "version\|__version__\|pip freeze" script.py` |

## 反模式检查

| # | 反模式 | grep 命令（不得出现） |
|---|--------|---------------------|
| 1 | import * | `! grep -q "import \*" script.py` |
| 2 | 绝对路径 | `! grep -q "/Users/\|C:\\\\|\~/data" script.py` |
| 3 | df.apply循环 | 允许但需注释说明为何不用向量化 |
| 4 | 无random_state | `! grep -q "scipy.stats.*("` 时检查附近有 `random_state` |
| 5 | 被试内用f_oneway | 如 design=within, `! grep -q "f_oneway" script.py` |

## 统计正确性检查

| # | 检查项 | 验证方式 |
|---|--------|---------|
| 1 | 模型与设计匹配 | within→ttest_rel/pingouin.ttest, between→ttest_ind/f_oneway |
| 2 | 随机效应合理 | MixedLM 至少含 `groups` 参数指定被试 |
| 3 | 分类变量为 category | `grep -q "astype.*category\|pd\.Categorical" script.py` |
| 4 | 效应量类型正确 | t-test→d, ANOVA→η², mixed→R²/ICC |
| 5 | 敏感度分析 | `grep -q "Sensitivity\|敏感\|agree" script.py` |
| 6 | 排除标准已声明 | cat()/print() 输出每步排除原因 |
| 7 | 多重比较已说明 | 注释或 print() 说明校正方法 |
