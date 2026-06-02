# Posner Cuing Experiment

> Source: [poserCuingExperiment](https://peterscarfe.com/poserCuingExperiment.html)

This demo will show you how to build a standard Posner cuing task. A person must detect a briefly presented target (a Gabor patch) to the left or right of fixation. Prior to this, a box is presented either at the location the Gabor will appear at, or the “other” location (thus cuing or not the location where the Gabor will appear). The effect of cueing at different timepoints relative to target appearance can be investigated. The decision time and whether they person was correct are saved out to a text file in the same location as the code.

```matlab
% Clear the workspace
close all;
clear;
sca;

%--------------------------------------------------------------------------
%   Code shows a basic Posner cuing tak. A location to the left of right of
%   fixation is "cued" by a framed square. Subsequently, after a
%   "cue-target-onset-asynchrony" a gabor "target" is presenetd at one of the
%   same left of right locations. The cue and target can either be in the
%   same location ("contingent") or different locations ("non-contingent").
%   the time taken to respond and whether you were correct is recorded and
%   saved to file.
%
% Not my area of research, but apparently this style of task is used
% extremely widely.
%
% Note that here I have used for loops for the stimulus presentation, even
% though not strickly needed. See "WaitFrameDemo" for an explanation of why
% I do this and a demonstration of an alternative way.
%--------------------------------------------------------------------------

%--------------------
%   Screen setup
%--------------------

% Setup PTB with some default values
PsychDefaultSetup(2);

% Skip sync tests ** This is for demo purposes only ** It should not be
% done in a real experiment.
Screen('Preference', 'SkipSyncTests', 2);

% Set the random number generator so we get random numbers, not the same
% sequency if we restart Matlab
rng('shuffle');

% Set the screen number to the external secondary monitor if there is one
% connected
screenNumber = max(Screen('Screens'));

% Define black, white and grey
white = WhiteIndex(screenNumber);
grey = white / 2;
black = BlackIndex(screenNumber);

% Open the screen
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey, []);

% Flip to clear
Screen('Flip', window);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Set the text size
Screen('TextSize', window, 40);

% Query and set the maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);


%----------------------------
% Gabor target information
%----------------------------

% Dimension of the region where will draw the Gabor in pixels
gaborDimPix = 300;

% Sigma of Gaussian
sigma = gaborDimPix / 7;

% Obvious Parameters
orientation = 90;
contrast = 1;
aspectRatio = 1.0;

% Spatial Frequency (Cycles Per Pixel)
% One Cycle = Grey-Black-Grey-White-Grey i.e. One Black and One White Lobe
numCycles = 8;
freq = numCycles / gaborDimPix;

% Build a procedural gabor texture
gabortex = CreateProceduralGabor(window, gaborDimPix, gaborDimPix, [],...
    [0.5 0.5 0.5 0.0], 1, 0.5);

% Our Gabor target will always be vertical
gaborAngle = 0;


%----------------------
% Box cue information
%----------------------

% Colour and width of the line for the box
boxColour = black;
boxLineWidth = 4;


%-----------------------------
% Fixation point information
%-----------------------------

% Colour and size of the fixation point
dotSizePix = 8;
dotColor = black;


%----------------------------------
% Positions to the left and right
%----------------------------------

% We will position the the target and Gabor 1/4 or 3/4 the screen width
leftPosX = windowRect(3) * 0.25;
rightPosX = windowRect(3) * 0.75;

% Rectangular regions for the Gabor target and cue box
leftRect = CenterRectOnPointd([0 0 gaborDimPix gaborDimPix], leftPosX, yCenter);
rightRect = CenterRectOnPointd([0 0 gaborDimPix gaborDimPix], rightPosX, yCenter);


%----------------------------------------------------------------------
%                       Timings
%----------------------------------------------------------------------

% These are pretty much random - you will need to look at the literature to
% see what is used. Also, note the use of "round" which would be
% dangerous to blindly use in an experiment.

% Fixation point time in seconds and frames
fixTimeSecs = 0.5;
fixTimeFrames = round(fixTimeSecs / ifi);

% Cue point time in seconds and frames
cueTimeSecs = 0.15;
cueTimeFrames = round(cueTimeSecs / ifi);

% Cue point time in seconds and frames
targetTimeSecs = 0.15;
targetTimeFrames = round(targetTimeSecs / ifi);

% Intertrial interval time
isiTimeSecs = 0.2;
isiTimeFrames = round(isiTimeSecs / ifi);

% Time between the cue and the target
cueTargetTimeSecs = 0.3;
cueTargetTimeFrames = round(isiTimeSecs / ifi);

% Frames to wait before redrawing
waitframes = 1;


%----------------------------------------------------------------------
%                       Keyboard information
%----------------------------------------------------------------------

% Define the keyboard keys that are listened for. We will be using the left
% and right arrow keys as response keys for the task and the escape key as
% a exit/reset key
escapeKey = KbName('ESCAPE');
leftKey = KbName('LeftArrow');
rightKey = KbName('RightArrow');

% Hide the mouse cursor
HideCursor;


%----------------------------------------------------------------------
%                             Procedure
%----------------------------------------------------------------------

% Gabor target and square cue will appear to the left and right of the
% fixation. Left will be signalled by a zero and right a one. They can be
% "contingent" (cue and target in same location) or non-contingent (cue and
% target in different locaitons). We create a matrix with the four possible
% cue and target positions. Upper line will be the cue position, lower line
% the target position.
baseMat = [0 0 1 1; 0 1 0 1];

% Repeat this matrix a certain number of times. We repeat the whole matrix
% to ensure the same number of trials per cue target position
numReps = 2;
cueTargetMat = repmat(baseMat, 1, numReps);

% Randomise the trials
cueTargetMatShuff = Shuffle(cueTargetMat, 2);

% How many trials are we doing in total
numTrials = size(cueTargetMatShuff, 2);

% Make our response matrix which will save the RT and correctness of the
% location choice. We preallocate the matrix with nans.
dataMat = nan(numTrials, 2);


%----------------------------------------------------------------------
%                       Experimental loop
%----------------------------------------------------------------------

% Animation loop: we loop for the total number of trials
for trial = 1:numTrials

    % Randomise the phase of the Gabor for this trial
    phase = rand .* 360;
    propertiesMat = [phase, freq, sigma, contrast, aspectRatio, 0, 0, 0]';

    % Cue and target position
    cuePos = cueTargetMatShuff(1, trial);
    targetPos = cueTargetMatShuff(2, trial);

    % Logic to assign the correct position to the cue and target
    if cuePos == 0
        cueRect = leftRect;
    elseif cuePos == 1
        cueRect = rightRect;
    end

    if targetPos == 0
        targetRect = leftRect;
    elseif targetPos == 1
        targetRect = rightRect;
    end

    % Set the blend funciton for a nice antialiasing
    Screen('BlendFunction', window, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    % If this is the first trial we present a start screen and wait for a
    % key-press
    if trial == 1

        % Draw the instructions
        DrawFormattedText(window, 'Press Any Key To Begin', 'center', 'center', black);

        % Flip to the screen
        Screen('Flip', window);

        % Wait for a key press
        KbStrokeWait(-1);

        % Flip the screen grey
        Screen('FillRect', window, grey);
        vbl = Screen('Flip', window);
        WaitSecs(0.5);

    end

    % Present the fixation point only (a nicely antialiased dot)
    for i = 1:fixTimeFrames
        Screen('DrawDots', window, [xCenter; yCenter], dotSizePix, dotColor, [], 2);
        vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
    end

    % Present the box cue and the fixation point
    for i = 1:cueTimeFrames
        Screen('DrawDots', window, [xCenter; yCenter], dotSizePix, dotColor, [], 2);
        Screen('FrameRect', window, boxColour, cueRect, boxLineWidth);
        vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
    end

    % Present a grey screen for the cue-target gap
    for i = 1:cueTargetTimeFrames
        Screen('FillRect', window, grey);
        Screen('DrawDots', window, [xCenter; yCenter], dotSizePix, dotColor, [], 2);
        vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
    end

    % Present the Gabor target and fixation point: note the swicth between
    % blend functions needed for drawing the fixation point and Gabor
    for i = 1:targetTimeFrames
        Screen('BlendFunction', window, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        Screen('DrawDots', window, [xCenter; yCenter], dotSizePix, dotColor, [], 2);
        Screen('BlendFunction', window, 'GL_ONE', 'GL_ZERO');
        Screen('DrawTextures', window, gabortex, [], targetRect, gaborAngle, [], [], [], [],...
            kPsychDontDoRotation, propertiesMat);
        vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
    end

    % Clear the screen ready for a response
    Screen('FillRect', window, grey);
    vbl = Screen('Flip', window, vbl + (1 - 0.5) * ifi);

    % Now we wait for a keyboard button signaling the observers response.
    % The left arrow key signals a "left" response and the right arrow key
    % a "right" response. You can also press escape if you want to exit the
    % program
    respToBeMade = true;
    startResp = GetSecs;
    while respToBeMade
        [keyIsDown,secs, keyCode] = KbCheck(-1);
        if keyCode(escapeKey)
            ShowCursor;
            sca;
            return
        elseif keyCode(leftKey)
            response = 0;
            respToBeMade = false;
        elseif keyCode(rightKey)
            response = 1;
            respToBeMade = false;
        end
    end
    endResp = GetSecs;
    rt = endResp - startResp;

    % Work out if the location of the gabpr target was identified corrcetly
    if targetPos == response
        correctness = 1;
    elseif targetPos ~= response
        correctness = 0;
    end

    % Save out the data after having added the data to the data matrix. We
    % save to the same directory as the code as a tab dilimited text file
    dataMat(trial, :) = [rt correctness];
    writematrix(dataMat, [cd filesep 'posnerData.txt'], 'Delimiter', '\t')

    % Inter trial interval black screen. Note that the timestamp for the
    % initial frame will be missed due to the first vbl being "old" due to
    % the response loop. I leave it as an excercise to the reader as to how
    % one could fix this simply.
    for i = 1:isiTimeFrames
        Screen('FillRect', window, grey);
        vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
    end

    % If this is the last trial we present screen saying that the experimet
    % is over.
    Screen('BlendFunction', window, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    if trial == numTrials

        % Draw the instructions: in reality the person could press any of
        % the listened to keys to exist. But they do not know that.
        DrawFormattedText(window, 'Experiment Complete: press ESCAPE to exit', 'center', 'center', black);

        % Flip to the screen
        vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

        % Wait for a key press
        KbStrokeWait(-1);

    end


end

% Done! Clear up and leave the building
disp('Experiment Finished')
sca

```
