# Countdown Timer

> Source: [countdownTimer](https://peterscarfe.com/countdownTimer.html)

This demo shows how to implement a simple countdown timer. The timer starts at 10 and counts down to 0, with the number shown on the screen updating each second. The color of the text updates randomly each time the number changes. It uses the inbuilt functionality of PTB to present a stimulus for multiple frames at a time (as in

```matlab
% Clear the workspace and the screen
close all;
clear;
sca

% Randomly seed the random number generation
rng('shuffle');

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');

% Select the external screen if it is present, else revert to the native
% screen
screenNumber = max(screens);

% Define black
black = BlackIndex(screenNumber);

% Open an on screen window and color it grey
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);

% Get the vertical refresh rate of the monitor
ifi = Screen('GetFlipInterval', window);

% Set the blend funciton for the screen
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the size of the on screen window in pixels
% For help see: Screen WindowSize?
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window in pixels
% For help see: help RectCenter
[xCenter, yCenter] = RectCenter(windowRect);

% We set the text size to be nice and big here
Screen('TextSize', window, 300);

% We will be presenting each of our numbers 10 through 0 for one seconds
% each
presSecs = 1;
waitframes = round(presSecs / ifi);

% We change the color of the number every "nominalFrameRate" frames
colorChangeCounter = 0;

% Randomise a start color
color = rand(1, 3);

% Starting number
currentNumber = 10;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Flip to the vertical retrace rate
vbl = Screen('Flip', window);

% We use a while loop to count down. On each iteration of the loop we use a
% waitframes value greater than 1 so that each number is presented for one
% second
while currentNumber >= 0

    % Convert our current number to display into a string
    numberString = num2str(currentNumber);

    % Draw our number to the screen
    DrawFormattedText(window, numberString, 'center', 'center', color);

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % New random colour for the next number
    color = rand(1, 3);

    % Increment the number
    currentNumber = currentNumber - 1;

end

% Wait a second before closing the screen
WaitSecs(1);

% Clear the screen
close all;
sca

```
