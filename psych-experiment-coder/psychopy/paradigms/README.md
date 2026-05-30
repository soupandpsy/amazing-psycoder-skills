# PsychoPy Paradigms

> **Layer 3**: 范式参考文件 — 每个范式一个 `.md` 文件，包含实验逻辑和代码示例。

## 范式索引

### 核心范式（14个条目，13个文件 + 1个交叉引用）

| 范式 | 文件 | 类型 |
|------|------|------|
| Stroop | [stroop.md](stroop.md) | Pavlovia demo |
| Go/No-go | [go-nogo.md](go-nogo.md) | Pavlovia demo |
| Eriksen Flanker | [eriksen-flanker.md](eriksen-flanker.md) | CONFIG-DRIVEN |
| Simon | [simon.md](simon.md) | Pavlovia demo |
| N-back | [n-back.md](n-back.md) | CONFIG-DRIVEN |
| Dot-probe | [dot-probe.md](dot-probe.md) | Pavlovia demo |
| Visual search | [visual-search.md](visual-search.md) | CONFIG-DRIVEN |
| Task switching | [task-switching.md](task-switching.md) | CONFIG-DRIVEN |
| Stop-signal | [stop-signal.md](stop-signal.md) | CONFIG-DRIVEN |
| IAT | [iat.md](iat.md) | Pavlovia demo |
| Priming | [priming.md](priming.md) | Pavlovia demo |
| Rating | [rating.md](rating.md) | Pavlovia demo |
| Navon | [navon.md](navon.md) | CONFIG-DRIVEN |
| EAST | (参见 jspsych) | — |

### 扩展范式（14个，参考描述）

| 范式 | 文件 |
|------|------|
| Antisaccade | [antisaccade.md](antisaccade.md) |
| Change Detection | [change-detection.md](change-detection.md) |
| Choice Reaction Time | [choice-reaction-time.md](choice-reaction-time.md) |
| Cyberball | [cyberball.md](cyberball.md) |
| Delay Discounting | [delay-discount.md](delay-discount.md) |
| Mental Rotation | [mental-rotation.md](mental-rotation.md) |
| Multisensory Nature | [multisensory-nature.md](multisensory-nature.md) |
| Numerical Stroop | [numerical-stroop.md](numerical-stroop.md) |
| Phone a Friend | [phone-a-friend.md](phone-a-friend.md) |
| Psychophysics Staircase | [psychophysics-staircase.md](psychophysics-staircase.md) |
| Sternberg | [sternberg.md](sternberg.md) |
| Ultimatum Game | [ultimatum-game.md](ultimatum-game.md) |
| Wisconsin Card Sorting | [wisconsin-card-sorting.md](wisconsin-card-sorting.md) |
| Writing Distraction | [writing-distraction.md](writing-distraction.md) |

> **重要：范式 ≠ API 参考。** 以下文件中的代码示例来自 Pavlovia demo（多为 PsychoPy v3.1），使用旧版 API（如 `event.getKeys(maxWait=)`、`exec()` 条件注入、`trialClock.getTime()`）。**生成实验代码时，API 模式以 [spec/README.md](../spec/README.md) 的 Canonical Code Skeleton 为准**（PTB keyboard、`key.rt`、`getFutureFlipTime`、`try/finally`）。范式文件仅提供实验逻辑：窗口序列、条件结构、正确性规则。

每个文件的**实验逻辑**章节定义设计模式、窗口序列、正确性规则。**代码示例**在末尾给出完整的可直接运行的代码。

另有 13 个范式仅有 jsPsych/PsychoJS 代码（无 Python 实现），参见 [jspsych/paradigms/README.md](../../jspsych/paradigms/README.md)。
