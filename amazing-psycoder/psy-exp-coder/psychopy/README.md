# PsychoPy Platform

> **状态**: 生成流程与其他平台统一（同一 8 步 Config→Code 流程）。28 个范式参考，45 个 demo。

## 生成代码流程（平台特化映射见 mapping/）

```
config.yaml
    │
    ▼
1. 复制 [Canonical Code Skeleton](spec/README.md#19-canonical-code-skeleton)
    │
    ▼
2. 参数区：填入 config 的 display / timing / font / audio / participant_info
    │
    ▼
3. 刺激预加载：从 config.windows[].content 提取 {col} → 创建 TextBox2/ImageStim
    │
    ▼
4. Trial 循环：按 config.windows[] 选择窗口模式（合并/顺序/定时）
    → 详情见 [mapping/README.md §Windows[] → 三种窗口模式](mapping/README.md#windows--trial-事件循环三种窗口模式)
    │
    ▼
5. 响应收集：config.windows[].response → PTB keyboard + getKeys(waitRelease=False)
    │
    ▼
6. 正确性判断：config.response_rules.correct → 双重判断（循环内+循环外）
    │
    ▼
7. 数据保存：config.output → ExperimentHandler + TrialHandler + 增量 flush
    │
    ▼
8. 运行 Quality Gate（10 项）→ 修复 → 交付
```

关键：每个步骤对应的 config 字段映射见 [mapping/README.md](mapping/README.md)。

## 文件结构

```
psychopy/
├── README.md              ← 本文件
├── spec/                  ← L1: API 规范 + Canonical Skeleton
│   └── README.md
├── mapping/               ← L2: Config → PsychoPy 代码映射
│   └── README.md
├── paradigms/              ← L3: 范式参考（实验逻辑，非 API 参考）
│   ├── README.md          ← 范式索引 + API 醒示
│   └── *.md               ← 28 个范式文件（不含索引/README）
└── demo/                  ← L4: Pavlovia 原始导出
    └── _raw/              ← 45 个 .py（v3.1 旧版 API）
```

## 层级填充状态

| 层级 | 内容 |
|------|------|
| L1 `spec/` | Canonical Skeleton + API 规范（PTB keyboard, getFutureFlipTime, callOnFlip, Sound, TextBox2, ExperimentHandler, DlgFromDict）+ 19 反模式 |
| L2 `mapping/` | 三版本差异对照 + 三种窗口模式 + Config→Code 完整映射 + 12步模板实现 + 音频/参与者信息映射 |
| L3 `paradigms/` | 28 个范式 — 实验逻辑参考。**API 模式以 spec 为准，不沿用范式代码中的旧版 API** |
| L4 `demo/` | 45 个 Pavlovia .py — 仅参考实验逻辑 |

## 强制 API 规则

所有生成的 PsychoPy 代码遵守（完整规范见 [spec/README.md](spec/README.md)）：

| 类别 | 必须使用 | 禁止使用 |
|------|---------|---------|
| 时序关键键盘 | 显式选择目标环境支持的 `keyboard.Keyboard` 后端并验证 | 隐式回退却宣称已验证精度 |
| 按键获取 | 需持续刷新/触发/退出处理时用 `kb.getKeys(waitRelease=False)` | 在并行阶段工作尚未完成时使用阻塞等待 |
| RT | 所选后端返回的 `key.rt`，并记录/验证环境 | `kb.clock.getTime()` / `time.time()` 作为按键事件时刻 |
| RT 起点 | `win.callOnFlip(kb.clock.reset)` | 手动 `clock.reset()` before flip |
| 计时 | `CountdownTimer` 循环 + `getFutureFlipTime` | `time.sleep()` / `core.wait()` |
| 音频 | 按固定 runtime 选择 backend/device；循环前创建声音，支持时用 `play(when=)`，目标机测量 onset | 仅凭 backend 或 buffer 参数声称固定精度 |
| 文本 | `TextBox2`（推荐）/ `TextStim` | — |
| 条件字段 | 显式、经 schema 校验的 `trial["field"]` 访问 | `exec()` / `globals()` namespace 注入 |
| 数据保存 | `try/finally` + per-trial flush | 仅实验结束时保存 |
| 退出 | Escape 在 keyList + 每帧检查 | 无 Escape 处理 |

## 范式差异速查

不同范式在 PsychoPy 上的实现差异：

| 范式 | 窗口模式 | 条件结构 | 特殊逻辑 |
|------|---------|---------|---------|
| Stroop | 单 Routine 合并 | word × color 因子设计 | `setColor()` 动态颜色 |
| Go/No-go | 顺序 Routine | go × no-go 比例 | 双重 accuracy，正确计数器 |
| Stop-signal | 定时响应循环 | SSD staircase | `CountdownTimer`，stop signal 中间插入 |
| Dot-probe | 顺序 Routine | cue 位置 × target 位置 | congruency 编码在条件文件 |
| N-back | 顺序 Routine | 程序化序列 | 环缓冲区，lure 检测，d-prime |

详细窗口模板和代码见 [mapping/README.md §范式差异速查](mapping/README.md#范式差异速查)。
