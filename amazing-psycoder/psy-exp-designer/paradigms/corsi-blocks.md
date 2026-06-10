# Corsi Block-Tapping Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/corsi_blocks) · PsychoJS

## When to Use

User mentions: Corsi blocks, Corsi span, spatial working memory, visuospatial span, 科西方块, 空间工作记忆. Measures visuospatial short-term/working memory span by requiring participants to reproduce a sequence of spatial locations.

## Core Logic

Nine blocks are arranged in an irregular spatial pattern on screen (the classic Corsi board layout, avoiding a regular grid to prevent verbal encoding). On each trial, a subset of blocks is highlighted (flashed) one at a time in a random sequence. The participant must reproduce the sequence by clicking the blocks in the same order (forward span).

**Two-phase within-trial structure**:
1. **Presentation phase**: Blocks flash in sequence with a fixed stimulus onset asynchrony. Each block briefly changes color (e.g., from dark to light) to indicate selection.
2. **Recall phase**: The participant clicks blocks with the mouse to reproduce the sequence. Mouse position is tracked via `eventManager.getMousePos()` to detect clicks on block locations.

**Adaptive sequencing**: The task is self-contained in a single routine that programmatically generates sequences. Sequence length starts at 2 and increases with successful reproduction (span increases) or decreases with failure (span decreases). The task continues until a stopping criterion is met (e.g., failure on both attempts at a given span length).

**Span scoring**: The traditional method gives two attempts at each sequence length. The span score is the longest sequence length for which at least one trial was correctly reproduced. An alternative is the total correct trials score (sum of all correctly reproduced sequences). Typical forward spans are 5–7 items for healthy young adults; backward spans (reverse order recall) are typically 1–2 items shorter and tap the central executive.

**No condition files**: Unlike most PsychoJS experiments, the Corsi task does not use a condition spreadsheet. All sequence generation, presentation timing, and response collection logic is implemented programmatically in code components.

## Must Confirm

- **Direction**: Forward span (same order) or backward span (reverse order), or both?
- **Block count**: Classic 9-block Corsi board or custom arrangement?
- **Scoring method**: Strict span (longest length with at least 1 correct) or total correct?
- **Stopping rule**: Two attempts per span, or different rule?
- **Starting length**: Sequence length 2, or custom?
- **Recall modality**: Mouse click on screen, or touchscreen tap (different hit detection)?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │
│ Presentation Phase       │    │ Recall Phase             │
│ Content: blocks flash    │    │ Content: 9 blocks static │
│   in sequence            │    │ Duration: until click    │
│ Duration: N * SOA        │    │   (self-paced)           │
│   (SOA ~750-1000 ms)     │    │ Response: mouse clicks   │
│ Response: none           │    │   on blocks              │
│ Condition: {seq_length}  │    │ Condition: none          │
│ Data: sequence presented │    │ Data: sequence clicked,  │
└──────────────────────────┘    │   accuracy               │
                                └──────────────────────────┘
```

## Data Analysis

Primary measures: Corsi span (forward, backward, or both), total correct trials score. Compare to digit span for domain-specific working memory dissociations. Clinical populations (e.g., patients with right-hemisphere lesions, neglect, or ADHD) often show disproportionate Corsi deficits relative to verbal spans. Analyze error types: order errors vs. item omissions vs. intrusions.

## References

Corsi, P. M. (1972). Human memory and the medial temporal region of the brain. *Dissertation Abstracts International, 34*(2-B), 891.

Kessels, R. P. C., van Zandvoort, M. J. E., Postma, A., Kappelle, L. J., & de Haan, E. H. F. (2000). The Corsi block-tapping task: Standardization and normative data. *Applied Neuropsychology, 7*(4), 252–258. https://doi.org/10.1207/S15324826AN0704_8

## Do Not Assume

- Do not assume recall direction is forward-only without confirmation. 逆向回忆（backward Corsi）同样常见，且涉及不同的认知过程——逆向需要中央执行功能的参与（信息的保持和操纵），而正向主要测量视空间存储。确认是正向、逆向还是两者都包含。
- Do not assume the classic 9-block Corsi布局 without confirmation. 虽然9块是最经典的配置，但部分研究使用简化版（如5块用于儿童或严重认知障碍患者）或自定义空间排列以适应特殊人群或屏幕尺寸。
- Do not assume mouse click is the only valid response modality. 触摸屏点击在平板实验和临床床边评估中同样常见，其点击检测逻辑与鼠标不同（直接触屏坐标 vs. 鼠标光标跟踪+点击事件），需要不同的hit detection实现。
- Do not assume a fixed SOA across studies without confirmation. 典型SOA为750-1000 ms，但部分研究使用500 ms或1500 ms。更快的SOA增加任务难度，影响编码深度，需与现有文献对齐。
- Do not assume the stopping rule is always two-attempts-per-span. 有些实现使用单次尝试、三次尝试、或固定总试次数（如每个span长度固定4个试次）。停止规则直接影响span分数的计算方式和统计效力。
- Do not assume condition files are used. 与其他大多数PsychoJS实验不同，Corsi任务通常完全通过代码生成序列、控制呈现时序和收集响应，不使用条件电子表格。

## Condition File Columns

Corsi任务通常**不使用条件文件**——所有序列生成、呈现时序和响应收集均在代码组件中以编程方式实现。如果出于实验设计需要创建条件文件（例如固定跨被试序列以实现精确复制），最简列如下：

| Column | Type | Description |
|--------|------|-------------|
| sequence | str | 本次trial的块序列，用逗号分隔的块编号列表（如 `"3,7,2,5"`） |
| span_length | int | 序列长度（如 4） |
| direction | str | `"forward"` 或 `"backward"` |

## Variants

### 逆向Corsi（Backward Corsi）

参与者需要以**相反顺序**再现呈现的序列。与正向Corsi相比，逆向Corsi对中央执行功能的要求更高（需要保持并操纵信息），典型逆向span比正向span低1-2个项。在临床群体中，逆向Corsi对额叶功能缺陷更敏感，常与stroop任务（见 [stroop.md](stroop.md)）和n-back任务（见 [n-back.md](n-back.md)）联合使用以全面评估执行功能。

### Corsi超span学习（Corsi Supraspan Learning）

在固定序列长度（通常设置为被试span+1或span+2）下重复呈现同一序列，测量达到一次完全正确再现所需的学习次数。这一变体评估视空间**学习**能力而非简单的短时记忆span，对海马和内侧颞叶功能更敏感。

### 触摸屏/平板Corsi（Touchscreen/Tablet Corsi）

针对移动设备或平板电脑的适配版本，使用触摸事件替代鼠标点击。除了输入方式差异外，还需考虑手指遮挡问题（触摸时手指可能遮挡目标块）、块尺寸的物理大小适配、以及不同屏幕分辨率的坐标校准。9块布局在小平板上可能拥挤，有时缩减为5块或7块版本。

---

## Example

### User Request

> "我要做一个Corsi方块任务实验。屏幕上呈现9个不规则的方块，每个trial依次高亮其中几个方块（从长度2开始）。高亮结束后，被试需要用鼠标按相同顺序点击刚才高亮的方块。每个序列长度有2次尝试机会，如果2次都错了就停止。如果至少1次正确，序列长度+1继续。正向回忆。高亮每个方块750 ms，间隔500 ms。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │
│ 呈现阶段                  │    │ 回忆阶段                  │
│ Content: 9个方块静态     │    │ Content: 9个方块静态     │
│   依次高亮N个方块         │    │   （无高亮）             │
│ Duration: N × 750 ms     │    │ Duration: 直到点击完成    │
│   + (N-1) × 500 ms ISI   │    │   （自定步速）           │
│ Response: none           │    │ Response: 鼠标点击方块   │
│ Condition: {span_length} │    │ Condition: none          │
│ Data: 呈现序列           │    │ Data: 点击序列, acc      │
└──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | Condition | Data |
|--------|---------|----------|----------|-----------|------|
| 呈现阶段 | 9个方块，依次高亮 | N×750ms呈现 + (N-1)×500ms间隔 | none | {span_length} | presented_sequence |
| 回忆阶段 | 9个方块静态 | 自定步速（直到点击N次） | 鼠标点击方块 | none | clicked_sequence, acc |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Corsi Block-Tapping Task |
| Platform | PsychoPy |
| Task type | Corsi blocks (visuospatial working memory span) |
| Block count | 9 (classic Corsi layout) |
| Recall direction | Forward (same order) |
| Starting span length | 2 |
| Attempts per span | 2 |
| Stopping rule | Stop when both attempts at a given span fail |
| Highlight duration | 750 ms per block |
| Inter-block interval | 500 ms |
| Response modality | Mouse click on blocks |
| Condition file | None (fully programmatic) |

### Missing Information

1. 方块的具体屏幕位置未指定 → 默认使用经典Corsi 9块不规则布局坐标（需确认屏幕分辨率以缩放坐标）
2. 指导语内容未说明 → 需询问：指导语措辞、是否包含示例演示
3. 是否收集练习数据未明确 → 需确认：是否包含练习阶段？练习数据是否保存？

### Critical Assumptions

- 使用经典9块Corsi不规则布局（非网格排列，防止言语编码）
- 正向回忆（非逆向），鼠标点击输入，无时间限制的回忆阶段
- 无练习阶段——直接进入正式测试；若用户期望练习，需补充
- Span分数 = 至少1次正确的最长序列长度（经典计分法）
- 序列中同一方块不重复出现（无放回抽样）

### Expected Code Architecture

```
corsi_blocks.py
├── Parameters (n_blocks=9, start_span=2, max_attempts=2,
│               highlight_dur=0.75, isi=0.5)
├── Window setup (全屏 or 窗口)
├── Block position definition (classic Corsi 9-block layout)
│   └── List of (x, y) coordinates, scaled to window size
├── Trial generation (programmatic — no condition file):
│   ├── span_length ← 2
│   ├── while stopping criterion not met:
│   │   ├── for attempt in range(2):
│   │   │   ├── Generate random sequence of span_length blocks
│   │   │   ├── 呈现阶段: Highlight each block in sequence
│   │   │   │   (highlight_dur + isi between)
│   │   │   ├── 回忆阶段: Wait for N mouse clicks on blocks
│   │   │   ├── Score: compare clicked vs. presented sequence
│   │   │   └── Record: span_length, attempt, sequence, acc
│   │   ├── If at least 1 correct: span_length += 1
│   │   ├── Else: stop and compute final span score
│   └── End screen with span score
├── Data: try/finally CSV with incremental writes
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| span_length | int | 当前序列长度 |
| attempt | int | 当前长度下的第几次尝试 (1 or 2) |
| presented_sequence | str | 呈现的方块序列（如 `"3,7,2,5"`） |
| clicked_sequence | str | 被试点击的方块序列（如 `"3,7,2,5"`） |
| acc | int | 1 = 完全正确（顺序一致），0 = 错误 |
| span_score | float | 最终span分数（任务结束后统一写入） |
