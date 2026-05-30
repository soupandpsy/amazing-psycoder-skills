# 伽马校正与色彩空间管理

> 来源: 蒋挺老师知乎 PTB 教程 §3.3.3  
> 归类: `demo/_raw/other/` — L4 参考
> 参考层级: L4 demo（生成代码使用 spec/README.md §2.2 色彩规范）

## 原理

Psychtoolbox 默认使用线性 RGB 色彩空间，但大多数显示器具有非线性响应曲线（伽马效应）。未校正的颜色会导致亮度感知失真。

假设目标呈现 50% 亮度灰度：
```matlab
linear_gray = 0.5;                           % 线性值
actual_displayed = linear_gray ^ (1/2.2);    % 未经校正，实际显示更暗
```

## 反向伽马校正

```matlab
gamma = 2.2;
target_luminance = 0.5;
corrected_value = target_luminance ^ gamma;   % 预补偿
Screen('FillRect', win, corrected_value, rect);
```

## LoadNormalizedGammaTable（推荐）

通过光度计测量 LUT 后加载：

```matlab
lut_size = 256;
gamma = 2.2;
r_lut = (linspace(0, 1, lut_size)') .^ gamma;
g_lut = r_lut;
b_lut = r_lut;

Screen('LoadNormalizedGammaTable', win, [r_lut, g_lut, b_lut]);
```

一旦加载，所有后续颜色值都自动经过校正路径。

## 常见显示器伽马参考值

| 显示器类型 | 典型伽马值 | 备注 |
|-----------|----------|------|
| CRT | 2.2 ~ 2.5 | 接近理想幂律 |
| LCD (sRGB) | 2.2 | 标准配置 |
| OLED | 2.0 ~ 2.1 | 更高对比度 |
| 投影仪 | 1.8 ~ 2.0 | 需单独校准 |

## 反模式标注

| 问题 | 规范替代 |
|------|---------|
| 未校正的线性 RGB 值直接用于亮度关键实验 | 实验前加载 Gamma LUT 或使用校正后的颜色值 |
| 假设所有显示器 Gamma = 2.2 | 用光度计实测或至少查询显示器规格 |
