# Partial Window

> Source: [partialWindow](https://peterscarfe.com/partialWindow.html)

This demo demostrates how to create a PTB window which covers only part of the screen. This is useful if you are developing code on a single monitor setup as it means if your code crashes, you are not stuck with a full PTB window covering your whole screen. You can put the window wherever you like on your screen. It will behave like any normal window. So in this instance it will close when any keyboard button is pressed. 

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

% Start cordinate in pixels of our window. Note that setting both of these
% to zero will make the window appear in the top right of the screen.
startXpix = 120;
startYpix = 50;

% Dimensions in pixels of our window in the X (left-right) and Y (up down)
% dimensions
dimX = 400;
dimY = 250;

% Open an on screen window using PsychImaging and color it grey.
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey,...
    [startXpix startYpix startXpix + dimX startYpix + dimY]);

% Now we have drawn to the screen we wait for a keyboard button press (any
% key) to terminate the demo.
KbStrokeWait;

% Clear the screen.
sca;

```
