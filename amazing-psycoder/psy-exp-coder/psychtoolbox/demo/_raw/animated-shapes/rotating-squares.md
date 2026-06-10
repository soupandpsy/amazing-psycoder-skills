# Rotating Squares

> Source: [rotatingSquares](https://peterscarfe.com/rotatingSquares.html)

Animates three different coloured rotating squares using basic OpenGL commands. OpenGL underlies the presentation of visual stimuli in PTB and there are a number of ways in which to directly access OpenGL functionality. This is one of the great powers of PTB.

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

% Set the blend funciton for the screen
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Our sqaures will have sides 150 pixels in length, as we are going to be
% rotating these around the origin using OpenGL commands we use -75 to +75
% for the X and Y coordinates
dim = 150 / 2;
baseRect = [-dim -dim dim dim];

% For this Demo we will draw 3 squares
numRects = 3;

% We will randomise the intial rotation angles of the squares. OpenGL uses
% Degrees (not Radians) in these commands, so our angles are in degrees
angles = rand(1, numRects) .* 360;

% We will set the rotations angles to increase by 1 degree on every frame
degPerFrame = 1;

% We position the squares in the middle of the screen in Y, spaced equally
% scross the screen in X
posXs = [screenXpixels * 0.25 screenXpixels * 0.5 screenXpixels * 0.75];
posYs = ones(1, numRects) .* (screenYpixels / 2);

% Finally, we will set the colors of the sqaures to red, green and blue
colors = [1 0 0; 0 1 0; 0 0 1];

% Sync us and get a time stamp
vbl = Screen('Flip', window);
waitframes = 1;

% Animation loop
while ~KbCheck

    % With this basic way of drawing we have to translate each square from
    % its screen position, to the coordinate [0 0], then rotate it, then
    % move it back to its screen position.
    % This is rather inefficient when drawing many rectangles at high
    % refresh rates. But will work just fine for simple drawing tasks.
    % For a much more efficient way of drawing rotated squares and rectangles
    % have a look at the texture tutorials
    for i = 1:numRects

        % Get the current squares position ans rotation angle
        posX = posXs(i);
        posY = posYs(i);
        angle = angles(i);

        % Translate, rotate, re-tranlate and then draw our square
        Screen('glPushMatrix', window)
        Screen('glTranslate', window, posX, posY)
        Screen('glRotate', window, angle, 0, 0);
        Screen('glTranslate', window, -posX, -posY)
        Screen('FillRect', window, colors(i,:),...
            CenterRectOnPoint(baseRect, posX, posY));
        Screen('glPopMatrix', window)

    end

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the rotation angles of the sqaures now that we have drawn
    % to the screen
    angles = angles + degPerFrame;

end

% Clear the screen
sca;

```
