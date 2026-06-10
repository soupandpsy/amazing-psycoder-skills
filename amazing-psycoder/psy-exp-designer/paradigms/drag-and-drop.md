# Drag and Drop Puzzle Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/drag_and_drop) · PsychoJS

## When to Use

User mentions: Drag and drop, puzzle task, pattern matching, spatial arrangement, 拖放任务, 拼图任务. A pattern-matching puzzle task using drag-and-drop interaction, demonstrating mouse-based stimulus manipulation for spatial reasoning, problem-solving, or visuospatial ability assessment.

## Core Logic

Participants view a target pattern (e.g., a black-and-white design) displayed above an empty grid. Draggable puzzle pieces (black and white squares) are positioned around the grid. Participants must click and drag each piece from its starting position into the correct grid cell to recreate the target pattern.

**Trial structure**: target design image displayed above grid → participant drags black/white pieces into grid cells → when satisfied, clicks "Continue" button → feedback (correct/incorrect + completion time) → next trial. The condition file (`conditions.xlsx`) defines the target design image and the correct arrangement (which cells should be black vs. white).

**Drag-and-drop mechanics**: PsychoJS `visual.ImageStim` components are created with `setDraggable(true)`. Piece positions are tracked via each stimulus's `.pos` property. The grid is defined using pixel coordinates (`units: 'pix'` for precise positioning). Each trial has 9 grid cells (3x3 arrangement), each requiring either a black or white piece.

**Accuracy verification**: When the participant clicks "Continue", the code compares the final dragged positions of black and white pieces against the target pattern cells defined in the condition file columns (`a1` through `a9`, or equivalent grid labels). The trial is marked correct only if all pieces are in their correct positions.

**Completion time**: A trial timer runs from trial onset until the "Continue" button is clicked. Time taken and accuracy are displayed as feedback.

## Must Confirm

- **Grid layout**: 3x3 grid (9 cells), or different size? Rectangular or irregular?
- **Puzzle complexity**: Black/white binary pieces, color pieces, or more complex pattern pieces?
- **Target designs**: Pre-made design images or programmatically generated patterns?
- **Trial count**: How many puzzles to solve?
- **Interaction mode**: Mouse drag-and-drop, touchscreen, or both?
- **Feedback**: Full accuracy feedback (all-or-nothing) or partial credit (number of pieces correct)?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Puzzle Assembly          │    │ Feedback                 │    │ ITI                      │
│ Content: target design   │    │ Content: correct/incorrect│   │ Content: blank           │
│   above grid + draggable │    │   + completion time      │    │ Duration: 1000 ms        │
│   black/white pieces     │    │ Duration: 2000 ms        │    │ Response: none           │
│ Duration: self-paced     │    │ Response: none           │    │ Condition: none          │
│   (click Continue to end)│    │ Condition: none          │    │ Data: none               │
│ Response: mouse drag     │    │ Data: none               │    └──────────────────────────┘
│ Condition: {design_id}   │    └──────────────────────────┘
│ Data: piece_positions,   │
│   completion_time        │
└──────────────────────────┘
```

## Data Analysis

Primary measures: completion time (time to solve each puzzle), accuracy (proportion of correctly solved puzzles), and error patterns (which grid cells had incorrect pieces). Analyze learning effects across trials (faster completion on later puzzles). Individual differences in visuospatial ability can be inferred from accuracy and speed. Mouse trajectories (piece drag paths) provide process-tracing data on solution strategies.

## References

This paradigm demonstrates drag-and-drop interaction capabilities in PsychoJS/PsychoPy. Adaptable to visuospatial ability testing, puzzle-solving research, and any paradigm requiring spatial manipulation of on-screen elements.

---

## Do Not Assume

- Do not assume the grid is always 3x3 — the grid size (e.g., 2x2, 4x4, irregular shapes) should be explicitly confirmed with the user before generation
- Do not assume binary black/white pieces — some variants use colored pieces, patterned pieces, or pieces with varying shapes; the piece type directly affects stimulus creation and condition file structure
- Do not assume pieces return to their original position after an incorrect drop — some implementations allow pieces to snap into the nearest grid cell, while others reject invalid placements
- Do not assume the "Continue" button is always present — some paradigms auto-advance after all pieces are placed, while others require explicit confirmation; this affects the trial termination logic
- Do not assume target designs come from image files — some experiments generate target patterns programmatically (e.g., random placement of colored squares), which eliminates the need for external image assets
- Do not assume mouse-only interaction — touchscreen compatibility may be required, which affects event handling and stimulus sizing (larger touch targets needed)

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| design_id | str | 目标图案的标识符，对应图片文件名或程序化生成参数 |
| grid_rows | int | 网格行数 |
| grid_cols | int | 网格列数 |
| solution | str | 正确答案编码，如 `"B,W,B;W,B,W;B,W,B"` 表示每个格子的颜色（B=黑色, W=白色），按行排列 |

## Variants

- **标准拖拽拼图 (Standard Drag-and-Drop Puzzle)**: 参与者从备选区拖拽图形块到网格中，完成目标图案的复现。多见于空间认知和问题解决研究。详见本文件主体描述。
- **自由排序拖拽 (Free-Sorting Drag-and-Drop)**: 参与者将屏幕上散落的项目拖拽到任意分组区域中，无固定的正确位置。常用于分类任务和概念形成研究。可参考 [free-sorting.md](free-sorting.md)。
- **时间限制拖拽 (Timed Drag-and-Drop)**: 在标准拖拽拼图基础上增加了时间压力，参与者必须在限定时间内完成拖拽操作，超时则自动提交当前状态。适合研究决策速度和压力下的空间推理。

---

## Example

### User Request

> "我想做一个拖拽拼图实验。屏幕上显示一个3x3的黑白目标图案，图案下方是一个3x3的空白网格。旁边有5个黑色方块和4个白色方块可以拖拽。参与者把方块拖到正确的位置后点击'提交'按钮。一共10个试次，每次的目标图案不同。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Puzzle Assembly          │    │ Feedback                 │    │ ITI                      │
│ Content: 目标图案(上)    │    │ Content: 正确/错误       │    │ Content: 空白            │
│   + 3×3空白网格(中)      │    │   + 完成时间             │    │ Duration: 800 ms         │
│   + 5黑4白可拖拽方块(侧) │    │ Duration: 2000 ms        │    │ Response: none           │
│ Duration: 自定步调        │    │ Response: none           │    │ Condition: none          │
│   (点击提交按钮结束)      │    │ Condition: none          │    │ Data: none               │
│ Response: 鼠标拖拽        │    │ Data: none               │    └──────────────────────────┘
│ Condition: {design_id}   │    └──────────────────────────┘
│ Data: 每格最终状态,      │
│   完成时间, 提交前移动次数│
└──────────────────────────┘
```

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 3×3 黑白拖拽拼图任务 |
| 平台 | PsychoPy |
| 任务类型 | Drag-and-Drop Puzzle（空间拼图） |
| 网格尺寸 | 3×3（9个格子） |
| 方块类型 | 黑色方块 × 5，白色方块 × 4 |
| 交互方式 | 鼠标拖拽到网格指定位置 |
| 提交方式 | 点击"提交"按钮 |
| 试次数量 | 10 个试次 |
| 目标图案 | 每个试次不同（需提供 10 张目标图案图片或程序化定义） |

### Missing Information

1. 目标图案来源未说明 — 需要用户提供 10 张目标图案图片，或确认是否由程序随机生成黑白排列
2. 练习试次未提及 — 是否需要练习阶段？练习试次数量？
3. 指导语内容未说明 — 需要用户提供中文字幕或确认使用默认指导语（"请将方块拖到正确位置"）

### Critical Assumptions

- 方块拖放到大致正确的网格位置即视为有效放置（允许一定的位置容差，如 ±20 像素），不需要像素级精确对齐
- 反馈仅显示正确/错误和完成时间，不显示部分得分（全对或全错评判）
- 目标图案以图片文件形式提供（存放在 `stimuli/` 目录下），而非程序化生成

### Code Architecture

```
drag_puzzle.py
├── 实验参数（网格尺寸、方块颜色、试次数量、计时设置）
├── 窗口初始化（单位设为像素以精确定位）
├── 预加载刺激材料（目标图案图片、网格线条、可拖拽方块）
├── 条件文件读取（design_id → 目标图片 + 正确答案编码）
├── 试次循环:
│   ├── 绘制网格线条（3×3 参考线）
│   ├── 显示目标图案（网格上方居中）
│   ├── 创建可拖拽方块（初始位置在网格周围随机排列）
│   ├── 等待拖拽交互（自定步调，监听拖拽事件和提交按钮）
│   ├── 记录每格最终状态和完成时间
│   ├── 比对答案（与 condition 中的 solution 编码比对）
│   ├── 显示反馈（正确/错误 + 用时，持续 2000 ms）
│   └── ITI（800 ms 空白）
├── 数据保存：try/finally 结构，增量写入 CSV
└── 结束界面
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| design_id | str | 当前试次的目标图案标识 |
| grid_state | str | 提交时各格子的实际状态编码（如 `"B,W,B;W,B,W;B,W,B"`） |
| acc | int | 是否完全正确（1 = 全对，0 = 有错误） |
| completion_time | float | 从试次开始到点击提交的耗时（秒） |
| n_moves | int | 拖拽操作的总次数（方块被移动的次数） |
