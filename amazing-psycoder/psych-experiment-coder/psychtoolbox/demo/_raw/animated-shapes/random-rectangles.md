# Random Rectangles

> Source: [randomRectangles](https://peterscarfe.com/randomRectangles.html)

Draws a large number of rectangles with random aspect ratios and random colours at random positions on the screen. Note that PTB elegently deals with cases where part of the rectangle would appear off of the screen due to its dimensions and positioning. The part of the rectangle off of the screen is simple not drawn, so the code does not crash.

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

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Make a base Rect of 200 by 200 pixels (we will randomly scale this for
% each of our rectangles)
baseRect = [0 0 200 200];

% Number of rectangles that we will draw (reduce this number if you
% computer struggles)
numOfRect = 1000;

% Generate a random set of colors. Note here the dimensions of the matrix
% that we are producing. This is needed for the format of
% Screen('DrawRects', ...)
allColors = round(rand(3, numOfRect));

% Make our rectangle coordinates. Here we are doing a little bit of math
% withing the call to CenterRectOnPointd(). Also again not the dimensions
% of the matrix that we end up with.
allRects = nan(4, numOfRect);
for i = 1:numOfRect
    allRects(:, i) = CenterRectOnPointd(baseRect .* [0 0 rand / 2 rand / 2], ...
        rand .* screenXpixels,...
        rand .* screenYpixels);
end

% Draw all of our rectangles to the sceen. Note here that we can draw
% rectangles at the very edge of our screen and only part of them will be
% visible.
Screen('FillRect', window, allColors, allRects);

% Flip to the screen
Screen('Flip', window);

% Wait for a key press
KbStrokeWait;

% Clear the screen
sca;

```
