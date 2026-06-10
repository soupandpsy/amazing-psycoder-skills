# Oval

> Source: [oval](https://peterscarfe.com/oval.html)

Shows you how to draw a filled in oval

```matlab
% Clear the workspace and the screen
sca;
close all;
clear;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');

% Draw to the external screen if avaliable
screenNumber = max(screens);

% Define black and white
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);

% Set the blend funciton for the screen
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Make a base Rect of 200 by 250 pixels
baseRect = [0 0 200 250];

% For Ovals we set a miximum diameter up to which it is perfect for
maxDiameter = max(baseRect) * 1.01;

% Center the rectangle on the centre of the screen
centeredRect = CenterRectOnPointd(baseRect, xCenter, yCenter);

% Set the color of the rect to red
rectColor = [1 0 0];

% Draw the rect to the screen
Screen('FillOval', window, rectColor, centeredRect, maxDiameter);

% Flip to the screen
Screen('Flip', window);

% Wait for a key press
KbStrokeWait;

% Clear the screen
sca;

```
