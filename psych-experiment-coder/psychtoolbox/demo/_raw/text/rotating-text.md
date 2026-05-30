# Rotating Text

> Source: [rotatingText](https://peterscarfe.com/rotatingText.html)

In this demo we show you dynamically rotate text. PTB doesn't offer a direct way in which to rotate text using the "

```matlab
% Clear the workspace and the screen
close all;
clear;
sca

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');

% Select the external screen if it is present, else revert to the native
% screen
screenNumber = max(screens);

% Define black, white and grey
black = BlackIndex(screenNumber);
white = WhiteIndex(screenNumber);
grey = white / 2;

% Open an on screen window and color it grey
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Set the blend funciton for the screen
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the size of the on screen window in pixels
% For help see: Screen WindowSize?
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window in pixels
% For help see: help RectCenter
[xCenter, yCenter] = RectCenter(windowRect);

% Draw text in the middle of the screen. We just to this so that we can get
% the text bounds. These are the "dimensions" of the text as it would be
% drawn to the screen
Screen('TextSize', window, 80);
[~, ~, textBounds] = DrawFormattedText(window, 'Hello World', 'center', 'center', white);

% Over-write the screen in grey so that it is back to its original state
Screen('FillRect', window, grey);

% Make a rectangular texture to hold our text. This has the same background
% color to that of the screen. Note also, that we increase the size of the
% text bounds slightly and round upwards to the nearest pixel. This is to
% make sure the text fits in the texture and because texture dimensions can
% only be to interger pixels.
textureRect = ones(ceil((textBounds(4) - textBounds(2)) * 1.1),...
    ceil((textBounds(3) - textBounds(1)) * 1.1)) .* grey;
textTexture = Screen('MakeTexture', window, textureRect);

% Set the text size for this texture and then draw our text to the texture,
% just as if we were drawing it to the screen
Screen('TextSize', textTexture, 80);

% No draw our text, but here we draw it to a texture "pretending" that it is
% the screen
DrawFormattedText(textTexture, 'Hello World', 'center', 'center', white);

% Sync us and get a time stamp
vbl = Screen('Flip', window);
waitframes = 1;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Angular increment per frame, one rotation every 2 seconds
% (just an arbitary nice value)
anglePerFrame = 360 * ifi / 2;
currentAngle = 0;

% Animation loop
while ~KbCheck

    % Here we draw our texture to the screen. This texture contains our
    % predrawn text and allows us to rotate it easily.
    Screen('DrawTextures', window, textTexture, [], [], currentAngle);

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the angle
    currentAngle = currentAngle + anglePerFrame;

end

% Clear the screen
sca;

```
