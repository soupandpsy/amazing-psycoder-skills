# Psychtoolbox Implementation Guide

> **Status**: Layer 1 — API 规范、反模式表、强制模式。所有 PTB 实验代码必须遵守这些规则。
> **Last updated**: 2026-05-27 — 基于 psychtoolbox.org 官方文档全面修订

## Version Assumption

Default to **Psychtoolbox 3.0.21+** (March 2025) for MATLAB/Octave。

**重要版本变更**:
- 3.0.20+ (Dec 2024): Apple Silicon ARM 原生支持（beta）、macOS/Windows 需要付费许可证
- 3.0.21+ (Mar 2025): 强制付费订阅、系统级机器许可证、离线宽限期最长 120 天
- Linux 和 Raspberry Pi 永久免费
- 代码生成默认不依赖 3.0.21 专有特性 — 向下兼容至 3.0.19

## 1. 强制代码骨架

所有 PTB 实验必须从这个骨架开始：

```matlab
% 1. 设置
PsychDefaultSetup(2);                                  % 默认设置 + 统一键名
Screen('Preference', 'SkipSyncTests', 0);              % 生产环境必须跑同步测试
KbName('UnifyKeyNames');                               % 跨平台键名统一
rng('shuffle');                                        % 随机种子

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

        % 数据保存
        % fprintf(dataFile, ...);
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

### 1.1 Canonical Code Skeleton（生成代码必须以此为模板）

以下是完整的、可运行的最小实验骨架。**所有生成的 PTB 代码必须从这个骨架开始。** 它展示了每一个强制 API 模式的正确用法：

```matlab
% ============================================================
% Canonical PTB Experiment Skeleton
% 展示所有强制 API 模式：KbQueue、帧精确 timing、RT、增量保存、try/catch
% 修改下方参数区即可适配不同范式
% ============================================================
close all; clear; sca;

% ============================================================
% 可修改参数 — 所有可调参数集中在此
% ============================================================
subjectID = 'test';
sessionNum = 1;
screenNumber = max(Screen('Screens'));
backgroundColor = [128 128 128] / 255;  % grey
textColor = [0 0 0];
fontName = 'PingFang SC';  % macOS 中文；Windows 用 'Microsoft YaHei'
fontSize = 60;

% 时间参数 (秒)
fixationTime = 0.5;
stimulusTime = 1.0;
feedbackTime = 0.5;
responseDeadline = 2.0;
itiMin = 0.6;
itiMax = 0.9;

% 按键定义（必须 KbName('UnifyKeyNames') 后使用）
KbName('UnifyKeyNames');
keyLeft  = KbName('LeftArrow');
keyRight = KbName('RightArrow');
escapeKey = KbName('ESCAPE');
responseKeys = [keyLeft, keyRight];

% 条件定义
conditions = {
    'stim_a', 'left';
    'stim_b', 'right';
};
nReps = 10;
nTrials = size(conditions, 1) * nReps;

% 数据目录
dataDir = fullfile(pwd, 'data');
if ~exist(dataDir, 'dir'), mkdir(dataDir); end
dataFile = fullfile(dataDir, sprintf('sub-%s_task_%s.csv', subjectID, datestr(now, 'yyyymmdd_HHMM')));

% ============================================================
% 屏幕初始化
% ============================================================
PsychDefaultSetup(2);
Screen('Preference', 'SkipSyncTests', 0);
rng('shuffle');

[window, windowRect] = PsychImaging('OpenWindow', screenNumber, backgroundColor, [], 32, 2);
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');
Screen('TextFont', window, fontName);
Screen('TextSize', window, fontSize);

ifi = Screen('GetFlipInterval', window);
waitframes = 1;
[xCenter, yCenter] = RectCenter(windowRect);

topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);
HideCursor;

% ============================================================
% 刺激预加载（循环外）
% ============================================================
fixCross = [-20 20 0 0; 0 0 -20 20];  % 注视点十字坐标

% ============================================================
% KbQueue 初始化（循环前一次创建+启动）
% ============================================================
KbQueueCreate([], responseKeys);  % 只监听响应键
KbQueueStart;

% ============================================================
% 数据文件初始化
% ============================================================
fid = fopen(dataFile, 'w');
fprintf(fid, 'trial,condition,rt,response,correct\n');

% ============================================================
% 辅助函数
% ============================================================
    function saveTrial(fid, trial, cond, rt, resp, correct)
        fprintf(fid, '%d,%s,%.4f,%s,%d\n', trial, cond, rt, resp, correct);
    end

    function cleanup()
        KbQueueStop; KbQueueRelease;
        fclose('all');
        sca; Priority(0); ShowCursor;
    end

% ============================================================
% 主实验循环
% ============================================================
try
    vbl = Screen('Flip', window);  % 初始 Flip

    for trial = 1:nTrials
        % --- 每 trial 清除键盘队列 ---
        KbQueueFlush([], 2);  % 清除+等待（防残留）

        % === 注视点 (固定时长) ===
        Screen('DrawLines', window, fixCross, 3, textColor, [xCenter yCenter], 2);
        vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

        fixationFrames = round(fixationTime / ifi);
        for f = 1:fixationFrames - 1
            Screen('DrawLines', window, fixCross, 3, textColor, [xCenter yCenter], 2);
            vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
        end

        % === 刺激 + 响应窗口（KbQueueCheck 收集 RT）===
        cond = conditions{mod(trial-1, size(conditions,1)) + 1, 1};
        corrAns = conditions{mod(trial-1, size(conditions,1)) + 1, 2};

        DrawFormattedText(window, cond, 'center', 'center', textColor);
        vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
        stimOnset = vbl;  % VBLTimestamp = GPU 翻页时刻，RT 起点

        gotResponse = false;
        rt = NaN;
        response = '';
        deadline = stimOnset + responseDeadline;

        while ~gotResponse && GetSecs < deadline
            [pressed, firstPress] = KbQueueCheck;
            if pressed
                keyIdx = find(firstPress > 0);
                firstKey = keyIdx(1);
                rt = (firstPress(firstKey) - stimOnset) * 1000;  % ms

                if firstKey == keyLeft
                    response = 'left'; gotResponse = true;
                elseif firstKey == keyRight
                    response = 'right'; gotResponse = true;
                end
            end

            % Escape 检查（每帧）
            [~, ~, keyCode] = KbCheck;
            if keyCode(escapeKey)
                cleanup(); error('用户手动退出');
            end

            % 保持刺激显示
            DrawFormattedText(window, cond, 'center', 'center', textColor);
            vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
        end

        % --- 正确率判断 ---
        if ~gotResponse
            correct = strcmp(corrAns, 'none');  % no-go 正确不反应
            response = 'timeout';
        else
            correct = strcmp(response, corrAns);
        end

        % --- 增量保存 ---
        saveTrial(fid, trial, cond, rt, response, correct);

        % === ITI (随机时长) ===
        itiDuration = itiMin + rand * (itiMax - itiMin);
        itiFrames = round(itiDuration / ifi);
        for f = 1:itiFrames
            Screen('Flip', window);
            [~, ~, keyCode] = KbCheck;
            if keyCode(escapeKey)
                cleanup(); error('用户手动退出');
            end
        end
    end

    % --- 实验结束清理 ---
    cleanup();
    fprintf('数据已保存至: %s\n', dataFile);

catch ME
    cleanup();
    rethrow(ME);
end
```

**使用方式**：复制此骨架 → 修改参数区 → 在刺激+响应窗口内替换为你的范式逻辑 → 添加指导语/练习/Block 结构。不要改变 API 模式（KbQueue、Flip timing、RT 测量方式）。

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

**为什么减 0.5 * ifi**: `vbl + ifi` 是浮点计算，可能因舍入误差略超预期刷新时刻，导致 PTB 等待近一整帧。提前半帧 (`ifi/2`) 请求 flip 可保证发生在正确的刷新周期内，且留有足够安全裕度。

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
| `Screen('Flip')` 返回值 `vbl` | 实际翻页时间戳（GPU 完成时刻），所有计时以此为准 |
| `ifi` | 单帧时长（秒），从 `Screen('GetFlipInterval')` 获取 |
| `waitframes` | 必须为整数，`waitframes = round(seconds / ifi)` |
| `sca` | `Screen('CloseAll')` 的快捷方式 — 紧急清理 |
| `Priority(MaxPriority(window))` | 提升 MATLAB 进程优先级，减少帧丢失 |
| `Screen('DrawingFinished')` | 提示 PTB 当前帧绘制完成，可提前开始渲染 |

## 3. 键盘响应收集

> **完整示例**: [../demo/_raw/getting-started/keyboard-q.md](../demo/_raw/getting-started/keyboard-q.md) — KbQueue 创建、轮询、释放的完整 demo。

### 3.1 KbQueue 生命周期（强制规则）

**KbQueue 是唯一推荐的生产级响应收集方式。** 它在 PTB 的高优先级后台线程中运行，提供亚毫秒级时间戳精度。

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
| `KbQueueCheck` | **生产级 RT 收集** — 首选 | 需完整生命周期管理 |
| `KbStrokeWait` | 指令屏"按任意键继续" | 阻塞，不返回时间戳 |
| `KbCheck` | Escape 检测 | 不提供精确时间戳，**禁止用于 RT** |
| `KbWait` | — | **禁止** — 阻塞、不提供时间戳、无法 Escape |

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

PTB 的音频系统以 **PortAudio** 为基础，提供亚毫秒级延迟。

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

% 精确时间播放 — 与视觉 Flip 同步
nextFlip = Screen('Flip', window, ...);
PsychPortAudio('Start', pahandle, 1, nextFlip + 0.001);  % Flip 后 1ms
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
