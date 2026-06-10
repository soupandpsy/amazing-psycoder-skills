# Psychtoolbox (MATLAB)

> **状态**: 生成流程与 PsychoPy 一致（统一 Generation Pipeline）。L1 spec + L2 mapping + 5 范式 + 100 demo。

## 生成代码流程（与 PsychoPy 统一，平台特化映射见 mapping/）

```
config.yaml
    │
    ▼
1. 复制 [Canonical Code Skeleton](spec/README.md#11-canonical-code-skeleton)
    │
    ▼
2. 参数区：填入 config 的 display / timing / font / audio
    │
    ▼
3. 刺激预加载：从 config.windows[].content → Screen('MakeTexture') 循环前预创建
    │
    ▼
4. Trial 循环：按 config.windows[] 选择帧循环模式
    → 模式 1: 单帧 Flip（固定时长静态刺激）
    → 模式 2: for 循环 Flip（帧精确控制）
    → 模式 3: KbQueue 响应循环（生产推荐）
    → 详情见 [mapping/README.md §三种帧循环模式](mapping/README.md#窗口事件的-ptb-帧循环模式)
    │
    ▼
5. 响应收集：config.windows[].response → KbQueueCheck + VBLTimestamp RT
    │
    ▼
6. 正确性判断：config.response_rules.correct → strcmp(response, corrAns)
    │
    ▼
7. 数据保存：config.output → fopen/fprintf/fclose 增量写入
    │
    ▼
8. 运行 Quality Gate（9 项）→ 修复 → 交付
```

关键：每个步骤对应的 config 字段映射见 [mapping/README.md](mapping/README.md)。

## 文件结构

```
psychtoolbox/
├── README.md                  ← 本文件
├── spec/                      ← L1: API 规范 + Canonical Skeleton
│   └── README.md              ← KbQueue lifecycle, Flip timing, PsychPortAudio, 18 反模式
├── mapping/                   ← L2: Config → MATLAB 代码映射
│   └── README.md              ← 12步模板 + 3种帧循环 + 音频/条件映射
├── paradigms/                  ← L3: 范式参考（实验逻辑，非 API 参考）
│   ├── README.md              ← 范式索引 + API 醒示
│   └── *.md                   ← 5 个范式文件
└── demo/                      ← L4: 原始代码示例（100 个 .md，按功能分类）
    └── _raw/                  ← 仅参考实验逻辑，API 以 L1 spec 为准
        ├── getting-started/   ← 11 — 安装配置 + 最小窗口 + 精确计时 + 键盘队列
        ├── drawing-shapes/    ← 15 — dots, rectangles, fixation
        ├── animated-shapes/   ← 17 — motion, keyboard/mouse
        ├── textures/          ← 23 — images, Gabors, gratings
        ├── text/              ←  6 — text rendering
        ├── 3d-vr/             ← 19 — OpenGL, stereoscopic
        └── other/             ←  9 — 完整实验 + 伽马校正 + 多屏幕 + 音频等
```

## 层级填充状态

| 层级 | 内容 |
|------|------|
| L1 `spec/` | Canonical Skeleton + API 规范（KbQueue lifecycle, Screen Flip half-IFI rule, PsychPortAudio, try/catch/sca）+ 18 反模式 |
| L2 `mapping/` | 12步模板 PTB 实现 + 3 种帧循环模式 + Config→Code 完整映射 + 音频映射 |
| L3 `paradigms/` | 5 个范式（Stroop, Posner Cuing, Orientation Threshold, Likert Scale, Slider）。**API 模式以 spec 为准，不沿用范式代码中的 KbCheck** |
| L4 `demo/_raw/` | 92 个原始示例（`_raw/` = 仅参考实验逻辑，API 以 L1 spec 为准） — 按功能分类，代码生成时按需查阅 |

## 强制 API 规则

所有生成的 PTB 代码遵守（完整规范见 [spec/README.md](spec/README.md)）：

| 类别 | 必须使用 | 禁止使用 |
|------|---------|---------|
| 键盘输入 | `KbQueueCreate` + `KbQueueStart` + `KbQueueCheck` | `KbCheck` / `KbWait`（用于 RT） |
| RT 起点 | `VBLTimestamp`（`Screen('Flip')` 返回值） | `GetSecs` |
| RT 计算 | `(min(firstPress) - stimOnset) * 1000` | `secs - tStimFlip` |
| 帧 Timing | `vbl + (waitframes - 0.5) * ifi` | `WaitSecs()`（实验计时） |
| 每 trial 清队列 | `KbQueueFlush([], 2)` | 不清队列导致前 trial 按键残留 |
| 错误处理 | `try/catch/sca/Priority(0)/ShowCursor` | 裸 `sca` |
| 刺激预加载 | `Screen('MakeTexture')` 在循环前 | `imread` 在 trial 内 |
| 注视点 | `Screen('DrawLines')` 十字 | `Screen('DrawText', '+')` |
| 数据保存 | `fopen/fprintf/fclose` 增量写入 | workspace 内矩阵（崩溃=全丢） |
| 同步测试 | `SkipSyncTests, 0` | 跳过 SyncTests |

## PTB vs PsychoPy（概念对应）

用于从 PsychoPy 切换过来的用户快速定位 PTB 等价 API：

| 概念 | Psychtoolbox | PsychoPy |
|------|-------------|----------|
| 窗口创建 | `PsychImaging('OpenWindow', ...)` | `visual.Window(...)` |
| 翻页 | `Screen('Flip', window, when)` | `win.flip()` |
| 帧间隔 | `Screen('GetFlipInterval')` → `ifi` | `win.getFutureFlipTime()` |
| RT 键盘 | `KbQueueCreate`/`KbQueueCheck` | `keyboard.Keyboard(backend='ptb')` |
| RT 获取 | `firstPress - VBLTimestamp` | `key.rt` |
| 文本渲染 | `DrawFormattedText` / `Screen('DrawText')` | `TextBox2` / `TextStim` |
| 图片 | `imread` + `Screen('MakeTexture')` | `visual.ImageStim()` |
| 音频 | `PsychPortAudio`（亚毫秒延迟） | `sound.Sound`（PTB backend） |
| 数据保存 | `fopen`/`fprintf`/`fclose` | `csv.DictWriter` + `flush` |
| 错误处理 | `try/catch/sca` | `try/finally/win.close()` |
| Gabor | `CreateProceduralGabor`（GPU shader） | `visual.GratingStim` |

## 范式差异速查

不同范式在 PTB 上的实现要点：

| 范式 | 帧循环模式 | 响应方式 | 特殊逻辑 |
|------|----------|---------|---------|
| Stroop | 模式 3（KbQueue） | 方向键 → 颜色映射 | `DrawFormattedText` 动态颜色 |
| Posner Cuing | 模式 2（for Flip） | KbQueue 轮询 | `CreateProceduralGabor` + cue validity |
| Orientation Threshold | 模式 2 | 2AFC 左/右键 | 恒定刺激法 + psychometric function |
| Likert Scale | 模式 2 | 鼠标交互 | 悬停放大 + 点击选中 |
| Slider | 模式 2 | 鼠标 drag | 连续拖动 + 实时百分比 |

详细代码模板见 [mapping/README.md §窗口事件帧循环模式](mapping/README.md#窗口事件的-ptb-帧循环模式)。
