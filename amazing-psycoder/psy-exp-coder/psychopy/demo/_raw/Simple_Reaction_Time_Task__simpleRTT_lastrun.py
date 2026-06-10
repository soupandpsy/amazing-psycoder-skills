# Source: Simple Reaction Time Task (demos/Simple_Reaction_Time_Task)
# Project URL: https://gitlab.pavlovia.org/demos/Simple_Reaction_Time_Task
# Original file: simpleRTT_lastrun.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.0.0alpha3),
    on August 29, 2018, at 15:34
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'simpleRTT'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\lpzdb\\pavloviaDemos\\simpleRTT\\simpleRTT_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
instr = visual.TextStim(win=win, name='instr',
    text="In this task you will push the space bar or click/touch the target whenever you see the target 'X' appear.\n\nFirst, we shall have a practice.\n\nPush space bar or click/touch to begin the practice session.",
    font='Arial',
    units='height', pos=(0, 0), height=0.03, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Initialize components for Routine "main"
mainClock = core.Clock()
bgMain = visual.ImageStim(
    win=win, name='bgMain',units='height', 
    image='plainWhite.png', mask=None,
    ori=0, pos=(0, 0), size=(0.25, 0.25),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
targ = visual.ImageStim(
    win=win, name='targ',units='height', 
    image='target.png', mask=None,
    ori=0, pos=(0, 0), size=(0.25, 0.25),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
mouseResp = event.Mouse(win=win)
x, y = [None, None]
mouseResp.mouseClock = core.Clock()

# Initialize components for Routine "startTask"
startTaskClock = core.Clock()
ready = visual.TextStim(win=win, name='ready',
    text='Now we shall begin the actual experiment.\n\nReady?\n\nPush space bar or click/touch to begin.',
    font='Arial',
    units='height', pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
mouseGo = event.Mouse(win=win)
x, y = [None, None]
mouseGo.mouseClock = core.Clock()

# Initialize components for Routine "main"
mainClock = core.Clock()
bgMain = visual.ImageStim(
    win=win, name='bgMain',units='height', 
    image='plainWhite.png', mask=None,
    ori=0, pos=(0, 0), size=(0.25, 0.25),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
targ = visual.ImageStim(
    win=win, name='targ',units='height', 
    image='target.png', mask=None,
    ori=0, pos=(0, 0), size=(0.25, 0.25),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
mouseResp = event.Mouse(win=win)
x, y = [None, None]
mouseResp.mouseClock = core.Clock()

# Initialize components for Routine "thanks"
thanksClock = core.Clock()
thanksText = visual.TextStim(win=win, name='thanksText',
    text='Thank you for participating.\n\nThe experiment is now over.',
    font='Arial',
    units='height', pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "instructions"-------
t = 0
instructionsClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
startInst = event.BuilderKeyResponse()
# setup some python lists for storing info about the mouse
gotValidClick = False  # until a click is received
mouse.mouseClock.reset()
# keep track of which components have finished
instructionsComponents = [instr, startInst, mouse]
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instructions"-------
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instr* updates
    if t >= 0.0 and instr.status == NOT_STARTED:
        # keep track of start time/frame for later
        instr.tStart = t
        instr.frameNStart = frameN  # exact frame index
        instr.setAutoDraw(True)
    
    # *startInst* updates
    if t >= 0.0 and startInst.status == NOT_STARTED:
        # keep track of start time/frame for later
        startInst.tStart = t
        startInst.frameNStart = frameN  # exact frame index
        startInst.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if startInst.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    # *mouse* updates
    if t >= 0.0 and mouse.status == NOT_STARTED:
        # keep track of start time/frame for later
        mouse.tStart = t
        mouse.frameNStart = frameN  # exact frame index
        mouse.status = STARTED
        prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
    if mouse.status == STARTED:  # only update if started and not stopped!
        buttons = mouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # abort routine on response
                continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# store data for thisExp (ExperimentHandler)
thisExp.nextEntry()
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
practiceTrials = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('srttConditions.xlsx', selection='0:8'),
    seed=None, name='practiceTrials')
thisExp.addLoop(practiceTrials)  # add the loop to the experiment
thisPracticeTrial = practiceTrials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPracticeTrial.rgb)
if thisPracticeTrial != None:
    for paramName in thisPracticeTrial:
        exec('{} = thisPracticeTrial[paramName]'.format(paramName))

for thisPracticeTrial in practiceTrials:
    currentLoop = practiceTrials
    # abbreviate parameter names if possible (e.g. rgb = thisPracticeTrial.rgb)
    if thisPracticeTrial != None:
        for paramName in thisPracticeTrial:
            exec('{} = thisPracticeTrial[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "main"-------
    t = 0
    mainClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    response = event.BuilderKeyResponse()
    # setup some python lists for storing info about the mouseResp
    mouseResp.clicked_name = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    mainComponents = [bgMain, targ, response, mouseResp]
    for thisComponent in mainComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "main"-------
    while continueRoutine:
        # get current time
        t = mainClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *bgMain* updates
        if t >= 0 and bgMain.status == NOT_STARTED:
            # keep track of start time/frame for later
            bgMain.tStart = t
            bgMain.frameNStart = frameN  # exact frame index
            bgMain.setAutoDraw(True)
        
        # *targ* updates
        if t >= isi and targ.status == NOT_STARTED:
            # keep track of start time/frame for later
            targ.tStart = t
            targ.frameNStart = frameN  # exact frame index
            targ.setAutoDraw(True)
        
        # *response* updates
        if t >= isi and response.status == NOT_STARTED:
            # keep track of start time/frame for later
            response.tStart = t
            response.frameNStart = frameN  # exact frame index
            response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(response.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if response.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                if response.keys == []:  # then this was the first keypress
                    response.keys = theseKeys[0]  # just the first key pressed
                    response.rt = response.clock.getTime()
                    # was this 'correct'?
                    if (response.keys == str('space')) or (response.keys == 'space'):
                        response.corr = 1
                    else:
                        response.corr = 0
                    # a response ends the routine
                    continueRoutine = False
        # *mouseResp* updates
        if t >= isi and mouseResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouseResp.tStart = t
            mouseResp.frameNStart = frameN  # exact frame index
            mouseResp.status = STARTED
            mouseResp.mouseClock.reset()
            prevButtonState = mouseResp.getPressed()  # if button is down already this ISN'T a new click
        if mouseResp.status == STARTED:  # only update if started and not stopped!
            buttons = mouseResp.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False;
                    for obj in [targ]:
                        if obj.contains(mouseResp):
                            gotValidClick = True
                            mouseResp.clicked_name.append(obj.name)
                    if gotValidClick:  # abort routine on response
                        continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in mainComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "main"-------
    for thisComponent in mainComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if response.keys in ['', [], None]:  # No response was made
        response.keys=None
        # was no response the correct answer?!
        if str('space').lower() == 'none':
           response.corr = 1;  # correct non-response
        else:
           response.corr = 0;  # failed to respond (incorrectly)
    # store data for practiceTrials (TrialHandler)
    practiceTrials.addData('response.keys',response.keys)
    practiceTrials.addData('response.corr', response.corr)
    if response.keys != None:  # we had a response
        practiceTrials.addData('response.rt', response.rt)
    # store data for practiceTrials (TrialHandler)
    x, y = mouseResp.getPos()
    buttons = mouseResp.getPressed()
    mouseResp.time = mouseResp.mouseClock.getTime()
    if sum(buttons):
        # check if the mouse was inside our 'clickable' objects
        gotValidClick = False;
        for obj in [targ]:
            if obj.contains(mouseResp):
                gotValidClick = True
                mouseResp.clicked_name.append(obj.name)
    practiceTrials.addData('mouseResp.x', x)
    practiceTrials.addData('mouseResp.y', y)
    practiceTrials.addData('mouseResp.leftButton', buttons[0])
    practiceTrials.addData('mouseResp.midButton', buttons[1])
    practiceTrials.addData('mouseResp.rightButton', buttons[2])
    practiceTrials.addData('mouseResp.time', mouseResp.time)
    if len(mouseResp.clicked_name):
        practiceTrials.addData('mouseResp.clicked_name', mouseResp.clicked_name[0])
    # the Routine "main" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'practiceTrials'


# ------Prepare to start Routine "startTask"-------
t = 0
startTaskClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
go = event.BuilderKeyResponse()
# setup some python lists for storing info about the mouseGo
gotValidClick = False  # until a click is received
# keep track of which components have finished
startTaskComponents = [ready, go, mouseGo]
for thisComponent in startTaskComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "startTask"-------
while continueRoutine:
    # get current time
    t = startTaskClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *ready* updates
    if t >= 0.0 and ready.status == NOT_STARTED:
        # keep track of start time/frame for later
        ready.tStart = t
        ready.frameNStart = frameN  # exact frame index
        ready.setAutoDraw(True)
    
    # *go* updates
    if t >= 0.0 and go.status == NOT_STARTED:
        # keep track of start time/frame for later
        go.tStart = t
        go.frameNStart = frameN  # exact frame index
        go.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if go.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    # *mouseGo* updates
    if t >= 0.0 and mouseGo.status == NOT_STARTED:
        # keep track of start time/frame for later
        mouseGo.tStart = t
        mouseGo.frameNStart = frameN  # exact frame index
        mouseGo.status = STARTED
        mouseGo.mouseClock.reset()
        prevButtonState = mouseGo.getPressed()  # if button is down already this ISN'T a new click
    if mouseGo.status == STARTED:  # only update if started and not stopped!
        buttons = mouseGo.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # abort routine on response
                continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in startTaskComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "startTask"-------
for thisComponent in startTaskComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# store data for thisExp (ExperimentHandler)
thisExp.nextEntry()
# the Routine "startTask" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
mainTrials = data.TrialHandler(nReps=2, method='fullRandom', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('srttConditions.xlsx'),
    seed=None, name='mainTrials')
thisExp.addLoop(mainTrials)  # add the loop to the experiment
thisMainTrial = mainTrials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisMainTrial.rgb)
if thisMainTrial != None:
    for paramName in thisMainTrial:
        exec('{} = thisMainTrial[paramName]'.format(paramName))

for thisMainTrial in mainTrials:
    currentLoop = mainTrials
    # abbreviate parameter names if possible (e.g. rgb = thisMainTrial.rgb)
    if thisMainTrial != None:
        for paramName in thisMainTrial:
            exec('{} = thisMainTrial[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "main"-------
    t = 0
    mainClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    response = event.BuilderKeyResponse()
    # setup some python lists for storing info about the mouseResp
    mouseResp.clicked_name = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    mainComponents = [bgMain, targ, response, mouseResp]
    for thisComponent in mainComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "main"-------
    while continueRoutine:
        # get current time
        t = mainClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *bgMain* updates
        if t >= 0 and bgMain.status == NOT_STARTED:
            # keep track of start time/frame for later
            bgMain.tStart = t
            bgMain.frameNStart = frameN  # exact frame index
            bgMain.setAutoDraw(True)
        
        # *targ* updates
        if t >= isi and targ.status == NOT_STARTED:
            # keep track of start time/frame for later
            targ.tStart = t
            targ.frameNStart = frameN  # exact frame index
            targ.setAutoDraw(True)
        
        # *response* updates
        if t >= isi and response.status == NOT_STARTED:
            # keep track of start time/frame for later
            response.tStart = t
            response.frameNStart = frameN  # exact frame index
            response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(response.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if response.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                if response.keys == []:  # then this was the first keypress
                    response.keys = theseKeys[0]  # just the first key pressed
                    response.rt = response.clock.getTime()
                    # was this 'correct'?
                    if (response.keys == str('space')) or (response.keys == 'space'):
                        response.corr = 1
                    else:
                        response.corr = 0
                    # a response ends the routine
                    continueRoutine = False
        # *mouseResp* updates
        if t >= isi and mouseResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouseResp.tStart = t
            mouseResp.frameNStart = frameN  # exact frame index
            mouseResp.status = STARTED
            mouseResp.mouseClock.reset()
            prevButtonState = mouseResp.getPressed()  # if button is down already this ISN'T a new click
        if mouseResp.status == STARTED:  # only update if started and not stopped!
            buttons = mouseResp.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False;
                    for obj in [targ]:
                        if obj.contains(mouseResp):
                            gotValidClick = True
                            mouseResp.clicked_name.append(obj.name)
                    if gotValidClick:  # abort routine on response
                        continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in mainComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "main"-------
    for thisComponent in mainComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if response.keys in ['', [], None]:  # No response was made
        response.keys=None
        # was no response the correct answer?!
        if str('space').lower() == 'none':
           response.corr = 1;  # correct non-response
        else:
           response.corr = 0;  # failed to respond (incorrectly)
    # store data for mainTrials (TrialHandler)
    mainTrials.addData('response.keys',response.keys)
    mainTrials.addData('response.corr', response.corr)
    if response.keys != None:  # we had a response
        mainTrials.addData('response.rt', response.rt)
    # store data for mainTrials (TrialHandler)
    x, y = mouseResp.getPos()
    buttons = mouseResp.getPressed()
    mouseResp.time = mouseResp.mouseClock.getTime()
    if sum(buttons):
        # check if the mouse was inside our 'clickable' objects
        gotValidClick = False;
        for obj in [targ]:
            if obj.contains(mouseResp):
                gotValidClick = True
                mouseResp.clicked_name.append(obj.name)
    mainTrials.addData('mouseResp.x', x)
    mainTrials.addData('mouseResp.y', y)
    mainTrials.addData('mouseResp.leftButton', buttons[0])
    mainTrials.addData('mouseResp.midButton', buttons[1])
    mainTrials.addData('mouseResp.rightButton', buttons[2])
    mainTrials.addData('mouseResp.time', mouseResp.time)
    if len(mouseResp.clicked_name):
        mainTrials.addData('mouseResp.clicked_name', mouseResp.clicked_name[0])
    # the Routine "main" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 2 repeats of 'mainTrials'


# ------Prepare to start Routine "thanks"-------
t = 0
thanksClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(3.000000)
# update component parameters for each repeat
# keep track of which components have finished
thanksComponents = [thanksText]
for thisComponent in thanksComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "thanks"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = thanksClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *thanksText* updates
    if t >= 0.0 and thanksText.status == NOT_STARTED:
        # keep track of start time/frame for later
        thanksText.tStart = t
        thanksText.frameNStart = frameN  # exact frame index
        thanksText.setAutoDraw(True)
    frameRemains = 0.0 + 3- win.monitorFramePeriod * 0.75  # most of one frame period left
    if thanksText.status == STARTED and t >= frameRemains:
        thanksText.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in thanksComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "thanks"-------
for thisComponent in thanksComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
