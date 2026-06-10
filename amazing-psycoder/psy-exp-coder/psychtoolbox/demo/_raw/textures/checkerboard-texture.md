# Checkerboard Texture

> Source: [checkerboardTexture](https://peterscarfe.com/checkerboardTexture.html)

Exploits dynamic texture scaling to draw a checkerboard texture very efficiently using onboard filtering in PTB. The original 4 x 4 pixel texture is scaled up by 90% with nearest neighbour filtering. Also demonstrates how to rotate textures when drawing them to the screen (see the animated texture demos for more information on texture rotation).

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

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Set up alpha-blending for smooth (anti-aliased) lines
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Define a simple 4 by 4 checker board, this will effectively be a four by
% four pixel image that we scale using onboard PTB filtering.
checkerboard = repmat(eye(2), 2, 2);

% Make the checkerboard into a texure (4 x 4 pixels)
checkerTexture = Screen('MakeTexture', window, checkerboard);

% We will scale our texure up to 90 times its current size be defining a
% larger screen destination rectangle
[s1, s2] = size(checkerboard);
dstRect = [0 0 s1 s2] .* 90;
dstRect = CenterRectOnPointd(dstRect, xCenter, yCenter);

% Draw the checkerboard texture to the screen. By default bilinear
% filtering is used. For this example we don't want that, we want nearest
% neighbour so we change the filter mode to zero
filterMode = 0;
Screen('DrawTextures', window, checkerTexture, [],...
    dstRect, 45, filterMode);

% Flip to the screen
Screen('Flip', window);

% Wait for a key press
KbStrokeWait;

% Clear the screen
sca;

```
