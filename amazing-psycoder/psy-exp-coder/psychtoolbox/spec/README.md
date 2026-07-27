# Psychtoolbox Implementation Guide

> **Status**: Layer 1 — API 规范、反模式表、强制模式。生成时必须与 config 固定的 MATLAB/Octave、Psychtoolbox 和目标 OS/hardware 版本核对。
> **Last updated**: 2026-07-25 — 17-rule quality template applied (8-section PTB adaptation)

## Critical Rules (Read First — errors here invalidate data)

| Rule | Why Critical |
|------|-------------|
| **RT from `VBLTimestamp`, never `GetSecs`** | Wrong RT source = all RT data invalid. `Screen('Flip')` return value is the GPU flip time |
| **`fclose` after every trial** | Missing = buffered data lost on crash. `fopen('a')` + `fprintf` + `fclose` per trial |
| **`KbQueueFlush` at start of each trial** | Missing = previous trial keypress contaminates current RT |
| **`cleanup()` in BOTH `try` AND `catch`** | MATLAB has no `finally`. One missed branch = screen locked, cursor hidden |
| **`global` declarations in both script AND functions** | MATLAB requires `global x` in main script AND each function that uses it |
| **Preload stimuli outside trial loop** | `imread`/`MakeTexture` inside loop = frame drops |

Full anti-patterns table: [§11](#11-anti-patterns-quick-reference). Full 17-rule template: [§0](#0-code-structure-requirements-17-rule-quality-template-ptb-adaptation).

## Version Assumption

Do not assume a default PTB release, host runtime, license state, or backwards-compatibility range. Confirm the exact target versions and current official installation/licensing requirements, pin them in the runtime contract, and run synchronization tests on the collection machine.

## 0. Code Structure Requirements (17-Rule Quality Template — PTB Adaptation)

Every generated PTB experiment must follow these rules. The template is identical to the PsychoPy version except where MATLAB/PTB API differences require adaptation (marked **[PTB]**).

### 0.1 File-Level Structure (Rules 1–2)

```matlab
% {filename}.m
% ---------------------------------------------------------------
% 一体化流程：
%   {stage_1} → {stage_2} → {stage_3}
%
% 数据输出：
%   {stage} -> sub-{id}_{stage}_{date}.csv
%
% 设计概要：
%   每个 block：{trial_count} trial
%   正式阶段：{block_count} block × {trials_per_block} = {total} trial
%
% 当前版本关键修改：
%   1) {change_1}
%   2) {change_2}
% ---------------------------------------------------------------
```

### 0.2 Section Order (Rules 1, 3, 5 — PTB: 8 sections)

```
Section 1:  参数配置区（路径 / 屏幕 / 字体 / 时序 / 按键 / 条件 / 随机种子）
            包含文本常量 — 所有指导语/反馈文字在此定义为字符串变量        ← Rule 3+5
Section 2:  屏幕初始化（PsychImaging + BlendFunction + ifi + Priority）
Section 3:  刺激预加载（MakeTexture / CreateProceduralGabor — 循环外）    ← Rule 13
Section 4:  KbQueue 初始化（Create + Start — 循环前一次）                ← [PTB]
Section 5:  数据文件初始化（fopen + fprintf header + fclose）             ← [PTB]
Section 6:  工具函数（cleanup / saveTrial / checkEscape / safeWait / 伪随机引擎）
Section 7:  主循环（try → trial loop → cleanup → catch → cleanup）       ← Rule 8 [PTB]
Section 8:  本地函数（cleanup / saveTrial — 必须在 script 文件末尾）     ← [PTB]
```

**[PTB]** MATLAB script 文件要求所有本地函数定义在文件末尾。不允许在 script 中间插入 function 定义。

### 0.3 Variable Naming (Rule 4 — PTB: camelCase)

```
<stagePrefix><Category><Meaning>

stagePrefix = kp | nv | prac | main | (按实验阶段自定义)
Category    = Txt (指导语文本) | Key (按键) | Sec (秒级时序)
            | Dir (文件夹路径) | Fb (反馈) | Xlsx (条件表文件名)
            | MaxConsec (伪随机约束) | n (计数)

正例: kpItiSec, nvFeedTimeout, nvMaxConsecEllipse
反例: iti, feedback_timeout, max_ellipse
```

**[PTB]** PTB 惯例用 camelCase。Python 的 UPPER_SNAKE 在此不适用。跨平台常量（`KEY_QUIT`、`BASE_DIR`）保留 UPPER_SNAKE 因为它们是运行环境常量而非实验参数。

### 0.4 Pseudorandom Constraints (Rule 6 — PTB: Shuffle + while)

```matlab
% ---------- 伪随机约束 ----------
nvMaxConsecEllipse    = 2;      % 每个约束一个常量
nvMaxConsecPrimeWidth = 3;
nvMaxPseudorandTries  = 5000;   % 硬性上限，防止死循环

function ok = canAppendTrial(seq, candidate)
    % 检查 candidate 加在 seq 末尾是否违反任何约束
end

function ordered = pseudorandomize(rawTrials)
    for attempt = 1:nvMaxPseudorandTries
        remaining = rawTrials(randperm(length(rawTrials)));
        seq = {};
        while ~isempty(remaining)
            validIdx = [];
            for i = 1:length(remaining)
                if canAppendTrial(seq, remaining{i})
                    validIdx(end+1) = i;
                end
            end
            if isempty(validIdx), break; end
            pick = validIdx(randi(length(validIdx)));
            seq{end+1} = remaining{pick};
            remaining(pick) = [];
        end
        if length(seq) == length(rawTrials)
            ordered = seq; return;
        end
    end
    error('无法生成满足约束的 trial 顺序。');  % 失败必须退出
end
```

**[PTB]** MATLAB 用 `Shuffle()` (Psychtoolbox) 或 `randperm()` 替代 Python 的 `random.shuffle()`。`error()` 替代 Python 的 `exit_without_saving()`。

### 0.5 Exit Safety (Rule 7 — PTB: cleanup + error)

```matlab
function cleanup()
    KbQueueStop; KbQueueRelease;
    fclose('all');
    sca; Priority(0); ShowCursor;
end

% 退出点：用户按 Escape → cleanup(); error('用户手动退出');
%         文件缺失    → cleanup(); error('Missing: %s', path);
%         校验失败    → cleanup(); error('条件表校验失败');
```

**[PTB]** MATLAB 无 `core.quit()` — `error()` 会跳转到 `catch` 块。`sca` (= `Screen('CloseAll')`) 恢复显示。`cleanup()` 必须在 `try` 和 `catch` 两个分支都调用。

### 0.6 Condition Validation (Rule 9)

```matlab
validPrimeNames  = {'narrow', 'broad'};
validShapes      = {'circle', 'ellipse'};

% 逐行校验
for i = 1:length(primeRows)
    if ~ismember(lower(primeRows{i}.prime), validPrimeNames)
        error('prime 表第 %d 行 prime 非法：%s', i, primeRows{i}.prime);
    end
end

% 素材文件预检查
for i = 1:length(neededFiles)
    if ~isfile(neededFiles{i})
        error('素材缺失: %s', neededFiles{i});
    end
end
```

### 0.7 Trial Function Contract (Rule 12 — PTB: KbQueue timing)

```matlab
function [respKey, rtMs, correct, timeout] = runOneTrial(row, trialIdx, blockIdx, phase)
    % ① 刺激呈现（VBLTimestamp = RT 起点）
    % ② 反应收集（KbQueueCheck loop + deadline + escape）
    % ③ 反馈呈现（根据 phase 分支）
    % ④ ITI（帧循环 + escape 检查）
    % ⑤ 数据写出（saveTrial 立即写盘）
end
```

**[PTB]** RT 起点必须是 `Screen('Flip')` 返回的 `VBLTimestamp`，不是 `GetSecs`。RT 公式: `rtMs = (firstPress - stimOnset) * 1000`。

### 0.8 Per-Trial Data Write (Rules 10, 14–16 — PTB: saveTrial)

```matlab
function saveTrial(path, subjectID, block, trial, condition, stimulus, ...
        correctResp, response, rtMs, accuracy, onsetTs, seed)
    fid = fopen(path, 'a');  % 'a' = append mode — crash-safe
    if fid < 0, error('无法打开数据文件: %s', path); end
    if isnan(rtMs), rtText = ''; else, rtText = sprintf('%.0f', rtMs); end  % Rule 14: 整数 ms
    fprintf(fid, '%s,%d,%d,%s,%s,%s,%s,%s,%d,%s,%d\n', ...
        subjectID, block, trial, condition, stimulus, correctResp, ...
        response, rtText, accuracy, onsetTs, seed);                         % Rule 15: accuracy 为 0/1 int
    fclose(fid);  % fclose 每 trial — 耐久 checkpoint                            Rule 10
end
```

**[PTB]** PTB 无 ExperimentHandler。用 `fopen(..., 'a')` + `fprintf` + `fclose` 实现等价增量保存。`fclose` 必须在每次 trial 后调用以确保崩溃可恢复。

### 0.9 Main Flow (Rule 8 — PTB: try/catch)

```matlab
try
    % --- 指导语 ---
    showText(txtStart);

    % --- 条件加载 + 校验 ---
    rows = loadConditions(conditionXlsx);

    % --- 正式实验 ---
    for trial = 1:nTrials
        KbQueueFlush([], 2);
        runOneTrial(rows{trialOrder(trial)}, trial, 1, 'main');
    end

    % --- 结束 ---
    showText(txtEnd);
    cleanup();
    fprintf('数据已保存至: %s\n', dataFile);

catch ME
    cleanup();
    rethrow(ME);
end
```

**[PTB]** MATLAB 无 `finally`。`cleanup()` 在两个分支都显式调用。效果等价于 Python 的 `try/except/finally`。`rethrow(ME)` 保留原始错误信息。

### 0.10 Comment Rules (Rule 17)

```matlab
% 正例 — 解释意图
stimOnset = VBLTimestamp;                    % RT 起点：GPU 翻页时刻
% 已删除 pre-blank，仅保留 ITI                  ← 解释设计决策
itiSec = itiMinSec + rand * (itiMaxSec - itiMinSec);  ← 不写 "% 生成随机数"（废话）

% 反例 — 不做
vbl = Screen('Flip', window);  % 执行翻屏         ← 代码已自明
ifi = Screen('GetFlipInterval', window); % 获取帧间隔 ← 废话
```

## 1. Canonical Safety/Timing Baseline（契约概览 — 完整可运行代码见 §1.1）

新 PTB 项目应保留该基线中的同步测试、显式 seed、受保护清理、实际 flip/response 时间戳和增量保存契约；组件与循环结构由 config 决定。本节展示 API 契约要点；完整的可复制粘贴骨架在 [§1.1](#11-canonical-code-skeleton新项目的契约基线)。

```matlab
% 1. 设置
PsychDefaultSetup(2);                                  % 默认设置 + 统一键名
Screen('Preference', 'SkipSyncTests', 0);              % 生产环境必须跑同步测试
KbName('UnifyKeyNames');                               % 跨平台键名统一
randomSeed = resolvedSeed;                             % 部署层按 config.seed_scope 解析并记录
rng(randomSeed, 'twister');                            % 可复现随机化

try
    % 2. 打开窗口
    screens = Screen('Screens');
    screenNumber = max(screens);
    white = WhiteIndex(screenNumber);
    black = BlackIndex(screenNumber);
    grey = white / 2;
    [window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey);
    Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');
    ifi = Screen('GetFlipInterval', window);
    [centerX, centerY] = RectCenter(windowRect);
    HideCursor(window);
    Priority(MaxPriority(window));
    topPriorityLevel = MaxPriority(window);
    Priority(topPriorityLevel);

    % 3. 预加载刺激（循环前）
    % ... Screen('MakeTexture') / CreateProceduralGabor / PsychPortAudio('CreateBuffer') ...

    % 4. 键盘队列初始化
    KbQueueCreate();         % 创建队列（可在参数中指定 keyList）
    KbQueueStart();          % 开始记录

    % 5. 实验循环
    for trial = 1:nTrials
        KbQueueFlush();      % 每 trial 开始时清除旧事件

        % 绘制 + Flip + RT 收集
        % ...

        % 数据保存：trial 结束后 append + fclose，确保崩溃可恢复
        % saveTrial(dataPath, trialData, randomSeed);
    end

    % 6. 键盘队列释放
    KbQueueStop();
    KbQueueRelease();

    % 7. 数据文件关闭
    fclose(dataFile);

    % 8. 清理
    sca;
    Priority(0);
    ShowCursor;

catch ME
    sca;
    Priority(0);
    ShowCursor;
    rethrow(ME);
end
```

### 1.1 Canonical Code Skeleton（新项目的契约基线）

以下骨架展示支持的 API 契约。按任务设备/事件模型调整结构；偏离必须保持等价同步、数据和清理保障并接受目标机测试，`modify`/`debug` 不需重写无关架构：

```matlab
% {filename}.m
% ---------------------------------------------------------------
% 一体化流程：
%   {stage_1} → {stage_2} → {stage_3}
%
% 数据输出：
%   {stage} -> sub-{id}_{stage}_{date}.csv
%
% 设计概要：
%   每个 block：{n} trial
%   正式阶段：{m} block × {t} = {total} trial
%
% 当前版本关键修改：
%   1) {change_1}
%   2) {change_2}
% ---------------------------------------------------------------
close all; clear; sca;

% ============================================================
% 一、参数配置区（所有可调参数 + 文本常量集中在此）
% ============================================================
% MATLAB script 中的变量不会自动对本地函数可见。
% 需要在脚本和函数中都声明 global。
% 不要去掉这些 global 声明 —— 否则 showText/checkEscape/cleanup 会读到空变量。
global window textColor fontSize escapeKey;

taskName    = '{experiment_name}';
taskVersion = '1.0.0';
subjectID   = 'test';
baseDataColumns = {'subject_id', 'block', 'trial', 'condition', 'stimulus', ...
    'correct_response', 'response', 'rt', 'accuracy', 'timestamp'};

% ---------- 屏幕 ----------
screenNumber    = max(Screen('Screens'));
backgroundColor = [128 128 128] / 255;  % grey
textColor       = [0 0 0];
fontName        = 'PingFang SC';
fontSize        = 60;

% ---------- 时序 (秒) ----------
fixationSec    = 0.5;
stimulusSec    = 1.0;
feedbackSec    = 0.5;
respDeadlineSec = 2.0;
itiMinSec      = 0.6;
itiMaxSec      = 0.9;

% ---------- 按键 ----------
KbName('UnifyKeyNames');
keyLeft   = KbName('LeftArrow');
keyRight  = KbName('RightArrow');
escapeKey = KbName('ESCAPE');
responseKeys = [keyLeft, keyRight];

% ---------- 文本常量 ----------
txtStart = '欢迎参加实验。\n\n按任意键开始。';
txtEnd   = '实验结束，感谢参与！\n\n按任意键退出。';

% ---------- 条件 ----------
conditionXlsx = 'conditions.xlsx';
nReps = 10;

% ---------- 伪随机约束 ----------
maxConsecSameCondition = 3;
maxPseudorandTries     = 5000;

% ---------- 数据 ----------
dataDir = fullfile(pwd, 'data');
if ~exist(dataDir, 'dir')
    [ok, msg] = mkdir(dataDir);
    if ~ok
        error('无法创建数据文件夹 %s: %s。请检查磁盘空间和权限。', dataDir, msg);
    end
end
runTs = datestr(now, 'yyyymmdd_HHMMSSFFF');
dataFile = fullfile(dataDir, sprintf('sub-%s_%s_%s.csv', subjectID, taskName, runTs));

% ============================================================
% 二、屏幕初始化
% ============================================================
PsychDefaultSetup(2);
Screen('Preference', 'SkipSyncTests', 0);

% 种子（FNV-1a — 可复现随机化）
seedMat = unicode2native(sprintf('%s|%s', taskVersion, subjectID), 'UTF-8');
seedHash = uint32(2166136261);
for b = seedMat
    seedHash = bitxor(seedHash, uint32(b));
    seedHash = uint32(mod(uint64(seedHash) * uint64(16777619), uint64(4294967296)));
end
randomSeed = double(seedHash);
rng(randomSeed, 'twister');

[window, windowRect] = PsychImaging('OpenWindow', screenNumber, backgroundColor, [], 32, 2);
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');
Screen('TextFont', window, fontName);
Screen('TextSize', window, fontSize);

ifi = Screen('GetFlipInterval', window);
waitframes = 1;
[xCenter, yCenter] = RectCenter(windowRect);

Priority(MaxPriority(window));
HideCursor;

% ============================================================
% 三、刺激预加载（循环外）
% ============================================================
fixCross = [-20 20 0 0; 0 0 -20 20];  % 注视点十字

% ============================================================
% 四、KbQueue 初始化（循环前一次 Create + Start）
% ============================================================
KbQueueCreate([], responseKeys);
KbQueueStart;

% ============================================================
% 五、数据文件初始化
% ============================================================
fid = fopen(dataFile, 'w');
fprintf(fid, ['subject_id,block,trial,condition,stimulus,correct_response,' ...
              'response,response_status,rt,accuracy,timestamp,rng_seed\n']);
fclose(fid);

% ============================================================
% 六、工具函数（声明在 Section 8，此处为调用点注释）
%    cleanup()   — KbQueue 释放 + sca + Priority 恢复
%    saveTrial() — fopen('a') + fprintf + fclose 增量写入
%    showText()  — 指导语/反馈文本展示
%    checkEscape() — 每帧 escape 检测
% ============================================================

% ============================================================
% 七、主循环
% ============================================================
% ⚠️ MATLAB 无 finally。cleanup() 必须在 try 和 catch 两个分支都调用。
% OpenWindow 放在 try 内部 — 如果窗口创建失败，catch 仍执行 cleanup。
try
    % --- 指导语 ---
    showText(txtStart);

    % --- 条件加载 + 校验 ---
    rows = loadConditions(conditionXlsx);
    nTrials = size(rows, 1) * nReps;
    trialOrder = Shuffle(repelem(1:size(rows, 1), nReps));

    % --- 正式实验 ---
    vbl = Screen('Flip', window);

    for trial = 1:nTrials
        KbQueueFlush([], 2);  % 清除旧事件

        row = rows{trialOrder(trial)};

        % === 注视点 ===
        fixationFrames = round(fixationSec / ifi);
        for f = 1:fixationFrames
            Screen('DrawLines', window, fixCross, 3, textColor, [xCenter yCenter], 2);
            vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
            checkEscape();
        end

        % === 刺激 + 响应窗口 ===
        DrawFormattedText(window, row.stimulus, 'center', 'center', textColor);
        [vbl, ~, ~, ~] = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
        stimOnset = vbl;  % Rule 14: VBLTimestamp = RT 起点
        onsetTs = char(datetime('now', 'TimeZone', 'UTC', ...
            'Format', "yyyy-MM-dd'T'HH:mm:ss.SSSXXX"));

        gotResp = false; rtMs = NaN; resp = '';
        deadline = stimOnset + respDeadlineSec;
        while ~gotResp && GetSecs < deadline
            [pressed, firstPress] = KbQueueCheck;
            if pressed
                keyIdx = find(firstPress > 0);
                firstKey = keyIdx(1);
                rtMs = (firstPress(firstKey) - stimOnset) * 1000;  % Rule 14
                if firstKey == keyLeft
                    resp = 'left'; gotResp = true;
                elseif firstKey == keyRight
                    resp = 'right'; gotResp = true;
                end
            end
            checkEscape();
            DrawFormattedText(window, row.stimulus, 'center', 'center', textColor);
            vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
        end

        % --- 正确率 ---
        if ~gotResp
            accuracy = double(strcmp(row.correct_key, 'none'));  % Rule 15: 0/1 int
            status = 'timeout'; resp = '';
        else
            accuracy = double(strcmp(resp, row.correct_key));
            status = 'responded';
        end

        % --- 增量保存 (Rule 10: 立即写盘) ---
        saveTrial(dataFile, subjectID, 1, trial, row.condition, row.stimulus, ...
            row.correct_key, resp, status, rtMs, accuracy, onsetTs, randomSeed);

        % === ITI (随机) ===
        itiSec = itiMinSec + rand * (itiMaxSec - itiMinSec);
        itiFrames = round(itiSec / ifi);
        for f = 1:itiFrames
            vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
            checkEscape();
        end
    end

    % --- 结束 ---
    showText(txtEnd);
    cleanup();
    fprintf('数据已保存至: %s\n', dataFile);

catch ME
    cleanup();
    rethrow(ME);
end

% ============================================================
% 八、本地函数（MATLAB script 要求函数定义在文件末尾）
% ============================================================

function showText(text)
    global window textColor fontSize;
    DrawFormattedText(window, double(text), 'center', 'center', textColor);
    Screen('Flip', window);
    KbStrokeWait;
end

function rows = loadConditions(xlsxPath)
    rows = table2struct(readtable(xlsxPath));
    if isempty(rows), error('条件表为空: %s', xlsxPath); end
end

function checkEscape()
    global escapeKey;
    [keyDown, ~, keyCode] = KbCheck;
    if keyDown && keyCode(escapeKey)
        cleanup(); error('用户手动退出');
    end
end

function saveTrial(path, subjectID, block, trial, condition, stimulus, ...
        correctResp, response, status, rtMs, accuracy, onsetTs, seed)
    fid = fopen(path, 'a');
    if fid < 0, error('无法打开数据文件: %s', path); end
    if isnan(rtMs), rtText = ''; else, rtText = sprintf('%.0f', rtMs); end  % Rule 14: 整数 ms
    fprintf(fid, '%s,%d,%d,%s,%s,%s,%s,%s,%s,%d,%s,%d\n', ...
        subjectID, block, trial, condition, stimulus, correctResp, ...
        response, status, rtText, accuracy, onsetTs, seed);                   % Rule 15: accuracy 0/1 int
    fclose(fid);  % Rule 10: 每 trial 耐久 checkpoint
end

function cleanup()
    KbQueueStop; KbQueueRelease;
    fclose('all');
    sca; Priority(0); ShowCursor;
end
```

**使用方式**：复制此骨架 → 修改 Section 1 中的参数 + 文本常量 → 替换 Section 7 中的刺激/响应/反馈逻辑 → 添加多阶段/多 block 循环。不要改变 API 模式（KbQueue、VBLTimestamp RT、帧精确 Flip、try/catch、`saveTrial` 增量写入）。

## 2. 屏幕与窗口设置

> **完整示例**: [demo/_raw/getting-started/totally-minimal.md](../demo/_raw/getting-started/totally-minimal.md) — 最小窗口设置，[demo/_raw/getting-started/screen-coordinates.md](../demo/_raw/getting-started/screen-coordinates.md) — 坐标系统。

### 2.1 窗口打开

```matlab
PsychDefaultSetup(2);
Screen('Preference', 'SkipSyncTests', 0);                  % 生产环境必须为 0
[window, windowRect] = PsychImaging('OpenWindow', ...       % 使用 PsychImaging 打开
    screenNumber, backgroundColor);
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');
ifi = Screen('GetFlipInterval', window);                    % 获取帧间隔
```

### 2.2 `Screen('Flip')` — 帧精确计时核心

**完整签名**:
```matlab
[VBLTimestamp, StimulusOnsetTime, FlipTimestamp, Missed, Beampos] = ...
    Screen('Flip', windowPtr [, when] [, dontclear] [, dontsync] [, multiflip]);
```

**`when` 参数 — 最关键的 timing 参数**:
| 值 | 行为 |
|----|------|
| `0`（默认） | 在下一个可能的垂直回描时 Flip |
| `> 0` | 在系统时间到达 `when` 后的第一个回描时 Flip |

**Half-IFI 规则** — PTB 帧精确计时的核心：

```matlab
vbl = Screen('Flip', window);                            % 初始 flip，获取 vbl 时间戳
for frame = 1:nFrames
    % ... 绘制命令 ...
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);  % 帧精确
end
```

**为什么减 0.5 * ifi**: 提前半帧提交目标时刻可降低因调度/舍入而错过预期回描截止点的风险。这是 PTB 常用调度模式，不是守时保证；仍必须检查 `Missed`、记录实际 flip 时间戳，并在目标机器运行同步与负载测试。

**返回值详解**:
| 返回值 | 说明 |
|--------|------|
| `VBLTimestamp` | Flip 实际发生时间的高精度估计 — **所有计时以此为准** |
| `StimulusOnsetTime` | 刺激起始时间估计，部分后端与 VBLTimestamp 相同 |
| `FlipTimestamp` | Flip 执行结束时的时间戳 |
| `Missed` | 负 = 守时；正 = 丢帧。不可完全依赖（Vulkan/VR 后端下不准确） |
| `Beampos` | 测量时光束位置，-1 或 0 = 不支持 |

### 2.3 固定时长呈现

```matlab
% 呈现 N ms（转换为帧数）
durationSecs = N / 1000;
nFrames = round(durationSecs / ifi);

vbl = Screen('Flip', window);
for f = 1:nFrames
    % 重绘刺激
    Screen('DrawTexture', window, texture);
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
end
```

### 2.4 PTB 关键概念速查

| 概念 | 说明 |
|------|------|
| `PsychImaging` | 窗口打开入口，支持 HDR/立体/Retina/浮点帧缓冲 |
| `Screen('Flip')` 返回值 `vbl` | PTB 报告的 VBL/flip 软件时间参考；物理显示 onset 仍需目标硬件测量 |
| `ifi` | 单帧时长（秒），从 `Screen('GetFlipInterval')` 获取 |
| `waitframes` | 必须为整数，`waitframes = round(seconds / ifi)` |
| `sca` | `Screen('CloseAll')` 的快捷方式 — 紧急清理 |
| `Priority(MaxPriority(window))` | 提升 MATLAB 进程优先级，减少帧丢失 |
| `Screen('DrawingFinished')` | 提示 PTB 当前帧绘制完成，可提前开始渲染 |

## 3. 键盘响应收集

> **完整示例**: [../demo/_raw/getting-started/keyboard-q.md](../demo/_raw/getting-started/keyboard-q.md) — KbQueue 创建、轮询、释放的完整 demo。

### 3.1 KbQueue 生命周期（时序关键键盘任务的 canonical pattern）

For time-critical keyboard tasks, this skill's supported canonical path is `KbQueue`. That choice does not prove end-to-end accuracy: device polling, OS, display synchronization, code, and hardware still require target-machine verification. Other input devices/procedures must use their own documented contract rather than being forced into KbQueue.

```matlab
% === 实验开始前（一次） ===
KbQueueCreate();                            % 创建队列
% 可选指定 keyList:
% keyList = zeros(1, 256);
% keyList(KbName({'LeftArrow', 'RightArrow', 'ESCAPE'})) = 1;
% KbQueueCreate([], keyList);
KbQueueStart();                             % 开始记录

% === 每个 trial 开始时 ===
KbQueueFlush();                             % 清除之前的所有事件

% === 响应收集（帧循环内） ===
[pressed, firstPress] = KbQueueCheck();     % 获取自上次 Check/Flush 以来的按键
if pressed
    keyCodes = find(firstPress > 0);
    rt = min(firstPress(keyCodes)) - stimOnset;  % 秒
    responseKey = KbName(find(firstPress == min(firstPress(keyCodes))));
end

% === 实验结束后 ===
KbQueueStop();
KbQueueRelease();
```

**关键规则:**
- `Create`/`Start` 在 trial 循环**之前**，`Stop`/`Release` 在循环**之后**
- **不要**在 trial 循环内调用 Start/Stop — 队列应持续运行
- **每个 trial 开始前必须 `KbQueueFlush()`** — 防止前 trial 残留按键污染当前 RT
- `KbQueueCheck` 隐含清除效果 — 不能对同一数据调用两次
- **不要**用 `KbCheck` 做 RT（不提供精确时间戳）

### 3.2 KbQueueCheck 返回值详解

```matlab
[pressed, firstPress, firstRelease, lastPress, lastRelease] = KbQueueCheck();
```

| 输出 | 说明 |
|------|------|
| `pressed` | 是否有任何键被按下 |
| `firstPress` | 1×256 数组 — 每个键的**首次按下**时间戳（秒），0 = 未按下 |
| `firstRelease` | 每个键的首次释放时间戳 |
| `lastPress` | 每个键的**最后一次**按下时间戳 |
| `lastRelease` | 每个键的最后一次释放时间戳 |

**RT 计算**:
```matlab
if pressed
    keyIdx = find(firstPress > 0);        % 哪些键被按下
    rtTime = min(firstPress(keyIdx));      % 最早按键的时间
    responseName = KbName(find(firstPress == rtTime, 1));  % 键名
    rt = (rtTime - stimOnset) * 1000;     % 转换为 ms
end
```

### 3.3 多按键处理

由于每键只保留首次/末次时间戳，记录同一键的多次按下需频繁调用 `KbQueueCheck`：
```matlab
% 连续响应场景 — 每次按键后立即 Check 并累积
allKeys = {};
allRTs = [];
while GetSecs < stimOnset + deadline
    [pressed, firstPress] = KbQueueCheck();
    if pressed
        idx = find(firstPress > 0);
        for i = 1:length(idx)
            allKeys{end+1} = KbName(idx(i));
            allRTs(end+1) = firstPress(idx(i)) - stimOnset;
        end
    end
end
```

### 3.4 替代键盘 API

| API | 适用场景 | 限制 |
|-----|---------|------|
| `KbQueueCheck` | This skill's primary pattern for time-critical keyboard events | 需完整生命周期管理和目标机验证 |
| `KbStrokeWait` | 指令屏"按任意键继续" | 阻塞，不返回时间戳 |
| `KbCheck` | Escape/status polling | Polling semantics differ from queued event timestamps; do not substitute it silently for the confirmed RT event definition |
| `KbWait` | Justified static, non-critical wait screens | Blocking; unsuitable when concurrent drawing, triggers, deadlines, or cleanup handling must continue |

## 4. RT 计时规范

> **完整示例**: [../demo/_raw/getting-started/accurate-timing.md](../demo/_raw/getting-started/accurate-timing.md) — 帧精确 timing demo，[../demo/_raw/getting-started/wait-frames.md](../demo/_raw/getting-started/wait-frames.md) — waitframes 用法。

```matlab
% RT 起点必须从 Screen('Flip') 的返回值 VBLTimestamp 获取
% VBLTimestamp 是 GPU 实际完成翻页的时间

Screen('DrawText', window, stimulusText, x, y, textColor);
[VBLTimestamp, ~, ~, ~] = Screen('Flip', window);
stimOnset = VBLTimestamp;                    % 用于 RT 计算

% ... KbQueue 轮询 ...

rt = (keypressTime - stimOnset) * 1000;     % ms
```

**反模式 — 禁止**:
- `stimOnset = GetSecs` 在 Flip 之前或之后 → 不精确
- `rt = GetSecs - stimOnset` 使用 `KbCheck` → 双倍不精确

## 5. 刺激预加载

```matlab
% 循环前预创建所有纹理
trialTextures = cell(1, nStimuli);
for i = 1:nStimuli
    img = imread(stimulusFiles{i});
    trialTextures{i} = Screen('MakeTexture', window, img);
end

% 循环内直接使用
Screen('DrawTexture', window, trialTextures{condition(trial)});
```

| 刺激类型 | 循环前操作 | 循环内操作 |
|---------|----------|----------|
| 图像 | `imread` + `Screen('MakeTexture')` | `Screen('DrawTexture')` |
| Gabor | `CreateProceduralGabor()` | `Screen('DrawTexture', ..., gabortex)` |
| 文本 | `Screen('TextFont')`, `Screen('TextSize')` | `DrawFormattedText` / `Screen('DrawText')` |
| 形状 | 预计算坐标矩阵 | `Screen('FillRect')` / `Screen('DrawLines')` |

**反模式 — 禁止**: 在 trial 循环内调用 `imread` 或 `Screen('MakeTexture')` — 磁盘 I/O 导致帧丢失。

## 6. Audio / PsychPortAudio

PTB 的音频系统以 **PortAudio** 为基础，支持面向低延迟实验的调度与时间戳。实际启动延迟、抖动和同步取决于设备、驱动、缓冲与系统负载，必须在目标机器测量。

### 6.1 基本生命周期

```matlab
InitializePsychSound(1);                                 % 1 = 低延迟 aggressive 模式
pahandle = PsychPortAudio('Open', [], [], 2, freq, nChannels);
% 参数: deviceID(默认=[]), mode(2=standard playback), latencyClass, sampleRate, channels

% 加载音频数据
[audioData, sampleRate] = audioread('stimulus.wav');
audioData = audioData';                                 % 转置为 行=通道 列=采样点
PsychPortAudio('FillBuffer', pahandle, audioData);      % 填充缓冲区

% 播放
PsychPortAudio('Start', pahandle, 1);                    % repetitions=1

% 等待播放完成
PsychPortAudio('Stop', pahandle, 1);                     % waitForStop=1

% 清理
PsychPortAudio('Close', pahandle);
```

### 6.2 Schedule-Based 精确同步

```matlab
% 使用 schedule 实现精确的音频-视觉同步
PsychPortAudio('UseSchedule', pahandle, 1);              % 启用 schedule 模式

% 添加缓冲到 schedule
bufferHandle = PsychPortAudio('CreateBuffer', [], audioData);
PsychPortAudio('AddToSchedule', pahandle, bufferHandle, 1);  % 播放 1 次

% 目标时间来自已确认的 SOA/offset，并在 deadline 之前预调度
targetOnset = priorVbl + confirmedAudioVisualSOA;
PsychPortAudio('Start', pahandle, 1, targetOnset, 0);
visualVbl = Screen('Flip', window, targetOnset - 0.5 * ifi);
% 保存 targetOnset、visualVbl 和设备测量结果；调度请求本身不证明物理同步
```

### 6.3 预加载与低延迟

```matlab
% 方式 1: FillBuffer（简单播放）
PsychPortAudio('FillBuffer', pahandle, audioData);

% 方式 2: CreateBuffer + AddToSchedule（预加载多个音频、精确时序）
buf1 = PsychPortAudio('CreateBuffer', pahandle, audio1);
buf2 = PsychPortAudio('CreateBuffer', pahandle, audio2);
PsychPortAudio('UseSchedule', pahandle, 1, 128);         % 最多 128 slots
PsychPortAudio('AddToSchedule', pahandle, buf1, 1);
PsychPortAudio('AddToSchedule', pahandle, buf2, 1);

% 触发播放（与视觉同步）
PsychPortAudio('Start', pahandle, 0, nextFlipTime, 0);   % repetitions=0, when=nextFlipTime
```

### 6.4 FillBuffer 参数详解

```matlab
[underflow, nextSampleStartIndex, nextSampleETASecs] = ...
    PsychPortAudio('FillBuffer', pahandle, bufferdata [, streamingrefill=0][, startIndex=Append]);
```

| 参数 | 说明 |
|------|------|
| `streamingrefill=0` | 播放停止时一次性填充 |
| `streamingrefill=1` | 播放期间立即重填（替换已播放数据），用于流式 |
| `underflow` 返回 | 1 = 缓冲区欠载（可听出问题） |

**关键**: `bufferdata` 必须是浮点 `[-1.0, +1.0]`，每行一个通道、每列一个采样点。

## 7. 绘图命令速查

| 需求 | 命令 | 关键参数 |
|------|------|---------|
| 矩形填充 | `Screen('FillRect', w, color, rect)` | `rect = [left top right bottom]` |
| 矩形边框 | `Screen('FrameRect', w, color, rect, penWidth)` | |
| 椭圆填充 | `Screen('FillOval', w, color, rect)` | |
| 线条连接 | `Screen('DrawLines', w, xy, width, colors)` | `xy` 为 2×n 矩阵 |
| 单像素点 | `Screen('DrawDots', w, xy, size, color)` | `xy` 为 2×n 矩阵 |
| 简单文本 | `Screen('DrawText', w, text, x, y, color)` | 需先设置 `TextFont`, `TextSize` |
| 格式化文本 | `DrawFormattedText(w, text, 'center', 'center', color, wrapat)` | 支持 `\n` 换行 |
| 纹理绘制 | `Screen('DrawTexture', w, tex, srcRect, dstRect, angle)` | |
| 创建纹理 | `tex = Screen('MakeTexture', w, imageMatrix)` | 需在循环前调用 |
| 注视十字（推荐） | `Screen('DrawLines', w, crossCoords, 3, color)` | 不用 `DrawText('+')` |

## 8. CJK 字体配置

```matlab
% macOS
Screen('TextFont', window, 'PingFang SC');
% Windows
Screen('TextFont', window, 'Microsoft YaHei');
% Linux
Screen('TextFont', window, 'Noto Sans CJK SC');
% 备选（跨平台）
Screen('TextFont', window, '-:Arial Unicode MS');

% 中文文本
Screen('TextSize', window, 60);
DrawFormattedText(window, double('你好世界'), 'center', 'center', textColor);
% double() 确保字符编码正确
```

## 9. 数据保存

### 9.1 增量写入（强制模式）

```matlab
dataDir = fullfile(pwd, 'data');
if ~exist(dataDir, 'dir')
    mkdir(dataDir);
end

dataFile = fopen(fullfile(dataDir, ['sub-' subjectID '_' task '.csv']), 'w');
fprintf(dataFile, 'trial,block,condition,rt,response,correct\n');

for trial = 1:nTrials
    % ... 实验逻辑 ...
    fprintf(dataFile, '%d,%d,%d,%.4f,%s,%d\n', ...
        trial, block, condition, rt, response, correct);
end

fclose(dataFile);
```

### 9.2 崩溃安全版本

```matlab
% 每 trial 写入后立即 fclose + 追加模式重开（最安全）
for trial = 1:nTrials
    % ... 实验逻辑 ...
    fprintf(dataFile, '%d,%d,%d,%.4f,%s,%d\n', trial, block, condition, rt, response, correct);
    fclose(dataFile);
    dataFile = fopen(dataPath, 'a');
end
```

## 10. Escape 处理

```matlab
function checkEscape()
    [keyIsDown, ~, keyCode] = KbCheck;
    if keyIsDown && keyCode(KbName('ESCAPE'))
        sca;
        Priority(0);
        ShowCursor;
        error('Experiment aborted by user.');
    end
end
```

- 在定时循环的每一帧调用 `checkEscape()`
- 响应收集循环内 Escape 需在 `keyList` 中包含
- `sca` 是紧急清理 — 恢复显示、释放纹理、显示光标

## 11. 反模式速查表

| 禁止的 API / 模式 | 原因 | 替代方案 |
|-------------------|------|---------|
| `WaitSecs(N)` 用于实验计时 | 阻塞、无法 Escape、不精确 | `Screen('Flip', ..., vbl + (wf-0.5)*ifi)` 帧循环 |
| `KbWait` | 阻塞、无法计时 RT、无法 Escape | `KbQueueCreate` + `KbQueueCheck` |
| `KbCheck` 用于 RT | 不提供精确时间戳 | `KbQueueCheck` 的 `firstPress` 时间戳 |
| `input()` | 在 PTB 全屏不可见 | PTB 文本 + `KbQueue` |
| `imread` 在 trial 循环内 | 磁盘 I/O 导致帧丢失 | 循环前 `Screen('MakeTexture')` 预加载 |
| `Screen('MakeTexture')` 在 trial 循环内 | 纹理创建开销不确定 | 循环前创建，循环内只 `DrawTexture` |
| 不带 Escape 检查的 `while` 循环 | 用户无法退出全屏 | 每帧 `KbCheck(KbName('ESCAPE'))` |
| `Screen('DrawText', ..., '+')` 用于注视点 | 字体依赖、不居中 | `Screen('DrawLines')` 绘制注视十字 |
| 不带 `sca` 的异常退出 | 屏幕锁死、光标隐藏 | `try/catch` + `sca` + `Priority(0)` + `ShowCursor` |
| `GetSecs` 记录 `stimOnset`（Flip 前后） | 不是 GPU 实际翻页时间 | `VBLTimestamp` = `Screen('Flip')` 返回值 |
| `rt = GetSecs - stimOnset` | 双倍不精确（起点不准+KbCheck 不准）| `firstPress - VBLTimestamp` |
| KbQueue `Create`/`Start` 在 trial 循环内 | 性能开销、可能丢失事件 | `Create`/`Start` 放在循环前，只 `Flush` 每 trial |
| 不在每 trial 前 `KbQueueFlush()` | 前一 trial 残留按键污染当前 RT | 每 trial 开始前 `KbQueueFlush()` |
| `KbQueueCheck` 同一数据两次 | 第一次调用已清除数据 | 保存输出变量 |
| `Sound()` / `audioplayer()` 用于实验音频 | 高延迟、无精确时序 | `PsychPortAudio` |
| `PsychPortAudio('FillBuffer')` 在 trial 循环内 | 非流式场景下无关/可能欠载 | `CreateBuffer` + 循环前预加载 |
| `Screen('Flip')` 无 `when` 参数 | 帧率不固定 | `vbl + (waitframes-0.5)*ifi` |
| 跳过 SyncTests (`SkipSyncTests, 1`) | 帧计时不可靠 | 生产环境设为 0，过不了换机器 |

## 12. 跨平台注意事项

| 平台 | 特点 |
|------|------|
| **macOS ARM** | PTB 3.0.20+ 原生支持 M1/M2/M3/M4；帧顺序立体不工作；`AsyncFlipBegin` 不工作 |
| **macOS Intel** | 需 macOS 10.13+；PTB 3.0.19 免费，3.0.20+ 付费 |
| **Windows** | `Priority` 效果显著；PTB 3.0.20+ 付费 |
| **Linux** | 永久免费；`PsychPortAudio` 暂停 PulseAudio 独占硬件 |
| **Raspberry Pi** | 32-bit 永久免费 |

## 13. API 参考索引

| 需要实现的功能 | 核心 API | 参考 |
|---------------|---------|------|
| 最小窗口骨架 | `PsychDefaultSetup(2)` + `PsychImaging('OpenWindow')` | `../demo/_raw/getting-started/totally-minimal.md` |
| 帧精确计时 | `Screen('Flip', w, vbl+(wf-0.5)*ifi)` | `../demo/_raw/getting-started/accurate-timing.md` |
| 键盘队列 | `KbQueueCreate`/`Start`/`Flush`/`Check`/`Stop`/`Release` | `../demo/_raw/getting-started/keyboard-q.md` |
| 音频播放 | `PsychPortAudio('Open'/'FillBuffer'/'Start')` | 本文件 §6 |
| 音频精确同步 | `PsychPortAudio('UseSchedule'/'AddToSchedule')` | 本文件 §6.2 |
| 文本呈现 | `DrawFormattedText` / `Screen('DrawText')` | `../demo/_raw/text/basic-text.md` |
| 图像呈现 | `imread` + `Screen('MakeTexture')` + `DrawTexture` | `../demo/_raw/textures/draw-image.md` |
| 注视十字 | `Screen('DrawLines', w, coords, width, color)` | `../demo/_raw/drawing-shapes/fixation-cross.md` |
| Gabor 刺激 | `CreateProceduralGabor()` | `../demo/_raw/textures/gabor.md` |
| 矩形/椭圆 | `Screen('FillRect'/'FillOval')` | `../demo/_raw/drawing-shapes/rectangle.md` |
| 数据保存 | `fopen`/`fprintf`/`fclose` | 本文件 §9 |
| Escape 检测 | `KbCheck` + `KbName('ESCAPE')` | 本文件 §10 |
| 条件加载 | `readtable('conditions.xlsx')` | `mapping/README.md` §blocks |
| 窗口查询 | `Screen('Screens')`, `RectCenter`, `GetFlipInterval` | `../demo/_raw/getting-started/totally-minimal-with-info.md` |
