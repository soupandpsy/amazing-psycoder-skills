# Bounding Box

> Source: [boundingBox](https://peterscarfe.com/boundingBox.html)

Demonstrates how to poll the dimensions of the bounding box for a piece of text. The bounding box is a rectangle which (broadly speaking) is the smallest to enclose a given bit of text (it is in reality a little different from this). However, it is essential to understand this concept if you which to position pieces of text centred upon a given position on the screen. You will see this concept used in many other demos to position text. The code draws a piece of text once in standard mode (bottom left corner of the text bounding box being aligned with the requested text position) and a second time with the text positioned such that the bounding box of the text is centred on the requested text position.

```matlab
% Clear the workspace
close all;
clear;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');

% Draw to the external screen if avaliable
screenNumber = max(screens);

% Define colors
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
grey = GrayIndex(screenNumber);
red = [white 0 0];
blue = [0 0 white];

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black,...
    [], [], [], [], [], kPsychNeedRetinaResolution);

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Change the blend function for anti-aliasing
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Set the size of the text
textSize = 240;
Screen('TextSize', window, textSize);

% The text to write
myText = 'Hello World';

% Get the Bounding box for the text: Broadly speaking this is the minimal
% rectangle which will encompass all of the text - it is defined in the top
% left of the screen. But, all we are interested in is its size
[~, ~, textBounds] = DrawFormattedText(window, myText, 0, 0, white);
textWidth = range([textBounds(1) textBounds(3)]);
textHeight = range([textBounds(2) textBounds(4)]);

% Hide the mouse cursor
HideCursor;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Number of frames to wait before redrawing
waitframes = 1;

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Position of the text: this will be for the standard drawing of the text
% where the text is positioned such that the bottom left corner of the
% bounding box is aligned with the requested screen position of the text
tx = screenYpixels * 0.25;
ty = screenXpixels * 0.25;

% Position of the centered text: This is the position upon which we will
% centre a second peice of text such that the centre of the bounding box is
% aligned with this point
txc = screenYpixels * 0.6;
tyc = screenXpixels * 0.4;

% In order to align the centre of the text we need to move the drawing
% position requested to the left by half the width of the bounding box and
% down by half the height of the bounding box
txcCorrected = txc - textWidth / 2;
tycCorrected = tyc + textHeight / 2;

% Sync us and get a time stamp. We blank the window first to remove the
% text that we drew to get the bounding box.
Screen('FillRect', window, black)
vbl = Screen('Flip', window);

% Loop the animation until a key is pressed
while ~KbCheck(-1)

    % Draw the text in the deafult way: where the text is positioned such
    % that the bottom left corner of the bounding box is aligned with
    % the requested screen position of the text
    DrawFormattedText(window, myText, tx, ty, white);

    % Draw the text again, but in the corrected position such that the
    % centre of the bounding box in on the requested drawing coordinate
    DrawFormattedText(window, myText, txcCorrected, tycCorrected, white);

    % Draw the Bounding box of both bits of text
    Screen('FrameRect', window, blue, textBounds + [tx, ty, tx, ty]);
    Screen('FrameRect', window, red, textBounds + [txcCorrected, tycCorrected, txcCorrected, tycCorrected]);

    % Draw the requested points at which the text is being drawn
    Screen('DrawDots', window, [tx ty], 25, blue, [], 2);
    Screen('DrawDots', window, [txc tyc], 25, red, [], 2);

    % Draw crosshairs for the aligned bounding box text - this shows its
    % centering
    Screen('DrawLines', window, [txc - textWidth / 2 tyc; txc + textWidth / 2 tyc]', [], red);
    Screen('DrawLines', window, [txc tyc - textHeight / 2; txc tyc + textHeight / 2]', [], red)

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

end

% Clear the screen
sca;

```
