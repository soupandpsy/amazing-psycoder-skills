# Source: Choice Reaction Time Task (demos/Choice_Reaction_Time_Task)
# Project URL: https://gitlab.pavlovia.org/demos/Choice_Reaction_Time_Task
# Original file: choiceRTT_lastrun.py
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.2.3),
    on January 07, 2022, at 19:30
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
prefs.hardware['audioLib'] = 'ptb'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.2.3'
expName = 'choiceRTT'  # from the Builder filename that created this script
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
    originPath='C:\\Users\\suely\\OneDrive\\Desktop\\demos\\updatedChoiceRTT\\choiceRTT_lastrun.py',
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
    size=[1280, 800], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='white', colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Setup eyetracking
ioDevice = ioConfig = ioSession = ioServer = eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
instr = visual.TextStim(win=win, name='instr',
    text='In this task you will make a decision as to which shape you have seen.\n\nPress C or click cross for a cross\nPress V or click square for a square\nPress B or click plus for a plus\n\nFirst, we will have a quick practice.\n\nPush space bar or click / touch one of the buttons to begin.',
    font='Arial',
    units='height', pos=(0, 0.1), height=0.035, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
startInst = keyboard.Keyboard()
startMouse = event.Mouse(win=win)
x, y = [None, None]
startMouse.mouseClock = core.Clock()
intro_square = visual.ImageStim(
    win=win,
    name='intro_square', 
    image='images/response_square.jpg', mask=None,
    ori=0.0, pos=(0, -0.25), size=(0.2, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
intro_plus = visual.ImageStim(
    win=win,
    name='intro_plus', 
    image='images/response_plus.jpg', mask=None,
    ori=0.0, pos=(0.25, -0.25), size=(0.2, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)
intro_cross = visual.ImageStim(
    win=win,
    name='intro_cross', 
    image='images/response_cross.jpg', mask=None,
    ori=0.0, pos=(-0.25, -0.25), size=(0.2, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-5.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
rightright_tile = visual.ImageStim(
    win=win,
    name='rightright_tile', 
    image='images/grey_square.jpg', mask=None,
    ori=0.0, pos=(0.375, 0), size=(0.22, 0.22),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
right_tile = visual.ImageStim(
    win=win,
    name='right_tile', 
    image='images/grey_square.jpg', mask=None,
    ori=0.0, pos=(0.125, 0), size=(0.22, 0.22),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
left_tile = visual.ImageStim(
    win=win,
    name='left_tile', 
    image='images/grey_square.jpg', mask=None,
    ori=0.0, pos=(-0.125, 0), size=(0.22, 0.22),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
leftleft_tile = visual.ImageStim(
    win=win,
    name='leftleft_tile', 
    image='images/grey_square.jpg', mask=None,
    ori=0.0, pos=(-0.375, 0), size=(0.22, 0.22),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)
square_button = visual.ImageStim(
    win=win,
    name='square_button', 
    image='images/response_square.jpg', mask=None,
    ori=0.0, pos=(0, -0.25), size=(0.2, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-5.0)
plus_button = visual.ImageStim(
    win=win,
    name='plus_button', 
    image='images/response_plus.jpg', mask=None,
    ori=0.0, pos=(0.25, -0.25), size=(0.2, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-6.0)
cross_button = visual.ImageStim(
    win=win,
    name='cross_button', 
    image='images/response_cross.jpg', mask=None,
    ori=0.0, pos=(-0.25, -0.25), size=(0.2, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-7.0)
targetImage = visual.ImageStim(
    win=win,
    name='targetImage', units='height', 
    image='sin', mask=None,
    ori=0, pos=[0,0], size=(0.2, 0.2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-8.0)
keyResp = keyboard.Keyboard()
mouseResp = event.Mouse(win=win)
x, y = [None, None]
mouseResp.mouseClock = core.Clock()

# Initialize components for Routine "trial_feedback"
trial_feedbackClock = core.Clock()
text_fb = visual.TextStim(win=win, name='text_fb',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
moveOnKeys = keyboard.Keyboard()
moveOnMouse = event.Mouse(win=win)
x, y = [None, None]
moveOnMouse.mouseClock = core.Clock()

# Initialize components for Routine "mainTrial_instruct"
mainTrial_instructClock = core.Clock()
main_trial_instruct = visual.TextStim(win=win, name='main_trial_instruct',
    text='Well done, that’s the practice over!\n\nNow for the main experiment.\n\nClick / tap / press space to continue!',
    font='Arial',
    pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp = keyboard.Keyboard()
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()
ready_button = visual.ImageStim(
    win=win,
    name='ready_button', 
    image='images/response_ready.jpg', mask=None,
    ori=0.0, pos=(0, -0.25), size=(0.2, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
rightright_tile = visual.ImageStim(
    win=win,
    name='rightright_tile', 
    image='images/grey_square.jpg', mask=None,
    ori=0.0, pos=(0.375, 0), size=(0.22, 0.22),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
right_tile = visual.ImageStim(
    win=win,
    name='right_tile', 
    image='images/grey_square.jpg', mask=None,
    ori=0.0, pos=(0.125, 0), size=(0.22, 0.22),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
left_tile = visual.ImageStim(
    win=win,
    name='left_tile', 
    image='images/grey_square.jpg', mask=None,
    ori=0.0, pos=(-0.125, 0), size=(0.22, 0.22),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
leftleft_tile = visual.ImageStim(
    win=win,
    name='leftleft_tile', 
    image='images/grey_square.jpg', mask=None,
    ori=0.0, pos=(-0.375, 0), size=(0.22, 0.22),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)
square_button = visual.ImageStim(
    win=win,
    name='square_button', 
    image='images/response_square.jpg', mask=None,
    ori=0.0, pos=(0, -0.25), size=(0.2, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-5.0)
plus_button = visual.ImageStim(
    win=win,
    name='plus_button', 
    image='images/response_plus.jpg', mask=None,
    ori=0.0, pos=(0.25, -0.25), size=(0.2, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-6.0)
cross_button = visual.ImageStim(
    win=win,
    name='cross_button', 
    image='images/response_cross.jpg', mask=None,
    ori=0.0, pos=(-0.25, -0.25), size=(0.2, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-7.0)
targetImage = visual.ImageStim(
    win=win,
    name='targetImage', units='height', 
    image='sin', mask=None,
    ori=0, pos=[0,0], size=(0.2, 0.2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-8.0)
keyResp = keyboard.Keyboard()
mouseResp = event.Mouse(win=win)
x, y = [None, None]
mouseResp.mouseClock = core.Clock()

# Initialize components for Routine "end_message"
end_messageClock = core.Clock()
end_text = visual.TextStim(win=win, name='end_text',
    text='That’s the experiment finished!\n\nThanks for your time. You’ve earned a cup of tea.',
    font='Arial',
    pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "instructions"-------
continueRoutine = True
# update component parameters for each repeat
startInst.keys = []
startInst.rt = []
_startInst_allKeys = []
# setup some python lists for storing info about the startMouse
gotValidClick = False  # until a click is received
startMouse.mouseClock.reset()
# keep track of which components have finished
instructionsComponents = [instr, startInst, startMouse, intro_square, intro_plus, intro_cross]
for thisComponent in instructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
instructionsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "instructions"-------
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=instructionsClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instr* updates
    if instr.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instr.frameNStart = frameN  # exact frame index
        instr.tStart = t  # local t and not account for scr refresh
        instr.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instr, 'tStartRefresh')  # time at next scr refresh
        instr.setAutoDraw(True)
    
    # *startInst* updates
    waitOnFlip = False
    if startInst.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        startInst.frameNStart = frameN  # exact frame index
        startInst.tStart = t  # local t and not account for scr refresh
        startInst.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(startInst, 'tStartRefresh')  # time at next scr refresh
        startInst.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(startInst.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(startInst.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if startInst.status == STARTED and not waitOnFlip:
        theseKeys = startInst.getKeys(keyList=None, waitRelease=False)
        _startInst_allKeys.extend(theseKeys)
        if len(_startInst_allKeys):
            startInst.keys = _startInst_allKeys[-1].name  # just the last key pressed
            startInst.rt = _startInst_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    # *startMouse* updates
    if startMouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        startMouse.frameNStart = frameN  # exact frame index
        startMouse.tStart = t  # local t and not account for scr refresh
        startMouse.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(startMouse, 'tStartRefresh')  # time at next scr refresh
        startMouse.status = STARTED
        prevButtonState = startMouse.getPressed()  # if button is down already this ISN'T a new click
    if startMouse.status == STARTED:  # only update if started and not finished!
        buttons = startMouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                continueRoutine = False    
    # *intro_square* updates
    if intro_square.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        intro_square.frameNStart = frameN  # exact frame index
        intro_square.tStart = t  # local t and not account for scr refresh
        intro_square.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(intro_square, 'tStartRefresh')  # time at next scr refresh
        intro_square.setAutoDraw(True)
    
    # *intro_plus* updates
    if intro_plus.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        intro_plus.frameNStart = frameN  # exact frame index
        intro_plus.tStart = t  # local t and not account for scr refresh
        intro_plus.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(intro_plus, 'tStartRefresh')  # time at next scr refresh
        intro_plus.setAutoDraw(True)
    
    # *intro_cross* updates
    if intro_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        intro_cross.frameNStart = frameN  # exact frame index
        intro_cross.tStart = t  # local t and not account for scr refresh
        intro_cross.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(intro_cross, 'tStartRefresh')  # time at next scr refresh
        intro_cross.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# store data for thisExp (ExperimentHandler)
thisExp.addData('startMouse.started', startMouse.tStart)
thisExp.addData('startMouse.stopped', startMouse.tStop)
thisExp.nextEntry()
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
PracticeLoop = data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('RTtimeConditions.xlsx'),
    seed=None, name='PracticeLoop')
thisExp.addLoop(PracticeLoop)  # add the loop to the experiment
thisPracticeLoop = PracticeLoop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPracticeLoop.rgb)
if thisPracticeLoop != None:
    for paramName in thisPracticeLoop:
        exec('{} = thisPracticeLoop[paramName]'.format(paramName))

for thisPracticeLoop in PracticeLoop:
    currentLoop = PracticeLoop
    # abbreviate parameter names if possible (e.g. rgb = thisPracticeLoop.rgb)
    if thisPracticeLoop != None:
        for paramName in thisPracticeLoop:
            exec('{} = thisPracticeLoop[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "trial"-------
    continueRoutine = True
    # update component parameters for each repeat
    positionList = [-0.375,-0.125,0.125,0.375] #list of possible X coordinates for target to appear
    shuffle(positionList) #randomise these positions
    targetX = positionList[0] #pick the first value from the list 
    
    #thisImage is the variable in the Image field of targetImage
    if thisImage == 'images/target_square.jpg': #path of where to find the target image
        corrAns = 'v' #setting the key press that will be the correct answer
        corrButton = square_button #setting the button that will be the correct answer
        corrButtonName = 'square_button' #making this a string so that it can be compared later when checking for acccuracy
    elif thisImage == 'images/target_cross.jpg':
        corrAns = 'c'
        corrButton = cross_button
        corrButtonName = 'cross_button'
    elif thisImage == 'images/target_plus.jpg':
        corrAns = 'b'
        corrButton = plus_button
        corrButtonName = 'plus_button'
    
    
    targetImage.setPos([targetX, 0])
    targetImage.setImage(thisImage)
    keyResp.keys = []
    keyResp.rt = []
    _keyResp_allKeys = []
    # setup some python lists for storing info about the mouseResp
    mouseResp.x = []
    mouseResp.y = []
    mouseResp.leftButton = []
    mouseResp.midButton = []
    mouseResp.rightButton = []
    mouseResp.time = []
    mouseResp.clicked_name = []
    gotValidClick = False  # until a click is received
    mouseResp.mouseClock.reset()
    # keep track of which components have finished
    trialComponents = [rightright_tile, right_tile, left_tile, leftleft_tile, square_button, plus_button, cross_button, targetImage, keyResp, mouseResp]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=trialClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *rightright_tile* updates
        if rightright_tile.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            rightright_tile.frameNStart = frameN  # exact frame index
            rightright_tile.tStart = t  # local t and not account for scr refresh
            rightright_tile.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(rightright_tile, 'tStartRefresh')  # time at next scr refresh
            rightright_tile.setAutoDraw(True)
        
        # *right_tile* updates
        if right_tile.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            right_tile.frameNStart = frameN  # exact frame index
            right_tile.tStart = t  # local t and not account for scr refresh
            right_tile.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(right_tile, 'tStartRefresh')  # time at next scr refresh
            right_tile.setAutoDraw(True)
        
        # *left_tile* updates
        if left_tile.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            left_tile.frameNStart = frameN  # exact frame index
            left_tile.tStart = t  # local t and not account for scr refresh
            left_tile.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(left_tile, 'tStartRefresh')  # time at next scr refresh
            left_tile.setAutoDraw(True)
        
        # *leftleft_tile* updates
        if leftleft_tile.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            leftleft_tile.frameNStart = frameN  # exact frame index
            leftleft_tile.tStart = t  # local t and not account for scr refresh
            leftleft_tile.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(leftleft_tile, 'tStartRefresh')  # time at next scr refresh
            leftleft_tile.setAutoDraw(True)
        
        # *square_button* updates
        if square_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            square_button.frameNStart = frameN  # exact frame index
            square_button.tStart = t  # local t and not account for scr refresh
            square_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(square_button, 'tStartRefresh')  # time at next scr refresh
            square_button.setAutoDraw(True)
        
        # *plus_button* updates
        if plus_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            plus_button.frameNStart = frameN  # exact frame index
            plus_button.tStart = t  # local t and not account for scr refresh
            plus_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(plus_button, 'tStartRefresh')  # time at next scr refresh
            plus_button.setAutoDraw(True)
        
        # *cross_button* updates
        if cross_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            cross_button.frameNStart = frameN  # exact frame index
            cross_button.tStart = t  # local t and not account for scr refresh
            cross_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(cross_button, 'tStartRefresh')  # time at next scr refresh
            cross_button.setAutoDraw(True)
        
        # *targetImage* updates
        if targetImage.status == NOT_STARTED and tThisFlip >= onsetTime-frameTolerance:
            # keep track of start time/frame for later
            targetImage.frameNStart = frameN  # exact frame index
            targetImage.tStart = t  # local t and not account for scr refresh
            targetImage.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(targetImage, 'tStartRefresh')  # time at next scr refresh
            targetImage.setAutoDraw(True)
        if targetImage.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > targetImage.tStartRefresh + 0.2-frameTolerance:
                # keep track of stop time/frame for later
                targetImage.tStop = t  # not accounting for scr refresh
                targetImage.frameNStop = frameN  # exact frame index
                win.timeOnFlip(targetImage, 'tStopRefresh')  # time at next scr refresh
                targetImage.setAutoDraw(False)
        
        # *keyResp* updates
        if keyResp.status == NOT_STARTED and t >= 0-frameTolerance:
            # keep track of start time/frame for later
            keyResp.frameNStart = frameN  # exact frame index
            keyResp.tStart = t  # local t and not account for scr refresh
            keyResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(keyResp, 'tStartRefresh')  # time at next scr refresh
            keyResp.status = STARTED
            # keyboard checking is just starting
            keyResp.clock.reset()  # now t=0
            keyResp.clearEvents(eventType='keyboard')
        if keyResp.status == STARTED:
            theseKeys = keyResp.getKeys(keyList=['b', 'c', 'v'], waitRelease=False)
            _keyResp_allKeys.extend(theseKeys)
            if len(_keyResp_allKeys):
                keyResp.keys = _keyResp_allKeys[-1].name  # just the last key pressed
                keyResp.rt = _keyResp_allKeys[-1].rt
                # was this correct?
                if (keyResp.keys == str(corrAns)) or (keyResp.keys == corrAns):
                    keyResp.corr = 1
                else:
                    keyResp.corr = 0
                # a response ends the routine
                continueRoutine = False
        # *mouseResp* updates
        if mouseResp.status == NOT_STARTED and t >= 0-frameTolerance:
            # keep track of start time/frame for later
            mouseResp.frameNStart = frameN  # exact frame index
            mouseResp.tStart = t  # local t and not account for scr refresh
            mouseResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouseResp, 'tStartRefresh')  # time at next scr refresh
            mouseResp.status = STARTED
            prevButtonState = mouseResp.getPressed()  # if button is down already this ISN'T a new click
        if mouseResp.status == STARTED:  # only update if started and not finished!
            buttons = mouseResp.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    try:
                        iter(square_button, plus_button, cross_button)
                        clickableList = square_button, plus_button, cross_button
                    except:
                        clickableList = [square_button, plus_button, cross_button]
                    for obj in clickableList:
                        if obj.contains(mouseResp):
                            gotValidClick = True
                            mouseResp.clicked_name.append(obj.name)
                    x, y = mouseResp.getPos()
                    mouseResp.x.append(x)
                    mouseResp.y.append(y)
                    buttons = mouseResp.getPressed()
                    mouseResp.leftButton.append(buttons[0])
                    mouseResp.midButton.append(buttons[1])
                    mouseResp.rightButton.append(buttons[2])
                    mouseResp.time.append(mouseResp.mouseClock.getTime())
                    if gotValidClick:  # abort routine on response
                        continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    PracticeLoop.addData('targetImage.started', targetImage.tStartRefresh)
    PracticeLoop.addData('targetImage.stopped', targetImage.tStopRefresh)
    # check responses
    if keyResp.keys in ['', [], None]:  # No response was made
        keyResp.keys = None
        # was no response the correct answer?!
        if str(corrAns).lower() == 'none':
           keyResp.corr = 1;  # correct non-response
        else:
           keyResp.corr = 0;  # failed to respond (incorrectly)
    # store data for PracticeLoop (TrialHandler)
    PracticeLoop.addData('keyResp.keys',keyResp.keys)
    PracticeLoop.addData('keyResp.corr', keyResp.corr)
    if keyResp.keys != None:  # we had a response
        PracticeLoop.addData('keyResp.rt', keyResp.rt)
    # store data for PracticeLoop (TrialHandler)
    if len(mouseResp.x): PracticeLoop.addData('mouseResp.x', mouseResp.x[0])
    if len(mouseResp.y): PracticeLoop.addData('mouseResp.y', mouseResp.y[0])
    if len(mouseResp.leftButton): PracticeLoop.addData('mouseResp.leftButton', mouseResp.leftButton[0])
    if len(mouseResp.midButton): PracticeLoop.addData('mouseResp.midButton', mouseResp.midButton[0])
    if len(mouseResp.rightButton): PracticeLoop.addData('mouseResp.rightButton', mouseResp.rightButton[0])
    if len(mouseResp.time): PracticeLoop.addData('mouseResp.time', mouseResp.time[0])
    if len(mouseResp.clicked_name): PracticeLoop.addData('mouseResp.clicked_name', mouseResp.clicked_name[0])
    #this code is to record the reaction times and accuracy of the trial
    
    thisRoutineDuration = t # how long did this trial last
    
    # keyResp.rt is the time with which a key was pressed
    # mouseResp.time is the time with which a button was clicked/pressed
    # thisRecRT - how long it took for participants to respond after onset of targetImage
    # thisRespType - keeping track of which response component was used
    # thisAcc - whether or not the response was correct
    # correctMouseResp - name of column in data output which records the accuracy of mouse responses
    
    if keyResp.keys:
        thisRespType = 'keyboard' #record type of response 
        thisRecRT = keyResp.rt - onsetTime #record time taken to response
        if keyResp.corr == 1: #if the response is correct
            thisAcc = 'correct' #print correct
        else:
            thisAcc = 'incorrect'
    else:
        thisRespType = 'mouse'
        thisRecRT = mouseResp.time[0] - onsetTime
        if mouseResp.clicked_name[0] == corrButtonName: #check if what was clicked corresponds to the correct button
            thisAcc = 'correct'
            thisExp.addData('correctMouseResp', 1) #record accuracy of mouse clicks
        else:
            thisAcc = 'incorrect'
            thisExp.addData('correctMouseResp', 0)
    
    thisExp.addData('trialRespTimes', thisRecRT) #record the actual response times of each trial
    
    
    #print(thisRoutineDuration, thisRecRT, thisRespType, thisAcc, onsetTime)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "trial_feedback"-------
    continueRoutine = True
    # update component parameters for each repeat
    text_fb.setText("The duration of the last routine was: "  + str(round(thisRoutineDuration, 3)) + " \nThe last recorded RT was: "  + str(round(thisRecRT, 3)) + " \nThe response type was: "  + thisRespType + " \nThe response was: "  + thisAcc + " \n\nPress or click to continue."  )
    moveOnKeys.keys = []
    moveOnKeys.rt = []
    _moveOnKeys_allKeys = []
    # setup some python lists for storing info about the moveOnMouse
    gotValidClick = False  # until a click is received
    moveOnMouse.mouseClock.reset()
    # keep track of which components have finished
    trial_feedbackComponents = [text_fb, moveOnKeys, moveOnMouse]
    for thisComponent in trial_feedbackComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    trial_feedbackClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "trial_feedback"-------
    while continueRoutine:
        # get current time
        t = trial_feedbackClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=trial_feedbackClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_fb* updates
        if text_fb.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_fb.frameNStart = frameN  # exact frame index
            text_fb.tStart = t  # local t and not account for scr refresh
            text_fb.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_fb, 'tStartRefresh')  # time at next scr refresh
            text_fb.setAutoDraw(True)
        
        # *moveOnKeys* updates
        waitOnFlip = False
        if moveOnKeys.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            moveOnKeys.frameNStart = frameN  # exact frame index
            moveOnKeys.tStart = t  # local t and not account for scr refresh
            moveOnKeys.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(moveOnKeys, 'tStartRefresh')  # time at next scr refresh
            moveOnKeys.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(moveOnKeys.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(moveOnKeys.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if moveOnKeys.status == STARTED and not waitOnFlip:
            theseKeys = moveOnKeys.getKeys(keyList=['c', 'v', 'b', 'space'], waitRelease=False)
            _moveOnKeys_allKeys.extend(theseKeys)
            if len(_moveOnKeys_allKeys):
                moveOnKeys.keys = _moveOnKeys_allKeys[-1].name  # just the last key pressed
                moveOnKeys.rt = _moveOnKeys_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        # *moveOnMouse* updates
        if moveOnMouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            moveOnMouse.frameNStart = frameN  # exact frame index
            moveOnMouse.tStart = t  # local t and not account for scr refresh
            moveOnMouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(moveOnMouse, 'tStartRefresh')  # time at next scr refresh
            moveOnMouse.status = STARTED
            prevButtonState = moveOnMouse.getPressed()  # if button is down already this ISN'T a new click
        if moveOnMouse.status == STARTED:  # only update if started and not finished!
            buttons = moveOnMouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    continueRoutine = False        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trial_feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "trial_feedback"-------
    for thisComponent in trial_feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    PracticeLoop.addData('text_fb.started', text_fb.tStartRefresh)
    PracticeLoop.addData('text_fb.stopped', text_fb.tStopRefresh)
    # check responses
    if moveOnKeys.keys in ['', [], None]:  # No response was made
        moveOnKeys.keys = None
    PracticeLoop.addData('moveOnKeys.keys',moveOnKeys.keys)
    if moveOnKeys.keys != None:  # we had a response
        PracticeLoop.addData('moveOnKeys.rt', moveOnKeys.rt)
    PracticeLoop.addData('moveOnKeys.started', moveOnKeys.tStartRefresh)
    PracticeLoop.addData('moveOnKeys.stopped', moveOnKeys.tStopRefresh)
    # store data for PracticeLoop (TrialHandler)
    PracticeLoop.addData('moveOnMouse.started', moveOnMouse.tStart)
    PracticeLoop.addData('moveOnMouse.stopped', moveOnMouse.tStop)
    # the Routine "trial_feedback" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'PracticeLoop'


# ------Prepare to start Routine "mainTrial_instruct"-------
continueRoutine = True
# update component parameters for each repeat
key_resp.keys = []
key_resp.rt = []
_key_resp_allKeys = []
# setup some python lists for storing info about the mouse
gotValidClick = False  # until a click is received
# keep track of which components have finished
mainTrial_instructComponents = [main_trial_instruct, key_resp, mouse, ready_button]
for thisComponent in mainTrial_instructComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
mainTrial_instructClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "mainTrial_instruct"-------
while continueRoutine:
    # get current time
    t = mainTrial_instructClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=mainTrial_instructClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *main_trial_instruct* updates
    if main_trial_instruct.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
        # keep track of start time/frame for later
        main_trial_instruct.frameNStart = frameN  # exact frame index
        main_trial_instruct.tStart = t  # local t and not account for scr refresh
        main_trial_instruct.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(main_trial_instruct, 'tStartRefresh')  # time at next scr refresh
        main_trial_instruct.setAutoDraw(True)
    
    # *key_resp* updates
    waitOnFlip = False
    if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp.frameNStart = frameN  # exact frame index
        key_resp.tStart = t  # local t and not account for scr refresh
        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
        key_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp.status == STARTED and not waitOnFlip:
        theseKeys = key_resp.getKeys(keyList=['y', 'n', 'left', 'right', 'space'], waitRelease=False)
        _key_resp_allKeys.extend(theseKeys)
        if len(_key_resp_allKeys):
            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
            key_resp.rt = _key_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    # *mouse* updates
    if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
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
                # abort routine on response
                continueRoutine = False
    
    # *ready_button* updates
    if ready_button.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        ready_button.frameNStart = frameN  # exact frame index
        ready_button.tStart = t  # local t and not account for scr refresh
        ready_button.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ready_button, 'tStartRefresh')  # time at next scr refresh
        ready_button.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in mainTrial_instructComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "mainTrial_instruct"-------
for thisComponent in mainTrial_instructComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp.keys in ['', [], None]:  # No response was made
    key_resp.keys = None
thisExp.addData('key_resp.keys',key_resp.keys)
if key_resp.keys != None:  # we had a response
    thisExp.addData('key_resp.rt', key_resp.rt)
thisExp.addData('key_resp.started', key_resp.tStartRefresh)
thisExp.addData('key_resp.stopped', key_resp.tStopRefresh)
thisExp.nextEntry()
# store data for thisExp (ExperimentHandler)
x, y = mouse.getPos()
buttons = mouse.getPressed()
thisExp.addData('mouse.x', x)
thisExp.addData('mouse.y', y)
thisExp.addData('mouse.leftButton', buttons[0])
thisExp.addData('mouse.midButton', buttons[1])
thisExp.addData('mouse.rightButton', buttons[2])
thisExp.addData('mouse.started', mouse.tStart)
thisExp.addData('mouse.stopped', mouse.tStop)
thisExp.nextEntry()
# the Routine "mainTrial_instruct" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
ExptLoop = data.TrialHandler(nReps=2.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('RTtimeConditions.xlsx'),
    seed=None, name='ExptLoop')
thisExp.addLoop(ExptLoop)  # add the loop to the experiment
thisExptLoop = ExptLoop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisExptLoop.rgb)
if thisExptLoop != None:
    for paramName in thisExptLoop:
        exec('{} = thisExptLoop[paramName]'.format(paramName))

for thisExptLoop in ExptLoop:
    currentLoop = ExptLoop
    # abbreviate parameter names if possible (e.g. rgb = thisExptLoop.rgb)
    if thisExptLoop != None:
        for paramName in thisExptLoop:
            exec('{} = thisExptLoop[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "trial"-------
    continueRoutine = True
    # update component parameters for each repeat
    positionList = [-0.375,-0.125,0.125,0.375] #list of possible X coordinates for target to appear
    shuffle(positionList) #randomise these positions
    targetX = positionList[0] #pick the first value from the list 
    
    #thisImage is the variable in the Image field of targetImage
    if thisImage == 'images/target_square.jpg': #path of where to find the target image
        corrAns = 'v' #setting the key press that will be the correct answer
        corrButton = square_button #setting the button that will be the correct answer
        corrButtonName = 'square_button' #making this a string so that it can be compared later when checking for acccuracy
    elif thisImage == 'images/target_cross.jpg':
        corrAns = 'c'
        corrButton = cross_button
        corrButtonName = 'cross_button'
    elif thisImage == 'images/target_plus.jpg':
        corrAns = 'b'
        corrButton = plus_button
        corrButtonName = 'plus_button'
    
    
    targetImage.setPos([targetX, 0])
    targetImage.setImage(thisImage)
    keyResp.keys = []
    keyResp.rt = []
    _keyResp_allKeys = []
    # setup some python lists for storing info about the mouseResp
    mouseResp.x = []
    mouseResp.y = []
    mouseResp.leftButton = []
    mouseResp.midButton = []
    mouseResp.rightButton = []
    mouseResp.time = []
    mouseResp.clicked_name = []
    gotValidClick = False  # until a click is received
    mouseResp.mouseClock.reset()
    # keep track of which components have finished
    trialComponents = [rightright_tile, right_tile, left_tile, leftleft_tile, square_button, plus_button, cross_button, targetImage, keyResp, mouseResp]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=trialClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *rightright_tile* updates
        if rightright_tile.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            rightright_tile.frameNStart = frameN  # exact frame index
            rightright_tile.tStart = t  # local t and not account for scr refresh
            rightright_tile.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(rightright_tile, 'tStartRefresh')  # time at next scr refresh
            rightright_tile.setAutoDraw(True)
        
        # *right_tile* updates
        if right_tile.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            right_tile.frameNStart = frameN  # exact frame index
            right_tile.tStart = t  # local t and not account for scr refresh
            right_tile.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(right_tile, 'tStartRefresh')  # time at next scr refresh
            right_tile.setAutoDraw(True)
        
        # *left_tile* updates
        if left_tile.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            left_tile.frameNStart = frameN  # exact frame index
            left_tile.tStart = t  # local t and not account for scr refresh
            left_tile.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(left_tile, 'tStartRefresh')  # time at next scr refresh
            left_tile.setAutoDraw(True)
        
        # *leftleft_tile* updates
        if leftleft_tile.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            leftleft_tile.frameNStart = frameN  # exact frame index
            leftleft_tile.tStart = t  # local t and not account for scr refresh
            leftleft_tile.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(leftleft_tile, 'tStartRefresh')  # time at next scr refresh
            leftleft_tile.setAutoDraw(True)
        
        # *square_button* updates
        if square_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            square_button.frameNStart = frameN  # exact frame index
            square_button.tStart = t  # local t and not account for scr refresh
            square_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(square_button, 'tStartRefresh')  # time at next scr refresh
            square_button.setAutoDraw(True)
        
        # *plus_button* updates
        if plus_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            plus_button.frameNStart = frameN  # exact frame index
            plus_button.tStart = t  # local t and not account for scr refresh
            plus_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(plus_button, 'tStartRefresh')  # time at next scr refresh
            plus_button.setAutoDraw(True)
        
        # *cross_button* updates
        if cross_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            cross_button.frameNStart = frameN  # exact frame index
            cross_button.tStart = t  # local t and not account for scr refresh
            cross_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(cross_button, 'tStartRefresh')  # time at next scr refresh
            cross_button.setAutoDraw(True)
        
        # *targetImage* updates
        if targetImage.status == NOT_STARTED and tThisFlip >= onsetTime-frameTolerance:
            # keep track of start time/frame for later
            targetImage.frameNStart = frameN  # exact frame index
            targetImage.tStart = t  # local t and not account for scr refresh
            targetImage.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(targetImage, 'tStartRefresh')  # time at next scr refresh
            targetImage.setAutoDraw(True)
        if targetImage.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > targetImage.tStartRefresh + 0.2-frameTolerance:
                # keep track of stop time/frame for later
                targetImage.tStop = t  # not accounting for scr refresh
                targetImage.frameNStop = frameN  # exact frame index
                win.timeOnFlip(targetImage, 'tStopRefresh')  # time at next scr refresh
                targetImage.setAutoDraw(False)
        
        # *keyResp* updates
        if keyResp.status == NOT_STARTED and t >= 0-frameTolerance:
            # keep track of start time/frame for later
            keyResp.frameNStart = frameN  # exact frame index
            keyResp.tStart = t  # local t and not account for scr refresh
            keyResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(keyResp, 'tStartRefresh')  # time at next scr refresh
            keyResp.status = STARTED
            # keyboard checking is just starting
            keyResp.clock.reset()  # now t=0
            keyResp.clearEvents(eventType='keyboard')
        if keyResp.status == STARTED:
            theseKeys = keyResp.getKeys(keyList=['b', 'c', 'v'], waitRelease=False)
            _keyResp_allKeys.extend(theseKeys)
            if len(_keyResp_allKeys):
                keyResp.keys = _keyResp_allKeys[-1].name  # just the last key pressed
                keyResp.rt = _keyResp_allKeys[-1].rt
                # was this correct?
                if (keyResp.keys == str(corrAns)) or (keyResp.keys == corrAns):
                    keyResp.corr = 1
                else:
                    keyResp.corr = 0
                # a response ends the routine
                continueRoutine = False
        # *mouseResp* updates
        if mouseResp.status == NOT_STARTED and t >= 0-frameTolerance:
            # keep track of start time/frame for later
            mouseResp.frameNStart = frameN  # exact frame index
            mouseResp.tStart = t  # local t and not account for scr refresh
            mouseResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouseResp, 'tStartRefresh')  # time at next scr refresh
            mouseResp.status = STARTED
            prevButtonState = mouseResp.getPressed()  # if button is down already this ISN'T a new click
        if mouseResp.status == STARTED:  # only update if started and not finished!
            buttons = mouseResp.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    try:
                        iter(square_button, plus_button, cross_button)
                        clickableList = square_button, plus_button, cross_button
                    except:
                        clickableList = [square_button, plus_button, cross_button]
                    for obj in clickableList:
                        if obj.contains(mouseResp):
                            gotValidClick = True
                            mouseResp.clicked_name.append(obj.name)
                    x, y = mouseResp.getPos()
                    mouseResp.x.append(x)
                    mouseResp.y.append(y)
                    buttons = mouseResp.getPressed()
                    mouseResp.leftButton.append(buttons[0])
                    mouseResp.midButton.append(buttons[1])
                    mouseResp.rightButton.append(buttons[2])
                    mouseResp.time.append(mouseResp.mouseClock.getTime())
                    if gotValidClick:  # abort routine on response
                        continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    ExptLoop.addData('targetImage.started', targetImage.tStartRefresh)
    ExptLoop.addData('targetImage.stopped', targetImage.tStopRefresh)
    # check responses
    if keyResp.keys in ['', [], None]:  # No response was made
        keyResp.keys = None
        # was no response the correct answer?!
        if str(corrAns).lower() == 'none':
           keyResp.corr = 1;  # correct non-response
        else:
           keyResp.corr = 0;  # failed to respond (incorrectly)
    # store data for ExptLoop (TrialHandler)
    ExptLoop.addData('keyResp.keys',keyResp.keys)
    ExptLoop.addData('keyResp.corr', keyResp.corr)
    if keyResp.keys != None:  # we had a response
        ExptLoop.addData('keyResp.rt', keyResp.rt)
    # store data for ExptLoop (TrialHandler)
    if len(mouseResp.x): ExptLoop.addData('mouseResp.x', mouseResp.x[0])
    if len(mouseResp.y): ExptLoop.addData('mouseResp.y', mouseResp.y[0])
    if len(mouseResp.leftButton): ExptLoop.addData('mouseResp.leftButton', mouseResp.leftButton[0])
    if len(mouseResp.midButton): ExptLoop.addData('mouseResp.midButton', mouseResp.midButton[0])
    if len(mouseResp.rightButton): ExptLoop.addData('mouseResp.rightButton', mouseResp.rightButton[0])
    if len(mouseResp.time): ExptLoop.addData('mouseResp.time', mouseResp.time[0])
    if len(mouseResp.clicked_name): ExptLoop.addData('mouseResp.clicked_name', mouseResp.clicked_name[0])
    #this code is to record the reaction times and accuracy of the trial
    
    thisRoutineDuration = t # how long did this trial last
    
    # keyResp.rt is the time with which a key was pressed
    # mouseResp.time is the time with which a button was clicked/pressed
    # thisRecRT - how long it took for participants to respond after onset of targetImage
    # thisRespType - keeping track of which response component was used
    # thisAcc - whether or not the response was correct
    # correctMouseResp - name of column in data output which records the accuracy of mouse responses
    
    if keyResp.keys:
        thisRespType = 'keyboard' #record type of response 
        thisRecRT = keyResp.rt - onsetTime #record time taken to response
        if keyResp.corr == 1: #if the response is correct
            thisAcc = 'correct' #print correct
        else:
            thisAcc = 'incorrect'
    else:
        thisRespType = 'mouse'
        thisRecRT = mouseResp.time[0] - onsetTime
        if mouseResp.clicked_name[0] == corrButtonName: #check if what was clicked corresponds to the correct button
            thisAcc = 'correct'
            thisExp.addData('correctMouseResp', 1) #record accuracy of mouse clicks
        else:
            thisAcc = 'incorrect'
            thisExp.addData('correctMouseResp', 0)
    
    thisExp.addData('trialRespTimes', thisRecRT) #record the actual response times of each trial
    
    
    #print(thisRoutineDuration, thisRecRT, thisRespType, thisAcc, onsetTime)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 2.0 repeats of 'ExptLoop'


# ------Prepare to start Routine "end_message"-------
continueRoutine = True
routineTimer.add(3.000000)
# update component parameters for each repeat
# keep track of which components have finished
end_messageComponents = [end_text]
for thisComponent in end_messageComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
end_messageClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "end_message"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = end_messageClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=end_messageClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_text* updates
    if end_text.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
        # keep track of start time/frame for later
        end_text.frameNStart = frameN  # exact frame index
        end_text.tStart = t  # local t and not account for scr refresh
        end_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_text, 'tStartRefresh')  # time at next scr refresh
        end_text.setAutoDraw(True)
    if end_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > end_text.tStartRefresh + 2.5-frameTolerance:
            # keep track of stop time/frame for later
            end_text.tStop = t  # not accounting for scr refresh
            end_text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(end_text, 'tStopRefresh')  # time at next scr refresh
            end_text.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in end_messageComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end_message"-------
for thisComponent in end_messageComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
