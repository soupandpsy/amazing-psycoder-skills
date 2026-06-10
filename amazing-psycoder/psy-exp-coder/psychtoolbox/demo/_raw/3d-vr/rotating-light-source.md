# Rotating Light Source

> Source: [rotatingLightSource](https://peterscarfe.com/rotatingLightSource.html)

In this demo we render a light source rotating around a sphere. You will be able to see how the changing light-source position effects the luminance of the spheres surface (given an assumed lighting model) We also introduce the concept of “display lists”, which can be used to speed up rendering.

```matlab
% Clear the workspace
close all;
clear;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Find the screen to use for display
screenid = max(Screen('Screens'));

% Initialise OpenGL
InitializeMatlabOpenGL;

% We will use multisampling to get nice smooth edges (reduce this number to
% zero if you computer can't handle four samples)
numSamples = 6;

% Open the main window with multi-sampling for anti-aliasing
[window, windowRect] = PsychImaging('OpenWindow', screenid, 0, [],...
    32, 2, [], numSamples,  []);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Start the OpenGL context
Screen('BeginOpenGL', window);

% For this demo we will assume our screen is 0.3m (30cm) in height. The units are
% essentially arbitary with OpenGL as it is all about ratios. But it is
% nice to define things in normal scale numbers
ar = windowRect(3) / windowRect(4);
screenHeight = 0.3;
screenWidth = screenHeight * ar;

% Enable lighting See Chapter 5 of the OpenGL "red book"
glEnable(GL.LIGHTING);

% Force there to be no ambient light (OpenGL default is for there to be
% some, however for this demo we want to fully demonstrate directional
% lighting)
glLightModelfv(GL.LIGHT_MODEL_AMBIENT, [0 0 0 1]);

% Define a local light source
glEnable(GL.LIGHT0);

% Defuse light only
glLightfv(GL.LIGHT0, GL.DIFFUSE, [1 1 1 1]);

% Point the light at the origin (this is where we will place our sphere)
glLightfv(GL.LIGHT0, GL.SPOT_DIRECTION, [0 0 0]);

% Enable proper occlusion handling via depth tests
glEnable(GL.DEPTH_TEST);

% Allow normalisation
glEnable(GL.NORMALIZE);

% Our light source is going to circle around the origin [0 0 0], where our
% ball will be positioned. Here we set the radius of the circle and use
% trig to calculate its X and Z position for an angle of zero.]
% Note: the lights Y position
% will be fixed, so that the light is always in the plane of the sphere.
% all angles will be specified in degrees.
lightRadius = 1;
lightAngle = 0;
lightZpos = lightRadius * cosd(lightAngle);
lightXpos = lightRadius * sind(lightAngle);

% Lets set up a projection matrix, the projection matrix defines how images
% in our 3D simulated scene are projected to the images on our 2D monitor
glMatrixMode(GL.PROJECTION);
glLoadIdentity;

% Calculate the field of view assming that our object is at at "dist" away
% from our camera
dist = 0.4;
angle = 2 * atand(screenHeight / dist);

% Set up our perspective projection. This is defined by our field of view
% (here given by the variable "angle") and the aspect ratio of our frustum
% (our screen) and two clipping planes. These define the minimum and
% maximum distances allowable here 1cm and 10m.
gluPerspective(angle, ar, 0.01, 10);

% Setup modelview matrix: This defines the position, orientation and
%  direction of the virtual camera that will  look at our scene with
glMatrixMode(GL.MODELVIEW);
glLoadIdentity;

% Location of the camera
cam = [0 0 dist];

% Set our camera to be looking directly down the -Z axis (depth) of our
% coordinate system
fix = [0 0 -1];

% Define "up"
up = [0 1 0];

% Here we set up the attributes of our camera using the variables we have
% defined in the last three lines of code
gluLookAt(cam(1), cam(2), cam(3), fix(1), fix(2), fix(3), up(1), up(2), up(3));

% Set background color to 'black' (the 'clear' color)
glClearColor(0, 0, 0, 0);

% Clear out the backbuffer
glClear;

% Size of our sphere (12cm)
dim = 0.12;

% Make a display list with our red ball. Our red ball is not changing at
% all, so compiling it in a display list can help with rendering speed. In
% reality it probably does not make a huge difference to such a simple
% stimulus, but can help greatly when rendering complex stimuli.
%
% Chapter 7 of the OpenGL "red book"
sphereList = glGenLists(1);
glNewList(sphereList, GL.COMPILE);

% Our ball will reflect only diffuse light as that is all that is coiming from
% our light source.
glMaterialfv(GL.FRONT_AND_BACK, GL.DIFFUSE, [0.8 0.0 0 1]);

% Here we use the GLUT library to define a simple sphere
glutSolidSphere(dim, 100, 100);

glEndList;

% End the OpenGL context now that we have finished setting things up
Screen('EndOpenGL', window);

% Set the frames to wait to one
waitframes = 1;

% Get a time stamp with a flip
vbl = Screen('Flip', window);


% The simulation will loop until you press any key on the keyboard
while ~KbCheck

    % Begin the OpenGL context now we want to issue OpenGL commands again
    Screen('BeginOpenGL', window);

    % Position the light-source for this run of the rendering loop
    glLightfv(GL.LIGHT0, GL.POSITION, [lightXpos 0 lightZpos 1]);

    % To start with we clear everything
    glClear;

    % Next we draw our sphere by calling our sphere display list
    glPushMatrix;
    glCallList(sphereList);
    glPopMatrix;

    % End the OpenGL context now that we have finished doing OpenGL stuff.
    % This hands back control to PTB
    Screen('EndOpenGL', window);

    % Show rendered image at next vertical retrace
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the light position by a degree for the next rendering loop
    lightAngle = lightAngle + 1;
    lightZpos = lightRadius * cosd(lightAngle);
    lightXpos = lightRadius * sind(lightAngle);

end

% Clear up and leave the building
sca

```
