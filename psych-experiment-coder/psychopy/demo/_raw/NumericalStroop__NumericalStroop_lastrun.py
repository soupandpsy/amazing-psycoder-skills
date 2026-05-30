# Source: NumericalStroop (demos/NumericalStroop)
# Project URL: https://gitlab.pavlovia.org/demos/NumericalStroop
# Original file: NumericalStroop_lastrun.py
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.3),
    on July 13, 2023, at 11:02
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.tools import environmenttools
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
psychopyVersion = '2023.1.3'
expName = 'NumericalStroop'  # from the Builder filename that created this script
expInfo = {
    'participant': '',
    'session': '001',
}
# --- Show participant info dialog --
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
    originPath='C:\\Users\\suely\\OneDrive\\Desktop\\demos\\pavlovia demos\\numericalstroop\\NumericalStroop_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1280, 800], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    backgroundImage='', backgroundFit='none',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
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

# --- Initialize components for Routine "BlockInstruct" ---
BlockInstrText = visual.TextStim(win=win, name='BlockInstrText',
    text='',
    font='Arial',
    pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
Key_resp_2 = keyboard.Keyboard()

# --- Initialize components for Routine "Trial" ---
Fixation = visual.TextStim(win=win, name='Fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
NumberLeft = visual.TextStim(win=win, name='NumberLeft',
    text='',
    font='Arial',
    pos=(-0.075, 0), height=1.0, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
NumberRight = visual.TextStim(win=win, name='NumberRight',
    text='',
    font='Arial',
    pos=(0.075, 0), height=1.0, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
Response = keyboard.Keyboard()

# --- Initialize components for Routine "Feedback" ---
# Run 'Begin Experiment' code from Code
#msg variable just needs some value at start
msg='hello'
FeedbackMessage = visual.TextStim(win=win, name='FeedbackMessage',
    text='',
    font='Arial',
    pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# --- Initialize components for Routine "EndOfPractice" ---
Text = visual.TextStim(win=win, name='Text',
    text='This is the end of practice trials.\nPress the spacebar when ready to start the main trials',
    font='Arial',
    pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
Key_resp_3 = keyboard.Keyboard()

# --- Initialize components for Routine "Trial" ---
Fixation = visual.TextStim(win=win, name='Fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
NumberLeft = visual.TextStim(win=win, name='NumberLeft',
    text='',
    font='Arial',
    pos=(-0.075, 0), height=1.0, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
NumberRight = visual.TextStim(win=win, name='NumberRight',
    text='',
    font='Arial',
    pos=(0.075, 0), height=1.0, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
Response = keyboard.Keyboard()

# --- Initialize components for Routine "End" ---
Text5 = visual.TextStim(win=win, name='Text5',
    text='This is the end of the experiment.\nThank you for your participation!',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# set up handler to look after randomisation of conditions etc
blocks = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('blockDefinitions.xlsx'),
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
    
    # --- Prepare to start Routine "BlockInstruct" ---
    continueRoutine = True
    # update component parameters for each repeat
    BlockInstrText.setText(instructionText)
    Key_resp_2.keys = []
    Key_resp_2.rt = []
    _Key_resp_2_allKeys = []
    # keep track of which components have finished
    BlockInstructComponents = [BlockInstrText, Key_resp_2]
    for thisComponent in BlockInstructComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "BlockInstruct" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *BlockInstrText* updates
        
        # if BlockInstrText is starting this frame...
        if BlockInstrText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            BlockInstrText.frameNStart = frameN  # exact frame index
            BlockInstrText.tStart = t  # local t and not account for scr refresh
            BlockInstrText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(BlockInstrText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'BlockInstrText.started')
            # update status
            BlockInstrText.status = STARTED
            BlockInstrText.setAutoDraw(True)
        
        # if BlockInstrText is active this frame...
        if BlockInstrText.status == STARTED:
            # update params
            pass
        
        # *Key_resp_2* updates
        waitOnFlip = False
        
        # if Key_resp_2 is starting this frame...
        if Key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Key_resp_2.frameNStart = frameN  # exact frame index
            Key_resp_2.tStart = t  # local t and not account for scr refresh
            Key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Key_resp_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Key_resp_2.started')
            # update status
            Key_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(Key_resp_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(Key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if Key_resp_2.status == STARTED and not waitOnFlip:
            theseKeys = Key_resp_2.getKeys(keyList=['space'], waitRelease=False)
            _Key_resp_2_allKeys.extend(theseKeys)
            if len(_Key_resp_2_allKeys):
                Key_resp_2.keys = _Key_resp_2_allKeys[-1].name  # just the last key pressed
                Key_resp_2.rt = _Key_resp_2_allKeys[-1].rt
                Key_resp_2.duration = _Key_resp_2_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in BlockInstructComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "BlockInstruct" ---
    for thisComponent in BlockInstructComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if Key_resp_2.keys in ['', [], None]:  # No response was made
        Key_resp_2.keys = None
    blocks.addData('Key_resp_2.keys',Key_resp_2.keys)
    if Key_resp_2.keys != None:  # we had a response
        blocks.addData('Key_resp_2.rt', Key_resp_2.rt)
        blocks.addData('Key_resp_2.duration', Key_resp_2.duration)
    # the Routine "BlockInstruct" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    ftrials = data.TrialHandler(nReps=1, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(practiceFile),
        seed=None, name='ftrials')
    thisExp.addLoop(ftrials)  # add the loop to the experiment
    thisFtrial = ftrials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisFtrial.rgb)
    if thisFtrial != None:
        for paramName in thisFtrial:
            exec('{} = thisFtrial[paramName]'.format(paramName))
    
    for thisFtrial in ftrials:
        currentLoop = ftrials
        # abbreviate parameter names if possible (e.g. rgb = thisFtrial.rgb)
        if thisFtrial != None:
            for paramName in thisFtrial:
                exec('{} = thisFtrial[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "Trial" ---
        continueRoutine = True
        # update component parameters for each repeat
        NumberLeft.setText(number1)
        NumberLeft.setHeight(size1)
        NumberRight.setText(number2)
        NumberRight.setHeight(size2)
        Response.keys = []
        Response.rt = []
        _Response_allKeys = []
        # keep track of which components have finished
        TrialComponents = [Fixation, NumberLeft, NumberRight, Response]
        for thisComponent in TrialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Trial" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fixation* updates
            
            # if Fixation is starting this frame...
            if Fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fixation.frameNStart = frameN  # exact frame index
                Fixation.tStart = t  # local t and not account for scr refresh
                Fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fixation.started')
                # update status
                Fixation.status = STARTED
                Fixation.setAutoDraw(True)
            
            # if Fixation is active this frame...
            if Fixation.status == STARTED:
                # update params
                pass
            
            # if Fixation is stopping this frame...
            if Fixation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Fixation.tStartRefresh + 0.1-frameTolerance:
                    # keep track of stop time/frame for later
                    Fixation.tStop = t  # not accounting for scr refresh
                    Fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Fixation.stopped')
                    # update status
                    Fixation.status = FINISHED
                    Fixation.setAutoDraw(False)
            
            # *NumberLeft* updates
            
            # if NumberLeft is starting this frame...
            if NumberLeft.status == NOT_STARTED and tThisFlip >= 0.2-frameTolerance:
                # keep track of start time/frame for later
                NumberLeft.frameNStart = frameN  # exact frame index
                NumberLeft.tStart = t  # local t and not account for scr refresh
                NumberLeft.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(NumberLeft, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'NumberLeft.started')
                # update status
                NumberLeft.status = STARTED
                NumberLeft.setAutoDraw(True)
            
            # if NumberLeft is active this frame...
            if NumberLeft.status == STARTED:
                # update params
                pass
            
            # *NumberRight* updates
            
            # if NumberRight is starting this frame...
            if NumberRight.status == NOT_STARTED and tThisFlip >= 0.2-frameTolerance:
                # keep track of start time/frame for later
                NumberRight.frameNStart = frameN  # exact frame index
                NumberRight.tStart = t  # local t and not account for scr refresh
                NumberRight.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(NumberRight, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'NumberRight.started')
                # update status
                NumberRight.status = STARTED
                NumberRight.setAutoDraw(True)
            
            # if NumberRight is active this frame...
            if NumberRight.status == STARTED:
                # update params
                pass
            
            # *Response* updates
            waitOnFlip = False
            
            # if Response is starting this frame...
            if Response.status == NOT_STARTED and tThisFlip >= 0.2-frameTolerance:
                # keep track of start time/frame for later
                Response.frameNStart = frameN  # exact frame index
                Response.tStart = t  # local t and not account for scr refresh
                Response.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Response, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Response.started')
                # update status
                Response.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(Response.clock.reset)  # t=0 on next screen flip
            if Response.status == STARTED and not waitOnFlip:
                theseKeys = Response.getKeys(keyList=['a','k'], waitRelease=False)
                _Response_allKeys.extend(theseKeys)
                if len(_Response_allKeys):
                    Response.keys = _Response_allKeys[-1].name  # just the last key pressed
                    Response.rt = _Response_allKeys[-1].rt
                    Response.duration = _Response_allKeys[-1].duration
                    # was this correct?
                    if (Response.keys == str(corrAns)) or (Response.keys == corrAns):
                        Response.corr = 1
                    else:
                        Response.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in TrialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Trial" ---
        for thisComponent in TrialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if Response.keys in ['', [], None]:  # No response was made
            Response.keys = None
            # was no response the correct answer?!
            if str(corrAns).lower() == 'none':
               Response.corr = 1;  # correct non-response
            else:
               Response.corr = 0;  # failed to respond (incorrectly)
        # store data for ftrials (TrialHandler)
        ftrials.addData('Response.keys',Response.keys)
        ftrials.addData('Response.corr', Response.corr)
        if Response.keys != None:  # we had a response
            ftrials.addData('Response.rt', Response.rt)
            ftrials.addData('Response.duration', Response.duration)
        # the Routine "Trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "Feedback" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from Code
        if Response.corr:#stored on last run routine
          msg = "Correct!" 
        else:
          msg = "Oops! That was wrong"
        FeedbackMessage.setText(msg)
        # keep track of which components have finished
        FeedbackComponents = [FeedbackMessage]
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
        frameN = -1
        
        # --- Run Routine "Feedback" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *FeedbackMessage* updates
            
            # if FeedbackMessage is starting this frame...
            if FeedbackMessage.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                FeedbackMessage.frameNStart = frameN  # exact frame index
                FeedbackMessage.tStart = t  # local t and not account for scr refresh
                FeedbackMessage.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(FeedbackMessage, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'FeedbackMessage.started')
                # update status
                FeedbackMessage.status = STARTED
                FeedbackMessage.setAutoDraw(True)
            
            # if FeedbackMessage is active this frame...
            if FeedbackMessage.status == STARTED:
                # update params
                pass
            
            # if FeedbackMessage is stopping this frame...
            if FeedbackMessage.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > FeedbackMessage.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    FeedbackMessage.tStop = t  # not accounting for scr refresh
                    FeedbackMessage.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'FeedbackMessage.stopped')
                    # update status
                    FeedbackMessage.status = FINISHED
                    FeedbackMessage.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in FeedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Feedback" ---
        for thisComponent in FeedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        thisExp.nextEntry()
        
    # completed 1 repeats of 'ftrials'
    
    
    # --- Prepare to start Routine "EndOfPractice" ---
    continueRoutine = True
    # update component parameters for each repeat
    Key_resp_3.keys = []
    Key_resp_3.rt = []
    _Key_resp_3_allKeys = []
    # keep track of which components have finished
    EndOfPracticeComponents = [Text, Key_resp_3]
    for thisComponent in EndOfPracticeComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "EndOfPractice" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Text* updates
        
        # if Text is starting this frame...
        if Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text.frameNStart = frameN  # exact frame index
            Text.tStart = t  # local t and not account for scr refresh
            Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Text.started')
            # update status
            Text.status = STARTED
            Text.setAutoDraw(True)
        
        # if Text is active this frame...
        if Text.status == STARTED:
            # update params
            pass
        
        # *Key_resp_3* updates
        waitOnFlip = False
        
        # if Key_resp_3 is starting this frame...
        if Key_resp_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Key_resp_3.frameNStart = frameN  # exact frame index
            Key_resp_3.tStart = t  # local t and not account for scr refresh
            Key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Key_resp_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Key_resp_3.started')
            # update status
            Key_resp_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(Key_resp_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(Key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if Key_resp_3.status == STARTED and not waitOnFlip:
            theseKeys = Key_resp_3.getKeys(keyList=['space'], waitRelease=False)
            _Key_resp_3_allKeys.extend(theseKeys)
            if len(_Key_resp_3_allKeys):
                Key_resp_3.keys = _Key_resp_3_allKeys[-1].name  # just the last key pressed
                Key_resp_3.rt = _Key_resp_3_allKeys[-1].rt
                Key_resp_3.duration = _Key_resp_3_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in EndOfPracticeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "EndOfPractice" ---
    for thisComponent in EndOfPracticeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if Key_resp_3.keys in ['', [], None]:  # No response was made
        Key_resp_3.keys = None
    blocks.addData('Key_resp_3.keys',Key_resp_3.keys)
    if Key_resp_3.keys != None:  # we had a response
        blocks.addData('Key_resp_3.rt', Key_resp_3.rt)
        blocks.addData('Key_resp_3.duration', Key_resp_3.duration)
    # the Routine "EndOfPractice" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(conditionsFile),
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
        
        # --- Prepare to start Routine "Trial" ---
        continueRoutine = True
        # update component parameters for each repeat
        NumberLeft.setText(number1)
        NumberLeft.setHeight(size1)
        NumberRight.setText(number2)
        NumberRight.setHeight(size2)
        Response.keys = []
        Response.rt = []
        _Response_allKeys = []
        # keep track of which components have finished
        TrialComponents = [Fixation, NumberLeft, NumberRight, Response]
        for thisComponent in TrialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Trial" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fixation* updates
            
            # if Fixation is starting this frame...
            if Fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fixation.frameNStart = frameN  # exact frame index
                Fixation.tStart = t  # local t and not account for scr refresh
                Fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fixation.started')
                # update status
                Fixation.status = STARTED
                Fixation.setAutoDraw(True)
            
            # if Fixation is active this frame...
            if Fixation.status == STARTED:
                # update params
                pass
            
            # if Fixation is stopping this frame...
            if Fixation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Fixation.tStartRefresh + 0.1-frameTolerance:
                    # keep track of stop time/frame for later
                    Fixation.tStop = t  # not accounting for scr refresh
                    Fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Fixation.stopped')
                    # update status
                    Fixation.status = FINISHED
                    Fixation.setAutoDraw(False)
            
            # *NumberLeft* updates
            
            # if NumberLeft is starting this frame...
            if NumberLeft.status == NOT_STARTED and tThisFlip >= 0.2-frameTolerance:
                # keep track of start time/frame for later
                NumberLeft.frameNStart = frameN  # exact frame index
                NumberLeft.tStart = t  # local t and not account for scr refresh
                NumberLeft.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(NumberLeft, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'NumberLeft.started')
                # update status
                NumberLeft.status = STARTED
                NumberLeft.setAutoDraw(True)
            
            # if NumberLeft is active this frame...
            if NumberLeft.status == STARTED:
                # update params
                pass
            
            # *NumberRight* updates
            
            # if NumberRight is starting this frame...
            if NumberRight.status == NOT_STARTED and tThisFlip >= 0.2-frameTolerance:
                # keep track of start time/frame for later
                NumberRight.frameNStart = frameN  # exact frame index
                NumberRight.tStart = t  # local t and not account for scr refresh
                NumberRight.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(NumberRight, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'NumberRight.started')
                # update status
                NumberRight.status = STARTED
                NumberRight.setAutoDraw(True)
            
            # if NumberRight is active this frame...
            if NumberRight.status == STARTED:
                # update params
                pass
            
            # *Response* updates
            waitOnFlip = False
            
            # if Response is starting this frame...
            if Response.status == NOT_STARTED and tThisFlip >= 0.2-frameTolerance:
                # keep track of start time/frame for later
                Response.frameNStart = frameN  # exact frame index
                Response.tStart = t  # local t and not account for scr refresh
                Response.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Response, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Response.started')
                # update status
                Response.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(Response.clock.reset)  # t=0 on next screen flip
            if Response.status == STARTED and not waitOnFlip:
                theseKeys = Response.getKeys(keyList=['a','k'], waitRelease=False)
                _Response_allKeys.extend(theseKeys)
                if len(_Response_allKeys):
                    Response.keys = _Response_allKeys[-1].name  # just the last key pressed
                    Response.rt = _Response_allKeys[-1].rt
                    Response.duration = _Response_allKeys[-1].duration
                    # was this correct?
                    if (Response.keys == str(corrAns)) or (Response.keys == corrAns):
                        Response.corr = 1
                    else:
                        Response.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
                if eyetracker:
                    eyetracker.setConnectionState(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in TrialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Trial" ---
        for thisComponent in TrialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if Response.keys in ['', [], None]:  # No response was made
            Response.keys = None
            # was no response the correct answer?!
            if str(corrAns).lower() == 'none':
               Response.corr = 1;  # correct non-response
            else:
               Response.corr = 0;  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('Response.keys',Response.keys)
        trials.addData('Response.corr', Response.corr)
        if Response.keys != None:  # we had a response
            trials.addData('Response.rt', Response.rt)
            trials.addData('Response.duration', Response.duration)
        # the Routine "Trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'trials'
    
# completed 1 repeats of 'blocks'


# --- Prepare to start Routine "End" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
EndComponents = [Text5]
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
frameN = -1

# --- Run Routine "End" ---
routineForceEnded = not continueRoutine
while continueRoutine and routineTimer.getTime() < 1.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *Text5* updates
    
    # if Text5 is starting this frame...
    if Text5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Text5.frameNStart = frameN  # exact frame index
        Text5.tStart = t  # local t and not account for scr refresh
        Text5.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Text5, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'Text5.started')
        # update status
        Text5.status = STARTED
        Text5.setAutoDraw(True)
    
    # if Text5 is active this frame...
    if Text5.status == STARTED:
        # update params
        pass
    
    # if Text5 is stopping this frame...
    if Text5.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > Text5.tStartRefresh + 1.0-frameTolerance:
            # keep track of stop time/frame for later
            Text5.tStop = t  # not accounting for scr refresh
            Text5.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Text5.stopped')
            # update status
            Text5.status = FINISHED
            Text5.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in EndComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "End" ---
for thisComponent in EndComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-1.000000)

# --- End experiment ---
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
