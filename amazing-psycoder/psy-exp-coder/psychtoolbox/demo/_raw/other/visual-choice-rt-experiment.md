# 视觉选择反应时实验 — 完整 PTB 实验模板

> 来源: 蒋挺老师知乎 PTB 教程 §5  
> 归类: `demo/_raw/other/` — L4 完整实验参考
> 参考层级: L4 demo（仅参考实验逻辑，API 模式以 spec/README.md Canonical Skeleton 为准）

## 实验逻辑

- **任务**: 红、绿两色光斑随机出现在左/中/右三个位置，按键判断颜色
- **试次结构**: ITI(1s) → 刺激(0.5s内有响应窗口) → 反馈音 → 数据保存
- **条件**: 2(颜色) × 3(位置) = 6 种，拉丁方平衡
- **输出**: `.mat` 结构体数组，含 flipTime / rt / color / xpos / pressedKey

## 原始代码

```matlab
% 视觉选择反应时实验 (Visual Choice RT Experiment)
% 蒋挺老师知乎 PTB 教程 §5

close all; clear; sca;

% ============================================================
% 实验参数
% ============================================================
expParams.screenNum = 0;
expParams.fullscreen = 1;
expParams.monitorHz = 60;
expParams.trialsPerBlock = 40;
expParams.ITI = 1.0;                % 试次间间隔（秒）
expParams.stimDur = 0.5;            % 刺激持续时间（秒）
expParams.validKeys = [32, 38];     % 空格键和上箭头键

% 生成试次序列（2颜色 × 3位置 × 重复）
colors = [1, 2];                    % 1=红色[255,0,0], 2=绿色[0,255,0]
positions = [-400, 0, 400];         % X坐标（像素），Y=0居中
trialList = [];
for c = 1:length(colors)
    for p = 1:length(positions)
        trialList = [trialList; colors(c), positions(p)];
    end
end
trialList = repmat(trialList, expParams.trialsPerBlock / size(trialList,1), 1);
trialList = trialList(randperm(size(trialList,1)), :);  % 随机打乱

% ============================================================
% 窗口初始化
% ============================================================
PsychDefaultSetup(2);
Screen('Preference', 'SkipSyncTests', 0);

[windowPtr, windowRect] = Screen('OpenWindow', expParams.screenNum, [0 0 0], ...
    [], [], [], [], 2);  % 双缓冲
Screen('BlendFunction', windowPtr, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');
ifi = Screen('GetFlipInterval', windowPtr);
[centerX, centerY] = RectCenter(windowRect);
HideCursor;
Priority(MaxPriority(windowPtr));

% ============================================================
% 颜色辅助函数
% ============================================================
function rgb = GetColorFromList(colorID)
    if colorID == 1
        rgb = [255, 0, 0];    % 红色
    elseif colorID == 2
        rgb = [0, 255, 0];    % 绿色
    else
        rgb = [255, 255, 255];
    end
end

function rect = MakeRectFromCenter(cx, cy, w, h)
    rect = [cx-w/2, cy-h/2, cx+w/2, cy+h/2];
end

% ============================================================
% 主实验循环
% ============================================================
data = struct([]);

for t = 1:expParams.trialsPerBlock
    currentColor = trialList(t, 1);
    currentX = trialList(t, 2);
    currentY = 0;

    % --- ITI ---
    vbl = Screen('Flip', windowPtr);  % 清屏
    WaitSecs(expParams.ITI);

    % --- 绘制刺激 ---
    Screen('FillOval', windowPtr, GetColorFromList(currentColor), ...
        MakeRectFromCenter(currentX, currentY, 50, 50));

    % --- Flip + 时间戳记录 ---
    stimOnset = Screen('Flip', windowPtr);  % 返回实际翻转时刻

    % --- 响应收集（非阻塞轮询） ---
    responseDetected = false;
    responseKey = NaN;
    rt = NaN;

    deadline = stimOnset + expParams.stimDur;
    while (GetSecs < deadline) && ~responseDetected
        [keyIsDown, ~, keyCodes] = KbCheck;
        if keyIsDown
            if any(ismember(keyCodes, expParams.validKeys))
                rt = (GetSecs - stimOnset) * 1000;  % 转换为毫秒
                responseKey = find(keyCodes, 1);
                responseDetected = true;
            end
        end
    end

    % --- 数据记录 ---
    data(t).stimOnset = stimOnset;
    data(t).rt = rt;
    data(t).color = currentColor;
    data(t).xpos = currentX;
    data(t).responseKey = responseKey;
end

% ============================================================
% 保存与清理
% ============================================================
save('ExpData_Subj01.mat', 'data');
sca;
Priority(0);
ShowCursor;

% ============================================================
% 数据预处理示例
% ============================================================
% load('ExpData_Subj01.mat');
% validRTs = [data(:).rt];
% validRTs = validRTs(~isnan(validRTs) & validRTs > 100 & validRTs < 2000);
% fprintf('平均反应时: %.2f ms ± %.2f ms\n', mean(validRTs), std(validRTs));
```

## 反模式标注

| 问题 | 位置 | 规范替代（spec Canonical Skeleton） |
|------|------|-------------------------------------|
| `WaitSecs(expParams.ITI)` 阻塞 | ITI 阶段 | 帧循环 `for f=1:nFrames; Screen('Flip',w,vbl+(wf-0.5)*ifi); end` |
| `KbCheck` 轮询而非 `KbQueueCheck` | 响应收集 | `KbQueueCreate` + `KbQueueCheck` + `firstPress - VBLTimestamp` |
| `GetSecs - stimOnset` 手动计算 RT | RT 计算 | `firstPress(keyIdx) - VBLTimestamp`（KbQueue 自动时间戳） |
| `save()` 实验结束后一次性保存 | 数据保存 | `fopen`/`fprintf` 每试次增量写入 |
| 无 `try-catch` | 全局 | 必须包裹 |
| 反馈音 `PlaySound` 未实现 | 反馈阶段 | 使用 `PsychPortAudio` 预加载 + 异步播放 |

## 实验逻辑要点（可用于 Programming 层范式设计）

- 2(颜色) × 3(位置) 因子设计，拉丁方平衡
- 刺激持续时间固定 500ms，内有响应窗口
- 数据结构: struct 数组 → `.mat` 保存
- 异常 RT 剔除: < 100ms 或 > 2000ms
