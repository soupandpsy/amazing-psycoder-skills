# Log Gabor Filter

> Source: [logGaborFilter](https://peterscarfe.com/logGaborFilter.html)

This demo uses code contributed by

```matlab
% This PTB demo shows the use of the LogGabor filter code contributed by
% Steven Dakin, s.dakin@auckland.ac.nz
% To run the code you will need to place this code in the same directory as
% the "DoLogGabor.m" function contributed by Steven

% Clear the workspace
close all;
clear;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Load in the face data from the PTB distro
matdemopath = [PsychtoolboxRoot 'PsychDemos/OpenGL4MatlabDemos/mogldemo.mat'];
load(matdemopath, 'face');

% Apply the log gabor filter from Steve Dakin
% Here we set a narrow orientation bandwidth (10 deg) and a FreqSigma to Inf
% for broadband. This give "facial barcodes" as in Goffaux & Dakin (2010)
FreqPeak = [8 32 128];
FreqSigma = Inf;
ThetaPeak = (0:45:135) .* pi/180;
ThetaSigma = 10 .* pi/180;

origFace = face{1};
[res]= DoLogGabor(origFace, FreqPeak, FreqSigma, ThetaPeak, ThetaSigma);

% Get the dimensions of the image matrix and calculate how manay images we
% have
[s1, s2, s3, s4] = size(res);
numImages = s3 * s4;

% Make a matrix of the filter parameters for display on the screen
freqPeaksLine = sort(repmat(FreqPeak, 1, s4));
thetaPeaksLine = repmat(ThetaPeak, 1, s3);

% Get the screen numbers
screens = Screen('Screens');

% Draw to the external screen if avaliable
screenNumber = max(screens);

% Define black and white
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
grey = white / 2;
inc = white - grey;
darkGrey = white * 0.25;

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, darkGrey, [], 32, 2);

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Set up alpha-blending for smooth (anti-aliased) lines
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Set the text size
Screen('TextSize', window, 30);

% Make the filtered images into textures
imageTexture = nan(1, numImages);
thisIm = 0;
for i = 1:s3
    for j = 1:s4

        thisIm = thisIm + 1;

        % Grab the real component of the filtered image
        thisImage = real(res(:, :, i, j));

        % Max-Min normalise the image so that all the values fall between 0 and
        % 1 in order to draw correctly with our code
        %
        % (1) This step gives use the minimum luminance value in the image,
        % after first concerting the image into a column vector, and also the
        % range of intensity values
        imageMin = min(thisImage(:));
        rangeImage = max(thisImage(:)) - imageMin;
        %
        % (2) We normalise the image based on these values
        thisImageNorm = (thisImage - imageMin) / rangeImage;

        % Make our texture
        imageTexture(thisIm) = Screen('MakeTexture', window, thisImageNorm);

    end
end

% Make the orginal image into a texture
origFaceNorm = (origFace - min(origFace(:))) / (max(origFace(:)) - min(origFace(:)));
imageTextureFace = Screen('MakeTexture', window, origFaceNorm);

% The images are relatively small, so we will scale them by a factor of 2x
% when drawing them
scaleFactor = 2;
baseRect = [0 0 s1 s2];
scaledRect = baseRect .* 2;

% Left and right hand destination rectangles
leftRect = CenterRectOnPointd(scaledRect, screenXpixels * 0.25, screenYpixels / 2);
rightRect = CenterRectOnPointd(scaledRect, screenXpixels * 0.75, screenYpixels / 2);
bothRects = [leftRect; rightRect];

% We will change the filtered image show on every second. For this simple
% demo we will just do this by counting frames shown
changeFrame = round(1 / ifi);
faceTicker = 0;
imageToShow = 1;

% Determine the bounding box of the text to allow us to center our text
% nicely above have image, some of this could be done with the extra
% parameters of the screen function, but it is nice to see what is going on
% here
textBoundsOrig = Screen('TextBounds', window, 'Original Image');
pixelsAboveImage = 10;
xLocOrig = screenXpixels * 0.25;
yLocOrig = (screenYpixels / 2) - (textBoundsOrig(4) / 2)...
    - (s1 / 2 * scaleFactor) - pixelsAboveImage;
leftTextPos = CenterRectOnPointd(textBoundsOrig, xLocOrig, yLocOrig);

textBoundsFilt = Screen('TextBounds', window, 'Filtered Image');
pixelsAboveImage = 10;
xLocOrig = screenXpixels * 0.75;
yLocOrig = (screenYpixels / 2) - (textBoundsFilt(4) / 2)...
    - (s1 / 2 * scaleFactor) - pixelsAboveImage;
rightTextPos = CenterRectOnPointd(textBoundsFilt, xLocOrig, yLocOrig);


% We will update the screen on every frame
waitframes = 1;

% Sync us and get a time stamp
vbl = Screen('Flip', window);


% No we present the original image on the left hand side of the screen and
% cycle through each of the filtered image on the right hand side of the
% screen
while ~KbCheck

    % Draw our images
    Screen('DrawTextures', window,...
        [imageTextureFace imageTexture(imageToShow)], [], bothRects', 0);

    % Label eveything up
    DrawFormattedText(window, 'Original Image',...
        leftTextPos(1), leftTextPos(2), white);
    DrawFormattedText(window, 'Filtered Image',...
        rightTextPos(1), rightTextPos(2), white);
    DrawFormattedText(window, ['Filter Parameters\n\n Frequency-Peak '...
        num2str(freqPeaksLine(imageToShow))...
        ', Frequency-Sigma ' num2str(FreqSigma)...
        ', Theta-Peak ' num2str(thetaPeaksLine(imageToShow))...
        ', Theta-Sigma ' num2str(ThetaSigma)],...
        'center', screenYpixels * 0.8, white);

    % Flip to the screen
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);

    % Increment the ticker and see if we should change the filtered face
    % image shown, if the ticker get to the last image loop back to the
    % first
    faceTicker = faceTicker + 1;
    if faceTicker == 60
        imageToShow = imageToShow + 1;
        if imageToShow > numImages
            imageToShow = 1;
        end
        faceTicker = 0;
    end

end

% Clear up and leave the building
sca

```
