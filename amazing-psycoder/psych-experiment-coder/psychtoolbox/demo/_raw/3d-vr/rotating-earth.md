# Rotating Earth

> Source: [rotatingEarth](https://peterscarfe.com/rotatingEarth.html)

The demo loads in an image of the planet earth from NASA. Converts it into an OpenGL texture and maps it to the surface of a sphere. Earth is rotated over time. You will need to download the image from

```matlab

% Clear the workspace
clear;
close all;
sca;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Setup Psychtoolbox for OpenGL 3D rendering support and initialize the
% mogl OpenGL for Matlab wrapper
InitializeMatlabOpenGL;

% Distance to the sphere
distanceCm = 60;

% Radius of our earth sphere
earthRad = 8;

% Rotation per second
degPerSec = 15;
currentRotAngle = 0;

% Number of samples per pixel for multisampling
multiSample = 4;

% Find the screen to use for display
screenid = max(Screen('Screens'));

% Set the black and white index
black = BlackIndex(screenid);

% Start the PsychImaging Configuration
PsychImaging('PrepareConfiguration');
PsychImaging('AddTask', 'General', 'FloatingPoint32Bit');

% Open an on screen window using PsychImaging to optimise drawing
[window, winRect] = PsychImaging('OpenWindow', screenid, black,...
    [], 32, 2, [], multiSample);

% Set to maximum priority
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Get the width and height of the window in pixels
[screenXpix, screenYpix] = Screen('WindowSize', window);

% Reported dimensions of the screen in cm
[widthMm, heightMm] = Screen('DisplaySize', screenid);
screenWidth = widthMm / 10;
screenHeight = heightMm / 10;

% Measure the vertical refresh rate of the monitor
ifi = Screen('GetFlipInterval', window);

% Fill the screen black
Screen('FillRect', window, black);
Screen('Flip', window);

% Convert the rotation per second into per frame
degPerFrame = degPerSec * ifi;

% We will update our rotation animation every frame
waitframes = 1;

%----------------------------------------------------------------------
%                 Load and make the earth texture
%----------------------------------------------------------------------

% Load the earth texture and make it into a texture. This is a texture
% freely avaliable from NASA at the following link.
% https://www.visibleearth.nasa.gov/...
% images/57735/the-blue-marble-land-surface-ocean-color-sea-ice-and-clouds
myimg = imread([cd '/NASA Earth.jpg']);
mytex = Screen('MakeTexture', window, myimg, [], 1, 0);

% Make into an OpenGL texture
[gltex, gltextarget] = Screen('GetOpenGLTexture', window, mytex);


%----------------------------------------------------------------------
%                       OpenGL Setup
%----------------------------------------------------------------------

% We start the OpenGL context
Screen('BeginOpenGL', window);

% Set background color to 'black'
glClearColor(0, 0, 0, 0);

% Enable depth buffer
glEnable(GL.DEPTH_TEST);


%----------------------------------------------------------------------
%                 We will use perspective projection
%----------------------------------------------------------------------

% Near and far clipping planes (these difine the rendering volume, anything
% outside of these is not rendered)
clipNear = 0.1;
clipFar = 100;

% Angular subtense of the screen
angle = 2 * atand((screenHeight / 2) / distanceCm);

% Aspect ratio of the screen
aspectRatio = screenWidth / screenHeight;

% Lets set up a projection matrix, the projection matrix defines how images
% in our 3D simulated scene are projected to the images on our 2D monitor
glMatrixMode(GL.PROJECTION);
glLoadIdentity;
gluPerspective(angle, aspectRatio, clipNear, clipFar);

% Setup modelview matrix: This defines the position, orientation and
% direction of the virtual camera that will  look at our scene with
glMatrixMode(GL.MODELVIEW);
glLoadIdentity;

% Location of the camera
cam = [0 0 0];

% Set our camera to be looking directly down the -Z axis (depth) of our
% coordinate system
fix = [0 0 -1];

% Define "up"
up = [0 1 0];

% Here we set up the attributes of our camera using the variables we have
% defined in the last three lines of code
gluLookAt(cam(1), cam(2), cam(3), fix(1), fix(2), fix(3), up(1), up(2), up(3));


%----------------------------------------------------------------------
%               Setup the lighting for the environment
%----------------------------------------------------------------------

% Enable OpenGL Lighting
glEnable(GL.LIGHTING);

% Force there to be no ambient light (OpenGL default is for there to be
% some)
glLightModelfv(GL.LIGHT_MODEL_AMBIENT, [0 0 0 1]);

% Define a local light source
glEnable(GL.LIGHT0);

% Defuse light only
glLightfv(GL.LIGHT0, GL.DIFFUSE, [1 1 1 1]);

% Point the light at the origin (this is where we will place our sphere)
glLightfv(GL.LIGHT0, GL.SPOT_DIRECTION, [0 0 -distanceCm]);

% Allow normalisation
glEnable(GL.NORMALIZE);


%----------------------------------------------------------------------
%          Enable the earth texture and make the earth
%----------------------------------------------------------------------

% Enable the texture
glEnable(gltextarget);

% Bind the texture for use
glBindTexture(gltextarget, gltex);

% Allow the colour of the texture and the lighting to interact
glTexEnvfv(GL.TEXTURE_ENV,GL.TEXTURE_ENV_MODE,GL.MODULATE);

% Cyclic clamping of the texture
glTexParameteri(gltextarget, GL.TEXTURE_WRAP_S, GL.REPEAT);
glTexParameteri(gltextarget, GL.TEXTURE_WRAP_T, GL.REPEAT);

% Filtring for the texture
glTexParameteri(gltextarget, GL.TEXTURE_MIN_FILTER, GL.LINEAR);
glTexParameteri(gltextarget, GL.TEXTURE_MAG_FILTER, GL.LINEAR);

% Make a quadratic sphere
mysphere = gluNewQuadric;

% Generate texture coordinate automatically
gluQuadricTexture(mysphere, GL.TRUE);

% We end the OpenGL context for now
Screen('EndOpenGL', window);

%----------------------------------------------------------------------
%                       Earth rotation loop
%----------------------------------------------------------------------

% Flip to sync us to the screen
vbl = Screen('Flip', window);

while ~KbCheck(-1)

    Screen('BeginOpenGL', window);

    % Clear the buffers
    glClear;

    % Push the matrix stack for this transform
    glPushMatrix;

    % Move the earth down the negative z-axis and rotate it
    glTranslatef(0, 0, -distanceCm)
    glRotatef(currentRotAngle, 0, 1, 0);
    glRotatef(-90, 1, 0, 0);

    % Render the sphere
    gluSphere(mysphere, earthRad, 1000, 1000);

    % Discard the current transforms
    glPopMatrix;

    % We are done with OenGL for now in order to flip
    Screen('EndOpenGL', window);

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the rotation
    currentRotAngle = currentRotAngle + degPerFrame;

end

% Clear the screen
sca

```
