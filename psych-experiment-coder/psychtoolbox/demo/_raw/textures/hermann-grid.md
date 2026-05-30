# Hermann Grid

> Source: [hermannGrid](https://peterscarfe.com/hermannGrid.html)

Draws a set of black squares on a white background to make the Hermann Grid Illusion. The blobs that you see at the cross over of the gaps are illusory. They are also contingent upon where you are focusing in the image. 

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
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, white);

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Set up alpha-blending for smooth (anti-aliased) lines
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Pixel size of the squares and gaps for our Hermann grid
gridSqSize = 100;
gapSize = 20;
stepSize = gridSqSize + gapSize;

% How many can we fit on the screen. Rough hacky code to make sure the
% sqaures do not go off of the screen.
numLines = floor(screenYpixels / stepSize) - 2;
if rem(numLines, 2) ~= 0
    numLines = numLines + 1;
end
halfNumLines = numLines / 2;

% Screen positions for the centre of all of our sqaures
[xpos, ypos] = meshgrid(-halfNumLines:halfNumLines, -halfNumLines:halfNumLines);
xpos = xpos .* stepSize + xCenter;
ypos = ypos .* stepSize + yCenter;

% Dimensions and count
[s1, s2] = size(ypos);
numSquares = numel(ypos);

% Rectangle positions where our squares will go
allRects = nan(numSquares, 4);
ticker = 0;
for i = 1:s1
    for ii = 1:s2
        ticker = ticker + 1;
        allRects(ticker, :) = CenterRectOnPointd([0 0 gridSqSize gridSqSize],...
            xpos(i, ii), ypos(i, ii));
    end
end

% Draw all of the squares
Screen('FillRect', window, black, allRects');

% Flip to the screen
Screen('Flip', window);

% Wait for a key press
KbStrokeWait;

% Clear the screen
sca;

```
