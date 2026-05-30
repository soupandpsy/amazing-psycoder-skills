# Stacked Circles

> Source: [stackedCircles](https://peterscarfe.com/stackedCircles.html)

Renders a random dot stereogram of a set of three "stacked" disks/circles, each progressively closer in depth. The demo shows some math related to sorting, filtering and modifying dot coordinates based upon set criteria.

```matlab
% Clear the workspace
sca;
clear;
close all;

% Shuffle the random number generator so that we get randomly positioned
% dots on each rune
rng('shuffle');

%--------------------------------------------------------------------------
%                      Set up the screen
%--------------------------------------------------------------------------

% Set the stereomode 6 for red-green anaglyph presentation. You will need
% to view the image with the red filter over the left eye and the green
% filter over the right eye. Note that with color filters you will get some
% from of cross talk normally, unless you have matched the filtered well to
% your screen, or compensated for this.
stereoMode = 6;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Setup Psychtoolbox for OpenGL 3D rendering support and initialize the
% mogl OpenGL for Matlab wrapper
InitializeMatlabOpenGL;

% Get the screen number
screenid = max(Screen('Screens'));

% Open the main window
[window, windowRect] = PsychImaging('OpenWindow', screenid, 0,...
    [], 32, 2, stereoMode);

% Show cleared start screen:
Screen('Flip', window);

% Screen size pixels
[screenXpix, screenYpix] = Screen('WindowSize', window);

% Queries the display size in mm as reported by the operating system. Note
% that there are some complexities here. See Screen DisplaySize? for
% information. So always measure your screen size directly. We just use the
% reported value for the purposes of this demo.
[widthMM, heightMM] = Screen('DisplaySize', screenid);

% Convert to CM
screenYcm = heightMM / 10;
screenXcm = widthMM / 10;

% Centimeters per pixel
pixPerCm = mean([screenYpix / screenYcm screenXpix / screenXcm]);

% Set up alpha-blending for smooth (anti-aliased) edges to our dots
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');


%--------------------------------------------------------------------------
%                      Set up the screen
%--------------------------------------------------------------------------

% Diameters and radius of each of our circles
circleDiaCm = [5 10 15];
circleDiaPix = circleDiaCm .* pixPerCm;
circleRadsPix = circleDiaPix ./ 2;

% Number of dots
numDots = 3000;

% Generate some dot coordinates
biggestRad = max(circleRadsPix);
dotPosX = (rand(1, numDots) .* 2 - 1) .* biggestRad;
dotPosY = (rand(1, numDots) .* 2 - 1) .* biggestRad;

% Filter the ones in the biggest circle
inBig = dotPosX.^2 + dotPosY.^2 < biggestRad^2;
dotPosX = dotPosX(inBig == 1);
dotPosY = dotPosY(inBig == 1);
numDotsNew = length(dotPosY);

% See which of the circles the dots belong to and shift the pixels
% accordingly
shifterPix = [10 5 0];
shifterBase = zeros(1, numDotsNew);

shifterBase(dotPosX.^2 + dotPosY.^2 < circleRadsPix(2)^2) = shifterPix(2);
shifterBase(dotPosX.^2 + dotPosY.^2 < circleRadsPix(1)^2) = shifterPix(1);

% Now shift the dots in the X dimension for the left and right
dotPosXleft = dotPosX + shifterBase;
dotPosXright = dotPosX - shifterBase;

% The Y position of the dots is the same in both eyes
dotPosYleft = dotPosY;
dotPosYright = dotPosY;

% Dot diameter in pixels
dotDiaPix = 6;


%------------------------
% Drawing to the screen
%------------------------

% When drawing in stereo we have to select which eyes buffer we are going
% to draw in. These are labelled 0 for left and 1 for right. Note also, if
% you wear your anaglyph glasses the opposite way around the depth will
% reverse.

% Select left-eye image buffer for drawing (buffer = 0)
Screen('SelectStereoDrawBuffer', window, 0);

% Now draw our left eyes dots
Screen('DrawDots', window, [dotPosXleft; dotPosYleft], dotDiaPix,...
    [], [screenXpix / 2 screenYpix / 2], 2);

% Select right-eye image buffer for drawing (buffer = 1)
Screen('SelectStereoDrawBuffer', window, 1);

% Now draw our right eyes dots
Screen('DrawDots', window, [dotPosXright; dotPosYright], dotDiaPix,...
    [], [screenXpix / 2 screenYpix / 2], 2);

% Flip to the screen
Screen('Flip', window);

% Wait for a button press to exit the demo
KbStrokeWait;
sca;

```
