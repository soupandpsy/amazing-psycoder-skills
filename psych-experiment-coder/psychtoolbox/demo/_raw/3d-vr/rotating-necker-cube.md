# Rotating Necker Cube

> Source: [rotatingNeckerCube](https://peterscarfe.com/rotatingNeckerCube.html)

Uses OpenGL commands to draw a rotating Necker Cube using Orthographic projection. This type of stimulus is in fact bistable, so perceptually the rotation direction of the Necker Cube will stochastically flip whilst watching it.

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

% Make sure that the computer is running the OpenGL psych toolbox
AssertOpenGL;

% Find the screen to use for displaying the stimuli. By using "max" this
% will display on an external monitor if one is connected.
screenid = max(Screen('Screens'));

% Determine the values of black and white
black = BlackIndex(screenid);
white = WhiteIndex(screenid);

% Initialise OpenGL
InitializeMatlabOpenGL;

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

% Convert to CM
screenYcm = heightMM / 10;
screenXcm = widthMM / 10;


%--------------------------------------------------------------------------
%                   Projection information
%--------------------------------------------------------------------------

% Start the OpenGL context (you have to do this before you issue OpenGL
% commands such as we are using here)
Screen('BeginOpenGL', window);

% Enable proper occlusion handling via depth tests
glEnable(GL.DEPTH_TEST);

% Enable blending for anti-aliased lines
glEnable(GL.BLEND);
glBlendFunc(GL.SRC_ALPHA, GL.ONE_MINUS_SRC_ALPHA);

% Set the line width in pixels
glLineWidth(6);

% Lets set up a projection matrix, the projection matrix defines how images
% in our 3D simulated scene are projected to the images on our 2D monitor
glMatrixMode(GL.PROJECTION);
glLoadIdentity;

% We are using orthographic projection for our necker cube, this is what
% makes the stimulus ambiguous.
depthClipLimit = 1000;
glOrtho(-screenXcm/2, screenXcm/2,...
    -screenYcm/2, screenYcm/2, -depthClipLimit, depthClipLimit);

% Setup modelview matrix: This defines the position, orientation and
% looking direction of the virtual camera that will be look at our scene.
glMatrixMode(GL.MODELVIEW);
glLoadIdentity;

% Location of the camera is at the origin
cam = [0 0 0];

% Nominal distance of the object: this is a nominal distance as it will not
% effect the size of the rendered image due to this being orthographic
% projection. We just need to make sure that the position of the object is
% within the clipping planes of the glOrtho(...) call.
dist = -100;

% Start angle for the cube
angle = rand * 360;

% Rotation per second and frame: the object will rotate 60 degree per
% second
rotPerSec = 60;
rotPerFrame = rotPerSec * ifi;

% Set our camera to be looking directly down the Z axis (depth) of our
% coordinate system.
fix = [0 0 dist];

% Define "up": this sets the orientation of our coordinate system
up = [0 1 0];

% Here we set up the attributes of our camera using the variables we have
% defined in the last three lines of code
gluLookAt(cam(1), cam(2), cam(3), fix(1), fix(2), fix(3), up(1), up(2), up(3));

% Set background color to 'black' (the 'clear' color)
glClearColor(0, 0, 0, 0);

% Clear out the backbuffer
glClear;

% For now we end the OpenGL context to allow us to call standard screen
% functions of PTB
Screen('EndOpenGL', window);


%--------------------------------------------------------------------------
%                   Stimulus information / timing
%--------------------------------------------------------------------------

% Our stimulus is very simple and can be drawn in a single line of OpenGL
% code. All we need to do is specify its size. Here just a 3rd of our
% reported screen height.
cubeSize = screenYcm / 3;

% Position of our cube relative to the camera
cubePos = [0 0 dist];

% We will update the stimulus on each frame
waitframes = 1;

% Get a flip to sync our timing
vbl = Screen(window, 'Flip');


%--------------------------------------------------------------------------
%                           Drawing Loop
%--------------------------------------------------------------------------

% Stimulus drawing loop (exits when any button is pressed)
while ~KbCheck

    % Begin OpenGL again for this frame as we will be issuing OpenGL
    % commands
    Screen('BeginOpenGL', window);

    % Push the matrix stack
    glPushMatrix;

    % Clear stuff
    glClear;

    % Translate
    glTranslatef(cubePos(1), cubePos(2), cubePos(3));

    % Rotate the cube (in reality OpenGL will rotate and then translate the
    % cube. That is the instructions are applied the reverse in which you
    % state them.
    glRotatef(25, 1, 0, 1);
    glRotatef(angle, 0, 1, 0);

    % Render the cube: we will color it white, we are not useing lighting
    % and material properties here, just standard RGB colors.
    glColor3f(white, white, white);
    glutWireCube(cubeSize);

    % Pop the matrix now that we applied our transformations
    glPopMatrix;

    % End the OpenGL context so that we can flip to the screen
    Screen('EndOpenGL', window);

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the angle of the cube
    angle = angle + rotPerFrame;

end

% Clean up and leave the building
sca;

```
