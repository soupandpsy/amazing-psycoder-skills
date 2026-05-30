# Scaled Sprial Texture

> Source: [scaledSpiralTexture](https://peterscarfe.com/scaledSpiralTexture.html)

Shows how you can dynamically rescale a single texture to be different sizes when drawn to the screen.

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
inc = white - grey;

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

% Define a simple spiral texture by defining cartasian X and Y coordinates
% with the meshgrid command, converting these to polar coordinates
% with cart2pol and finally defining the spiral texture
[x, y] = meshgrid(-150:1:150, -150:1:150);
[th, r] = cart2pol(x, y);
spiral = grey + inc .* cos(r / 5 + th * 5);

% Make our sprial texure into a screen texture for drawing
spiralTexture = Screen('MakeTexture', window, spiral);

% Define the destination rectangles for our spiral textures. For this demo
% we will make the left hand destination rectangle half the size of the
% texture, the middle one the same size as the texture and the right hand
% on 1.25 times the size of the texture
[s1, s2] = size(x);
baseRect = [0 0 s1 s2];
dstRects = nan(4, 3);
dstRects(:, 1) = CenterRectOnPointd(baseRect .* 0.5,...
    screenXpixels * 0.2, yCenter);
dstRects(:, 2) = CenterRectOnPointd(baseRect,...
    screenXpixels * 0.5, yCenter);
dstRects(:, 3) = CenterRectOnPointd(baseRect .* 1.25,...
    screenXpixels * 0.8, yCenter);

% Batch Draw all of the texures to screen
Screen('DrawTextures', window, spiralTexture, [], dstRects);

% Flip to the screen
Screen('Flip', window);

% Wait for a key press
KbStrokeWait;

% Clear the screen
sca;

```
