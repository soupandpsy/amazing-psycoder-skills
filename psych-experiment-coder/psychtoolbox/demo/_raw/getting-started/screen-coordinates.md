# Screen Coordinates

> Source: [screenCoordinates](https://peterscarfe.com/screenCoordinates.html)

In this demo you can move the mouse cursor around the screen and we write text on the screen letting you know what the X and Y pixel coordinates of the cursor are (rounded to the nearest pixel). This allows you to picture how screen coordinates are defined as well as how to query the position of the mouse.

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

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Setup the text type for the window
Screen('TextFont', window, 'Ariel');
Screen('TextSize', window, 50);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Set the mouse to the top left of the screen to start with
SetMouse(0, 0, window);

% We will update our screen on each frame
waitframes = 1;

% Gets a starting flip for timestamping
vbl = Screen('Flip', window);

% Loop the animation until a key is pressed
while ~KbCheck

    % Get the current position of the mouse
    [x, y, buttons] = GetMouse(window);

    % We clamp the values at the maximum values of the screen in X and Y
    % incase people have two monitors connected. This is all we want to
    % show for this basic demo.
    x = min(x, screenXpixels);
    y = min(y, screenYpixels);

    % Construct our text string
    textString = ['Mouse at X pixel ' num2str(round(x))...
        ' and Y pixel ' num2str(round(y))];

    % Text output of mouse position draw in the centre of the screen
    DrawFormattedText(window, textString, 'center', 'center', white);

    % Draw a white dot where the mouse cursor is
    Screen('DrawDots', window, [x y], 10, white, [], 2);

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

end

% Clear the screen
sca;

```
