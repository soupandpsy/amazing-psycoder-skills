# Transparent Square

> Source: [transparentWindow](https://peterscarfe.com/transparentWindow.html)

This shows how to create full onscreen PTB window, but for this to be semi-transparent. Again, this is useful when developing code, as if you code crashes you can still see your desktop "behind" the full screen PTB window. This route should only be used for developing and debugging code, not for experiments, as it results in poor timing fidelity.

```matlab
% Clear the workspace and the screen
sca;
close all;
clear;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers. This gives us a number for each of the screens
% attached to our computer.
screens = Screen('Screens');

% To draw we select the maximum of these numbers. So in a situation where we
% have two screens attached to our monitor we will draw to the external
% screen.
screenNumber = max(screens);

% Define black and white (white will be 1 and black 0). This is because
% in general luminace values are defined between 0 and 1 with 255 steps in
% between. With our setup, values defined between 0 and 1.
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);

% Do a simply calculation to calculate the luminance value for grey. This
% will be half the luminace value for white
grey = white / 2;

% Make our window transparent Transparence is in the 0 (fully transparent) to
% 1 (fully opaque) range
opacity = 0.8;
PsychDebugWindowConfiguration([], opacity)

% Open an on screen window using PsychImaging and color it grey.
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey);

% Now we have drawn to the screen we wait for a keyboard button press (any
% key) to terminate the demo.
KbStrokeWait;

% Clear the screen.
sca;

```
