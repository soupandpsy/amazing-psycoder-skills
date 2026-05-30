# Likert Scale

> Source: [likertScale](https://peterscarfe.com/likertScale.html)

Demonstrates an interactive Likert scale where a person can click on the points on the Likert scale using the mouse. Hovering over a button is animated, as is selecting a button. The demo also shows how to align text to various interface elements using the bounding boxes of the text.

```matlab
% Clear the workspace
close all;
clear;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');

% Draw to the external screen if avaliable
screenNumber = max(screens);

% Define colours
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
grey = GrayIndex(screenNumber);
darkGrey = grey * 0.8;

red = [white 0 0];
green = [0 white 0];
blue = [0 0 white];

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black,...
    [], [], [], [], [], kPsychNeedRetinaResolution);

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Change the blend function to draw an antialiased fixation point
% in the centre of the array
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% We will use a range of text sizes
textSize = 90;
smallTextSize = 60;

% Set just now to the standard text size
Screen('TextSize', window, textSize);

% Hide the mouse cursor
HideCursor;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Our scale will span a proportion of the screens x dimension
scaleLengthPix = screenYpixels / 1.5;
scaleHLengthPix = scaleLengthPix / 2;

% Coordiantes of the scale left and right ends
leftEnd = [xCenter - scaleHLengthPix yCenter];
rightEnd = [xCenter + scaleHLengthPix yCenter];
scaleLineCoords = [leftEnd' rightEnd'];

% Scale line thickness
scaleLineWidth = 10;

% Here we set the initial position of the mouse to the centre of the screen
SetMouse(xCenter, yCenter, window);

% Number of points on our likert scale
numScalePoints = 7;

% The points will be linearly spaced over the scale: here we make the xy
% coordinateas of each point
xPosScalePoints = linspace(xCenter - scaleHLengthPix, xCenter + scaleHLengthPix, numScalePoints);
yPosScalePoints = repmat(yCenter, 1, numScalePoints);
xyScalePoints = [xPosScalePoints; yPosScalePoints];

% Text labels for the scale
sliderLabels = {'Not Cool', 'Cool'};

% Get bounding boxes for the scale end label text
textBoundsAll = nan(2, 4);
for i = 1:2
    [~, ~, textBoundsAll(i, :)] = DrawFormattedText(window, sliderLabels{i}, 0, 0, white);
end

% Width and height of the scale end label text bounding boxs
textWidths = textBoundsAll(:, 3)';
halfTextWidths = textWidths / 2;
textHeights = range([textBoundsAll(:, 2) textBoundsAll(:, 4)], 2)';
halfTextHeights = textHeights / 2;

% Do the same for the numbers that we will put on the buttons. Here we
% toggle first to the smaller text size we will be using for the labels for
% the buttons then reinstate the standard text size
Screen('TextSize', window, smallTextSize);
numBoundsAll = nan(numScalePoints, 4);
for i = 1:numScalePoints
    [~, ~, numBoundsAll(i, :)] = DrawFormattedText(window, num2str(i), 0, 0, white);
end
Screen('TextSize', window, textSize);

% Width and height of the scale number text bounding boxs
numWidths = numBoundsAll(:, 3)';
halfNumWidths = numWidths / 2;
numHeights = [range([numBoundsAll(:, 2) numBoundsAll(:, 4)], 2)]';
halfNumHeights = numHeights / 2;

% Dimensions of the dots on our scale
dim = 40;
hDim = dim / 2;

% Position of the scale text so that it is at the ends of the scale but does
% not overlap with the scales points. Make sure it is also
% centered in the y dimension of the screen. To do this we used the bounding
% boxes of the text, plus a little gap so that the text does not completely
% edge the slider toggle in the x dimension
textPixGap = 50;
leftTextPosX = xCenter - scaleHLengthPix - hDim - textWidths(1) - textPixGap;
rightTextPosX = xCenter + scaleHLengthPix + hDim + textPixGap;

leftTextPosY = yCenter + halfTextHeights(1);
rightTextPosY = yCenter + halfTextHeights(2);

% The numbers are aligned to be directly under the relevent button (tops of
% their bounding boxes "numShiftDownPix" below the button y coordinate, and
% aligned laterally such that the centre of the text bounding boxes aligned
% with the x coordinate of the button
numShiftDownPix = 80;
xNumText = xPosScalePoints - halfNumWidths;
yNumText = yPosScalePoints + halfNumHeights + numShiftDownPix;

% Colors for the likert scale buttons when pressed (blue to red)
br = linspace(0, 1, numScalePoints);
bg = zeros(1, numScalePoints);
bb = abs(1 - br);
bRGB = [br; bg; bb];

% Number of frames to wait before updating the screen
waitframes = 1;

% Sync us and get a time stamp. We blank the window first to remove the
% text that we drew to get the bounding boxes.
Screen('FillRect', window, black)
vbl = Screen('Flip', window);

% Loop the animation until a key is pressed
while ~KbCheck(-1)

    % Get the current position of the mouse
    [mx, my, buttons] = GetMouse(window);

    % Check if the mouse is within any of the circles: this is done by
    % seeing if the Euclidean distance between the mouse and the buttons in
    % less than their radius. The mouse can only overlap with one, as the
    % buttons do not overlap.
    inCircles = sqrt((xPosScalePoints - mx).^2 + (yPosScalePoints - my).^2) < hDim;

    % Identify the index of the circle if we are in one and get its coordinates
    weInCircle = sum(inCircles) > 0;
    if weInCircle == 1
        [~, posCircle] = max(inCircles);
        coordsCircle = xyScalePoints(:, posCircle);
    end

    % Draw the scale line
    Screen('DrawLines', window, scaleLineCoords, scaleLineWidth, grey);

    % Text for the ends of the slider
    DrawFormattedText(window, sliderLabels{1}, leftTextPosX, leftTextPosY, blue);
    DrawFormattedText(window, sliderLabels{2}, rightTextPosX, rightTextPosY, red);

    % Draw the title for the slider
    DrawFormattedText(window, 'Coolness Rating Scale', 'center', screenYpixels * 0.25, white);

    % If we are in a circle identify it with a frame (exploiting drawing
    % order of operations)
    if weInCircle == 1
        Screen('DrawDots', window, coordsCircle, dim * 1.2, white, [], 2);
    end

    % Draw the likert scale points
    Screen('DrawDots', window, xyScalePoints, dim, darkGrey, [], 2);

    % If we are clicking a circle we flag it (exploiting drawing
    % order of operations)
    if weInCircle == 1 && sum(buttons) > 0

        % Highlight the pressed button
        Screen('DrawDots', window, coordsCircle, dim * 1.2, bRGB(:, posCircle), [], 2);

        % Signal button pressed
        DrawFormattedText(window, ['Button ' num2str(posCircle) ' being pressed'], 'center', screenYpixels * 0.75, bRGB(:, posCircle));

    end

    % Draw the numbers for the scale: First toggling to the smaller text
    % size and then reverting back to the standard text size
    Screen('TextSize', window, smallTextSize);
    for thisNum = 1:numScalePoints
        DrawFormattedText(window, num2str(thisNum), xNumText(thisNum), yNumText(thisNum), white);
    end
    Screen('TextSize', window, textSize);

    % Draw a white dot where the mouse cursor is
    Screen('DrawDots', window, [mx my], 10, white, [], 2);

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

end

% Clear the screen
sca;

```
