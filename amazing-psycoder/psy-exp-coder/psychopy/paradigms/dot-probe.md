# Dot-Probe — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [dot-probe](../../../psy-exp-designer/paradigms/dot-probe.md)
> **Source**: [Pavlovia demos/dot_probe](https://gitlab.pavlovia.org/demos/dot_probe) · PsychoPy 2024.2.4

## Experiment Logic

The experiment measures attentional bias toward emotional stimuli using the dot-probe paradigm with words instead of faces. Participants view vertically-arranged word pairs (one emotional, one neutral) followed by an arrow probe that replaces one of the two positions, and must indicate the arrow's direction as quickly as possible.

Each trial begins with a central fixation cross (`+++`) displayed for 500 ms. After a 500 ms blank gap, the stimulus pair appears: the `top_word` is presented at screen position (0, 0.1) and the `bottom_word` at (0, -0.1), both in white Arial text using PsychoPy `TextBox2` components. The two words remain visible for exactly 500 ms (stimulus onset asynchrony of 500 ms), then both disappear simultaneously as the probe arrow appears.

The probe is a single character — either `<` (left-pointing arrow) or `>` (right-pointing arrow) — displayed at either the top position (0, 0.1) or the bottom position (0, -0.1), as determined by the `cue_y` condition parameter. The trial is **congruent** (valid) when the probe replaces the emotional word's location, meaning attention was already directed there. It is **incongruent** (invalid) when the probe replaces the neutral word's location, requiring a shift of attention. This validity manipulation is the core mechanism for measuring attentional bias.

Participants respond using the keyboard: the **`z` key** for a left-pointing arrow (`<`) and the **`m` key** for a right-pointing arrow (`>`). A `Keyboard` device (PTB backend) captures the response with the clock reset synchronized to the probe onset flip via `win.callOnFlip()`. The response ends the trial immediately, and a 500 ms feedback screen displays "Correct!" in green or "Incorrect" in red. Reaction times and accuracy are logged per trial.

The attentional bias score is computed post-hoc as the difference in mean correct RT between incongruent and congruent trials: **bias = RT_incongruent - RT_congruent**. A positive bias indicates vigilance toward emotional stimuli (faster to detect the probe when it replaces the emotional word), while a negative bias indicates avoidance. The condition file (`conditions.xlsx`) controls all trial parameters including word content, emotional/neutral status, probe position, probe direction, and the correct answer — making the experiment fully reconfigurable without code changes.

## Key Design Patterns

- **Condition-driven trial generation**: All trial parameters (`top_text`, `bottom_text`, `cue_y`, `this_probe`, `answer`) are loaded from `conditions.xlsx` via `TrialHandler2` with sequential presentation (`nReps=1`). This separates experimental design from code completely.
- **Vertical stimulus arrangement**: Unlike the classic left-right dot-probe, stimuli are arranged top/bottom with the probe's y-coordinate (`cue_y`) determining whether it replaces the top word (0.1) or bottom word (-0.1). Congruency is encoded implicitly by pairing `cue_y` with the emotional word's position in the condition file.
- **Non-slip sequential timing with state machines**: Each routine component transitions through NOT_STARTED, STARTED, and FINISHED states driven by frame-accurate `tThisFlipGlobal` comparisons. Fixation (0-500ms), stimulus pair (1000-1500ms), and probe (1500ms onward) use offset-based durations rather than Builder's built-in timing components.
- **`globals()` injection of condition variables**: Condition column names are injected into the global namespace (`globals()[paramName] = thisTrial[paramName]`), allowing direct variable-name references throughout the trial code (e.g., `top_text` rather than `thisTrial['top_text']`).
- **RT measurement via `callOnFlip`**: The `key_resp` Keyboard clock is reset via `win.callOnFlip(key_resp.clock.reset)` synchronized to the probe onset screen flip, ensuring frame-accurate reaction time measurement.
- **Feedback with Begin Routine code**: A custom code block at the start of the feedback routine inspects `key_resp.corr` and dynamically sets both the text content and text color — green for correct, red for incorrect — before drawing.

## Code Example

Complete runnable PsychoPy code for Dot-Probe task:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on Mon Dec 30 12:07:50 2024
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
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'dot_probe'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1440, 900]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/Becca/Library/CloudStorage/GoogleDrive-becca@opensciencetools.org/Shared drives/Science/Pavlovia Demos/dot-probe/dot_probe_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=True,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ptb'
        )
    if deviceManager.getDevice('instr_resp') is None:
        # initialise instr_resp
        instr_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='instr_resp',
        )
    if deviceManager.getDevice('instr_resp_2') is None:
        # initialise instr_resp_2
        instr_resp_2 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='instr_resp_2',
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='PsychToolbox',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='PsychToolbox'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "instructions1" ---
    instrtxt = visual.TextBox2(
         win, text='In this task you will see some crosses int he middle of the screen like this.\n\n+++ \n\nTry to keep your eyes on the fixation crosses. \n\nPress space to continue', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(1, 1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instrtxt',
         depth=0, autoLog=True,
    )
    instr_resp = keyboard.Keyboard(deviceName='instr_resp')
    
    # --- Initialize components for Routine "instructions2" ---
    instrtxt_2 = visual.TextBox2(
         win, text='You will then briefly see two words like this:\n\nCAT\n\nDOG\n\nOne of the words will be followed by an arrow facing left ( < ) or right ( > ). Use the Z and M keys on your keyboard to identify the direction the arrow faces:\n\n< = press the Z key. \n> = press the M key.  \n\nPress space to start', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(1, 1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instrtxt_2',
         depth=0, autoLog=True,
    )
    instr_resp_2 = keyboard.Keyboard(deviceName='instr_resp_2')
    
    # --- Initialize components for Routine "trial" ---
    fixation = visual.TextBox2(
         win, text='+++', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(0.5, 0.5), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='fixation',
         depth=0, autoLog=True,
    )
    top_word = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.1), draggable=False,      letterHeight=0.05,
         size=(0.3, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='top_word',
         depth=-1, autoLog=True,
    )
    bottom_word = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, -0.1), draggable=False,      letterHeight=0.05,
         size=(0.3, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='bottom_word',
         depth=-2, autoLog=True,
    )
    probe = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=[0,0], draggable=False,      letterHeight=0.05,
         size=(0.2, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='probe',
         depth=-3, autoLog=True,
    )
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
    # --- Initialize components for Routine "feedback" ---
    textbox = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(0.5, 0.5), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='textbox',
         depth=-1, autoLog=True,
    )
    
    # --- Initialize components for Routine "bye" ---
    bye_txt = visual.TextBox2(
         win, text='That is the end - goodbye!', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(0.5, 0.5), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='bye_txt',
         depth=0, autoLog=True,
    )
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "instructions1" ---
    # create an object to store info about Routine instructions1
    instructions1 = data.Routine(
        name='instructions1',
        components=[instrtxt, instr_resp],
    )
    instructions1.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    instrtxt.reset()
    # create starting attributes for instr_resp
    instr_resp.keys = []
    instr_resp.rt = []
    _instr_resp_allKeys = []
    # store start times for instructions1
    instructions1.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructions1.tStart = globalClock.getTime(format='float')
    instructions1.status = STARTED
    thisExp.addData('instructions1.started', instructions1.tStart)
    instructions1.maxDuration = None
    # keep track of which components have finished
    instructions1Components = instructions1.components
    for thisComponent in instructions1.components:
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
    
    # --- Run Routine "instructions1" ---
    instructions1.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instrtxt* updates
        
        # if instrtxt is starting this frame...
        if instrtxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instrtxt.frameNStart = frameN  # exact frame index
            instrtxt.tStart = t  # local t and not account for scr refresh
            instrtxt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instrtxt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instrtxt.started')
            # update status
            instrtxt.status = STARTED
            instrtxt.setAutoDraw(True)
        
        # if instrtxt is active this frame...
        if instrtxt.status == STARTED:
            # update params
            pass
        
        # *instr_resp* updates
        waitOnFlip = False
        
        # if instr_resp is starting this frame...
        if instr_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instr_resp.frameNStart = frameN  # exact frame index
            instr_resp.tStart = t  # local t and not account for scr refresh
            instr_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instr_resp.started')
            # update status
            instr_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(instr_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(instr_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if instr_resp.status == STARTED and not waitOnFlip:
            theseKeys = instr_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _instr_resp_allKeys.extend(theseKeys)
            if len(_instr_resp_allKeys):
                instr_resp.keys = _instr_resp_allKeys[-1].name  # just the last key pressed
                instr_resp.rt = _instr_resp_allKeys[-1].rt
                instr_resp.duration = _instr_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            instructions1.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructions1.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructions1" ---
    for thisComponent in instructions1.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instructions1
    instructions1.tStop = globalClock.getTime(format='float')
    instructions1.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructions1.stopped', instructions1.tStop)
    # check responses
    if instr_resp.keys in ['', [], None]:  # No response was made
        instr_resp.keys = None
    thisExp.addData('instr_resp.keys',instr_resp.keys)
    if instr_resp.keys != None:  # we had a response
        thisExp.addData('instr_resp.rt', instr_resp.rt)
        thisExp.addData('instr_resp.duration', instr_resp.duration)
    thisExp.nextEntry()
    # the Routine "instructions1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "instructions2" ---
    # create an object to store info about Routine instructions2
    instructions2 = data.Routine(
        name='instructions2',
        components=[instrtxt_2, instr_resp_2],
    )
    instructions2.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    instrtxt_2.reset()
    # create starting attributes for instr_resp_2
    instr_resp_2.keys = []
    instr_resp_2.rt = []
    _instr_resp_2_allKeys = []
    # store start times for instructions2
    instructions2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructions2.tStart = globalClock.getTime(format='float')
    instructions2.status = STARTED
    thisExp.addData('instructions2.started', instructions2.tStart)
    instructions2.maxDuration = None
    # keep track of which components have finished
    instructions2Components = instructions2.components
    for thisComponent in instructions2.components:
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
    
    # --- Run Routine "instructions2" ---
    instructions2.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instrtxt_2* updates
        
        # if instrtxt_2 is starting this frame...
        if instrtxt_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instrtxt_2.frameNStart = frameN  # exact frame index
            instrtxt_2.tStart = t  # local t and not account for scr refresh
            instrtxt_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instrtxt_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instrtxt_2.started')
            # update status
            instrtxt_2.status = STARTED
            instrtxt_2.setAutoDraw(True)
        
        # if instrtxt_2 is active this frame...
        if instrtxt_2.status == STARTED:
            # update params
            pass
        
        # *instr_resp_2* updates
        waitOnFlip = False
        
        # if instr_resp_2 is starting this frame...
        if instr_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instr_resp_2.frameNStart = frameN  # exact frame index
            instr_resp_2.tStart = t  # local t and not account for scr refresh
            instr_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_resp_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instr_resp_2.started')
            # update status
            instr_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(instr_resp_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(instr_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if instr_resp_2.status == STARTED and not waitOnFlip:
            theseKeys = instr_resp_2.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _instr_resp_2_allKeys.extend(theseKeys)
            if len(_instr_resp_2_allKeys):
                instr_resp_2.keys = _instr_resp_2_allKeys[-1].name  # just the last key pressed
                instr_resp_2.rt = _instr_resp_2_allKeys[-1].rt
                instr_resp_2.duration = _instr_resp_2_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            instructions2.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructions2.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructions2" ---
    for thisComponent in instructions2.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instructions2
    instructions2.tStop = globalClock.getTime(format='float')
    instructions2.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructions2.stopped', instructions2.tStop)
    # check responses
    if instr_resp_2.keys in ['', [], None]:  # No response was made
        instr_resp_2.keys = None
    thisExp.addData('instr_resp_2.keys',instr_resp_2.keys)
    if instr_resp_2.keys != None:  # we had a response
        thisExp.addData('instr_resp_2.rt', instr_resp_2.rt)
        thisExp.addData('instr_resp_2.duration', instr_resp_2.duration)
    thisExp.nextEntry()
    # the Routine "instructions2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler2(
        name='trials',
        nReps=1.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('conditions.xlsx'), 
        seed=None, 
    )
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisTrial in trials:
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        # --- Prepare to start Routine "trial" ---
        # create an object to store info about Routine trial
        trial = data.Routine(
            name='trial',
            components=[fixation, top_word, bottom_word, probe, key_resp],
        )
        trial.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        fixation.reset()
        top_word.reset()
        top_word.setText(top_text)
        bottom_word.reset()
        bottom_word.setText(bottom_text)
        probe.reset()
        probe.setPos((0, cue_y))
        probe.setText(this_probe)
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # store start times for trial
        trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        trial.tStart = globalClock.getTime(format='float')
        trial.status = STARTED
        thisExp.addData('trial.started', trial.tStart)
        trial.maxDuration = None
        # keep track of which components have finished
        trialComponents = trial.components
        for thisComponent in trial.components:
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
        
        # --- Run Routine "trial" ---
        # if trial has changed, end Routine now
        if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
            continueRoutine = False
        trial.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation* updates
            
            # if fixation is starting this frame...
            if fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation.frameNStart = frameN  # exact frame index
                fixation.tStart = t  # local t and not account for scr refresh
                fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation.started')
                # update status
                fixation.status = STARTED
                fixation.setAutoDraw(True)
            
            # if fixation is active this frame...
            if fixation.status == STARTED:
                # update params
                pass
            
            # if fixation is stopping this frame...
            if fixation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation.tStop = t  # not accounting for scr refresh
                    fixation.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation.stopped')
                    # update status
                    fixation.status = FINISHED
                    fixation.setAutoDraw(False)
            
            # *top_word* updates
            
            # if top_word is starting this frame...
            if top_word.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                top_word.frameNStart = frameN  # exact frame index
                top_word.tStart = t  # local t and not account for scr refresh
                top_word.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(top_word, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'top_word.started')
                # update status
                top_word.status = STARTED
                top_word.setAutoDraw(True)
            
            # if top_word is active this frame...
            if top_word.status == STARTED:
                # update params
                pass
            
            # if top_word is stopping this frame...
            if top_word.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > top_word.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    top_word.tStop = t  # not accounting for scr refresh
                    top_word.tStopRefresh = tThisFlipGlobal  # on global time
                    top_word.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'top_word.stopped')
                    # update status
                    top_word.status = FINISHED
                    top_word.setAutoDraw(False)
            
            # *bottom_word* updates
            
            # if bottom_word is starting this frame...
            if bottom_word.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                bottom_word.frameNStart = frameN  # exact frame index
                bottom_word.tStart = t  # local t and not account for scr refresh
                bottom_word.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(bottom_word, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'bottom_word.started')
                # update status
                bottom_word.status = STARTED
                bottom_word.setAutoDraw(True)
            
            # if bottom_word is active this frame...
            if bottom_word.status == STARTED:
                # update params
                pass
            
            # if bottom_word is stopping this frame...
            if bottom_word.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > bottom_word.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    bottom_word.tStop = t  # not accounting for scr refresh
                    bottom_word.tStopRefresh = tThisFlipGlobal  # on global time
                    bottom_word.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'bottom_word.stopped')
                    # update status
                    bottom_word.status = FINISHED
                    bottom_word.setAutoDraw(False)
            
            # *probe* updates
            
            # if probe is starting this frame...
            if probe.status == NOT_STARTED and tThisFlip >= 1.5-frameTolerance:
                # keep track of start time/frame for later
                probe.frameNStart = frameN  # exact frame index
                probe.tStart = t  # local t and not account for scr refresh
                probe.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(probe, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'probe.started')
                # update status
                probe.status = STARTED
                probe.setAutoDraw(True)
            
            # if probe is active this frame...
            if probe.status == STARTED:
                # update params
                pass
            
            # *key_resp* updates
            waitOnFlip = False
            
            # if key_resp is starting this frame...
            if key_resp.status == NOT_STARTED and tThisFlip >= 1.5-frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp.started')
                # update status
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['z', 'm'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    key_resp.duration = _key_resp_allKeys[-1].duration
                    # was this correct?
                    if (key_resp.keys == str(answer)) or (key_resp.keys == answer):
                        key_resp.corr = 1
                    else:
                        key_resp.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                trial.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trial.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial" ---
        for thisComponent in trial.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for trial
        trial.tStop = globalClock.getTime(format='float')
        trial.tStopRefresh = tThisFlipGlobal
        thisExp.addData('trial.stopped', trial.tStop)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
            # was no response the correct answer?!
            if str(answer).lower() == 'none':
               key_resp.corr = 1;  # correct non-response
            else:
               key_resp.corr = 0;  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('key_resp.keys',key_resp.keys)
        trials.addData('key_resp.corr', key_resp.corr)
        if key_resp.keys != None:  # we had a response
            trials.addData('key_resp.rt', key_resp.rt)
            trials.addData('key_resp.duration', key_resp.duration)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "feedback" ---
        # create an object to store info about Routine feedback
        feedback = data.Routine(
            name='feedback',
            components=[textbox],
        )
        feedback.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from fbcode
        if key_resp.corr == 1:
            fbtxt = "Correct!"
            fbcol = "Green"
        else:
            fbtxt = "Incorrect"
            fbcol = "Red"
        textbox.reset()
        textbox.setColor(fbcol, colorSpace='rgb')
        textbox.setText(fbtxt)
        # store start times for feedback
        feedback.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        feedback.tStart = globalClock.getTime(format='float')
        feedback.status = STARTED
        thisExp.addData('feedback.started', feedback.tStart)
        feedback.maxDuration = None
        # keep track of which components have finished
        feedbackComponents = feedback.components
        for thisComponent in feedback.components:
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
        
        # --- Run Routine "feedback" ---
        # if trial has changed, end Routine now
        if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
            continueRoutine = False
        feedback.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *textbox* updates
            
            # if textbox is starting this frame...
            if textbox.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                textbox.frameNStart = frameN  # exact frame index
                textbox.tStart = t  # local t and not account for scr refresh
                textbox.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(textbox, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'textbox.started')
                # update status
                textbox.status = STARTED
                textbox.setAutoDraw(True)
            
            # if textbox is active this frame...
            if textbox.status == STARTED:
                # update params
                pass
            
            # if textbox is stopping this frame...
            if textbox.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > textbox.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    textbox.tStop = t  # not accounting for scr refresh
                    textbox.tStopRefresh = tThisFlipGlobal  # on global time
                    textbox.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'textbox.stopped')
                    # update status
                    textbox.status = FINISHED
                    textbox.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                feedback.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in feedback.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "feedback" ---
        for thisComponent in feedback.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for feedback
        feedback.tStop = globalClock.getTime(format='float')
        feedback.tStopRefresh = tThisFlipGlobal
        thisExp.addData('feedback.stopped', feedback.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if feedback.maxDurationReached:
            routineTimer.addTime(-feedback.maxDuration)
        elif feedback.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.500000)
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'trials'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "bye" ---
    # create an object to store info about Routine bye
    bye = data.Routine(
        name='bye',
        components=[bye_txt],
    )
    bye.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    bye_txt.reset()
    # store start times for bye
    bye.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    bye.tStart = globalClock.getTime(format='float')
    bye.status = STARTED
    thisExp.addData('bye.started', bye.tStart)
    bye.maxDuration = None
    # keep track of which components have finished
    byeComponents = bye.components
    for thisComponent in bye.components:
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
    
    # --- Run Routine "bye" ---
    bye.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 2.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *bye_txt* updates
        
        # if bye_txt is starting this frame...
        if bye_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            bye_txt.frameNStart = frameN  # exact frame index
            bye_txt.tStart = t  # local t and not account for scr refresh
            bye_txt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(bye_txt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'bye_txt.started')
            # update status
            bye_txt.status = STARTED
            bye_txt.setAutoDraw(True)
        
        # if bye_txt is active this frame...
        if bye_txt.status == STARTED:
            # update params
            pass
        
        # if bye_txt is stopping this frame...
        if bye_txt.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > bye_txt.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                bye_txt.tStop = t  # not accounting for scr refresh
                bye_txt.tStopRefresh = tThisFlipGlobal  # on global time
                bye_txt.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'bye_txt.stopped')
                # update status
                bye_txt.status = FINISHED
                bye_txt.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            bye.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in bye.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "bye" ---
    for thisComponent in bye.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for bye
    bye.tStop = globalClock.getTime(format='float')
    bye.tStopRefresh = tThisFlipGlobal
    thisExp.addData('bye.stopped', bye.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if bye.maxDurationReached:
        routineTimer.addTime(-bye.maxDuration)
    elif bye.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-2.000000)
    thisExp.nextEntry()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
```
