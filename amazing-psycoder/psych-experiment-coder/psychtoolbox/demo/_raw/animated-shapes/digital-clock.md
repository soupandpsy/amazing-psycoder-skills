# Digital Clock

> Source: [digitalClock](https://peterscarfe.com/digitalClock.html)

Shows you how to poll the current date and time with Matlab, format the returned numbers into text strings and then present them on screen like a digital clock. The code uses numerical, string and cell data so is useful in seeing how to format and index these different types of data structure. 

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

% Get the vertical refresh rate of the monitor
ifi = Screen('GetFlipInterval', window);

% Retreive the maximum priority number and set max priority
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Set the blend funciton for the screen
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Text properties
Screen('TextSize', window, 80);
Screen('TextFont', window, 'Courier');

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Months of the year
monthsText = {'January', 'February', 'March', 'April', 'May', 'June',...
    'July', 'August', 'September', 'October', 'November', 'December'};

% Flip outside of the loop to get a time stamp
vbl = Screen('Flip', window);

% We will refresh the screen each frame
waitframes = 1;

% Time in frames we want the blinkers to flash
flashTimeFrames = 1 / ifi * 0.5;

% Toggle for the seperators
sepText = {' ', ':'};
frameCountChange = 0;

% We will set the colour of the numbers to be a red-ish colour like a
% digital clock
numColour = [0.9 0.1 0.1];

while ~KbCheck

    % Get the clock
    matClock = clock;
    yearNum = matClock(1);
    monthNum = matClock(2);
    dayNum = matClock(3);
    hourNum = matClock(4);
    minsNum = matClock(5);
    secsNum = round(matClock(6));

    % Add a zero to minutes and seconds of the clock if needed, as this is
    % how a digital clock generally displays the time
    if minsNum < 10
        minsAdd = '0';
    else
        minsAdd = '';
    end

    if secsNum < 10
        secsAdd = '0';
    else
        secsAdd = '';
    end

    % Get the date postfix correct for the date
    if dayNum == 1
        dayText = 'st';
    elseif dayNum == 2
        dayText = 'nd';
    elseif dayNum == 3
        dayText = 'rd';
    else
        dayText = 'th';
    end

    % Year line
    yearMonthLineText = [monthsText{monthNum} ' ' num2str(dayNum) dayText ' ' num2str(yearNum)];

    % Time line
    timeLineText = [num2str(hourNum) ':' minsAdd num2str(minsNum) sepText{1} secsAdd num2str(secsNum)];

    % Draw to the screen
    DrawFormattedText(window, timeLineText, 'center', yCenter * 0.9, numColour);
    DrawFormattedText(window, yearMonthLineText, 'center', yCenter * 1.1, numColour);

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the frame counter
    frameCountChange = frameCountChange + 1;

    % Do the toggle for the seperator and counter
    if frameCountChange >= flashTimeFrames
        frameCountChange = 0;
        sepText = fliplr(sepText);
    end

end

% Clear the screen
sca;

```
