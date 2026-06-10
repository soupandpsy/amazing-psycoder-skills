# ============================================================
# 分析项目：Stroop 颜色-词义冲突任务
# 统计模型：线性混合模型（lmer）
# 实验设计：单因素被试内（condition: congruent vs incongruent）
# 因变量：反应时（rt, ms）、正确率（acc, 0/1）
# 生成日期：2026-06-11 | 随机种子：20260609
# ============================================================

# ============================================================
# Config 参数（来自 analysis_config.yaml，可在此处修改）
# ============================================================
# data_path     <- "data/stroop_data.csv"   # 数据文件路径
# rt_lower      <- 150                      # RT 下界（ms），低于此值视为预期反应
# rt_upper      <- 2000                     # RT 上界（ms），高于此值视为走神
# accuracy_min  <- 0.6                      # 被试最低平均正确率，低于此值排除该被试
# sd_multiplier <- 2.5                      # 试次排除的 SD 倍数（按被试×条件）
# save_path     <- "output"                 # 图表输出目录
# seed          <- 20260609                 # 随机种子，保证结果可重复
# ============================================================

# ---- 参数设置（从 config 读取，此处为默认值）----
data_path     <- "data/stroop_data.csv"
rt_lower      <- 150
rt_upper      <- 2000
accuracy_min  <- 0.6
sd_multiplier <- 2.5
save_path     <- "output"
seed          <- 20260609

# ============================================================
# 第 1 步：环境设置
# 加载所有需要的 R 包，设置全局选项和随机种子
# ============================================================
library(tidyverse)    # 数据处理：readr, dplyr, tidyr, ggplot2
library(here)          # 项目相对路径管理
library(lme4)          # 线性混合模型：lmer()
library(lmerTest)      # 为 lmer 提供 p 值（Satterthwaite 自由度近似）
library(effectsize)    # 效应量：repeated_measures_d(), r2() 等
library(ggplot2)       # 数据可视化
library(ggrain)        # 雨云图：geom_rain()，小提琴+箱线+散点三合一
library(patchwork)     # 拼图：将多个 ggplot 拼接为一个图
library(emmeans)       # 边际均值估计 + 事后两两比较
library(performance)   # 模型诊断：r2() 计算 Marginal/Conditional R²
options(dplyr.summarise.inform = FALSE)  # 关闭 summarise 的分组提示
set.seed(seed)  # 固定随机种子，确保结果可重复

# ============================================================
# 第 2 步：数据导入 + 列名校验
# ============================================================
# 使用 here::here() 构建相对于项目根目录的路径，避免硬编码
data <- read_csv(here::here(data_path), show_col_types = FALSE)

# 校验必需的列是否存在，缺失则立即报错停止
expected_cols <- c("subject_id", "condition", "rt", "acc")
missing_cols <- setdiff(expected_cols, names(data))
if (length(missing_cols) > 0) {
  stop("缺少列: ", paste(missing_cols, collapse = ", "))
}

# 输出数据概览
cat(sprintf("已加载 %d 行, %d 列\n", nrow(data), ncol(data)))
cat(sprintf("被试数: %d, 条件: %s\n",
    n_distinct(data$subject_id),
    paste(unique(data$condition), collapse = ", ")))

# ============================================================
# 第 3 步：数据清洗（四层排除 + 完整日志）
# 每一步都打印排除的试次数量和比例，确保透明可追溯
# ============================================================
cat("\n========== 排除日志 ==========\n")
n_before <- nrow(data)

# 3a. RT 范围过滤 —— 排除过快（预期反应）和过慢（走神）的试次
data <- data %>% filter(rt > rt_lower & rt < rt_upper)
cat(sprintf("RT 越界 (<%d 或 >%d ms): %d 试次 (%.1f%%)\n",
    rt_lower, rt_upper,
    n_before - nrow(data),
    100 * (n_before - nrow(data)) / n_before))

# 3b. 仅保留正确试次 —— 错误试次的 RT 不可靠，不纳入 RT 分析
n_with_acc <- nrow(data)
data_rt <- data %>% filter(acc == 1)
cat(sprintf("错误试次排除: %d 试次 (%.1f%%)\n",
    n_with_acc - nrow(data_rt),
    100 * (n_with_acc - nrow(data_rt)) / n_with_acc))

# 3c. 被试级排除 —— 整体正确率过低说明该被试未认真完成任务
subj_acc <- data %>%
  group_by(subject_id) %>%
  summarise(mean_acc = mean(acc, na.rm = TRUE), .groups = "drop")
excluded_subj <- subj_acc %>% filter(mean_acc < accuracy_min)
if (nrow(excluded_subj) > 0) {
  cat(sprintf("正确率低于 %.0f%% 的被试: %d (ID: %s)\n",
      accuracy_min * 100,
      nrow(excluded_subj),
      paste(excluded_subj$subject_id, collapse = ", ")))
  data_rt <- data_rt %>% filter(!subject_id %in% excluded_subj$subject_id)
} else {
  cat(sprintf("正确率低于 %.0f%% 的被试: 0\n", accuracy_min * 100))
}

# 3d. 试次级排除 —— 按被试×条件，排除超过 ±SD 倍数的极端值
n_before_sd <- nrow(data_rt)
data_rt <- data_rt %>%
  group_by(subject_id, condition) %>%
  mutate(
    mean_rt    = mean(rt, na.rm = TRUE),      # 该被试在该条件的均值
    sd_rt      = sd(rt, na.rm = TRUE),         # 该被试在该条件的标准差
    is_outlier = abs(rt - mean_rt) > sd_multiplier * sd_rt  # 标记离群值
  ) %>%
  ungroup()
cat(sprintf("SD 排除 (>%.1f SD): %d 试次 (%.1f%%)\n",
    sd_multiplier,
    sum(data_rt$is_outlier),
    100 * sum(data_rt$is_outlier) / n_before_sd))
data_rt <- data_rt %>% filter(!is_outlier)

# 汇总清洗结果
cat(sprintf("最终数据集: %d 试次, %d 被试\n",
    nrow(data_rt), n_distinct(data_rt$subject_id)))

# ============================================================
# 第 4 步：描述统计
# 按条件分组计算：样本量、均值、标准差、标准误、95% CI、中位数
# ============================================================
cat("\n========== 描述统计 ==========\n")
desc <- data_rt %>%
  group_by(condition) %>%
  summarise(
    n          = n(),                                       # 试次数
    n_subj     = n_distinct(subject_id),                    # 被试数
    mean_rt    = mean(rt, na.rm = TRUE),                    # 平均 RT
    sd_rt      = sd(rt, na.rm = TRUE),                      # RT 标准差
    se_rt      = sd_rt / sqrt(n_subj),                      # 标准误（被试间）
    ci95_lo    = mean_rt - qt(0.975, n_subj - 1) * se_rt,  # 95% CI 下界
    ci95_hi    = mean_rt + qt(0.975, n_subj - 1) * se_rt,  # 95% CI 上界
    median_rt  = median(rt, na.rm = TRUE),                  # 中位数（偏态时更稳健）
    .groups    = "drop"
  )
print(desc, width = 120)

# ============================================================
# 第 5 步：统计假设检验
# 混合模型假设：残差近似正态。按条件检验原始 RT 的正态性 + QQ 图
# ============================================================
cat("\n========== 假设检验 ==========\n")

# Shapiro-Wilk 正态性检验（按条件）
data_rt %>%
  group_by(condition) %>%
  summarise(
    shapiro_W = shapiro.test(rt)$statistic,  # W 值，越接近 1 越正态
    shapiro_p = shapiro.test(rt)$p.value,     # p > 0.05 表示不拒绝正态
    .groups   = "drop"
  ) %>%
  mutate(verdict = ifelse(shapiro_p > 0.05, "通过", "未通过")) %>%
  print()

# Q-Q 图：可视化正态性（点应贴近对角线）
ggplot(data_rt, aes(sample = rt)) +
  geom_qq() +
  geom_qq_line(color = "red") +
  facet_wrap(~ condition) +
  labs(title    = "Q-Q 图：按条件的 RT 正态性检验",
       subtitle = "点贴近红色对角线 = 数据近似正态") +
  theme_minimal()

# ============================================================
# 第 6 步：统计建模
# 线性混合模型（lmer），包含随机截距和随机斜率
# 模型公式: rt ~ condition + (1 + condition | subject_id)
#   固定效应: condition（一致 vs 不一致的 RT 差异）
#   随机效应: 每个被试有自己的基线 RT（随机截距）和条件效应（随机斜率）
# ============================================================
cat("\n========== 统计模型 ==========\n")
model <- lmer(
  rt ~ condition + (1 + condition | subject_id),
  data    = data_rt,
  control = lmerControl(optimizer = "bobyqa")  # 更稳健的优化器
)
cat("\n模型摘要:\n")
print(summary(model))

# ============================================================
# 第 7 步：效应量 + 事后比较
# ============================================================
cat("\n========== 效应量 ==========\n")

# 混合模型的 R²：Marginal（仅固定效应）和 Conditional（固定+随机效应）
cat("\n模型 R²:\n")
print(r2(model))

# 边际均值：控制随机效应后，每个条件的估计均值
emm <- emmeans(model, ~ condition)
cat("\n边际均值:\n")
print(emm)

# 事后两两比较（Bonferroni 校正）
contrast_result <- pairs(emm, adjust = "bonferroni")
cat("\n两两比较（Bonferroni 校正）:\n")
print(contrast_result)

# ============================================================
# 第 8 步：敏感性分析
# 用配对 t 检验（方法 A）与混合模型（方法 B）比较
# 如果两者结论一致 → 结果稳健。如果不一致 → 需进一步检查
# ============================================================
cat("\n========== 敏感性分析 ==========\n")

# 聚合到被试×条件均值（配对 t 检验需要）
data_agg <- data_rt %>%
  group_by(subject_id, condition) %>%
  summarise(mean_rt = mean(rt), .groups = "drop")

# 方法 A：配对 t 检验
tt_result <- t.test(mean_rt ~ condition, data = data_agg, paired = TRUE)
cat(sprintf("方法 A (配对 t 检验): t(%.0f) = %.2f, p = %.4f, d = %.2f\n",
    tt_result$parameter, tt_result$statistic, tt_result$p.value,
    repeated_measures_d(mean_rt ~ condition | subject_id, data = data_agg)$Cohens_d))

# 方法 B：线性混合模型
cat(sprintf("方法 B (lmer): p = %.4f\n",
    summary(model)$coefficients[2, 5]))

# 结论一致性判断
cat(sprintf("两种方法结论一致: %s\n",
    ifelse(
      (tt_result$p.value < 0.05) == (summary(model)$coefficients[2, 5] < 0.05),
      "是 —— 结论稳健",
      "否 —— 需进一步检查，可能存在方法依赖性"
    )))

# ============================================================
# 第 9 步：图表生成
# 图 1：雨云图（小提琴 + 箱线 + 散点，展示完整数据分布）
# 图 2：个体连线图（展示每个被试的变化方向和幅度）
# ============================================================

# 确保输出目录存在
if (!dir.exists(save_path)) dir.create(save_path, recursive = TRUE)

# 图 1: 雨云图 —— 被试内两组比较的首选图表
p1 <- ggplot(data_rt,
       aes(x = condition, y = rt, fill = condition, color = condition)) +
  ggrain::geom_rain(alpha = 0.5, point.size = 1) +  # 小提琴+箱线+散点
  scale_fill_brewer(palette = "Set2") +               # 色盲友好调色板
  scale_color_brewer(palette = "Set2") +
  labs(
    title = "Stroop: 各条件反应时",
    x     = "条件",
    y     = "反应时 (ms)"
  ) +
  theme_minimal(base_size = 12) +
  theme(legend.position = "none")
ggsave(file.path(save_path, "fig1_raincloud.png"),
       p1, width = 6, height = 5, dpi = 300)

# 图 2: 个体连线图 —— 展示每个被试从一致到不一致条件的 RT 变化
p2 <- data_agg %>%
  ggplot(aes(x = condition, y = mean_rt, group = subject_id)) +
  geom_line(alpha = 0.3, linewidth = 0.5) +            # 个体线（灰色半透明）
  geom_point(alpha = 0.3, size = 1) +                   # 个体点
  stat_summary(aes(group = 1), fun = mean,
               geom = "line", linewidth = 1.5, color = "red") +  # 组均值线
  stat_summary(fun = mean,
               geom = "point", size = 3, color = "red") +        # 组均值点
  labs(
    title = "Stroop: 个体 RT 变化",
    x     = "条件",
    y     = "平均反应时 (ms)"
  ) +
  theme_minimal(base_size = 12)
ggsave(file.path(save_path, "fig2_individual.png"),
       p2, width = 6, height = 5, dpi = 300)

# ============================================================
# 第 10 步：环境信息
# 输出 R 版本、包版本、系统时间 —— 确保分析完全可重复
# ============================================================
cat("\n========== 环境信息 ==========\n")
cat(sprintf("分析生成时间: %s\n", Sys.time()))
cat(sprintf("R 版本: %s\n", R.version.string))
for (pkg in c("tidyverse", "lme4", "lmerTest", "effectsize",
               "ggplot2", "ggrain", "patchwork", "emmeans", "performance")) {
  cat(sprintf("  %s: %s\n", pkg, as.character(packageVersion(pkg))))
}
sessionInfo()
