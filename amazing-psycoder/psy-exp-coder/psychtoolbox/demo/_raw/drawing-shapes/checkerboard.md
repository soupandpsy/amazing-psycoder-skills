# Checkerboard

> Source: [checkerboard](https://peterscarfe.com/checkerboard.html)

Builds on previous demos by showing how to build a multi-coloured and a black-and-white checker-board. As before we draw all of the components of our two checkerboards efficiently in a single line of code. Most of the coding work goes into the formatting of the inputs to our drawing function. 

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
grey = white / 2;

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey);

% Set up alpha-blending
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Make a base Rect of 80 by 80 pixels
dim = 80;
baseRect = [0 0 dim dim];

% Make the coordinates for our grid of squares
[xPos, yPos] = meshgrid(-2:1:2, -2:1:2);

% Calculate the number of squares and reshape the matrices of coordinates
% into a vector
[s1, s2] = size(xPos);
numSquares = s1 * s2;
xPos = reshape(xPos, 1, numSquares);
yPos = reshape(yPos, 1, numSquares);

% Scale the grid spacing to the size of our squares and centre
xPosLeft = xPos .* dim + screenXpixels * 0.25;
yPosLeft = yPos .* dim + yCenter;

xPosRight = xPos .* dim + screenXpixels * 0.75;
yPosRight = yPos .* dim + yCenter;

% Set the colors of each of our squares
multiColors = rand(3, numSquares);
bwColors = repmat(eye(2), 3, 3);
bwColors = bwColors(1:end-1, 1:end-1);
bwColors = reshape(bwColors, 1, numSquares);
bwColors = repmat(bwColors, 3, 1);

% Make our rectangle coordinates
allRectsLeft = nan(4, 3);
allRectsRight = nan(4, 3);
for i = 1:numSquares
    allRectsLeft(:, i) = CenterRectOnPointd(baseRect,...
        xPosLeft(i), yPosLeft(i));
    allRectsRight(:, i) = CenterRectOnPointd(baseRect,...
        xPosRight(i), yPosRight(i));
end

% Draw the rect to the screen
Screen('FillRect', window, [multiColors bwColors],...
    [allRectsLeft allRectsRight]);

% Flip to the screen
Screen('Flip', window);

% Wait for a key press
KbStrokeWait;

% Clear the screen
sca;

```
