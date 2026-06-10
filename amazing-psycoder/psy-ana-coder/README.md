# psy-ana-coder — 分析代码生成层

> **版本**: v1.3 | **角色**: 接收分析 config YAML，根据用户语言偏好（R/Python）生成完整可重复的分析脚本。不设计分析。amazing-psycoder 子技能。

## 一句话说明

输入分析 config YAML，输出 R 或 Python 分析脚本 + 可重复报告（RMarkdown / Jupyter）。

## 平台支持

| 平台 | 状态 | 内容 |
|------|:--:|------|
| R | ✅ | tidyverse + lme4 + ggplot2 + RMarkdown |
| Python | ✅ | pandas + statsmodels + seaborn + Jupyter |

## 12 步脚本结构

```
1. 标题注释  → 实验名、模型、日期、seed
2. 环境设置  → 包加载、seed、全局选项
3. 数据导入  → 读取 + 列名校验
4. 数据清洗  → RT过滤→正确试次→被试排除→SD排除→缺失处理
5. 排除日志  → 每步打印排除数量和比例
6. 描述统计  → 按条件分组汇总
7. 假设检验  → Shapiro-Wilk + QQ图 + Levene
8. 统计建模  → 按config选模型
9. 效应量    → Cohen's d / η²p / R²
10. 事后比较 → 边际均值 + 多重比较校正
11. 图表生成 → 雨云图/个体连线/箱线/交互图
12. 环境信息 → sessionInfo / sys.version
```

## 每平台 4 组件

```
r/                          python/
├── spec/README.md          ├── spec/README.md        API规范+反模式
├── mapping/README.md       ├── mapping/README.md     config→代码映射
├── checklist/README.md     ├── checklist/README.md   reviewer检查项
└── demo/                   └── demo/
    ├── stroop_lmer.R           ├── stroop_lmer.py      lmer 完整示例
    └── stroop_ttest.R          └── stroop_ttest.py     t检验 完整示例
```

## 10 项质量闸

| # | 检查项 |
|---|--------|
| 1 | Seed 已设 |
| 2 | 排除日志存在 |
| 3 | 正态性检验代码 |
| 4 | 效应量代码 |
| 5 | 多重比较校正 |
| 6 | 环境信息输出 |
| 7 | 无硬编码路径 |
| 8 | 图表保存到磁盘 |

**Any failure = fix before delivery.**

## 关键文件

| 文件 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | 共享分析逻辑 + R↔Python映射表 |
| [r/spec/README.md](r/spec/README.md) | R API规范 + 15项反模式 + 12步模板 |
| [r/mapping/README.md](r/mapping/README.md) | Config YAML → R 代码映射 |
| [r/checklist/README.md](r/checklist/README.md) | R 审计检查清单 |
| [python/spec/README.md](python/spec/README.md) | Python API规范 + 12项反模式 |
| [python/mapping/README.md](python/mapping/README.md) | Config YAML → Python 代码映射 |
