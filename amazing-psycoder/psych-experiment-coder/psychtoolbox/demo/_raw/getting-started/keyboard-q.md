# Keyboard Q

> Source: [keyboardQDemo](https://peterscarfe.com/keyboardQDemo.html)

In this demo we show the basic functionality of creating a keyboard queue. This allows precise capture of key presses. The demo is a bit fancier and demonstrates the use of logical operations to determine what is presented on the screen. It also shows a simple way in which to implement a “text fading” effect.

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
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey);

% Set the blend funciton for the screen
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the size of the on screen window in pixels
% For help see: Screen WindowSize?
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window in pixels
% For help see: help RectCenter
[xCenter, yCenter] = RectCenter(windowRect);

% Get the interframe interval
ifi = Screen('GetFlipInterval', window);

% Set some text properties
Screen('TextFont', window,'Helvetica');

% We will loop for a set amount of time to poll and report keyboard
% presses
numSecsDemo = 10;
numFramesDemo = round(numSecsDemo / ifi);

% We will flip on each frame
waitframes = 1;

% We will fade the letters over a decay time, this is just to make the demo
% fancy
fadeTimeSecs = 0.5;
fadeTimeFrames = round(fadeTimeSecs / ifi);
fadeColor = flipud(repmat(linspace(0.5, 1, fadeTimeFrames)', 3));
fading = false;

% Enable unified mode of KbName, so KbName accepts identical key names on
% all operating systems:
KbName('UnifyKeyNames');

% Escape key exits the demo
escapeKey = KbName('ESCAPE');
userExits = false;
demoDone = 0;

% Start the keyboard queue: this will log keypresses continously. We start
% the queue on the default keyboard device.
deviceIndex = [];
KbQueueCreate(deviceIndex)
KbQueueStart(deviceIndex);

% Stop the key presses vomiting out into the script or command window
ListenChar(-1);

% Flip to get a time stamp
vbl = Screen('Flip', window);

% Main loop
while demoDone == 0

    % If fading is false then no key has been pressed, so we just show the
    % instructions
    if fading == false

        % Draw the instruction
        Screen('TextSize', window, 60);
        DrawFormattedText(window, 'Press any key', 'center', screenYpixels * 0.15, [1 0.5 0.5]);

        % Check the queue for key presses.
        [pressed, firstPress] = KbQueueCheck(deviceIndex);

        % Check the keyboard for presses
        if pressed == 1

            % We get the first in the list of the keys that have been pressed,
            % in the case that multiple keys are pressed
            keyCode = find(firstPress, 1);
            theText = KbName(keyCode);

            % Turn on text and fading
            fading = true;
            fadeFrame = 1;

            % If escape is pressed signal end of the demo afterthe fade
            % time
            if escapeKey == keyCode
                userExits = true;
            end

        end

    end

    % If fading is true a key has been pressed
    if fading == true

        % Report the key pressed
        Screen('TextSize', window, 410);
        DrawFormattedText(window, theText, 'center', 'center', fadeColor(fadeFrame, :));

        % Increment the fade frame counter
        fadeFrame = fadeFrame + 1;

        % Check if we are at the end of the fading
        if fadeFrame > fadeTimeFrames

            % If so turn fading off
            fading = false;

            % If the user has pressed the escape key then this is also the
            % time to end the demo
            if userExits == 1
                demoDone = 1;
            end

        end

    end

    % Show at next retrace
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

end

% We are done, so release keyboard logging
KbQueueRelease(deviceIndex);

% Clear the screen
sca;
clear;

```
