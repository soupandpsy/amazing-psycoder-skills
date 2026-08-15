# Canvas Presentation Contract

Use this reference whenever the Designer presents a sequence timeline, phase
decision checklist, cumulative Decision Registry, or final Gate 5 review. The
saved config remains authoritative; these views make its meaning inspectable.

## Sequence-row format

- Show each sequence as an independent row separated by blank lines.
- Show sequences top-to-bottom and windows left-to-right.
- Start with `序列: <name>` plus condition table, cycles, and order policy.
- One cycle traverses every table row once; without a table it executes the window chain once.
- Each window card shows label, content, duration, and response mode.
- Annotate the response window with its RT anchor and recorded data.
- Use `[MISSING]` for unresolved values.
- A sequence name is only a label; never infer runtime behavior from it.
- Show every sequence, including instructions, practice, rest, and end rows.

```text
序列: Trial
  条件表: formal_table · cycles: 1 · order: fixed_random(seed=sub-01)

  ┌─ Fixation ─┐  ┌─ Stimulus ───┐  ┌─ Response ────┐  ┌─ ITI ──────┐
  │ "+"        │  │ "{stimulus}" │  │ "{stimulus}"  │  │ ""         │
  │ 500ms      │→ │ 500ms        │→ │ until_key     │→ │ 500-800ms  │
  │ 无响应     │  │ 无响应       │  │ [f, j, k]     │  │ 无响应     │
  └────────────┘  └──────────────┘  └───────────────┘  └────────────┘
                                            RT: Response onset
                                            数据: rt, key, acc

序列: Start       → 无条件表 · cycles: 1 → 欢迎文字
序列: End         → 无条件表 · cycles: 1 → 感谢文字
```

## Phase decision checklist

```text
## Phase N 设计决策确认清单

| # | 决策项 | 确认值 | 来源 |
|---|--------|--------|------|
| 1 | 注视点持续时间 | 500ms | 用户确认 |
| 2 | 反应按键 | f/j/k | 用户确认 |
| 3 | 反应截止时间 | 2000ms | 通用建议（待确认）⚠️ |
```

Only `用户确认` is confirmed. Values from a template, general suggestion, or
automatic inference remain proposed and visibly marked until accepted.

## Cumulative Decision Registry

```text
## 实验设计决策注册表

### Phase 1: Assess
| # | 决策项 | 值 | 来源 |
|---|--------|-----|------|
| 1 | 实验范式 | Stroop | 用户描述 |
| 2 | 平台 | PsychoPy | 用户确认 |

### Phase 2: Windows & Rules
| # | 决策项 | 值 | 来源 |
|---|--------|-----|------|
| 3 | 反应时定义 | 刺激实际呈现至按键按下 | 用户确认 |
| 4 | 注视点持续时间 | 500ms | 默认（通用）⚠️ |
```

Every non-trivial design decision must appear exactly once with its source.
Append rather than replacing prior phases. Corrected decisions retain a clear
record of the new confirmed value.

## Gate 5 final review

The final review contains:

1. Every sequence row and window, with its optional condition table, cycles, and order policy.
2. A compact window table covering content, duration, response, condition
   bindings, RT anchor, and recorded data.
3. The complete cumulative Decision Registry.
4. An explicit list of every proposed/defaulted/inferred value marked ⚠️.
5. The question: `以上所有设计决策确认无误，可以生成代码？如需修改请指定编号和新值。`

Do not route to the Coder until the user explicitly confirms the complete
review. If an item changes, update the config and registry, repeat technical
validation, and present Gate 5 again.
