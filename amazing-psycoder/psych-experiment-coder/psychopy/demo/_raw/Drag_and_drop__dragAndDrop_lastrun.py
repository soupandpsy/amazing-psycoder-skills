# Source: Drag and drop (demos/Drag_and_drop)
# Project URL: https://gitlab.pavlovia.org/demos/Drag_and_drop
# Original file: dragAndDrop_lastrun.py
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.2.0),
    on August 20, 2019, at 13:05
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
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
psychopyVersion = '3.2.0'
expName = 'puzzleDB'  # from the Builder filename that created this script
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
    originPath='C:\\Users\\lpzdb\\Desktop\\discourseExp\\dragAndDropDemo\\dragAndDrop_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=False, screen=0, 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='pix')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "InstructionsRoutine"
InstructionsRoutineClock = core.Clock()
introText = visual.TextStim(win=win, name='introText',
    text='This task shows you the drag and drop capabilities of PsychoPy and PsychoJS.\n\nThe demonstration uses a drag and drop puzzle game. \nThe task requires you to drag and drop the black and white\npieces into the empty square, in order to match the \npuzzle design above.\n\nWhen you have finished, press the "END" button to \nsee whether or not you were correct, and how long the\nthe trial took.\n\nClick or tap continue to begin.',
    font='Arial',
    units='pix', pos=(0, 0), height=25, wrapWidth=800, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
start = visual.ImageStim(
    win=win,
    name='start', units='pix', 
    image='continueButton.png', mask=None,
    ori=0, pos=(0, -400), size=(110, 40),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
startMouse = event.Mouse(win=win)
x, y = [None, None]
startMouse.mouseClock = core.Clock()

# Initialize components for Routine "designA"
designAClock = core.Clock()
masterPatternA = visual.ImageStim(
    win=win,
    name='masterPatternA', 
    image='sin', mask=None,
    ori=0, pos=(0, 200), size=1.0,
    color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=True, depth=0.0)
key_resp = keyboard.Keyboard()
polygon = visual.Rect(
    win=win, name='polygon',units='pix', 
    width=[1.0, 1.0][0], height=[1.0, 1.0][1],
    ori=0, pos=(0, -100),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1, depth=-2.0, interpolate=True)
whitePiece = visual.ImageStim(
    win=win,
    name='whitePiece', 
    image='white.png', mask=None,
    ori=0, pos=[0,0], size=1.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
blackPiece = visual.ImageStim(
    win=win,
    name='blackPiece', 
    image='black.png', mask=None,
    ori=0, pos=[0,0], size=1.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()
def createPiece(piece, pos, name):
    return visual.ImageStim(win, image=piece.image, name=name, size=piece.size, pos=pos)

def drawPicked(picked):
    for each in picked:
        each.draw()

def movePicked(picked, mouse, grabbed):
    if grabbed is not None and mouse.isPressedIn(grabbed):
        grabbed.pos = mouse.getPos()
        return grabbed
    else:
        for piece in picked:
            if mouse.isPressedIn(piece) and grabbed is None:
                return piece

def createGrid(rows, size, pos, names):
    inc = (size/rows)
    rowStart = pos[0] - size/2
    colStart = pos[1] + size/2
    row, col = rowStart  + inc/2, colStart - inc/2
    counter = 0
    
    grid = []
    for i in range(rows):
        for j in range(rows):
            grid.append(visual.Rect(win, name=names[counter], units='pix', size = [size/rows, size/rows], pos= [row,col], lineColor= 'lightgrey'))
            row += inc
            counter += 1
        col -= inc
        row = rowStart + inc/2
    return grid

def drawGrid(grid):
    for i in grid:
        i.draw()

def checkAnswer(grid, pieces):
    # Get names of pieces that were picked
    picNames = [pic.image for pic in pieces]
    correctPieces = []
    for cell in grid:
        # Check if piece has been picked
        if cell.name in picNames:
            
            for name in range(0, len(picNames)):
                if cell.name == picNames[name]:
                    if cell.contains(pieces[name].pos):
                        correctPieces.append(True)
                        break  # Piece found, go to next cell
        else:
            return False  # Correct piece not picked
    return len(correctPieces) == len(grid)
    
end = visual.ImageStim(
    win=win,
    name='end', units='pix', 
    image='continueButton.png', mask=None,
    ori=0, pos=(0, -400), size=(110, 40),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-7.0)

# Initialize components for Routine "result"
resultClock = core.Clock()
resultAccuracy = visual.TextStim(win=win, name='resultAccuracy',
    text=None,
    font='Arial',
    pos=(0, 200), height=20, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
resultTextA = visual.TextStim(win=win, name='resultTextA',
    text=None,
    font='Arial',
    pos=(0, 0), height=25, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
endFB = keyboard.Keyboard()
trialEnd = visual.ImageStim(
    win=win,
    name='trialEnd', units='pix', 
    image='continueButton.png', mask=None,
    ori=0, pos=(0, -400), size=(110, 40),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
endTrialMouse = event.Mouse(win=win)
x, y = [None, None]
endTrialMouse.mouseClock = core.Clock()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "InstructionsRoutine"-------
t = 0
InstructionsRoutineClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the startMouse
startMouse.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
InstructionsRoutineComponents = [introText, start, startMouse]
for thisComponent in InstructionsRoutineComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "InstructionsRoutine"-------
while continueRoutine:
    # get current time
    t = InstructionsRoutineClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=InstructionsRoutineClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *introText* updates
    if introText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        introText.frameNStart = frameN  # exact frame index
        introText.tStart = t  # local t and not account for scr refresh
        introText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(introText, 'tStartRefresh')  # time at next scr refresh
        introText.setAutoDraw(True)
    
    # *start* updates
    if start.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start.frameNStart = frameN  # exact frame index
        start.tStart = t  # local t and not account for scr refresh
        start.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start, 'tStartRefresh')  # time at next scr refresh
        start.setAutoDraw(True)
    # *startMouse* updates
    if startMouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        startMouse.frameNStart = frameN  # exact frame index
        startMouse.tStart = t  # local t and not account for scr refresh
        startMouse.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(startMouse, 'tStartRefresh')  # time at next scr refresh
        startMouse.status = STARTED
        startMouse.mouseClock.reset()
        prevButtonState = startMouse.getPressed()  # if button is down already this ISN'T a new click
    if startMouse.status == STARTED:  # only update if started and not finished!
        buttons = startMouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                for obj in [start]:
                    if obj.contains(startMouse):
                        gotValidClick = True
                        startMouse.clicked_name.append(obj.name)
                if gotValidClick:  # abort routine on response
                    continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstructionsRoutineComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "InstructionsRoutine"-------
for thisComponent in InstructionsRoutineComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('introText.started', introText.tStartRefresh)
thisExp.addData('introText.stopped', introText.tStopRefresh)
thisExp.addData('start.started', start.tStartRefresh)
thisExp.addData('start.stopped', start.tStopRefresh)
# store data for thisExp (ExperimentHandler)
thisExp.addData('startMouse.started', startMouse.tStart)
thisExp.addData('startMouse.stopped', startMouse.tStop)
thisExp.nextEntry()
# the Routine "InstructionsRoutine" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method='sequential', 
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
    
    # ------Prepare to start Routine "designA"-------
    t = 0
    designAClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    masterPatternA.setSize(size_design)
    masterPatternA.setImage(design1)
    key_resp.keys = [];
    key_resp.rt = None;
    polygon.setSize(size)
    whitePiece.setPos((-400, 0))
    whitePiece.setSize(size / nRows1)
    blackPiece.setPos((400, 0))
    blackPiece.setSize(size / nRows1)
    # setup some python lists for storing info about the mouse
    mouse.clicked_name = []
    gotValidClick = False  # until a click is received
    pieces = [whitePiece, blackPiece]
    answers = [a1,a2,a3,a4,a5,a6,a7,a8,a9]
    picked = []
    newPiece = None
    movingPiece = None
    grid = createGrid(nRows1, size, polygon.pos, answers)
    polygon.setFillColor(None)
    # keep track of which components have finished
    designAComponents = [masterPatternA, key_resp, polygon, whitePiece, blackPiece, mouse, end]
    for thisComponent in designAComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "designA"-------
    while continueRoutine:
        # get current time
        t = designAClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=designAClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *masterPatternA* updates
        if masterPatternA.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            masterPatternA.frameNStart = frameN  # exact frame index
            masterPatternA.tStart = t  # local t and not account for scr refresh
            masterPatternA.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(masterPatternA, 'tStartRefresh')  # time at next scr refresh
            masterPatternA.setAutoDraw(True)
        
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
            if len(theseKeys):
                theseKeys = theseKeys[0]  # at least one key was pressed
                
                # check for quit:
                if "escape" == theseKeys:
                    endExpNow = True
                key_resp.keys = theseKeys.name  # just the last key pressed
                key_resp.rt = theseKeys.rt
                # a response ends the routine
                continueRoutine = False
        
        # *polygon* updates
        if polygon.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            polygon.frameNStart = frameN  # exact frame index
            polygon.tStart = t  # local t and not account for scr refresh
            polygon.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(polygon, 'tStartRefresh')  # time at next scr refresh
            polygon.setAutoDraw(True)
        
        # *whitePiece* updates
        if whitePiece.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            whitePiece.frameNStart = frameN  # exact frame index
            whitePiece.tStart = t  # local t and not account for scr refresh
            whitePiece.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(whitePiece, 'tStartRefresh')  # time at next scr refresh
            whitePiece.setAutoDraw(True)
        
        # *blackPiece* updates
        if blackPiece.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            blackPiece.frameNStart = frameN  # exact frame index
            blackPiece.tStart = t  # local t and not account for scr refresh
            blackPiece.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(blackPiece, 'tStartRefresh')  # time at next scr refresh
            blackPiece.setAutoDraw(True)
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
                    for obj in [end]:
                        if obj.contains(mouse):
                            gotValidClick = True
                            mouse.clicked_name.append(obj.name)
                    if gotValidClick:  # abort routine on response
                        continueRoutine = False
        for piece in pieces:
            if mouse.isPressedIn(piece) and newPiece == None:
                newPiece = createPiece(piece, mouse.getPos(), piece.image)
                picked.append(newPiece)
                
            
        if newPiece is not None and mouse.getPressed()[0] == 0:
            newPiece = None
        
        movingPiece = movePicked(picked, mouse, movingPiece)
        drawGrid(grid)
        drawPicked(picked)
        
        
        # *end* updates
        if end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            end.frameNStart = frameN  # exact frame index
            end.tStart = t  # local t and not account for scr refresh
            end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(end, 'tStartRefresh')  # time at next scr refresh
            end.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in designAComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "designA"-------
    for thisComponent in designAComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    trials.addData('masterPatternA.started', masterPatternA.tStartRefresh)
    trials.addData('masterPatternA.stopped', masterPatternA.tStopRefresh)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    trials.addData('key_resp.keys',key_resp.keys)
    if key_resp.keys != None:  # we had a response
        trials.addData('key_resp.rt', key_resp.rt)
    trials.addData('key_resp.started', key_resp.tStartRefresh)
    trials.addData('key_resp.stopped', key_resp.tStopRefresh)
    trials.addData('polygon.started', polygon.tStartRefresh)
    trials.addData('polygon.stopped', polygon.tStopRefresh)
    trials.addData('whitePiece.started', whitePiece.tStartRefresh)
    trials.addData('whitePiece.stopped', whitePiece.tStopRefresh)
    trials.addData('blackPiece.started', blackPiece.tStartRefresh)
    trials.addData('blackPiece.stopped', blackPiece.tStopRefresh)
    # store data for trials (TrialHandler)
    trials.addData('mouse.started', mouse.tStart)
    trials.addData('mouse.stopped', mouse.tStop)
    designATime = int(designAClock.getTime())
    correctA = checkAnswer(grid, picked)
    trials.addData('end.started', end.tStartRefresh)
    trials.addData('end.stopped', end.tStopRefresh)
    # the Routine "designA" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "result"-------
    t = 0
    resultClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    if correctA:
        resultTextA.text = "Correct!\n"
    else:
        resultTextA.text = "Incorrect!\n"
        
    resultTextA.text += f"Time taken: {designATime} seconds\n"
    
    thisExp.addData('correctA', correctA)
    thisExp.addData('p1Actual', designATime)
    
    endFB.keys = [];
    endFB.rt = None;
    # setup some python lists for storing info about the endTrialMouse
    endTrialMouse.clicked_name = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    resultComponents = [resultAccuracy, resultTextA, endFB, trialEnd, endTrialMouse]
    for thisComponent in resultComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "result"-------
    while continueRoutine:
        # get current time
        t = resultClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=resultClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *resultAccuracy* updates
        if resultAccuracy.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            resultAccuracy.frameNStart = frameN  # exact frame index
            resultAccuracy.tStart = t  # local t and not account for scr refresh
            resultAccuracy.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(resultAccuracy, 'tStartRefresh')  # time at next scr refresh
            resultAccuracy.setAutoDraw(True)
        
        # *resultTextA* updates
        if resultTextA.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            resultTextA.frameNStart = frameN  # exact frame index
            resultTextA.tStart = t  # local t and not account for scr refresh
            resultTextA.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(resultTextA, 'tStartRefresh')  # time at next scr refresh
            resultTextA.setAutoDraw(True)
        
        # *endFB* updates
        waitOnFlip = False
        if endFB.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            endFB.frameNStart = frameN  # exact frame index
            endFB.tStart = t  # local t and not account for scr refresh
            endFB.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(endFB, 'tStartRefresh')  # time at next scr refresh
            endFB.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(endFB.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(endFB.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if endFB.status == STARTED and not waitOnFlip:
            theseKeys = endFB.getKeys(keyList=['space'], waitRelease=False)
            if len(theseKeys):
                theseKeys = theseKeys[0]  # at least one key was pressed
                
                # check for quit:
                if "escape" == theseKeys:
                    endExpNow = True
                endFB.keys = theseKeys.name  # just the last key pressed
                endFB.rt = theseKeys.rt
                # a response ends the routine
                continueRoutine = False
        
        # *trialEnd* updates
        if trialEnd.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            trialEnd.frameNStart = frameN  # exact frame index
            trialEnd.tStart = t  # local t and not account for scr refresh
            trialEnd.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trialEnd, 'tStartRefresh')  # time at next scr refresh
            trialEnd.setAutoDraw(True)
        # *endTrialMouse* updates
        if endTrialMouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            endTrialMouse.frameNStart = frameN  # exact frame index
            endTrialMouse.tStart = t  # local t and not account for scr refresh
            endTrialMouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(endTrialMouse, 'tStartRefresh')  # time at next scr refresh
            endTrialMouse.status = STARTED
            endTrialMouse.mouseClock.reset()
            prevButtonState = endTrialMouse.getPressed()  # if button is down already this ISN'T a new click
        if endTrialMouse.status == STARTED:  # only update if started and not finished!
            buttons = endTrialMouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    for obj in [trialEnd]:
                        if obj.contains(endTrialMouse):
                            gotValidClick = True
                            endTrialMouse.clicked_name.append(obj.name)
                    if gotValidClick:  # abort routine on response
                        continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in resultComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "result"-------
    for thisComponent in resultComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    trials.addData('resultAccuracy.started', resultAccuracy.tStartRefresh)
    trials.addData('resultAccuracy.stopped', resultAccuracy.tStopRefresh)
    trials.addData('resultTextA.started', resultTextA.tStartRefresh)
    trials.addData('resultTextA.stopped', resultTextA.tStopRefresh)
    # check responses
    if endFB.keys in ['', [], None]:  # No response was made
        endFB.keys = None
    trials.addData('endFB.keys',endFB.keys)
    if endFB.keys != None:  # we had a response
        trials.addData('endFB.rt', endFB.rt)
    trials.addData('endFB.started', endFB.tStartRefresh)
    trials.addData('endFB.stopped', endFB.tStopRefresh)
    trials.addData('trialEnd.started', trialEnd.tStartRefresh)
    trials.addData('trialEnd.stopped', trialEnd.tStopRefresh)
    # store data for trials (TrialHandler)
    trials.addData('endTrialMouse.started', endTrialMouse.tStart)
    trials.addData('endTrialMouse.stopped', endTrialMouse.tStop)
    # the Routine "result" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'trials'


# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
