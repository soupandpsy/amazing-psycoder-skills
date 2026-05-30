# Bubbles

> Source: [bubbles](https://peterscarfe.com/bubbles.html)

This demo shows how to produce a basic "Bubbles" stimulus. We load the standard PTB konijntjes image into a texture and then view it through a mask consisting of an opaque grey layer punctuated by Gaussian apertures through which the konijntjes image can be seen. You can easily explore all the components of the stimulus e.g. try drawing only the original Gaussian mask over the image.

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

% Here we load in an image from file. This one is a image of rabbits that
% is included with PTB
theImageLocation = [PsychtoolboxRoot 'PsychDemos' filesep...
    'AlphaImageDemo' filesep 'konijntjes1024x768.jpg'];
theImage = imread(theImageLocation);

% Get the size of the image
[s1, s2, s3] = size(theImage);

% Here we check if the image is too big to fit on the screen and abort if
% it is. See ImageRescaleDemo to see how to rescale an image.
if s1 > screenYpixels || s2 > screenYpixels
    disp('ERROR! Image is too big to fit on the screen');
    sca;
    return;
end

% Make the image into a texture
imageTexture = Screen('MakeTexture', window, theImage);

% Make a gaussian aperture with the "alpha" channel
gaussDim = 50;
gaussSigma = gaussDim / 3;
[xm, ym] = meshgrid(-gaussDim:gaussDim, -gaussDim:gaussDim);
gauss = exp(-(((xm .^2) + (ym .^2)) ./ (2 * gaussSigma^2)));
[s1, s2] = size(gauss);
mask = ones(s1, s2, 2) * grey;
mask(:, :, 2) = white * (1 - gauss);
masktex = Screen('MakeTexture', window, mask);

% Make a grey texture to cover the full window
fullWindowMask = Screen('MakeTexture', window,...
    ones(screenYpixels, screenXpixels) .* grey);

% Make coordinates in which to draw the apertures into our full screen mask
[xg, yg] = meshgrid(-3:1:3, -3:1:3);
spacing = gaussDim * 2;
xg = xg .* spacing + screenXpixels / 2;
yg = yg .* spacing + screenYpixels / 2;
xg = reshape(xg, 1, numel(xg));
yg = reshape(yg, 1, numel(yg));

% Make the destination rectangles for the gaussian apertures
dstRects = nan(4, numel(xg));
for i = 1:numel(xg)
    dstRects(:, i) = CenterRectOnPointd([0 0 s1, s2], xg(i), yg(i));
end

% Draw the gaussian apertures  into our full screen aperture mask
Screen('DrawTextures', fullWindowMask, masktex, [], dstRects);

% Draw the image to the screen, unless otherwise specified PTB will draw
% the texture full size in the center of the screen. We first draw the
% image in its correct orientation.
Screen('DrawTexture', window, imageTexture, [], [], 0);
Screen('DrawTexture', window, fullWindowMask);

% Flip to the screen
Screen('Flip', window);

% Wait for key press
KbStrokeWait;

% Clear the screen
sca;

```
