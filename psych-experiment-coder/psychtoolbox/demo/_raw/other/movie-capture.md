# Movie Capture

> Source: [movieCaptureDemo](https://peterscarfe.com/movieCaptureDemo.html)

I am often asked how I capture movies of PTB for the website. This is how I do it. This demo is the same as "

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

% Open an on screen window. If we are on a mac we request native retina
% resolution to avoid only part of the movie being recorded.
if IsOSX
    [window, windowRect] = PsychImaging('OpenWindow', screenNumber, black,...
        [], [], [], [], [], kPsychNeedRetinaResolution);
else
    [window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);
end

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

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Our sqaures will have sides 150 pixels in length, as we are going to be
% rotating these around the origin using OpenGL commands we use -150 to
% +150 for the X and Y coordinates
dim = 300 / 2;
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

% Here we set up a movie pointer, the string that you see at the end of
% this command specifies the codec that we will use in recording our video.
% Video recording is handled via GStreamer via PTB. I have found that this
% codec plays nicely for my purposes. Note that the codec will determine
% which players will be able to play the movie. This codec will not open in
% macOS QuickTime, but does fin in VLC.
moviePtr = Screen('CreateMovie', window, 'rotatingSquaresDemo.mp4', ...
    [], [], [], ':CodecType=avenc_mpeg4');

% For this demo we will record a 10 second movie
numSecs = 10;
numFrames = round(numSecs / ifi);

% Animation loop
for frame = 1:numFrames

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

    % Now that we have flipped to the screen we add this displayed window
    % to our movie
    Screen('AddFrameToMovie', window);

    % Increment the rotation angles of the sqaures now that we have drawn
    % to the screen
    angles = angles + degPerFrame;

end

% We are done with movie recording now so we finalise and save
Screen('FinalizeMovie', moviePtr);

% Clear the screen
sca;

```
