# jsPsych Implementation Guide

> **Status**: Layer 1 — API 规范、反模式表、强制模式。所有 jsPsych 7.x 实验代码必须遵守这些规则。

## Version Assumption

Default to **jsPsych 7.3.x** (ECMAScript 2017+). Plugins are loaded as **separate npm packages** under `@jspsych/plugin-*` scope. `jsPsych.init()` no longer exists — use `initJsPsych()` + `jsPsych.run()`.

**Key jsPsych 7.x breaking changes from v6.x:**

| v6.x | v7.x |
|------|------|
| `jsPsych.init({timeline: [...], ...})` | `var jsPsych = initJsPsych({...}); jsPsych.run([...])` |
| `type: 'html-keyboard-response'` (string) | `type: jsPsychHtmlKeyboardResponse` (class) |
| `jsPsych.NO_KEYS` / `jsPsych.ALL_KEYS` | `"NO_KEYS"` / `"ALL_KEYS"` (string) |
| `jsPsych.currentTimelineNodeID` | `jsPsych.getCurrentTimelineNodeID()` |
| `jsPsych.progress` | `jsPsych.getProgress()` |

## 1. 强制代码骨架

所有 jsPsych 实验必须从这个骨架开始：

```html
<!DOCTYPE html>
<html>
<head>
  <title>Experiment</title>
  <script src="https://unpkg.com/jspsych@7.3.4"></script>
  <script src="https://unpkg.com/@jspsych/plugin-html-keyboard-response@1.1.3"></script>
  <script src="https://unpkg.com/@jspsych/plugin-image-keyboard-response@1.1.3"></script>
  <link href="https://unpkg.com/jspsych@7.3.4/css/jspsych.css" rel="stylesheet" type="text/css" />
</head>
<body></body>
<script>
  // 1. Initialize jsPsych
  const jsPsych = initJsPsych({
    display_element: 'jspsych-target',
    on_finish: function() {
      jsPsych.data.get().localSave('csv', 'experiment_data.csv');
    },
    on_trial_finish: function(data) {
      // Per-trial incremental save (optional, for crash-safety)
    }
  });

  // 2. Preload media
  const preload = {
    type: jsPsychPreload,
    auto_preload: true
  };

  // 3. Define timeline
  const timeline = [preload, /* ...trials... */];

  // 4. Run experiment
  jsPsych.run(timeline);
</script>
</html>
```

## 2. 核心 API 规范

### 2.1 initJsPsych() — 实验配置

```js
const jsPsych = initJsPsych({
  // Display
  display_element: 'jspsych-target',  // 目标 HTML 元素 ID，默认 <body>
  experiment_width: 800,              // px，默认 100%

  // Timing
  default_iti: 0,                     // trial 间默认间隔 (ms)
  minimum_valid_rt: 0,                // 最低有效 RT (ms)

  // Data & Callbacks
  on_finish: function(data) { },      // 实验结束时触发，接收全部数据
  on_trial_start: function(trial) { },// 每 trial 开始时触发，可修改 trial 对象
  on_trial_finish: function(data) { },// 每 trial 结束时触发
  on_data_update: function(data) { }, // 写入新数据时触发
  on_close: function() { },           // 页面关闭前触发

  // Progress bar
  show_progress_bar: false,
  auto_update_progress_bar: true,

  // Audio
  use_webaudio: true,                 // true=WebAudio API, false=HTML5 Audio

  // Extensions
  extensions: [
    // { type: jsPsychExtensionMouseTracking, params: {} }
  ]
});
```

### 2.2 Timeline — 声明式实验结构

jsPsych 使用声明式 timeline — 实验 = 嵌套数组。每个节点可以是一对一 trial 或包含子节点的 block：

```js
const timeline = [
  welcome_trial,              // 简单 trial 对象
  instruction_block,          // 嵌套 timeline block
  practice_block,             // 包含 timeline_variables 的 block
  main_block,                 // 主实验 block
  debrief_trial               // 结束屏
];
jsPsych.run(timeline);
```

**核心参数 — 所有 timeline 节点通用：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `type` | Plugin class | **必须是类引用，不是字符串**。如 `jsPsychHtmlKeyboardResponse` |
| `stimulus` | string/function | HTML 内容或图片路径 |
| `choices` | array \| `"NO_KEYS"` \| `"ALL_KEYS"` | 允许的按键 |
| `trial_duration` | number/function | 最大时长 (ms)，null = 无限 |
| `response_ends_trial` | boolean | 是否按键结束 trial，默认 true |
| `post_trial_gap` | number/function | trial 后暂停 (ms)，默认 `default_iti` |
| `data` | object/function | 附加到此 trial 的元数据 |
| `on_start` | function | trial 刚开始时触发 |
| `on_finish` | function(data) | trial 结束时触发，可修改 data |
| `on_load` | function | DOM 加载完成时触发 |

**Block 级参数（嵌套 timeline）：**

| 参数 | 说明 |
|------|------|
| `timeline` | 子 trial 数组 |
| `timeline_variables` | 条件数组，每个元素是一个对象，key=变量名, value=变量值 |
| `randomize_order` | 是否随机化 trial 顺序，默认 false |
| `repetitions` | 重复次数，默认 1 |
| `loop_function` | 返回 true 则重复此 block（循环直到返回 false） |
| `conditional_function` | 返回 false 则跳过此 block |

### 2.3 Timeline Variables — 条件驱动

**正确模式** — `jsPsych.timelineVariable()` 作为静态参数：

```js
const stimuli = [
  { word: 'RED',   color: 'red',   corr_ans: 'left' },
  { word: 'GREEN', color: 'green', corr_ans: 'down' },
  { word: 'BLUE',  color: 'blue',  corr_ans: 'right' },
];

const trial = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: function() {
    return `<p style="color:${jsPsych.timelineVariable('color', true)}">${jsPsych.timelineVariable('word', true)}</p>`;
  },
  choices: ['left', 'down', 'right'],
  data: jsPsych.timelineVariable('data')  // 静态引用，不需要 true
};

const stroop_block = {
  timeline: [fixation, trial],
  timeline_variables: stimuli,
  randomize_order: true,
  repetitions: 5
};
```

**关键规则**：
- **静态参数**: `stimulus: jsPsych.timelineVariable('name')` — 无需第二个参数
- **函数内调用**: `jsPsych.timelineVariable('name', true)` — 必须传 `true` 获取实际值
- **条件预计算**: `timeline_variables` 数组在脚本加载时求值，不支持运行时动态生成
- 如需运行时动态条件，在 `on_trial_start` 中修改 trial 参数

### 2.4 按键响应收集

**正确模式** — 使用 `choices` 参数限制允许的按键：

```js
const trial = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: 'Press F or J',
  choices: ['f', 'j'],
  trial_duration: 2000,           // 2s deadline
  response_ends_trial: true       // 按键即结束
};
// 自动记录: data.response (按键名), data.rt (ms, 从 stimulus 出现算起)
```

**固定时长（无响应）**:
```js
const fixation = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: '+',
  choices: "NO_KEYS",             // 不接受任何按键
  trial_duration: 500,            // 固定 500ms
  response_ends_trial: false      // 时间到才结束
};
```

**强制纠正 (practice)**:
```js
// 使用 categorize-html 插件
const practiceTrial = {
  type: jsPsychCategorizeHtml,
  stimulus: jsPsych.timelineVariable('stim'),
  choices: ['f', 'j'],
  key_answer: 'f',                    // 正确答案的 keyCode
  correct_text: '<span style="color:green">√</span>',
  incorrect_text: '<span style="color:red">X</span>',
  feedback_duration: 500,
  force_correct_button_press: true    // 必须按正确键才能继续
};
```

### 2.5 RT 计时

jsPsych 自动记录 RT — 从 trial 开始到按键之间的时间（ms）。**不需要手动管理时钟。**

```js
// RT 自动记录在 data.rt
// 来源: performance.now()，舍入到最近 ms
jsPsych.data.get().filter({task: 'response'}).select('rt').mean();

// 验证最低有效 RT
const jsPsych = initJsPsych({
  minimum_valid_rt: 200  // ms，排除过快猜测反应
});
```

**反模式** — 禁止手动计时：
- 不要在 `on_start` 中记录 `Date.now()` 并在 `on_finish` 中相减
- 不要使用 `setTimeout` 实现 trial_duration — 用 `trial_duration` 参数

### 2.6 准确性判断

**模式 1 — `on_finish` 回调（推荐）**:

```js
const test = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: jsPsych.timelineVariable('word'),
  choices: ['f', 'j'],
  data: jsPsych.timelineVariable('data'),
  on_finish: function(data) {
    data.correct = jsPsych.pluginAPI.compareKeys(
      data.response, data.correct_response
    );
  }
};
```

**模式 2 — `categorize-html` 插件内置**:

```js
key_answer: 'f',  // 或动态函数: key_answer: function() { return keyCode(correctKey) }
// 插件自动记录 data.correct = true/false
```

**模式 3 — correctness_field 参数（部分插件支持）**:

```js
const trial = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: jsPsych.timelineVariable('stim'),
  choices: ['f', 'j'],
  data: { corr_ans: 'f' },
  correctness_field: 'corr_ans'  // 插件自动比较 response == corr_ans
};
```

### 2.7 条件文件加载

jsPsych 不支持直接加载 xlsx/csv 文件。条件必须定义为 JavaScript 数组：

```js
// 方式 1: 内联数组
const conditions = [
  { stimulus: 'img/a.png', correct: 'f', category: 'target' },
  { stimulus: 'img/b.png', correct: 'j', category: 'foil' },
];

// 方式 2: jsPsych.randomization.factorial（因子设计）
const factors = {
  cue_validity: ['valid', 'invalid'],
  target_location: ['left', 'right']
};
const conditions = jsPsych.randomization.factorial(factors);
// 生成: [{cue_validity:'valid', target_location:'left'}, ...] 共 4 条

// 方式 3: 动态生成（脚本加载时预计算）
const csStimuli = ['cs1.jpg', 'cs2.jpg'];
const usStimuli = ['us1.jpg'];
const conditions = [];
csStimuli.forEach(function(cs) {
  usStimuli.forEach(function(us) {
    conditions.push({cs: cs, us: us, cs_type: 'CS', us_type: 'US'});
  });
});
```

### 2.8 数据保存

**强制模式** — 在 `on_finish` 中集中保存：

```js
const jsPsych = initJsPsych({
  on_finish: function() {
    jsPsych.data.get()
      .filter({task: 'response'})               // 只保留正式试验
      .filterCustom(function(t) {                // 自定义过滤
        return t.rt > 200 && t.rt < 3000;
      })
      .ignore(['internal_node_id', 'stimulus', 'trial_type', 'plugin_version'])
      .localSave('csv', `sub-${subjectID}_${expName}.csv`);
  }
});
```

**DataCollection 方法速查：**

| 方法 | 说明 |
|------|------|
| `jsPsych.data.get()` | 获取全部数据 |
| `.filter({key: value})` | 条件过滤（AND） |
| `.filter([{a:1},{b:2}])` | 条件过滤（OR） |
| `.filterCustom(fn)` | 自定义过滤函数 |
| `.ignore(['col1','col2'])` | 排除指定列 |
| `.addToLast({key: val})` | 向最后一条数据添加属性 |
| `.localSave('csv', filename)` | 本地下载 CSV/JSON |
| `.csv()` | 导出 CSV 字符串 |
| `.json()` | 导出 JSON 字符串 |
| `.values()` | 返回原始对象数组 |
| `.count()` | 返回 trial 数量 |
| `.select('col')` | 返回指定列值的数组 |
| `jsPsych.data.addProperties({key:val})` | 全局添加属性到所有数据 |

## 3. 刺激预加载（强制规则）

**正确模式** — 在 timeline 最前面插入 `preload` trial：

```js
// 自动检测（推荐 — 覆盖大部分场景）
const preload = {
  type: jsPsychPreload,
  auto_preload: true      // 自动扫描 timeline 中所有文件的路径
};

// 手动指定（动态 stimulus 或函数内引用的文件）
const preload = {
  type: jsPsychPreload,
  images: ['img/blue.png', 'img/orange.png'],
  audio: ['audio/beep.mp3'],
  video: ['video/instruction.mp4'],
  show_progress_bar: true,
  message: 'Loading stimuli...'
};

const timeline = [preload, /* ...所有其他试验... */];
jsPsych.run(timeline);
```

**反模式 — 禁止**:
- 不在 timeline 起始放置 preload trial → 第一次呈现图片时会因网络请求延迟造成计时误差

## 4. CJK 字体配置

```html
<!-- 方式 1: Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC&display=swap" rel="stylesheet">

<!-- 方式 2: 系统字体 fallback -->
<style>
  body {
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  }
  .jspsych-display-element {
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  }
</style>
```

```js
// 方式 3: 在 stimulus HTML 中内联
const instruction = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <div style="font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; font-size: 24px;">
      你好！欢迎参加本实验。<br/>
      请按空格键继续。
    </div>`,
  choices: [' ']
};
```

**关键规则**: jsPsych 渲染一切为 HTML — 所有样式通过 CSS 控制。中文字体在 macOS 用 `PingFang SC`，Windows 用 `Microsoft YaHei`。

## 5. 反模式速查表

| 禁止的 API / 模式 | 原因 | 替代方案 |
|-------------------|------|---------|
| `jsPsych.init()` | v7 已移除 | `initJsPsych()` + `jsPsych.run()` |
| `type: 'html-keyboard-response'` (字符串) | v7 类型必须是类 | `type: jsPsychHtmlKeyboardResponse` |
| `jsPsych.NO_KEYS` / `jsPsych.ALL_KEYS` | v7 已移除 | `"NO_KEYS"` / `"ALL_KEYS"` (字符串) |
| `jsPsych.timelineVariable('x')` 在函数内不传 `true` | v7 返回对象而非值 | `jsPsych.timelineVariable('x', true)` |
| `jsPsych.data.get().select('col')` | v7 无此方法 | 导出后用其他工具选列，或使用 `.filter()`+`.ignore()` |
| `timeline_variables` 作为函数 | 不支持运行时生成 | 在脚本加载时预计算所有条件 |
| `setTimeout` / `setInterval` 实现计时 | 不精确，破坏 jsPsych 事件循环 | `trial_duration` 参数 |
| `Date.now()` 手动计时 | jsPsych 自动记录 RT | 使用 `data.rt` |
| 不在 timeline 起始放置 preload | 运行时加载导致帧丢失 | `timeline: [preload, ...]` |
| `XMLHttpRequest` / `fetch` 在 trial 内加载 xlsx | 网络延迟破坏计时 | 预计算为 JavaScript 数组 |
| 硬编码 `keyCode` 数字 | 跨浏览器不可靠 | `jsPsych.pluginAPI.convertKeyCharacterToKeyCode('f')` 或直接使用 `'f'` |
| 在 `on_finish` 中修改 data 后不做 return | 修改不会反映到保存的数据中 | 直接修改传入的 `data` 对象（它是引用） |
| 不处理 Escape 键 | 无法退出全屏/暂停实验 | 在各 trial 的 `choices` 中包含 `'escape'`，或在 `on_trial_finish` 中检查 |

## 6. Trial 生命周期

```
1. on_load()          ← DOM 加载完成
2. on_trial_start()   ← trial 即将开始（全局回调）
3. on_start()         ← trial 开始时（trial 级回调）
4. stimulus 渲染      ← 显示刺激，启动计时
5. [response 收集]    ← 按键 / 超时
6. on_finish(data)    ← trial 结束时（trial 级），可修改 data
7. on_trial_finish(data) ← trial 结束（全局回调）
8. post_trial_gap     ← 屏幕清空，等待间隔
9. next trial / finish← 进入下一个 trial 或实验结束
```

**关键：** `data.rt` 是在第 4-5 步之间测量的。`on_finish` 是修改 data（如计算 accuracy）的最佳位置。

## 7. 插件类型速查

### 使用频率最高的插件

| 需求 | 插件类型 | 关键参数 |
|------|---------|---------|
| HTML + 按键 | `jsPsychHtmlKeyboardResponse` | `stimulus`, `choices`, `trial_duration` |
| 图片 + 按键 | `jsPsychImageKeyboardResponse` | `stimulus`(图片路径), `choices` |
| 音频 + 按键 | `jsPsychAudioKeyboardResponse` | `stimulus`(音频路径), `choices` |
| HTML + 按钮 | `jsPsychHtmlButtonResponse` | `stimulus`, `choices`(按钮label数组) |
| 分类 + 反馈 | `jsPsychCategorizeHtml` | `key_answer`, `correct_text`, `incorrect_text`, `force_correct_button_press` |
| 指令（多页） | `jsPsychInstructions` | `pages`(文字数组), `key_forward`, `allow_backward` |
| 问卷（通用） | `jsPsychSurvey` | `pages`(含 questions 数组) |
| Likert 量表 | `jsPsychSurveyLikert` | `questions`, `labels`(7点/5点标签) |
| 多选 | `jsPsychSurveyMultiChoice` | `questions`, `options` |
| 文本输入 | `jsPsychSurveyText` | `questions`, `rows` |
| 调用函数 | `jsPsychCallFunction` | `func` |
| 全屏切换 | `jsPsychFullscreen` | `fullscreen_mode`, `message` |
| 预加载 | `jsPsychPreload` | `auto_preload`, `images`, `audio` |
| IAT | `jsPsychIatHtml` | `stimulus`(words数组), `labels`(左右标签) |

## 8. Canonical Code Skeleton（生成代码必须以此为模板）

以下是完整的、可直接运行的 Stroop 实验骨架。**所有生成的 jsPsych 代码必须从这个骨架开始。** 修改 conditions 数组和 stimulus 函数即可适配不同范式。

```html
<!DOCTYPE html>
<html>
<head>
  <title>Stroop Experiment</title>
  <script src="https://unpkg.com/jspsych@7.3.4"></script>
  <script src="https://unpkg.com/@jspsych/plugin-html-keyboard-response@1.1.3"></script>
  <script src="https://unpkg.com/@jspsych/plugin-preload@1.1.3"></script>
  <script src="https://unpkg.com/@jspsych/plugin-fullscreen@1.1.3"></script>
  <link href="https://unpkg.com/jspsych@7.3.4/css/jspsych.css" rel="stylesheet" type="text/css" />
  <style>
    body { font-family: "PingFang SC", "Microsoft YaHei", sans-serif; }
  </style>
</head>
<body></body>
<script>
  const jsPsych = initJsPsych({
    on_finish: function() {
      jsPsych.data.get().filter({task:'stroop'}).localSave('csv', 'stroop_data.csv');
    }
  });

  // Conditions
  const conditions = [
    { word: 'RED',  color: 'red',   corr_ans: 'left' },
    { word: 'GREEN', color: 'green', corr_ans: 'down' },
    { word: 'BLUE',  color: 'blue',  corr_ans: 'right' },
  ];

  const fullConditions = [];
  conditions.forEach(row => {
    conditions.forEach(col => {
      fullConditions.push({
        word: row.word, color: col.color,
        corr_ans: col.corr_ans,
        congruent: row.word === col.word
      });
    });
  });

  // Trials
  const instruction = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>请判断字的<strong>墨水颜色</strong>，忽略字本身的含义。</p><p>红色 → 左箭头<br>绿色 → 下箭头<br>蓝色 → 右箭头</p><p>按空格键开始。</p>',
    choices: [' ']
  };

  const fixation = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<div style="font-size:60px;">+</div>',
    choices: "NO_KEYS",
    trial_duration: 500,
    data: { task: 'fixation' }
  };

  const trial = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: function() {
      return `<p style="color:${jsPsych.timelineVariable('color', true)}; font-size:96px;">${jsPsych.timelineVariable('word', true)}</p>`;
    },
    choices: ['ArrowLeft', 'ArrowDown', 'ArrowRight'],
    trial_duration: 3000,
    data: function() {
      return {
        task: 'stroop',
        word: jsPsych.timelineVariable('word', true),
        color: jsPsych.timelineVariable('color', true),
        corr_ans: jsPsych.timelineVariable('corr_ans', true),
        congruent: jsPsych.timelineVariable('congruent', true)
      };
    },
    on_finish: function(data) {
      data.correct = data.response === data.corr_ans;
    }
  };

  const debrief = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: function() {
      const trials = jsPsych.data.get().filter({task:'stroop'});
      const correct = trials.filter({correct:true});
      const acc = Math.round(correct.count() / trials.count() * 100);
      const rt = Math.round(correct.select('rt').mean());
      return `<p>正确率: ${acc}%</p><p>平均反应时: ${rt}ms</p><p>按任意键结束。</p>`;
    }
  };

  const stroopBlock = {
    timeline: [fixation, trial],
    timeline_variables: fullConditions,
    randomize_order: true,
    repetitions: 5
  };

  const timeline = [
    { type: jsPsychFullscreen, fullscreen_mode: true },
    instruction,
    stroopBlock,
    debrief
  ];

  jsPsych.run(timeline);
</script>
</html>
```

## 9. API 参考索引

| 需要实现的功能 | 核心 API / 插件 |
|---------------|----------------|
| 创建实验、配置回调 | `initJsPsych({on_finish, on_trial_start, ...})` |
| 启动实验 | `jsPsych.run(timelineArray)` |
| 显示 HTML 文本 + 按键 | `jsPsychHtmlKeyboardResponse` |
| 显示图片 + 按键 | `jsPsychImageKeyboardResponse` |
| 播放音频 + 按键 | `jsPsychAudioKeyboardResponse` |
| 分类任务 + 反馈 | `jsPsychCategorizeHtml` / `jsPsychCategorizeImage` |
| 多页指令 | `jsPsychInstructions` |
| Likert 量表 | `jsPsychSurveyLikert` |
| 多选问卷 | `jsPsychSurveyMultiChoice` |
| IAT 任务 | `jsPsychIatHtml` / `jsPsychIatImage` |
| 全屏切换 | `jsPsychFullscreen` |
| 预加载媒体 | `jsPsychPreload` |
| 执行任意 JS | `jsPsychCallFunction` |
| 条件数组驱动 trial | `timeline_variables` + `jsPsych.timelineVariable()` |
| 因子设计 | `jsPsych.randomization.factorial(factors)` |
| 随机化 | `jsPsych.randomization.shuffle(arr)` / `randomize_order: true` |
| 按键比较 | `jsPsych.pluginAPI.compareKeys(response, expected)` |
| 数据过滤 | `jsPsych.data.get().filter({...}).filterCustom(fn)` |
| 数据保存 | `.localSave('csv', filename)` |
| 数据显示（调试） | `jsPsych.data.displayData()` |
| 鼠标轨迹 | `extension-mouse-tracking` |
| 眼动追踪 | `extension-webgazer` |
