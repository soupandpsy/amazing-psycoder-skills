# 视觉识别实验 — 鼠标空间反应 + 多区组自适应学习

> 来源: [Matt Jones, University of Colorado](http://matt.colorado.edu/teaching/exptworkshop/example/main.m)  
> 参考层级: L4 demo（仅参考实验逻辑 — 鼠标反应、自适应区组、反馈显示）

## 实验逻辑

- **任务**: 看到蜥蜴图片，用鼠标点击 9 个圆形反应区之一，指出它生活在哪
- **刺激**: 9 种蜥蜴图片（`stimuli/lizard1.jpg` ~ `lizard9.jpg`）
- **反应**: 9 个圆形区域均匀环绕刺激排列，鼠标点击
- **区组**: 36 试次/区组，错误 ≤ 2 个则实验结束（自适应学习标准）
- **反馈**: 正确=绿色，错误=红色→显示正确答案
- **数据**: 按被试独立保存 `.mat` + 合并到总数据文件 `dataMaster_*.mat`

## 原始代码（main.m，241 行）

```matlab
function main
%Matt Jones, Dec 20
%Visual identification experiment with spatial (mouse) response
%Some older parts of this code were inherited from Todd Maddox

clear global
rng('shuffle')

global data blockLength errorThreshold window screenRect
global W H stimWidth responseSize stimrect respRadius respBox respX respY
global white brown green red bground
global instrSize respSize
global wrongTime demoIti iti FBtime postInstrTime
global stimuli

%parameters for experiment duration
blockLength = 36;
errorThreshold = 2;

%Timing parameters
iti = .25;
FBtime = .4;
wrongDelay = .05;
wrongTime = .2;
demoIti = .4;
postInstrTime = .5;

%Set up data structure
data = struct('version', '12/9/13');
data.computer = machineID;
if setup == -1
    disp 'Experiment Canceled'
    return
end

%Load stimulus image files
stimuli = cell(9,1);
for i=1:9
    imfile = ['stimuli/lizard' num2str(i) '.jpg'];
    stimuli{i} = imread(imfile);
end

%Set up psychtoolbox and graphics
[window, screenRect] = Screen('OpenWindow',0);
W = screenRect(3);
H = screenRect(4);
Screen('TextFont', window, 'Verdana');

%Graphical parameters
stimWidth = W/15;
respSize = stimWidth/2;
respRadius = respSize*5;
responseSize = 30;
instrSize = 18;

%Colors
white = [250 250 250];
brown = [50 30 10];
red = [150 25 25];
green = [25 150 25];
bground = [0 0 0];

%Compute stimulus and response locations
ratio = size(stimuli{1},1)/size(stimuli{1},2);
stimrect = [W/2-floor(stimWidth/2), H/2-floor(stimWidth*ratio/2), W/2+ceil(stimWidth/2), H/2+ceil(stimWidth*ratio/2)];
respX = W/2 + respRadius*sin(2*pi*(0:8)/9);
respY = H/2 - respRadius*cos(2*pi*(0:8)/9);
respBox = [respX'-respSize,respY'-respSize,respX'+respSize,respY'+respSize];

%Text for display
Screen('TextSize',window,responseSize);
prompt = 'Where does this lizard live?';
[promptWidth,~] = Screen('DrawText',window,prompt,0,0);
wrong = 'Wrong';
[wrongWidth,~] = Screen('DrawText',window,wrong,0,0);
right = 'Correct';
[rightWidth,~] = Screen('DrawText',window,right,0,0);

HideCursor

if instruct(1) == -1
    abort
    return
end

if demo == -1;
    abort
    return
end

if instruct(2) == -1
    abort
    return
end

%Main task
passed = 0;
while(~passed)
    blockStim = mod(randperm(blockLength)',9)+1;
    data.stim = [data.stim;blockStim];
    blockResp = zeros(blockLength,1);
    blockRT = zeros(blockLength,1);
    Screen(window,'TextSize',responseSize);
    
    for trial = 1:blockLength
        %ITI with response regions visible
        Screen('FillRect',window,bground);
        for r = 1:9
            Screen('FillOval',window,brown,respBox(r,:));
        end
        Screen('Flip',window);
        WaitSecs(iti);
        
        %Stimulus presentation
        Screen('FillRect',window,bground);
        Screen('DrawText',window,prompt,W/2-promptWidth/2,responseSize*1.5,white);
        Screen('PutImage', window, stimuli{blockStim(trial)}, stimrect);
        for r = 1:9
            Screen('FillOval',window,brown,respBox(r,:));
        end
        SetMouse(W/2,H/2,window);
        Screen('Flip',window);
        
        %Get response
        ShowCursor;
        x = getResp;
        if x(1) == -1
            data.aborted = 1;
            passed = 1;
            break
        end
        blockResp(trial) = x(1);
        blockRT(trial) = x(2);
        
        %Feedback
        HideCursor
        Screen('FillRect',window,bground);
        Screen('DrawText',window,prompt,W/2-promptWidth/2,responseSize*1.5,white);
        Screen('PutImage', window, stimuli{blockStim(trial)}, stimrect);
        for r = 1:9
            Screen('FillOval',window,brown,respBox(r,:));
        end
        if blockResp(trial)==data.map(blockStim(trial))
            Screen('FillOval',window,green,respBox(blockResp(trial),:));
            Screen('DrawText',window,right,W/2-rightWidth/2,H-responseSize*2,green);
            Screen('Flip',window);
            WaitSecs(FBtime);
        else
            Screen('FillOval',window,red,respBox(blockResp(trial),:));
            Screen('DrawText',window,wrong,W/2-wrongWidth/2,H-responseSize*2,red);
            Screen('Flip',window);
            WaitSecs(wrongDelay);
            Screen('FillRect',window,bground);
            Screen('DrawText',window,prompt,W/2-promptWidth/2,responseSize*1.5,white);
            Screen('PutImage', window, stimuli{blockStim(trial)}, stimrect);
            for r = 1:9
                Screen('FillOval',window,brown,respBox(r,:));
            end
            Screen('FillOval',window,red,respBox(blockResp(trial),:));
            Screen('DrawText',window,wrong,W/2-wrongWidth/2,H-responseSize*2,red);
            Screen('FillOval',window,green,respBox(data.map(blockStim(trial)),:));
            Screen('Flip',window);
            WaitSecs(FBtime-wrongDelay);
        end
    end
    
    data.resp = [data.resp;blockResp];
    data.RT = [data.RT;blockRT];
    
    if data.aborted==0
        errors = sum(blockResp~=data.map(blockStim));
        if errors <= errorThreshold
            passed=1;
        else
            if instruct(3,errors) == -1
                data.aborted=1;
                passed=1;
            end
        end
    end
end

data.elapsedTime = (clock-data.dateTime)*[0;0;1440;60;1;1/60];

%Write data
if ~isdir('data')
    mkdir('data');
end
indFile = ['data',num2str(data.sub),'_',machineID];
a = what('data');
foundMaster = 0;
foundInd = 0;
for i=1:length(a.mat)
    if isequal(a.mat{i},['dataMaster_',machineID,'.mat'])
        foundMaster=1;
    end
    if isequal(a.mat{i},[indFile,'.mat'])
        foundInd=1;
    end
end
if foundInd
    suffix = num2str(rand);
    save(['data/',indFile,'-',suffix(3:6)],'data');
else save(['data/',indFile],'data');
end
if foundMaster
    load(['data/dataMaster_',machineID]);
    eval(['dataMaster_',machineID,' = [dataMaster_',machineID,' data];']);
else eval(['dataMaster_',machineID,' = data;']);
end
save(['data/dataMaster_',machineID],['dataMaster_',machineID]);
disp('Data have been saved.');
disp(' ');

if data.aborted==0
    instruct(4,errors);
    getPasswd(300)
end
ShowCursor;
Screen('CloseAll');
home
end

function abort
ShowCursor;
Screen('CloseAll');
disp('Experiment aborted by escape sequence')
end
```

## 反模式标注

| 问题 | 位置 | 规范替代 |
|------|------|---------|
| 全局变量 `global` | 文件顶部 | 结构体传参或嵌套函数闭包 |
| `WaitSecs` 多处 | ITI、反馈 | 帧循环定时 |
| `Screen('PutImage')` 而非 `MakeTexture` 预加载 | 试次循环 | 循环前 `Screen('MakeTexture')` 预处理所有纹理 |
| 依赖外部文件 `setup.m`, `instruct.m`, `demo.m`, `getResp.m` | 多处 | 自包含单文件 |
| `Screen('CloseAll')` | 清理 | `sca` |
| 无 `try-catch` | 全局 | 必须包裹 |
| `save()` 块结束后保存 | 数据保存 | 增量写入每试次 |
| 鼠标 RT 来源不透明 | `getResp` 函数 | 需确认 RT 基于 `GetSecs` 还是 `VBLTimestamp` |

## 实验逻辑要点（可用于 Programming 层范式设计）

- **刺激-反应映射**: 9 个蜥蜴图片 → 9 个空间位置（圆形排列，`2π/9` 弧度间隔）
- **自适应区组**: 每区组 36 试次，错误 ≤ 2 即通过
- **反馈设计**: 正确=绿色高亮+文字，错误=红色高亮→短暂延迟→显示正确答案
- **错误反馈分两阶段**: 先红色闪烁 50ms → 切换为绿色正确答案
- **数据合并**: 独立文件 + 总合文件双写，防止重复被试号（加随机后缀）
