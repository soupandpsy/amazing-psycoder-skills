# PsychoPy Implementation Guide

> **Parent**: [psy-exp-coder](../../SKILL.md)
> **Status**: reference — apply these rules to every generated PsychoPy experiment
> **Last updated**: 2026-07-25 — 17-rule quality template applied

## Critical Rules (Read First — errors here invalidate data)

| Rule | Why Critical |
|------|-------------|
| **RT from `key.rt`, never `clock.getTime()`** | Wrong RT source = all reaction-time data invalid |
| **`nextEntry()` after every trial** | Missing = crash loses all data. `try/finally` alone is not enough |
| **`callOnFlip(kb.clock.reset)` at stimulus onset** | Missing = RT measures from wrong origin |
| **Escape in every timed loop** | Missing = user trapped in fullscreen, must force-quit |
| **Preload stimuli outside trial loop** | `ImageStim()` inside loop = frame drops, timing jitter |
| **`event.getKeys(maxWait=...)` forbidden** | Blocks event loop, escape unresponsive |

Full anti-patterns table: [§11](#11-anti-patterns). Full 17-rule template: [§0](#0-code-structure-requirements-17-rule-quality-template).

## Version Assumption

Do not silently default a PsychoPy/Python version. Generate against the exact `runtime.framework_version` and pinned dependency strategy in config, verify every used API against that version, and record the target OS/device profile. Builder-export compatibility is required only when the user/config requests it.

## 0. Code Structure Requirements (17-Rule Quality Template)

Every generated PsychoPy experiment must follow these rules. Order matters — sections must appear in the sequence listed below.

### 0.1 File-Level Structure (Rules 1–2)

```python
# {filename}.py
# ---------------------------------------------------------------
# 一体化流程：
#   {stage_1} → {stage_2} → {stage_3}
#
# 数据输出：
#   {stage} -> <prefix>_{stage}.csv / <prefix>_{stage}.psydat
#
# 设计概要：
#   每个 block：{trial_count} trial
#   正式阶段：{block_count} block × {trials_per_block} = {total} trial
#
# 当前版本关键修改：
#   1) {change_1}
#   2) {change_2}
# ---------------------------------------------------------------
```

**Rule**: 文件第一行 = 文件名。一体化流程用 `→` 箭头表示阶段顺序。每个阶段的数据输出格式明确写出。关键修改用编号列表。

### 0.2 Section Order (Rules 1, 3, 5, 11)

```
一、基本配置区（路径 / 屏幕 / 字体 / 退出键）                              ← Rule 3: 配置在前 1/3
二、文本常量区（所有指导语 / 反馈 / 提示文字集中定义）                      ← Rule 5
三、条件表 / 时序 / 约束配置区（数据表名 / 路径 / 约束常量）               ← Rule 6
四、被试信息区（gui.DlgFromDict）
五、窗口 + 通用对象区（win / kb / TextStim 池 / show_text 函数）
六、数据处理器配置区（ExperimentHandler 按阶段独立）                       ← Rule 11
七、工具函数区（路径合成 / 条件加载 / 安全等待 / 伪随机 / 退出安全网）     ← Rule 7
八、单次 trial 函数（呈现→ 收集→ 反馈→ ITI→ 写数据）                      ← Rule 12
九、主流程（try → 各阶段顺序执行 → except → finally 清理）                 ← Rule 8
```

**Rule**: 每段以 `# ============================================================` 开始，段内子配置以 `# ----------` 分隔。不允许打乱段顺序。

### 0.3 Variable Naming (Rule 4)

```
<STAGE_PREFIX>_<CATEGORY>_<MEANING>

STAGE_PREFIX = KP | NV | PRAC | MAIN | (按实验阶段自定义)
CATEGORY     = TXT (指导语文本) | KEY (按键) | MS (毫秒时序)
             | DIR (文件夹路径) | FB (反馈) | EXCEL (条件表文件名)
             | MAX_CONSEC (伪随机约束) | N_ (计数)

正例: KP_ITI_MS, NV_FEED_TIMEOUT, NV_MAX_CONSEC_ELLIPSE
反例: iti, feedback_timeout, max_ellipse  (无阶段前缀, 无分类信息)
```

### 0.4 Pseudorandom Constraints (Rule 6)

```python
# ---------- 伪随机约束 ----------
NV_MAX_CONSEC_ELLIPSE     = 2       # 每个约束一个常量, 可独立调整
NV_MAX_CONSEC_PRIME_WIDTH = 3
NV_MAX_CONSEC_CORRECT_KEY = 3
NV_MAX_PSEUDORAND_TRIES   = 5000   # 硬性上限, 防止死循环

def can_append_trial(current_seq, candidate):
    """检查 candidate 加在 current_seq 末尾是否违反任何约束"""
    # ... 逐约束检查 ...

def pseudorandomize(raw_trials, max_tries=NV_MAX_PSEUDORAND_TRIES):
    """在 max_tries 次内找到合法序列, 失败 = 退出, 不降级"""
    for _ in range(max_tries):
        # ... shuffle + constraint check ...
        if len(seq) == len(raw_trials):
            return seq
    exit_without_saving()  # 失败必须退出
```

**Rule**: 约束尝试失败必须退出。不允许降级为简单随机。不允许返回可能违反约束的序列。

### 0.5 Exit Safety (Rule 7)

```python
aborted_by_user = False

def cleanup_outputs():
    """删除中途退出的不完整数据文件"""
    for prefix in [filename_prefix_kp, filename_prefix_navon]:
        for path in glob.glob(prefix + ".*"):
            try:
                os.remove(path)
            except:
                pass

def exit_without_saving():
    """Escape / 异常 / 条件校验失败时调用"""
    global aborted_by_user
    aborted_by_user = True
    cleanup_outputs()
    try:
        win.close()
    except:
        pass
    core.quit()
```

**Rule**: `exit_without_saving()` 必须在以下位置调用：用户按 Escape、文件缺失、条件校验失败、伪随机失败。

### 0.6 Condition Validation (Rule 9)

```python
# 先定义合法值集合, 再逐行校验
NV_VALID_PRIME_NAMES  = ["narrow", "broad"]
NV_VALID_SHAPES       = ["circle", "ellipse"]

# 逐行校验 — 报告具体第几行什么字段非法
prime_errors = []
for i, r in enumerate(nv_prime_rows, start=1):
    if r["prime"].lower() not in NV_VALID_PRIME_NAMES:
        prime_errors.append(f"prime 表第 {i} 行 prime 非法：{r['prime']}")

if prime_errors:
    show_text("Error:\n" + "\n".join(prime_errors[:20]), True)
    exit_without_saving()

# 素材文件预检查
missing = [f for f in sorted(needed_files) if not os.path.isfile(f)]
if missing:
    show_text(f"Error: 以下素材缺失：\n\n" + "\n".join(missing[:20]), True)
    exit_without_saving()
```

**Rule**: 校验必须覆盖: 列存在性、行数非零、列值在合法集合内、素材文件在磁盘上存在、关键条件数量达标。错误信息截断 (`[:20]`) 防止刷屏。

### 0.7 Trial Function Contract (Rule 12)

```python
def {stage}_run_one_trial(
    row: dict,              # 条件表的一行 — 总是第一个参数, 总是命名为 row
    trial_index: int,       # block 内 trial 序号 (1-based)
    block_index: int,       # block 序号
    phase: str,             # "practice" | "main" — 控制反馈逻辑
    # ... 其他行为开关作为布尔参数
):
    """单次 trial: 呈现→ 收集→ 反馈→ ITI→ 写数据"""

    # ① 刺激呈现（含随机参数如 prime_duration_ms）
    # ② 反应收集（while 循环 + rt_clock + timeout 检查）
    # ③ 反馈呈现（根据 phase 分支：practice 全部反馈 / formal 仅超时）
    # ④ ITI（安全等待）
    # ⑤ 数据写出（全部字段一次性 addData + nextEntry）
```

**Rule**: trial 函数内部不允许出现裸数字 — 全部引用配置常量。RT 必须用 `int(key.rt * 1000)`。所有布尔值保存为 `0/1` int。运行时动态值（随机 duration、实际 ITI、onset timestamp）必须写入数据。

### 0.8 Per-Trial Data Write (Rules 10, 14–16)

```python
# ⑤ 数据写出 — 全部字段显式, 一次性完成
for kk in SUBJECT_COLS:
    thisExp.addData(kk, info.get(kk, ""))
thisExp.addData("phase", phase)
thisExp.addData("block_index", block_index)
thisExp.addData("trial_index", trial_index)
thisExp.addData("resp_key", resp_key)
thisExp.addData("rt_ms", rt_ms)                            # Rule 14: 整数 ms, 来自 key.rt 而非 clock.getTime()
thisExp.addData("correct", int(correct))                   # Rule 15: 0/1 int
thisExp.addData("timeout", int(timeout))
thisExp.addData("prime_duration_ms", prime_duration_ms)    # Rule 16: 运行时值
thisExp.addData("iti_ms_actual", iti_ms_actual)            # Rule 16: 运行时值
thisExp.nextEntry()                                         # Rule 10: 立即写盘
```

### 0.9 Main Flow (Rule 8)

```python
try:
    # 所有实验阶段按顺序调用
    stage_1_run_and_save()
    stage_2_run_and_save()
    # ...

except SystemExit:
    exit_without_saving()

except Exception as e:
    exit_without_saving()

finally:
    try:
        thisExpKP.abort()
    except:
        pass
    try:
        thisExpNV.abort()
    except:
        pass
    try:
        win.close()
    except:
        pass
    core.quit()
```

**Rule**: 三个 except 分支缺一不可。finally 中每个清理操作独立 try-except。每个阶段结束后必须立即 `saveAsWideText` + `saveAsPickle`，不等实验结束。

### 0.10 Comment Rules (Rule 17)

```python
# 正例 — 解释意图
rt_clock = core.Clock()
# 已删除 fixation, 仅保留 ITI                           ← 解释设计决策
prime_duration_ms = random.randint(400, 600)             ← 不写 "# 生成随机数"（废话）
NV_PRIME_MIN_MS = 400                                    ← 配置值自带注释

# 反例 — 不做
rt_clock = core.Clock()  # 创建时钟对象                   ← 代码已自明
win = visual.Window(...) # 创建 PsychoPy 窗口              ← 废话
```

**Rule**: 禁止 `# 创建 X 对象`、`# 设置 Y 为 Z`。允许且鼓励: 解释为什么删除、为什么选这个值、非标准处理的理由。

## 1. Timing Rules

### 1.1 Frame-Accurate Timing Foundation

Visual onset/duration must be referenced to actual/predicted flips, and response timing must use the selected device backend's event timestamps. Wall-clock calls may record metadata, but must not substitute for flip- or device-referenced measurements. These are the core visual-timing APIs:

| API | Purpose | Notes |
|-----|---------|-------|
| `win.getFutureFlipTime(clock=None)` | Predicted time of next flip in **global** time | Use for component status checks: `tThisFlipGlobal > comp.tStartRefresh + duration - frameTolerance` |
| `win.getFutureFlipTime(clock=routineTimer)` | Predicted time of next flip in **routine-local** time | Reset `routineTimer` at routine start |
| `win.callOnFlip(callback, *args)` | Schedule callback at next screen refresh | Kernel of RT timing — `kb.clock.reset` must go here |
| `win.timeOnFlip(obj, 'attribute')` | Record flip time into object attribute | e.g. `win.timeOnFlip(comp, 'tStartRefresh')` |
| `frameTolerance = 0.001` | Frame comparison tolerance (1ms) | Prevents rounding errors from blocking state transitions |

```python
# Supported duration-managed visual frame-loop pattern
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

`psychopy.hardware.keyboard.Keyboard` accepts a `backend` parameter. Backend availability and timing behavior depend on PsychoPy version, OS, device, and driver, so choose deliberately and verify on the target machine:

| Backend | Characteristics | Recommendation |
|---------|-----------------|----------------|
| `'ptb'` (Psychtoolbox) | Asynchronous keyboard timestamps when supported | Preferred candidate for time-critical RT tasks; verify availability and timing |
| `'iohub'` | Separate-process device handling and release-event support | Use when its device/event features are required; verify timing |
| `'event'` | Legacy/fallback event path | Use only with a documented justification and target-machine validation for timing-critical tasks |

```python
from psychopy.hardware import keyboard

# Candidate configuration for a timing-critical RT task
kb = keyboard.Keyboard(backend='ptb')
```

**关键**: 不要把后端名称本身当作精度证明。记录 PsychoPy/PTB/OS/设备版本，并用目标硬件的 smoke test 或外部测量验证设计所需的时序精度。

### 1.3 Correct RT Measurement

Reset the keyboard clock on the flip used as the software onset reference. `win.callOnFlip()` aligns the clock reset with that flip callback; physical display onset still depends on the display pipeline and requires target-hardware measurement when scientifically material.

**Core pattern:**

```python
kb = keyboard.Keyboard(backend='ptb')
ALLOWED_KEYS = ['f', 'j']

# --- inside trial loop ---
stim.draw()
win.callOnFlip(kb.clock.reset)   # RT starts at the recorded flip-referenced onset
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
| `key.rt` | 所选 keyboard backend 报告的 key-down 事件时间，相对 `kb.clock.reset()` | 通常优于轮询代码时间；端到端误差取决于设备/backend/OS，需实测 |
| `kb.clock.getTime()` | 代码**执行到该行**的时间 | 受轮询与代码路径延迟影响，不能替代设备事件时间戳 |

**永远用 `key.rt` 做 RT，永远不要手动 `clock.getTime()` 计算 RT。**

### 1.5 waitRelease 参数

| `waitRelease` | 行为 | 适用场景 |
|---------------|------|---------|
| `False` | 返回 key-down 事件，`.rt` 对应按下时刻 | 当 protocol 的 scored event 是 key-down 时使用 |
| `True`（默认） | 等按键释放后才返回，`.duration` 可用 | 需要按键持续时间的场景 |

**按键按下作为响应的 RT 任务应设置 `waitRelease=False`**。`True` 只返回已经释放的按键，可能推迟程序获得事件；只有研究按键持续时间/释放时刻时才使用，并明确相应 estimand。

### 1.6 getKeys() vs waitKeys()

```python
# getKeys() — 非阻塞，必须在循环中轮询（推荐）
keys = kb.getKeys(keyList=['f', 'j'], waitRelease=False, clear=False)

# waitKeys() — 阻塞等待，不适合需要同时做帧循环的场景
keys = kb.waitKeys(maxWait=5.0, keyList=['f', 'j'])
```

在需要持续刷新、并行触发、动画、超时状态或持续 Escape/窗口事件处理的 trial 中使用非阻塞 `getKeys()` 循环。静态、单一响应的非关键屏幕可使用 `waitKeys()`，但必须包含退出键并保证清理路径；不要把阻塞本身误报成固定的 RT 偏差。

### 1.7 RT Onset Window Resolution

Check the `rt_onset` field on each response window:
- `rt_onset: self` → reset `kb.clock` at this window's own flip (merged pattern)
- `rt_onset: Target` → reset `kb.clock` at the actual flip of the window named "Target". Interpret what that interval includes from the confirmed timeline; do not attach a generic cognitive-process label.
- Missing → **ask the user before generating code**. Do not guess.

### 1.8 core.wait() — 限用

`core.wait(duration)` blocks concurrent event handling. Do not use it for an interactive interval. A hardware protocol may require a measured blocking pulse, but that duration must come from the device contract and the design must preserve cleanup; otherwise use a timed loop:

```python
# Instead of: core.wait(0.5)
timer = core.CountdownTimer(0.5)
while timer.getTime() > 0:
    if any(key.name == 'escape' for key in kb.getKeys(keyList=['escape'], waitRelease=False)):
        save_and_quit()
    win.flip()
```

### 1.9 Canonical Code Skeleton（新项目的契约基线）

以下骨架展示新项目必须保留的安全、计时、数据和清理契约。按 config 选择实际组件/设备/API；有依据的结构偏离必须记录并测试，`modify`/`debug` 不重写无关架构。

```python
#!/usr/bin/env python3
# {filename}.py
# ---------------------------------------------------------------
# 一体化流程：
#   {stage_1} → {stage_2} → {stage_3}
#
# 数据输出：
#   {stage} -> <prefix>_{stage}.csv / <prefix>_{stage}.psydat
#
# 设计概要：
#   每个 block：{n} trial
#   正式阶段：{m} block × {t} = {total} trial
#
# 当前版本关键修改：
#   1) {change_1}
#   2) {change_2}
# ---------------------------------------------------------------

import platform, os, csv, random, hashlib, glob
from datetime import datetime, timezone
from psychopy import visual, core, data, gui, event
from psychopy.hardware import keyboard

# ============================================================
# 一、基本配置（通用）
# ============================================================
EXP_NAME = "{experiment_name}"

if "__file__" in globals():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
else:
    BASE_DIR = os.getcwd()

SAVE_DIR = os.path.join(BASE_DIR, "data")
try:
    os.makedirs(SAVE_DIR, exist_ok=True)
except OSError:
    # 权限不足 / 磁盘满 / 只读文件系统 — 直接退出，不等实验开始后才发现
    print(f"无法创建数据文件夹: {SAVE_DIR}")
    print("请检查磁盘空间和写入权限后重试。")
    core.quit()

# ---------- 屏幕 ----------
WIN_SIZE  = [1920, 1080]
FULLSCR   = True
BG_COLOR  = [0, 0, 0]        # black
WIN_UNITS = "height"

# ---------- 字体 ----------
# 显式记录主字体和目标机验证过的回退；启动检查应在正式采集前验证字形覆盖。
FONT_CONFIG        = {"primary": "PingFang SC", "fallback": "Noto Sans CJK SC"}
TEXT_FONT          = FONT_CONFIG["primary"]
FONT_SIZE          = 0.05
FEEDBACK_FONT_SIZE = 0.07
TEXT_WRAP_WIDTH    = 2.5
TXT_COLOR          = "white"

# ---------- 退出键 ----------
KEY_QUIT = "escape"

# ============================================================
# 二、文本常量区（所有指导语 / 反馈文字集中在此）
# ============================================================
TXT_START = (
    "欢迎参加实验。\n\n"
    "按任意键开始。"
)

TXT_END = (
    "实验结束，感谢参与！\n\n"
    "按任意键退出。"
)

# ============================================================
# 三、条件表 / 时序 / 约束配置
# ============================================================
CONDITION_XLSX = "conditions.xlsx"

# ---------- 时序 (秒) ----------
FIXATION_S    = 0.5
STIMULUS_S    = 1.0
FEEDBACK_S    = 0.5
RESP_MAX_S    = 2.0
ITI_MIN_S     = 0.6
ITI_MAX_S     = 0.9

# ---------- 按键 ----------
ALLOWED_KEYS = ["f", "j"]

# ---------- 伪随机约束 ----------
MAX_CONSEC_SAME_CONDITION = 3
MAX_PSEUDORAND_TRIES      = 5000

# ============================================================
# 四、被试信息
# ============================================================
fields_order = ["Participant ID", "Age", "Gender", "Handedness"]

while True:
    info = {
        "Participant ID": "",
        "Age": "",
        "Gender": ["Male", "Female"],
        "Handedness": ["Right", "Left"]
    }
    dlg = gui.DlgFromDict(info, title=EXP_NAME, order=fields_order, sortKeys=False)
    if not dlg.OK:
        core.quit()
    if info["Participant ID"].strip() != "":
        break

filename_prefix = os.path.join(
    SAVE_DIR, f"{info['Participant ID']}_{data.getDateStr()}"
)
RANDOM_SEED = int.from_bytes(
    hashlib.sha256(f"{EXP_NAME}|{info['Participant ID']}".encode("utf-8")).digest()[:8],
    "big",
)
rng = random.Random(RANDOM_SEED)

SUBJECT_COLS = ["Participant ID", "Age", "Gender", "Handedness"]
BASE_DATA_COLUMNS = [
    "subject_id", "block", "trial", "condition", "stimulus",
    "correct_response", "response", "rt", "accuracy", "timestamp",
]

# ============================================================
# 五、窗口与通用对象
# ============================================================
win = visual.Window(size=WIN_SIZE, fullscr=FULLSCR, color=BG_COLOR, units=WIN_UNITS)
kb  = keyboard.Keyboard(backend="ptb")
event.Mouse(visible=False, win=win)

msg = visual.TextStim(
    win, text="", color=TXT_COLOR, height=FONT_SIZE,
    wrapWidth=TEXT_WRAP_WIDTH, font=TEXT_FONT
)

def show_text(s: str, wait_key: bool = True, font_size: float = FONT_SIZE, color=None):
    """通用文本展示 — 指导语 / 反馈 / 结束提示"""
    msg.text = s
    msg.height = font_size
    msg.color = color or TXT_COLOR
    msg.draw()
    win.flip()
    if wait_key:
        kb.clearEvents()
        keys = kb.waitKeys(keyList=None)
        if any(k.name == KEY_QUIT for k in keys):
            raise SystemExit

# ============================================================
# 六、数据处理器（每个阶段独立 ExperimentHandler）
# ============================================================
thisExp = data.ExperimentHandler(
    name=EXP_NAME,
    extraInfo=info,
    savePickle=False,
    saveWideText=False,
    dataFileName=filename_prefix
)
thisExp.extraInfo = {}

# ============================================================
# 七、工具函数
# ============================================================

# ---------- 退出安全网 ----------
aborted_by_user = False

def cleanup_outputs():
    for path in glob.glob(filename_prefix + ".*"):
        try:
            os.remove(path)
        except:
            pass

def exit_without_saving():
    global aborted_by_user
    aborted_by_user = True
    cleanup_outputs()
    try:
        win.close()
    except:
        pass
    core.quit()

# ---------- 路径 ----------
def stim_path(filename: str) -> str:
    return os.path.join(BASE_DIR, "stimuli", filename)

# ---------- 条件加载 + 校验 ----------
def load_rows_or_exit(xlsx_path: str, required_cols: list):
    full_path = os.path.join(BASE_DIR, xlsx_path)
    try:
        rows = data.importConditions(full_path)
    except Exception as e:
        show_text(f"Error loading {full_path}:\n{repr(e)}", True)
        exit_without_saving()
    if len(rows) == 0:
        show_text(f"Error: {full_path} is empty.", True)
        exit_without_saving()
    missing = [c for c in required_cols if c not in rows[0]]
    if missing:
        show_text(f"Missing columns in {xlsx_path}: {', '.join(missing)}", True)
        exit_without_saving()
    return rows

# ---------- 安全等待（可被 escape 中断） ----------
def safe_wait(sec: float):
    """Escape-checking wait. core.wait(0.001) here is a polling yield (~1ms), not a timing block —
    it prevents CPU spinning while keeping the escape path responsive. This is safe. """
    t0 = core.getTime()
    while core.getTime() - t0 < sec:
        if kb.getKeys(keyList=[KEY_QUIT], waitRelease=False, clear=False):
            exit_without_saving()
        core.wait(0.001)

# ---------- 伪随机 ----------
def can_append_trial(seq, candidate):
    """检查是否违反任何连续性约束"""
    key = "condition"
    count = 0
    for row in reversed(seq):
        if row[key] == candidate[key]:
            count += 1
        else:
            break
    return count < MAX_CONSEC_SAME_CONDITION

def pseudorandomize(raw_trials):
    for _ in range(MAX_PSEUDORAND_TRIES):
        remaining = list(raw_trials)
        rng.shuffle(remaining)
        seq = []
        while remaining:
            valid = [i for i, c in enumerate(remaining) if can_append_trial(seq, c)]
            if not valid:
                break
            seq.append(remaining.pop(rng.choice(valid)))
        if len(seq) == len(raw_trials):
            return seq
    show_text("Error: 无法生成满足约束的 trial 顺序。", True)
    exit_without_saving()

# ============================================================
# 八、单次 trial 函数（五步法则）
# ============================================================
def run_one_trial(row: dict, trial_index: int, block_index: int, phase: str):
    """呈现→ 收集→ 反馈→ ITI→ 写数据"""

    # ① 刺激呈现
    stimText.text = row["stimulus"]
    stimText.draw()
    win.callOnFlip(kb.clock.reset)
    win.callOnFlip(kb.clearEvents)
    win.flip()
    rt_clock = core.Clock()
    onset_ts = datetime.now(timezone.utc).isoformat()

    # ② 反应收集
    resp_key, rt_ms, correct, timeout = "", None, 0, 0
    while rt_clock.getTime() < RESP_MAX_S:
        keys = kb.getKeys(keyList=ALLOWED_KEYS + [KEY_QUIT], waitRelease=False, clear=False)
        if keys:
            k = keys[0]
            if k.name == KEY_QUIT:
                exit_without_saving()
            resp_key = k.name
            rt_ms = int(k.rt * 1000)                         # Rule 14: 整数 ms
            correct = int(resp_key == row["correct_key"])    # Rule 15: 0/1 int
            break
        stimText.draw()
        win.flip()
        core.wait(0.001)

    if rt_ms is None:
        timeout = 1

    # ③ 反馈（根据 phase 分支）
    if phase == "practice":
        if timeout:
            t, c = "超时", "red"
        elif correct:
            t, c = "正确", "green"
        else:
            t, c = "错误", "red"
        show_text(t, wait_key=False, font_size=FEEDBACK_FONT_SIZE, color=c)
        safe_wait(FEEDBACK_S)

    # ④ ITI
    iti_ms = rng.randint(int(ITI_MIN_S * 1000), int(ITI_MAX_S * 1000))
    win.flip()
    safe_wait(iti_ms / 1000.0)

    # ⑤ 数据写出 — 全部字段一次性 addData + nextEntry
    for kk in SUBJECT_COLS:
        thisExp.addData(kk, info.get(kk, ""))
    thisExp.addData("subject_id", info["Participant ID"])
    thisExp.addData("phase", phase)
    thisExp.addData("block", block_index)
    thisExp.addData("trial", trial_index)
    thisExp.addData("condition", row["condition"])
    thisExp.addData("stimulus", row["stimulus"])
    thisExp.addData("correct_response", row["correct_key"])
    thisExp.addData("response", resp_key)
    thisExp.addData("rt", rt_ms)
    thisExp.addData("accuracy", correct)
    thisExp.addData("timeout", timeout)
    thisExp.addData("iti_ms_actual", iti_ms)                # Rule 16: 运行时值
    thisExp.addData("timestamp", onset_ts)
    thisExp.nextEntry()                                      # Rule 10: 立即写盘
    thisExp.saveAsWideText(filename_prefix + ".csv", delim=",")
    with open(filename_prefix + ".csv", "ab") as checkpoint_file:
        checkpoint_file.flush()
        os.fsync(checkpoint_file.fileno())                    # Rule 10: 耐久 checkpoint

# ============================================================
# 九、主流程
# ============================================================
try:
    # --- 指导语 ---
    show_text(TXT_START, True)

    # --- 条件加载 + 校验 ---
    rows = load_rows_or_exit(CONDITION_XLSX, ["stimulus", "correct_key"])

    # --- 正式实验 ---
    trials = pseudorandomize(rows)
    for i, row in enumerate(trials, start=1):
        run_one_trial(row, trial_index=i, block_index=1, phase="main")

    # --- 结束 ---
    show_text(TXT_END, True, font_size=FEEDBACK_FONT_SIZE)

except SystemExit:
    exit_without_saving()

except Exception as e:
    show_text(f"程序异常：{repr(e)}", True)
    exit_without_saving()

finally:
    if not aborted_by_user:
        thisExp.saveAsWideText(filename_prefix + ".csv")     # Rule 11: 阶段保存
        thisExp.saveAsPickle(filename_prefix)
    try:
        thisExp.abort()
    except:
        pass
    try:
        win.close()
    except:
        pass
    core.quit()
```

**使用方式**：复制此骨架 → 修改配置区参数 → 替换文本常量 → 在 `run_one_trial` 内替换刺激/响应/反馈逻辑 → 添加多阶段/多 block 循环 → 不要改变 API 模式（PTB keyboard、`key.rt`、`callOnFlip`、`try/except/finally`、`nextEntry`）。

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

| 特性 | TextBox2 | TextStim |
|------|-----------------|-----------------|
| 主要用途 | 多行排版、可编辑文本、复杂对齐 | 简单/传统文本刺激 |
| 字体与非等宽文本 | 支持；需验证目标字体 | 支持；需验证目标字体 |
| 排版/边界属性 | 以 pinned runtime 的公共 API 为准 | 以 pinned runtime 的公共 API 为准 |
| 动态颜色/透明度 | 使用该版本公开属性并做视觉测试 | 使用该版本公开属性并做视觉测试；不要写入私有 `_need*` 状态 |

按 config 的排版、编辑和兼容性需求选择组件。不要把某一版本的私有实现细节当作跨版本生成规则。

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

| Backend | Scheduling capability | Evidence requirement |
|---------|-----------------------|----------------------|
| **PTB** (`backend_ptb`) | Supports scheduled playback APIs such as `play(when=)` in compatible pinned environments | Measure onset/synchrony with the actual device, driver, buffer, and load |
| **sounddevice** | Host/device dependent streaming | Verify supported API/version and measure the target setup |
| **pyo** | Host/device dependent | Verify installation compatibility and measure the target setup |
| **pygame** | Basic fallback playback; not the supported path for claim-relevant onset timing | Do not use for timing claims without independent calibration evidence |

**当前支持路径**: 对需要可验证音频起始时间的实验，默认使用并测试 PTB 音频后端，同时记录实际设备/驱动/缓冲设置。若采用其他后端或外部音频硬件，必须给出等价的时间戳、校准和目标机测量证据；不能仅凭后端名称声称精度。

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
sound_stim.play(when=nextFlip)                 # scheduled request; validate measured onset/synchrony
win.flip()

# Or via callOnFlip
stim.draw()
win.callOnFlip(sound_stim.play)
win.flip()
```

### 3.4 Speaker / Latency Class

```python
# Only for pinned runtimes whose verified API exposes SpeakerDevice this way.
from psychopy.hardware.speaker import SpeakerDevice

speaker = SpeakerDevice(name=CONFIRMED_DEVICE, latencyClass=CONFIRMED_LATENCY_CLASS)
sound_stim = sound.Sound('stim.wav', speaker=speaker, preBuffer=-1)
```

`latencyClass` changes sharing/exclusivity and failure behavior; it is not a measured latency value. Confirm the class and device against the exact runtime documentation, keep sample-rate/resampling decisions explicit, and record device profile/dropout/timing evidence when audio onset matters. Do not assume a default across PsychoPy releases.

## 4. Response Collection

Edge cases to handle:
- **Anticipatory responses**: apply the prespecified task/device-derived rule — retain raw RT and flag it for analysis rather than silently deleting it
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
    seed=RANDOM_SEED,      # 按 config.seed_scope 从任务版本、被试和 session 解析
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

TRIGGER_PULSE_SECONDS = CONFIRMED_DEVICE_PULSE_WIDTH
trigger_clock = core.Clock()
trigger_active = False

def start_trigger(code):
    global trigger_active
    port.setData(code)
    trigger_clock.reset()
    trigger_active = True

# CORRECT: trigger synchronized to stimulus onset
stim.draw()
win.callOnFlip(start_trigger, trigger_code)
win.flip()

# In the active frame/event loop; cleanup must also force port.setData(0).
if trigger_active and trigger_clock.getTime() >= TRIGGER_PULSE_SECONDS:
    port.setData(0)
    trigger_active = False

# BAD: trigger sent before flip — it can precede the measured visual onset by a display frame/phase
port.setData(trigger_code)
win.flip()
```

### 7.2 Audio-Visual Sync with Triggers

```python
# Sync sound + visual + parallel port trigger
stim.draw()
nextFlip = win.getFutureFlipTime(clock='ptb')
win.callOnFlip(start_trigger, trigger_code)
sound_stim.play(when=nextFlip)  # audio at same time as new frame
win.flip()
```

Backend scheduling is a request, not proof of physical synchrony. Measure audio, visual, and trigger onsets on the actual collection hardware and record the observed distribution.

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
| `kb.waitKeys(maxWait=...)` during a phase that needs refresh/triggers/continuous abort handling | Prevents concurrent phase work | `kb.getKeys()` in a non-blocking loop; allow `waitKeys()` only for justified static, non-critical screens |
| `time.sleep(0.5)` | Blocks event loop | `CountdownTimer` loop or flip-based timing |
| `core.wait(duration)` in an interactive/timed phase | Blocks concurrent event handling | Timed loop with escape check; use a device-required pulse only with an explicit measured contract |
| Loading images inside trial loop | Frame drops from disk I/O | Preload at startup, `.setImage()` per trial |
| `ImageStim` per trial without preloading | Re-allocation causes jitter | Create once, `.setImage()` per trial |
| RT measured with `time.time()` or `clock.getTime()` | Not sync'd to screen refresh, ignores USB HID timestamp | `key.rt` (async USB HID timestamp) |
| `kb.clock.getTime()` for RT | Returns code-execution time, not key-press time | `key.rt` |
| `kb.getKeys(waitRelease=True)` when the scored event is key-down | Filters for released keys and can delay event delivery | `waitRelease=False`; use `True` only when release/duration is the intended event |
| Data saved only at end | Crash = zero data | Save + flush per trial, `try/finally` |
| No escape key handler | Can't quit if something goes wrong | Escape in timed loop + between-trial check |
| Default font for Chinese text | □□□ tofu characters | Explicit CJK font path via FONT_CONFIG |
| EEG trigger before `win.flip()` | Trigger can precede the measured visual onset by a display frame/phase | `win.callOnFlip(port.setData, code)` |
| `exec()` / `globals()` condition injection | Namespace mutation, unsafe column collisions, weak provenance | Explicit validated `trial["field"]` access |
| Constructing/loading sound inside a timed trial or leaving backend/device implicit for a timing claim | I/O and backend behavior are unverified | Prepare sounds before trials, pin backend/device/buffer settings, schedule where supported, and measure the target setup |
| Adding loops to ExperimentHandler at start | Loop tracking breaks | `exp.addLoop()` right before loop runs |
| Implicit keyboard backend in a timing-critical task | Timing behavior and fallback are undocumented | Choose an available backend explicitly and verify it on the target machine |
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
| 音频播放 | `sound.Sound()` | Pre-create before trials; PTB `play(when=)` where supported; record backend/device/buffer and measured onset |
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
