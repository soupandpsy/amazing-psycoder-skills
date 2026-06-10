# Contrast Rev Checkerboard

> Source: [contrastRevCheckerboard](https://peterscarfe.com/contrastRevCheckerboard.html)

Displays an animated radial checkerboard that reverses in contrast over time (this demo is a modified version of one coded by

```matlab
% Clear the workspace
close all;
clear;
sca;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');

% Draw to the external screen if avaliable
screenNumber = max(screens);

% Define black and white
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
grey = white / 2;

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber,...
    grey, [], 32, 2, [], [], kPsychNeed32BPCFloat);

% CBlend function
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Screen resolution in Y
screenYpix = windowRect(4);

% Number of white/black circle pairs
rcycles = 8;

% Number of white/black angular segment pairs (integer)
tcycles = 24;

% Now we make our checkerboard pattern
xylim = 2 * pi * rcycles;
[x, y] = meshgrid(-xylim: 2 * xylim / (screenYpix - 1): xylim,...
    -xylim: 2 * xylim / (screenYpix - 1): xylim);
at = atan2(y, x);
checks = ((1 + sign(sin(at * tcycles) + eps)...
    .* sign(sin(sqrt(x.^2 + y.^2)))) / 2) * (white - black) + black;
circle = x.^2 + y.^2 <= xylim^2;
checks = circle .* checks + grey * ~circle;

% Now we make this into a PTB texture
radialCheckerboardTexture(1)  = Screen('MakeTexture', window, checks);
radialCheckerboardTexture(2)  = Screen('MakeTexture', window, 1 - checks);

% Time we want to wait before reversing the contrast of the checkerboard
checkFlipTimeSecs = 2;
checkFlipTimeFrames = round(checkFlipTimeSecs / ifi);
frameCounter = 0;

% Time to wait in frames for a flip
waitframes = 1;

% Texture cue that determines which texture we will show
textureCue = [1 2];

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Sync us to the vertical retrace
vbl = Screen('Flip', window);

while ~KbCheck

    % Increment the counter
    frameCounter = frameCounter + 1;

    % Draw our texture to the screen
    Screen('DrawTexture', window, radialCheckerboardTexture(textureCue(1)));

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Reverse the texture cue to show the other polarity if the time is up
    if frameCounter == checkFlipTimeFrames
        textureCue = fliplr(textureCue);
        frameCounter = 0;
    end

end

% Clear up and leave the building
sca;

```
