# Mouse In Square

> Source: [mouseInSquareDemo](https://peterscarfe.com/mouseInSquareDemo.html)

Shows how change the colour of a square contingent upon whether or not the mouse cursor is inside it or not.

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

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Change the blend function to draw an antialiased stimuli
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Make a base Rect which is a proportion of the screen in size
dim = round(screenYpixels / 6);
baseRect = [0 0 dim dim];

% Define red and blue
red = [1 0 0];
blue = [0 0 1];

% Hide the stanard mouse cursor
HideCursor;

% Here we set the initial position of the mouse to be in the centre of the
% screen
SetMouse(xCenter, yCenter, window);

% Sync us and get a time stamp
vbl = Screen('Flip', window);
waitframes = 1;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Loop the animation until a key is pressed
while ~KbCheck

    % Get the current position of the mouse
    [x, y, buttons] = GetMouse(window);

    % Center the rectangle on the centre of the screen
    centeredRect = CenterRectOnPointd(baseRect, xCenter, yCenter);

    % See if the mouse cursor is inside the square
    inside = IsInRect(x, y, centeredRect);

    % Set the color of the square to be red if the mouse is inside it or
    % blue if the mouse is outside it
    if inside == 1
        rectColor = red;
    elseif inside == 0
        rectColor = blue;
    end

    % Draw the rect to the screen
    Screen('FillRect', window, rectColor, centeredRect);

    % Draw a white dot where the mouse is
    Screen('DrawDots', window, [x y], 10, white, [], 2);

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

end

% Clear the screen
sca;

```
