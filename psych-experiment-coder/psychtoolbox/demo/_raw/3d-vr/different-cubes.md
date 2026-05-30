# Different Cubes

> Source: [differentCubes](https://peterscarfe.com/differentCubes.html)

This simple demo will introduce you to 3D rendering with OpenGL. OpenGL is a powerful way in which to create stimuli and is at the heart of much of PTB, all be it behind the scenes. This demo renders an array of 3D cubes, each with a different position and rotation angle. It lights these cubes with a single light source. The scene is rendered with anti-aliasing via multi-sampling to give us nice smooth edges to the rendered objects on screen.

```matlab
% Clear the workspace
close all
clear
sca;

% Shuffle the random number generator to ensure randomness
rng('shuffle');

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

% Start the OpenGL context (you have to do this before you issue OpenGL
% commands such as we are using here)
Screen('BeginOpenGL', window);

% For this demo we will assume our screen is 30cm in height. The units are
% essentially arbitary with OpenGL as it is all about ratios. But it is
% nice to define things in normal scale numbers
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
% maximum distances allowable here 0.1cm and 200cm. If we draw outside of
% these regions then the stimuli won't be rendered
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
% coordinate system
fix = [0 0 -100];

% Define "up": here we say that up is positive Y
up = [0 1 0];

% Here we set up the attributes of our camera using the variables we have
% defined in the last three lines of code
gluLookAt(cam(1), cam(2), cam(3), fix(1), fix(2), fix(3), up(1), up(2), up(3));

% Set background color to 'black' (the 'clear' color)
glClearColor(0, 0, 0, 0);

% Clear out the backbuffer
glClear;

% Setup the positions of the spheres using the mexhgrid command
[cubeX, cubeY] = meshgrid(linspace(-25, 25, 10), linspace(-20, 20, 8));
[s1, s2] = size(cubeX);
cubeX = reshape(cubeX, 1, s1 * s2);
cubeY = reshape(cubeY, 1, s1 * s2);

% Draw all the cubes in a loop. We apply a translation and rotation to each
% of the cubes. The Puch and Pop commands ensure that our transforms are
% only applied to the current cube that we are drawing.
for i = 1:1:length(cubeX)

    % Push the matrix stack
    glPushMatrix;

    % Translate the cube in xyz
    glTranslatef(cubeX(i), cubeY(i), -dist);

    % Rotate the cube randomly in xyz
    glRotatef(rand * 360, 1, 0, 0);
    glRotatef(rand * 360, 0, 1, 0);
    glRotatef(rand * 360, 0, 0, 1);

    % Scale the cubes in size randomly. They will get a minimum of half the
    % specified size
    cubeScale = 0.5 + rand * 0.5;
    glScalef(cubeScale, cubeScale, cubeScale);

    % Change the light reflection properties of the material the cube is
    % made of. Here we do this randomly.
    theCubeColour = rand(1, 3);
    glMaterialfv(GL.FRONT_AND_BACK,GL.AMBIENT, [theCubeColour 1]);
    glMaterialfv(GL.FRONT_AND_BACK,GL.DIFFUSE, [theCubeColour 1]);

    % Draw the solid cube (3x3x3 in size)
    glutSolidCube(3);

    % Pop the matrix stack for the next cube
    glPopMatrix;

end

% End the OpenGL context now that we have finished
Screen('EndOpenGL', window);

% Show rendered image at next vertical retrace. We do not specify a time
% here as for this demo we are only presenting the stimuli flipped to
% screen once.
Screen('Flip', window);

% Wait for keyboard press
KbStrokeWait;

% Shut the screen down
sca;

```
