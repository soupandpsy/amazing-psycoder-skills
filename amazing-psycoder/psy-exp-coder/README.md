# psy-exp-coder — 代码生成层

> **版本**: v1.3 | **角色**: 接收完整的 config YAML + 条件表，产出可直接运行采集数据的实验代码。不设计实验 — 那是编排层的工作。amazing-psycoder 子技能。

## 代码生成流程（跨平台通用）

```
config.yaml + 条件.xlsx + 刺激文件/
        │
        ▼
  1. 选定平台 (PsychoPy / jsPsych / Psychtoolbox)
        │
        ▼
  2. 打开平台 spec → 复制 Canonical Code Skeleton
        │
        ▼
  3. 打开平台 mapping → 按 config 字段逐项映射为代码结构
        │
        ▼
  4. 打开范式文件 → 提取窗口序列、条件结构、正确性规则
        │
        ▼
  5. 将范式逻辑填入骨架 → 生成完整代码
        │
        ▼
  6. 运行 Quality Gate（9 项检查）→ 修复 → 交付
```

每一步的详细规则见 [SKILL.md](SKILL.md)。

## 12 步代码模板（所有平台、所有范式通用）

每个生成的实验脚本，无论平台和范式，都按以下结构组织：

```
 1. Imports / 依赖
 2. 实验参数（所有可调参数置顶，含 FONT_CONFIG 开关）
 3. 显示设置（窗口/屏幕/画布）
 4. 刺激预加载（循环外，禁止循环内 I/O）
 5. 条件文件加载 / 条件数组生成
 6. 辅助函数
 7. 指导语 Routine
 8. 练习 Routine（含反馈）
 9. 主实验循环
    a. Block 级设置
    b. Trial 随机化
    c. 每 trial: 注视点 → 刺激 → 响应 → 反馈 → ITI
    d. Block 级反馈（如适用）
10. 数据保存（增量写入，try/finally 保护）
11. 清理 / 退出（始终包含 Escape / 中止处理）
12. 打包为平台文件 + 生成 README
```

各平台的实现细节： [PsychoPy](psychopy/README.md) · [jsPsych](jspsych/README.md) · [Psychtoolbox](psychtoolbox/README.md)

## 4 层知识体系

```
SKILL.md           ← 代码生成流程 + 质量门（跨平台）
 ├── 平台 README    ← 平台特定的生成规则 + 强制 API
 │    ├── spec/     ← L1: API 模式 + 反模式 + Canonical Skeleton
 │    ├── mapping/  ← L2: Config YAML → 代码结构映射
 │    ├── paradigms/ ← L3: 范式参考（实验逻辑，非 API 参考）
 │    └── demo/_raw/ ← L4: 原始代码参考（仅参考逻辑）
```

层级冲突时：**Canonical Skeleton > spec 反模式 > mapping 规则 > 范式逻辑 > demo 代码**

## 平台支持

| 平台 | 状态 | 何时使用 |
|------|------|---------|
| **PsychoPy** (2024.x+, Python 3.10+) | 4层完整 — config→代码自动生成 | 本地实验，需要精确 RT 计时 |
| **jsPsych** (7.x, JavaScript) | 4层完整 — config→代码自动生成 | 在线实验，Pavlovia 部署 |
| **Psychtoolbox** (3.0.21+, MATLAB) | 4层完整 — config→代码自动生成 | MATLAB 实验室，需要 GPU 级控制 |

## Quality Gate（生成后强制检查）

| # | 检查项 | 验证方法 |
|---|--------|---------|
| 1 | **骨架一致** | 代码结构与平台 spec 的 Canonical Skeleton 一致 |
| 2 | **无反模式** | 扫描代码，任何 spec 反模式表中的模式 = 拒绝 |
| 3 | **范式 API 已覆盖** | 范式文件只提供了逻辑，API 模式来自 spec |
| 4 | **参数置顶** | 所有可调值在参数区，逻辑代码中无魔数 |
| 5 | **Escape 全覆盖** | 每个含 Flip/flip/绘制的 while 循环有 Escape 检查 |
| 6 | **RT 来源正确** | PsychoPy=`key.rt`, PTB=`firstPress-VBLTimestamp`, jsPsych=`data.rt` |
| 7 | **增量保存** | 崩溃后已完成的 trial 数据留存 |
| 8 | **预加载在外** | 循环内无 `imread`/`MakeTexture`/`ImageStim()` 构造 |
| 9 | **FONT_CONFIG** | 中文实验 → 参数区有 FONT_AUTO_DETECT/MANUAL_FONT_PATH 开关 |

## 入口文件

| 入口 | 何时读 |
|------|--------|
| [SKILL.md](SKILL.md) | 了解代码生成全流程 + 质量门 + 输出格式 |
| [psychopy/README.md](psychopy/README.md) | 生成 PsychoPy 代码时 |
| [jspsych/README.md](jspsych/README.md) | 生成 jsPsych 代码时 |
| [psychtoolbox/README.md](psychtoolbox/README.md) | 生成 Psychtoolbox 代码时 |
