# Drifiting Gabor

> Source: [driftingGabor](https://peterscarfe.com/driftingGabor.html)

Simple demonstration of animating a single drifting Gabor patch. The Gabor is rendered highly efficiently on the graphics card using a GLSL Shader.

```matlab
% Clear the workspace and the screen
sca;
close all;
clear;

% Setup PTB with some default values
PsychDefaultSetup(2);

% Set the screen number to the external secondary monitor if there is one
% connected
screenNumber = max(Screen('Screens'));

% Define black, white and grey
white = WhiteIndex(screenNumber);
grey = white / 2;

% Open the screen
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey,...
    [], 32, 2, [], [], kPsychNeedRetinaResolution);

% Get the vertical refresh rate of the monitor
ifi = Screen('GetFlipInterval', window);

% Set maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);


%--------------------
% Gabor information
%--------------------

% Dimension of the region where will draw the Gabor in pixels
gaborDimPix = windowRect(4) / 2;

% Sigma of Gaussian
sigma = gaborDimPix / 7;

% Obvious Parameters
orientation = 0;
contrast = 0.8;
aspectRatio = 1.0;
phase = 0;

% Spatial Frequency (Cycles Per Pixel)
% One Cycle = Grey-Black-Grey-White-Grey i.e. One Black and One White Lobe
numCycles = 5;
freq = numCycles / gaborDimPix;

% Build a procedural gabor texture (Note: to get a "standard" Gabor patch
% we set a grey background offset, disable normalisation, and set a
% pre-contrast multiplier of 0.5).
backgroundOffset = [0.5 0.5 0.5 0.0];
disableNorm = 1;
preContrastMultiplier = 0.5;
gabortex = CreateProceduralGabor(window, gaborDimPix, gaborDimPix, [],...
    backgroundOffset, disableNorm, preContrastMultiplier);

% Randomise the phase of the Gabors and make a properties matrix.
propertiesMat = [phase, freq, sigma, contrast, aspectRatio, 0, 0, 0];


%------------------------------------------
%    Draw stuff - button press to exit
%------------------------------------------

% FLip to the vertical retrace rate
vbl = Screen('Flip', window);

% We will update the stimulus on each frame
waitframes = 1;

% We choose an arbitary value at which our Gabor will drift
phasePerFrame = 4 * pi;

while ~KbCheck

    % Draw the Gabor. By default PTB will draw this in the center of the screen
    % for us.
    Screen('DrawTextures', window, gabortex, [], [], orientation, [], [], [], [],...
        kPsychDontDoRotation, propertiesMat');

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Update the phase element of the properties matrix (we could if we
    % want update any or all of the properties on each frame. Here the
    % Gabor will drift to the left.
    propertiesMat(1) = propertiesMat(1) + phasePerFrame;

end

% Clear screen
sca;

```
