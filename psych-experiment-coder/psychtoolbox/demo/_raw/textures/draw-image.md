# Draw Image

> Source: [drawImage](https://peterscarfe.com/drawImage.html)

Shows you how to load an image into PTB, convert it to a texture and then present it on the screen for a specific amount of time. Specifically, the code presents an image for two seconds on a grey background, fills the screen green for two seconds, then finally presents the same image (now upside down) again for two seconds, this time on the green background.

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

% Get the size of the image
[s1, s2, s3] = size(theImage);

% We will present each element of our sequence for two seconds
presSecs = 2;
waitframes = round(presSecs / ifi);

% Make the image into a texture
imageTexture = Screen('MakeTexture', window, theImage);

% Get an initial screen flip for timing
vbl = Screen('Flip', window);

% Draw the image to the screen, unless otherwise specified PTB will draw
% the texture full size in the center of the screen. We first draw the
% image in its correct orientation.
Screen('DrawTexture', window, imageTexture, [], [], 0);

% Flip to the screen
vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

% Now fill the screen green
Screen('FillRect', window, [0 1 0]);

% Flip to the screen
vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

% Draw the image to the screen for a second time this time upside down and
% drawn onto our updated blue background
Screen('DrawTexture', window, imageTexture, [], [], 180);

% Flip to the screen
vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

% Clear the screen
WaitSecs(presSecs);
sca;

```
