# Accurate Timing

> Source: [accurateTiming](https://peterscarfe.com/accurateTiming.html)

This demo shows three basic ways in which to present a stimulus which would change on each frame with varying degrees of potential accuracy. Please read the extensive comments in the demo closely, they are important and should not be ignored. For presenting a stimulus which is unchanging, or changes less frequently then each frame, see Wait Frames Demo.

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
% secondary screen.
screenNumber = max(screens);

% Define black and white (white will be 1 and black 0)
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);

% Do a simply calculation to calculate the luminance value for grey. This
% will be half the numerical luminace values for white
grey = white / 2;

% Open an on screen window using PsychImaging and color it grey.
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey);

% Measure the vertical refresh rate of the monitor
ifi = Screen('GetFlipInterval', window);

% Retreive the maximum priority number
topPriorityLevel = MaxPriority(window);

% Length of time and number of frames we will use for each drawing test
numSecs = 1;
numFrames = round(numSecs / ifi);

% Number of frames to wait when specifying good timing. Note: the use of
% wait frames is to show a generalisable coding. For example, by using
% waitframes = 2 one would flip on every other frame. See the PTB
% documentation for details. In what follows we flip every frame.
waitframes = 1;

%--------------------------------------------------------------------------
% NOTE: The aim in the following is to demonstrate how one might setup code
% to present a stimulus that changes on each frame. One would not for
% instance present a uniform screen of a fixed colour using this approach.
% The only reason I do this here to to make the code as simple as possible,
% and to avoid a screen which flickers a different colour every, say,
% 1/60th of a second. Virtually all the remianing demos show a stimulus
% which changes on each frame, so I want to show an approach which will
% generalise to the rest of the demos. Therefore, one would clearly not
% write a script in this form for an experiment; it is to demonstrate
% core principles.
%
% Specifically,
%
% vbl + (waitframes - 0.5) * ifi
%
% is the same as
%
% vbl + 0.5 * ifi
%
% As here waitframes is set to 1 (i.e. (1 - 0.5) == 0.5)
%
% For discussion see PTB forum thread 20178 for discussion.
%
%--------------------------------------------------------------------------

%------------
% EXAMPLE #1
%------------

% First we will demonstrate a poor way in which to get good timing of
% visually presented stimuli. In this way of presenting we leave much to
% chance as regards when our stimuli get to the screen, so it is not
% reccomended that you use this approach.
for frame = 1:numFrames

    % Color the screen grey
    Screen('FillRect', window, [0.5 0.5 0.5]);

    % Flip to the screen
    Screen('Flip', window);

end


%------------
% EXAMPLE #2
%------------

% Here we now specify a time at which PTB should be ready to draw to the
% screen by. In this example we use half a inter-frame interval. This
% specification allows us to get an accurate idea of whether PTB is making
% the stimulus timings we want.
vbl = Screen('Flip', window);
for frame = 1:numFrames

    % Color the screen red
    Screen('FillRect', window, [0.5 0 0]);

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

end


%------------
% EXAMPLE #3
%------------

% Here we do exactly the same as the second example, but we additionally
% first set the PTB prority level to maximum. This means PTB will take
% processing priority over other system and applicaiton processes. On
% modern multi-core processors Priority can be set high at once prior to
% presenting stimuli and kept in this state until the end of the script.
%
% One older machines with few cores, one use to set the priority prior to
% drawing to the screen and then reduced the priority after. This is now
% egenerally not needed.
%
% On Linux this operation can take much much longer
% then on Windows and OSX (up to minutes in some use cases). So it is now
% suggested that you set Priority once at the start of a script after
% setting up your onscreen window.
% See PTB forum thread 20178 (and those linked to it) for discussion.
Priority(topPriorityLevel);
vbl = Screen('Flip', window);
for frame = 1:numFrames

    % Color the screen purple
    Screen('FillRect', window, [0.5 0 0.5]);

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

end
Priority(0);


%------------
% EXAMPLE #4
%------------

% Finally we do the same as the last example except now we additionally
% tell PTB that no more drawing commands will be given between coloring the
% screen and the flip command. This, can help acheive good timing when one
% is needing to do additional non-PTB processing between setting up drawing
% and flipping to the screen. Thus, you would only use this technique if
% you were doing this. So, if you are not, go with example #3
Priority(topPriorityLevel);
vbl = Screen('Flip', window);
for frame = 1:numFrames

    % Color the screen blue
    Screen('FillRect', window, [0 0 0.5]);

    % Tell PTB no more drawing commands will be issued until the next flip
    Screen('DrawingFinished', window);

    % One would do some additional stuff here to make the use of
    % "DrawingFinished" meaningful / useful

    % Flip to the screen
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

end
Priority(0);

% Clear the screen.
sca;

```
