# Order of Drawing

> Source: [orderOfDrawing](https://peterscarfe.com/orderOfDrawing.html)

This demo explains about sequential drawing. This is key to drawing multiple objects to the screen e.g. overlapping objects. It also demonstrates how to draw multiple objects in a single line of code. This is far more efficient than many seperate lines of code, or the use of a for loop.

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

% Define black and white
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);

% Open an on screen window and color it black
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);

% Set the blend funciton for the screen
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the size of the on screen window in pixels
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window in pixels
[xCenter, yCenter] = RectCenter(windowRect);

% Make a base Rect of 200 by 200 pixels.
baseRect = [0 0 200 200];

% Center the left hand side squares on positions in the screen.
leftBackRect = CenterRectOnPointd(baseRect, screenXpixels * 0.25, yCenter);
leftForwardRect = CenterRectOnPointd(baseRect,...
    screenXpixels * 0.25 + 100, yCenter + 100);

% Do the same of the right hand side squares, but not concatonate these
% into a single matrix. This is bacause we will be drawing these both in a
% single line of code. For more details use Screen DrawRect?
rightBackRect = CenterRectOnPointd(baseRect,...
    screenXpixels * 0.75, yCenter);
rightForwardRect = CenterRectOnPointd(baseRect,...
    screenXpixels * 0.75 + 100, yCenter + 100);
rightRects = [rightBackRect; rightForwardRect]';

% We do the same of the colors of the rects. Put them in one matrix for
% drawing
rightRectColors = [1 0 0; 0 1 0]';

% Draw the left hand side squares onto the screen, we do this sequentially
% with two lines of code, one for each rectangle.
Screen('FillRect', window, [1 0 0], leftBackRect);
Screen('FillRect', window, [0 1 0], leftForwardRect);

% Now we draw the two right hand side squares to the screen. We get the
% same results as if we draw in two seperate lines, however we efficiently
% draw both squares in a single line of code. Note, that as detailed above,
% we acheive the same ordering of squares by placing the coordinates of the
% square we want to draw first into the matrix first.
Screen('FillRect', window, rightRectColors, rightRects);

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
