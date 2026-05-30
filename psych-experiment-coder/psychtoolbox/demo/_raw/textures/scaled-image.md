# Scaled Image

> Source: [scaledImage](https://peterscarfe.com/scaledImage.html)

This demo loads an image and then dynamically rescales it in size on each frame within a for loop. Scaling is acheived by modulating the destination rectangle in which the image will be draw to on the screen. It demonstrates automatic texture scaling in PTB. By default bilinear filtering is used to rescale the texture. The image never gets larger than the maximum needed for the image to span the fully height of the screen. 

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

% Here we load in an image from file. This one is a image of rabbits that
% is included with PTB
theImageLocation = [PsychtoolboxRoot 'PsychDemos' filesep...
    'AlphaImageDemo' filesep 'konijntjes1024x768.jpg'];
theImage = imread(theImageLocation);

% Make the image into a texture
imageTexture = Screen('MakeTexture', window, theImage);

% Get the size of the image
[s1, s2, s3] = size(theImage);

% Determine the scaling needed to make the rabbit image fill the whole
% screen in the y dimension
maxScaling = screenYpixels / s1;

% Our square will oscilate with a sine wave function to the left and right
% of the screen. These are the parameters for the sine wave
% See: http://en.wikipedia.org/wiki/Sine_wave
amplitude = maxScaling;
frequency = 0.1;
angFreq = 2 * pi * frequency;
startPhase = 0;

% Flip each frame
waitframes = 1;
time = 0;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Get an initial timestamp
vbl = Screen('Flip', window);

% Endless loop in which we scale the size of the texture
while ~KbCheck

    % Image scale on this frame. We use abs as negative scaling makes no
    % sense. The scaling will never get larger than the maximum needed for
    % the image to be fully screen height.
    theScale = abs(amplitude * sin(angFreq * time + startPhase));

    % Set the based rectangle size for drawing to the screen
    baseRect = CenterRectOnPointd([0 0 s2 s1] .* theScale, xCenter, yCenter);

    % Draw the image to the screen, unless otherwise specified PTB will draw
    % the texture full size in the center of the screen. We first draw the
    % image in its correct orientation.
    Screen('DrawTexture', window, imageTexture, [], baseRect, 0);

    % Get an initial screen flip for timing
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the time
    time = time + ifi;

end

% Clear the screen
sca;

```
