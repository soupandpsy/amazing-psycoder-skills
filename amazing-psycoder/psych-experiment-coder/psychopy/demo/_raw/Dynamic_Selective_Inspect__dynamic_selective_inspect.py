# Source: Dynamic Selective Inspect (demos/Dynamic_Selective_Inspect)
# Project URL: https://gitlab.pavlovia.org/demos/Dynamic_Selective_Inspect
# Original file: dynamic_selective_inspect.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.0.0alpha3),
    on August 29, 2018, at 16:34
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
expName = 'inspect_images'  # from the Builder filename that created this script
expInfo = {'session': '001', 'participant': ''}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\lpzdb\\pavloviaDemos\\dynamicInsp\\dynamic_selective_inspect.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[2560, 1440], fullscr=True, screen=0,
    allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "instruct"
instructClock = core.Clock()
instructFirst = visual.TextStim(win=win, name='instructFirst',
    text='On each trial you have to search the screen to find the ball\n(by moving the mouse around)\n\nClick the mouse to get started',
    font='Arial',
    units='height', pos=(0, 0.3), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
finishInstruct = event.Mouse(win=win)
x, y = [None, None]
finishInstruct.mouseClock = core.Clock()

# Initialize components for Routine "trial"
trialClock = core.Clock()
imageStimulus = visual.ImageStim(
    win=win, name='imageStimulus',units='norm', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2, 2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
imageAperture = visual.ImageStim(
    win=win, name='imageAperture',units='height', 
    image='images/plainWhite.png', mask='images/circleMask.png',
    ori=0, pos=[0,0], size=(4, 4),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=True, depth=-1.0)
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Initialize components for Routine "explanation"
explanationClock = core.Clock()
instruct2 = visual.TextStim(win=win, name='instruct2',
    text='This is essentially the same thing but\nthe mask is now smaller ( w,h = 2,2 in height units) so you can see \nwhat was happening.',
    font='Arial',
    units='height', pos=(0, 0.3), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
explanationFinish = event.Mouse(win=win)
x, y = [None, None]
explanationFinish.mouseClock = core.Clock()

# Initialize components for Routine "showMeHow"
showMeHowClock = core.Clock()
imageStimulus_2 = visual.ImageStim(
    win=win, name='imageStimulus_2',units='norm', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2, 2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
imageAperture_2 = visual.ImageStim(
    win=win, name='imageAperture_2',units='height', 
    image='images/plainWhite.png', mask='images/circleMask.png',
    ori=0, pos=[0,0], size=(1,1),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=True, depth=-1.0)
mouse_2 = event.Mouse(win=win)
x, y = [None, None]
mouse_2.mouseClock = core.Clock()

# Initialize components for Routine "thanks"
thanksClock = core.Clock()
text = visual.TextStim(win=win, name='text',
    text="That's all there is to it.\n\nBye!",
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "instruct"-------
t = 0
instructClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the finishInstruct
gotValidClick = False  # until a click is received
# keep track of which components have finished
instructComponents = [instructFirst, finishInstruct]
for thisComponent in instructComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instruct"-------
while continueRoutine:
    # get current time
    t = instructClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instructFirst* updates
    if t >= 0.0 and instructFirst.status == NOT_STARTED:
        # keep track of start time/frame for later
        instructFirst.tStart = t
        instructFirst.frameNStart = frameN  # exact frame index
        instructFirst.setAutoDraw(True)
    # *finishInstruct* updates
    if t >= 0.0 and finishInstruct.status == NOT_STARTED:
        # keep track of start time/frame for later
        finishInstruct.tStart = t
        finishInstruct.frameNStart = frameN  # exact frame index
        finishInstruct.status = STARTED
        finishInstruct.mouseClock.reset()
        prevButtonState = finishInstruct.getPressed()  # if button is down already this ISN'T a new click
    if finishInstruct.status == STARTED:  # only update if started and not stopped!
        buttons = finishInstruct.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # abort routine on response
                continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instruct"-------
for thisComponent in instructComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# store data for thisExp (ExperimentHandler)
thisExp.nextEntry()
# the Routine "instruct" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('conditions.xlsx'),
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
    
    # ------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    imageStimulus.setImage(imageFile)
    # setup some python lists for storing info about the mouse
    gotValidClick = False  # until a click is received
    mouse.mouseClock.reset()
    # keep track of which components have finished
    trialComponents = [imageStimulus, imageAperture, mouse]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *imageStimulus* updates
        if t >= 0.0 and imageStimulus.status == NOT_STARTED:
            # keep track of start time/frame for later
            imageStimulus.tStart = t
            imageStimulus.frameNStart = frameN  # exact frame index
            imageStimulus.setAutoDraw(True)
        
        # *imageAperture* updates
        if t >= 0.0 and imageAperture.status == NOT_STARTED:
            # keep track of start time/frame for later
            imageAperture.tStart = t
            imageAperture.frameNStart = frameN  # exact frame index
            imageAperture.setAutoDraw(True)
        if imageAperture.status == STARTED:  # only update if drawing
            imageAperture.setPos(mouse.getPos(), log=False)
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
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for trials (TrialHandler)
    x, y = mouse.getPos()
    buttons = mouse.getPressed()
    mouse.time = mouse.mouseClock.getTime()
    trials.addData('mouse.x', x)
    trials.addData('mouse.y', y)
    trials.addData('mouse.leftButton', buttons[0])
    trials.addData('mouse.midButton', buttons[1])
    trials.addData('mouse.rightButton', buttons[2])
    trials.addData('mouse.time', mouse.time)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'trials'


# ------Prepare to start Routine "explanation"-------
t = 0
explanationClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the explanationFinish
gotValidClick = False  # until a click is received
# keep track of which components have finished
explanationComponents = [instruct2, explanationFinish]
for thisComponent in explanationComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "explanation"-------
while continueRoutine:
    # get current time
    t = explanationClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instruct2* updates
    if t >= 0.0 and instruct2.status == NOT_STARTED:
        # keep track of start time/frame for later
        instruct2.tStart = t
        instruct2.frameNStart = frameN  # exact frame index
        instruct2.setAutoDraw(True)
    # *explanationFinish* updates
    if t >= 0.0 and explanationFinish.status == NOT_STARTED:
        # keep track of start time/frame for later
        explanationFinish.tStart = t
        explanationFinish.frameNStart = frameN  # exact frame index
        explanationFinish.status = STARTED
        explanationFinish.mouseClock.reset()
        prevButtonState = explanationFinish.getPressed()  # if button is down already this ISN'T a new click
    if explanationFinish.status == STARTED:  # only update if started and not stopped!
        buttons = explanationFinish.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # abort routine on response
                continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in explanationComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "explanation"-------
for thisComponent in explanationComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# store data for thisExp (ExperimentHandler)
thisExp.nextEntry()
# the Routine "explanation" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
showMeTrials = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('conditions.xlsx'),
    seed=None, name='showMeTrials')
thisExp.addLoop(showMeTrials)  # add the loop to the experiment
thisShowMeTrial = showMeTrials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisShowMeTrial.rgb)
if thisShowMeTrial != None:
    for paramName in thisShowMeTrial:
        exec('{} = thisShowMeTrial[paramName]'.format(paramName))

for thisShowMeTrial in showMeTrials:
    currentLoop = showMeTrials
    # abbreviate parameter names if possible (e.g. rgb = thisShowMeTrial.rgb)
    if thisShowMeTrial != None:
        for paramName in thisShowMeTrial:
            exec('{} = thisShowMeTrial[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "showMeHow"-------
    t = 0
    showMeHowClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    imageStimulus_2.setImage(imageFile)
    # setup some python lists for storing info about the mouse_2
    mouse_2.x = []
    mouse_2.y = []
    mouse_2.leftButton = []
    mouse_2.midButton = []
    mouse_2.rightButton = []
    mouse_2.time = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    showMeHowComponents = [imageStimulus_2, imageAperture_2, mouse_2]
    for thisComponent in showMeHowComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "showMeHow"-------
    while continueRoutine:
        # get current time
        t = showMeHowClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *imageStimulus_2* updates
        if t >= 0.0 and imageStimulus_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            imageStimulus_2.tStart = t
            imageStimulus_2.frameNStart = frameN  # exact frame index
            imageStimulus_2.setAutoDraw(True)
        
        # *imageAperture_2* updates
        if t >= 0.0 and imageAperture_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            imageAperture_2.tStart = t
            imageAperture_2.frameNStart = frameN  # exact frame index
            imageAperture_2.setAutoDraw(True)
        if imageAperture_2.status == STARTED:  # only update if drawing
            imageAperture_2.setPos(mouse.getPos(), log=False)
        # *mouse_2* updates
        if t >= 0.0 and mouse_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouse_2.tStart = t
            mouse_2.frameNStart = frameN  # exact frame index
            mouse_2.status = STARTED
            mouse_2.mouseClock.reset()
            prevButtonState = mouse_2.getPressed()  # if button is down already this ISN'T a new click
        if mouse_2.status == STARTED:  # only update if started and not stopped!
            buttons = mouse_2.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    x, y = mouse_2.getPos()
                    mouse_2.x.append(x)
                    mouse_2.y.append(y)
                    mouse_2.leftButton.append(buttons[0])
                    mouse_2.midButton.append(buttons[1])
                    mouse_2.rightButton.append(buttons[2])
                    mouse_2.time.append(mouse_2.mouseClock.getTime())
                    # abort routine on response
                    continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in showMeHowComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "showMeHow"-------
    for thisComponent in showMeHowComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for showMeTrials (TrialHandler)
    if len(mouse_2.x): showMeTrials.addData('mouse_2.x', mouse_2.x[0])
    if len(mouse_2.y): showMeTrials.addData('mouse_2.y', mouse_2.y[0])
    if len(mouse_2.leftButton): showMeTrials.addData('mouse_2.leftButton', mouse_2.leftButton[0])
    if len(mouse_2.midButton): showMeTrials.addData('mouse_2.midButton', mouse_2.midButton[0])
    if len(mouse_2.rightButton): showMeTrials.addData('mouse_2.rightButton', mouse_2.rightButton[0])
    if len(mouse_2.time): showMeTrials.addData('mouse_2.time', mouse_2.time[0])
    # the Routine "showMeHow" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'showMeTrials'


# ------Prepare to start Routine "thanks"-------
t = 0
thanksClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(1.000000)
# update component parameters for each repeat
# keep track of which components have finished
thanksComponents = [text]
for thisComponent in thanksComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "thanks"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = thanksClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text* updates
    if t >= 0.0 and text.status == NOT_STARTED:
        # keep track of start time/frame for later
        text.tStart = t
        text.frameNStart = frameN  # exact frame index
        text.setAutoDraw(True)
    frameRemains = 0.0 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
    if text.status == STARTED and t >= frameRemains:
        text.setAutoDraw(False)
    
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
