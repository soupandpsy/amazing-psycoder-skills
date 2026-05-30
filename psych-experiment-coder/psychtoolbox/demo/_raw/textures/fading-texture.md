# Fading Texture

> Source: [fadingTexture](https://peterscarfe.com/fadingTexture.html)

This demo loads a picture of rabbits included in the PTB distribution, conversts it to a texture and dynamically fades the texture in and out of visibility with a temporal sine wave function. It does this by changing the "alpha" value of the texture (this is called alpha blending, or compositing). The alpha value ranges between 0-1, 0 being completely invisible and 1 being completely visible. For a value of 0.5 you can see half of the image and half of the background colour (the alpha value of the texture oscillates around this value during the demo).

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

% Our will fade in and out with a sine wave function
% See: http://en.wikipedia.org/wiki/Sine_wave
amplitude = 0.5;
frequency = 0.2;
angFreq = 2 * pi * frequency;
startPhase = 0;
time = 0;

% Numer of frames to wait before re-drawing
waitframes = 1;

% Perform initial flip to gray background and sync us to the retrace:
vbl = Screen('Flip', window);

% Presentation loop (press any key to exit)
while ~KbCheck

    % Position of the square on this frame
    thisContrast = amplitude * sin(angFreq * time + startPhase) + amplitude;

    % Draw the image to the screen
    Screen('DrawTexture', window, imageTexture, [], [], 0, [], thisContrast);

    % Increment the time
    time = time + ifi;

    % Flip our drawing to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

end

% Clear the screen
sca;

```
