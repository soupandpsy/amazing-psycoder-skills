# jsPsych Paradigms

> **L3**: 范式参考文件 — 22 个 PsychoJS + 1 个 lab.js + 2 个 jsPsych 6.1.0 原生范式，包含完整可运行代码。

## 范式索引

| 范式 | 文件 | 类型 |
|------|------|------|
| Antisaccade | [antisaccade.md](antisaccade.md) | PsychoJS |
| Attention Network Task | [attention-network-task.md](attention-network-task.md) | PsychoJS |
| BART | [bart.md](bart.md) | PsychoJS |
| Bilingual Stroop | [bilingual-stroop.md](bilingual-stroop.md) | PsychoJS |
| Butterfly Simon | [butterfly-simon.md](butterfly-simon.md) | PsychoJS |
| Change Detection | [change-detection.md](change-detection.md) | PsychoJS |
| Children Flanker Task | [children-flanker-task.md](children-flanker-task.md) | PsychoJS |
| Choice Reaction Time | [choice-reaction-time.md](choice-reaction-time.md) | PsychoJS |
| Climate Reflection Task | [climate-reflection-task.md](climate-reflection-task.md) | PsychoJS |
| Continuous Performance Test | [continuous-performance-test.md](continuous-performance-test.md) | PsychoJS |
| Corsi Blocks | [corsi-blocks.md](corsi-blocks.md) | PsychoJS |
| Cyberball | [cyberball.md](cyberball.md) | PsychoJS |
| Drag and Drop | [drag-and-drop.md](drag-and-drop.md) | PsychoJS |
| EAST | [east.md](east.md) | jsPsych 6.1.0 原生 |
| IAT | [iat.md](iat.md) | jsPsych 6.1.0 原生 |
| Stroop (lab.js) | [labjs-stroop.md](labjs-stroop.md) | lab.js |
| Mental Rotation | [mental-rotation.md](mental-rotation.md) | PsychoJS |
| Multisensory Nature | [multisensory-nature.md](multisensory-nature.md) | PsychoJS |
| Multisensory Nature Climate | [multisensory-nature-climate.md](multisensory-nature-climate.md) | PsychoJS |
| Numerical Stroop | [numerical-stroop.md](numerical-stroop.md) | PsychoJS |
| Phone a Friend | [phone-a-friend.md](phone-a-friend.md) | PsychoJS |
| Psychophysics Staircase | [psychophysics-staircase.md](psychophysics-staircase.md) | PsychoJS |
| Rating to Choice Task | [rating-to-choice-task.md](rating-to-choice-task.md) | PsychoJS |
| Sternberg | [sternberg.md](sternberg.md) | PsychoJS |
| Wisconsin Card Sorting | [wisconsin-card-sorting.md](wisconsin-card-sorting.md) | PsychoJS |

## 类型说明

- **PsychoJS**: Pavlovia 平台上的 jsPsych 实现，使用 PsychoJS 插件
- **lab.js**: 独立的 JavaScript 实验框架（非 jsPsych/PsychoJS），使用 HTML 模板 + messageHandlers
- **jsPsych 6.1.0 原生**: 标准 jsPsych 6.1.0 库的原生实现（来源：psychbruce/jspsych）

> **重要：范式 ≠ API 参考。** 以下文件中的代码示例使用 jsPsych 6.1.0 或 PsychoJS API（如 `jsPsych.init()`、字符串类型 `'html-keyboard-response'`、`jsPsych.NO_KEYS`）。**生成实验代码时，API 模式以 [spec/README.md](../spec/README.md) 的 Canonical Code Skeleton 为准**（`initJsPsych()`+`jsPsych.run()`、class 引用类型、`"NO_KEYS"` 字符串）。范式文件仅提供实验逻辑：窗口序列、条件结构、准确度规则。

每个文件包含**实验逻辑**（设计模式、窗口序列、准确度规则）和**代码示例**（可直接运行的完整代码）。

