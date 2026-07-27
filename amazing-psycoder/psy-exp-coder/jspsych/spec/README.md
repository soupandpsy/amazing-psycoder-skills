# jsPsych Implementation Guide

> **Status**: Layer 1 — API 规范、反模式表、强制模式。当前生成目标为 jsPsych 8.x；项目必须固定并记录精确 core/plugin 版本。
> **Last updated**: 2026-07-25 — 17-rule quality template applied (9-section jsPsych adaptation)

## Critical Rules (Read First — errors here invalidate data)

| Rule | Why Critical |
|------|-------------|
| **`on_data_update` for durable per-trial checkpoint** | `localSave` at end only = browser close/crash loses all data |
| **`addEventListener(..., true)` — capture phase required** | Missing `true` = jsPsych plugins capture Escape first, abort handler never fires |
| **`Number(jsPsych.pluginAPI.compareKeys(...))` for accuracy** | `true`/`false` in data breaks CSV analysis. Must output 0/1 int |
| **`timeline_variables` precomputed at script load** | jsPsych cannot dynamically generate conditions at runtime |
| **`type: jsPsychHtmlKeyboardResponse` (class, not string)** | `type: 'html-keyboard-response'` = legacy, broken in jsPsych 8.x |
| **`initJsPsych()` + `jsPsych.run()`, never `jsPsych.init()`** | `jsPsych.init()` = legacy API, removed in current versions |

Full anti-patterns table: [§5](#5-anti-patterns-quick-reference). Full 17-rule template: [§0](#0-code-structure-requirements-17-rule-quality-template-jspsych-adaptation).

## Version Assumption

The canonical CDN example is pinned to **jsPsych 8.2.3** and official plugin packages 2.1.0. Before generation, confirm the project's target version and consult its official migration guide; never silently mix core and plugin major versions. `jsPsych.init()` is legacy — use `initJsPsych()` + `jsPsych.run()`.

**Key current-vs-legacy distinctions:**

| Legacy | jsPsych 8.x target |
|--------|--------------------|
| `jsPsych.init({timeline: [...], ...})` | `var jsPsych = initJsPsych({...}); jsPsych.run([...])` |
| `type: 'html-keyboard-response'` (string) | `type: jsPsychHtmlKeyboardResponse` (class) |
| `jsPsych.NO_KEYS` / `jsPsych.ALL_KEYS` | `"NO_KEYS"` / `"ALL_KEYS"` (string) |
| `jsPsych.currentTimelineNodeID` | `jsPsych.getCurrentTimelineNodeID()` |
| `jsPsych.progress` | `jsPsych.getProgress()` |
| `jsPsych.timelineVariable('x', true)` inside a function (v7 pattern) | `jsPsych.evaluateTimelineVariable('x')` inside a function |

## 0. Code Structure Requirements (17-Rule Quality Template — jsPsych Adaptation)

Every generated jsPsych experiment must follow these rules. The template is identical to the PsychoPy version except where jsPsych/JavaScript API differences require adaptation (marked **[jsPsych]**).

### 0.1 File-Level Structure (Rules 1–2 — jsPsych: HTML comments)

```html
<!-- {filename}.html -->
<!--
  一体化流程：
    {stage_1} → {stage_2} → {stage_3}

  数据输出：
    on_finish → sub-{id}_{task}_{date}.csv
    on_data_update → localStorage durable checkpoint

  设计概要：
    每个 block：{n} trial
    正式阶段：{m} block × {t} = {total} trial

  当前版本关键修改：
    1) {change_1}
    2) {change_2}
-->
```

**[jsPsych]** jsPsych 是 HTML 文件。文件头用 HTML 注释 `<!-- -->` 而非 Python `#`。CDN 版本号必须在文件头中明确写出。

### 0.2 Section Order (Rules 1, 3, 5 — jsPsych: 9 sections)

```
Section 1:  HTML 头（CDN 版本号 + CSS 字体/样式 + <body> 容器）           ← Rule 3
Section 2:  实验常量（subject/session/task 版本/seed 材料）
Section 3:  文本常量（所有指导语/反馈/提示 HTML 字符串集中定义）            ← Rule 5
Section 4:  退出安全网（AUTOSAVE_KEY + handleEmergencyAbort + persistTrialCheckpoint）
Section 5:  jsPsych 初始化（initJsPsych + on_data_update + on_finish + on_close）
Section 6:  条件定义（内联数组 / factorial / 预计算生成）                  ← Rule 9
Section 7:  Trial 定义（注视点 / 刺激 / 反馈 / ITI — 每个 trial 一个对象） ← Rule 12
Section 8:  Block 定义（timeline_variables + repetitions + randomize_order）
Section 9:  Timeline 组装 + 启动（preload → instruction → blocks → debrief → run）
```

**[jsPsych]** jsPsych 是声明式的——trial 定义为对象，不是函数。`jsPsych.run(timeline)` 替代命令式主循环。

### 0.3 Variable Naming (Rule 4 — jsPsych: camelCase)

```
<prefix><Category><Meaning>

prefix   = kp | nv | prac | main | (按实验阶段自定义)
Category = Txt (文本) | Key (按键名) | Ms (毫秒时序)
         | MaxConsec (约束) | n (计数)

正例: pracFeedbackMs, mainItiMinMs, nvMaxConsecSame
反例: feedback_timeout, iti, max_ellipse
```

**[jsPsych]** JavaScript 惯例用 camelCase。跨平台常量（`SUBJECT_ID`、`RUN_ID`、`AUTOSAVE_KEY`）保留 UPPER_SNAKE 因为它们是运行环境标识符。

### 0.4 Pseudorandom Constraints (Rule 6 — jsPsych: timeline_variables + randomize_order)

```js
// ---------- 伪随机约束 ----------
const MAX_CONSEC_SAME_CONDITION = 3;
const MAX_PSEUDORAND_TRIES = 5000;

function canAppendTrial(seq, candidate) {
    let count = 0;
    for (let i = seq.length - 1; i >= 0; i--) {
        if (seq[i].condition === candidate.condition) count++;
        else break;
    }
    return count < MAX_CONSEC_SAME_CONDITION;
}

function pseudorandomize(rawTrials) {
    for (let attempt = 0; attempt < MAX_PSEUDORAND_TRIES; attempt++) {
        const remaining = jsPsych.randomization.shuffle([...rawTrials]);
        const seq = [];
        while (remaining.length > 0) {
            const validIdx = [];
            for (let i = 0; i < remaining.length; i++) {
                if (canAppendTrial(seq, remaining[i])) validIdx.push(i);
            }
            if (validIdx.length === 0) break;
            const pick = validIdx[
              jsPsych.randomization.randomInt(0, validIdx.length - 1)
            ];
            seq.push(remaining.splice(pick, 1)[0]);
        }
        if (seq.length === rawTrials.length) return seq;
    }
    throw new Error('无法生成满足约束的 trial 顺序。');  // 失败必须退出
}
```

**[jsPsych]** jsPsych 的 `randomize_order: true` 只支持简单随机——无法表达"连续不超过 N 个同条件"等约束。约束伪随机**必须在脚本加载时预计算**：先调用 `jsPsych.randomization.setSeed()`，再在 `jsPsych.run()` 前调用 `pseudorandomize()`，将完整结果直接赋给 `timeline_variables`。调用方必须捕获 `throw new Error()`，保存失败 checkpoint，并显式调用 `jsPsych.abortExperiment()`；抛错本身不会自动触发 jsPsych 的中止流程。

### 0.5 Exit Safety (Rule 7 — jsPsych: abortExperiment + localStorage checkpoint)

```js
let abortRequested = false;
function handleEmergencyAbort(event) {
  if (event.key !== 'Escape' || abortRequested) return;
  event.preventDefault();
  abortRequested = true;
  localStorage.setItem(`${AUTOSAVE_KEY}:aborted_at`, new Date().toISOString());
  jsPsych.abortExperiment(
    '实验已安全终止，最近的 checkpoint 已保留。',
    { abort_reason: 'escape' }
  );
}
document.addEventListener('keydown', handleEmergencyAbort, true);
```

**[jsPsych]** jsPsych 无全屏退出问题——浏览器自身的 Escape 行为不会锁屏。`jsPsych.abortExperiment()` 终止执行并触发 `on_finish`（含 `localSave`）。关键：`addEventListener` 的第三个参数必须是 `true`（capture phase）以确保在任何 jsPsych 事件处理器之前捕获。

### 0.6 Condition Validation (Rule 9 — jsPsych: precomputed arrays)

```js
// 条件必须在脚本加载时预计算 —— jsPsych 不支持运行时动态生成 timeline_variables
const validStimuli = ['RED', 'GREEN', 'BLUE'];
const validColors  = ['red', 'green', 'blue'];
const validKeys    = ['f', 'j'];

const conditions = [];
for (const word of validStimuli) {
  for (const color of validColors) {
    if (word === color) continue;  // 排除一致条件? (取决于实验设计)
    conditions.push({
      word: word,
      color: color,
      corr_ans: color === 'red' ? 'f' : 'j',
      congruent: word === color
    });
  }
}
if (conditions.length === 0) {
  throw new Error('条件表为空。');
}
```

### 0.7 Trial Definition Contract (Rule 12 — jsPsych: five steps distributed across timeline)

**[jsPsych]** jsPsych 没有"一个函数做五步"——框架是声明式的，每个 trial 对象只管一个屏幕。五步分散在多个 trial 对象 + block timeline 中：

```
① 呈现  = stimulus 参数（HTML 字符串或返回 HTML 的函数）
② 收集  = jsPsych 自动（data.response, data.rt — 整数 ms，无需手动计时）
③ 反馈  = 单独的 feedback trial 对象（通过 block timeline 插入在 trial 之后）
④ ITI   = post_trial_gap 参数（简单定长）或单独的 ITI trial 对象（随机时长）
⑤ 写数据 = on_finish 回调（计算 accuracy, response_status 等派生字段）
```

```js
// ①+② 刺激 + 响应（单个 trial 对象）
const trial = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: function() {
    const word = jsPsych.evaluateTimelineVariable('word');
    const color = jsPsych.evaluateTimelineVariable('color');
    return `<p style="color:${color}; font-size:96px;">${word}</p>`;
  },
  choices: ['f', 'j'],
  trial_duration: 2000,
  data: function() {
    return {
      task: 'stroop',
      word: jsPsych.evaluateTimelineVariable('word'),
      color: jsPsych.evaluateTimelineVariable('color'),
      corr_ans: jsPsych.evaluateTimelineVariable('corr_ans')
    };
  },
  on_load: function() {
    onsetTimestamp = new Date().toISOString();            // Rule 16: 运行时值
  },
  on_finish: function(data) {
    data.accuracy = data.response === null                // Rule 15: 0/1 int
      ? 0
      : Number(jsPsych.pluginAPI.compareKeys(data.response, data.corr_ans));
    data.response_status = data.response === null ? 'timeout' : 'responded';
    data.timestamp = onsetTimestamp;
    data.block = blockIndex;
    data.trial = data.trial_index + 1;                    // 1-based
  }
};

// ③ 反馈（单独的 trial 对象）
const feedbackTrial = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: function() {
    const last = jsPsych.data.get().last(1).values()[0];
    if (last.accuracy === 1) return '<p style="color:green">正确</p>';
    return '<p style="color:red">错误</p>';
  },
  choices: "NO_KEYS",
  trial_duration: FEEDBACK_MS,
  data: { task: 'feedback' }
};

// ④ ITI（jsPsych: 通过 post_trial_gap 实现随机时长）
// post_trial_gap 在 on_finish 之后、下一个 trial 之前自动执行。
// 放在 block 内最后一个 trial 上，确保反应/反馈之后才插入间隔。
const feedbackWithIti = Object.assign({}, feedbackTrial, {
  post_trial_gap: function() {
    return jsPsych.randomization.randomInt(ITI_MIN_MS, ITI_MAX_MS);
  }
});

// 五步组装在 block timeline 中
const trialBlock = {
  timeline: [trial, feedbackWithIti],                   // ①② → ③ → ④
  timeline_variables: conditions,
  randomize_order: true
};
```

**Rule**: trial 对象内部不允许出现裸数字——`trial_duration` 全部引用配置常量。`on_finish` 是唯一可以安全修改 data 的位置。`Number()` 将布尔值转换为 0/1 int。`data.trial_index` 是 0-based，转换为 1-based 后保存。

### 0.8 Per-Trial Data Write (Rules 10, 14–16 — jsPsych: on_data_update checkpoint)

```js
function persistTrialCheckpoint(data) {
  try {
    localStorage.setItem(
      `${AUTOSAVE_KEY}:trial:${data.trial_index}`,
      JSON.stringify(data)
    );
    localStorage.setItem(`${AUTOSAVE_KEY}:last_trial`, String(data.trial_index));
  } catch (error) {
    jsPsych.abortExperiment(`数据保存失败：${error.name === 'QuotaExceededError' ? '存储已满' : '存储不可用'}。`);
    throw error;
  }
}

const jsPsych = initJsPsych({
  on_data_update: persistTrialCheckpoint,  // Rule 10: 每个 trial 后自动触发
  on_close: function() {
    localStorage.setItem(`${AUTOSAVE_KEY}:closed_at`, new Date().toISOString());
  },
  on_finish: function() {
    document.removeEventListener('keydown', handleEmergencyAbort, true);
    jsPsych.data.get().filter({task: 'stroop'}).localSave(       // Rule 11: 阶段保存
      'csv',
      `sub-${SUBJECT_ID}_${EXP_NAME}_${new Date().toISOString().slice(0,10)}.csv`
    );
  }
});
```

**[jsPsych]** `on_data_update` 在每个 trial 写入数据后自动触发——等价于 PsychoPy 的 `nextEntry()`。`localSave('csv')` 在 `on_finish` 中调用——等价于 `saveAsWideText`。localStorage checkpoint 是每个 trial 的耐久备份——浏览器崩溃时，下次加载可恢复。

### 0.9 Main Flow (Rule 8 — jsPsych: declarative timeline, no try/catch)

```js
// jsPsych 是声明式框架 — 没有命令式 try/except/finally 主循环。
// jsPsych.run(timeline) 按 timeline 数组顺序执行。
// on_finish 始终触发（正常结束、abort、Escape 均触发）。
// Escape 通过 addEventListener('keydown', handler, true) 在 capture phase 处理。
//
// 执行顺序等价于:
//   preload → fullscreen → instruction → practice blocks → main blocks → debrief → on_finish

const timeline = [
  preload,                                         // Rule 13: 最先，所有媒体预加载
  { type: jsPsychFullscreen, fullscreen_mode: true },
  instruction,
  practiceBlock,                                   // timeline_variables + repetitions + feedback
  mainBlock,                                       // timeline_variables + repetitions (无 feedback)
  debrief
];
jsPsych.run(timeline);
```

**[jsPsych]** `jsPsych.abortExperiment()` 终止执行后，jsPsych 自动触发 `on_finish`——所以 `localSave` 和 cleanup 在 abort 情况下也能执行。这是 jsPsych 等价于 `finally` 的机制。关键：`handleEmergencyAbort` 的 `addEventListener` 第三个参数**必须是 `true`**（capture phase），否则 jsPsych 插件的事件处理器会先捕获 Escape 按键，导致 abort handler 不触发。

Block 模式——通过 timeline 数组控制哪些 trial 出现：
```js
const practiceBlock = {
  timeline: [fixation, trial, feedback, iti],       // 练习: 有 feedback
  timeline_variables: practiceConditions,
  randomize_order: true,
  repetitions: 1
};

const mainBlock = {
  timeline: [fixation, trial, iti],                 // 正式: 无 feedback
  timeline_variables: mainConditions,
  randomize_order: true,
  repetitions: 4
};
```

### 0.10 Comment Rules (Rule 17)

```js
// 正例 — 解释意图
const AUTOSAVE_KEY = `psycoder-${SUBJECT_ID}-${EXP_NAME}`;  // localStorage 恢复标记

// 正式阶段无反馈 — 仅练习阶段显示 correct/incorrect     ← 解释设计决策

// data.accuracy 用 Number() 确保输出 0/1 而非 true/false  ← 解释非标准做法

// 反例 — 不做
const jsPsych = initJsPsych({...});  // 初始化 jsPsych        ← 代码已自明
choices: ['f', 'j']                  // 设置允许的按键          ← 废话
```

## 1. Minimal Keyboard-Task Scaffolding

This scaffolding shows pinned core/plugin loading for a keyboard task. Select only the plugins required by config; mouse, survey, audio, video, and custom-event tasks need their own verified nodes while preserving the shared persistence/abort/data contracts.

```html
<!DOCTYPE html>
<html>
<head>
  <title>Experiment</title>
  <script src="https://unpkg.com/jspsych@8.2.3"></script>
  <script src="https://unpkg.com/@jspsych/plugin-html-keyboard-response@2.1.0"></script>
  <script src="https://unpkg.com/@jspsych/plugin-image-keyboard-response@2.1.0"></script>
  <script src="https://unpkg.com/@jspsych/plugin-preload@2.1.0"></script>
  <link href="https://unpkg.com/jspsych@8.2.3/css/jspsych.css" rel="stylesheet" type="text/css" />
</head>
<body><div id="jspsych-target"></div></body>
<script>
  // 1. Initialize jsPsych
  const SUBJECT_ID = 'test';
  const SESSION_ID = 'session-1';
  const TASK_VERSION = '1.0.0';
  const RUN_ID = globalThis.crypto?.randomUUID?.();
  if (!RUN_ID) throw new Error('Target browser must provide crypto.randomUUID(); verify the pinned browser/runtime contract.');
  const AUTOSAVE_KEY = `amazing-psycoder-${SUBJECT_ID}-${SESSION_ID}-${RUN_ID}-autosave`;
  function persistTrialCheckpoint(data) {
    try {
      localStorage.setItem(`${AUTOSAVE_KEY}:trial:${data.trial_index}`, JSON.stringify(data));
      localStorage.setItem(`${AUTOSAVE_KEY}:last_trial`, String(data.trial_index));
    } catch (error) {
      const reason = error.name === 'QuotaExceededError'
        ? 'localStorage 已满，请清理浏览器存储'
        : 'localStorage 不可用（可能为隐私模式），请使用普通浏览模式';
      jsPsych.abortExperiment(`数据保存失败：${reason}。`, { abort_reason: 'storage_unavailable' });
      throw error;
    }
  }
  let abortRequested = false;
  function handleEmergencyAbort(event) {
    if (event.key !== 'Escape' || abortRequested) return;
    event.preventDefault();
    abortRequested = true;
    localStorage.setItem(`${AUTOSAVE_KEY}:aborted_at`, new Date().toISOString());
    jsPsych.abortExperiment(
      'The experiment ended safely; the latest checkpoint was preserved.',
      { abort_reason: 'escape' }
    );
  }
  const jsPsych = initJsPsych({
    display_element: 'jspsych-target',
    on_data_update: persistTrialCheckpoint,
    on_close: function() {
      localStorage.setItem(`${AUTOSAVE_KEY}:closed_at`, new Date().toISOString());
    },
    on_finish: function() {
      document.removeEventListener('keydown', handleEmergencyAbort, true);
      jsPsych.data.get().localSave(
        'csv',
        `sub-${SUBJECT_ID}_ses-${SESSION_ID}_run-${RUN_ID}_experiment_data.csv`
      );
      localStorage.setItem(`${AUTOSAVE_KEY}:completed_at`, new Date().toISOString());
    }
  });
  const RNG_SEED = `${TASK_VERSION}|${SUBJECT_ID}|${SESSION_ID}`; // config seed_scope determines the material
  jsPsych.randomization.setSeed(RNG_SEED);
  jsPsych.data.addProperties({
    subject_id: SUBJECT_ID,
    session_id: SESSION_ID,
    run_id: RUN_ID,
    task_version: TASK_VERSION,
    rng_seed: RNG_SEED
  });
  document.addEventListener('keydown', handleEmergencyAbort, true);
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

This compact example uses synchronous per-trial `localStorage` records. A generated deployment must first assess expected payload/quota, privacy, browser lifecycle, and recovery/export requirements; use a tested server or IndexedDB path for larger or centrally managed studies. Never call a device-local checkpoint a remote backup.

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
    return `<p style="color:${jsPsych.evaluateTimelineVariable('color')}">${jsPsych.evaluateTimelineVariable('word')}</p>`;
  },
  choices: ['left', 'down', 'right'],
  data: jsPsych.timelineVariable('data')
};

const stroop_block = {
  timeline: [fixation, trial],
  timeline_variables: stimuli,
  randomize_order: true,
  repetitions: 5
};
```

**关键规则**：
- **静态参数 placeholder**: `stimulus: jsPsych.timelineVariable('name')`
- **函数内立即取值**: `jsPsych.evaluateTimelineVariable('name')`
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

**强制模式** — 每个 trial 后创建耐久 checkpoint，并在正常结束时导出最终 CSV。`on_data_update` 在每次插件写入数据后触发，不能只依赖内存和结束时的 `localSave`：

```js
const AUTOSAVE_KEY = `amazing-psycoder-${subjectID}-${expName}`;
const jsPsych = initJsPsych({
  on_data_update: function() {
    localStorage.setItem(AUTOSAVE_KEY, jsPsych.data.get().json());
  },
  on_close: function() {
    localStorage.setItem(AUTOSAVE_KEY, jsPsych.data.get().json());
  },
  on_finish: function() {
    jsPsych.data.get()
      .filter({task: 'response'})
      .localSave('csv', `sub-${subjectID}_${expName}.csv`);
  }
});
```

采集导出保留原始响应、RT、状态和设计字段。不要在浏览器采集端套用通用 RT 阈值或删除 provenance；已确认的排除规则由分析脚本执行并记录样本流转。

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
| `jsPsych.init()` | legacy initialization | `initJsPsych()` + `jsPsych.run()` |
| `type: 'html-keyboard-response'` (字符串) | current plugins use class references | `type: jsPsychHtmlKeyboardResponse` |
| `jsPsych.NO_KEYS` / `jsPsych.ALL_KEYS` | legacy constants | `"NO_KEYS"` / `"ALL_KEYS"` (strings) |
| `jsPsych.timelineVariable('x', true)` inside a function | v7 immediate-evaluation pattern, not current API | `jsPsych.evaluateTimelineVariable('x')` |
| `timeline_variables` 作为函数 | 不支持运行时生成 | 在脚本加载时预计算所有条件 |
| `setTimeout` / `setInterval` 实现计时 | 不精确，破坏 jsPsych 事件循环 | `trial_duration` 参数 |
| `Date.now()` 手动计时 | jsPsych 自动记录 RT | 使用 `data.rt` |
| 媒体任务未在首次使用前 preload | 运行时加载会污染呈现 | 媒体任务把 `preload` 放在首次媒体 trial 前；纯 HTML/文本任务无需空 preload 节点 |
| `XMLHttpRequest` / `fetch` 在 trial 内加载 xlsx | 网络延迟破坏计时 | 预计算为 JavaScript 数组 |
| 硬编码 `keyCode` 数字 | 跨浏览器不可靠 | `jsPsych.pluginAPI.convertKeyCharacterToKeyCode('f')` 或直接使用 `'f'` |
| 在 `on_finish` 中修改 data 后不做 return | 修改不会反映到保存的数据中 | 直接修改传入的 `data` 对象（它是引用） |
| 不处理 Escape 键，或把 Escape 混入计分 `choices` | 无法安全退出，或把中止键误记为任务反应 | 使用跨阶段集中 `keydown` handler；先写 abort checkpoint，再调用 `jsPsych.abortExperiment()`，并在 `on_finish` 移除 listener |
| 只在实验结束时 `localSave` | 关闭/崩溃会丢失整场数据 | `on_data_update` 持久化到 server/IndexedDB/localStorage，结束时再 `localSave` |

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

## 8. Canonical Code Skeleton — Keyboard Task

以下是 pinned keyboard 参考骨架，展示版本、seed、持久化、退出与语义数据字段。它不是所有范式的通用实现；生成器必须按 config 选择插件和事件模型，并记录任何契约偏离的理由与测试。

```html
<!-- {filename}.html -->
<!--
  一体化流程：
    指导语 → 练习 → 正式实验 → 结束

  数据输出：
    on_finish → sub-{id}_{task}_{date}.csv
    on_data_update → localStorage durable checkpoint

  设计概要：
    每个 block：{n} trial
    正式阶段：{m} block × {t} = {total} trial

  当前版本关键修改：
    1) {change_1}
    2) {change_2}
-->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{experiment_name}</title>
  <!-- ============================================================
  一、CDN 版本 + CSS
  ============================================================ -->
  <script src="https://unpkg.com/jspsych@8.2.3"></script>
  <script src="https://unpkg.com/@jspsych/plugin-html-keyboard-response@2.1.0"></script>
  <script src="https://unpkg.com/@jspsych/plugin-preload@2.1.0"></script>
  <script src="https://unpkg.com/@jspsych/plugin-fullscreen@2.1.0"></script>
  <link href="https://unpkg.com/jspsych@8.2.3/css/jspsych.css" rel="stylesheet" type="text/css" />
  <style>
    body {
      font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
    }
  </style>
</head>
<body></body>
<script>
  // ============================================================
  // 二、实验常量
  // ============================================================
  const SUBJECT_ID   = 'test';
  const SESSION_ID   = 'session-1';
  const TASK_VERSION = '1.0.0';
  const EXP_NAME     = '{experiment_name}';
  const BASE_DATA_COLUMNS = [
    'subject_id', 'block', 'trial', 'condition', 'stimulus',
    'correct_response', 'response', 'rt', 'accuracy', 'timestamp'
  ];
  const RUN_ID = globalThis.crypto?.randomUUID?.();
  if (!RUN_ID) throw new Error('Target browser must provide crypto.randomUUID().');

  // ============================================================
  // 三、文本常量（所有指导语/反馈 HTML 集中在此）
  // ============================================================
  const txtWelcome = '<p>欢迎参加实验。</p><p>按空格键开始。</p>';
  const txtEnd = '<p>实验结束，感谢参与！</p><p>按任意键退出。</p>';

  // ---------- 时序 (ms) ----------
  const FIXATION_MS    = 500;
  const STIMULUS_MS    = 1000;
  const FEEDBACK_MS    = 500;
  const RESP_DEADLINE_MS = 2000;
  const ITI_MIN_MS     = 600;
  const ITI_MAX_MS     = 900;

  // ---------- 按键 ----------
  const RESP_KEYS = ['f', 'j'];

  // ---------- 约束 ----------
  const MAX_PSEUDORAND_TRIES = 5000;

  // ============================================================
  // 四、退出安全网 + 耐久 checkpoint
  // ============================================================
  const AUTOSAVE_KEY = `psycoder-${SUBJECT_ID}-${EXP_NAME}-${RUN_ID}`;
  function persistTrialCheckpoint(data) {
    try {
      localStorage.setItem(
        `${AUTOSAVE_KEY}:trial:${data.trial_index}`,
        JSON.stringify(data)
      );
      localStorage.setItem(`${AUTOSAVE_KEY}:last_trial`, String(data.trial_index));
    } catch (error) {
      jsPsych.abortExperiment('Checkpoint persistence failed.');
      throw error;
    }
  }
  let abortRequested = false;
  function handleEmergencyAbort(event) {
    if (event.key !== 'Escape' || abortRequested) return;
    event.preventDefault();
    abortRequested = true;
    localStorage.setItem(`${AUTOSAVE_KEY}:aborted_at`, new Date().toISOString());
    jsPsych.abortExperiment('实验已安全终止。', { abort_reason: 'escape' });
  }
  // ⚠️ 不要在此处注册 handleEmergencyAbort — jsPsych 尚未创建。
  // addEventListener 必须在 initJsPsych 之后注册。

  // ============================================================
  // 五、jsPsych 初始化
  // ============================================================
  let onsetTimestamp = '';
  let blockIndex = 0;
  const jsPsych = initJsPsych({
    on_data_update: persistTrialCheckpoint,
    on_close: function() {
      localStorage.setItem(`${AUTOSAVE_KEY}:closed_at`, new Date().toISOString());
    },
    on_finish: function() {
      document.removeEventListener('keydown', handleEmergencyAbort, true);
      jsPsych.data.get().filter({task: 'main'}).localSave(
        'csv',
        `sub-${SUBJECT_ID}_${EXP_NAME}_${new Date().toISOString().slice(0,10)}.csv`
      );
      localStorage.setItem(`${AUTOSAVE_KEY}:completed_at`, new Date().toISOString());
    }
  });
  // Escape 监听器必须在 jsPsych 创建之后注册（此时 jsPsych 已存在）
  document.addEventListener('keydown', handleEmergencyAbort, true);

  const RNG_SEED = `${TASK_VERSION}|${SUBJECT_ID}|${SESSION_ID}`;
  jsPsych.randomization.setSeed(RNG_SEED);
  jsPsych.data.addProperties({
    subject_id: SUBJECT_ID,
    session_id: SESSION_ID,
    run_id: RUN_ID,
    task_version: TASK_VERSION,
    rng_seed: RNG_SEED
  });

  // ============================================================
  // 六、条件定义（预计算）
  // ============================================================
  const stimuli = [
    { word: 'RED',  color: 'red',   corr_ans: 'f' },
    { word: 'GREEN', color: 'green', corr_ans: 'j' },
  ];
  const fullConditions = [];
  stimuli.forEach(function(row) {
    stimuli.forEach(function(col) {
      fullConditions.push({
        word: row.word,
        color: col.color,
        corr_ans: col.corr_ans,
        congruent: row.word === col.word
      });
    });
  });

  // ============================================================
  // 七、Trial 定义（声明式对象）
  // ============================================================

  // --- 注视点 ---
  const fixation = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<div style="font-size:60px;">+</div>',
    choices: "NO_KEYS",
    trial_duration: FIXATION_MS,                        // Rule 13: 引用常量
    data: { task: 'fixation' }
  };

  // --- 刺激 + 响应 ---
  const trial = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: function() {
      const word = jsPsych.evaluateTimelineVariable('word');
      const color = jsPsych.evaluateTimelineVariable('color');
      return `<p style="color:${color}; font-size:96px;">${word}</p>`;
    },
    choices: RESP_KEYS,
    trial_duration: RESP_DEADLINE_MS,
    data: function() {
      return {
        task: 'main',
        word: jsPsych.evaluateTimelineVariable('word'),
        color: jsPsych.evaluateTimelineVariable('color'),
        corr_ans: jsPsych.evaluateTimelineVariable('corr_ans'),
        congruent: jsPsych.evaluateTimelineVariable('congruent')
      };
    },
    on_load: function() {
      onsetTimestamp = new Date().toISOString();        // Rule 16: 运行时值
    },
    on_finish: function(data) {
      data.block = blockIndex;
      data.trial = data.trial_index + 1;                // 1-based
      data.condition = data.congruent ? 'congruent' : 'incongruent';
      data.stimulus = `${data.word}|${data.color}`;
      data.correct_response = data.corr_ans;
      data.response_status = data.response === null ? 'timeout' : 'responded';
      data.rt = data.rt === null ? null : Math.round(data.rt);
      data.accuracy = data.response === null            // Rule 15: 0/1 int
        ? 0
        : Number(jsPsych.pluginAPI.compareKeys(data.response, data.corr_ans));
      data.timestamp = onsetTimestamp;
    }
  };

  // --- 反馈（仅练习阶段）---
  const feedback = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: function() {
      const accuracy = jsPsych.data.get().last(1).values()[0].accuracy;
      if (accuracy === 1) return '<p style="color:green; font-size:48px;">正确</p>';
      return '<p style="color:red; font-size:48px;">错误</p>';
    },
    choices: "NO_KEYS",
    trial_duration: FEEDBACK_MS,
    post_trial_gap: function() {                           // 反馈后的随机 ITI
      return jsPsych.randomization.randomInt(ITI_MIN_MS, ITI_MAX_MS);
    },
    data: { task: 'feedback' }
  };

  // --- 正式 trial（自带随机 ITI）---
  // jsPsych: post_trial_gap 在 on_finish 后、下一个 trial 前自动执行。
  // 放在 block 内最后一个 trial 上，确保反应/反馈之后才插入 ITI。
  const mainTrial = Object.assign({}, trial, {
    post_trial_gap: function() {
      return jsPsych.randomization.randomInt(ITI_MIN_MS, ITI_MAX_MS);
    }
  });

  // ============================================================
  // 八、Block 定义
  // ============================================================
  // 每个 block 的 timeline 应用于 timeline_variables 中的每一行。
  // practiceBlock: 每个条件执行 fixation → trial → feedback（feedback 后带 ITI）
  // mainBlock: 每个条件执行 fixation → mainTrial（trial 后带 ITI，无 feedback）
  const practiceBlock = {
    timeline: [fixation, trial, feedback],
    timeline_variables: fullConditions,
    randomize_order: true,
    repetitions: 1
  };

  const mainBlock = {
    timeline: [fixation, mainTrial],
    timeline_variables: fullConditions,
    randomize_order: true,
    repetitions: 4
  };

  // ============================================================
  // 九、Timeline 组装 + 启动
  // ============================================================
  const preload = {
    type: jsPsychPreload,
    auto_preload: true
  };

  const welcome = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: txtWelcome,
    choices: [' ']
  };

  const endScreen = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: txtEnd,
    choices: "ALL_KEYS"
  };

  const timeline = [
    preload,                                              // Rule 13: 最先预加载
    { type: jsPsychFullscreen, fullscreen_mode: true },
    welcome,
    practiceBlock,
    mainBlock,
    endScreen
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
| 数据保存 | `on_data_update` durable checkpoint + final `.localSave('csv', filename)` |
| 数据显示（调试） | `jsPsych.data.displayData()` |
| 鼠标轨迹 | `extension-mouse-tracking` |
| 眼动追踪 | `extension-webgazer` |
