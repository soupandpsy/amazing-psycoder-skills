# Structure From Motion

> Source: [structureFromMotion](https://peterscarfe.com/structureFromMotion.html)

Shows how to render a 3D rotating cylinder with moving dots. Structure from motion, in this instance, is ambiguous about the depth of the cylinder, as the dots are projected orthographically onto a 2D surface (your screen). The stimulus will therefore be perceived to ‘flip’ rotation direction. In fact, the stimulus is quad-stable i.e. there are four possible stable interpretations of its depth structure.

```matlab
% Clear the workspace
clear;
close all;
sca;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

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

% We assume some screen dimensions here so that the stimulus will fit
% nicely on the screen. Obviously this means that the dimensions we state
% here will only be correct if you screen happens to be the same size.
screenYcm = heightMM / 10;
screenXcm = widthMM / 10;
pixPerCm = mean([screenXpix / screenXcm screenYpix/ screenYcm]);

% Set the blend function so that we get nice antialised edges to the dots
% defining our cyliner
Screen('BlendFunction', window, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);


%--------------------------------------------------------------------------
%                   Stimulus information
%--------------------------------------------------------------------------

% Cylinder height, width and radius
cylHeight = 14;
cylHalfHeight = cylHeight / 2;
cylWidth = 4;
cylRadius = cylWidth / 2;

% Numer of dots to place over the surface of the cylinder
numDots = 250;

% Dot track centres over the height of the cylinder
ypos = (rand(1, numDots) .* 2 - 1) .* cylHalfHeight .* pixPerCm;

% Randomly assign the dots angles. This determines their X position on the
% screen. We are using ortographic projection, so the dots do not have a Z
% position.
angles = rand(1, numDots) .* 360;

% Set the dot size in pixels
dotSizePixels = 7;

% We will update the stimulus on each frame
waitframes = 1;

% Get a flip to sync our timing
vbl = Screen(window, 'Flip');


%--------------------------------------------------------------------------
%                           Drawing Loop
%--------------------------------------------------------------------------

% Stimulus drawing loop (exits when any button is pressed)
while ~KbCheck

    % Calculate the X screen position of the dots (note we have to convert
    % from degrees to radians here.
    xpos = cos(angles .* (pi / 180)) * cylWidth.* pixPerCm;

    % Draw the dots. Here we set them to white, determine the point at
    % which the dots are drawn relative to, in this case our screen center.
    % And set anti-aliasing to 1. This gives use smooth dots. If you use 0
    % instead you will get squares. And if you use 2 you will get nicer
    % anti-aliasing of the dots.
    Screen('DrawDots', window, [xpos; ypos], dotSizePixels, white, center, 1);

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the angle of the dots by one degree per frame
    angles = angles + 1;

end

% Clean up and leave the building
sca;

```
