# 多屏幕与多 GPU 环境适配

> 来源: 蒋挺老师知乎 PTB 教程 §2.4  
> 归类: `demo/_raw/other/` — L4 参考
> 推荐层级: 不参与代码生成，仅作为实验配置参考

## 枚举显示器

```matlab
nScreens = Screen('NumDisplays');
for i = 0:nScreens-1
    bounds = Screen('Rect', i);
    fprintf('Screen %d: %d x %d @ (%d,%d)\n', i, ...
        bounds(3), bounds(4), bounds(1), bounds(2));
end
```

编号从 0 开始，0 通常为主屏。创建窗口时指定屏幕索引：

```matlab
win1 = Screen('OpenWindow', 0, [0 0 0]);        % 主屏（被试看）
win2 = Screen('OpenWindow', 1, [255 255 255]);  % 副屏（主试监控）
```

**注意**: 跨屏窗口无法共享 OpenGL 纹理资源，需分别管理。

## 双显卡系统 GPU 绑定

在同时拥有集成显卡（Intel）和独立显卡（NVIDIA）的笔记本上：

```matlab
% 检查当前活动 GPU
info = Screen('GetWindowInfo', win);
if contains(info.Renderer, 'Intel')
    warning('Running on integrated GPU. Switch to discrete.');
end
```

- **Windows**: NVIDIA 控制面板 > 设置 MATLAB 为"高性能 NVIDIA 处理器"
- **Linux**: `export __NV_PRIME_RENDER_OFFLOAD=1 && matlab -nodesktop`

## 多屏刷新率不同步风险

多屏间刷新率可能不同步，导致跨屏实验出现时间偏差。解决方案：
- 确保主、副屏设置为相同刷新率
- 实验数据采集仅使用被试屏幕的 Flip 时间戳

## 副屏复合特效干扰

某些集成显卡无法对副屏关闭复合特效（如 macOS Mission Control 动画）。推荐：
- 副屏仅用于监控，不用于刺激呈现
- 若需双屏呈现刺激，两屏使用相同型号并统一显卡驱动
