# Moving Text

> Source: [movingText](https://peterscarfe.com/movingText.html)

In this demo we show you how to animate text. We write "Hello World" in different vertical positions on the screen and then oscillate the horizontal position of the text sinusoidally over time.

```matlab
% Clear the workspace and the screen
close all;
clear;
sca

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');

% Select the external screen if it is present, else revert to the native
% screen
screenNumber = max(screens);

% Define black, white and grey
black = BlackIndex(screenNumber);
white = WhiteIndex(screenNumber);
grey = white / 2;

% Open an on screen window and color it grey
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Set the blend funciton for the screen
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the size of the on screen window in pixels
% For help see: Screen WindowSize?
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

Screen('TextSize', window, 90);

% Get the centre coordinate of the window in pixels
% For help see: help RectCenter
[xCenter, yCenter] = RectCenter(windowRect);

% Our text will oscilate with a sine wave function to the left and right
% of the screen. These are the parameters for the sine wave
% See: http://en.wikipedia.org/wiki/Sine_wave
amplitude = screenXpixels * 0.2;
frequency = 0.2;
angFreq = 2 * pi * frequency;
time = 0;

% Our two text strings will be pi out of phase
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

    % Position of the two text strings on this frame
    xposOne = amplitude * sin(angFreq * time + startPhaseOne);
    xposTwo = amplitude * sin(angFreq * time + startPhaseTwo);

    % Add this position to the screen center coordinate.
    squareXposOne = xCenter + xposOne;
    squareXposTwo = xCenter + xposTwo;

    % Draw the text to the screen
    DrawFormattedText(window, 'Hello World', squareXposOne,...
        screenYpixels * 0.25, [1 0 0]);
    DrawFormattedText(window, 'Hello World', squareXposTwo,...
        screenYpixels * 0.75, [1 0 1]);

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the time
    time = time + ifi;

end

% Clear the screen
sca;

```
