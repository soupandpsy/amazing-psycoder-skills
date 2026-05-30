# Framed Squares

> Source: [framedSquares](https://peterscarfe.com/framedSquares.html)

Shows you how to draw multiple framed squares simultaneously in a single line of code. 

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

% Make a base Rect of 200 by 200 pixels
baseRect = [0 0 200 200];

% Screen X positions of our three rectangles
squareXpos = [screenXpixels * 0.25 screenXpixels * 0.5 screenXpixels * 0.75];
numSquares = length(squareXpos);

% Set the colors to Red, Green and Blue
allColors = [1 0 0; 0 1 0; 0 0 1];

% Make our rectangle coordinates
allRects = nan(4, 3);
for i = 1:numSquares
    allRects(:, i) = CenterRectOnPointd(baseRect, squareXpos(i), yCenter);
end

% Pen width for the frames
penWidthPixels = 6;

% Draw the rect to the screen
Screen('FrameRect', window, allColors, allRects, penWidthPixels);

% Flip to the screen
Screen('Flip', window);

% Wait for a key press
KbStrokeWait;

% Clear the screen
sca;

```
