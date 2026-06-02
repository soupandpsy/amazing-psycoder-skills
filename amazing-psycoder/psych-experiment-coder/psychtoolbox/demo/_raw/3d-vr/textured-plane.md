# Textured Plane

> Source: [texturedPlane](https://peterscarfe.com/texturedPlane.html)

Loads an image in from file, converts it to an OpenGL texture, maps that texture to a plane and then renders the plane with geometric transforms applied to position and orientate it in 3D space.

```matlab

% Clear the workspace
clear;
close all;
sca;

% Randomly seed the random number generation
rng('shuffle');

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

%----------------------------------------------------------------------
%                   Physical set-up variables
%----------------------------------------------------------------------

% Assumed viewing distance
distanceCm = 60;

% Height dimensionn of the surface we will apply the texture to
surfaceHeightCm = 10;

% Our surface will oscilate with a sine wave function around the X Y ans Z
% axes

% Amplitude of ossilation
amplitude = 50;

% Frequency in each dimension (these are just a few random numbers to make
% the simulation look nice)
frequencyX = 0.2;
frequencyY = 0.25;
frequencyZ = 0.18;

% Angular frequency
angFreqX = 2 * pi * frequencyX;
angFreqY = 2 * pi * frequencyY;
angFreqZ = 2 * pi * frequencyZ;

% Starting phase
startPhaseX = rand * 360;
startPhaseY = rand * 360;
startPhaseZ = rand * 360;

% Zero time
time = 0;


%----------------------------------------------------------------------
%                   Screen initialisation
%----------------------------------------------------------------------

% Make sure that the computer is running the OpenGL psych toolbox
AssertOpenGL;

% Setup Psychtoolbox for OpenGL 3D rendering support and initialize the
% mogl OpenGL for Matlab wrapper
InitializeMatlabOpenGL;

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


%----------------------------------------------------------------------
%                       Timing information
%----------------------------------------------------------------------

% Number of frames to wait before drawing again
waitframes = 1;


%----------------------------------------------------------------------
%            Load in our image and convert to a texture
%----------------------------------------------------------------------

% Load in the rabbit image whihc comes wiht the PTB distro
theImageLocation = [PsychtoolboxRoot 'PsychDemos' filesep...
    'AlphaImageDemo' filesep 'konijntjes1024x768.jpg'];
image = imread(theImageLocation);
[s1, s2, s3] = size(image);
image = im2double(image);

% Get the aspect ratio of the image
imAspect = s2 / s1;

% Convert to a texture for PTB drawing (orientation needs changing for
% rendering)
imageFlipped = rot90(flipud(image));
planeTexture = Screen('MakeTexture', window, imageFlipped, [], 1, 2);

% Get the information we need about the texture
[imw, imh] = Screen('WindowSize', planeTexture);
[texNameFront, targetFront, tuFront, tvFront] = Screen('GetOpenGLTexture', window, planeTexture, imh, imw);

% Bind our texture and setup filtering to allow nice presentation of our
% texture
glBindTexture(targetFront, texNameFront);
glGenerateMipmapEXT(targetFront);
glTexParameterf(targetFront, GL.TEXTURE_MAG_FILTER, GL.LINEAR);
glTexParameterf(targetFront, GL.TEXTURE_MIN_FILTER, GL.LINEAR_MIPMAP_LINEAR);

% Allow the texture and lighting to interact
glTexEnvfv(GL.TEXTURE_ENV, GL.TEXTURE_ENV_MODE, GL.MODULATE);

% This gives nice texture rendering without artifacts
maxAnisotropy = glGetFloatv(GL.MAX_TEXTURE_MAX_ANISOTROPY_EXT);
glTexParameterf(targetFront, GL.TEXTURE_MAX_ANISOTROPY_EXT, maxAnisotropy);


%----------------------------------------------------------------------
%                       OpenGL Setup
%----------------------------------------------------------------------

% Setup the OpenGL rendering context of the onscreen window for use by
% OpenGL wrapper
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
%             Display list for the slanted surface
%----------------------------------------------------------------------

% Surface dimensions
surfaceHalfHeightCm = surfaceHeightCm / 2;

% Calculate the width of the surface needed based upon the image aspect
% ratio
surfaceWidthCm = surfaceHeightCm * imAspect;
surfaceHalfWidthCm = surfaceWidthCm / 2;

% Surface corner coordinates
surfCoords = [-surfaceHalfWidthCm surfaceHalfHeightCm 0;...
    surfaceHalfWidthCm surfaceHalfHeightCm 0;...
    surfaceHalfWidthCm -surfaceHalfHeightCm 0;...
    -surfaceHalfWidthCm -surfaceHalfHeightCm 0]';

% Calculate the surface normal (this insures proper lighting calculations)
surfNormal = cross(surfCoords(:, 3) - surfCoords(:, 2), surfCoords(:, 2) - surfCoords(:, 1));

% Create a display list for the surface
surfaceDisplayList = glGenLists(1);
glNewList(surfaceDisplayList, GL.COMPILE);

% Enable and bind the texture
glEnable(targetFront);
glBindTexture(targetFront, texNameFront);

% Set the surface normal we calculated earlier
glNormal3f(surfNormal(1), surfNormal(2), surfNormal(3));

% Begin drawing of a quad (square) which will be the support of our
% texture, we associate the geometric coordinates of the plane with the
% texture coordinates of the image
glBegin(GL.QUADS);

glTexCoord2f(tvFront, tuFront);
glVertex3f(surfCoords(1, 1), surfCoords(2, 1), surfCoords(3, 1));

glTexCoord2f(0, tuFront);
glVertex3f(surfCoords(1, 2), surfCoords(2, 2), surfCoords(3, 2));

glTexCoord2f(0, 0);
glVertex3f(surfCoords(1, 3), surfCoords(2, 3), surfCoords(3, 3));

glTexCoord2f(tvFront, 0);
glVertex3f(surfCoords(1, 4), surfCoords(2, 4),surfCoords(3, 4));

glEnd;

glEndList;

% End the open GL wrapper for now
Screen('EndOpenGL', window);


%----------------------------------------------------------------------
%                       Keyboard information
%----------------------------------------------------------------------

% Unify the keyboard names for mac and windows computers
KbName('UnifyKeyNames');

% Define the keyboard keys that are listened for
escapeKey = KbName('ESCAPE');


%----------------------------------------------------------------------
%                           Drawing Loop
%----------------------------------------------------------------------

% Get a vbl for the start time
vbl = Screen('Flip', window);
startTimeFix = vbl;

while ~KbCheck

    % Orientation of the square on this frame
    angleX = amplitude * sin(angFreqX * time + startPhaseX);
    angleY = amplitude * sin(angFreqY * time + startPhaseY);
    angleZ = amplitude * sin(angFreqZ * time + startPhaseZ);

    % Begin open GL
    Screen('BeginOpenGL', window);

    % Clear the buffers
    glClear;

    % Push and pop are needed to avoid accumulations of transforms
    glPushMatrix;

    % Rotate and then translate the surface (these commands need to be
    % issued in the opposite way in which you want them applied by OpenGL)
    glTranslatef(0, 0, -distanceCm);
    glRotatef(angleX, 1, 0, 0);
    glRotatef(angleY, 0, 1, 0);
    glRotatef(angleZ, 0, 0, 1);

    % Call the display list i.e. show our textured plan
    glCallList(surfaceDisplayList);

    % Ditch the matrix transforms
    glPopMatrix;

    % End the open GL context
    Screen('EndOpenGL', window);

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment time
    time = time + ifi;

end

% Close the screen
sca

```
