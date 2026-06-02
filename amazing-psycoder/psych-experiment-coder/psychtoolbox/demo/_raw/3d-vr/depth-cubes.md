# Depth Cubes

> Source: [depthCubes](https://peterscarfe.com/depthCubes.html)

This demo builds directly on previous demos by rendering the cubes randomly moving in and out of depth (the z dimension) following a sine wave function.

```matlab
% Clear the workspace
close all;
clear;
sca;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Find the screen to use for display
screenid = max(Screen('Screens'));

% Initialise OpenGL
InitializeMatlabOpenGL;

% Open the main window with multi-sampling for anti-aliasing. Multisampling
% is a brute force but effective way in which to avoid aliasing of computer
% generated objects. PTB clamps the requested number of multisamples to the
% maximum allowed by the computer if more are requested. See help AntiAliasing
numMultiSamples = 6;
[window, windowRect] = PsychImaging('OpenWindow', screenid, 0, [],...
    32, 2, [], numMultiSamples,  []);

% Set the priority of PTB to max
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Start the OpenGL context (you have to do this before you issue OpenGL
% commands such as we are using here)
Screen('BeginOpenGL', window);

% For this demo we will assume our screen is 30cm in height. The units are
% essentially arbitary with OpenGL as it is all about ratios. But it is
% nice to define things in normal scale numbers. You would obviously want
% to define this properly for your setup.
ar = windowRect(3) / windowRect(4);
screenHeight = 30;
screenWidth = screenHeight * ar;

% Enable lighting
glEnable(GL.LIGHTING);

% Define a local light source
glEnable(GL.LIGHT0);

% Enable proper occlusion handling via depth tests
glEnable(GL.DEPTH_TEST);

% Lets set up a projection matrix, the projection matrix defines how images
% in our 3D simulated scene are projected to the images on our 2D monitor
glMatrixMode(GL.PROJECTION);
glLoadIdentity;

% Calculate the field of view in the y direction assuming a distance to the
% objects of 100cm
dist = 100;
angle = 2 * atand(screenHeight / dist);

% Set up our perspective projection. This is defined by our field of view
% (here given by the variable "angle") and the aspect ratio of our frustum
% (our screen) and two clipping planes. These define the minimum and
% maximum distances allowable here 0.1cm and 200cm.
gluPerspective(angle, ar, 0.1, 200);

% Setup modelview matrix: This defines the position, orientation and
% looking direction of the virtual camera that will be look at our scene.
glMatrixMode(GL.MODELVIEW);
glLoadIdentity;

% Our point lightsource is at position (x,y,z) == (1,2,3)
glLightfv(GL.LIGHT0, GL.POSITION, [1 2 3 0]);

% Location of the camera is at the origin
cam = [0 0 0];

% Set our camera to be looking directly down the Z axis (depth) of our
% coordinate system. Again, all of these numbers are arbitary to some
% extent. Looking down the negative Z axis is just how I learned to
% program.
fix = [0 0 -100];

% Define "up"
up = [0 1 0];

% Here we set up the attributes of our camera using the variables we have
% defined in the last three lines of code
gluLookAt(cam(1), cam(2), cam(3), fix(1), fix(2), fix(3), up(1), up(2), up(3));

% Set background color to 'black' (the 'clear' color)
glClearColor(0, 0, 0, 0);

% Clear out the backbuffer
glClear;

% End the OpenGL context now that we have finished setting things up
Screen('EndOpenGL', window);

% Setup the positions of the spheres using the mexhgrid command
[cubeX, cubeY] = meshgrid(linspace(-25, 25, 10), linspace(-20, 20, 8));
[s1, s2] = size(cubeX);
cubeX = reshape(cubeX, 1, s1 * s2);
cubeY = reshape(cubeY, 1, s1 * s2);
numCubes = length(cubeX);

% Define the intial rotation angles of our cubes
rotaX = rand(1, numCubes) .* 360;
rotaY = rand(1, numCubes) .* 360;
rotaZ = rand(1, numCubes) .* 360;

% Randomise the colours of our cubes
cubeColours = rand(numCubes, 3);

% Now we define how many degrees our cubes will rotated per second and per
% frame. Note we use Degrees here (not Radians)
degPerSec = 180;
degPerFrame = degPerSec * ifi;

% Our cubes will oscilate in and out of depth with a sine wave profile. We
% set the amplitude such that from the viewpoint of the camera the cubes
% will occlude one another.
amplitude = 10;
frequency = 0.2;
angFreq = 2 * pi * frequency;
startPhase = rand(1, numCubes) * 2 * pi;
time = 0;

% Position in depth of the squares
depthPos = amplitude .* sin(angFreq .* time + startPhase);

% Get a time stamp with a flip
vbl = Screen('Flip', window);

% Set the frames to wait to one
waitframes = 1;

while ~KbCheck

    % Begin the OpenGL context now we want to issue OpenGL commands again
    Screen('BeginOpenGL', window);

    % To start with we clear everything
    glClear;

    % Draw all the cubes sequentially in a loop.
    for i = 1:1:length(cubeX)

        % Push the matrix stack
        glPushMatrix;

        % Translate the cube in xyz
        glTranslatef(cubeX(i), cubeY(i), -dist + depthPos(i));

        % Rotate the cube randomly in xyz
        glRotatef(rotaX(i), 1, 0, 0);
        glRotatef(rotaY(i), 0, 1, 0);
        glRotatef(rotaZ(i), 0, 0, 1);

        % Change the light reflection properties of the material to blue. We could
        % force a color to the cubes or do this.
        thisCubeColour = cubeColours(i, :);
        glMaterialfv(GL.FRONT_AND_BACK,GL.AMBIENT,...
            [thisCubeColour(1) thisCubeColour(2), thisCubeColour(3) 1]);
        glMaterialfv(GL.FRONT_AND_BACK,GL.DIFFUSE,...
            [thisCubeColour(1) thisCubeColour(2), thisCubeColour(3) 1]);

        % Draw the solid cube
        glutSolidCube(3);

        % Pop the matrix stack for the next cube
        glPopMatrix;

    end

    % End the OpenGL context now that we have finished doing OpenGL stuff.
    % This hands back control to PTB
    Screen('EndOpenGL', window);

    % Show rendered image at next vertical retrace
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Rotate the cubes for the next drawing loop
    rotaX = rotaX + degPerFrame;
    rotaY = rotaY + degPerFrame;
    rotaZ = rotaZ + degPerFrame;

    % Increment time
    time = time + ifi;

    % Position in depth of the squares for the next frame
    depthPos = amplitude .* sin(angFreq .* time + startPhase);

end

% Shut the screen down
sca;

```
