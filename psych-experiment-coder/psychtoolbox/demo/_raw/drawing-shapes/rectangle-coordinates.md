# Rectangle Coordinates

> Source: [rectangleCoordinates](https://peterscarfe.com/rectangleCoordinates.html)

This demo is rather complex as it consolidates a bunch of the previous demos, so have a look at the movie to see what can be done. When the mouse cursor (white dot) is contacting either the top-left or bottom-right corner circles of the rectangle, the dot defining the corner circle will turn from blue to red. Clicking on one of the corner circles highlights it with a white outline ring. Clicking and holding the mouse button down on one of the corner circles allows one to “drag” the selected corner circle around the screen, which also alters the shape of the rectangle. The rectangle has minimum specified dimensions, so cannot be shrunk beyond this minimum limit.

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
grey = white / 2;

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Change the blend function to draw an antialiased stimuli
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Hide the standard computer as we will be rendering our own
HideCursor;

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Make a base Rect a proportion of the screen
dim = round(screenYpixels / 5);
baseRect = [0 0 dim dim];

% Define red and blue
blue = [0 0 1];
red = [1 0 0];

% Here we set the initial position of the mouse to be in the centre of the
% screen
SetMouse(xCenter, yCenter, window);

% We now set the squares initial position to the centre of the screen
sx = xCenter;
sy = yCenter;

% Center the rectangle on screen position
centeredRect = CenterRectOnPointd(baseRect, sx, sy);
topLeft = [centeredRect(1) centeredRect(2)]';
bottomRight = [centeredRect(3) centeredRect(4)]';

% Diameter of the dots showing the top left and bottom right corners
cornerDim = 40;

% Minimum size of the rect
minDim = 60;

% Signal not to draw the rings around the corner dots
drawTopLeftRing = 0;
drawBottomRightRing = 0;

% Set the previous ring drawing cue to zero
drawTopLeftRingPrevious = 0;
drawBottomRightRingPrevious = 0;

% Signal the the person is not holding down the mouse button
leftPressed = 0;
rightPressed = 0;

% Offset cue to allow nice dragging effect
topLeftOffsetSet = 0;
bottomRightOffsetSet = 0;

% Sync us and get a time stamp
vbl = Screen('Flip', window);
waitframes = 1;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Loop the animation until a key is pressed
while ~KbCheck

    % Cache the previous centered rect: we revert to this if the user trys
    % to turn the rectangle inside out
    previousCentredRect = centeredRect;

    % Get the current position of the mouse
    [mx, my, buttons] = GetMouse(window);

    % Offsets between the cursor and the two control points
    offsetTopLeft = topLeft' - [mx my];
    offsetBottomRight = bottomRight' - [mx my];

    % Calculate the screen distance in pixels bewteen the mouse cursor and
    % each of the corners
    distTopLeft = EuclidDist([mx, my], topLeft');
    distBottomRight = EuclidDist([mx, my], bottomRight');

    % Calculations for the top left corner
    if distTopLeft <= cornerDim / 2 || leftPressed == 1

        % If the mouse is in the circle color it red
        topLeftColor = red;

        % If the button is pressed draw a ring around the circle
        if sum(buttons) > 0
            drawTopLeftRing = 1;
        else
            drawTopLeftRing = 0;
        end

        % If we are drawing a ring both this frame and last then move the
        % coordinates of the corner that is being clicked
        if drawTopLeftRingPrevious == 1 && drawTopLeftRing == 1

            % We are pressing and holding the mouse button, so we cache the
            % offset between the mouse cursor and the centre of the pressed
            % circle
            if topLeftOffsetSet == 0
                theOffset = offsetTopLeft;
                topLeftOffsetSet = 1;
            end

            % Update corner coordinates
            centeredRect(1:2) = [mx , my] + theOffset;

            % Signal the person is depressing the mouse button on the top
            % left corner
            leftPressed = 1;

        else

            % Signal the person is not depressing the mouse button on the
            % top left corner
            leftPressed = 0;
            topLeftOffsetSet = 0;

        end

        % Cache this value for the next frame
        drawTopLeftRingPrevious = drawTopLeftRing;

    else

        % If the mouse is not in the circle color it blue
        topLeftColor = blue;

    end

    % Calculations for the bottom right corner
    if distBottomRight <= cornerDim / 2 || rightPressed == 1

        % If the mouse is in the circle color it red
        bottomRightColor = red;

        % If the button is pressed draw a ring around the circle
        if sum(buttons) > 0
            drawBottomRightRing = 1;
        else
            drawBottomRightRing = 0;
        end

        % If we are drawing a ring both this frame and last then move the
        % coordinates of the coorner that is being clicked
        if drawBottomRightRingPrevious == 1 && drawBottomRightRing == 1

            % We are pressing and holding the mouse button, so we cache the
            % offset between the mouse cursor and the centre of the pressed
            % circle
            if bottomRightOffsetSet == 0
                theOffset = offsetBottomRight;
                bottomRightOffsetSet = 1;
            end

            % Update corner coordinates
            centeredRect(3:4) = [mx, my] + theOffset;

            % Signal the person is depressing the mouse button on the
            % bottom right
            rightPressed = 1;

        else
            % Signal the person is not depressing the mouse button on the
            % bottom right corner
            rightPressed = 0;
            bottomRightOffsetSet = 0;

        end

        % Cache this value for the next frame
        drawBottomRightRingPrevious = drawBottomRightRing;

    else

        % If the mouse is not in the circle color it blue
        bottomRightColor = blue;

    end

    % Here we gauard against the user trying to turn the rectangle inside
    % out - this will break the drawing code
    if (centeredRect(3) - centeredRect(1)) < minDim || ...
            (centeredRect(4) - centeredRect(2)) < minDim
        centeredRect = previousCentredRect;
    end

    % Coordinates of the movable corners on this frame
    topLeft = [centeredRect(1) centeredRect(2)]';
    bottomRight = [centeredRect(3) centeredRect(4)]';

    % Make the matrices we need for the corner dots
    cornerCoords = [topLeft bottomRight];
    cornerColors = [topLeftColor' bottomRightColor'];

    % Draw the rect to the screen
    Screen('FillRect', window, grey, centeredRect);

    % Draw the appropriate ring of the corner is clicked
    if drawTopLeftRing == 1
        Screen('DrawDots', window, topLeft', cornerDim * 1.2, white, [], 2);
    end

    if drawBottomRightRing == 1
        Screen('DrawDots', window, bottomRight', cornerDim * 1.2, white, [], 2);
    end

    % Draw the position of the active corners
    Screen('DrawDots', window, cornerCoords, cornerDim, cornerColors, [], 2);

    % Draw a white dot where the mouse cursor is
    Screen('DrawDots', window, [mx my], 10, white, [], 2);

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

end

% Clear the screen
sca;


% Simple function to calculate 2D euclidean distance
function dist = EuclidDist(p1, p2)

    dist = sqrt(sum((p1 - p2).^2));

end

```
