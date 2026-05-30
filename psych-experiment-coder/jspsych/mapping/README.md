# jsPsych / PsychoJS Config → Code Mapping

> **Layer 2**: Config YAML → JavaScript 代码结构映射。覆盖 jsPsych 7.x（推荐）、jsPsych 6.1.0（历史）和 PsychoJS（Pavlovia）三个目标。

## 关键架构区分：三个不同的目标

| 维度 | jsPsych 7.x（推荐） | jsPsych 6.1.0（历史） | PsychoJS (Pavlovia) |
|------|---------------------|----------------------|---------------------|
| **架构** | 声明式 timeline | 声明式 timeline | 命令式 Scheduler |
| **初始化** | `initJsPsych()` + `jsPsych.run()` | `jsPsych.init({timeline: [...]})` | `psychoJS.start()` + `flowScheduler.add()` |
| **插件类型** | class 引用: `jsPsychHtmlKeyboardResponse` | 字符串: `'html-keyboard-response'` | Routine Begin/EachFrame/End 函数组 |
| **条件处理** | `timeline_variables` 数组 | `timeline_variables` 数组 | `TrialHandler` + xlsx 文件 |
| **RT 记录** | 自动 `.rt`（`performance.now()`，ms） | 自动 `.rt` | `callOnFlip(clock.reset)` + `key_resp.rt` |
| **准确性** | `on_finish` + `jsPsych.pluginAPI.compareKeys()` | `key_answer` / `on_finish` 回调 | 手动 `resp.keys == corrAns` |
| **按键映射** | `choices: ['f', 'j']` | `choices: ['f', 'j']` + `key_answer` 函数 | `key_resp.getKeys({keyList: ['f', 'j']})` |
| **无按键** | `choices: "NO_KEYS"`（字符串） | `choices: jsPsych.NO_KEYS` | `key_resp` component 不添加 |
| **时长控制** | `trial_duration: N`（ms） | `trial_duration: N`（ms） | `routineTimer.getTime() < N/1000` |
| **ITI** | `post_trial_gap: N` | `post_trial_gap: N` | 独立 ISI Routine |
| **数据保存** | `jsPsych.data.get().localSave('csv', fn)` | `jsPsych.data.get().localSave('csv')` | `psychoJS.experiment.nextEntry()` → server upload |
| **预加载** | `jsPsychPreload` + `auto_preload: true` | 无需（HTML 渲染） | Component 在 `experimentInit()` 中初始化 |
| **范式文件** | 需迁移（当前 25 个均为 v6.1/PsychoJS） | IAT, EAST（2 个原生） | 22 个 PsychoJS + 1 lab.js |
| **全屏** | `jsPsychFullscreen` plugin | `'fullscreen'` plugin | `psychoJS.openWindow({fullscr: true})` |

**关键结论**: 新代码必须使用 jsPsych 7.x API。jsPsych 6.1.0 模式仅存在于历史范式文件中。PsychoJS 是 PsychoPy Builder 的 JavaScript 运行时，代码结构完全不同。

## Config → Code 映射表（jsPsych 7.x）

| Config section | jsPsych code generated |
|---------------|----------------------|
| `name` | `const expName = '{name}'` + timeline 注释 |
| `paradigm` | 范式逻辑 → `timeline_variables` + `on_finish` accuracy |
| `windows[]` | Nested timeline per trial: `timeline: [{fixation node}, {stimulus node}, ...]` |
| `windows[].content: "{col}"` | `stimulus: function() { return jsPsych.timelineVariable('col', true) }` |
| `windows[].duration: N` | `trial_duration: N` — 无 response 时配合 `choices: "NO_KEYS"` |
| `windows[].duration: [min, max]` | `trial_duration: function() { return Math.random()*(max-min)+min }` |
| `windows[].response: [keys]` | `choices: [keys]` + `response_ends_trial: true` |
| `windows[].rt_onset` | jsPsych 自动：RT 从 stimulus 出现到按键，记录在 `data.rt` |
| `blocks[]` | 顶层 `timeline: [block1, block2, ...]` — 每个 block 是独立 timeline 对象 |
| `blocks[].condition_file` | `timeline_variables: conditionsArray`（JS 数组，非文件加载） |
| `response_rules.correct` | `on_finish: function(data) { data.correct = jsPsych.pluginAPI.compareKeys(data.response, data.correct_response) }` |
| `response_rules.mapping` | `choices: ['f', 'j']` + `data:` 中附带 `correct_response` 字段 |
| `paradigm_config` | 范式特定 — IAT 7-block 结构、SSD staircase、n-back target detection |
| `display` | CSS + `jsPsychFullscreen` plugin + `document.body.style` |
| `font` | CSS `font-family` 属性 + `<link>` Google Fonts 或系统字体 fallback |
| `audio` | `jsPsychAudioKeyboardResponse` plugin（`stimulus` 填音频路径），或 `jsPsychPreload` 预加载 `audio` 数组 |
| `participant_info` | 自定义 HTML 表单（实验前显示），或 URL query params（`?subject=001`），存储到 `jsPsych.data.addProperties()` |
| `output` | `jsPsych.data.get().filter({...}).localSave('csv', filename)` |

## Config → Code 映射表（PsychoJS）

| Config section | PsychoJS code generated |
|---------------|------------------------|
| `name` | `expName = '{name}'` in `psychoJS.start({expName})` |
| `windows[]` | Routine Begin/EachFrame/End 函数组，每个 window = component 状态转换 |
| `windows[].content: "{col}"` | `stimulus.setText(thisTrial['col'])` |
| `windows[].duration: N` | `if tThisFlipGlobal > comp.tStartRefresh + N/1000 - frameTolerance` → FINISHED |
| `windows[].response: [keys]` | `core.Keyboard()` + `key_resp.getKeys({keyList: [keys]})` + `callOnFlip(clock.reset)` |
| `windows[].rt_onset` | `psychoJS.window.callOnFlip(function() { key_resp.clock.reset(); })` |
| `blocks[]` | `TrialHandler({nReps: N, method: RANDOM, trialList: 'conditions.xlsx'})` |
| `blocks[].condition_file` | xlsx/csv 文件名传给 `TrialHandler` 的 `trialList` 参数 |
| `response_rules.correct` | `resp.keys == corr_ans` 在 trialRoutineEnd 中判断 |
| `output` | `psychoJS.experiment.dataFileName` + server-side CSV download |

## Windows[] → Timeline 节点映射（jsPsych 7.x）

jsPsych 7.x 的声明式特性使 `windows[]` 映射为嵌套 timeline 节点数组。

### 基本节点模式

```js
// 典型 trial：Fixation → Stimulus + Response
const trialTimeline = {
    timeline: [
        // Window 1: Fixation (fixed duration, no response)
        {
            type: jsPsychHtmlKeyboardResponse,
            stimulus: '<div style="font-size:60px;">+</div>',
            choices: "NO_KEYS",               // v7: string, not jsPsych.NO_KEYS
            trial_duration: 500,
            response_ends_trial: false,
            data: { window: 'fixation' }
        },
        // Window 2: Stimulus + Response
        {
            type: jsPsychHtmlKeyboardResponse,
            stimulus: function() {
                return jsPsych.timelineVariable('stim', true);  // v7: second arg = true
            },
            choices: ['f', 'j'],
            response_ends_trial: true,
            data: { window: 'target' }
        }
    ]
};
```

### 反馈节点（categorize-html 插件）

```js
// Practice trial with feedback
{
    type: jsPsychCategorizeHtml,      // v7: class reference
    stimulus: jsPsych.timelineVariable('s'),
    choices: ['f', 'j'],
    key_answer: 'f',                  // 或动态: key_answer: function() { return ... }
    correct_text: "<span style='color:green'>√</span>",
    incorrect_text: "<span style='color:red'>X</span>",
    feedback_duration: 500,
    force_correct_button_press: true,
    show_stim_with_feedback: true
}
```

### 嵌套 Timeline（条件变量驱动）

```js
// 顶层: block template
const stroopBlock = {
    timeline_variables: fullConditions,   // [{word:'RED', color:'red', corr_ans:'left'}, ...]
    timeline: [fixationNode, trialNode],
    randomize_order: true,
    repetitions: 5
};

// 顶层: 实验结构
const timeline = [
    { type: jsPsychFullscreen, fullscreen_mode: true },
    instructionTrial,
    practiceBlock,
    mainBlock,
    debriefTrial
];

const jsPsych = initJsPsych({
    on_finish: function() {
        jsPsych.data.get().filter({task:'stroop'}).localSave('csv', 'stroop_data.csv');
    }
});
jsPsych.run(timeline);
```

### Windows[] → Timeline 映射规则

| Config window | jsPsych 7.x timeline node | 关键参数 |
|--------------|--------------------------|---------|
| Fixation (duration: N, no response) | `{type: jsPsychHtmlKeyboardResponse, stimulus: '+', choices: "NO_KEYS", trial_duration: N}` | `response_ends_trial: false` |
| Stimulus (content: {col}, duration: N) | `{type: jsPsychHtmlKeyboardResponse, stimulus: fn() { return jsPsych.timelineVariable('col', true) }, trial_duration: N}` | `choices: "NO_KEYS"` |
| Stimulus + Response (content: {col}, response: [keys]) | `{type: jsPsychHtmlKeyboardResponse, stimulus: fn(){...}, choices: [keys]}` | `response_ends_trial: true` |
| Stimulus + Response + Feedback | `{type: jsPsychCategorizeHtml, stimulus: ..., choices: [keys], key_answer: fn}` | `force_correct_button_press: true/false` |
| Image stimulus | `{type: jsPsychImageKeyboardResponse, stimulus: fn(){...}, choices: [keys]}` | `stimulus` 填图片路径 |
| ITI (duration: N) | `post_trial_gap: N` 在前一个节点上 | 或独立空白节点 |
| Instruction | `{type: jsPsychHtmlKeyboardResponse, stimulus: text, choices: [' ']}` | |
| 多页指令 | `{type: jsPsychInstructions, pages: [page1, page2, ...], key_forward: ' '}` | `allow_backward: false` |

## Windows[] → Routine 映射（PsychoJS）

PsychoJS 是命令式的 — 每个 window 对应 component 在 `EachFrame` 中的状态机转换：

```javascript
// PsychoJS Routine 三段式结构
function trialRoutineBegin(snapshot) {
  return async function() {
    trialClock.reset();
    frameN = -1;
    continueRoutine = true;

    // Component 参数更新
    target.setPos([target_x, target_y]);
    key_resp.keys = undefined;
    key_resp.rt = undefined;
    _key_resp_allKeys = [];

    for (const comp of trialComponents)
      if ('status' in comp) comp.status = PsychoJS.Status.NOT_STARTED;

    return Scheduler.Event.NEXT;
  };
}

function trialRoutineEachFrame() {
  return async function() {
    t = trialClock.getTime();
    frameN++;

    // Fixation component: t >= 0 → STARTED, t >= 500ms → FINISHED
    // Target component: t >= 500ms → STARTED
    if (t >= 0.5 && target.status === PsychoJS.Status.NOT_STARTED) {
      target.tStart = t;
      target.setAutoDraw(true);
      // RT clock reset on flip
      psychoJS.window.callOnFlip(function() { key_resp.clock.reset(); });
      psychoJS.window.callOnFlip(function() { key_resp.start(); });
    }

    // Keyboard component: STARTED → poll keys
    if (key_resp.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_resp.getKeys({keyList: ['left', 'right'], waitRelease: false});
      _key_resp_allKeys = _key_resp_allKeys.concat(theseKeys);
      if (_key_resp_allKeys.length > 0) {
        key_resp.keys = _key_resp_allKeys[_key_resp_allKeys.length - 1].name;
        key_resp.rt = _key_resp_allKeys[_key_resp_allKeys.length - 1].rt;
        continueRoutine = false;
      }
    }

    // Escape check
    if (psychoJS.eventManager.getKeys({keyList: ['escape']}).length > 0)
      return quitPsychoJS('Esc pressed', false);

    if (!continueRoutine) return Scheduler.Event.NEXT;

    // Component status check
    continueRoutine = false;
    for (const comp of trialComponents)
      if (comp.status !== PsychoJS.Status.FINISHED)
        { continueRoutine = true; break; }

    return continueRoutine ? Scheduler.Event.FLIP_REPEAT : Scheduler.Event.NEXT;
  };
}

function trialRoutineEnd(snapshot) {
  return async function() {
    for (const comp of trialComponents)
      if (typeof comp.setAutoDraw === 'function') comp.setAutoDraw(false);

    // Accuracy check
    key_resp.corr = (key_resp.keys == corr_ans) ? 1 : 0;

    psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
    psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
    psychoJS.experiment.addData('key_resp.corr', key_resp.corr);

    return Scheduler.Event.NEXT;
  };
}
```

## 条件处理对比

### jsPsych 7.x: timeline_variables 数组

```js
// 方式 1: 内联数据数组
const stimArray = [
    { data: { stim_type: 'pos' }, s: '健康', corr_ans: 'f' },
    { data: { stim_type: 'neg' }, s: '邪恶', corr_ans: 'j' },
];

const block = {
    timeline_variables: stimArray,
    timeline: [fixationNode, categorizationNode],
    repetitions: 2,
    randomize_order: true
};

// 方式 2: jsPsych.randomization.factorial（因子设计）
const factors = {
    cue_validity: ['valid', 'invalid'],
    target_location: ['left', 'right']
};
const conditions = jsPsych.randomization.factorial(factors);
// 生成 4 条: [{cue_validity:'valid', target_location:'left'}, ...]

// 方式 3: 脚本加载时预计算（仅此一次）
const fullConditions = [];
congruentWords.forEach(function(row) {
    incongruentWords.forEach(function(col) {
        fullConditions.push({
            word: row.word, color: col.color,
            corr_ans: col.corr_ans,
            congruent: row.word === col.word
        });
    });
});
```

**关键**: jsPsych 7.x 不使用外部 xlsx/csv 文件 — 所有条件在 JavaScript 代码内定义为数组。

### PsychoJS: TrialHandler + xlsx

```javascript
// 从外部 xlsx 文件加载条件
trials = new TrialHandler({
    psychoJS: psychoJS,
    nReps: 1,
    method: TrialHandler.Method.RANDOM,
    trialList: 'conditions.xlsx',  // 外部文件
    seed: undefined,
    name: 'trials'
});

// 资源需在 psychoJS.start() 中注册
psychoJS.start({
    resources: [
        {'name': 'conditions.xlsx', 'path': 'conditions.xlsx'},
    ]
});

// 每 trial 注入条件变量
async function importConditions(snapshot) {
    return async function() {
        for (const paramName in currentLoop.getCurrentTrial()) {
            window[paramName] = currentLoop.getCurrentTrial()[paramName];
        }
        return Scheduler.Event.NEXT;
    };
}
```

## 准确性判断对比

| 平台 | 方式 | 代码 |
|------|------|------|
| jsPsych 7.x | `on_finish` 回调（推荐） | `on_finish: function(data) { data.correct = jsPsych.pluginAPI.compareKeys(data.response, data.correct_response) }` |
| jsPsych 7.x | `correctness_field` 参数 | `data: { correct_response: 'f' }` + `correctness_field: 'correct_response'` |
| jsPsych 7.x | `categorize-html` 内置 | `key_answer: 'f'` — 插件自动记录 `data.correct` |
| jsPsych 6.1.0 | `key_answer` 函数 | `key_answer: function() { return stim_type === 'pos' ? keyCode('f') : keyCode('j') }` |
| PsychoJS | Routine 结束层 | `key_resp.corr = (key_resp.keys == corr_ans) ? 1 : 0` |
| PsychoJS | 无响应处理 | `if (key_resp.keys == undefined) { key_resp.corr = (corr_ans == 'none') ? 1 : 0 }` |

## RT 处理对比

| 平台 | RT 计时方式 | 精度 |
|------|----------|------|
| jsPsych 7.x | 插件自动：stimulus 出现 → 按键，记录在 `data.rt`（ms） | ms 级（`performance.now()`） |
| jsPsych 6.1.0 | 插件自动：记录在 `.rt`（ms） | ms 级 |
| PsychoJS | `callOnFlip(key_resp.clock.reset())` → `.rt` 自动从 reset 算起 | 帧精确 |

## 数据保存模式对比

### jsPsych 7.x: 声明式过滤 + localSave

```js
const jsPsych = initJsPsych({
    on_finish: function() {
        jsPsych.data.get()
            .filter({task: 'response'})              // 仅正式实验数据
            .filterCustom(function(t) {               // 自定义 RT 过滤
                return t.rt > 200 && t.rt < 3000;
            })
            .ignore(['internal_node_id', 'stimulus', 'trial_type', 'plugin_version'])
            .localSave('csv', `${expName}_${subID}.csv`);
    }
});
```

### PsychoJS: ExperimentHandler 自动管理

```javascript
// 每 trial 写入
psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
psychoJS.experiment.nextEntry();

// 数据文件名在 init 时设定
psychoJS.experiment.dataFileName = `data/${participant}_${expName}_${date}`;
// 数据自动上传到 Pavlovia 服务器
```

## 12 步模板实现对比

| 步骤 | jsPsych 7.x | jsPsych 6.1.0 | PsychoJS |
|------|-----------|--------------|----------|
| 1 Imports | `<script src="unpkg.com/jspsych@7.3.4">` + 独立 plugin scripts | `<script>` tags + inline JS | `import { core, data, util, visual } from './lib/psychojs-*.js'` |
| 2 Params | `const jsPsych = initJsPsych({...})` | `const subID = jsPsych.randomization.randomID(8)` | `expInfo = {participant: '', session: '001'}` |
| 3 Display | `jsPsychFullscreen` plugin + CSS 样式 | `'fullscreen'` plugin + CSS | `psychoJS.openWindow({fullscr: true, units: 'height'})` |
| 4 Preloading | `jsPsychPreload` + `auto_preload: true` | 无需（HTML/CSS 渲染） | Component 在 `experimentInit()` 中初始化 |
| 5 Condition | `timeline_variables: conditionsArray` | `timeline_variables: stimArray` | `new TrialHandler({trialList: 'conditions.xlsx'})` |
| 6 Helpers | `jsPsych.randomization.factorial()` / 预计算函数 | `function keyCode(c)`, `blockTemplate(...)` | `importConditions()`, `showExpInfoDlg()` |
| 7 Instruction | `jsPsychInstructions` 或 `jsPsychHtmlKeyboardResponse` | `{type:'html-keyboard-response', stimulus: instrText}` | `instructionsRoutineBegin/EachFrame/End` |
| 8 Practice | `jsPsychCategorizeHtml` + `force_correct_button_press: true` | `categorize-html` + `force_correct_button_press` | 独立 `TrialHandler` + feedback Routine |
| 9a Block | `timeline: [block1, block2, ...]` | `timeline: [block1, block2, ...]` | `for (const trial of trials)` in `trialsLoopBegin()` |
| 9b Randomize | `randomize_order: true` | `randomize_order: true` | `TrialHandler.Method.RANDOM` |
| 9c Per-trial | Timeline 节点数组 | Timeline 节点数组 | Routine Begin/EachFrame/End 三段 |
| 9d Block fb | `on_finish` 中计算并显示 | `categorize-html` correct_text/incorrect_text | 独立 feedback Routine |
| 10 Data save | `jsPsych.data.get().localSave('csv', fn)` | `jsPsych.data.get().localSave('csv')` | `addData()` + `nextEntry()` |
| 11 Cleanup | `jsPsych.endExperiment()` | `jsPsych.endExperiment()` | `quitPsychoJS(msg)` → `closeWindow()` |
| 12 Package | 单个 `.html` + CDN scripts | 单个 `.html` + inline JS | 单个 `.js` 模块 |

## jsPsych 6.1.0 → 7.x 迁移速查

从现有范式文件（大部分为 6.1.0/PsychoJS）迁移到 7.x 的核心变更：

| 6.1.0 模式 | 7.x 替代 | 影响范围 |
|-----------|---------|---------|
| `jsPsych.init({timeline: t})` | `initJsPsych({...}); jsPsych.run(t)` | 所有实验 |
| `type: 'html-keyboard-response'` | `type: jsPsychHtmlKeyboardResponse` | 所有 trial 节点 |
| `type: 'categorize-html'` | `type: jsPsychCategorizeHtml` | 反馈 trial |
| `type: 'call-function'` | `type: jsPsychCallFunction` | 工具函数调用 |
| `type: 'fullscreen'` | `type: jsPsychFullscreen` | 全屏请求 |
| `jsPsych.NO_KEYS` | `"NO_KEYS"`（字符串） | fixation / 无响应节点 |
| `jsPsych.ALL_KEYS` | `"ALL_KEYS"`（字符串） | 任意按键响应 |
| `jsPsych.timelineVariable('x')` in function | `jsPsych.timelineVariable('x', true)` | 函数内引用 |
| `jsPsych.currentTimelineNodeID()` | `jsPsych.getCurrentTimelineNodeID()` | getter 迁移 |
| `jsPsych.progress()` | `jsPsych.getProgress()` | getter 迁移 |
| `jsPsych.totalTime()` | `jsPsych.getTotalTime()` | getter 迁移 |
| `jsPsych.data.get().select('col')` | `.filter({...})` + `.ignore([...])` | 数据过滤 |

## 范式架构对比

| 范式 | 平台 | 关键架构模式 |
|------|------|-----------|
| IAT | jsPsych 6.1.0 | 7-block 工厂函数, `factorial` counterbalance, D-score `on_finish` |
| EAST | jsPsych 6.1.0 | 3-phase: 2 practice + 1 test, color-word mapping via `stim_type`, `key_answer` 动态函数 |
| Antisaccade | PsychoJS | Routine Begin/EachFrame/End, `conditions.xlsx`, `callOnFlip(clock.reset)` |
| Change-detection | PsychoJS | 2-phase: detection + localisation, dynamic `ShapeStim`, CSV-driven positions |
| Sternberg | PsychoJS | 2-phase: practice + main, xlsx-defined memory sets, `TextStim` sequential |
| Bilingual-Stroop | PsychoJS | Dual-language word display, `TextBox2`, key-mapping by color |
| Numerical-Stroop | PsychoJS | Number pair comparison, size-congruency manipulation, feedback Routine |

## 反模式速查（Config→Code 生成特化）

> 通用 API 反模式见 [spec/README.md](../spec/README.md#5-反模式速查表)。

| 平台 | 禁止的模式 | 替代 |
|------|----------|------|
| jsPsych 7.x | `timeline_variables` 作为函数 | 脚本加载时预计算所有条件（条件文件映射为 JS 数组） |
| jsPsych 7.x | 不在 timeline 起始放 preload | `timeline: [preload, ...]` — 刺激预加载必须作为 timeline 第一个节点 |
| PsychoJS | 在 trial 循环内 `new visual.TextStim()` | `experimentInit()` 中初始化，循环内只 `.setText()` — 对应 config 的 stimulus_folder 预加载规则 |
