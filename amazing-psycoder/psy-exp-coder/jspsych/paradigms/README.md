# jsPsych Paradigms

> **L3 legacy source set**: 22 个 PsychoJS + 1 个 lab.js + 2 个 jsPsych 6.1.0。代码块是隔离的历史来源，不得复制、执行或标为当前 jsPsych 可运行代码。

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

- **PsychoJS**: PsychoPy Builder 的独立 JavaScript runtime，常部署于 Pavlovia；不是 jsPsych 实现或插件集
- **lab.js**: 独立的 JavaScript 实验框架（非 jsPsych/PsychoJS），使用 HTML 模板 + messageHandlers
- **jsPsych 6.1.0 原生**: 标准 jsPsych 6.1.0 库的原生实现（来源：psychbruce/jspsych）

> **重要：范式 ≠ API 参考。** 只读取设计意图、窗口序列、条件字段和评分语义，再用 [spec](../spec/README.md) 与 [mapping](../mapping/README.md) 重新实现。任何 legacy 代码片段都必须被当前 validator 拒绝或重写。

每个文件可能混有实验逻辑和历史导出代码；后者不构成可运行性或正确性证据。
