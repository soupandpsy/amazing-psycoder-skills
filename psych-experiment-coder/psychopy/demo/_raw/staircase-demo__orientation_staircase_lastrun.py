# Source: staircase-demo (demos/staircase-demo)
# Project URL: https://gitlab.pavlovia.org/demos/staircase-demo
# Original file: orientation_staircase_lastrun.py
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2020.2.8),
    on November 27, 2020, at 15:55
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2020.2.8'
expName = 'orientation_staircase'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001', 'startOri': ['left', 'right']}
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
    originPath='C:\\Users\\44797\\OneDrive - Open Science Tools\\Research\\EPIC\\tasks\\staircase\\orientation_staircase_lastrun.py',
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
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
instrTxt = visual.TextStim(win=win, name='instrTxt',
    text='This is a demo of a basic orientation discrimination staricase. \n\nPress left or right to identify the 0 degree probe\n\npress space to start',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
start_resp = keyboard.Keyboard()

# Initialize components for Routine "trial"
trialClock = core.Clock()
'''
stair params similar to stairhandler class
but simplified for basic online task
'''
# trials.N not supported in psychoJS - add manual counter
trialCount = 0

# starting orientation
startVal=70

# parameters used in stairhandler

nReversals=5 #number of reversals 
stepSizes=[10, 5, 2, 1, 0.5] #size of steps (will move to next on each reversal)
nTrials = 100 #max number of trials
nUp = 1 #number of incorrect responses before increase
nDown = 1 #number of correct responses before decrease
maxVal = 90 #maximum orientation
minVal = 0 #minimum orientation
currentDirection = 'down' #direction of steps
reversalVals =[]#track reversal values

leftGrating = visual.ImageStim(
    win=win,
    name='leftGrating', 
    image='Stimuli/grating_cropped.png', mask=None,
    ori=1.0, pos=(-.3, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
rightGrating = visual.ImageStim(
    win=win,
    name='rightGrating', 
    image='Stimuli/grating_cropped.png', mask=None,
    ori=1.0, pos=(0.3, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
key_resp = keyboard.Keyboard()
incrementText = visual.TextStim(win=win, name='incrementText',
    text='default text',
    font='Arial',
    pos=(0, -.4), height=0.02, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-5.0);
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.02, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-6.0);

# Initialize components for Routine "end"
endClock = core.Clock()
feedbackTxt = visual.TextStim(win=win, name='feedbackTxt',
    text='default text',
    font='Arial',
    pos=(0, 0.4), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
orientedGrating = visual.ImageStim(
    win=win,
    name='orientedGrating', 
    image='Stimuli/grating_cropped.png', mask=None,
    ori=1.0, pos=(0, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
threshGratingText = visual.TextStim(win=win, name='threshGratingText',
    text='That looks like this!',
    font='Arial',
    pos=(0, -.2), height=0.02, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-3.0);
endButton = visual.TextStim(win=win, name='endButton',
    text='click here to end',
    font='Arial',
    pos=(.4, -.4), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-4.0);
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "instructions"-------
continueRoutine = True
# update component parameters for each repeat
start_resp.keys = []
start_resp.rt = []
_start_resp_allKeys = []
# keep track of which components have finished
instructionsComponents = [instrTxt, start_resp]
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
    
    # *instrTxt* updates
    if instrTxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instrTxt.frameNStart = frameN  # exact frame index
        instrTxt.tStart = t  # local t and not account for scr refresh
        instrTxt.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instrTxt, 'tStartRefresh')  # time at next scr refresh
        instrTxt.setAutoDraw(True)
    
    # *start_resp* updates
    waitOnFlip = False
    if start_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_resp.frameNStart = frameN  # exact frame index
        start_resp.tStart = t  # local t and not account for scr refresh
        start_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_resp, 'tStartRefresh')  # time at next scr refresh
        start_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(start_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(start_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if start_resp.status == STARTED and not waitOnFlip:
        theseKeys = start_resp.getKeys(keyList=['space'], waitRelease=False)
        _start_resp_allKeys.extend(theseKeys)
        if len(_start_resp_allKeys):
            start_resp.keys = _start_resp_allKeys[-1].name  # just the last key pressed
            start_resp.rt = _start_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
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
thisExp.addData('instrTxt.started', instrTxt.tStartRefresh)
thisExp.addData('instrTxt.stopped', instrTxt.tStopRefresh)
# check responses
if start_resp.keys in ['', [], None]:  # No response was made
    start_resp.keys = None
thisExp.addData('start_resp.keys',start_resp.keys)
if start_resp.keys != None:  # we had a response
    thisExp.addData('start_resp.rt', start_resp.rt)
thisExp.addData('start_resp.started', start_resp.tStartRefresh)
thisExp.addData('start_resp.stopped', start_resp.tStopRefresh)
thisExp.nextEntry()
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=nTrials, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
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
    continueRoutine = True
    # update component parameters for each repeat
    '''Because the grating stim class is not currently supported in PsychoJS
    this demo uses an image. We set a mask to avoid black image borders locally. 
    '''
    leftGrating.mask = 'gauss'
    rightGrating.mask = 'gauss'
    orientedGrating.mask = 'gauss'
    #  set starting val and stepsize
    if trialCount ==0:
        this_ori = startVal
        thisStep = 0
    
    #select current stepsize from the list
    stepSize = stepSizes[thisStep]
    
    #if we want our oriented grating to be leftward *-1
    if expInfo['startOri']=='left':
        this_ori = this_ori * -1
    
    #shuffle if the probe is presented on the left or the right
    these_oris = [this_ori, 0]
    shuffle(these_oris)
    
    #  correct answer is..
    if these_oris[1] ==0:
        corrAns = 'right'
    elif these_oris[0] ==0:
        corrAns = 'left'
    
    leftGrating.setOri(these_oris[0])
    rightGrating.setOri(these_oris[1])
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    incrementText.setText('(for debugging/teaching only) current stepSize is: '+str(stepSize))
    # keep track of which components have finished
    trialComponents = [leftGrating, rightGrating, key_resp, incrementText, fixation]
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
        
        # *leftGrating* updates
        if leftGrating.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            leftGrating.frameNStart = frameN  # exact frame index
            leftGrating.tStart = t  # local t and not account for scr refresh
            leftGrating.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(leftGrating, 'tStartRefresh')  # time at next scr refresh
            leftGrating.setAutoDraw(True)
        if leftGrating.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > leftGrating.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                leftGrating.tStop = t  # not accounting for scr refresh
                leftGrating.frameNStop = frameN  # exact frame index
                win.timeOnFlip(leftGrating, 'tStopRefresh')  # time at next scr refresh
                leftGrating.setAutoDraw(False)
        
        # *rightGrating* updates
        if rightGrating.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            rightGrating.frameNStart = frameN  # exact frame index
            rightGrating.tStart = t  # local t and not account for scr refresh
            rightGrating.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(rightGrating, 'tStartRefresh')  # time at next scr refresh
            rightGrating.setAutoDraw(True)
        if rightGrating.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > rightGrating.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                rightGrating.tStop = t  # not accounting for scr refresh
                rightGrating.frameNStop = frameN  # exact frame index
                win.timeOnFlip(rightGrating, 'tStopRefresh')  # time at next scr refresh
                rightGrating.setAutoDraw(False)
        
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
            theseKeys = key_resp.getKeys(keyList=['left', 'right'], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                # was this correct?
                if (key_resp.keys == str('corrAns')) or (key_resp.keys == 'corrAns'):
                    key_resp.corr = 1
                else:
                    key_resp.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # *incrementText* updates
        if incrementText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            incrementText.frameNStart = frameN  # exact frame index
            incrementText.tStart = t  # local t and not account for scr refresh
            incrementText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(incrementText, 'tStartRefresh')  # time at next scr refresh
            incrementText.setAutoDraw(True)
        
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
            if tThisFlipGlobal > fixation.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                fixation.tStop = t  # not accounting for scr refresh
                fixation.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fixation, 'tStopRefresh')  # time at next scr refresh
                fixation.setAutoDraw(False)
        
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
    # print useful information for the experimenter
    print('Orientation was: ', this_ori)
    print('Correct answer was: ', corrAns)
    print('This resp was: ', key_resp.keys)
    
    # save information to output file 
    trials.addData('this_ori', this_ori)
    trials.addData('Response', key_resp.keys)
    trials.addData('currentDirection', currentDirection)
    trials.addData('corrAns', corrAns)
    trials.addData('currentStepSize', thisStep)
    
    #if oriented grating is leftward convert back to positive before applying stepsize
    if expInfo['startOri']=='left':
       this_ori = this_ori * -1
    
    # check if correct, adjust orientation and add to reversal vals (if needed)
    if key_resp.keys == corrAns:
        print('Answer correct!')
        trials.addData('corr', 1)
        if currentDirection == 'down':
            if this_ori > minVal:
                this_ori -=stepSize
            else:
                print('minimal value reached maintaining current val')
        else:
            currentDirection = 'down'
            reversalVals.append(this_ori)
            if stepSize != stepSizes[-1]:#if this is not the minimal stepsize
                thisStep +=1
    else:
        trials.addData('corr', 0)
        if currentDirection == 'down':
            currentDirection = 'up'
            reversalVals.append(this_ori)
            if stepSize != stepSizes[-1]:#if this is not the minimal stepsize
                thisStep +=1
        if this_ori < maxVal:
            this_ori +=stepSize
        else:
            print('max value reached. keeping current value')
    
    #if we have reached our max reversals end the loop
    #(if we reach nTrials the loop will end anyway)
    if len(reversalVals) == nReversals:
        continueRoutine = False
        trials.finished = True
        print('nReversals reached, ending staircase')
    
    trialCount +=1
    trials.addData('leftGrating.started', leftGrating.tStartRefresh)
    trials.addData('leftGrating.stopped', leftGrating.tStopRefresh)
    trials.addData('rightGrating.started', rightGrating.tStartRefresh)
    trials.addData('rightGrating.stopped', rightGrating.tStopRefresh)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
        # was no response the correct answer?!
        if str('corrAns').lower() == 'none':
           key_resp.corr = 1;  # correct non-response
        else:
           key_resp.corr = 0;  # failed to respond (incorrectly)
    # store data for trials (TrialHandler)
    trials.addData('key_resp.keys',key_resp.keys)
    trials.addData('key_resp.corr', key_resp.corr)
    if key_resp.keys != None:  # we had a response
        trials.addData('key_resp.rt', key_resp.rt)
    trials.addData('key_resp.started', key_resp.tStartRefresh)
    trials.addData('key_resp.stopped', key_resp.tStopRefresh)
    trials.addData('incrementText.started', incrementText.tStartRefresh)
    trials.addData('incrementText.stopped', incrementText.tStopRefresh)
    trials.addData('fixation.started', fixation.tStartRefresh)
    trials.addData('fixation.stopped', fixation.tStopRefresh)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed nTrials repeats of 'trials'


# ------Prepare to start Routine "end"-------
continueRoutine = True
# update component parameters for each repeat
# how many of the final reversals do we want to average to get the threshold?
avRevs=3
#calculate threshold
threshold = np.average(reversalVals[-avRevs:])
print('Threshold was: ', threshold)
feedbackTxt.setText('Your threshold was '+str(round(threshold, 3)) +' degrees!')
orientedGrating.setOri(threshold)
# setup some python lists for storing info about the mouse
mouse.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
endComponents = [feedbackTxt, orientedGrating, threshGratingText, endButton, mouse]
for thisComponent in endComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "end"-------
while continueRoutine:
    # get current time
    t = endClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=endClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *feedbackTxt* updates
    if feedbackTxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        feedbackTxt.frameNStart = frameN  # exact frame index
        feedbackTxt.tStart = t  # local t and not account for scr refresh
        feedbackTxt.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(feedbackTxt, 'tStartRefresh')  # time at next scr refresh
        feedbackTxt.setAutoDraw(True)
    
    # *orientedGrating* updates
    if orientedGrating.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        orientedGrating.frameNStart = frameN  # exact frame index
        orientedGrating.tStart = t  # local t and not account for scr refresh
        orientedGrating.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(orientedGrating, 'tStartRefresh')  # time at next scr refresh
        orientedGrating.setAutoDraw(True)
    
    # *threshGratingText* updates
    if threshGratingText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        threshGratingText.frameNStart = frameN  # exact frame index
        threshGratingText.tStart = t  # local t and not account for scr refresh
        threshGratingText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(threshGratingText, 'tStartRefresh')  # time at next scr refresh
        threshGratingText.setAutoDraw(True)
    
    # *endButton* updates
    if endButton.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        endButton.frameNStart = frameN  # exact frame index
        endButton.tStart = t  # local t and not account for scr refresh
        endButton.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(endButton, 'tStartRefresh')  # time at next scr refresh
        endButton.setAutoDraw(True)
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
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                for obj in [endButton]:
                    if obj.contains(mouse):
                        gotValidClick = True
                        mouse.clicked_name.append(obj.name)
                if gotValidClick:  # abort routine on response
                    continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('feedbackTxt.started', feedbackTxt.tStartRefresh)
thisExp.addData('feedbackTxt.stopped', feedbackTxt.tStopRefresh)
thisExp.addData('orientedGrating.started', orientedGrating.tStartRefresh)
thisExp.addData('orientedGrating.stopped', orientedGrating.tStopRefresh)
thisExp.addData('threshGratingText.started', threshGratingText.tStartRefresh)
thisExp.addData('threshGratingText.stopped', threshGratingText.tStopRefresh)
thisExp.addData('endButton.started', endButton.tStartRefresh)
thisExp.addData('endButton.stopped', endButton.tStopRefresh)
# store data for thisExp (ExperimentHandler)
x, y = mouse.getPos()
buttons = mouse.getPressed()
if sum(buttons):
    # check if the mouse was inside our 'clickable' objects
    gotValidClick = False
    for obj in [endButton]:
        if obj.contains(mouse):
            gotValidClick = True
            mouse.clicked_name.append(obj.name)
thisExp.addData('mouse.x', x)
thisExp.addData('mouse.y', y)
thisExp.addData('mouse.leftButton', buttons[0])
thisExp.addData('mouse.midButton', buttons[1])
thisExp.addData('mouse.rightButton', buttons[2])
if len(mouse.clicked_name):
    thisExp.addData('mouse.clicked_name', mouse.clicked_name[0])
thisExp.addData('mouse.started', mouse.tStart)
thisExp.addData('mouse.stopped', mouse.tStop)
thisExp.nextEntry()
# the Routine "end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

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
