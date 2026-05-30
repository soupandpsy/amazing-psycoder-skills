# Psychtoolbox Config → Code Mapping

> **Status**: Layer 2 — 基于 stroop.md 和 posner-cuing-experiment.md 的实验逻辑分析 + psychtoolbox.org 官方 API 文档。
> **Last updated**: 2026-05-30

## Version Note

PTB 3.0.20+ (Dec 2024): Apple Silicon 原生支持（beta）、macOS/Windows 付费许可证要求。代码生成默认兼容 3.0.19+，不依赖付费版本特性。

## 12 步模板 PTB 实现

| 步骤 | 模板定义 | Stroop 实现 | Posner Cuing 实现 | 通用 PTB 模式 |
|------|---------|------------|-------------------|-------------|
| 1 | Imports / dependencies | `close all; clear; sca; PsychDefaultSetup(2)` | 同 Stroop | `PsychDefaultSetup(2); KbName('UnifyKeyNames'); rng('shuffle')` |
| 2 | Experiment params | `isiTimeSecs`, `trialsPerCondition` | `fixTimeSecs`, `cueTimeSecs`, `targetTimeSecs`, `isiTimeSecs` | 时间参数用秒定义 → `round(secs / ifi)` 转帧数 |
| 3 | Display setup | `PsychImaging('OpenWindow', ..., grey, [], 32, 2)` | `PsychImaging('OpenWindow', ..., grey, [])` | `PsychImaging` + `ifi` + `RectCenter` + `BlendFunction` + `MaxPriority` |
| 4 | Stimulus preloading | 无图片，文字/颜色内联 | `CreateProceduralGabor` 预创建 | 纹理/位置/参数在 trial 循环前计算好 |
| 5 | Condition loading | `condMatrixBase = [sort(repmat([1 2 3], 1, 3)); repmat([1 2 3], 1, 3)]` | `baseMat = [0 0 1 1; 0 1 0 1]` | 矩阵生成 → `repmat` 扩展 → `Shuffle` 随机化 |
| 6 | Helper functions | `GetColorFromList()` + `MakeRectFromCenter()` 嵌套函数 | 无（Gabor 参数内联） | 嵌套函数在脚本末尾：`saveTrial()`, `cleanup()`, `checkEscape()`, `drawFixation()` |
| 7 | Instruction | `if trial==1` + `DrawFormattedText` + `KbStrokeWait` | 同上 | `DrawFormattedText(window, text, 'center', 'center', color)` |
| 8 | Practice | 同上（指令屏 + 练习 trial 循环，不保存数据） | 同上 | `isPractice = true` flag + 相同 trial 循环结构；练习反馈 `DrawFormattedText` + `KbStrokeWait`；正式实验前重置数据计数器 |
| 9a | Block | 单 block | 单 block | `for trial = 1:numTrials` |
| 9b | Randomization | `Shuffle(1:numTrials)` | `Shuffle(cueTargetMat, 2)` | `Shuffle()` 按列/行随机化 |
| 9c | Per-trial | Fixation(1帧) → ISI(多帧) → Stimulus+Response(KbCheck while) | Fixation(N帧) → Cue(N帧) → Gap(N帧) → Target(N帧) → Response(KbCheck while) → ITI(N帧) | `for f=1:nFrames` + `vbl = Screen('Flip', w, vbl+(wf-0.5)*ifi)` |
| 9d | Block feedback | 单 block — 无跨 block 反馈 | 同上 | `blockEnd; meanRT = mean(blockRTs); meanAcc = mean(blockCorrect); feedbackText = sprintf('平均反应时: %.0f ms\\n正确率: %.1f%%', meanRT, meanAcc*100); DrawFormattedText(window, feedbackText, 'center', 'center', textColor); Screen('Flip', window); KbStrokeWait;` |
| 10 | Data saving | `respMat(:, trial) = [wordNum, colorNum, response, rt, isiDuration]` | `dataMat(trial,:) = [rt, correctness]` + 每 trial 调用 `writematrix` | `fopen`/`fprintf`/`fclose` 增量写入 |
| 11 | Cleanup | `sca` + `Priority(0)` + `ShowCursor` | 同 | `try/catch/sca` |
| 12 | Package | 单一 `.m` 文件 | 单一 `.m` 文件 | 主 `.m` 脚本（自包含）+ 可选 `conditions.xlsx` / `conditions.csv` + `data/` 子目录（自动创建） |

## Config YAML → MATLAB 代码详细映射

### `windows[]` → Trial 事件循环

| Config 字段 | PTB 代码模板 |
|------------|------------|
| `windows[].content: "{col}"` | 根据 stimulus 类型: `DrawFormattedText` / `Screen('DrawTextures')` / `Screen('DrawDots')` / `Screen('FillRect')` |
| `windows[].duration: N` (固定) | `nFrames = round(N/1000 / ifi); for f=1:nFrames; drawStim(); vbl=Screen('Flip',w,vbl+(wf-0.5)*ifi); end` |
| `windows[].duration: [min, max]` (随机) | `randDur = randi([min, max]); randFrames = round(randDur/1000 / ifi)` |
| `windows[].response: [keys]` | `KbQueueFlush(); stimOnset=Screen('Flip',w); while ~gotResp && GetSecs<deadline; [pressed,firstPress]=KbQueueCheck(); ... end` |
| `windows[].rt_onset: "self"` | RT 起点 = `VBLTimestamp` (Flip 返回值) |

### `windows[]` 完整序列生成逻辑

```matlab
for trial = 1:numTrials
    KbQueueFlush();                    % 每 trial 清除旧事件
    vbl = Screen('Flip', window);      % 初始同步

    for w = 1:length(windows)
        win = windows(w);

        if isfield(win, 'response')
            % === 响应窗口 ===
            stimOnset = Screen('Flip', window);  % 或作为上一窗口的 Flip
            deadline = stimOnset + RESPONSE_DEADLINE/1000;

            gotResponse = false;
            while ~gotResponse && GetSecs < deadline
                [pressed, firstPress] = KbQueueCheck();
                if pressed
                    keyIdx = find(firstPress > 0);
                    rt = (min(firstPress(keyIdx)) - stimOnset) * 1000;  % ms
                    response = KbName(find(firstPress == min(firstPress(keyIdx)), 1));
                    gotResponse = true;
                end
                % 可选: 在响应窗口持续重绘刺激
                checkEscape();
            end

        elseif isfield(win, 'duration')
            % === 固定/随机时长窗口 ===
            nFrames = win.durationFrames;
            for f = 1:nFrames
                drawStimulus(win);     % 每次 Flip 前重绘
                vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
                checkEscape();
            end
        end
    end
end
```

### `blocks[]` → 条件加载

```matlab
% 从 xlsx/csv 文件加载条件
condTable = readtable('conditions.xlsx');
condData = table2array(condTable);
numTrials = size(condData, 1);

% 随机化
trialOrder = Shuffle(1:numTrials);

% 每 trial 获取条件
for t = 1:numTrials
    trialIdx = trialOrder(t);
    word = condData{trialIdx, 1};
    color = condData{trialIdx, 2};
    corrAns = condData{trialIdx, 3};
end
```

**代码内条件生成**（备选，无需外部文件）:
```matlab
% Config: blocks[].conditions = [{word:'RED',color:'red',correct:'left'}, ...]
% 生成因子设计矩阵
wordList = {'Red', 'Green', 'Blue'};
rgbColors = [1 0 0; 0 1 0; 0 0 1];
condBase = [sort(repmat([1 2 3], 1, 3)); repmat([1 2 3], 1, 3)];
condMatrix = repmat(condBase, 1, nReps);
trialOrder = Shuffle(1:size(condMatrix, 2));
condShuffled = condMatrix(:, trialOrder);
```

### `response_rules` → 正确性判断

```matlab
% Config: response_rules.correct = "response == corr_ans"
% 生成:
if strcmp(response, corrAns)
    correct = 1;
else
    correct = 0;
end

% 无响应处理
if ~gotResponse
    response = 'none';
    if strcmp(corrAns, 'none')  % no-go trial
        correct = 1;
    else
        correct = 0;
    end
end
```

### `response_rules.mapping` → 按键映射

```matlab
% Config: response_rules.mapping = {leftKey: "Red", downKey: "Green", rightKey: "Blue"}
% 生成:
leftKey = KbName('LeftArrow');
downKey = KbName('DownArrow');
rightKey = KbName('RightArrow');
escapeKey = KbName('ESCAPE');

% 在 KbQueue 回调中:
if pressed
    idx = find(firstPress > 0, 1);
    if idx == leftKey
        response = 1;    % 映射到条件值
    elseif idx == downKey
        response = 2;
    elseif idx == rightKey
        response = 3;
    end
end
```

### `display` → 屏幕参数

```matlab
% Config: display = {resolution: [1920, 1080], color: [128, 128, 128], fullscreen: true}
% 生成:
PsychDefaultSetup(2);
Screen('Preference', 'SkipSyncTests', 0);     % 生产环境必须为 0
screenNumber = max(Screen('Screens'));
white = WhiteIndex(screenNumber);
grey = white / 2;                              % 对应 [128, 128, 128]
black = BlackIndex(screenNumber);

[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey, [], 32, 2);
ifi = Screen('GetFlipInterval', window);
[centerX, centerY] = RectCenter(windowRect);
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);
HideCursor(window);
```

### `font` → PTB 字体配置

```matlab
% Config: font = {name: "PingFang SC", size: 60}
Screen('TextFont', window, 'PingFang SC');
Screen('TextSize', window, 60);

% 中文文本
DrawFormattedText(window, double('你好'), 'center', 'center', textColor);
```

### `audio` → PsychPortAudio 配置

| Config 场景 | PTB 代码 |
|-------------|---------|
| 简单音效 | `InitializePsychSound(1); pa=PsychPortAudio('Open',[],2,2,freq,1); PsychPortAudio('FillBuffer',pa,data); PsychPortAudio('Start',pa,1)` |
| 精确视觉同步 | `PsychPortAudio('Start', pa, 1, nextFlipTime, 0)` |
| 多音效预加载 | `buf1=PsychPortAudio('CreateBuffer',pa,data1); buf2=...; PsychPortAudio('UseSchedule',pa,1,n); PsychPortAudio('AddToSchedule',pa,buf1,1)` |
| 实验结束时清理 | `PsychPortAudio('Close', pa)` |

### `output` → 数据保存

```matlab
% Config: output = {filename: "data/sub-{subject}_stroop.csv", format: csv}
dataDir = fullfile(pwd, 'data');
if ~exist(dataDir, 'dir'), mkdir(dataDir); end
dataFile = fopen(fullfile(dataDir, ['sub-' subjectID '_stroop.csv']), 'w');
fprintf(dataFile, 'trial,condition,rt,response,correct\n');

for trial = 1:numTrials
    % ... 实验逻辑 ...
    fprintf(dataFile, '%d,%d,%.4f,%s,%d\n', trial, condition, rt, response, correct);
end

fclose(dataFile);
```

### `paradigm_config` → 范式特定逻辑

| 范式 | 关键逻辑 | PTB 实现 |
|------|---------|---------|
| SSD staircase (Stop-signal) | SSD 跟踪 | `ssd = startSSD; if prevTrial.correct; ssd = ssd + stepSize; else ssd = ssd - stepSize; end` |
| n-back match | 环缓冲区 | `buffer = circshift(buffer, 1); buffer(1) = currentStim; isMatch = buffer(1) == buffer(n+1)` |
| Lure detection | 非目标干扰 | `isLure = stimAppearedBefore && ~isTarget` |

## 两个范式的 PTB API 使用差异

| API / 模式 | Stroop | Posner Cuing | 生产推荐 |
|-----------|--------|-------------|---------|
| 窗口打开 | `PsychImaging('OpenWindow', ..., grey, [], 32, 2)` | `PsychImaging('OpenWindow', ..., grey, [])` | 指定 `32, 2`（32位色深+双缓冲） |
| 响应收集 | `KbCheck` 在绘制+Flip 循环内 | `KbCheck` 在独立轮询循环内 | `KbQueueCreate`+`KbQueueCheck`（更高精度） |
| RT 计时 | `vbl - iEnd`（Flip 时间戳差） | `endResp - startResp`（GetSecs 书夹） | `firstPress - VBLTimestamp` |
| 刺激呈现 | 每帧 Flip 时重绘 | `for i=1:nFrames` 每帧重绘+Flip | for 循环更清晰、更灵活 |
| 帧时长控制 | `waitframes` 参数单次 Flip | `for i=1:nFrames` 循环 Flip | for 循环更灵活（支持帧内逻辑） |
| 数据保存 | `respMat` 矩阵（workspace 内） | `writematrix` 每 trial 写文件 | 增量 `fprintf` + `fclose`（崩溃安全） |
| Escape 处理 | `if keyCode(escapeKey); ShowCursor; sca; return; end` | 同 | KbCheck 检查 + `try/catch/sca` |
| 刺激预加载 | 无纹理 | `CreateProceduralGabor` 循环前创建 | 所有纹理/参数在循环前准备完毕 |
| Blend 函数切换 | 不切换 | Gabor 期切换为 `GL_ONE/GL_ZERO` | 非默认 blend 后记得恢复 |
| SkipSyncTests | 不跳过 | `Screen('Preference', 'SkipSyncTests', 2)` | 生产环境必须设为 0 |
| 音频 | 无 | 无 | `PsychPortAudio` (若需要) |

## 窗口事件的 PTB 帧循环模式

### 模式 1：单帧 Flip（简单固定时长）

```matlab
% 一次 Flip 维持 N 帧 — 仅适用于无需帧内逻辑的静态刺激
Screen('DrawDots', window, [xCenter; yCenter], 10, black, [], 2);
vbl = Screen('Flip', window, vbl + ((isiTimeFrames - 1) - 0.5) * ifi);
```

适用：固定时长的静态刺激（注视点、空白屏、ISI）

### 模式 2：for 循环 Flip（帧精确控制）

```matlab
% 每帧显式 Flip — 需要帧精确控制或每帧更新内容
for f = 1:nFrames
    % 重绘（支持动画/动态内容）
    Screen('DrawDots', window, dotPositions(:, f), dotSizePix, dotColor, [], 2);
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
end
```

适用：需要每帧更新内容（动画）、需要显式控制帧数

### 模式 3：KbQueue 响应循环（生产推荐）

```matlab
% 持续重绘刺激 + KbQueue 轮询
KbQueueFlush();
stimOnset = Screen('Flip', window);           % VBLTimestamp 作为 RT 起点
deadline = stimOnset + RESPONSE_DEADLINE/1000;

gotResponse = false;
while ~gotResponse && GetSecs < deadline
    % 持续重绘刺激
    DrawFormattedText(window, stimulusText, 'center', 'center', stimColor);
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    [pressed, firstPress] = KbQueueCheck();
    if pressed
        keyIdx = find(firstPress > 0);
        rt = (min(firstPress(keyIdx)) - stimOnset) * 1000;
        gotResponse = true;
    end

    % Escape 检查
    [~, ~, keyCode] = KbCheck;
    if keyCode(KbName('ESCAPE'))
        save_and_quit();
    end
end
```

适用：刺激持续呈现直到按键的响应窗口 — 所有需要 RT 的范式

## 时序示意图

### Stroop 窗口序列
```
┌──────────┐  ┌──────────────────┐  ┌──────────────────────────────┐
│ Fixation │  │   ISI (1s)       │  │  Stimulus + Response         │
│ (1 frame)│  │   "请说出墨色"     │  │  "Red" (蓝色字) → RightArrow │
│    ●     │  │       ●          │  │  直到按键                     │
└──────────┘  └──────────────────┘  └──────────────────────────────┘
     vbl          iStart  →  iEnd        VBLTimestamp → firstPress - VBLTimestamp = RT
```

### Posner 窗口序列
```
┌───────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐ ┌──────────┐ ┌──────┐
│ Fixation  │ │  Cue     │ │  Gap     │ │   Target      │ │ Response │ │ ITI  │
│ 0.5s      │ │  0.15s   │ │  0.3s    │ │   0.15s       │ │  until   │ │ 0.2s │
│    ●      │ │  □  ●    │ │     ●    │ │  Gabor  ●     │ │  key     │ │      │
└───────────┘ └──────────┘ └──────────┘ └───────────────┘ └──────────┘ └──────┘
  nFrames       nFrames      nFrames      nFrames+         KbQueue        nFrames
  for loop      for loop     for loop     blend switch      Check          for loop
```

## 反模式速查（Config→Code 生成特化）

> 通用 API 反模式见 [spec/README.md](../spec/README.md#11-反模式速查表)。

| 禁止的 API / 模式 | 原因 | 替代方案 |
|-----------|------|------|
| `imread` / `MakeTexture` 在 trial 循环内 | 帧丢失 — 条件文件的图片路径应预加载为纹理 | 循环前预创建所有纹理 |
| KbQueue `Create`/`Start` 在 trial 循环内 | 事件丢失风险 — KbQueue 生命周期应映射到实验级而非 trial 级 | 循环前一次 `Create`+`Start`, trial 内只 `Flush` |
| 不用 `KbQueueFlush()` 每 trial | 前 trial 残留污染 RT — 每个 trial 的 KbQueue 状态应独立 | 每 trial 开头 `KbQueueFlush()` |
