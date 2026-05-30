# Position Shift

> Source: [positionShift](https://peterscarfe.com/positionShift.html)

Renders two Gabors vertically above one another. The Gabors drift in opposite directions (left and right motion). This internal motion signal causes the Gabors to appear as if they are not vertically aligned with one another i.e. their "envelopes" are shifted.

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
black = BlackIndex(screenNumber);
grey = white / 2;

% % Open the screen
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey, [], 32, 2,...
    [], [],  kPsychNeed32BPCFloat);

% Get the vertical refresh rate of the monitor
ifi = Screen('GetFlipInterval', window);

% Set maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);


%--------------------
% Gabor information
%--------------------

% Dimension of the region where will draw the Gabors in pixels
gaborDimPix = windowRect(4) / 4;

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

% Number of Gabors
numGabors = 2;

% Randomise the phase of the Gabors and make a properties matrix
propertiesMat = repmat([phase, freq, sigma, contrast, aspectRatio, 0, 0, 0], numGabors, 1);
propertiesMat(:, 1) = rand(1, 2) * 360;

% Positions of the gabors
gabShifts = [0.25 0.75] * windowRect(4);
gaborsRects = nan(4, 2);
for i = 1:numGabors
    gaborsRects(:, i) = CenterRectOnPointd([0 0 gaborDimPix gaborDimPix], windowRect(3) / 2, gabShifts(i));
end

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

    % Set the right blend function for drawing the gabors
    Screen('BlendFunction', window, 'GL_ONE', 'GL_ZERO');

    % Draw the Gabor. By default PTB will draw this in the center of the screen
    % for us.
    Screen('DrawTextures', window, gabortex, [], gaborsRects, orientation, [], [], [], [],...
        kPsychDontDoRotation, propertiesMat');

    % Change the blend function to draw an antialiased fixation point
    % in the centre of the array
    Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

    % Draw the fixation point
    Screen('DrawDots', window, [xCenter; yCenter], 10, black, [], 2);

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Update the phase element of the properties matrix (we could if we
    % want update any or all of the properties on each frame. Here the
    % Gabor will drift to the left.
    propertiesMat(:, 1) = propertiesMat(:, 1) + ([-1; 1] * phasePerFrame);

end

% Clear screen
sca;

```
