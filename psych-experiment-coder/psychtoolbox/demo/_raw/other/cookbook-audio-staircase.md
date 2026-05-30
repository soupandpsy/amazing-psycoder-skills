# 听觉楼梯实验 — KbQueue + PsychPortAudio 同步

> 来源: [PTB Cookbook: Simple Experiment 4](https://github.com/Psychtoolbox-3/Psychtoolbox-3/wiki/Cookbook:-simple-experiment-4)  
> 作者: Aaron Seitz (2012)  
> 参考层级: L4 demo（仅参考音频同步 + 楼梯算法 + KbQueue RT 模式）

## 实验逻辑

40 试次听觉检测楼梯实验：
- 刺激: 牛叫声（强度由楼梯控制）
- 任务: 听到声音就按键
- 楼梯规则: 3-down 法则，连续 3 次正确 → 声音强度降低
- 数据: 每试次保存当前楼梯阈值

## 原始代码

```matlab
% SampleExperiment.m
%
% shows a simple experiment, press a key whenever you see or hear a
% cow...instructions to the subject are an excercise to the user ;-).
% runs a staircase
%
% written for Psychtoolbox 3  by Aaron Seitz 1/2012

%% Example Experiment
% Gets subject Info sets up experiment
prompt = {'Enter subject number:'};
defaults = {''};
answer = inputdlg(prompt, 'Subject Number',1.2,defaults);
SUBJECT = answer{1,:};

c = clock;
baseName=[SUBJECT '_DemoExp_' num2str(c(2)) '_' num2str(c(3)) '_' num2str(c(4)) '_' num2str(c(5))];
rand('seed',GetSecs);

% Opens Sets up Psychtoolbox
[window, rect]=Screen('OpenWindow',0);
FlipInt=Screen('GetFlipInterval',window);
ListenChar(-1);
HideCursor();
KbName('UnifyKeyNames');
KbQueueCreate;
KbQueueStart;

[wavedata freq] = wavread('./cow.wav');
TheSnd=[wavedata wavedata];
InitializePsychSound(1);
pahandle = PsychPortAudio('Open', [], [], 2, freq, 2, 0);

vbl=Screen('Flip',window);

%staircase parameters
numdown=3;
stepsize=-.01;
thresh=.3;
CorCounter=0;

for trial=1:40
    starttime=vbl +round((3*rand + 1)/FlipInt)*FlipInt

    PsychPortAudio('FillBuffer', pahandle, thresh*TheSnd');
    PsychPortAudio('Start', pahandle,1,inf);
    PsychPortAudio('RescheduleStart', pahandle, starttime, 0)
    vbl=Screen('Flip',window,starttime-FlipInt/2);
    KbQueueFlush;
    Waitsecs(.5);
    if KbQueueCheck
        CorCounter = CorCounter+1;
    else
        CorCounter=0;
    end
    threshhist(trial)=thresh;
    if CorCounter>=numdown
        thresh=thresh+stepsize;
    else
        thresh=thresh-stepsize;
    end
    thresh=max(thresh,0);
    thresh=min(thresh,1);
    save(baseName)
end
ListenChar(0);
ShowCursor();
Screen('CloseAll');
Priority(0);
KbQueueRelease;
ListenChar(0);
PsychPortAudio('Close');
```

## 反模式标注

| 问题 | 位置 | 规范替代 |
|------|------|---------|
| `Waitsecs(.5)` 等待反应 | 反应窗口 | 帧循环 + `GetSecs` 超时检测 |
| `KbQueueCheck` 未读取 `firstPress` 时间戳 | 反应收集 | `[pressed, firstPress]=KbQueueCheck` → 提取 RT |
| `save(baseName)` 每试次全量保存 | 数据保存 | 追加式写入（`fprintf` + `fclose`） |
| `Screen('CloseAll')` | 清理 | `sca` |
| 无 `try-catch` | 全局 | 必须包裹 |
| `wavread` 已废弃 | 音频加载 | `audioread` (R2015b+) |

## 关键 API 模式（符合 spec 规范的部分）

```matlab
% PsychPortAudio 精确调度：先 FillBuffer + Start(inf) → 再 RescheduleStart 对齐 Flip
PsychPortAudio('FillBuffer', pahandle, audioData);
PsychPortAudio('Start', pahandle, 1, inf);          % 无限循环等待调度
PsychPortAudio('RescheduleStart', pahandle, targetTime, 0);  % 对齐到 Flip 时刻

% 刺激 onset 半帧提前 Flip
vbl = Screen('Flip', window, starttime - FlipInt/2);
KbQueueFlush;  % 清空 Flip 前的按键缓冲
```

## 楼梯算法逻辑（可用于范式设计）

```
3-down 法则:
  if 连续正确 >= 3:
      阈值降低（难度增加）
  else:
      阈值升高（难度降低）

约束: 阈值 ∈ [0, 1]
```
