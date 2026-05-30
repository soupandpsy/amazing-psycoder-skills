# Analog Clock

> Source: [analogClock](https://peterscarfe.com/analogClock.html)

This is the same as "

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

% Define the colours
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
grey = white / 2;
darkGrey = white / 8;
lightGrey = white / 2.1;

red = [white 0 0];
green = [0 white 0];
blue = [0 0 white];

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Set up alpha-blending for smooth (anti-aliased) lines
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Set the text properties
Screen('TextFont', window, 'Ariel');
Screen('TextSize', window, 75);

% Get bounding boxes for all of the letters we will use for our clock
numNums = 12;
textBoundsAll = nan(numNums, 4);
for i = 1:12
    [~, ~, textBoundsAll(i, :)] = DrawFormattedText(window, num2str(i), 0, 0, white);
end

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Diameter of the clock (defined relative to the screen
clockDiameter = screenYpixels * 0.8;
clockRadius = clockDiameter / 2;

% Hours mins and secs
numHours = 12;
numMins = 60;

% Angles for hours minutes and secs
anglePerHour = 360 / numHours;
anglePerMin = 360 / numMins;
anglePerSec = anglePerMin;

% Initial colour for the letters on the clock
numColour = rand(1, 3) ./ 2 + 0.5;

% Scale for various elemnts of the clock
clockFaceScale = 1.2;
hourHandScale = .7;
minHandScale = .8;
secHandScale = .9;
clockTickScale = .95;

% Get an initial timestamp
vbl = Screen('Flip', window);
waitframes = 1;
time = 0;

% Endless loop in which we scale the size of the texture
while ~KbCheck

    % Get the clock
    matClock = clock;
    yearNum = matClock(1);
    monthNum = matClock(2);
    dayNum = matClock(3);
    hourNum = matClock(4);
    minsNum = matClock(5);
    secsNum = round(matClock(6));

    % Draw the outline of the clock, we scale it so that it fits nicely on
    % the screen
    clockRect = CenterRectOnPointd([0 0 clockDiameter clockDiameter] * clockFaceScale, xCenter, yCenter);
    Screen('FillOval', window, darkGrey,...
        clockRect, clockDiameter * 1.1);
    Screen('FrameOval', window, lightGrey, clockRect, 6);

    % Draw the clock tick lines
    for i = 0:numMins - 1

        % Increment angle in the loop
        minAngle = i * anglePerMin;

        % End position of the tick
        xposEnd = clockRadius * clockFaceScale * sind(minAngle);
        yposEnd = clockRadius * clockFaceScale * cosd(minAngle) * -1;

        % Start position of the tick
        xposStart = clockRadius * clockFaceScale * clockTickScale * sind(minAngle);
        yposStart = clockRadius * clockFaceScale * clockTickScale * cosd(minAngle) * -1;

        % We want a white tick on the quarter hours, this is therfore
        % modulus 15 in minutes.
        if mod(i, 15)
            Screen('DrawLines', window, [xposStart yposStart; xposEnd yposEnd]', 6, lightGrey, [xCenter yCenter], 2);
        else
            Screen('DrawLines', window, [xposStart yposStart; xposEnd yposEnd]', 8, white, [xCenter yCenter], 2);
        end

    end

    % Draw the clock numbers
    for i = 1:numHours

        % X and Y posiitons of our clock numbers
        xpos = xCenter - clockRadius * sind(anglePerHour * i - 180);
        ypos = yCenter + clockRadius * cosd(anglePerHour * i - 180);

        % Draw the number (notice that we use the text bounding boxes to
        % make sure that the text is positioned nicely)
        DrawFormattedText(window, num2str(i),...
            xpos - ((textBoundsAll(i, 3) - textBoundsAll(i, 1)) / 2),...
            ypos + ((textBoundsAll(i, 4) - textBoundsAll(i, 2)) / 2), numColour);

    end

    % Draw the hour hand. Hours on a clock are modulus 12, and the matlab
    % code we use outputs time formatted as a 24hr clock
    hourNum = mod(hourNum, 12);
    hourAngle = hourNum * anglePerHour;
    xposHour = clockRadius * hourHandScale * sind(hourAngle);
    yposHour = clockRadius * hourHandScale * cosd(hourAngle) * -1;
    Screen('DrawLines', window, [0 0; xposHour yposHour]', 18, green, [xCenter yCenter], 2);
    Screen('DrawDots', window, [xposHour yposHour]', 20, green, [xCenter yCenter], 2);

    % Draw the minute hand
    minAngle = minsNum * anglePerMin;
    xposMin = clockRadius * minHandScale * sind(minAngle);
    yposMin = clockRadius * minHandScale * cosd(minAngle) * -1;
    Screen('DrawLines', window, [0 0; xposMin yposMin]', 12, red, [xCenter yCenter], 2);
    Screen('DrawDots', window, [xposMin yposMin]', 20, red, [xCenter yCenter], 2);

    % Draw the second hand
    secAngle = secsNum * anglePerSec;
    xposSec = clockRadius * secHandScale * sind(secAngle);
    yposSec = clockRadius * secHandScale * cosd(secAngle) * -1;
    Screen('DrawLines', window, [0 0; xposSec yposSec]', 2, blue, [xCenter yCenter], 2);
    Screen('DrawDots', window, [xposSec yposSec]', 20, blue, [xCenter yCenter], 2);

    % Draw a dot in the centre of the clock
    Screen('DrawDots', window, [0 0]', 25, white, [xCenter yCenter], 2);

    % Get an initial screen flip for timing
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment time by the ifi and if a second has elapsed change the
    % coulurs of the letters
    time = time + ifi;
    if time >= 1
        numColour = rand(1, 3) ./ 2 + 0.5;
        time = 0;
    end

end

% Clear the screen
sca;

```
