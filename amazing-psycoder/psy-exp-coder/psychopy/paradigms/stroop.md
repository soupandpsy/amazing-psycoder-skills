# Stroop — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [stroop](../../../psy-exp-designer/paradigms/stroop.md)
> **Source**: [Pavlovia demos/Stroop](https://gitlab.pavlovia.org/demos/Stroop) · PsychoPy 3.1.3

## Experiment Logic

The classic Stroop task measures the cost of conflicting semantic and perceptual information on response selection. On each trial, a color word (e.g., "RED", "GREEN", "BLUE") is displayed on screen, but the font color of that word is independently controlled. The participant's task is to identify the font color while ignoring the word's meaning. This creates congruent trials (word meaning matches font color, e.g., "RED" in red font), incongruent trials (word meaning conflicts with font color, e.g., "RED" in green font), and neutral trials.

The trial routine uses a merged stimulus-and-response pattern: after a brief 500 ms blank period, the word text stimulus and the keyboard response component both become active simultaneously. The word is drawn via `visual.TextStim`, with its text content set from the conditions file's `text` column and its font color set via `setColor()` from the `letterColor` column. The response keyboard listens for exactly three keys: `left`, `down`, and `right`.

The key-to-color mapping is fixed and presented in the instructions: the Left arrow means red, the Down arrow means green, and the Right arrow means blue. For example, if the word "RED" appears in blue font, the correct response is Right (because the font color is blue). Accuracy is determined by comparing the pressed key name to the `corrAns` value from the conditions spreadsheet -- `corrAns` contains the key name (e.g., `'left'`, `'down'`, `'right'`) that corresponds to the font color for that trial.

Response collection uses `keyboard.Keyboard()`. On the first frame that the response component starts, the keyboard clock is reset and any prior events are cleared via `win.callOnFlip()`. This ensures reaction time is measured from the moment the stimulus appears on screen. On subsequent frames, `getKeys()` polls the specified key list. When a key is detected, its `.name` and `.rt` attributes are stored, `resp.corr` is scored as 1 or 0, and the routine ends. If no response is made, the trial is recorded with `resp.keys = None` and `resp.corr = 0`.

The experiment flow is: participant info dialog, an instruction screen (any-key-to-continue), a block of trials (5 repetitions of the conditions file, randomly ordered), a thank-you screen (2-second timed display), and data export to both CSV and Excel formats. The conditions are loaded from `trialTypes.xls` and the key columns are `text` (the word to display), `letterColor` (the RGB font color), and `corrAns` (the correct key name).

## Variants

### Numerical Stroop

The Numerical Stroop variant replaces color words with digits. Two numbers are displayed simultaneously on the left and right sides of the screen. The participant must judge which number is numerically larger and press 'a' for the left number or 'k' for the right number. The key manipulation is that the physical font size of each number can be congruent (the numerically larger number is also physically larger) or incongruent (the numerically larger number is physically smaller). This tests whether participants can ignore the irrelevant dimension of physical size when making numerical magnitude judgments. The conditions file provides `number1`, `number2`, `size1`, `size2`, and `corrAns`. A short fixation cross (100 ms) precedes the stimuli, which appear at 200 ms. Feedback ("Correct!" / "Oops! That was wrong") is shown for 1 second after each trial. The experiment has a block structure with per-block instruction screens, separate practice and main trial loops, and uses the newer PsychoPy iohub keyboard backend.

### Children's Flanker Task

The Flanker task uses fish images rather than text stimuli to be child-friendly. Five fish are displayed in a horizontal row: a central target fish flanked by two fish on each side. The participant must respond to the direction the central fish is facing (left or right arrow key) while ignoring the direction of the flanking fish. Congruent trials have all five fish facing the same direction; incongruent trials have the flankers facing the opposite direction from the target. A fixation cross appears for 1 second before the fish array. The conditions CSV file contains `Fish1`, `Fish2`, `targetFish`, `Fish3`, `Fish4` (image filenames), and `corrAns`. Practice trials (first 6 rows of conditions) include feedback showing RT; main trials (rows 6--12) have no feedback. The code uses the modern PsychoPy `TrialHandler2` and `data.Routine` API with structured setup functions (`showExpInfoDlg`, `setupData`, `setupWindow`, `setupDevices`) and proper pause/quit handling.

### Simon Task

The Simon task tests spatial compatibility: two circles are displayed side by side, and one of them is colored (red or green). The color indicates which side to select -- red means click the left circle, green means click the right circle. Critically, the position of the colored circle varies independently of the color rule, creating congruent trials (the red circle appears on the left, or the green circle appears on the right) and incongruent trials (the red circle appears on the right, or the green circle appears on the left). Response is collected via mouse click rather than keyboard. A `loop_until_correct` inner loop (max 10 repetitions) repeats each practice trial until the correct circle is clicked. Feedback ("Correct!" / "Incorrect") is displayed for 500 ms after each trial. The conditions file provides `left_color`, `right_color`, and `correct_response` (the object name to click). The experiment includes practice trials followed by 5 repetitions of the main conditions, both using mouse-based `event.Mouse` with click detection on `ShapeStim` circles via `.contains()`.

## Key Design Patterns

- **Merged stimulus+response onset**: Both the word and the keyboard component start at the same timestamp (0.5s into the routine). There is no separate fixation or ISI routine -- everything runs in a single `trial` routine. This keeps the trial loop simpler at the cost of less flexibility.
- **Conditions-driven congruency**: The `text` (word meaning) and `letterColor` (font color) are both columns in the conditions spreadsheet. Congruency is an emergent property of which rows are included, not computed in code. The `corrAns` column pre-computes the correct key for each row.
- **Keyboard clock reset on flip**: `win.callOnFlip(resp.clock.reset)` and `win.callOnFlip(resp.clearEvents, eventType='keyboard')` ensure that RT measurement starts precisely when the stimulus appears on screen, not when the Python code begins executing. The `waitOnFlip` guard prevents `getKeys()` from polling before the flip completes.
- **Dynamic parameter injection via `exec()`**: The conditions file columns are injected as local variables using `exec('{} = thisTrial[paramName]'.format(paramName))`. This means column names like `text`, `letterColor`, and `corrAns` become directly usable Python variable names within the trial loop, avoiding explicit dictionary lookups.
- **Non-slip timer for timed routines**: The "thanks" routine uses `routineTimer.add(2.0)` and `while continueRoutine and routineTimer.getTime() > 0` to run for exactly 2 seconds. At the end, `routineTimer.reset()` cleans up the timer state.
- **Component lifecycle tracking**: Every component (stimuli, keyboards) tracks its status through `NOT_STARTED`, `STARTED`, and `FINISHED` states, with corresponding `tStartRefresh`/`tStopRefresh` timestamps recorded for data logging. The routine continues until all components report `FINISHED` or a response forces an early exit.

## Code Example (Stroop)

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.1.3),
    on June 24, 2019, at 16:21
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

from psychopy.hardware import keyboard

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '3.1.3'
expName = 'stroop'  # from the Builder filename that created this script
expInfo = {'session': '01', 'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data' + os.sep + '%s_%s' % (expInfo['participant'], expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\lpzdb\\pavloviaDemos\\stroop\\stroop.py',
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
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='black', colorSpace='rgb',
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

# Initialize components for Routine "instruct"
instructClock = core.Clock()
instrText = visual.TextStim(win=win, name='instrText',
    text='OK. Ready for the real thing?\n\nRemember, ignore the word itself; press:\nLeft for red LETTERS\nDown for green LETTERS\nRight for blue LETTERS\n(Esc will quit)\n\nPress any key to continue',
    font='Arial',
    units='height', pos=[0, 0], height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "trial"
trialClock = core.Clock()
word = visual.TextStim(win=win, name='word',
    text='default text',
    font='Arial',
    units='height', pos=[0, 0], height=0.15, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "thanks"
thanksClock = core.Clock()
thanksText = visual.TextStim(win=win, name='thanksText',
    text='This is the end of the experiment.\n\nThanks!',
    font='Arial',
    units='height', pos=[0, 0], height=0.05, wrapWidth=None, ori=0, 
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
ready = keyboard.Keyboard()
# keep track of which components have finished
instructComponents = [instrText, ready]
for thisComponent in instructComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instruct"-------
while continueRoutine:
    # get current time
    t = instructClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instrText* updates
    if t >= 0 and instrText.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrText.tStart = t  # not accounting for scr refresh
        instrText.frameNStart = frameN  # exact frame index
        win.timeOnFlip(instrText, 'tStartRefresh')  # time at next scr refresh
        instrText.setAutoDraw(True)
    
    # *ready* updates
    waitOnFlip = False
    if t >= 0 and ready.status == NOT_STARTED:
        # keep track of start time/frame for later
        ready.tStart = t  # not accounting for scr refresh
        ready.frameNStart = frameN  # exact frame index
        win.timeOnFlip(ready, 'tStartRefresh')  # time at next scr refresh
        ready.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(ready.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if ready.status == STARTED and not waitOnFlip:
        theseKeys = ready.getKeys(keyList=None, waitRelease=False)
        if len(theseKeys):
            theseKeys = theseKeys[0]  # at least one key was pressed
            
            # check for quit:
            if "escape" == theseKeys:
                endExpNow = True
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instruct"-------
for thisComponent in instructComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('instrText.started', instrText.tStartRefresh)
thisExp.addData('instrText.stopped', instrText.tStopRefresh)
# the Routine "instruct" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('trialTypes.xls'),
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
    word.setColor(letterColor, colorSpace='rgb')
    word.setText(text)
    resp = keyboard.Keyboard()
    # keep track of which components have finished
    trialComponents = [word, resp]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *word* updates
        if t >= 0.5 and word.status == NOT_STARTED:
            # keep track of start time/frame for later
            word.tStart = t  # not accounting for scr refresh
            word.frameNStart = frameN  # exact frame index
            win.timeOnFlip(word, 'tStartRefresh')  # time at next scr refresh
            word.setAutoDraw(True)
        
        # *resp* updates
        waitOnFlip = False
        if t >= 0.5 and resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            resp.tStart = t  # not accounting for scr refresh
            resp.frameNStart = frameN  # exact frame index
            win.timeOnFlip(resp, 'tStartRefresh')  # time at next scr refresh
            resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if resp.status == STARTED and not waitOnFlip:
            theseKeys = resp.getKeys(keyList=['left', 'down', 'right'], waitRelease=False)
            if len(theseKeys):
                theseKeys = theseKeys[0]  # at least one key was pressed
                
                # check for quit:
                if "escape" == theseKeys:
                    endExpNow = True
                resp.keys = theseKeys.name  # just the last key pressed
                resp.rt = theseKeys.rt
                # was this 'correct'?
                if (resp.keys == str(corrAns)) or (resp.keys == corrAns):
                    resp.corr = 1
                else:
                    resp.corr = 0
                # a response ends the routine
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
    trials.addData('word.started', word.tStartRefresh)
    trials.addData('word.stopped', word.tStopRefresh)
    # check responses
    if resp.keys in ['', [], None]:  # No response was made
        resp.keys = None
        # was no response the correct answer?!
        if str(corrAns).lower() == 'none':
           resp.corr = 1;  # correct non-response
        else:
           resp.corr = 0;  # failed to respond (incorrectly)
    # store data for trials (TrialHandler)
    trials.addData('resp.keys',resp.keys)
    trials.addData('resp.corr', resp.corr)
    if resp.keys != None:  # we had a response
        trials.addData('resp.rt', resp.rt)
    trials.addData('resp.started', resp.tStartRefresh)
    trials.addData('resp.stopped', resp.tStopRefresh)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 5 repeats of 'trials'

# get names of stimulus parameters
if trials.trialList in ([], [None], None):
    params = []
else:
    params = trials.trialList[0].keys()
# save data for this loop
trials.saveAsExcel(filename + '.xlsx', sheetName='trials',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

# ------Prepare to start Routine "thanks"-------
t = 0
thanksClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(2.000000)
# update component parameters for each repeat
# keep track of which components have finished
thanksComponents = [thanksText]
for thisComponent in thanksComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
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
        thanksText.tStart = t  # not accounting for scr refresh
        thanksText.frameNStart = frameN  # exact frame index
        win.timeOnFlip(thanksText, 'tStartRefresh')  # time at next scr refresh
        thanksText.setAutoDraw(True)
    frameRemains = 0.0 + 2.0- win.monitorFramePeriod * 0.75  # most of one frame period left
    if thanksText.status == STARTED and t >= frameRemains:
        # keep track of stop time/frame for later
        thanksText.tStop = t  # not accounting for scr refresh
        thanksText.frameNStop = frameN  # exact frame index
        win.timeOnFlip(thanksText, 'tStopRefresh')  # time at next scr refresh
        thanksText.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in thanksComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "thanks"-------
for thisComponent in thanksComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('thanksText.started', thanksText.tStartRefresh)
thisExp.addData('thanksText.stopped', thanksText.tStopRefresh)

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
```
