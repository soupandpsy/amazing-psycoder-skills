# Scaled Dot Grid

> Source: [scaledDotGrid](https://peterscarfe.com/scaledDotGrid.html)

Shows you how to expand and contract a grid of dots draw on the screen. The size of the dots also modulates contingent upon their expansion.

```matlab
% Clear the workspace and the screen
sca;
close all;
clear;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers. This gives us a number for each of the screens
% attached to our computer.
screens = Screen('Screens');

% Draw we select the maximum of these numbers. So in a situation where we
% have two screens attached to our monitor we will draw to the external
% screen. When only one screen is attached to the monitor we will draw to
% this.
screenNumber = max(screens);

% Define black and white (white will be 1 and black 0).
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);

% Open an on screen window and color it black
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);

% Get the size of the on screen window in pixels
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window in pixels
[xCenter, yCenter] = RectCenter(windowRect);

% Enable alpha blending for anti-aliasing
Screen('BlendFunction', window, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Use the meshgrid command to create our base dot coordinates
dim = 10;
[x, y] = meshgrid(-dim:1:dim, -dim:1:dim);

% Scale this by the distance in pixels we want between each dot
pixelScale = screenYpixels / (dim * 2 + 2);
x = x .* pixelScale;
y = y.* pixelScale;

% Calculate the number of dots
numDots = numel(x);

% Make the matrix of positions for the dots into two vectors
xPosVector = reshape(x, 1, numDots);
yPosVector = reshape(y, 1, numDots);

% We can define a center for the dot coordinates to be relaitive to. Here
% we set the centre to be the centre of the screen
dotCenter = [screenXpixels / 2 screenYpixels / 2];

% Set the color of our dot to be random
dotColors = rand(3, numDots);

% Set the maximum size of the dots to 25 pixels
maxDotSize = 25;

% Our grid will pulse by taking the absolute value of a sine wave, we
% therefore set the amplitude of the sine wave to 1 as this will be a
% multiplicative scale factor ranging between 0 and 1.
% With 0 the dots will all be on top of one another. With 1 the gird will
% have its maximum size.
% These are the parameters for the sine wave
% See: http://en.wikipedia.org/wiki/Sine_wave
amplitude = 1;
frequency = 0.05;
angFreq = 2 * pi * frequency;
startPhase = 0;
time = 0;

% Sync us and get a time stamp
vbl = Screen('Flip', window);
waitframes = 1;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Loop the animation until a key is pressed
while ~KbCheck

    % Scale the grid coordinates
    scaleFactor = abs(amplitude * sin(angFreq * time + startPhase));

    % Scale the dot size. Here we limit the minimum dot size to one pixel
    % by using the max function as PTB won't allow the dot size to scale to
    % zero (sensibly, as you'd be drawing no dots at all)
    thisDotSize = max(1, maxDotSize .* scaleFactor);

    % Draw all of our dots to the screen in a single line of code adding
    % the sine oscilation to the X coordinates of the dots
    Screen('DrawDots', window, [xPosVector; yPosVector] .* scaleFactor,...
        thisDotSize, dotColors, dotCenter, 2);

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the time
    time = time + ifi;

end

% Clear the screen. "sca" is short hand for "Screen CloseAll". This clears
% all features related to PTB. Note: we leave the variables in the
% workspace so you can have a look at them if you want.
sca;

```
