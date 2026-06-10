# PsychoPy Implementation Guide

> **Parent**: [psy-exp-coder](../../SKILL.md)
> **Status**: reference — apply these rules to every generated PsychoPy experiment
> **Last updated**: 2026-05-27 — 基于 psychopy.org 官方文档全面修订

## Version Assumption

Default to **PsychoPy 2024.x+** (Python 3.10+). Use Builder-compatible API where possible. If the user's version differs, adapt.

## 1. Timing Rules

### 1.1 Frame-Accurate Timing Foundation

All timing must be frame-based, not wall-clock. Use these core APIs:

| API | Purpose | Notes |
|-----|---------|-------|
| `win.getFutureFlipTime(clock=None)` | Predicted time of next flip in **global** time | Use for component status checks: `tThisFlipGlobal > comp.tStartRefresh + duration - frameTolerance` |
| `win.getFutureFlipTime(clock=routineTimer)` | Predicted time of next flip in **routine-local** time | Reset `routineTimer` at routine start |
| `win.callOnFlip(callback, *args)` | Schedule callback at next screen refresh | Kernel of RT timing — `kb.clock.reset` must go here |
| `win.timeOnFlip(obj, 'attribute')` | Record flip time into object attribute | e.g. `win.timeOnFlip(comp, 'tStartRefresh')` |
| `frameTolerance = 0.001` | Frame comparison tolerance (1ms) | Prevents rounding errors from blocking state transitions |

```python
# Modern frame loop — mandatory pattern
routineTimer = core.Clock()
frameTolerance = 0.001

while continueRoutine and routineTimer.getTime() < maxDuration:
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)

    # Component STARTED: when tThisFlip >= onset time
    if comp.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        comp.tStartRefresh = tThisFlipGlobal
        comp.status = STARTED
        comp.setAutoDraw(True)

    # Component FINISHED: when on-screen time >= duration
    if comp.status == STARTED:
        if tThisFlipGlobal > comp.tStartRefresh + compDuration - frameTolerance:
            comp.status = FINISHED
            comp.setAutoDraw(False)

    win.flip()
```

### 1.2 Keyboard Backend Selection

`psychopy.hardware.keyboard.Keyboard` accepts a `backend` parameter — this choice significantly affects RT precision:

| Backend | Latency | Platform | Recommendation |
|---------|---------|----------|---------------|
| `'ptb'` (Psychtoolbox) | Sub-ms precision, USB HID level | All (64-bit Python) | **首选** — 生产级 RT 计时 |
| `'iohub'` | ~5ms lag, separate process | All | 需要 key release 事件时使用 |
| `'event'` | OS-level, highest latency | All (fallback) | 仅开发调试时使用 |

```python
from psychopy.hardware import keyboard

# Production-grade RT measurement
kb = keyboard.Keyboard(backend='ptb')
```

**关键**: 不指定 `backend='ptb'` 会导致 50-70ms 的 RT 误差（`key.rt` 与实际按键时间的差异）。

### 1.3 Correct RT Measurement

The keyboard clock must be reset **exactly at stimulus onset** (screen flip). Use `win.callOnFlip()` so the reset is synchronized to the refresh.

**Core pattern:**

```python
kb = keyboard.Keyboard(backend='ptb')
ALLOWED_KEYS = ['f', 'j']

# --- inside trial loop ---
stim.draw()
win.callOnFlip(kb.clock.reset)   # RT starts at true stimulus onset
win.callOnFlip(kb.clearEvents)   # clear any pre-flip keypresses
win.flip()

# Timed response loop
response = None
rt = None
timer = core.CountdownTimer(RESPONSE_DEADLINE)
while timer.getTime() > 0:
    keys = kb.getKeys(keyList=ALLOWED_KEYS + ['escape'], waitRelease=False, clear=False)
    if keys:
        key = keys[0]
        if key.name == 'escape':
            save_and_quit()
        response = key.name
        rt = key.rt  # seconds, from kb.clock.reset on the flip
        break

if rt is not None:
    rt *= 1000  # convert to ms
```

### 1.4 key.rt vs clock.getTime() — 关键区别

| 时间源 | 含义 | 精度 |
|--------|------|------|
| `key.rt` | 按键物理发生的**异步时间戳** — 从 `kb.clock.reset()` 到按键时刻 | **最高** — USB HID 级 |
| `kb.clock.getTime()` | 代码**执行到该行**的时间 | 低 — 可比实际按键晚一帧（~16.7ms） |

**永远用 `key.rt` 做 RT，永远不要手动 `clock.getTime()` 计算 RT。**

### 1.5 waitRelease 参数

| `waitRelease` | 行为 | 适用场景 |
|---------------|------|---------|
| `False`（推荐） | 按键按下立即返回，`.rt` 为按下时刻 | RT 任务 — 精度最高 |
| `True`（默认） | 等按键释放后才返回，`.duration` 可用 | 需要按键持续时间的场景 |

**RT 任务必须设置 `waitRelease=False`** — `True` 会导致 `.rt` 正确但代码执行延迟到释放后（额外 100-200ms 偏差）。

### 1.6 getKeys() vs waitKeys()

```python
# getKeys() — 非阻塞，必须在循环中轮询（推荐）
keys = kb.getKeys(keyList=['f', 'j'], waitRelease=False, clear=False)

# waitKeys() — 阻塞等待，不适合需要同时做帧循环的场景
keys = kb.waitKeys(maxWait=5.0, keyList=['f', 'j'])
```

**生成代码只使用 `getKeys()`** — `waitKeys()` 阻塞事件循环，等同于旧版 `event.waitKeys()`。

### 1.7 RT Onset Window Resolution

Check the `rt_onset` field on each response window:
- `rt_onset: self` → reset `kb.clock` at this window's own flip (merged pattern)
- `rt_onset: Target` → reset `kb.clock` at the window named "Target"'s flip (split pattern — RT excludes stimulus encoding time)
- Missing → **ask the user before generating code**. Do not guess.

### 1.8 core.wait() — 限用

`core.wait(duration)` blocks the event loop — Escape does not respond. Only use it for sub-frame delays (< 5ms trigger pulses). For any interactive interval, use a timed loop:

```python
# Instead of: core.wait(0.5)
timer = core.CountdownTimer(0.5)
while timer.getTime() > 0:
    if 'escape' in event.getKeys():
        save_and_quit()
    win.flip()
```

### 1.9 Canonical Code Skeleton（生成代码必须以此为模板）

以下是完整的、可运行的最小实验骨架。**所有生成的 PsychoPy 代码必须从这个骨架开始。**

```python
#!/usr/bin/env python3
# ============================================================
# Canonical PsychoPy Experiment Skeleton
# 展示所有强制 API 模式：PTB keyboard、帧精确 timing、key.rt、增量保存、try/finally
# 修改下方参数区即可适配不同范式
# ============================================================
import platform, os, csv, random
from psychopy import visual, core, data, event, gui
from psychopy.hardware import keyboard

# ============================================================
# 可修改参数 — 所有可调参数集中在此
# ============================================================
expName = 'canonical_skeleton'
subjectID = 'test'
sessionNum = 1

# 显示
fullscreen = True
screenSize = [1920, 1080]
bgColor = 'black'

# 时间参数 (秒)
fixationTime = 0.5
stimulusTime = 1.0
feedbackTime = 0.5
responseDeadline = 2.0
itiMin = 0.6
itiMax = 0.9

# 响应
ALLOWED_KEYS = ['f', 'j']
corrAnsMap = {'stim_a': 'f', 'stim_b': 'j'}

# 条件
conditions = [
    {'stim': 'stim_a', 'corr_ans': 'f'},
    {'stim': 'stim_b', 'corr_ans': 'j'},
]
nReps = 10

# ============================================================
# FONT_CONFIG — 中文文本的字体开关
# ============================================================
FONT_AUTO_DETECT = True
MANUAL_FONT_PATH = None

def get_cjk_font():
    if not FONT_AUTO_DETECT and MANUAL_FONT_PATH:
        if os.path.exists(MANUAL_FONT_PATH):
            return MANUAL_FONT_PATH
    _system = platform.system()
    if _system == 'Darwin':
        candidates = ['/System/Library/Fonts/PingFang.ttc', '/System/Library/Fonts/STHeiti Light.ttc']
    elif _system == 'Windows':
        candidates = ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']
    else:
        candidates = ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc']
    for f in candidates:
        if os.path.exists(f):
            return f
    return None

# ============================================================
# 3. 显示设置
# ============================================================
win = visual.Window(size=screenSize, fullscr=fullscreen, color=bgColor, units='height')
kb = keyboard.Keyboard(backend='ptb')  # 生产级 RT 精度

# ============================================================
# 4. 刺激预加载（循环外）
# ============================================================
fixation = visual.TextStim(win, text='+', color='white', height=0.05)
stimText = visual.TextStim(win, text='', color='white', height=0.08)
feedbackText = visual.TextStim(win, text='', color='white', height=0.05)

# ============================================================
# 5. 条件准备
# ============================================================
trialList = conditions * nReps
random.shuffle(trialList)

# ============================================================
# 6. 数据文件
# ============================================================
dataDir = 'data'
os.makedirs(dataDir, exist_ok=True)
dataFile = open(os.path.join(dataDir, f'sub-{subjectID}_{expName}_{data.getDateStr()}.csv'),
                'w', newline='')
writer = csv.DictWriter(dataFile, fieldnames=['trial', 'stim', 'corr_ans', 'rt', 'response', 'correct'])
writer.writeheader()

# ============================================================
# 7. 主实验循环
# ============================================================
try:
    for trialIdx, thisTrial in enumerate(trialList):
        stim = thisTrial['stim']
        corrAns = thisTrial['corr_ans']

        # === 注视点 ===
        fixation.draw()
        win.flip()
        core.wait(fixationTime - win.monitorFramePeriod * 0.5)

        # === 刺激 + 响应窗口 ===
        stimText.text = stim
        stimText.draw()
        win.callOnFlip(kb.clock.reset)     # RT 起点 = 刺激出现时刻
        win.callOnFlip(kb.clearEvents)
        win.flip()

        response = None
        rt = None
        timer = core.CountdownTimer(responseDeadline)
        while timer.getTime() > 0:
            keys = kb.getKeys(keyList=ALLOWED_KEYS + ['escape'], waitRelease=False, clear=False)
            if keys:
                key = keys[0]
                if key.name == 'escape':
                    dataFile.flush(); dataFile.close()
                    win.close(); core.quit()
                response = key.name
                rt = key.rt * 1000  # ms — USB HID 异步时间戳
                break
            # 持续重绘刺激
            stimText.draw()
            win.flip()

        # === 正确率判断 ===
        if response is None:
            correct = (corrAns.lower() == 'none')
            response = 'timeout'
        else:
            correct = (response == corrAns)

        # === 增量保存 ===
        writer.writerow({'trial': trialIdx+1, 'stim': stim, 'corr_ans': corrAns,
                         'rt': rt, 'response': response, 'correct': correct})
        dataFile.flush()

        # === ITI (随机) ===
        itiDur = random.uniform(itiMin, itiMax)
        itiTimer = core.CountdownTimer(itiDur)
        while itiTimer.getTime() > 0:
            if 'escape' in event.getKeys():
                dataFile.flush(); dataFile.close()
                win.close(); core.quit()
            win.flip()

    # 实验结束
    print(f'数据已保存至 data/')

finally:
    dataFile.flush()
    dataFile.close()
    win.close()
```

**使用方式**：复制此骨架 → 修改参数区 → 在刺激+响应窗口内替换为你的范式逻辑 → 添加指导语/练习/Block。不要改变 API 模式（PTB keyboard、`key.rt`、`callOnFlip`、`try/finally`）。

## 2. Stimulus Rules

### 2.1 Preloading

Preload all stimuli before the trial loop. Disk I/O during a trial causes frame drops:

```python
stimuli = {}
for cond in conditions:
    path = os.path.join('stimuli', cond['filename'])
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing: {path}")
    stimuli[cond['filename']] = visual.ImageStim(win, image=path)
```

- **ImageStim**: Create once per unique image, use `.setImage()` to swap
- **TextStim / TextBox2**: Create once, use `.setText()` / `.text =` to update
- **Sound**: Create `sound.Sound()` objects before the trial loop

### 2.2 TextBox2 vs TextStim

| 特性 | TextBox2（推荐） | TextStim（经典） |
|------|-----------------|-----------------|
| 更新速度 | 快 | 慢 |
| 非等宽字体 | ✅ | ✅ |
| 可编辑文本 | ✅ | ❌ |
| 行间距控制 | ✅ `lineSpacing` | ❌（需用 `\n\n` 替代） |
| 对齐方式 | ✅ `alignment` | ✅ `alignText` |
| 获取文本尺寸 | ❌ 无 `.boundingBox` | ✅ `.boundingBox` |
| 颜色/透明度 | ✅ | ⚠️ 动态 opacity 需设置 `_needSetText=True`（v2024.2.4 bug） |

**推荐**: 默认使用 `TextBox2`，需要获取文本边界框尺寸时用 `TextStim`。

### 2.3 Chinese Text Rendering

Always specify a CJK-capable font — the default font may not include CJK glyphs.

**Font toggle block** (generate this at the top of the parameters section in every script that uses Chinese text):

```python
import platform, os

# ============================================================
# FONT CONFIGURATION — edit this block if Chinese text displays as □□□
# ============================================================
FONT_AUTO_DETECT = True      # True = auto-detect by OS; False = use MANUAL_FONT_PATH
MANUAL_FONT_PATH = None      # Set to your font path, e.g. '/System/Library/Fonts/PingFang.ttc'
# ============================================================

def get_cjk_font():
    """Resolve CJK font path. Returns None if no valid font found."""
    if not FONT_AUTO_DETECT and MANUAL_FONT_PATH:
        if os.path.exists(MANUAL_FONT_PATH):
            return MANUAL_FONT_PATH
        else:
            print(f"WARNING: MANUAL_FONT_PATH not found: {MANUAL_FONT_PATH}")

    _system = platform.system()
    if _system == 'Darwin':
        _FONTS = ['/System/Library/Fonts/PingFang.ttc',
                   '/System/Library/Fonts/STHeiti Light.ttc']
    elif _system == 'Windows':
        _FONTS = ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']
    elif _system == 'Linux':
        _FONTS = ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                  '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc']
    else:
        _FONTS = []

    for f in _FONTS:
        if os.path.exists(f):
            return f

    print("WARNING: No CJK font found. Chinese text may display as □□□.")
    print("Set FONT_AUTO_DETECT=False and MANUAL_FONT_PATH to a valid .ttc/.ttf path.")
    return None

_CJK_FONT = get_cjk_font()

# Usage:
text_stim = visual.TextStim(win, text='你好', font=_CJK_FONT,
                            fontFiles=[_CJK_FONT] if _CJK_FONT else None,
                            height=40, color='white', languageStyle='LTR')
```

Key pitfalls:
- Builder's default `Arial` renders Chinese on most but NOT all systems
- `languageStyle='LTR'` prevents misdetecting Chinese as RTL
- Always test Chinese rendering on the exact machine that will run subjects
- The `FONT_AUTO_DETECT` / `MANUAL_FONT_PATH` switches sit at the top of the parameters section — users edit them directly without touching logic code

## 3. Audio / Sound API

### 3.1 Backend Selection

| Backend | Latency | Stability | Prescheduling | Platform |
|---------|---------|-----------|---------------|----------|
| **PTB** (`backend_ptb`) | Sub-ms | Excellent | ✅ `play(when=)` | All (64-bit Python) |
| **sounddevice** | ~20ms+ | Good | ❌ | All |
| **pyo** | Variable | Unstable (macOS crash) | ❌ | All |
| **pygame** | Poor | Stable | ❌ | All (fallback) |

**强制**: 所有需要精确音频计时的实验必须使用 PTB 后端。

### 3.2 Sound Preloading

```python
from psychopy import sound

# PTB backend — preBuffer=-1 loads entire file into memory
sound_stim = sound.Sound('stimuli/beep.wav', preBuffer=-1)

# Multiple sounds — preload all before trial loop
sounds = {
    'go': sound.Sound('stimuli/go.wav'),
    'stop': sound.Sound('stimuli/stop.wav'),
    'feedback_correct': sound.Sound('stimuli/correct.wav'),
}
```

### 3.3 Playback with Prescheduling

```python
# Sync audio with visual stimulus onset
stim.draw()
nextFlip = win.getFutureFlipTime(clock='ptb')  # PTB timebase
sound_stim.play(when=nextFlip)                 # sub-ms sync
win.flip()

# Or via callOnFlip
stim.draw()
win.callOnFlip(sound_stim.play)
win.flip()
```

### 3.4 Latency Class

```python
# PTB latency class (0-4), higher = lower latency, more resource usage
# Default: 3 (aggressive exclusive mode)
sound_stim = sound.Sound('stim.wav', latency_class=3)
```

| Class | Latency | Use Case |
|-------|---------|----------|
| 0 | ~300ms | Not timing-critical |
| 2 | Moderate | Shared with other apps |
| 3 | Low（默认） | Most experiments — exclusive mode |
| 4 | Critical | Errors if not fully dominant |

## 4. Response Collection

Edge cases to handle:
- **Anticipatory responses**: RT < 100ms — record but flag for analysis
- **Multiple keys**: `kb.getKeys()` returns all pressed keys — `keys[0]` is the first
- **No-go trials**: `response is None` on no-go = correct rejection (accuracy=1); on go = miss (accuracy=0)
- **Key release**: Only available with `waitRelease=True` — `.duration` attribute

## 5. Data Management

### 5.1 ExperimentHandler — 顶层容器

```python
from psychopy import data

exp = data.ExperimentHandler(
    name=expName,
    version='1.0',
    extraInfo={'participant': expInfo['participant'], 'session': expInfo['session']},
    runtimeInfo=None,
    dataFileName=f'data/sub-{expInfo["participant"]}_{expName}_{expInfo["date"]}',
    savePickle=True,
    saveWideText=True,
)
```

**关键规则**:
- `addLoop(handler)` **必须在循环运行前**调用 — 不能在实验开始时提前添加所有 loop
- `nextEntry()` 标记 trial 结束 — Builder 代码自动处理，自定义脚本需显式调用
- 实验崩溃时 `atexit` 回调会尝试保存已有数据
- 调用 `exp.abort()` 可阻止数据保存（用于调试运行）

### 5.2 TrialHandler — 条件循环

```python
trials = data.TrialHandler(
    trialList=data.importConditions('conditions.xlsx'),
    nReps=5,
    method='random',       # 'random' | 'sequential' | 'fullRandom'
    extraInfo={'phase': 'main'},
    seed=42,               # 可重现的随机化
    name='trials'
)

exp.addLoop(trials)  # 必须在循环前调用

for thisTrial in trials:
    # ... present trial ...
    trials.addData('rt', rt)
    # nextEntry 自动调用
```

**随机化方法**:
| Method | 行为 |
|--------|------|
| `'random'` | 每个 repeat 内 shuffle，所有条件出现一次 |
| `'sequential'` | 按列表顺序呈现 |
| `'fullRandom'` | 跨 repeat 完全随机（可能连续多次同一条件） |

### 5.3 Column Priorities

添加数据时可设置优先级控制输出列顺序:

```python
from psychopy.constants import priority

exp.addData('rt', rt, priority=priority.HIGH)     # 排在前面
exp.addData('debug_var', val, priority=priority.EXCLUDE)  # 排在末尾
```

| Priority | Value | Usage |
|----------|-------|-------|
| CRITICAL | 30 | Routine start times（保留） |
| HIGH | 20 | RT, accuracy — 分析核心变量 |
| MEDIUM | 10 | 条件信息 |
| LOW | 0 | 辅助信息 |
| EXCLUDE | -10 | 调试变量，不用于分析 |

### 5.4 Data Output Formats

| Format | Method | Notes |
|--------|--------|-------|
| CSV/TSV (wide) | `exp.saveAsWideText('data.csv', delim=',')` | 每 trial 一行，"wide" 指所有变量存为列 |
| Pickle | `exp.saveAsPickle('data.psydat')` | 完整对象，可后续 Python 加载分析 |

### 5.5 Incremental Save (try/finally)

```python
data_file = open(f'data/sub-{sub_id}_{task}_{date}.csv', 'w', newline='')
writer = csv.DictWriter(data_file, fieldnames=columns)
writer.writeheader()

try:
    run_experiment()
finally:
    data_file.flush()
    data_file.close()
    win.close()
```

- Per trial: `writer.writerow()` + `data_file.flush()`
- Filename convention: `data/sub-{subject_id}_{task_name}_{date}.csv`

## 6. Participant Info Dialog

```python
from psychopy import gui

expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)

if not dlg.OK:
    core.quit()  # user pressed cancel

expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
```

**高级用法**:
```python
# 下拉菜单 — value 为 list
expInfo = {
    'participant': '',
    'gender': ['male', 'female', 'other'],  # list = dropdown
    'age': '',
    'handedness': ['right', 'left'],
}

# fixed 参数 — 不可编辑字段
dlg = gui.DlgFromDict(
    dictionary=expInfo,
    title=expName,
    fixed=['expVersion'],   # 显示但不可编辑
    order=['participant', 'age', 'gender'],
    tip={'participant': 'Unique subject ID'}
)
```

## 7. Hardware Integration

### 7.1 EEG / Parallel Port Triggers

Send triggers via `callOnFlip` — **not before** `flip()`:

```python
from psychopy import parallel

port = parallel.ParallelPort(address=0x378)

def send_trigger(code):
    port.setData(code)
    core.wait(0.005)     # hold 5ms pulse
    port.setData(0)

# CORRECT: trigger synchronized to stimulus onset
stim.draw()
win.callOnFlip(send_trigger, trigger_code)
win.flip()

# BAD: trigger sent before flip — early by ~16.7ms
port.setData(trigger_code)
win.flip()
```

### 7.2 Audio-Visual Sync with Triggers

```python
# Sync sound + visual + parallel port trigger
stim.draw()
nextFlip = win.getFutureFlipTime(clock='ptb')
win.callOnFlip(send_trigger, trigger_code)
sound_stim.play(when=nextFlip)  # audio at same time as new frame
win.flip()
```

**注意**: Windows 上音频+trigger 仍有 ±10-15ms jitter 的已知问题（PsychoPy 2024.2.4）。

## 8. Emergency Quit

```python
def check_quit(data_file, win):
    if 'escape' in event.getKeys():
        data_file.flush()
        data_file.close()
        win.close()
        core.quit()
```

Escape is checked inside the timed response loop AND between trials/ITIs. In the response loop, `'escape'` must be in the `keyList` passed to `kb.getKeys()`.

## 9. Debrief / Results Feedback Stage

```python
# At end of experiment, after trial loop:
debrief_text = f"""
实验结果:
你的平均反应时: {np.mean(rts):.0f} ms
正确率: {np.mean(corrects)*100:.1f}%
感谢你的参与!
"""
debrief_stim = visual.TextStim(win, text=debrief_text, color='black')
debrief_stim.draw()
win.flip()
# Wait for any key press
kb = keyboard.Keyboard()
kb.waitKeys()  # 这里阻塞等待是 OK 的（实验已结束）
```

## 10. Anti-Patterns

| Anti-pattern | Why it's wrong | Correct approach |
|--------------|---------------|-----------------|
| `event.getKeys(keyList=..., maxWait=...)` | Blocks event loop, Escape unresponsive | `keyboard.Keyboard(backend='ptb')` in `CountdownTimer` loop |
| `event.waitKeys(keyList=..., maxWait=...)` | Same blocking issue | `kb.getKeys()` in loop with `CountdownTimer` |
| `kb.waitKeys(maxWait=...)` in trial | Blocks event loop — identical to `event.waitKeys` | `kb.getKeys()` in non-blocking loop |
| `time.sleep(0.5)` | Blocks event loop | `CountdownTimer` loop or flip-based timing |
| `core.wait(duration)` for >5ms | Blocks event loop | Timed loop with escape check |
| Loading images inside trial loop | Frame drops from disk I/O | Preload at startup, `.setImage()` per trial |
| `ImageStim` per trial without preloading | Re-allocation causes jitter | Create once, `.setImage()` per trial |
| RT measured with `time.time()` or `clock.getTime()` | Not sync'd to screen refresh, ignores USB HID timestamp | `key.rt` (async USB HID timestamp) |
| `kb.clock.getTime()` for RT | Returns code-execution time, not key-press time | `key.rt` |
| `kb.getKeys(waitRelease=True)` for RT tasks | Code waits for release — adds 100-200ms to loop | `waitRelease=False` |
| Data saved only at end | Crash = zero data | Save + flush per trial, `try/finally` |
| No escape key handler | Can't quit if something goes wrong | Escape in timed loop + between-trial check |
| Default font for Chinese text | □□□ tofu characters | Explicit CJK font path via FONT_CONFIG |
| EEG trigger before `win.flip()` | Trigger ~16.7ms early | `win.callOnFlip(port.setData, code)` |
| `exec()` condition injection | Pavlovia incompatible, security risk | `globals()[paramName] = thisTrial[paramName]` |
| Sound without `preBuffer=-1` | Streaming latency | PTB backend + `preBuffer=-1` |
| Adding loops to ExperimentHandler at start | Loop tracking breaks | `exp.addLoop()` right before loop runs |
| `keyboard.Keyboard()` without `backend='ptb'` | 50-70ms RT error | `keyboard.Keyboard(backend='ptb')` |
| `sound.Sound()` without explicit backend | May fall back to high-latency pygame | Use PTB backend on 64-bit Python |

## 11. Environment Safety (Anti-Cheating)

```python
# Disable text selection and right-click (if using PsychoPy in windowed mode)
# For PsychoPy fullscreen, these are typically not needed

# Block specific keys that could interrupt the experiment
from psychopy.hardware import keyboard
disallowed_keys = ['escape', 'f5', 'f12']
```

## 12. Cross-platform Notes

- **macOS**: `PingFang.ttc`. PsychoPy via standalone `.dmg` or `pip`. PTB 3.0.20+ native ARM; 3.0.19 via Rosetta.
- **Windows**: `pyglet` 1.4.x preferred. Fonts: `msyh.ttc` / `simhei.ttf`. Button boxes may need Zadig. PsychHID slightly better than ioHub.
- **Linux**: Fonts: Noto CJK. `sound.backend_ptb` for low-latency audio. May need `libusb`. PsychHID significantly better than ioHub on macOS.

## 13. API Reference Index

| 需要实现的功能 | API / 类 | 关键参数 |
|---------------|---------|---------|
| 创建窗口 | `visual.Window()` | `size`, `fullscr`, `color`, `units`, `screen` |
| 帧计时 | `win.getFutureFlipTime(clock=None/routineTimer)` | `clock` 参数决定时间基准 |
| 帧同步回调 | `win.callOnFlip(callback, *args)` | callback + 参数 |
| 记录 flip 时间 | `win.timeOnFlip(obj, 'attr')` | 对象 + 属性名 |
| RT 计时键盘 | `keyboard.Keyboard(backend='ptb')` | `backend` 选择精度 |
| 获取按键 | `kb.getKeys(keyList, waitRelease=False, clear=False)` | 非阻塞轮询 |
| 清除按键 | `kb.clearEvents(eventType='keyboard')` | flip 前清除 |
| RT 时间戳 | `key.rt`（`KeyPress` 对象属性） | 从 `kb.clock.reset()` 算起 |
| 按键名 | `key.name` | 字符串，如 `'f'`, `'left'` |
| 按键时长 | `key.duration` | 需要 `waitRelease=True` |
| 倒计时 | `core.CountdownTimer(seconds)` | 响应截止时间 |
| 文本显示（推荐） | `visual.TextBox2()` | `text`, `font`, `letterHeight`, `color`, `alignment` |
| 文本显示（经典） | `visual.TextStim()` | `text`, `font`, `height`, `color` |
| 图片显示 | `visual.ImageStim()` | `image`, `pos`, `size` |
| 音频播放 | `sound.Sound()` | `preBuffer=-1`, PTB `play(when=)` |
| 条件循环 | `data.TrialHandler()` | `trialList`, `nReps`, `method`, `seed` |
| 条件导入 | `data.importConditions('file.xlsx')` | 返回条件 dict list |
| 数据容器 | `data.ExperimentHandler()` | `name`, `extraInfo`, `dataFileName` |
| 添加循环数据 | `exp.addLoop(trials)` | 循环前调用 |
| 添加 trial 数据 | `trials.addData(name, value)` | 自动转发至 ExperimentHandler |
| 标记 trial 结束 | `exp.nextEntry()` | 自定义代码需显式调用 |
| 保存为 CSV | `exp.saveAsWideText('file.csv', delim=',')` | 实验结束时调用 |
| 保存为 Pickle | `exp.saveAsPickle('file.psydat')` | 完整对象 |
| 参与者对话框 | `gui.DlgFromDict(dictionary=expInfo, title=expName)` | 下拉菜单用 list 值 |
| 日期字符串 | `data.getDateStr()` | 格式 `YYYY_Mon_DD_HHMM` |
| EEG 并口触发 | `parallel.ParallelPort(address=0x378)` | `callOnFlip(port.setData, code)` |
| 安全退出 | `core.quit()` | Escape 处理中调用 |
