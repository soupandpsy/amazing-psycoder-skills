# KbQueue 按键反应时 + 超时处理示例

> 来源: [PTB Cookbook: Response Example 2](https://github.com/Psychtoolbox-3/Psychtoolbox-3/wiki/Cookbook%3A-response-example-2)  
> 作者: Aaron Seitz (2012)  
> 参考层级: L4 demo（仅参考 KbQueueCheck + firstPress RT 模式）

## 实验逻辑

5 试次演示：随机颜色纹理 → 按键反应（0.5s 超时）→ 反馈 RT + 按键名

## 原始代码

```matlab
% Example 2 - Shows which key was pressed and timeouts after .5 seconds
% written for Psychtoolbox 3  by Aaron Seitz 1/2012

[window, rect]=Screen('OpenWindow',0);  % open screen
ListenChar(-1); %makes it so characters typed don't show up in the command window
HideCursor(); %hides the cursor

KbName('UnifyKeyNames'); %used for cross-platform compatibility of keynaming
KbQueueCreate; %creates cue using defaults
KbQueueStart;  %starts the cue

for trial=1:5 %runs 5 trials
    IM1=rand(100,100,3)*255; %creates random colored image
    tex(1) = Screen('MakeTexture', window, IM1); %makes texture
    Screen('DrawTexture', window, tex(1), []); %draws to backbuffer
    WaitSecs(rand+.5) %jitters prestim interval between .5 and 1.5 seconds

    starttime=Screen('Flip',window); %swaps backbuffer to frontbuffer
    KbQueueFlush; %Flushes Buffer so only response after stimonset are recorded
    Waitsecs(.5);  %gives .5 secs for a response

    [ pressed, firstPress]=KbQueueCheck; %  check if any key was pressed.

    if pressed %if key was pressed do the following
        firstPress(find(firstPress==0))=NaN; %little trick to get rid of 0s
        [endtime Index]=min(firstPress); % gets the RT of the first key-press and its ID
        thekeys=KbName(Index); %converts KeyID to keyname
        RTtext=sprintf('Response Time =%1.2f secs with %s-key',endtime-starttime,thekeys); %makes feedback string
    else
        RTtext=sprintf('Sorry, too slow!'); %makes feedback string
    end
    DrawFormattedText(window,RTtext,'center'  ,'center',[255 0 255]); %shows RT
    vbl=Screen('Flip',window); %swaps backbuffer to frontbuffer
    Screen('Flip',window,vbl+1); %erases feedback after 1 second
end

ListenChar(0); %makes it so characters typed do show up in the command window
ShowCursor(); %shows the cursor
Screen('CloseAll'); %Closes Screen
```

## 反模式标注

| 问题 | 位置 | 规范替代 |
|------|------|---------|
| `Waitsecs(.5)` 等待反应 | 反应窗口 | 应使用帧循环 + `GetSecs` 超时检测 |
| `Screen('CloseAll')` | 清理 | `sca` |
| 无 `try-catch` | 全局 | 必须包裹 |
| 无 `Priority(0)` + `KbQueueRelease` | 清理 | 恢复优先级 + 释放键盘队列 |
| `MakeTexture` 在循环内创建 | 试次循环 | 应预加载到循环外 |

## 关键 API 模式（符合 spec 规范的部分）

```matlab
% RT = 按键首次按下时间 - 刺激呈现时间
KbQueueFlush;                         % 清空刺激呈现前的按键缓冲
starttime = Screen('Flip', window);   % 刺激呈现 onset
[ pressed, firstPress] = KbQueueCheck; % 获取按键事件
firstPress(find(firstPress==0)) = NaN;
[RT, keyIndex] = min(firstPress);     % RT = 首个按键时间
RT = RT - starttime;                  % 减去刺激 onset
```
