# Multiple Moving Squares

> Source: [multipleMovingSquares](https://peterscarfe.com/multipleMovingSquares.html)

Shows how to animate two squares moving sinusoidally across the screen with different colours and different lateral offsets. Exit demo by pressing any key.

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

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);

% Enable alpha blending for anti-aliasing
Screen('BlendFunction', window, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Make a base Rect of 200 by 200 pixels
baseRect = [0 0 200 200];

% Set the color of the top rect to red and the bottom blue
topColor = [1 0 0];
bottomColor = [0 0 1];

% Our square will oscilate with a sine wave function to the left and right
% of the screen. These are the parameters for the sine wave
% See: http://en.wikipedia.org/wiki/Sine_wave
amplitude = screenXpixels * 0.25;
frequency = 0.2;
angFreq = 2 * pi * frequency;
time = 0;

% Our two squares will be pi out of phase
startPhaseOne = 0;
startPhaseTwo = pi;

% Sync us and get a time stamp
vbl = Screen('Flip', window);
waitframes = 1;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Loop the animation until a key is pressed
while ~KbCheck

    % Position of the two squares on this frame
    xposOne = amplitude * sin(angFreq * time + startPhaseOne);
    xposTwo = amplitude * sin(angFreq * time + startPhaseTwo);

    % Add this position to the screen center coordinate. This is the point
    % we want our squares to oscillate around
    squareXposOne = xCenter + xposOne;
    squareXposTwo = xCenter + xposTwo;

    % Center the rectangle on the centre of the screen
    centeredRectOne = CenterRectOnPointd(baseRect, squareXposOne,...
        screenYpixels * 0.25);
    centeredRectTwo = CenterRectOnPointd(baseRect, squareXposTwo,...
        screenYpixels * 0.75);

    % Draw the rect to the screen
    Screen('FillRect', window, [topColor' bottomColor'],...
        [centeredRectOne' centeredRectTwo']);

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the time
    time = time + ifi;

end

% Clear the screen
sca;

```
