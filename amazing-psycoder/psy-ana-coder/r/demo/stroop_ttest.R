# ============================================================
# 分析项目：Stroop 颜色-词义冲突任务
# 统计模型：配对 t 检验（被试内，基于每被试每条件的均值）
# 实验设计：单因素被试内（condition: congruent vs incongruent）
# 因变量：反应时（rt, ms）
# 生成日期：2026-06-11 | 随机种子：20260610
# ============================================================

# ============================================================
# Config 参数（来自 analysis_config.yaml，可在此处修改）
# ============================================================
# data_path     <- "data/stroop_data.csv"   # 数据文件路径
# rt_lower      <- 150                      # RT 下界（ms）
# rt_upper      <- 2000                     # RT 上界（ms）
# accuracy_min  <- 0.6                      # 被试最低平均正确率
# sd_multiplier <- 2.5                      # 试次排除 SD 倍数
# save_path     <- "output"                 # 图表输出目录
# seed          <- 20260610                 # 随机种子
# ============================================================

# ---- 参数设置（从 config 读取）----
data_path     <- "data/stroop_data.csv"
rt_lower      <- 150
rt_upper      <- 2000
accuracy_min  <- 0.6
sd_multiplier <- 2.5
save_path     <- "output"
seed          <- 20260610

# ============================================================
# 第 1 步：环境设置
# 加载需要的包，设置全局选项和随机种子
# ============================================================
library(tidyverse)    # 数据处理 + 可视化
library(here)          # 相对路径管理
library(effectsize)    # 效应量：repeated_measures_d()
library(ggplot2)       # 数据可视化
library(ggrain)        # 雨云图：geom_rain()
options(dplyr.summarise.inform = FALSE)
set.seed(seed)  # 固定随机种子，确保结果可重复

# ============================================================
# 第 2 步：数据导入 + 列名校验
# ============================================================
data <- read_csv(here::here(data_path), show_col_types = FALSE)

expected_cols <- c("subject_id", "condition", "rt", "acc")
missing_cols <- setdiff(expected_cols, names(data))
if (length(missing_cols) > 0) {
  stop("缺少列: ", paste(missing_cols, collapse = ", "))
}

cat(sprintf("已加载 %d 行, %d 列\n", nrow(data), ncol(data)))
cat(sprintf("被试数: %d, 条件: %s\n",
    n_distinct(data$subject_id),
    paste(unique(data$condition), collapse = ", ")))

# ============================================================
# 第 3 步：数据清洗（四层排除 + 完整日志）
# ============================================================
cat("\n========== 排除日志 ==========\n")
n_before <- nrow(data)

# 3a. RT 范围过滤
data <- data %>% filter(rt > rt_lower & rt < rt_upper)
cat(sprintf("RT 越界 (<%d 或 >%d ms): %d 试次 (%.1f%%)\n",
    rt_lower, rt_upper,
    n_before - nrow(data),
    100 * (n_before - nrow(data)) / n_before))

# 3b. 仅保留正确试次
n_with_acc <- nrow(data)
data_rt <- data %>% filter(acc == 1)
cat(sprintf("错误试次排除: %d 试次 (%.1f%%)\n",
    n_with_acc - nrow(data_rt),
    100 * (n_with_acc - nrow(data_rt)) / n_with_acc))

# 3c. 被试级排除
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

# 3d. 试次级排除（按被试×条件）
n_before_sd <- nrow(data_rt)
data_rt <- data_rt %>%
  group_by(subject_id, condition) %>%
  mutate(
    mean_rt    = mean(rt, na.rm = TRUE),
    sd_rt      = sd(rt, na.rm = TRUE),
    is_outlier = abs(rt - mean_rt) > sd_multiplier * sd_rt
  ) %>%
  ungroup()
cat(sprintf("SD 排除 (>%.1f SD): %d 试次 (%.1f%%)\n",
    sd_multiplier,
    sum(data_rt$is_outlier),
    100 * sum(data_rt$is_outlier) / n_before_sd))
data_rt <- data_rt %>% filter(!is_outlier)

cat(sprintf("最终数据集: %d 试次, %d 被试\n",
    nrow(data_rt), n_distinct(data_rt$subject_id)))

# ============================================================
# 第 4 步：聚合到被试均值
# 配对 t 检验分析的是被试×条件的均值，而非原始试次
# ============================================================
data_agg <- data_rt %>%
  group_by(subject_id, condition) %>%
  summarise(mean_rt = mean(rt), .groups = "drop")

# ============================================================
# 第 5 步：描述统计（基于被试均值）
# ============================================================
cat("\n========== 描述统计 ==========\n")
desc <- data_agg %>%
  group_by(condition) %>%
  summarise(
    n       = n(),                                     # 被试数
    mean_rt = mean(mean_rt),                            # 平均 RT
    sd_rt   = sd(mean_rt),                              # 被试间标准差
    se_rt   = sd_rt / sqrt(n),                          # 标准误
    ci95_lo = mean_rt - qt(0.975, n - 1) * se_rt,      # 95% CI 下界
    ci95_hi = mean_rt + qt(0.975, n - 1) * se_rt,      # 95% CI 上界
    .groups = "drop"
  )
print(desc, width = 120)

# ============================================================
# 第 6 步：统计假设检验
# 配对 t 检验的关键假设：两种条件的差值服从正态分布
# 注意：检验的是差值的正态性，而非原始数据的正态性！
# ============================================================
cat("\n========== 假设检验 ==========\n")

# 计算每被试的差值（不一致 - 一致）
diff_data <- data_agg %>%
  pivot_wider(names_from = condition, values_from = mean_rt) %>%
  mutate(diff = incongruent - congruent)

# Shapiro-Wilk 差值正态性检验
cat("差值正态性检验:\n")
cat(sprintf("  Shapiro-Wilk: W = %.3f, p = %.3f\n",
    shapiro.test(diff_data$diff)$statistic,
    shapiro.test(diff_data$diff)$p.value))

# Q-Q 图：差值正态性可视化
ggplot(diff_data, aes(sample = diff)) +
  geom_qq() +
  geom_qq_line(color = "red") +
  labs(
    title    = "Q-Q 图：RT 差值（不一致 - 一致）",
    subtitle = "点贴近红色对角线 = 差值近似正态"
  ) +
  theme_minimal()

# ============================================================
# 第 7 步：统计检验
# 配对 t 检验：比较同一批被试在两种条件下的均值差异
# ============================================================
cat("\n========== 配对 t 检验 ==========\n")

# 将数据转为宽格式（每个被试一行，两列分别为两种条件的均值）
wide_rt <- data_agg %>%
  pivot_wider(names_from = condition, values_from = mean_rt)

# 执行配对 t 检验
tt <- t.test(wide_rt$incongruent, wide_rt$congruent, paired = TRUE)
cat(sprintf("t(%d) = %.2f, p = %.4f\n",
    tt$parameter, tt$statistic, tt$p.value))
cat(sprintf("均值差: %.1f ms [%.1f, %.1f]\n",
    tt$estimate, tt$conf.int[1], tt$conf.int[2]))

# ============================================================
# 第 8 步：效应量
# 配对设计中推荐使用 Cohen's dz（差值均值 / 差值标准差）
# dz 反映的是被试内效应的一致性，通常大于被试间设计的 d
# ============================================================
cat("\n========== 效应量 ==========\n")
d_result <- repeated_measures_d(mean_rt ~ condition | subject_id, data = data_agg)
cat(sprintf("Cohen's dz = %.2f, 95%% CI [%.2f, %.2f]\n",
    d_result$Cohens_d, d_result$CI_low, d_result$CI_high))
cat("解释: 0.2 = 小, 0.5 = 中, 0.8 = 大\n")

# ============================================================
# 第 9 步：图表生成
# ============================================================

if (!dir.exists(save_path)) dir.create(save_path, recursive = TRUE)

# 图 1: 雨云图 —— 展示每个条件的分布 + 个体数据点
p1 <- data_agg %>%
  ggplot(aes(x = condition, y = mean_rt, fill = condition, color = condition)) +
  ggrain::geom_rain(alpha = 0.5, point.size = 1) +
  scale_fill_brewer(palette = "Set2") +
  scale_color_brewer(palette = "Set2") +
  labs(
    title = "Stroop: 各条件反应时",
    x     = "条件",
    y     = "平均反应时 (ms)"
  ) +
  theme_minimal(base_size = 12) +
  theme(legend.position = "none")
ggsave(file.path(save_path, "fig1_raincloud.png"),
       p1, width = 6, height = 5, dpi = 300)

# 图 2: 个体连线图 —— 红线表示组均值趋势
p2 <- data_agg %>%
  ggplot(aes(x = condition, y = mean_rt, group = subject_id)) +
  geom_line(alpha = 0.3, linewidth = 0.5) +
  geom_point(alpha = 0.3, size = 1) +
  stat_summary(aes(group = 1), fun = mean,
               geom = "line", linewidth = 1.5, color = "red") +
  stat_summary(fun = mean,
               geom = "point", size = 3, color = "red") +
  labs(
    title = "Stroop: 个体 RT 变化",
    x     = "条件",
    y     = "平均反应时 (ms)"
  ) +
  theme_minimal(base_size = 12)
ggsave(file.path(save_path, "fig2_individual.png"),
       p2, width = 6, height = 5, dpi = 300)

# ============================================================
# 第 10 步：环境信息 —— 确保完全可重复
# ============================================================
cat("\n========== 环境信息 ==========\n")
cat(sprintf("分析生成时间: %s\n", Sys.time()))
cat(sprintf("R 版本: %s\n", R.version.string))
for (pkg in c("tidyverse", "effectsize", "ggplot2", "ggrain")) {
  cat(sprintf("  %s: %s\n", pkg, as.character(packageVersion(pkg))))
}
sessionInfo()
