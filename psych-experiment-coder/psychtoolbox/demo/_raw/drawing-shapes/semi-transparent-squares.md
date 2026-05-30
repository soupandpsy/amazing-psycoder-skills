# Semi Transparent Squares

> Source: [semiTransparentSquares](https://peterscarfe.com/semiTransparentSquares.html)

Shows you how to make shapes semi-transparent using the "alpha" channel, so that you can partially "see through shapes" to those behind. Again, the order of operations is key.

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

% Set blend function for alpha blending
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Make a base Rect of 400 by 400 pixels
baseRect = [0 0 400 400];

% Screen X positions of our three rectangles
squareXpos = [xCenter - 200 xCenter + 200 xCenter];
squareYpos = [yCenter yCenter yCenter + 200];
numSqaures = length(squareXpos);

% Set the colors to Red, Green and Blue, with the fourth value being the
% "alpha" value. This also takes a value between 0 and 1 just like a
% normal colour, however now 0 = totally transparent and 1 = totally
% opaque. Our RGB triplets are now RGBA values.
allColors = [1 0 0 1; 0 1 0 1; 0 0 1 0.5]';

% Make our rectangle coordinates
allRects = nan(4, 3);
for i = 1:numSqaures
    allRects(:, i) = CenterRectOnPointd(baseRect,...
        squareXpos(i), squareYpos(i));
end

% Draw the rect to the screen
Screen('FillRect', window, allColors, allRects);

% Flip to the screen
Screen('Flip', window);

% Wait for a key press
KbStrokeWait;

% Clear the screen
sca;

```
