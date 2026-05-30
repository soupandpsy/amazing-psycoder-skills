# PsychoPy Config → Code Mapping

> **Layer 2**: Config YAML → PsychoPy 代码结构映射。基于 stroop、go-nogo、stop-signal、dot-probe、n-back 五个范式的代码分析 + psychopy.org 官方 API 文档。

## 三版本 PsychoPy 代码模式对照

Pavlovia demo 代码跨越 v3.1 → v2024.2，关键差异影响代码生成：

| 维度 | Old (v3.1) | Modern (v2023.2) | Latest (v2024.2) |
|------|-----------|-----------------|-----------------|
| 条件变量注入 | `exec('{} = thisTrial[p]'.format(p))` | `globals()[p] = thisTrial[p]` | `globals()[p] = thisTrial[p]` |
| 帧时间 | `t = trialClock.getTime()` | `tThisFlip = win.getFutureFlipTime(clock=routineTimer)` | 同 v2023.2 |
| 全局时间 | 无 | `tThisFlipGlobal = win.getFutureFlipTime(clock=None)` | 同 v2023.2 |
| 帧容差 | 无（硬编码 `t >= 0.5`） | `frameTolerance = 0.001` | 同 v2023.2 |
| 计时器 | `core.Clock()` | `routineTimer = core.Clock()` | 同 v2023.2 |
| TrialHandler | `data.TrialHandler(nReps=5, method='random')` | 同 | `data.TrialHandler2`（Pavlovia 兼容） |
| 文本组件 | `visual.TextStim` | `visual.TextBox2`（推荐） | 同 v2023.2 |
| 键盘后端 | `keyboard.Keyboard()` | `keyboard.Keyboard(backend='iohub')` | `keyboard.Keyboard(backend='ptb')` **首选** |
| 音频后端 | 无明确指定（pygame 默认） | `sound.Sound()` | `sound.Sound()` — **PTB 首选**，`preBuffer=-1` |
| 暂停/退出 | `core.quit()` | `pauseExperiment()` + `endExperiment()` | 同 v2023.2 |
| 函数封装 | 全内联 | `showExpInfoDlg()`, `setupData()`, `setupWindow()`, `setupInputs()`, `run()` | 同 v2023.2 |

**生成优先级**: Latest (v2024.2) 模式为首选 — `backend='ptb'` 键盘 + PTB 音频 + `TextBox2` + `globals()` 注入。

## Config → Code 映射表

| Config section | PsychoPy code generated |
|---------------|------------------------|
| `name` | `expName = '{name}'` + script docstring |
| `paradigm` | 加载范式知识，应用 SSD staircase / n-back match / go-nogo ratio 等逻辑 |
| `stimulus_folder` | 全局路径前缀，拼接到 `image.setImage(stimulus_folder + '/' + {column})` |
| `windows[]` | Trial 事件循环 — 每个 window 对应 component 状态机 |
| `windows[].content: "{col}"` | `TextStim` / `TextBox2` / `ImageStim`，值从 condition 列取值 |
| `windows[].duration: N` | `routineTimer.getTime() < N/1000` 循环守卫，component 在 `tThisFlipGlobal > tStartRefresh + N/1000 - frameTolerance` 时 FINISHED |
| `windows[].duration: [min, max]` | `random.randint(min, max) / 1000` 秒，赋给 component 的 duration |
| `windows[].response: [keys]` | `keyboard.Keyboard(backend='ptb')` + `kb.getKeys(keyList=[keys], waitRelease=False)` + `win.callOnFlip(kb.clock.reset)` |
| `windows[].rt_onset` | `"self"` → `win.callOnFlip(kb.clock.reset)` 在 stimulus onset flip；跨窗口 → 在前序窗口 flip 时 reset |
| `windows[].audio` | `sound.Sound(file, preBuffer=-1)` 预加载 + `win.callOnFlip(sound.play)` 或 `sound.play(when=nextFlip)` |
| `blocks[]` | Block 循环 + `data.importConditions('{condition_file}')` |
| `blocks[].condition_file` | `data.TrialHandler(nReps=N, method='random', trialList=data.importConditions('conditions.xlsx'), seed=seed)` |
| `response_rules.correct` | `key_resp.keys == str(corr_ans) or key_resp.keys == corr_ans`；无反应时检查 `str(corr_ans).lower() == 'none'` |
| `response_rules.mapping` | `keyList=[key1, key2]` 传入 `getKeys()`，corrAns 来自条件文件 |
| `response_rules.deadline` | `core.CountdownTimer(DEADLINE / 1000)` 控制 `while timer.getTime() > 0` |
| `paradigm_config` | 范式特定逻辑 — SSD staircase 跟踪、n-back 序列生成、go-nogo 比例等 |
| `display` | `visual.Window(size=resolution, fullscr=True, color=bg_color, units='height')` |
| `font` | `FONT_CONFIG` toggle + OS auto-detect |
| `audio` | `sound.Sound()` + PTB backend + `preBuffer=-1` + `play(when=nextFlip)` |
| `participant_info` | `gui.DlgFromDict(dictionary=expInfo, title=expName)` → `expInfo['participant']`, `expInfo['date']` |
| `output` | `data.ExperimentHandler(dataFileName=filename)` + `exp.addLoop(trials)` + `trials.saveAsWideText()` + `exp.saveAsPickle()` |

## Windows[] → Trial 事件循环（三种窗口模式）

### 模式 1：单 Routine 合并（Same-Routine）

Stroop 实验使用 — 刺激和响应在同一个 `while continueRoutine` 循环内。两个 component 共享同一个 `routineTimer`，各自有 `t >= onset_time` 的启动条件。

```
┌──────────────────────────────────────────────┐
│               Routine "trial"                │
│  t=0 开始                                     │
│  t=0.5: word.status → STARTED (setAutoDraw)  │
│  t=0.5: resp.status → STARTED (clock reset)  │
│  waitOnFlip → 一帧后开始 getKeys              │
│  getKeys 检测到按键 → continueRoutine = False  │
│  (无按键则持续到所有 component FINISHED)        │
└──────────────────────────────────────────────┘
```

**代码模板** (modern frame loop + PTB keyboard):
```python
frameTolerance = 0.001
kb = keyboard.Keyboard(backend='ptb')
waitOnFlip = False

while continueRoutine:
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)

    # Word component STARTED at t=0
    if word.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        word.tStartRefresh = tThisFlipGlobal
        word.status = STARTED
        word.setAutoDraw(True)

    # Response component STARTED at t=0.5
    if resp.status == NOT_STARTED and tThisFlip >= 0.5 - frameTolerance:
        resp.status = STARTED
        waitOnFlip = True
        win.callOnFlip(kb.clock.reset)
        win.callOnFlip(kb.clearEvents, eventType='keyboard')

    if resp.status == STARTED and not waitOnFlip:
        theseKeys = kb.getKeys(keyList=['left', 'down', 'right'], waitRelease=False)
        if len(theseKeys):
            resp.keys = theseKeys[0].name
            resp.rt = theseKeys[0].rt
            continueRoutine = False

    win.flip()
    waitOnFlip = False
```

**适用**: Stroop、Flanker、Simon — 刺激和响应同时开始、响应即结束的范式。

### 模式 2：顺序 Routine（Sequential Routines）

Go/No-go 实验使用 — trial、feedback、rest 各自为独立的 Routine。`routineTimer.getTime() < 2.0` 控制最大时长。component 的 START/FINISH 状态由 `tThisFlipGlobal` 与 `tStartRefresh + duration` 的比较驱动。

```
Routine "trial" (max 2s)    →    Routine "feedback" (500ms)    →    Routine "rest" (ITI)
  image: STARTED (t=0)             fbtxt: STARTED (t=0)              (blank, 500ms)
  key_resp: STARTED (t=0)          fbtxt: FINISHED (t=0.5)
  → 按键 → continueRoutine=False
  → 无按键 → image/key_resp FINISHED at t=2.0
```

**代码模板** (modern frame loop):
```python
while continueRoutine and routineTimer.getTime() < 2.0:
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)

    if image.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        image.tStartRefresh = tThisFlipGlobal
        image.status = STARTED
        image.setAutoDraw(True)

    if image.status == STARTED:
        if tThisFlipGlobal > image.tStartRefresh + 2 - frameTolerance:
            image.status = FINISHED
            image.setAutoDraw(False)

    if key_resp.status == STARTED and not waitOnFlip:
        theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
        if len(theseKeys):
            key_resp.keys = theseKeys[0].name
            key_resp.rt = theseKeys[0].rt
            continueRoutine = False

    win.flip()
```

**适用**: Go/No-go、Dot-probe、N-back — 刺激→响应→反馈→ITI 分阶段呈现的范式。

### 模式 3：定时响应循环（Timed Response Loop）

Stop-signal 实验使用 — `CountdownTimer` 控制 deadline，循环内检查 SSD 触发和键盘。

```python
go_stim.draw()
win.callOnFlip(kb.clock.reset)
win.flip()
go_onset = core.getTime()

timer = core.CountdownTimer(DEADLINE / 1000)
while timer.getTime() > 0:
    elapsed = (core.getTime() - go_onset) * 1000

    if is_stop_trial and not stop_presented and elapsed >= ssd:
        present_stop_signal()
        stop_presented = True

    keys = kb.getKeys(keyList=go_keys + ['escape'], waitRelease=False, clear=False)
    if keys:
        if keys[0].name == 'escape':
            save_and_quit()
        response = keys[0].name
        rt = keys[0].rt
        break
```

**适用**: Stop-signal、任何需要在响应窗口内按经过时间触发事件的范式。

### 窗口模式选择判断

| 条件 | 模式 |
|------|------|
| 刺激+响应完全重叠，无中间事件 | 模式 1：单 Routine 合并 |
| 刺激→响应→反馈→ITI 为独立阶段 | 模式 2：顺序 Routine |
| 响应窗口内需要按时间触发事件（SSD、dynamic stimulus update） | 模式 3：定时响应循环 |

## 响应收集模式

### Old 模式（v3.1 Stroop）

```python
resp = keyboard.Keyboard()
# ...
win.callOnFlip(resp.clock.reset)
win.callOnFlip(resp.clearEvents, eventType='keyboard')
waitOnFlip = True

if resp.status == STARTED and not waitOnFlip:
    theseKeys = resp.getKeys(keyList=['left', 'down', 'right'], waitRelease=False)
    if len(theseKeys):
        resp.keys = theseKeys[0].name
        resp.rt = theseKeys[0].rt
```

### Modern 模式（v2023.2+ Go/No-go）

```python
key_resp = keyboard.Keyboard()
_key_resp_allKeys = []
# ...
win.callOnFlip(key_resp.clock.reset)
win.callOnFlip(key_resp.clearEvents, eventType='keyboard')
waitOnFlip = True

if key_resp.status == STARTED and not waitOnFlip:
    theseKeys = key_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
    _key_resp_allKeys.extend(theseKeys)
    if len(_key_resp_allKeys):
        key_resp.keys = _key_resp_allKeys[-1].name
        key_resp.rt = _key_resp_allKeys[-1].rt
        key_resp.duration = _key_resp_allKeys[-1].duration
        # accuracy check inside loop
        if (key_resp.keys == str(corr_ans)) or (key_resp.keys == corr_ans):
            key_resp.corr = 1
        else:
            key_resp.corr = 0
        continueRoutine = False
```

### Latest 模式（v2024.2+ 推荐）

```python
kb = keyboard.Keyboard(backend='ptb')  # 显式 PTB 后端
# ...
win.callOnFlip(kb.clock.reset)
win.callOnFlip(kb.clearEvents, eventType='keyboard')
waitOnFlip = True

if resp.status == STARTED and not waitOnFlip:
    theseKeys = kb.getKeys(keyList=ALLOWED_KEYS, waitRelease=False, clear=False)
    if len(theseKeys):
        resp.keys = theseKeys[0].name
        resp.rt = theseKeys[0].rt           # USB HID 异步时间戳，最高精度
        continueRoutine = False
```

**关键差异**: Latest 模式使用 `backend='ptb'` + `waitRelease=False` 获得最高 RT 精度。

### 双重 accuracy 判断

```python
# 循环内（响应时）
if (key_resp.keys == str(corr_ans)) or (key_resp.keys == corr_ans):
    key_resp.corr = 1
else:
    key_resp.corr = 0

# 循环外（无响应时）
if key_resp.keys in ['', [], None]:
    key_resp.keys = None
    if str(corr_ans).lower() == 'none':
        key_resp.corr = 1  # 正确不反应
    else:
        key_resp.corr = 0  # 漏反应
```

## RT 计时与 rt_onset

### 同窗口 RT（rt_onset: "self"）

```python
# 在 stimulus component 的 START 帧
win.callOnFlip(kb.clock.reset)  # t=0 at stimulus onset
win.callOnFlip(kb.clearEvents, eventType='keyboard')
```

`.rt` 自动是从 `clock.reset` 到按键时刻的 USB HID 时间戳。

### 跨窗口 RT（rt_onset: "fixation"）

```python
# 在 fixation routine 结束时 reset
win.callOnFlip(kb.clock.reset)  # 此时 stimulus 尚未出现
# stimOnset 另行记录
stimOnset = win.getFutureFlipTime()
# RT = key.rt，已自动从 clock.reset 开始计时
```

## 条件文件加载

### Old 模式：exec() 注入（❌ 禁止）

```python
trials = data.TrialHandler(nReps=5, method='random',
    trialList=data.importConditions('trialTypes.xls'))

for thisTrial in trials:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))
```

### Modern 模式：globals() 注入（✅ 推荐）

```python
trials = data.TrialHandler(nReps=1.0, method='random',
    trialList=data.importConditions('conditions.xlsx'),
    seed=42)

if thisTrial != None:
    for paramName in thisTrial:
        globals()[paramName] = thisTrial[paramName]
```

**推荐**: `globals()` 注入 — 兼容 exec-free 环境（Pavlovia online）且更安全。

## 帧循环演进

| 特性 | Old (v3.1) | Modern (v2023.2+) |
|------|-----------|-------------------|
| 帧时间源 | `t = trialClock.getTime()` | `tThisFlip = win.getFutureFlipTime(clock=routineTimer)` |
| 全局时间 | 无 | `tThisFlipGlobal = win.getFutureFlipTime(clock=None)` |
| 帧容差 | 硬编码 `t >= 0.5` | `frameTolerance = 0.001` |
| Component 停止 | 无独立停止逻辑 | `tThisFlipGlobal > comp.tStartRefresh + duration - frameTolerance` |
| Timer | `routineTimer = core.CountdownTimer()` | `routineTimer = core.Clock()` |
| 时长控制 | `routineTimer.add(2.0); while routineTimer.getTime() > 0` | `while routineTimer.getTime() < 2.0` |
| Timestamp | `win.timeOnFlip(comp, 'tStartRefresh')` | 同 + `thisExp.timestampOnFlip(win, 'comp.started')` |
| 键盘后端 | `keyboard.Keyboard()` (默认 event) | `keyboard.Keyboard(backend='ptb')` |

## 音频映射

| Config 场景 | PsychoPy 代码 |
|-------------|--------------|
| 简单音效播放 | `s = sound.Sound('beep.wav', preBuffer=-1); s.play()` |
| 精确同步（音频+视觉） | `s.play(when=win.getFutureFlipTime(clock='ptb'))` 或 `win.callOnFlip(s.play)` |
| 多音效预加载 | 字典: `sounds = {'go': sound.Sound('go.wav'), 'stop': sound.Sound('stop.wav')}` |
| 实验前播放 | `s.play()` — 阻塞式预放以避免首次播放延迟 |
| 音频+并口触发同步 | `win.callOnFlip(send_trigger, code); s.play(when=nextFlip); win.flip()` |

## 参与者信息映射

| Config 字段 | PsychoPy 代码 |
|-------------|--------------|
| `participant_id` | `expInfo = {'participant': '', 'session': '001'}` |
| 下拉选择（性别/利手等） | `'gender': ['male', 'female', 'other']`（list = dropdown） |
| 不可编辑字段 | `gui.DlgFromDict(..., fixed=['expVersion'])` |
| 取消退出 | `if not dlg.OK: core.quit()` |
| 日期戳 | `expInfo['date'] = data.getDateStr()` |

## 12 步模板 PsychoPy 实现

| 步骤 | 模板定义 | Latest PsychoPy 实现 |
|------|---------|---------------------|
| 1 | Imports | `from psychopy import visual, core, data, event, clock, gui, sound` + `from psychopy.hardware import keyboard` |
| 2 | Experiment params | `expName = '{name}'` + FONT_CONFIG + `gui.DlgFromDict()` + `expInfo['date'] = data.getDateStr()` |
| 3 | Display setup | `visual.Window(size=[1920,1080], fullscr=True, color=bg, units='height')` + `frameDur` 校准 |
| 4 | Stimulus preloading | `visual.ImageStim(win, image='default.png')` / `visual.TextBox2(win, text='')` / `sound.Sound(file, preBuffer=-1)` 全部在循环前初始化 |
| 5 | Condition loading | `data.importConditions('conditions.xlsx')` → `data.TrialHandler(nReps=N, method='random', seed=seed)` |
| 6 | Helper functions | `showExpInfoDlg()`, `setupData()`, `setupWindow()`, `setupInputs()`, `pauseExperiment()`, `quitExperiment()` |
| 7 | Instruction | `visual.TextBox2` + `keyboard.Keyboard(backend='ptb')` + `win.callOnFlip(kb.clock.reset)` |
| 8 | Practice | 独立 `TrialHandler` + 反馈 Routine + `force_correct_button_press` 逻辑 |
| 9a | Block setup | `exp.addLoop(trials)` + `for thisTrial in trials:` + `globals()[p] = thisTrial[p]` |
| 9b | Randomization | `TrialHandler(method='random', seed=N)` |
| 9c | Per-trial | Component 状态机 (NOT_STARTED→STARTED→FINISHED) + `win.callOnFlip(kb.clock.reset)` + `kb.getKeys(waitRelease=False)` |
| 9d | Block feedback | 独立 feedback Routine，读取 `key_resp.corr` 设置文本/颜色 |
| 10 | Data saving | `trials.addData('key_resp.keys', key_resp.keys)` + `thisExp.nextEntry()` + `exp.saveAsWideText()` + `exp.saveAsPickle()` |
| 11 | Cleanup | `win.close()` + `core.quit()` (escape handler 中); `try/finally` 包裹主实验 |
| 12 | Package | `.py` + README |

## 范式差异速查

| 范式 | 窗口模式 | 条件文件 | 特殊逻辑 |
|------|---------|---------|---------|
| Stroop (v3.1) | 模式1 单Routine合并 | trialTypes.xls | `exec()`注入, `setColor(letterColor)`动态颜色 |
| Go/No-go (v2023.2) | 模式2 顺序Routine | conditions.xlsx | `globals()`注入, 双重accuracy判断, 正确计数器 |
| Stop-signal | 模式3 定时响应循环 | 条件文件+SSD tracker | SSD staircase, `CountdownTimer`, stop signal中间事件 |
| Dot-probe (v2024.2) | 模式2 顺序Routine | conditions.xlsx | `TextBox2`文本对, `cue_y`位置映射, congruency在条件文件编码 |
| N-back | 模式2 顺序Routine | 程序化生成序列 | 环缓冲区, lure trials, n-back match detection, d-prime计算 |

## 反模式速查（Config→Code 生成特化）

> 通用 API 反模式见 [spec/README.md](../spec/README.md#10-anti-patterns)。

| 禁止的模式 | 原因 | 替代 |
|-----------|------|------|
| `imread` / `setImage` 在 trial 循环内 | 磁盘 I/O 导致帧丢失 — 条件文件的图片路径应预加载 | 循环前 `ImageStim(..., image='default.png')` 初始化, 循环内 `.setImage(filename)` |
| `trialClock.getTime()` (老式帧循环) | 不帧精确 — 应使用 Latest 模式帧循环 | `win.getFutureFlipTime(clock=routineTimer)` |
| `exec()` 条件注入 (v3.1 遗留) | Pavlovia 不兼容 — 条件变量应通过 `globals()` 注入 | `globals()[paramName] = thisTrial[paramName]` |
| `keyboard.Keyboard()` 无 `backend='ptb'` | 50-70ms RT 误差 — 生成响应收集代码时必须指定 PTB 后端 | `keyboard.Keyboard(backend='ptb')` |
| `kb.getKeys(waitRelease=True)` 用于 RT 任务 | 代码等释放才继续 — 响应窗口生成时应使用 `waitRelease=False` | `waitRelease=False` |
| 数据仅在实验结束时保存 | 崩溃=全丢 — output 映射必须生成 `try/finally` + per-trial flush | 每 trial flush + `try/finally` |
| `TextBox2` 用于需要 bounding box 的场景 | 无 `.boundingBox` — 需根据 stimulus 类型选择合适的组件 | 需要边界框时用 `TextStim` |
