# Rotating Mesh

> Source: [rotatingMesh](https://peterscarfe.com/rotatingMesh.html)

This demo loads in a mesh object from a .obj file and renders rotating it with perspective projection and lighting. The rendering is achieved using vertex buffers. This allows very efficient rendering of highly detailed meshes (though the mesh we render here is very simple). This technique is used in the code provided with our

```matlab
% Clear the workspace
clear;
close all;

% Assumed distance of the screen
dist = 100;

% Rendered distance of the object
objectDist = dist;

% Assumed height of the screen
screenHeight = 30;

% How much to scale the mesh by in X, Y and Z
scaleFactor = 15;


%--------------------------------------------------------------------------
% Load in the .obj file. Here we use a funciton from the excellent
% gptoolbox for Matlab. We have found that the LoadOBJFile included with
% Psychtoolbox fails to load many common .obj files.
%
% If you use this, you will need to set you "addpath" appropriately.
%
% gptoolbox: https://github.com/alecjacobson/gptoolbox
%
%--------------------------------------------------------------------------

% Path to the mesh subfolder of the gptoolbox. You will need to alter this
% to the path on your own computer
addpath('/Users/peterscarfe/Documents/GitHub Local/gptoolbox/mesh')

% Load in the object mesh: the downloaded .obj file needs to be in the same
% folder as this piece of code.
[verticesAndColour, faces, texCoords, triTexCoords, normals, faceNormals] = readOBJ([cd filesep 'latticeObject.obj']);

% Split the vertices and vertex colours: the first three are x, y, z 3D
% coordinates, the last three the R, G, B colours.
vertices = verticesAndColour(:, 1:3);
colors = verticesAndColour(:, 4:6);

% Number of vertices and faces
[numVerts, ~] = size(vertices);
[numFaces, ~] = size(faces);


%----------------------------------------------------------------------
%               Pretty standard PTB setup here
%----------------------------------------------------------------------

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Skip sync tests (for demo purposes only - not to be used in a real
% experiment)
Screen('Preference', 'SkipSyncTests', 2);

% Find the screen to use for display
screenid = max(Screen('Screens'));

% Initialise OpenGL
InitializeMatlabOpenGL;

% Number of samples per pixel for multisampling
multiSample = 4;

% Background colour
bkGrColor = 0;

% Open the main window with multi-sampling for anti-aliasing
[window, windowRect] = PsychImaging('OpenWindow', screenid, bkGrColor, [], [], [], [], multiSample);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% For this demo we will assume our screen is 30cm in height. The units are
% essentially arbitary with OpenGL as it is all about ratios. But it is
% nice to define things in normal scale numbers
ar = windowRect(3) / windowRect(4);
screenWidth = screenHeight * ar;


%----------------------------------------------------------------------
%                       Keyboard information
%----------------------------------------------------------------------

% Unify the keyboard names for mac and windows computers
KbName('UnifyKeyNames');

% Define the keyboard keys that are listened for
escapeKey = KbName('ESCAPE');

% Signal no key is being pressed down
keyIsDown = 0;


%----------------------------------------------------------------------
%                     Open GL Lighting Setup
%----------------------------------------------------------------------

% Start the OpenGL context (you have to do this before you issue OpenGL
% commands such as we are using here)
Screen('BeginOpenGL', window);

% Enable lighting
glEnable(GL.LIGHTING);

% Ambient light: Force there to be none
glLightModelfv(GL.LIGHT_MODEL_AMBIENT, [0 0 0 1]);

% Defuse white light
glEnable(GL.LIGHT1);
glLightfv(GL.LIGHT1, GL.DIFFUSE, [1 1 1 1]);

% Enable proper occlusion handling via depth tests
glEnable(GL.DEPTH_TEST);

% Enable Normalisation
glEnable(GL.NORMALIZE);

% Set point size
glPointSize(0.5);

% Enable material color
glEnable(GL.COLOR_MATERIAL);


%----------------------------------------------------------------------
%                  Vertex Buffer Object (VBO) Setup
%----------------------------------------------------------------------

% Make vertices, normals, faces and colors into line vectors. This is
% needed for the setup of our buffers
vertLine = reshape(vertices', 1, numVerts * 3);
normalLine = reshape(normals', 1, numVerts * 3);
facesLine = reshape(faces', 1, numFaces * 3);
colorLine = reshape(colors', 1, numVerts * 3);

% Faces detailed needed for our draw elements call
facesLineInt = int32(facesLine - 1);
facesBy3 = numFaces * 3;

% Number of bytes in a floating point number - this is needed to
% appropriately set up the size of our buffers
bytesPerNum = 4;

% Calculate the buffer size in bytes
normSize = length(normalLine) * bytesPerNum;
vertSize = length(vertLine) * bytesPerNum;
colorSize = length(colorLine) * bytesPerNum;
bufferSize = normSize + vertSize + colorSize;

% The buffer ID
bufferID = glGenBuffers(1);

% Bind the buffer
glBindBuffer(GL.ARRAY_BUFFER, bufferID);

% Allocate but don't initialize it the buffer by providing a null pointer
glBufferData(GL.ARRAY_BUFFER, bufferSize, 0, GL.STATIC_DRAW);

% Fill the buffer: note the conversion to single i.e. floating point
% numbers
glBufferSubData(GL.ARRAY_BUFFER, 0, vertSize, single(vertLine));
glBufferSubData(GL.ARRAY_BUFFER, vertSize, normSize, single(normalLine));
glBufferSubData(GL.ARRAY_BUFFER, vertSize + normSize, colorSize, single(colorLine));

% Get the size of the buffer and check if it is correct. If it is not
% correct abort
theSize = glGetBufferParameteriv(GL.ARRAY_BUFFER, GL.BUFFER_SIZE);
if theSize ~= bufferSize
    glDeleteBuffersARB(1, bufferID);
    disp('Buffer size incorrect: aborting')
    sca
    return
end

% Unbind the buffer
glBindBuffer(GL.ARRAY_BUFFER, 0);


%----------------------------------------------------------------------
%                 Perspective Projection setup
%----------------------------------------------------------------------

% Lets set up a projection matrix, the projection matrix defines how images
% in our 3D simulated scene are projected to the images on our 2D monitor
glMatrixMode(GL.PROJECTION);
glLoadIdentity;

% Calculate the field of view in the y direction using the assumed distance
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

% Location of the camera is at the origin
cam = [0 0 0];

% Set our camera to be looking directly down the Z axis (depth) of our
% coordinate system
fix = [0 0 -dist];

% Define "up": here we say that up is positive Y
up = [0 1 0];

% Here we set up the attributes of our camera using the variables we have
% defined in the last three lines of code
gluLookAt(cam(1), cam(2), cam(3), fix(1), fix(2), fix(3), up(1), up(2), up(3));

% Set background color to 'black' (the 'clear' color)
glClearColor(0, 0, 0, 0);

% Clear
glClear;

% End the open GL context for now
Screen('EndOpenGL', window);

% We will rotate the model over time
theRot = rand(1, 3) .* 360;
maxRotPerFrame = repmat(0.3, 1, 3);

% We will update the animation every frame
waitframes = 1;

% Get a first flip timetamp
vbl = Screen('Flip', window);

% Draw our anitmation loop
while ~KbCheck(-1)

    % End the open GL context
    Screen('BeginOpenGL', window);

    % Clear stuff for the round of drawing
    glClear;

    %------------------------------------
    %          Draw the scene
    %------------------------------------

    % Push the matrix stack
    glPushMatrix;

    % Translate the object in xyz
    glTranslatef(0, 0, -objectDist);
    glRotatef(theRot(1), 1, 0, 0)
    glRotatef(theRot(2), 0, 1, 0)
    glRotatef(theRot(3), 0, 0, 1)
    glScalef(scaleFactor, scaleFactor, scaleFactor);


    %-------------------------------------------------------
    % VBO stuff: this is the part where we draw the object
    %-------------------------------------------------------

    % Bind the buffer
    glBindBuffer(GL.ARRAY_BUFFER, bufferID);

    % Enable all of the arrays we need
    glEnableClientState(GL.VERTEX_ARRAY);
    glEnableClientState(GL.NORMAL_ARRAY);
    glEnableClientState(GL.COLOR_ARRAY);

    % Set up our pointers
    glColorPointer(3, GL.FLOAT, 0, vertSize + colorSize);
    glNormalPointer(GL.FLOAT, 0, vertSize);
    glVertexPointer(3, GL.FLOAT, 0, 0);

    % Draw our mesh
    glDrawElements(GL.TRIANGLES, facesBy3, GL.UNSIGNED_INT, facesLineInt);

    % Disable our arrays
    glDisableClientState(GL.VERTEX_ARRAY);
    glDisableClientState(GL.NORMAL_ARRAY);
    glDisableClientState(GL.COLOR_ARRAY);

    % Unbind the buffer
    glBindBuffer(GL.ARRAY_BUFFER, 0);

    % Pop the matrix stack
    glPopMatrix;

    % End the open GL context
    Screen('EndOpenGL', window);

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the rotation in X, Y and Z
    theRot = theRot + maxRotPerFrame;

end

% Clean up
sca

```
