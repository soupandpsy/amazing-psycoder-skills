# Source: wisconsin_card_sorting (demos/wisconsin_card_sorting)
# Project URL: https://gitlab.pavlovia.org/demos/wisconsin_card_sorting
# Original file: Wisconsin Card Sorting Task_lastrun.py
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.1.2),
    on April 08, 2022, at 18:06
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.1.2'
expName = 'Wisconsin Card Sorting Task'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\p0071480\\Documents\\Pavlovia\\vespr\\wisconsin-card-sorting\\Wisconsin Card Sorting Task_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# Setup ioHub
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# Initialize components for Routine "Instructions"
InstructionsClock = core.Clock()
instructions = visual.TextStim(win=win, name='instructions',
    text='In this task you will be required to sort the presented cards based on a rule i.e. the cards will have to be sorted based on either colour, shape or number. The rule will not be presented, however you will receive feedback on each trial. After a certain amount of trials the rule will change to a different one. To select your response click on one of the four cards presented at the top of the screen. ',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=.9, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
continue_button = visual.ImageStim(
    win=win,
    name='continue_button', 
    image='continue.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -.4), size=(0.65, .1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
mouse_2 = event.Mouse(win=win)
x, y = [None, None]
mouse_2.mouseClock = core.Clock()

# Initialize components for Routine "Example"
ExampleClock = core.Clock()
example_text = visual.TextStim(win=win, name='example_text',
    text='For example, you may see a screen like this:',
    font='Arial',
    pos=(0, 0.4), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
example_image = visual.ImageStim(
    win=win,
    name='example_image', 
    image='example.jpg', mask=None, anchor='center',
    ori=0, pos=(0, 0.15), size=(0.7, 0.4),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
example_text_2 = visual.TextStim(win=win, name='example_text_2',
    text='The presented card (bottom centre) can be categorised based on shape (dots), colour (yellow) or number (three). Click on the first card if you want to categorise it by the shape, second if you want categorise it by colour and third if you want to categorise it by number. After you select your response, feedback will be provided. Click on the image to start the experiment.',
    font='Arial',
    pos=(0, -0.25), height=0.04, wrapWidth=.9, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Initialize components for Routine "Trials"
TrialsClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
one_red_dot = visual.ImageStim(
    win=win,
    name='one_red_dot', 
    image='images/1redDot.jpg', mask=None, anchor='center',
    ori=0, pos=(-0.375, 0.25), size=(0.2, 0.2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
two_yellow_triangles = visual.ImageStim(
    win=win,
    name='two_yellow_triangles', 
    image='images/2yellowTriangles.jpg', mask=None, anchor='center',
    ori=0, pos=(-0.125, 0.25), size=(0.2, 0.2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
three_green_crosses = visual.ImageStim(
    win=win,
    name='three_green_crosses', 
    image='images/3greenCrosses.jpg', mask=None, anchor='center',
    ori=0, pos=(0.125, 0.25), size=(0.2, 0.2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
four_blue_stars = visual.ImageStim(
    win=win,
    name='four_blue_stars', 
    image='images/4blueStars.jpg', mask=None, anchor='center',
    ori=0, pos=(0.375, 0.25), size=(0.2, 0.2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-5.0)
trial_card = visual.ImageStim(
    win=win,
    name='trial_card', 
    image='sin', mask=None, anchor='center',
    ori=0, pos=(0, -0.2), size=(0.25, 0.25),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-6.0)
response = event.Mouse(win=win)
x, y = [None, None]
response.mouseClock = core.Clock()

# Initialize components for Routine "Feedback"
FeedbackClock = core.Clock()
msg = ''
feedback_text = visual.TextStim(win=win, name='feedback_text',
    text='',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "End"
EndClock = core.Clock()
thank_you = visual.TextStim(win=win, name='thank_you',
    text='This is the end of the experiment.\nThank you for your time.',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "Instructions"-------
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the mouse_2
mouse_2.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
InstructionsComponents = [instructions, continue_button, mouse_2]
for thisComponent in InstructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
InstructionsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Instructions"-------
while continueRoutine:
    # get current time
    t = InstructionsClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=InstructionsClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instructions* updates
    if instructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instructions.frameNStart = frameN  # exact frame index
        instructions.tStart = t  # local t and not account for scr refresh
        instructions.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instructions, 'tStartRefresh')  # time at next scr refresh
        instructions.setAutoDraw(True)
    
    # *continue_button* updates
    if continue_button.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        continue_button.frameNStart = frameN  # exact frame index
        continue_button.tStart = t  # local t and not account for scr refresh
        continue_button.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(continue_button, 'tStartRefresh')  # time at next scr refresh
        continue_button.setAutoDraw(True)
    # *mouse_2* updates
    if mouse_2.status == NOT_STARTED and t >= 1-frameTolerance:
        # keep track of start time/frame for later
        mouse_2.frameNStart = frameN  # exact frame index
        mouse_2.tStart = t  # local t and not account for scr refresh
        mouse_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(mouse_2, 'tStartRefresh')  # time at next scr refresh
        mouse_2.status = STARTED
        mouse_2.mouseClock.reset()
        prevButtonState = mouse_2.getPressed()  # if button is down already this ISN'T a new click
    if mouse_2.status == STARTED:  # only update if started and not finished!
        buttons = mouse_2.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                try:
                    iter(continue_button)
                    clickableList = continue_button
                except:
                    clickableList = [continue_button]
                for obj in clickableList:
                    if obj.contains(mouse_2):
                        gotValidClick = True
                        mouse_2.clicked_name.append(obj.name)
                if gotValidClick:  
                    continueRoutine = False  # abort routine on response
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Instructions"-------
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('instructions.started', instructions.tStartRefresh)
thisExp.addData('instructions.stopped', instructions.tStopRefresh)
thisExp.addData('continue_button.started', continue_button.tStartRefresh)
thisExp.addData('continue_button.stopped', continue_button.tStopRefresh)
# store data for thisExp (ExperimentHandler)
thisExp.addData('mouse_2.started', mouse_2.tStart)
thisExp.addData('mouse_2.stopped', mouse_2.tStop)
thisExp.nextEntry()
# the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Example"-------
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the mouse
mouse.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
ExampleComponents = [example_text, example_image, example_text_2, mouse]
for thisComponent in ExampleComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
ExampleClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Example"-------
while continueRoutine:
    # get current time
    t = ExampleClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=ExampleClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *example_text* updates
    if example_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        example_text.frameNStart = frameN  # exact frame index
        example_text.tStart = t  # local t and not account for scr refresh
        example_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(example_text, 'tStartRefresh')  # time at next scr refresh
        example_text.setAutoDraw(True)
    
    # *example_image* updates
    if example_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        example_image.frameNStart = frameN  # exact frame index
        example_image.tStart = t  # local t and not account for scr refresh
        example_image.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(example_image, 'tStartRefresh')  # time at next scr refresh
        example_image.setAutoDraw(True)
    
    # *example_text_2* updates
    if example_text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        example_text_2.frameNStart = frameN  # exact frame index
        example_text_2.tStart = t  # local t and not account for scr refresh
        example_text_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(example_text_2, 'tStartRefresh')  # time at next scr refresh
        example_text_2.setAutoDraw(True)
    # *mouse* updates
    if mouse.status == NOT_STARTED and t >= 1-frameTolerance:
        # keep track of start time/frame for later
        mouse.frameNStart = frameN  # exact frame index
        mouse.tStart = t  # local t and not account for scr refresh
        mouse.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
        mouse.status = STARTED
        mouse.mouseClock.reset()
        prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
    if mouse.status == STARTED:  # only update if started and not finished!
        buttons = mouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                try:
                    iter(example_image)
                    clickableList = example_image
                except:
                    clickableList = [example_image]
                for obj in clickableList:
                    if obj.contains(mouse):
                        gotValidClick = True
                        mouse.clicked_name.append(obj.name)
                if gotValidClick:  
                    continueRoutine = False  # abort routine on response
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in ExampleComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Example"-------
for thisComponent in ExampleComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('example_text.started', example_text.tStartRefresh)
thisExp.addData('example_text.stopped', example_text.tStopRefresh)
thisExp.addData('example_image.started', example_image.tStartRefresh)
thisExp.addData('example_image.stopped', example_image.tStopRefresh)
thisExp.addData('example_text_2.started', example_text_2.tStartRefresh)
thisExp.addData('example_text_2.stopped', example_text_2.tStopRefresh)
# store data for thisExp (ExperimentHandler)
thisExp.nextEntry()
# the Routine "Example" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
blocks = data.TrialHandler(nReps=2, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('chooseRule.xlsx'),
    seed=None, name='blocks')
thisExp.addLoop(blocks)  # add the loop to the experiment
thisBlock = blocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
if thisBlock != None:
    for paramName in thisBlock:
        exec('{} = thisBlock[paramName]'.format(paramName))

for thisBlock in blocks:
    currentLoop = blocks
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock:
            exec('{} = thisBlock[paramName]'.format(paramName))
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('cards.xlsx', selection=useRows),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "Trials"-------
        continueRoutine = True
        # update component parameters for each repeat
        corr = 0
        rt = 0
        print('card',card)
        print('corrAns',corrAns)
        trial_card.setImage(card)
        # setup some python lists for storing info about the response
        response.clicked_name = []
        gotValidClick = False  # until a click is received
        # keep track of which components have finished
        TrialsComponents = [fixation, one_red_dot, two_yellow_triangles, three_green_crosses, four_blue_stars, trial_card, response]
        for thisComponent in TrialsComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        TrialsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Trials"-------
        while continueRoutine:
            # get current time
            t = TrialsClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=TrialsClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # RT more accurate in Each Frame
            rt = round(t*1000)
            
            # *fixation* updates
            if fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation.frameNStart = frameN  # exact frame index
                fixation.tStart = t  # local t and not account for scr refresh
                fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                fixation.setAutoDraw(True)
            if fixation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation.tStop = t  # not accounting for scr refresh
                    fixation.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(fixation, 'tStopRefresh')  # time at next scr refresh
                    fixation.setAutoDraw(False)
            
            # *one_red_dot* updates
            if one_red_dot.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                one_red_dot.frameNStart = frameN  # exact frame index
                one_red_dot.tStart = t  # local t and not account for scr refresh
                one_red_dot.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(one_red_dot, 'tStartRefresh')  # time at next scr refresh
                one_red_dot.setAutoDraw(True)
            
            # *two_yellow_triangles* updates
            if two_yellow_triangles.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                two_yellow_triangles.frameNStart = frameN  # exact frame index
                two_yellow_triangles.tStart = t  # local t and not account for scr refresh
                two_yellow_triangles.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(two_yellow_triangles, 'tStartRefresh')  # time at next scr refresh
                two_yellow_triangles.setAutoDraw(True)
            
            # *three_green_crosses* updates
            if three_green_crosses.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                three_green_crosses.frameNStart = frameN  # exact frame index
                three_green_crosses.tStart = t  # local t and not account for scr refresh
                three_green_crosses.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(three_green_crosses, 'tStartRefresh')  # time at next scr refresh
                three_green_crosses.setAutoDraw(True)
            
            # *four_blue_stars* updates
            if four_blue_stars.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                four_blue_stars.frameNStart = frameN  # exact frame index
                four_blue_stars.tStart = t  # local t and not account for scr refresh
                four_blue_stars.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(four_blue_stars, 'tStartRefresh')  # time at next scr refresh
                four_blue_stars.setAutoDraw(True)
            
            # *trial_card* updates
            if trial_card.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                trial_card.frameNStart = frameN  # exact frame index
                trial_card.tStart = t  # local t and not account for scr refresh
                trial_card.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trial_card, 'tStartRefresh')  # time at next scr refresh
                trial_card.setAutoDraw(True)
            # *response* updates
            if response.status == NOT_STARTED and t >= 1-frameTolerance:
                # keep track of start time/frame for later
                response.frameNStart = frameN  # exact frame index
                response.tStart = t  # local t and not account for scr refresh
                response.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(response, 'tStartRefresh')  # time at next scr refresh
                response.status = STARTED
                response.mouseClock.reset()
                prevButtonState = response.getPressed()  # if button is down already this ISN'T a new click
            if response.status == STARTED:  # only update if started and not finished!
                buttons = response.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        # check if the mouse was inside our 'clickable' objects
                        gotValidClick = False
                        try:
                            iter([one_red_dot, two_yellow_triangles, three_green_crosses, four_blue_stars])
                            clickableList = [one_red_dot, two_yellow_triangles, three_green_crosses, four_blue_stars]
                        except:
                            clickableList = [[one_red_dot, two_yellow_triangles, three_green_crosses, four_blue_stars]]
                        for obj in clickableList:
                            if obj.contains(response):
                                gotValidClick = True
                                response.clicked_name.append(obj.name)
                        if gotValidClick:  
                            continueRoutine = False  # abort routine on response
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in TrialsComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Trials"-------
        for thisComponent in TrialsComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        if response.clicked_name == corrAns:
            corr = 1
        # clicked_name seems to fail on mobile so:
        elif one_red_dot.contains(response) and corrAns == 'one_red_dot':
            corr = 1
        elif two_yellow_triangles.contains(response) and corrAns == 'two_yellow_triangles':
            corr = 1
        elif three_green_crosses.contains(response) and corrAns == 'three_green_crosses':
            corr = 1
        elif four_blue_stars.contains(response) and corrAns == 'four_blue_stars':
            corr = 1
            
        print('Response',response.clicked_name)
        thisExp.addData('Score', corr)
        thisExp.addData('RT', rt)
        trials.addData('fixation.started', fixation.tStartRefresh)
        trials.addData('fixation.stopped', fixation.tStopRefresh)
        trials.addData('one_red_dot.started', one_red_dot.tStartRefresh)
        trials.addData('one_red_dot.stopped', one_red_dot.tStopRefresh)
        trials.addData('two_yellow_triangles.started', two_yellow_triangles.tStartRefresh)
        trials.addData('two_yellow_triangles.stopped', two_yellow_triangles.tStopRefresh)
        trials.addData('three_green_crosses.started', three_green_crosses.tStartRefresh)
        trials.addData('three_green_crosses.stopped', three_green_crosses.tStopRefresh)
        trials.addData('four_blue_stars.started', four_blue_stars.tStartRefresh)
        trials.addData('four_blue_stars.stopped', four_blue_stars.tStopRefresh)
        trials.addData('trial_card.started', trial_card.tStartRefresh)
        trials.addData('trial_card.stopped', trial_card.tStopRefresh)
        # store data for trials (TrialHandler)
        x, y = response.getPos()
        buttons = response.getPressed()
        if sum(buttons):
            # check if the mouse was inside our 'clickable' objects
            gotValidClick = False
            try:
                iter([one_red_dot, two_yellow_triangles, three_green_crosses, four_blue_stars])
                clickableList = [one_red_dot, two_yellow_triangles, three_green_crosses, four_blue_stars]
            except:
                clickableList = [[one_red_dot, two_yellow_triangles, three_green_crosses, four_blue_stars]]
            for obj in clickableList:
                if obj.contains(response):
                    gotValidClick = True
                    response.clicked_name.append(obj.name)
        trials.addData('response.x', x)
        trials.addData('response.y', y)
        trials.addData('response.leftButton', buttons[0])
        trials.addData('response.midButton', buttons[1])
        trials.addData('response.rightButton', buttons[2])
        if len(response.clicked_name):
            trials.addData('response.clicked_name', response.clicked_name[0])
        trials.addData('response.started', response.tStart)
        trials.addData('response.stopped', response.tStop)
        # the Routine "Trials" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "Feedback"-------
        continueRoutine = True
        routineTimer.add(1.000000)
        # update component parameters for each repeat
        if corr == 1:
            msg="Correct! "
        else:
            msg="Incorrect"
        feedback_text.setText(msg)
        # keep track of which components have finished
        FeedbackComponents = [feedback_text]
        for thisComponent in FeedbackComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        FeedbackClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Feedback"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = FeedbackClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=FeedbackClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *feedback_text* updates
            if feedback_text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                feedback_text.frameNStart = frameN  # exact frame index
                feedback_text.tStart = t  # local t and not account for scr refresh
                feedback_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(feedback_text, 'tStartRefresh')  # time at next scr refresh
                feedback_text.setAutoDraw(True)
            if feedback_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > feedback_text.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    feedback_text.tStop = t  # not accounting for scr refresh
                    feedback_text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(feedback_text, 'tStopRefresh')  # time at next scr refresh
                    feedback_text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in FeedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Feedback"-------
        for thisComponent in FeedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        if trials.thisTrialN == 6:
            trials.finished = True
        trials.addData('feedback_text.started', feedback_text.tStartRefresh)
        trials.addData('feedback_text.stopped', feedback_text.tStopRefresh)
        thisExp.nextEntry()
        
    # completed 1 repeats of 'trials'
    
    thisExp.nextEntry()
    
# completed 2 repeats of 'blocks'


# ------Prepare to start Routine "End"-------
continueRoutine = True
routineTimer.add(3.000000)
# update component parameters for each repeat
# keep track of which components have finished
EndComponents = [thank_you]
for thisComponent in EndComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
EndClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "End"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = EndClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=EndClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *thank_you* updates
    if thank_you.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        thank_you.frameNStart = frameN  # exact frame index
        thank_you.tStart = t  # local t and not account for scr refresh
        thank_you.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(thank_you, 'tStartRefresh')  # time at next scr refresh
        thank_you.setAutoDraw(True)
    if thank_you.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > thank_you.tStartRefresh + 3-frameTolerance:
            # keep track of stop time/frame for later
            thank_you.tStop = t  # not accounting for scr refresh
            thank_you.frameNStop = frameN  # exact frame index
            win.timeOnFlip(thank_you, 'tStopRefresh')  # time at next scr refresh
            thank_you.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in EndComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "End"-------
for thisComponent in EndComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('thank_you.started', thank_you.tStartRefresh)
thisExp.addData('thank_you.stopped', thank_you.tStopRefresh)

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
