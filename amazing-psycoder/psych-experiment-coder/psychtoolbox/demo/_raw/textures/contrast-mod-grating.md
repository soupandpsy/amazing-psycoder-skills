# Contrast Mod Grating

> Source: [contrastModGrating](https://peterscarfe.com/contrastModGrating.html)

This is a modified version of "DriftDemo2" included with PTB. I've modified it to draw a contrast modulated grating (second order grating) rather then a luminance modulated grating (first order grating).

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

% Grating size in pixels
gratingSizePix = 600;

% Grating frequency in cycles / pixel
freqCyclesPerPix = 0.01;

% Drift speed cycles per second
cyclesPerSecond = 1;

% Define Half-Size of the grating image.
texsize = gratingSizePix / 2;

% First we compute pixels per cycle rounded to the nearest pixel
pixPerCycle = ceil(1 / freqCyclesPerPix);

% Frequency in Radians
freqRad = freqCyclesPerPix * 2 * pi;

% This is the visible size of the grating
visibleSize = 2 * texsize + 1;

% Define our grating. Note it is only 1 pixel high. PTB will make it a full
% grating upon drawing
x = meshgrid(-texsize:texsize + pixPerCycle, 1);
grating = grey * cos(freqRad*x) + grey;

% Make a two layer mask filled with the background colour
mask = ones(1, numel(x), 2) * grey;

% Contrast for our contrast modulation mask: 0 = mask has no effect, 1 = mask
% will at its strongest part be completely opaque frameCounter.e. 0 and 100% contrast
% respectively
contrast = 0.8;

% Place the grating in the 'alpha' channel of the mask
mask(:, :, 2)= grating .* contrast;

% Make our grating mask texture
gratingMaskTex = Screen('MakeTexture', window, mask);

% Make a black and white noise mask half the size of our grating. This will
% be scaled upon drawing to make a "chunky" noise texture which our grating
% will mask. Note the round function in here. For this demo we are simply
% rounding the size to the nearest pixel, leaving PTB to do some scaling.
noise = rand(round(visibleSize / 2)) .* white;

% Make our noise texture
noiseTex = Screen('MakeTexture', window, noise);

% Make a destination rectangle for our textures and center this on the
% screen
dstRect = [0 0 visibleSize visibleSize];
dstRect = CenterRect(dstRect, windowRect);

% We set PTB to wait one frame before re-drawing
waitframes = 1;

% Calculate the wait duration
waitDuration = waitframes * ifi;

% Recompute pixPerCycle, this time without the ceil() operation from above.
% Otherwise we will get wrong drift speed due to rounding errors
pixPerCycle = 1 / freqCyclesPerPix;

% Translate requested speed of the grating (in cycles per second) into
% a shift value in "pixels per frame"
shiftPerFrame = cyclesPerSecond * pixPerCycle * waitDuration;

% Sync us to the vertical retrace
vbl = Screen('Flip', window);

% Set the frame counter to zero, we need this to 'drift' our grating
frameCounter = 0;

% Loop until a key is pressed
while ~KbCheck

    % Calculate the xoffset for our window through which to sample our
    % grating
    xoffset = mod(frameCounter * shiftPerFrame, pixPerCycle);

    % Now increment the frame counter for the next loop
    frameCounter = frameCounter + 1;

    % Define our source rectangle for grating sampling
    srcRect = [xoffset 0 xoffset + visibleSize visibleSize];

    % Draw noise texture to the screen
    Screen('DrawTexture', window, noiseTex, [], dstRect, []);

    % Draw grating mask
    Screen('DrawTexture', window, gratingMaskTex, srcRect, dstRect, []);

    % Flip to the screen on the next vertical retrace
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

end

% Clear the screen
sca;
close all;

```
