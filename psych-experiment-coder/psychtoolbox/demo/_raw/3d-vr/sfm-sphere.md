# SFM Sphere

> Source: [sfmSphere](https://peterscarfe.com/sfmSphere.html)

This demo show you how make a structure from motion sphere with dots uniformly distributed over its surface. We modulate the size of the dots dependent upon their depth. It shows it shows the relationship between 3D to 2D coordinates for Orthographic projection.

```matlab
% Clear the workspace
clear;
sca;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Set numbers generated to be random
rng('shuffle');


%--------------------------------------------------------------------------
%                       Screen initialisation
%--------------------------------------------------------------------------

% Find the screen to use for displaying the stimuli. By using "max" this
% will display on an external monitor if one is connected.
screenid = max(Screen('Screens'));

% Determine the values of black and white
black = BlackIndex(screenid);
white = WhiteIndex(screenid);

% Set up our screen
[window, windowRect] = PsychImaging('OpenWindow', screenid, black, [], 32, 2);

% Get the vertical refresh rate of the monitor
ifi = Screen('GetFlipInterval', window);

% Get the width and height of the window in pixels
[screenXpix, screenYpix] = Screen('WindowSize', window);

% Determine the center of the screen. We will need this later when we draw
% our dots.
[center(1), center(2)] = RectCenter(windowRect);

% Queries the display size in mm as reported by the operating system. Note
% that there are some complexities here. See Screen DisplaySize? for
% information. So always measure your screen size directly. We just use the
% reported value for the purposes of this demo.
[widthMM, heightMM] = Screen('DisplaySize', screenid);

% We assume that the reported screen dimensions are correct and use these
% to size our stimulus.
screenYcm = heightMM / 10;
screenXcm = widthMM / 10;
pixPerCm = mean([screenXpix / screenXcm screenYpix/ screenYcm]);

% Set the blend function so that we get nice antialised edges to the dots
% defining our cyliner
Screen('BlendFunction', window, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

% Set drawing to maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);


%--------------------------------------------------------------------------
%                   Stimulus information
%--------------------------------------------------------------------------

% Radius of the sphere in cm
sphereRadius = 7;

% Maximum depth in pixels
maxDepthPix = sphereRadius * pixPerCm;

% Surface area of the sphere
sphereSurfArea = 4 * pi * sphereRadius^2;

% Specify the number of dots we want on the sphere
dotDensity = 6;
numDots = round(dotDensity * sphereSurfArea);

% Uniformly distribute the points in spherical space
th = 2 .* pi * rand(1, numDots);
ph = asin(-1 + 2 .* rand(1, numDots));

% Convert the point coordinates into cartesian space: we define things in
% 3D and then just use the X and Y coordinates as we are doing an
% Orthographic projection
[sphereCoordsX, sphereCoordsY, sphereCoordsZ] = sph2cart(th, ph, sphereRadius);

% Finally convert to pixels
sphereCoordsX = sphereCoordsX .* pixPerCm;
sphereCoordsY = sphereCoordsY .* pixPerCm;
sphereCoordsZ = sphereCoordsZ .* pixPerCm;

% Maximum and minimum depth possible: we will use this to scale the size of
% the dots
minMaxDepth = [0 1] * sphereRadius * pixPerCm;

% The dot coordinates: these coordinates are 3D
dotCoordsAll = [sphereCoordsX; sphereCoordsY; sphereCoordsZ];

% Set the dot size in pixels
dotMinSizePixels = 4;
dotMaxSizePixels = 8;

% We will randomly color the dots
dotColors = rand(3, numDots) .* white;

% We will update the stimulus on each frame
waitframes = 1;


%--------------------------------------------------------------------------
%                           Drawing Loop
%--------------------------------------------------------------------------

% Start angle and the angle in degrees that we will rotate per frame
angle = 0;
degPerFrame = 0.3;
rotYmat = roty(degPerFrame);

% Get a flip to sync our timing
vbl = Screen(window, 'Flip');

% Do the rendering
while ~KbCheck

    % This is orthographic projection, so we get only the dots which are in
    % front of the plane of the screen
    behindCue = dotCoordsAll(3, :) >= 0;
    dotCoords = dotCoordsAll(1:2, behindCue == 1);

    % Dot sizes for this frame, we add the min and max size for the
    % rescaling operation and then drop them for rendering
    dotDepths = [dotCoordsAll(3, behindCue == 1) minMaxDepth];
    dotsSizes = rescale(dotDepths, dotMinSizePixels, dotMaxSizePixels);
    dotsSizes = dotsSizes(1:end-2);

    % Colors of the dots that we will display
    theDotColors = dotColors(:, behindCue == 1);

    % Draw the dots
    Screen('DrawDots', window, dotCoords, dotsSizes,...
        theDotColors, [screenXpix / 2 screenYpix / 2], 2);

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the angle and rotate the 3D coordinates: there are much
    % more efficient ways in which to do this which are shown in subsequent
    % demos. Here we just do a simple loop so that you can get the
    % numerical values on each frame.
    dotCoordsAll = doRotation(dotCoordsAll, rotYmat, numDots);

end

% Wait for a button press to exit the demo
sca;

% Function to rotate the dots
function dotCoordsAll = doRotation(dotCoordsAll, rotYmat, numDots)

for i = 1:numDots
    dotCoordsAll(:, i) = dotCoordsAll(:, i)' * rotYmat;
end

end

```
