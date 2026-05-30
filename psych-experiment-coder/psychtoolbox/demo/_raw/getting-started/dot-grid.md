# Dot Grid

> Source: [antialiasingDemo](https://peterscarfe.com/antialiasingDemo.html)

The code draws multiple red dots in the top left corner of the screen. The dots are drawn with different levels / types of antialiasing to show the effect on graphics fidelity. The dots are an integer number of pixels in diameter and in the screen y-dimension aligned with the pixel grid of the screen. From left to right: (1) the first dot is drawn with no antialiasing and positioned in the x-dimension aligned with the pixel grid of the screen, (2) the second dot is drawn with no antialiasing and positioned in the x-dimension at a fractional pixel position, (3) the third dot is drawn with antialiasing favouring speed of drawing and positioned in the x-dimension at a fractional pixel position, (4) the fourth dot is drawn with hardware antialiasing favouring quality of drawing and positioned in the x-dimension at a fractional pixel position, (5) the fifth dot is drawn with PTB's inbuilt shader antialiasing favouring quality of drawing and positioned in the x-dimension at a fractional pixel position.

```matlab
% Clear the workspace and the screen
sca;
close all;
clear;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Seed the random number generator. Here we use the an older way to be
% compatible with older systems.
rng('shuffle')

% Get the screen numbers. This gives us a number for each of the screens
% attached to our computer. For help see: Screen Screens?
screens = Screen('Screens');

% Draw we select the maximum of these numbers. So in a situation where we
% have two screens attached to our monitor we will draw to the external
% screen. When only one screen is attached to the monitor we will draw to
% this. For help see: help max
screenNumber = max(screens);

% Define black and white (white will be 1 and black 0). This is because we
% are defining luminace values between 0 and 1 through the use of the PTB
% default setting call above.
% For help see: help WhiteIndex and help BlackIndex
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);

% Open an on screen window and color it black.
% For help see: Screen OpenWindow?
% [window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black,...
    [], [], [], [], [], kPsychNeedRetinaResolution);

% Get the size of the on screen window in pixels.
% For help see: Screen WindowSize?
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window in pixels
% For help see: help RectCenter
[xCenter, yCenter] = RectCenter(windowRect);

% Enable alpha blending for anti-aliasing
% For help see: Screen BlendFunction?
% Also see: Chapter 6 of the OpenGL programming guide
%

% Set the color of our dot to full red. Color is defined by red green
% and blue components (RGB). So we have three numbers which
% define our RGB values. The maximum number for each is 1 and the minimum
% 0. So, "full red" is [1 0 0]. "Full green" [0 1 0] and "full blue" [0 0
% 1]. Play around with these numbers and see the result.
dotColor = [1 0 0];

% Dot size in pixels (integer pixels)
dotSizePix = 20;

% Dot positions: first x position is integer pixels, second two not
dotXpos = [dotSizePix dotSizePix * 3 + 0.5, dotSizePix * 5 + 0.5 dotSizePix * 7 + 0.5 dotSizePix * 9 + 0.5];
dotYpos = ones(1, length(dotXpos)) .* dotSizePix;

% Draw the first dot to the screen with no antialiasing: this dot is
% centred on the pixel grid
Screen('DrawDots', window, [dotXpos(1) dotYpos(1)], dotSizePix, dotColor, [], 2);

% Draw the second dot to the screen with no antialiasing: this dot is not
% centred on the pixel grid
Screen('DrawDots', window, [dotXpos(2) dotYpos(2)], dotSizePix, dotColor, [], 2);

%-------------------------------------------------------------------------
% Draw the third - fifth dots to the screen with with antialiasing. All
% dots are not centered on the pixel grid, and have different levels /
% types of antialiasing
%-------------------------------------------------------------------------

% Enable altialiasing
Screen('BlendFunction', window, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

% Draw antialisaed dot for maximum drawing performance
Screen('DrawDots', window, [dotXpos(3) dotYpos(3)], dotSizePix, dotColor, [], 1);

% Draw antialisaed dot with hardware antialiasing
Screen('DrawDots', window, [dotXpos(4) dotYpos(4)], dotSizePix, dotColor, [], 2);

% Draw antialisaed dot with PTB onboard shader based antialiasing. In some
% cases maximum drawing performance and hardware based antialiasing are not
% suppoert, in which case PTB automatically switches to this mode
Screen('DrawDots', window, [dotXpos(5) dotYpos(5)], dotSizePix, dotColor, [], 3);

% Flip to the screen
Screen('Flip', window);

% Now we have drawn to the screen we wait for a keyboard button press (any
% key) to terminate the demo. For help see: help KbStrokeWait
KbStrokeWait;

% Clear the screen
sca;

```
