# Radial Checkerboard

> Source: [radialCheckerboard](https://peterscarfe.com/radialCheckerboard.html)

Radial Checkerboard Demo: Displays an static radial checkerboard, as is typically used as the basis for visual field mapping in fMRI (this demo is a modified version of one coded by

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

% Set up alpha-blending for smooth (anti-aliased) lines
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Here we calculate the radial distance from the center of the screen to
% the X and Y edges
xRadius = windowRect(3) / 2;
yRadius = windowRect(4) / 2;

% Set the dimensions of the texture to be just short of full screen height
screenYlim = windowRect(4) * .97;

% Number of white/black circle pairs
rcycles = 8;

% Number of white/black angular segment pairs (integer)
tcycles = 24;

% Now we make our checkerboard pattern
xylim = 2 * pi * rcycles;
[x, y] = meshgrid(-xylim: 2 * xylim / (screenYlim - 1): xylim,...
    -xylim: 2 * xylim / (screenYlim - 1): xylim);
at = atan2(y, x);
checks = ((1 + sign(sin(at * tcycles) + eps)...
    .* sign(sin(sqrt(x.^2 + y.^2)))) / 2) * (white - black) + black;
circle = x.^2 + y.^2 <= xylim^2;
checks = circle .* checks + grey * ~circle;

% Now we make this into a PTB texture
radialCheckerboardTexture  = Screen('MakeTexture', window, checks);

% Draw our texture to the screen
Screen('DrawTexture', window, radialCheckerboardTexture);

% Flip to the screen
Screen('Flip', window);

% Wait for a keypress
KbStrokeWait;

% Clear up and leave the building
sca;

```
