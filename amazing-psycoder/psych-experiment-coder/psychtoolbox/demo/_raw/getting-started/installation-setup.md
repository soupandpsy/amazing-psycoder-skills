# PTB 安装与环境配置

> 来源: 蒋挺老师知乎 PTB 教程  
> 归类: `demo/_raw/getting-started/` — L4 入门参考
> 参考层级: L4 demo（仅参考安装流程，API 模式以 spec/README.md 为准）

## 环境要求

| 环境类型 | 推荐版本 | 必须启用组件 |
|---------|---------|------------|
| MATLAB | R2018a - R2023b | OpenGL, Java Runtime |
| GNU Octave | ≥6.4 | Graphics Toolkit: gnuplot 或 qt |
| Windows | 10+ | 显卡驱动正常加载 |
| macOS | 10.14+ | Xcode CLI Tools |
| Linux | Kernel ≥5.4 | build-essential, libx11-dev, libgl1-mesa-dev |

## 安装步骤

### 1. 克隆仓库

```matlab
targetDir = '~/Documents/Psychtoolbox';
mkdir(targetDir);
system(['git clone https://github.com/Psychtoolbox-3/Psychtoolbox-3.git ' targetDir]);
addpath(genpath(fullfile(targetDir)));
```

### 2. 配置 MEX 编译器

```matlab
mex -setup C++
% 选择编译器: MinGW-w64 (Windows) / Xcode CLI (macOS) / gcc/g++ (Linux)
```

### 3. 运行首次初始化

```matlab
PsychtoolboxSetup;
```

### 4. 验证安装

```matlab
ver('psychtoolbox')          % 应显示版本号和构建日期
[win, rect] = Screen('OpenWindow', 0, [0 0 0]);
wait(1);
Screen('CloseAll');
```

## 常见安装错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `Undefined function 'PsychtoolboxSetup'` | 路径未添加 | `addpath(genpath('~/Documents/Psychtoolbox'))` |
| `Invalid MEX-file` | MEX 未配置 | `mex -setup C++` |
| MEX 编译失败 (Linux) | 缺少开发库 | `sudo apt-get install build-essential libx11-dev libgl1-mesa-dev` |
| 权限不足 | 无法写入系统路径 | 安装到用户家目录 + `setenv('PSYCHTOOLBOX_ROOT', '~/Documents/Psychtoolbox')` |

## 系统级性能优化

| 干扰源 | 影响机制 | 推荐对策 |
|-------|---------|----------|
| 屏幕保护程序 | 触发显示器休眠 | 实验前禁用 |
| 后台更新 | CPU 占用突增 | 关闭自动更新 |
| 动画效果 | 图形管线阻塞 | 切换至经典主题 (Windows: 调整为最佳性能) |
| 笔记本节能模式 | 降低 GPU 频率 | 插电并设为高性能 |
| macOS 通知 | 抢占线程 | 关闭通知中心 |
| DWM 桌面合成 (Windows) | Flip 无法精确同步 VBLANK | 控制面板 > 调整为最佳性能 |

## 双显卡系统 GPU 绑定

在同时拥有集成显卡和独立显卡的笔记本上，需强制 MATLAB 使用高性能 GPU：

- **Windows**: NVIDIA 控制面板 → 设置 MATLAB 为"高性能 NVIDIA 处理器"
- **macOS**: 使用 `gpuDevice()` 检查当前活动 GPU
- **Linux**: `export __NV_PRIME_RENDER_OFFLOAD=1 && matlab -nodesktop`

```matlab
% 运行时检查当前 GPU
info = Screen('GetWindowInfo', win);
if contains(info.Renderer, 'Intel')
    warning('Running on integrated GPU. Consider switching to discrete.');
end
```

## 时钟精度验证

```matlab
t0 = GetSecs;
for i = 1:100
    t(i) = GetSecs;
end
dt = diff(t);
fprintf('Min interval: %.6f s | Max: %.6f s | Jitter: %.6f s\n', min(dt), max(dt), std(dt));
```

理想情况下连续调用 `GetSecs` 的时间差应在微秒级别（< 100 μs），且标准差极小。若抖动超过 1 ms，则可能存在中断风暴或调度延迟问题。
