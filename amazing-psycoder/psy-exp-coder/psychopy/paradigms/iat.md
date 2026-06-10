# IAT -- PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [iat](../../../psy-exp-designer/paradigms/iat.md)
> **Source**: [Pavlovia demos/OpenIAT](https://gitlab.pavlovia.org/demos/OpenIAT) · PsychoPy 2020.1.0

## Experiment Logic

The OpenIAT implements the standard 7-block Implicit Association Test. The experiment begins with a participant-info dialog (participant ID, session, gender, and counterbalance order). The order parameter (1, 2, or random) selects which Excel-based block-order file to load from the `resources/` folder -- `blocks_order1.xlsx` or `blocks_order2.xlsx`. This is the counterbalancing mechanism: order 1 and order 2 swap which combined blocks (compatible vs incompatible pairings) appear first, controlling for order effects.

Each block in the condition file defines `label_left` and `label_right` (the category labels displayed on green on-screen buttons) and a `conds_file` that points to the trial-level condition file. For single-discrimination blocks (Blocks 1, 2, and 5), the labels are individual categories (e.g., "Flowers" / "Insects" or "Good" / "Bad"). For combined blocks (Blocks 3, 4, 6, and 7), the labels are concatenated pairs (e.g., "Flowers or Good" / "Insects or Bad"). Blocks 1, 2, 3, 5, and 6 are practice blocks with fewer trials; Blocks 4 and 7 are test blocks with more trials. The ready screen before each block displays the current left/right labels and waits for a spacebar press or green-button click, giving participants a moment to process which categories map to which side.

Each trial begins with a 500ms fixation cross (`+`), after which the stimulus appears along with the left/right category buttons. Stimuli come from trial condition files as either images (`stimImage` path) or text words (`stimWord`). The participant classifies the stimulus by pressing `a` (left) or `l` (right), or by clicking the on-screen green buttons. The correct answer key per trial is specified by the `CorrAns` field in the trial condition file. A 1-second feedback screen follows each response: `+` for correct, `oops` for incorrect. This is informational feedback, not forced error correction -- any valid response advances the trial regardless of correctness.

The critical data for IAT D-score computation are saved at two levels. Trial-level data (`key_resp.keys`, `key_resp.corr`, `key_resp.rt`) go into the trials TrialHandler, while experiment-level columns (`rt` and `corr`) are written via `thisExp.addData()` for every trial. This dual storage ensures the raw RT and accuracy data needed for D-score calculation are available in the output CSV. After all blocks finish, the experiment displays a thank-you screen and saves data as both CSV and Pickle files.

## Key Design Patterns

- **Condition-file-driven block sequences**: Block order, labels, and trial files are all loaded from Excel condition files, enabling counterbalancing by swapping which `blocks_orderN.xlsx` is used without changing code.
- **Dual response modality**: Both keyboard (`a`/`l`) and mouse/touch (on-screen green buttons) responses are supported and processed through parallel code paths, with correctness resolved after the trial.
- **Dynamic label rendering**: `label_left` and `label_right` are read from each block's condition row and injected into both the ready-screen labels and the trial-level left/right button text via `.setText()`.
- **Per-block trial file indirection**: Rather than hardcoding trial lists, each block's `conds_file` column names a separate Excel file whose rows supply `stimImage`, `stimWord`, and `CorrAns` for that block's trials.
- **Experiment-level RT/corr recording**: Response time and correctness are written to the ExperimentHandler via `thisExp.addData('rt', rt)` and `thisExp.addData('corr', corr)` on every trial, providing flat columns in the output CSV for easy D-score extraction.
- **Fixation onset timing**: The fixation cross is displayed for exactly 500ms by checking `tThisFlip > 0.5` in the trial routine, after which the stimulus and response buttons appear -- a simple non-slip timing pattern.

## Code Example

Complete runnable PsychoPy code for IAT:

```python
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
psychopyVersion = '2020.1.0rc3'
expName = 'IAT-1.4'  # from the Builder filename that created this script
expInfo = {'participant': '', 'order': ['random', 1, 2], 'session': '001', 'gender': ['male', 'female', 'other']}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\lpzjwp\\Dropbox\\_psychopyStuff\\experiments\\openIAT\\openIAT_lastrun.py',
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

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
if expInfo['order']=='random':
    expInfo['order'] = randint(1,2)

blocks_file = "blocks_order"+str(expInfo['order'])+".xlsx"
instructs_text = visual.TextStim(win=win, name='instructs_text',
    text='default text',
    font='Arial',
    units='height', pos=[0, 0], height=0.03, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=-1.0);
instruct_done = keyboard.Keyboard()
instr_done_button = visual.Rect(
    win=win, name='instr_done_button',units='height',
    width=(0.4, 0.1)[0], height=(0.4, 0.1)[1],
    ori=0, pos=(0, -0.4),
    lineWidth=1, lineColor='darkgreen', lineColorSpace='rgb',
    fillColor='lightgreen', fillColorSpace='rgb',
    opacity=1, depth=-3.0, interpolate=True)
instr_done_label = visual.TextStim(win=win, name='instr_done_label',
    text='Next...',
    font='Arial',
    units='height', pos=(0, -0.4), height=0.05, wrapWidth=None, ori=0,
    color='darkgreen', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=-4.0);
instr_done_touch = event.Mouse(win=win)
x, y = [None, None]
instr_done_touch.mouseClock = core.Clock()

# Initialize components for Routine "ready"
readyClock = core.Clock()
main_ready_msg = visual.TextStim(win=win, name='main_ready_msg',
    text='Take note of the categories below\n \nPosition your index fingers \n \nPress the space bar (or one of the green buttons) to begin',
    font='Arial',
    units='height', pos=[0, 0], height=0.03, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=0.0);
button_L = visual.Rect(
    win=win, name='button_L',units='height',
    width=(0.4, 0.2)[0], height=(0.4, 0.2)[1],
    ori=0, pos=(-0.4, -0.3),
    lineWidth=1, lineColor='darkgreen', lineColorSpace='rgb',
    fillColor='lightgreen', fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)
ready_label_L = visual.TextStim(win=win, name='ready_label_L',
    text='default text',
    font='Arial',
    units='height', pos=[-0.4, -0.3], height=0.05, wrapWidth=None, ori=0,
    color='darkgreen', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=-2.0);
button_R = visual.Rect(
    win=win, name='button_R',units='height',
    width=(0.4, 0.2)[0], height=(0.4, 0.2)[1],
    ori=0, pos=(0.4, -0.3),
    lineWidth=1, lineColor='darkgreen', lineColorSpace='rgb',
    fillColor='lightgreen', fillColorSpace='rgb',
    opacity=1, depth=-3.0, interpolate=True)
ready_label_R = visual.TextStim(win=win, name='ready_label_R',
    text='default text',
    font='Arial',
    units='height', pos=[0.4, -0.3], height=0.05, wrapWidth=None, ori=0,
    color='darkgreen', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=-4.0);
ready_done_mouse = event.Mouse(win=win)
x, y = [None, None]
ready_done_mouse.mouseClock = core.Clock()
ready_done = keyboard.Keyboard()

# Initialize components for Routine "trial"
trialClock = core.Clock()
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Arial',
    units='height', pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=0.0);
image_stim = visual.ImageStim(
    win=win,
    name='image_stim', units='height',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=[0.5, 0.5],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
text_stim = visual.TextStim(win=win, name='text_stim',
    text='default text',
    font='Arial',
    units='height', pos=(0, 0), height=0.05, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=-2.0);
key_resp = keyboard.Keyboard()
touch_resp = event.Mouse(win=win)
x, y = [None, None]
touch_resp.mouseClock = core.Clock()
button_left = visual.Rect(
    win=win, name='button_left',units='height',
    width=(0.4, 0.2)[0], height=(0.4, 0.2)[1],
    ori=0, pos=(-0.4, -0.3),
    lineWidth=1, lineColor='darkgreen', lineColorSpace='rgb',
    fillColor='lightgreen', fillColorSpace='rgb',
    opacity=1, depth=-6.0, interpolate=True)
trial_label_left = visual.TextStim(win=win, name='trial_label_left',
    text='default text',
    font='Arial',
    units='height', pos=[-0.4, -0.3], height=0.05, wrapWidth=None, ori=0,
    color='darkgreen', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=-7.0);
button_right = visual.Rect(
    win=win, name='button_right',units='height',
    width=(0.4, 0.2)[0], height=(0.4, 0.2)[1],
    ori=0, pos=(0.4, -0.3),
    lineWidth=1, lineColor='darkgreen', lineColorSpace='rgb',
    fillColor='lightgreen', fillColorSpace='rgb',
    opacity=1, depth=-8.0, interpolate=True)
trial_label_right = visual.TextStim(win=win, name='trial_label_right',
    text='default text',
    font='Arial',
    units='height', pos=[0.4, -0.3], height=0.05, wrapWidth=None, ori=0,
    color='darkgreen', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=-9.0);

# Initialize components for Routine "feedback"
feedbackClock = core.Clock()
feedback_msg = visual.TextStim(win=win, name='feedback_msg',
    text='default text',
    font='Arial',
    units='height', pos=[0, 0], height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "end_thanks"
end_thanksClock = core.Clock()
thanks_text = visual.TextStim(win=win, name='thanks_text',
    text='The End. \n \nThank you for your participation.',
    font='Arial',
    units='height', pos=[0, 0], height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# set up handler to look after randomisation of conditions etc
instruct_pages = data.TrialHandler(nReps=1, method='sequential',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('resources/instructs.xlsx'),
    seed=None, name='instruct_pages')
thisExp.addLoop(instruct_pages)  # add the loop to the experiment
thisInstruct_page = instruct_pages.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisInstruct_page.rgb)
if thisInstruct_page != None:
    for paramName in thisInstruct_page:
        exec('{} = thisInstruct_page[paramName]'.format(paramName))

for thisInstruct_page in instruct_pages:
    currentLoop = instruct_pages
    # abbreviate parameter names if possible (e.g. rgb = thisInstruct_page.rgb)
    if thisInstruct_page != None:
        for paramName in thisInstruct_page:
            exec('{} = thisInstruct_page[paramName]'.format(paramName))

    # ------Prepare to start Routine "instructions"-------
    continueRoutine = True
    # update component parameters for each repeat
    instructs_text.setText(instruct_text)
    instruct_done.keys = []
    instruct_done.rt = []
    _instruct_done_allKeys = []
    # setup some python lists for storing info about the instr_done_touch
    instr_done_touch.clicked_name = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    instructionsComponents = [instructs_text, instruct_done, instr_done_button, instr_done_label, instr_done_touch]
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

        # *instructs_text* updates
        if instructs_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructs_text.frameNStart = frameN  # exact frame index
            instructs_text.tStart = t  # local t and not account for scr refresh
            instructs_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructs_text, 'tStartRefresh')  # time at next scr refresh
            instructs_text.setAutoDraw(True)

        # *instruct_done* updates
        waitOnFlip = False
        if instruct_done.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instruct_done.frameNStart = frameN  # exact frame index
            instruct_done.tStart = t  # local t and not account for scr refresh
            instruct_done.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instruct_done, 'tStartRefresh')  # time at next scr refresh
            instruct_done.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(instruct_done.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(instruct_done.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if instruct_done.status == STARTED and not waitOnFlip:
            theseKeys = instruct_done.getKeys(keyList=['space'], waitRelease=False)
            _instruct_done_allKeys.extend(theseKeys)
            if len(_instruct_done_allKeys):
                instruct_done.keys = _instruct_done_allKeys[-1].name  # just the last key pressed
                instruct_done.rt = _instruct_done_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False

        # *instr_done_button* updates
        if instr_done_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instr_done_button.frameNStart = frameN  # exact frame index
            instr_done_button.tStart = t  # local t and not account for scr refresh
            instr_done_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_done_button, 'tStartRefresh')  # time at next scr refresh
            instr_done_button.setAutoDraw(True)

        # *instr_done_label* updates
        if instr_done_label.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instr_done_label.frameNStart = frameN  # exact frame index
            instr_done_label.tStart = t  # local t and not account for scr refresh
            instr_done_label.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_done_label, 'tStartRefresh')  # time at next scr refresh
            instr_done_label.setAutoDraw(True)
        # *instr_done_touch* updates
        if instr_done_touch.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instr_done_touch.frameNStart = frameN  # exact frame index
            instr_done_touch.tStart = t  # local t and not account for scr refresh
            instr_done_touch.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_done_touch, 'tStartRefresh')  # time at next scr refresh
            instr_done_touch.status = STARTED
            instr_done_touch.mouseClock.reset()
            prevButtonState = instr_done_touch.getPressed()  # if button is down already this ISN'T a new click
        if instr_done_touch.status == STARTED:  # only update if started and not finished!
            buttons = instr_done_touch.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    for obj in [instr_done_button]:
                        if obj.contains(instr_done_touch):
                            gotValidClick = True
                            instr_done_touch.clicked_name.append(obj.name)
                    if gotValidClick:  # abort routine on response
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
    instruct_pages.addData('instr_done_button.started', instr_done_button.tStartRefresh)
    instruct_pages.addData('instr_done_button.stopped', instr_done_button.tStopRefresh)
    instruct_pages.addData('instr_done_label.started', instr_done_label.tStartRefresh)
    instruct_pages.addData('instr_done_label.stopped', instr_done_label.tStopRefresh)
    # store data for instruct_pages (TrialHandler)
    x, y = instr_done_touch.getPos()
    buttons = instr_done_touch.getPressed()
    if sum(buttons):
        # check if the mouse was inside our 'clickable' objects
        gotValidClick = False
        for obj in [instr_done_button]:
            if obj.contains(instr_done_touch):
                gotValidClick = True
                instr_done_touch.clicked_name.append(obj.name)
    instruct_pages.addData('instr_done_touch.x', x)
    instruct_pages.addData('instr_done_touch.y', y)
    instruct_pages.addData('instr_done_touch.leftButton', buttons[0])
    instruct_pages.addData('instr_done_touch.midButton', buttons[1])
    instruct_pages.addData('instr_done_touch.rightButton', buttons[2])
    if len(instr_done_touch.clicked_name):
        instruct_pages.addData('instr_done_touch.clicked_name', instr_done_touch.clicked_name[0])
    instruct_pages.addData('instr_done_touch.started', instr_done_touch.tStart)
    instruct_pages.addData('instr_done_touch.stopped', instr_done_touch.tStop)
    # the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
# completed 1 repeats of 'instruct_pages'


# set up handler to look after randomisation of conditions etc
blocks = data.TrialHandler(nReps=1, method='sequential',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions("resources/"+blocks_file),
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

    # ------Prepare to start Routine "ready"-------
    continueRoutine = True
    # update component parameters for each repeat
    ready_label_L.setText(label_left)
    ready_label_R.setText(label_right)
    # setup some python lists for storing info about the ready_done_mouse
    ready_done_mouse.clicked_name = []
    gotValidClick = False  # until a click is received
    ready_done.keys = []
    ready_done.rt = []
    _ready_done_allKeys = []
    # keep track of which components have finished
    readyComponents = [main_ready_msg, button_L, ready_label_L, button_R, ready_label_R, ready_done_mouse, ready_done]
    for thisComponent in readyComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    readyClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "ready"-------
    while continueRoutine:
        # get current time
        t = readyClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=readyClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *main_ready_msg* updates
        if main_ready_msg.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            main_ready_msg.frameNStart = frameN  # exact frame index
            main_ready_msg.tStart = t  # local t and not account for scr refresh
            main_ready_msg.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(main_ready_msg, 'tStartRefresh')  # time at next scr refresh
            main_ready_msg.setAutoDraw(True)

        # *button_L* updates
        if button_L.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            button_L.frameNStart = frameN  # exact frame index
            button_L.tStart = t  # local t and not account for scr refresh
            button_L.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(button_L, 'tStartRefresh')  # time at next scr refresh
            button_L.setAutoDraw(True)

        # *ready_label_L* updates
        if ready_label_L.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ready_label_L.frameNStart = frameN  # exact frame index
            ready_label_L.tStart = t  # local t and not account for scr refresh
            ready_label_L.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ready_label_L, 'tStartRefresh')  # time at next scr refresh
            ready_label_L.setAutoDraw(True)

        # *button_R* updates
        if button_R.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            button_R.frameNStart = frameN  # exact frame index
            button_R.tStart = t  # local t and not account for scr refresh
            button_R.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(button_R, 'tStartRefresh')  # time at next scr refresh
            button_R.setAutoDraw(True)

        # *ready_label_R* updates
        if ready_label_R.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ready_label_R.frameNStart = frameN  # exact frame index
            ready_label_R.tStart = t  # local t and not account for scr refresh
            ready_label_R.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ready_label_R, 'tStartRefresh')  # time at next scr refresh
            ready_label_R.setAutoDraw(True)
        # *ready_done_mouse* updates
        if ready_done_mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ready_done_mouse.frameNStart = frameN  # exact frame index
            ready_done_mouse.tStart = t  # local t and not account for scr refresh
            ready_done_mouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ready_done_mouse, 'tStartRefresh')  # time at next scr refresh
            ready_done_mouse.status = STARTED
            ready_done_mouse.mouseClock.reset()
            prevButtonState = ready_done_mouse.getPressed()  # if button is down already this ISN'T a new click
        if ready_done_mouse.status == STARTED:  # only update if started and not finished!
            buttons = ready_done_mouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    for obj in [button_L, button_R]:
                        if obj.contains(ready_done_mouse):
                            gotValidClick = True
                            ready_done_mouse.clicked_name.append(obj.name)
                    if gotValidClick:  # abort routine on response
                        continueRoutine = False

        # *ready_done* updates
        waitOnFlip = False
        if ready_done.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ready_done.frameNStart = frameN  # exact frame index
            ready_done.tStart = t  # local t and not account for scr refresh
            ready_done.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ready_done, 'tStartRefresh')  # time at next scr refresh
            ready_done.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(ready_done.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(ready_done.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if ready_done.status == STARTED and not waitOnFlip:
            theseKeys = ready_done.getKeys(keyList=['space'], waitRelease=False)
            _ready_done_allKeys.extend(theseKeys)
            if len(_ready_done_allKeys):
                ready_done.keys = _ready_done_allKeys[-1].name  # just the last key pressed
                ready_done.rt = _ready_done_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in readyComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "ready"-------
    for thisComponent in readyComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    blocks.addData('button_L.started', button_L.tStartRefresh)
    blocks.addData('button_L.stopped', button_L.tStopRefresh)
    blocks.addData('button_R.started', button_R.tStartRefresh)
    blocks.addData('button_R.stopped', button_R.tStopRefresh)
    # store data for blocks (TrialHandler)
    # the Routine "ready" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1, method='random',
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions("resources/"+conds_file),
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
        image_stim.setImage(stimImage)
        text_stim.setText(stimWord)
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # setup some python lists for storing info about the touch_resp
        touch_resp.x = []
        touch_resp.y = []
        touch_resp.leftButton = []
        touch_resp.midButton = []
        touch_resp.rightButton = []
        touch_resp.time = []
        touch_resp.clicked_name = []
        gotValidClick = False  # until a click is received
        trial_label_left.setText(label_left)
        trial_label_right.setText(label_right)
        # keep track of which components have finished
        trialComponents = [fixation, image_stim, text_stim, key_resp, touch_resp, button_left, trial_label_left, button_right, trial_label_right]
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

            # *fixation* updates
            if fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation.frameNStart = frameN  # exact frame index
                fixation.tStart = t  # local t and not account for scr refresh
                fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                fixation.setAutoDraw(True)
            if fixation.status == STARTED:
                # is it time to stop? (based on local clock)
                if tThisFlip > 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation.tStop = t  # not accounting for scr refresh
                    fixation.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(fixation, 'tStopRefresh')  # time at next scr refresh
                    fixation.setAutoDraw(False)

            # *image_stim* updates
            if image_stim.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                # keep track of start time/frame for later
                image_stim.frameNStart = frameN  # exact frame index
                image_stim.tStart = t  # local t and not account for scr refresh
                image_stim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(image_stim, 'tStartRefresh')  # time at next scr refresh
                image_stim.setAutoDraw(True)

            # *text_stim* updates
            if text_stim.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                # keep track of start time/frame for later
                text_stim.frameNStart = frameN  # exact frame index
                text_stim.tStart = t  # local t and not account for scr refresh
                text_stim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_stim, 'tStartRefresh')  # time at next scr refresh
                text_stim.setAutoDraw(True)

            # *key_resp* updates
            waitOnFlip = False
            if key_resp.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
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
                theseKeys = key_resp.getKeys(keyList=['a', 'l'], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    # was this correct?
                    if (key_resp.keys == str(CorrAns)) or (key_resp.keys == CorrAns):
                        key_resp.corr = 1
                    else:
                        key_resp.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            # *touch_resp* updates
            if touch_resp.status == NOT_STARTED and t >= 0.5-frameTolerance:
                # keep track of start time/frame for later
                touch_resp.frameNStart = frameN  # exact frame index
                touch_resp.tStart = t  # local t and not account for scr refresh
                touch_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(touch_resp, 'tStartRefresh')  # time at next scr refresh
                touch_resp.status = STARTED
                touch_resp.mouseClock.reset()
                prevButtonState = touch_resp.getPressed()  # if button is down already this ISN'T a new click
            if touch_resp.status == STARTED:  # only update if started and not finished!
                buttons = touch_resp.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        # check if the mouse was inside our 'clickable' objects
                        gotValidClick = False
                        for obj in [button_left, button_right]:
                            if obj.contains(touch_resp):
                                gotValidClick = True
                                touch_resp.clicked_name.append(obj.name)
                        x, y = touch_resp.getPos()
                        touch_resp.x.append(x)
                        touch_resp.y.append(y)
                        buttons = touch_resp.getPressed()
                        touch_resp.leftButton.append(buttons[0])
                        touch_resp.midButton.append(buttons[1])
                        touch_resp.rightButton.append(buttons[2])
                        touch_resp.time.append(touch_resp.mouseClock.getTime())
                        if gotValidClick:  # abort routine on response
                            continueRoutine = False

            # *button_left* updates
            if button_left.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                # keep track of start time/frame for later
                button_left.frameNStart = frameN  # exact frame index
                button_left.tStart = t  # local t and not account for scr refresh
                button_left.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(button_left, 'tStartRefresh')  # time at next scr refresh
                button_left.setAutoDraw(True)

            # *trial_label_left* updates
            if trial_label_left.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                # keep track of start time/frame for later
                trial_label_left.frameNStart = frameN  # exact frame index
                trial_label_left.tStart = t  # local t and not account for scr refresh
                trial_label_left.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trial_label_left, 'tStartRefresh')  # time at next scr refresh
                trial_label_left.setAutoDraw(True)

            # *button_right* updates
            if button_right.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                # keep track of start time/frame for later
                button_right.frameNStart = frameN  # exact frame index
                button_right.tStart = t  # local t and not account for scr refresh
                button_right.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(button_right, 'tStartRefresh')  # time at next scr refresh
                button_right.setAutoDraw(True)

            # *trial_label_right* updates
            if trial_label_right.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                # keep track of start time/frame for later
                trial_label_right.frameNStart = frameN  # exact frame index
                trial_label_right.tStart = t  # local t and not account for scr refresh
                trial_label_right.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trial_label_right, 'tStartRefresh')  # time at next scr refresh
                trial_label_right.setAutoDraw(True)

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
        trials.addData('fixation.started', fixation.tStartRefresh)
        trials.addData('fixation.stopped', fixation.tStopRefresh)
        trials.addData('image_stim.started', image_stim.tStartRefresh)
        trials.addData('image_stim.stopped', image_stim.tStopRefresh)
        trials.addData('text_stim.started', text_stim.tStartRefresh)
        trials.addData('text_stim.stopped', text_stim.tStopRefresh)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
            # was no response the correct answer?!
            if str(CorrAns).lower() == 'none':
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
        # store data for trials (TrialHandler)
        if len(touch_resp.x): trials.addData('touch_resp.x', touch_resp.x[0])
        if len(touch_resp.y): trials.addData('touch_resp.y', touch_resp.y[0])
        if len(touch_resp.leftButton): trials.addData('touch_resp.leftButton', touch_resp.leftButton[0])
        if len(touch_resp.midButton): trials.addData('touch_resp.midButton', touch_resp.midButton[0])
        if len(touch_resp.rightButton): trials.addData('touch_resp.rightButton', touch_resp.rightButton[0])
        if len(touch_resp.time): trials.addData('touch_resp.time', touch_resp.time[0])
        if len(touch_resp.clicked_name): trials.addData('touch_resp.clicked_name', touch_resp.clicked_name[0])
        trials.addData('touch_resp.started', touch_resp.tStart)
        trials.addData('touch_resp.stopped', touch_resp.tStop)
        # check if correct (either mouse or keyboard)
        if key_resp.keys:
            corr = key_resp.corr
            rt = key_resp.rt
        else:
            rt = touch_resp.time[0]  # annoyingly mouse is a list of rts
            if (('left' in touch_resp.clicked_name[0] and CorrAns=='a') or
                ('right' in touch_resp.clicked_name[0] and CorrAns=='l')):
                corr = 1
            else:
                corr = 0

        thisExp.addData('rt',  rt)
        thisExp.addData('corr', corr)
        trials.addData('button_left.started', button_left.tStartRefresh)
        trials.addData('button_left.stopped', button_left.tStopRefresh)
        trials.addData('button_right.started', button_right.tStartRefresh)
        trials.addData('button_right.stopped', button_right.tStopRefresh)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

        # ------Prepare to start Routine "feedback"-------
        continueRoutine = True
        routineTimer.add(1.000000)
        # update component parameters for each repeat

        if corr==0:
            msg="oops"
        else:
            msg="+"
        feedback_msg.setText(msg)
        # keep track of which components have finished
        feedbackComponents = [feedback_msg]
        for thisComponent in feedbackComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        feedbackClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1

        # -------Run Routine "feedback"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = feedbackClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=feedbackClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *feedback_msg* updates
            if feedback_msg.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                feedback_msg.frameNStart = frameN  # exact frame index
                feedback_msg.tStart = t  # local t and not account for scr refresh
                feedback_msg.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(feedback_msg, 'tStartRefresh')  # time at next scr refresh
                feedback_msg.setAutoDraw(True)
            if feedback_msg.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > feedback_msg.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    feedback_msg.tStop = t  # not accounting for scr refresh
                    feedback_msg.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(feedback_msg, 'tStopRefresh')  # time at next scr refresh
                    feedback_msg.setAutoDraw(False)

            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in feedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "feedback"-------
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.nextEntry()

    # completed 1 repeats of 'trials'

# completed 1 repeats of 'blocks'


# ------Prepare to start Routine "end_thanks"-------
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
end_thanksComponents = [thanks_text]
for thisComponent in end_thanksComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
end_thanksClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "end_thanks"-------
while continueRoutine:
    # get current time
    t = end_thanksClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=end_thanksClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *thanks_text* updates
    if thanks_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        thanks_text.frameNStart = frameN  # exact frame index
        thanks_text.tStart = t  # local t and not account for scr refresh
        thanks_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(thanks_text, 'tStartRefresh')  # time at next scr refresh
        thanks_text.setAutoDraw(True)

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in end_thanksComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end_thanks"-------
for thisComponent in end_thanksComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('thanks_text.started', thanks_text.tStartRefresh)
thisExp.addData('thanks_text.stopped', thanks_text.tStopRefresh)
# the Routine "end_thanks" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

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
