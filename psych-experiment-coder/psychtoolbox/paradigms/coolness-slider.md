# Coolness Slider

> Source: [coolnessSlider](https://peterscarfe.com/coolnessSlider.html)

Builds upon "

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

% Define black and white
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
grey = GrayIndex(screenNumber);

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black,...
    [], [], [], [], [], kPsychNeedRetinaResolution);

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Change the blend function tfor antialaising
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Set the size of the text
Screen('TextSize', window, 90);

% Hide the mouse cursor
HideCursor;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Our slider will span a proportion of the screens x dimension
sliderLengthPix = screenYpixels / 1.5;
sliderHLengthPix = sliderLengthPix / 2;

% Coordiantes of the sliders left and right ends
leftEnd = [xCenter - sliderHLengthPix yCenter];
rightEnd = [xCenter + sliderHLengthPix yCenter];
sliderLineCoords = [leftEnd' rightEnd'];

% Slider line thickness
sliderLineWidth = 10;

% Define colours
red = [white 0 0];
green = [0 white 0];
blue = [0 0 white];
yellowTrans = [white white 0 0.5];

% Here we set the initial position of the mouse to the centre of the screen
SetMouse(xCenter, yCenter, window);

% Make a base Rect relative to the size of the screen: this will be the
% toggle we can slide on the slider
dim = screenYpixels  / 18;
hDim = dim / 2;
baseRect = [0 0 dim dim];

% We now set the toggles initial position at a random point on the slider
sx = xCenter + (rand * 2 - 1) * sliderHLengthPix;
centeredRect = CenterRectOnPointd(baseRect, sx, yCenter);

% Text labels for the slider scale
sliderLabels = {'Not Cool', 'Cool'};

% Get bounding boxes for the slider label text
textBoundsAll = nan(2, 4);
for i = 1:2
    [~, ~, textBoundsAll(i, :)] = DrawFormattedText(window, sliderLabels{i}, 0, 0, white);
end

% Width and height of the text
textWidths = textBoundsAll(:, 3)';
halfTextWidths = textWidths / 2;
textHeights = range([textBoundsAll(:, 2) textBoundsAll(:, 4)], 2)';
halfTextHeights = textHeights / 2;

% Position of the text so that it is at the ends of the slider but does
% not overlap with the slider line or silder toggle. Make sure it is also
% centered in the y dimension of the screen. To do this we used the bounding
% boxes of the text, plus a little gap so that the text does not completely
% edge the slider toggle in the x dimension
textPixGap = 10;
leftTextPosX = xCenter - sliderHLengthPix - hDim - textWidths(1) - textPixGap;
rightTextPosX = xCenter + sliderHLengthPix + hDim + textPixGap;

leftTextPosY = yCenter + halfTextHeights(1);
rightTextPosY = yCenter + halfTextHeights(2);

% Offset toggle. This determines if the offset between the mouse and centre
% of the square has been set. We use this so that we can move the position
% of the square around the screen without it "snapping" its centre to the
% position of the mouse
offsetSet = 0;

% Sync us and get a time stamp. We blank the window first to remove the
% text that we drew to get the bounding boxes.
Screen('FillRect', window, black)
vbl = Screen('Flip', window);

% Number of frames to wait before updating the screen
waitframes = 1;

% Loop the animation until a key is pressed
while ~KbCheck(-1)

    % Get the current position of the mouse
    [mx, my, buttons] = GetMouse(window);

    % Find the central position of the square
    [cx, cy] = RectCenter(centeredRect);

    % See if the mouse cursor is inside the square
    inside = IsInRect(mx, my, centeredRect);

    % If the mouse cursor is inside the square and a mouse button is being
    % pressed and the offset has not been set, set the offset and signal
    % that it has been set
    if inside == 1 && sum(buttons) > 0 && offsetSet == 0
        dx = mx - cx;
        offsetSet = 1;
    end

    % If the person has clicked, yoke the square to the mouse cursor in its
    % x dimension
    if offsetSet
        sx = mx - dx;
    end

    % Restrict the x position to be on the slider
    if sx > xCenter + sliderHLengthPix
        sx = xCenter + sliderHLengthPix;
    elseif sx < xCenter - sliderHLengthPix
        sx = xCenter - sliderHLengthPix;
    end

    % Center the slidre toggle on its new screen position
    centeredRect = CenterRectOnPointd(baseRect, sx, yCenter);

    % Draw the slider line
    Screen('DrawLines', window, sliderLineCoords, sliderLineWidth, grey);

    % Draw the rect to the screen
    Screen('FillRect', window, yellowTrans, centeredRect);

    % Draw an edge aroiund the slider toggle using the default line width
    Screen('FrameRect', window, green, centeredRect);

    % Text for the ends of the slider
    DrawFormattedText(window, sliderLabels{1}, leftTextPosX, leftTextPosY, blue);
    DrawFormattedText(window, sliderLabels{2}, rightTextPosX, rightTextPosY, red);

    % Draw the title for the slider
    DrawFormattedText(window, 'Coolness Slider', 'center', screenYpixels * 0.25, white);

    % Report the current coolness % rating: coloring the text according to
    % the coolness
    currentCoolness = (sx - (xCenter - sliderHLengthPix)) / sliderLengthPix;
    DrawFormattedText(window, ['Coolness Level: ' num2str(round(currentCoolness * 100)) '%'],...
        'center', screenYpixels * 0.75, [currentCoolness 0 1 - currentCoolness]);

    % Draw a white dot where the mouse cursor is
    Screen('DrawDots', window, [mx my], 10, white, [], 2);

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Check to see if the mouse button has been released and if so reset
    % the offset cue
    if sum(buttons) <= 0
        offsetSet = 0;
    end

end

% Clear the screen
sca;

```
