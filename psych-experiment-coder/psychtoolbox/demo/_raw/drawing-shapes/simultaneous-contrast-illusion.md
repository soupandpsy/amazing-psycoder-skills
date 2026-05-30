# Simultaneous Contrast Illusion

> Source: [simultaneousContrast](https://peterscarfe.com/simultaneousContrast.html)

This demo builds on "Order Of Drawing Demo" by drawing a simple simultaneous contrast illusion. Here we draw all four of the squares in our illusion in a single line of code. 

```matlab
% Clear the workspace and the screen
sca;
close all;
clear;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers. This gives us a number for each of the screens
% attached to our computer.
screens = Screen('Screens');

% Draw we select the maximum of these numbers. So in a situation where we
% have two screens attached to our monitor we will draw to the external
% screen. When only one screen is attached to the monitor we will draw to
% this.
screenNumber = max(screens);

% Define black, white and grey
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
grey = white / 2;

% Open an on screen window and color it black
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey);

% Get the size of the on screen window in pixels
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window in pixels
[xCenter, yCenter] = RectCenter(windowRect);

% Make a base Rect of 1/2 screen Y dimension for the black and white
% background squares, and 1/6 for the front grey squares. This will produce
% a standard simultaneous contrast illustion where the two smaller grey
% sqaures, although the same luminance will appear different shades of grey
% due to being on different backgrounds. The one on the white background
% square will look darker then the one on the white background square.
backDim = screenYpixels / 2;
baseRectBack = [0 0 backDim backDim];

frontDim = screenYpixels / 6;
baseRectFront = [0 0 frontDim frontDim];

% Position the rectangles on the screen
backLeftRect = CenterRectOnPointd(baseRectBack,...
    xCenter - backDim / 2, yCenter);
backRightRect = CenterRectOnPointd(baseRectBack,...
    xCenter + backDim / 2, yCenter);

frontLeftRect = CenterRectOnPointd(baseRectFront,...
    xCenter - backDim / 2, yCenter);
frontRightRect = CenterRectOnPointd(baseRectFront,...
    xCenter + backDim / 2, yCenter);

% Make a marix of all the rect coordinates
allRects = [backLeftRect; backRightRect; frontLeftRect; frontRightRect]';

% We do the same of the colors of the rects. Put them in one matrix for
% drawing
allColors = [white white white; black black black;...
    grey grey grey; grey grey grey]';

% Draw all the rects in one line of code
Screen('FillRect', window, allColors, allRects);

% Flip to the screen. This command basically draws all of our previous
% commands onto the screen. See later demos in the animation section on more
% timing details. And how to demos in this section on how to draw multiple
% rects at once.
Screen('Flip', window);

% Now we have drawn to the screen we wait for a keyboard button press (any
% key) to terminate the demo.
KbStrokeWait;

% Clear the screen. "sca" is short hand for "Screen CloseAll". This clears
% all features related to PTB. Note: we leave the variables in the
% workspace so you can have a look at them if you want.
sca;

```
