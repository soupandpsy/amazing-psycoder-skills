# Modulating Slant

> Source: [modulatingSlant](https://peterscarfe.com/modulatingSlant.html)

This demo extends "

```matlab
% Clear the workspace
sca;
clear;
close all;

% Set to generate random numbers
rng('shuffle');

%--------------------------------------------------------------------------
%                      Set up the screen
%--------------------------------------------------------------------------

% Set the stereomode 6 for red-green anaglyph presentation. You will need
% to view the image with the red filter over the left eye and the green
% filter over the right eye.
stereoMode = 6;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Setup Psychtoolbox for OpenGL 3D rendering support and initialize the
% mogl OpenGL for Matlab wrapper
InitializeMatlabOpenGL;

% Get the screen number
screenid = max(Screen('Screens'));

% Open the main window
[window, windowRect] = PsychImaging('OpenWindow', screenid, 0, [], 32, 2, stereoMode);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Screen size pixels
[screenXpix, screenYpix] = Screen('WindowSize', window);

% Set up alpha-blending for smooth (anti-aliased) edges to our dots
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

%--------------------------------------------------------------------------
%                      Set up the screen
%--------------------------------------------------------------------------

% Set the size of the square to be a fraction of the screen size. This will
% give us similar results on any demo system hopefully
squareDimPix = screenXpix / 2.5;

% For ease will will position dots +/- half of this size i.e. centered
% around zero. When we draw to the screen we center the dots automatically.
squareHalfDimPix = squareDimPix / 2;

% Number of dots
numDots = 2000;

% Dot base position in pixels for the left and right eye. As you will see
% the vertical do positions will be the same in both cases.
dotPosXleft = (rand(1, numDots) .* 2 - 1) .* squareHalfDimPix;
dotPosYleft = (rand(1, numDots) .* 2 - 1) .* squareHalfDimPix;
dotPosXright = dotPosXleft;
dotPosYright = dotPosYleft;

% Dot diameter in pixels
dotDiaPix = 6;

% Our slanted surface will oscillate in demo around its vertical axis. To
% do this we will modulate the magnification factor applied to the left and
% right eyes images with a sine-wave
% These are the parameters for the sine wave which we will use to modulate
% the magnification factor
% See: http://en.wikipedia.org/wiki/Sine_wave
amplitude = 0.1;
frequency = 0.2;
angFreq = 2 * pi * frequency;
startPhase = 0;
time = 0;


%------------------------
% Drawing to the screen
%------------------------

% We will update the screen on every frame
waitframes = 1;

% Sync us and get a time stamp
vbl = Screen('Flip', window);

% Loop the animation until a key is pressed
while ~KbCheck

    % Calculate the left and right eye magnification factor for this frame
    % of the animation. We do equal and opposite expandsion and contraction
    % in each eye.
    rightEyeMag = 1 + amplitude * sin(angFreq * time + startPhase);
    leftEyeMag = 1 - amplitude * sin(angFreq * time + startPhase);

    % Select left-eye image buffer for drawing (buffer = 0)
    Screen('SelectStereoDrawBuffer', window, 0);

    % Now draw our left eyes dots
    Screen('DrawDots', window, [dotPosXleft .* leftEyeMag; dotPosYleft], dotDiaPix,...
        [], [screenXpix / 2 screenYpix / 2], 2);

    % Select right-eye image buffer for drawing (buffer = 1)
    Screen('SelectStereoDrawBuffer', window, 1);

    % Now draw our right eyes dots
    Screen('DrawDots', window, [dotPosXright .* rightEyeMag; dotPosYright], dotDiaPix,...
        [], [screenXpix / 2 screenYpix / 2], 2);

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the time
    time = time + ifi;

end

% Wait for a button press to exit the demo
KbStrokeWait;
sca;

```
