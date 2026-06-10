# Basic Text

> Source: [basicText](https://peterscarfe.com/basicText.html)

This is a basic as it gets. Simply writes “Hello World” at three different screen positions, in three different colours, in three different fonts, with three different font sizes.

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

% Set the blend funciton for the screen
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the size of the on screen window in pixels
% For help see: Screen WindowSize?
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window in pixels
% For help see: help RectCenter
[xCenter, yCenter] = RectCenter(windowRect);

% Draw text in the upper portion of the screen with the default font in red
Screen('TextSize', window, 70);
DrawFormattedText(window, 'Hello World', 'center',...
    screenYpixels * 0.25, [1 0 0]);

% Draw text in the middle of the screen in Courier in white
Screen('TextSize', window, 80);
Screen('TextFont', window, 'Courier');
DrawFormattedText(window, 'Hello World', 'center', 'center', white);

% Draw text in the bottom of the screen in Times in blue
Screen('TextSize', window, 90);
Screen('TextFont', window, 'Times');
DrawFormattedText(window, 'Hello World', 'center',...
    screenYpixels * 0.75, [0 0 1]);

% Flip to the screen
Screen('Flip', window);

% Now we have drawn to the screen we wait for a keyboard button press (any
% key) to terminate the demo
KbStrokeWait;

% Clear the screen
sca;

```
