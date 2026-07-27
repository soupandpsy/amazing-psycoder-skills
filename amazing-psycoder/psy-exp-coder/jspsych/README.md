# jsPsych (JavaScript)

> **状态**: 当前生成目标为 config 中固定版本的 jsPsych 8.x。L3 的 26 个文件多数来自 PsychoJS/jsPsych 6/lab.js，只能提取范式逻辑，不能复制 API 或声称原样可运行。

## 生成代码流程（与 PsychoPy 统一，平台特化映射见 mapping/）

```
config.yaml
    │
    ▼
1. 确认 `runtime.framework_version` 与兼容的 core/plugin 固定版本，复制 [Canonical Code Skeleton](spec/README.md#8-canonical-code-skeleton)
    │
    ▼
2. 参数区：填入 config 的 display / font / output
    │
    ▼
3. Timeline 结构：config.windows[] → 嵌套 timeline 节点数组
    → 映射规则见 [mapping/README.md §Windows[] → Timeline 节点](mapping/README.md#windows--timeline-节点映射jspsych-7x)
    │
    ▼
4. 条件数组：config.blocks[].condition_file → JavaScript 数组（非外部文件）
    → 可用 `jsPsych.randomization.factorial()` 或脚本加载时预计算
    │
    ▼
5. 响应收集：config.windows[].response → `choices: [keys]` + `response_ends_trial: true`
    │
    ▼
6. 正确性判断：config.response_rules.correct → `on_finish` 回调 + `compareKeys()`
    │
    ▼
7. 数据保存：config.output → `on_data_update` 耐久 checkpoint + `on_finish` 原始 trial-summary 最终导出；分析排除不在采集端执行
    │
    ▼
8. 运行 Quality Gate（10 项）→ 修复 → 交付
```

关键：每个步骤对应的 config 字段映射见 [mapping/README.md](mapping/README.md)。

## 文件结构

```
jspsych/
├── README.md              ← 本文件
├── spec/                  ← L1: jsPsych 8.x API 规范 + Canonical Skeleton
│   └── README.md
├── mapping/               ← L2: Config → jsPsych timeline 节点映射
│   └── README.md          ← 含 legacy→8.x 迁移表 + PsychoJS 对照
├── paradigms/              ← L3: 范式参考（实验逻辑，非 API 参考）
│   ├── README.md          ← 范式索引 + API 醒示
│   └── *.md               ← 25 个范式文件
└── demo/                  ← L4: Pavlovia 原始导出
    └── _raw/              ← 23 个 .js
```

## 层级填充状态

| 层级 | 内容 |
|------|------|
| L1 `spec/` | jsPsych 8.x pinned Canonical Skeleton + API contract |
| L2 `mapping/` | jsPsych 8.x Config→Code mapping；legacy/PsychoJS 仅作迁移对照 |
| L3 `paradigms/` | 25 个 legacy 逻辑来源。代码块属于隔离区，**API 只能来自 L1-L2** |
| L4 `demo/` | 23 个 Pavlovia .js — 仅参考实验逻辑 |

## 强制 API 规则

所有生成的 jsPsych 代码遵守（完整规范见 [spec/README.md](spec/README.md)）：

| 类别 | 必须使用 | 禁止使用 |
|------|---------|---------|
| 初始化 | `initJsPsych()` + `jsPsych.run()` | `jsPsych.init()` |
| 插件类型 | class 引用：`jsPsychHtmlKeyboardResponse` | 字符串：`'html-keyboard-response'` |
| 无按键 | `"NO_KEYS"`（字符串） | `jsPsych.NO_KEYS` |
| 任意按键 | `"ALL_KEYS"`（字符串） | `jsPsych.ALL_KEYS` |
| Timeline variable | static placeholder: `timelineVariable('x')`; function: `evaluateTimelineVariable('x')` | v7 的 `timelineVariable('x', true)` |
| 条件数组 | 脚本加载时预计算所有条件 | `timeline_variables` 作为函数（运行时生成不支持） |
| 预加载 | 媒体首次使用前完成 preload | 纯文本也机械添加空 preload，或媒体使用后才 preload |
| RT | `data.rt`（自动记录） | `Date.now()` 手动计时 |
| 计时 | `trial_duration: N`（ms） | `setTimeout`/`setInterval` |
| 数据保存 | `on_data_update` checkpoint + `on_finish` 最终 `localSave` | 仅结束时保存或只保存在内存 |
| 正确性 | `jsPsych.pluginAPI.compareKeys()` | 手动 `==` 比较（跨浏览器不可靠） |

## 平台特有关键概念

jsPsych 是**声明式**实验框架 — 与其他平台的核心差异：

| 概念 | jsPsych 方式 | vs PsychoPy/Psychtoolbox |
|------|-------------|--------------------------|
| 实验结构 | 声明式 timeline 数组（嵌套） | 命令式循环（for/while） |
| Trial 定义 | 对象 `{type: PluginClass, stimulus: ..., choices: ...}` | 函数/代码块 |
| 条件控制 | `timeline_variables` 数组（纯数据） | 外部文件加载（xlsx/csv） |
| 准度判断 | `on_finish` 回调修改 `data.correct` | 手动 `if resp == corrAns` |
| RT 记录 | 插件自动记录 `data.rt`（ms） | 手动 clock reset + key.rt |
| 数据保存 | 每 trial checkpoint + 结束时 `.filter().localSave()` | 仅结束时写出 |
| 预加载 | `jsPsychPreload` plugin（自动扫描） | 显式预创建所有 stimulus 对象 |

## 范式差异速查

不同范式在当前 pinned jsPsych 8.x 目标上的实现要点：

| 范式 | 关键插件 | 条件结构 | 特殊逻辑 |
|------|---------|---------|---------|
| Stroop | `jsPsychHtmlKeyboardResponse` | word × color 因子数组 | `stimulus: function()` 动态生成 HTML |
| IAT | verified current plugin/custom nodes | 7-block 工厂函数 | 采集原始 block/RT/error；D-score 在分析阶段计算 |
| Go/No-go | `jsPsychHtmlKeyboardResponse` | go × no-go 比例 | `correctness_field` 或 `compareKeys` |
| Stop-signal | `jsPsychHtmlKeyboardResponse` | SSD staircase | `jsPsychCallFunction` 或自定义 plugin |
| N-back | `jsPsychHtmlKeyboardResponse` | 程序化序列 | 采集 target/lure/response 状态；d-prime 在分析阶段计算 |

详细映射见 [mapping/README.md §范式架构对比](mapping/README.md#范式架构对比)。
