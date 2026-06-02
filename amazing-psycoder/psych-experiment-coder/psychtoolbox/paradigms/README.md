# Psychtoolbox Paradigms

> **Layer 3**: 范式参考文件 — 5 个完整实验范式，包含实验逻辑和可运行 MATLAB 代码。

## 范式索引

| 范式 | 文件 | 说明 |
|------|------|------|
| Stroop | [stroop.md](stroop.md) | 颜色-词 Stroop 任务。词（Red/Green/Blue）× 墨水颜色独立操控，方向键反应，RT+正确率记录 |
| Posner Cuing | [posner-cuing-experiment.md](posner-cuing-experiment.md) | 空间线索任务。Gabor 目标，线索有效性操控（contingent/non-contingent），数据保存到 tab 分隔文件 |
| Orientation Threshold | [orientation-threshold.md](orientation-threshold.md) | 2AFC 朝向辨别阈限测量。恒定刺激法，程序化 Gabor，心理测量函数拟合 |
| Likert Scale | [likert-scale.md](likert-scale.md) | 7 点 Likert 量表。鼠标悬停放大+点击选中，颜色梯度反馈（蓝→红），响应收集组件 |
| Slider | [coolness-slider.md](coolness-slider.md) | 连续滑动条评分。Click-and-drag 交互，0-100% 实时百分比显示，动态颜色变化 |

## 类型说明

- **完整实验范式**（Stroop、Posner Cuing、Orientation Threshold）：包含 trial 循环、条件矩阵、数据记录、完整的实验逻辑
- **响应收集组件**（Likert Scale、Slider）：交互式 UI 组件，可作为子组件嵌入更大的实验中

## 文件结构

> **重要：范式 ≠ API 参考。** 以下文件中嵌入的 MATLAB 代码示例来自 Peter Scarfe 的 PTB 教程，使用教学级 API（如 `KbCheck`）。**生成实验代码时，API 模式以 [spec/README.md](../spec/README.md) 的 Canonical Code Skeleton 为准**（`KbQueueCheck` 替代 `KbCheck`、`VBLTimestamp` 替代 `GetSecs`、`try/catch/sca` 替代裸 `sca`）。范式文件仅提供实验逻辑：窗口序列、条件结构、正确性规则。

每个范式文件 `.md` 包含：
- 实验描述与设计逻辑
- 窗口/屏幕序列
- 完整可运行 MATLAB 代码
