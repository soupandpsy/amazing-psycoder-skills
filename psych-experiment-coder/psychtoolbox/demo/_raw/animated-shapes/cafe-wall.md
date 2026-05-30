# Cafe Wall

> Source: [cafeWall](https://peterscarfe.com/cafeWall.html)

This demo builds on the demos so far by drawing squares and framed squares to create the famous

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
grey = GrayIndex(screenNumber);
darkGrey = white * 0.25;

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, darkGrey);

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Set up alpha-blending for smooth (anti-aliased) lines
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Line width of the lines around the squares: this is like the "motar" of
% the brick wall
morterWidth = 3;

% Dimensions: the grid will be this plus one in width and height
dim = 5;

% A basic way to make sure this scales to the screen
gridSqSize = screenYpixels * 0.3 / (dim - 1);

% Screen positions for the centre of all of our sqaures
[xposOrig, yposOrig] = meshgrid(-dim:dim, -dim:dim);
xpos = xposOrig .* gridSqSize + xCenter;
ypos = yposOrig .* gridSqSize + yCenter;

% Define the black and white pattern of the grid
grid = repmat(reshape(mod(xposOrig + yposOrig, 2), 1, numel(xposOrig)), 3, 1);

% Dimensions and count
[s1, s2] = size(ypos);
numSquares = numel(ypos);

% Rectangle positions where our squares. The larger squares are needed for
% the motar to be the same width including at the edges of the grid
allRectsSquares = nan(numSquares, 4);
allRectsMortar = nan(numSquares, 4);
ticker = 0;
for i = 1:s1

    % We shift every other line laterally to make the Cafe Wall illusion
    if mod(i, 2) == 1
        adder = gridSqSize / 2;
    else
        adder = 0;
    end

    for ii = 1:s2

        % Increment ticker
        ticker = ticker + 1;

        % Make this square coordinates
        allRectsSquares(ticker, :) = CenterRectOnPointd([0 0 gridSqSize gridSqSize],...
            xpos(i, ii) + adder, ypos(i, ii));

        % We only want additional background squares for the outer edges
        if i == 1 || ii == 1 || i == s1 || ii == s2
            allRectsMortar(ticker, :) = CenterRectOnPointd([0 0 gridSqSize + morterWidth gridSqSize + morterWidth],...
                xpos(i, ii) + adder, ypos(i, ii));
        end

    end

end

% Remove the nans
allRectsMortar = allRectsMortar(all(~isnan(allRectsMortar), 2), :);

% Draw the background squres to make the edge motar work
Screen('FillRect', window, grey, allRectsMortar');

% Draw the black and white squares
Screen('FillRect', window, grid, allRectsSquares');

% Draw the mortar
Screen('FrameRect', window, grey, allRectsSquares', morterWidth);

% Flip to the screen
Screen('Flip', window);

% Wait for a key press
KbStrokeWait(-1);

% Clear the screen
sca;

```
