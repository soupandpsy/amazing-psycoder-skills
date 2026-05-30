# Texture Rotation

> Source: [inOutTextureRotation](https://peterscarfe.com/inOutTextureRotation.html)

In this demo we demonstrate the difference between "external" and "internal" texture rotation. A pinwheel texture is drawn to the screen in four positions, each colour modulated. The left two textures rotate "externally" the right two textures "internally".

```matlab
% Clear the workspace
close all;
clear;
sca;

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

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Dimension of our texure (it will be this value +1 pixel)
dim = 100;

% Make a second dimension value which is increased by a factor of the
% squareroot of 2. We need to do this because in this demo we will be using
% internal texture rotation. We round this to the nearest pixel.
dim2 = ceil(dim * sqrt(2));

% Define a simple spiral texture by defining X and Y coordinates with the
% meshgrid command, converting these to polar coordinates and finally
% defining the spiral texture. Not here we use dim2 NOT dim.
[x, y] = meshgrid(-dim2:1:dim2, -dim2:1:dim2);
[th, r] = cart2pol(x, y);
wheel = grey + inc .* cos(pi * th);

% Make our sprial texure into a screen texture for drawing
spiralTexture = Screen('MakeTexture', window, wheel);

% We are going to draw four textures to show how a black and white texture
% can be color modulated upon drawing.
yPos = yCenter;
xPos = linspace(screenXpixels * 0.2, screenXpixels * 0.8, 4);

% Define the destination rectangles for our spiral textures. This will be
% the same size as the window we use to view our texture.
ndim = dim * 2 + 1;
baseRectDst = [0 0 ndim ndim];
dstRects = nan(4, 4);
for i = 1:4
    dstRects(:, i) = CenterRectOnPointd(baseRectDst, xPos(i), yPos);
end

% Now we create a window through which we will view our texture. This is
% the same size as our destination rectangles. But we shift it in X and Y
% by a value of dim2 - dim. This makes sure our window is centered on the
% middle of the enlarged texture we made for internal texture rotation.
srcRect = baseRectDst + (dim2 - dim);

% Color Modulation
colorMod = [1 1 1; 1 0 0; 0 1 0; 0 0 1]';

% Start Angle for all of the textures
angle = 0;

% Angle increment per frame
angleInc = 2;

% Numer of frames to wait before re-drawing
waitframes = 1;

% Perform initial flip to gray background and sync us to the retrace:
vbl = Screen('Flip', window);

while ~KbCheck

    % Draw the first two textues using whole "external" texture rotation
    Screen('DrawTextures', window, spiralTexture, srcRect,...
        dstRects(:, 1:2), angle, [], [], colorMod(:, 1:2));

    % Draw the last two textues using "internal" texture rotation
    Screen('DrawTextures', window, spiralTexture, srcRect, dstRects(:, 3:end), angle,...
        [], [], colorMod(:, 3:end), [], kPsychUseTextureMatrixForRotation);

    % Flip our drawing to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the angle
    angle = angle + angleInc;

end

% Clear the screen
sca;

```
