# Priming — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [priming](../../../psy-exp-designer/paradigms/priming.md)
> **Source**: [Pavlovia demos/semantic_priming](https://gitlab.pavlovia.org/demos/semantic_priming) · PsychoPy 2025.1.0dev

## Experiment Logic

This is an **unmasked semantic priming** task using a **semantic relatedness judgment**. There is no masking of the prime -- the participant sees both words clearly and must decide whether they are semantically related.

**Trial structure.** Each trial begins with a jittered inter-trial interval (ITI) during which a fixation cross (`+`) is displayed for 0.5 seconds plus a uniformly random additional duration (0 to 1 second). The trial routine then starts with a brief 0.5-second blank period before the **prime word** appears. The prime is displayed for 1 full second, then disappears. After a 0.5-second gap (blank screen), the **target word** appears and remains on screen for 1 second. The stimulus onset asynchrony (SOA) from prime onset to target onset is 1.5 seconds. The target then disappears, and the question "Were those words related?" is shown along with two clickable buttons: YES (green) and NO (red). The participant clicks one of these buttons to respond.

**Prime-target relationship.** The prime-target relatedness is defined in a `conditions.csv` file with three columns: `Prime` (the prime word), `TargetWord` (the target word), and `Answer` (the correct response: `'yes'` for related pairs, `'no'` for unrelated pairs). Each row represents one trial, and trials are presented in random order with one repetition of the full list (`nReps=1.0`, `method='random'`). Both the prime and target are simple text stimuli rendered via PsychoPy's `TextBox2` component in white Arial font on a black background.

**Response collection.** The participant responds by clicking the YES or NO button with the mouse. Both buttons appear simultaneously at 3 seconds into the trial routine (1 second after target onset). Reaction time is measured from the moment the button is first clicked (`buttonClock.getTime()`, reset at button onset). The trial routine ends immediately upon a button click. Accuracy is determined by comparing the participant's response to the `Answer` column: if the participant clicks YES and `Answer == 'yes'`, or clicks NO and `Answer == 'no'`, the trial is scored as correct (`correct = 1`); otherwise incorrect (`correct = 0`). Both the response (`answer`: 'yes' or 'no') and RT are logged per trial.

**Feedback and flow.** After each trial, a 0.5-second feedback screen displays the word "Correct!" (in green, `#9acd32`) or "Incorrect" (in red, `#fa8072`) along with the response time in milliseconds. A success sound plays on correct trials but is silenced (volume set to 0) on incorrect trials. The experiment consists of an instructions screen with a START button, the trial loop, and a goodbye screen ("That is the end - goodbye!") displayed for 3 seconds. There are no practice trials in this implementation.

**No masking.** This task does not use forward or backward masking. The prime is presented supraliminally for a full second with a clearly visible duration, making this an unmasked priming paradigm. The task itself is a relatedness judgment rather than a lexical decision, meaning the prime-target relationship is the explicit focus of the participant's decision rather than an implicit manipulation.

## Key Design Patterns

- Builder-style component timing: Each stimulus component has a status cycle (NOT_STARTED -> STARTED -> FINISHED) driven by fixed onset delays relative to the routine timer, with offset determined by a fixed duration from onset.
- Button-based response with per-component clocks: YES and NO buttons each have their own `buttonClock` (reset via `win.callOnFlip`) for measuring reaction time independently of the routine timer.
- Condition file column-to-global mapping: TrialHandler2 imports `conditions.csv` and auto-maps columns (`Prime`, `TargetWord`, `Answer`) to global variables via `globals()[paramName] = thisTrial[paramName]`, making them directly accessible in the trial routine.
- Conditional feedback with auditory reward: Feedback color and sound volume are set dynamically in the "Begin Routine" code block based on the `correct` variable, with a success chime playing only on correct trials.
- Random ITI jitter: Fixation cross duration is `0.5 + random()` seconds, providing a variable inter-trial interval to prevent temporal expectation effects.
- Non-slip timing with frame tolerance: All timing checks use `frameTolerance = 0.001` seconds and compare against `tThisFlipGlobal` (the predicted time of the next screen flip), ensuring frame-accurate stimulus onsets.

## Code Example

Complete runnable PsychoPy code for Semantic Priming task:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2025.1.0dev149),
    on Wed Jan 15 13:49:44 2025
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Hochenberger R, Sogo H, Kastman E, Lindelov JK. (2019)
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195.
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED,
    RELEASED, FOREVER, priority
)

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
psychopyVersion = '2025.1.0dev149'
expName = 'semantic_priming'  # from the Builder filename that created this script
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
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
    # replace default participant ID
    if prefs.piloting['replaceParticipantID']:
        expInfo['participant'] = 'pilot'

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
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/Becca/Library/CloudStorage/GoogleDrive-becca@opensciencetools.org/Shared drives/Science/Pavlovia Demos/semantic_priming/semantic_priming_lastrun.py',
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
            winType='pyglet', allowGUI=True, allowStencil=True,
            monitor='testMonitor', color=[-1, -1, -1], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [-1, -1, -1]
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
    # create speaker 'sound_1'
    deviceManager.addDevice(
        deviceName='sound_1',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index='-1',
        resample='True',
        latencyClass=1,
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

    # --- Initialize components for Routine "instructions" ---
    instrtxt = visual.TextBox2(
         win, text='In this task you will see two words, one after the other. \n\nYour task is to decide if those two words are related or not. \n\nTry to be as FAST and ACCURATE as you can. ', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(1.5, 1), borderWidth=2.0,
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
    start_button = visual.ButtonStim(win,
        text='START', font='Arvo',
        pos=(0, -0.4),
        letterHeight=0.05,
        size=(0.3, 0.1),
        ori=0.0
        ,borderWidth=0.0,
        fillColor=[-0.2549, 0.2392, 0.2549], borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='start_button',
        depth=-1
    )
    start_button.buttonClock = core.Clock()

    # --- Initialize components for Routine "iti" ---
    cross_random_duration = visual.TextBox2(
         win, text='+', placeholder='Type here...', font='Arial',
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
         name='cross_random_duration',
         depth=0, autoLog=True,
    )

    # --- Initialize components for Routine "trial" ---
    word1 = visual.TextBox2(
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
         name='word1',
         depth=0, autoLog=True,
    )
    word2 = visual.TextBox2(
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
         name='word2',
         depth=-1, autoLog=True,
    )
    question = visual.TextBox2(
         win, text='Were those words related?', placeholder='Type here...', font='Arial',
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
         name='question',
         depth=-2, autoLog=True,
    )
    no = visual.ButtonStim(win,
        text='NO', font='Arvo',
        pos=(0, -0.35),
        letterHeight=0.05,
        size=(0.2, 0.1),
        ori=0.0
        ,borderWidth=0.0,
        fillColor=[0.9608, 0.0039, -0.1059], borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='no',
        depth=-3
    )
    no.buttonClock = core.Clock()
    yes = visual.ButtonStim(win,
        text='YES', font='Arvo',
        pos=(0, -0.2),
        letterHeight=0.05,
        size=(0.2, 0.1),
        ori=0.0
        ,borderWidth=0.0,
        fillColor=[0.2078, 0.6078, -0.6078], borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='yes',
        depth=-4
    )
    yes.buttonClock = core.Clock()

    # --- Initialize components for Routine "feedback" ---
    fbtxtbox = visual.TextBox2(
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
         name='fbtxtbox',
         depth=-1, autoLog=True,
    )
    sound_1 = sound.Sound(
        'A',
        secs=0.5,
        stereo=True,
        hamming=True,
        speaker='sound_1',    name='sound_1'
    )
    sound_1.setVolume(1.0)

    # --- Initialize components for Routine "goodbye" ---
    byetxt = visual.TextBox2(
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
         name='byetxt',
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

    # --- Prepare to start Routine "instructions" ---
    # create an object to store info about Routine instructions
    instructions = data.Routine(
        name='instructions',
        components=[instrtxt, start_button],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    instrtxt.reset()
    # reset start_button to account for continued clicks & clear times on/off
    start_button.reset()
    # store start times for instructions
    instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructions.tStart = globalClock.getTime(format='float')
    instructions.status = STARTED
    thisExp.addData('instructions.started', instructions.tStart)
    instructions.maxDuration = None
    # keep track of which components have finished
    instructionsComponents = instructions.components
    for thisComponent in instructions.components:
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

    # --- Run Routine "instructions" ---
    instructions.forceEnded = routineForceEnded = not continueRoutine
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
        # *start_button* updates

        # if start_button is starting this frame...
        if start_button.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            start_button.frameNStart = frameN  # exact frame index
            start_button.tStart = t  # local t and not account for scr refresh
            start_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_button, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_button.started')
            # update status
            start_button.status = STARTED
            win.callOnFlip(start_button.buttonClock.reset)
            start_button.setAutoDraw(True)

        # if start_button is active this frame...
        if start_button.status == STARTED:
            # update params
            pass
            # check whether start_button has been pressed
            if start_button.isClicked:
                if not start_button.wasClicked:
                    # if this is a new click, store time of first click and clicked until
                    start_button.timesOn.append(start_button.buttonClock.getTime())
                    start_button.timesOff.append(start_button.buttonClock.getTime())
                elif len(start_button.timesOff):
                    # if click is continuing from last frame, update time of clicked until
                    start_button.timesOff[-1] = start_button.buttonClock.getTime()
                if not start_button.wasClicked:
                    # end routine when start_button is clicked
                    continueRoutine = False
                if not start_button.wasClicked:
                    # run callback code when start_button is clicked
                    pass
        # take note of whether start_button was clicked, so that next frame we know if clicks are new
        start_button.wasClicked = start_button.isClicked and start_button.status == STARTED

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
                timers=[routineTimer, globalClock],
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            instructions.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "instructions" ---
    for thisComponent in instructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instructions
    instructions.tStop = globalClock.getTime(format='float')
    instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructions.stopped', instructions.tStop)
    thisExp.addData('start_button.numClicks', start_button.numClicks)
    if start_button.numClicks:
       thisExp.addData('start_button.timesOn', start_button.timesOn)
       thisExp.addData('start_button.timesOff', start_button.timesOff)
    else:
       thisExp.addData('start_button.timesOn', "")
       thisExp.addData('start_button.timesOff', "")
    thisExp.nextEntry()
    # the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler2(
        name='trials',
        nReps=1.0,
        method='random',
        extraInfo=expInfo,
        originPath=-1,
        trialList=data.importConditions('conditions.csv'),
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
        trials.status = STARTED
        if hasattr(thisTrial, 'status'):
            thisTrial.status = STARTED
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]

        # --- Prepare to start Routine "iti" ---
        # create an object to store info about Routine iti
        iti = data.Routine(
            name='iti',
            components=[cross_random_duration],
        )
        iti.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        cross_random_duration.reset()
        # store start times for iti
        iti.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        iti.tStart = globalClock.getTime(format='float')
        iti.status = STARTED
        thisExp.addData('iti.started', iti.tStart)
        iti.maxDuration = None
        # keep track of which components have finished
        itiComponents = iti.components
        for thisComponent in iti.components:
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

        # --- Run Routine "iti" ---
        iti.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *cross_random_duration* updates

            # if cross_random_duration is starting this frame...
            if cross_random_duration.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                cross_random_duration.frameNStart = frameN  # exact frame index
                cross_random_duration.tStart = t  # local t and not account for scr refresh
                cross_random_duration.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(cross_random_duration, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'cross_random_duration.started')
                # update status
                cross_random_duration.status = STARTED
                cross_random_duration.setAutoDraw(True)

            # if cross_random_duration is active this frame...
            if cross_random_duration.status == STARTED:
                # update params
                pass

            # if cross_random_duration is stopping this frame...
            if cross_random_duration.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > cross_random_duration.tStartRefresh + 0.5 + random()-frameTolerance:
                    # keep track of stop time/frame for later
                    cross_random_duration.tStop = t  # not accounting for scr refresh
                    cross_random_duration.tStopRefresh = tThisFlipGlobal  # on global time
                    cross_random_duration.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'cross_random_duration.stopped')
                    # update status
                    cross_random_duration.status = FINISHED
                    cross_random_duration.setAutoDraw(False)

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
                    timers=[routineTimer, globalClock],
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                iti.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in iti.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # --- Ending Routine "iti" ---
        for thisComponent in iti.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for iti
        iti.tStop = globalClock.getTime(format='float')
        iti.tStopRefresh = tThisFlipGlobal
        thisExp.addData('iti.stopped', iti.tStop)
        # the Routine "iti" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

        # --- Prepare to start Routine "trial" ---
        # create an object to store info about Routine trial
        trial = data.Routine(
            name='trial',
            components=[word1, word2, question, no, yes],
        )
        trial.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        word1.reset()
        word1.setText(Prime)
        word2.reset()
        word2.setText(TargetWord)
        question.reset()
        # reset no to account for continued clicks & clear times on/off
        no.reset()
        # reset yes to account for continued clicks & clear times on/off
        yes.reset()
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
        trial.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *word1* updates

            # if word1 is starting this frame...
            if word1.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                # keep track of start time/frame for later
                word1.frameNStart = frameN  # exact frame index
                word1.tStart = t  # local t and not account for scr refresh
                word1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(word1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'word1.started')
                # update status
                word1.status = STARTED
                word1.setAutoDraw(True)

            # if word1 is active this frame...
            if word1.status == STARTED:
                # update params
                pass

            # if word1 is stopping this frame...
            if word1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > word1.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    word1.tStop = t  # not accounting for scr refresh
                    word1.tStopRefresh = tThisFlipGlobal  # on global time
                    word1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'word1.stopped')
                    # update status
                    word1.status = FINISHED
                    word1.setAutoDraw(False)

            # *word2* updates

            # if word2 is starting this frame...
            if word2.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
                # keep track of start time/frame for later
                word2.frameNStart = frameN  # exact frame index
                word2.tStart = t  # local t and not account for scr refresh
                word2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(word2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'word2.started')
                # update status
                word2.status = STARTED
                word2.setAutoDraw(True)

            # if word2 is active this frame...
            if word2.status == STARTED:
                # update params
                pass

            # if word2 is stopping this frame...
            if word2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > word2.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    word2.tStop = t  # not accounting for scr refresh
                    word2.tStopRefresh = tThisFlipGlobal  # on global time
                    word2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'word2.stopped')
                    # update status
                    word2.status = FINISHED
                    word2.setAutoDraw(False)

            # *question* updates

            # if question is starting this frame...
            if question.status == NOT_STARTED and tThisFlip >= 3-frameTolerance:
                # keep track of start time/frame for later
                question.frameNStart = frameN  # exact frame index
                question.tStart = t  # local t and not account for scr refresh
                question.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(question, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'question.started')
                # update status
                question.status = STARTED
                question.setAutoDraw(True)

            # if question is active this frame...
            if question.status == STARTED:
                # update params
                pass
            # *no* updates

            # if no is starting this frame...
            if no.status == NOT_STARTED and tThisFlip >= 3-frameTolerance:
                # keep track of start time/frame for later
                no.frameNStart = frameN  # exact frame index
                no.tStart = t  # local t and not account for scr refresh
                no.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(no, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'no.started')
                # update status
                no.status = STARTED
                win.callOnFlip(no.buttonClock.reset)
                no.setAutoDraw(True)

            # if no is active this frame...
            if no.status == STARTED:
                # update params
                pass
                # check whether no has been pressed
                if no.isClicked:
                    if not no.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        no.timesOn.append(no.buttonClock.getTime())
                        no.timesOff.append(no.buttonClock.getTime())
                    elif len(no.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        no.timesOff[-1] = no.buttonClock.getTime()
                    if not no.wasClicked:
                        # end routine when no is clicked
                        continueRoutine = False
                    if not no.wasClicked:
                        # run callback code when no is clicked
                        thisExp.addData('answer', 'no')
                        rt = no.timesOn[0]
                        thisExp.addData('rt', rt)
                        if Answer == 'no':
                            correct = 1
                        else:
                            correct = 0
                        thisExp.addData('correct', correct)
            # take note of whether no was clicked, so that next frame we know if clicks are new
            no.wasClicked = no.isClicked and no.status == STARTED
            # *yes* updates

            # if yes is starting this frame...
            if yes.status == NOT_STARTED and tThisFlip >= 3-frameTolerance:
                # keep track of start time/frame for later
                yes.frameNStart = frameN  # exact frame index
                yes.tStart = t  # local t and not account for scr refresh
                yes.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(yes, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'yes.started')
                # update status
                yes.status = STARTED
                win.callOnFlip(yes.buttonClock.reset)
                yes.setAutoDraw(True)

            # if yes is active this frame...
            if yes.status == STARTED:
                # update params
                pass
                # check whether yes has been pressed
                if yes.isClicked:
                    if not yes.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        yes.timesOn.append(yes.buttonClock.getTime())
                        yes.timesOff.append(yes.buttonClock.getTime())
                    elif len(yes.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        yes.timesOff[-1] = yes.buttonClock.getTime()
                    if not yes.wasClicked:
                        # end routine when yes is clicked
                        continueRoutine = False
                    if not yes.wasClicked:
                        # run callback code when yes is clicked
                        thisExp.addData('answer', 'yes')
                        rt = yes.timesOn[0]
                        thisExp.addData('rt', rt)
                        if Answer == 'yes':
                            correct = 1
                        else:
                            correct = 0
                        thisExp.addData('correct', correct)
            # take note of whether yes was clicked, so that next frame we know if clicks are new
            yes.wasClicked = yes.isClicked and yes.status == STARTED

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
                    timers=[routineTimer, globalClock],
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
        trials.addData('no.numClicks', no.numClicks)
        if no.numClicks:
           trials.addData('no.timesOn', no.timesOn)
           trials.addData('no.timesOff', no.timesOff)
        else:
           trials.addData('no.timesOn', "")
           trials.addData('no.timesOff', "")
        trials.addData('yes.numClicks', yes.numClicks)
        if yes.numClicks:
           trials.addData('yes.timesOn', yes.timesOn)
           trials.addData('yes.timesOff', yes.timesOff)
        else:
           trials.addData('yes.timesOn', "")
           trials.addData('yes.timesOff', "")
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

        # --- Prepare to start Routine "feedback" ---
        # create an object to store info about Routine feedback
        feedback = data.Routine(
            name='feedback',
            components=[fbtxtbox, sound_1],
        )
        feedback.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code
        if correct:
            fbcol = '#9acd32'
            fbtxt = 'Correct!\nTime: '+str(int(rt*1000))+'ms'
            fbvol = 1
        else:
            fbcol = '#fa8072'
            fbtxt = 'Incorrect\nTime: '+str(int(rt*1000))+'ms'
            fbvol = 0
        fbtxtbox.reset()
        fbtxtbox.setColor(fbcol, colorSpace='rgb')
        fbtxtbox.setText(fbtxt)
        sound_1.setSound('sounds/short-success-sound-glockenspiel-treasure-video-game-6346.mp3', secs=0.5, hamming=True)
        sound_1.setVolume(fbvol, log=False)
        sound_1.seek(0)
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
        feedback.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.5:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *fbtxtbox* updates

            # if fbtxtbox is starting this frame...
            if fbtxtbox.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fbtxtbox.frameNStart = frameN  # exact frame index
                fbtxtbox.tStart = t  # local t and not account for scr refresh
                fbtxtbox.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fbtxtbox, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fbtxtbox.started')
                # update status
                fbtxtbox.status = STARTED
                fbtxtbox.setAutoDraw(True)

            # if fbtxtbox is active this frame...
            if fbtxtbox.status == STARTED:
                # update params
                pass

            # if fbtxtbox is stopping this frame...
            if fbtxtbox.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fbtxtbox.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    fbtxtbox.tStop = t  # not accounting for scr refresh
                    fbtxtbox.tStopRefresh = tThisFlipGlobal  # on global time
                    fbtxtbox.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fbtxtbox.stopped')
                    # update status
                    fbtxtbox.status = FINISHED
                    fbtxtbox.setAutoDraw(False)

            # *sound_1* updates

            # if sound_1 is starting this frame...
            if sound_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                sound_1.frameNStart = frameN  # exact frame index
                sound_1.tStart = t  # local t and not account for scr refresh
                sound_1.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('sound_1.started', tThisFlipGlobal)
                # update status
                sound_1.status = STARTED
                sound_1.play(when=win)  # sync with win flip

            # if sound_1 is stopping this frame...
            if sound_1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > sound_1.tStartRefresh + 0.5-frameTolerance or sound_1.isFinished:
                    # keep track of stop time/frame for later
                    sound_1.tStop = t  # not accounting for scr refresh
                    sound_1.tStopRefresh = tThisFlipGlobal  # on global time
                    sound_1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'sound_1.stopped')
                    # update status
                    sound_1.status = FINISHED
                    sound_1.stop()

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
                    timers=[routineTimer, globalClock],
                    playbackComponents=[sound_1]
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
        sound_1.pause()  # ensure sound has stopped at end of Routine
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if feedback.maxDurationReached:
            routineTimer.addTime(-feedback.maxDuration)
        elif feedback.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.500000)
        # mark thisTrial as finished
        if hasattr(thisTrial, 'status'):
            thisTrial.status = FINISHED
        # if awaiting a pause, pause now
        if trials.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp,
                win=win,
                timers=[globalClock],
            )
            # once done pausing, restore running status
            trials.status = STARTED
        thisExp.nextEntry()

    # completed 1.0 repeats of 'trials'
    trials.status = FINISHED

    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()

    # --- Prepare to start Routine "goodbye" ---
    # create an object to store info about Routine goodbye
    goodbye = data.Routine(
        name='goodbye',
        components=[byetxt],
    )
    goodbye.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    byetxt.reset()
    # store start times for goodbye
    goodbye.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    goodbye.tStart = globalClock.getTime(format='float')
    goodbye.status = STARTED
    thisExp.addData('goodbye.started', goodbye.tStart)
    goodbye.maxDuration = None
    # keep track of which components have finished
    goodbyeComponents = goodbye.components
    for thisComponent in goodbye.components:
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

    # --- Run Routine "goodbye" ---
    goodbye.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 3.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *byetxt* updates

        # if byetxt is starting this frame...
        if byetxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            byetxt.frameNStart = frameN  # exact frame index
            byetxt.tStart = t  # local t and not account for scr refresh
            byetxt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(byetxt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'byetxt.started')
            # update status
            byetxt.status = STARTED
            byetxt.setAutoDraw(True)

        # if byetxt is active this frame...
        if byetxt.status == STARTED:
            # update params
            pass

        # if byetxt is stopping this frame...
        if byetxt.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > byetxt.tStartRefresh + 3-frameTolerance:
                # keep track of stop time/frame for later
                byetxt.tStop = t  # not accounting for scr refresh
                byetxt.tStopRefresh = tThisFlipGlobal  # on global time
                byetxt.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'byetxt.stopped')
                # update status
                byetxt.status = FINISHED
                byetxt.setAutoDraw(False)

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
                timers=[routineTimer, globalClock],
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            goodbye.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in goodbye.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "goodbye" ---
    for thisComponent in goodbye.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for goodbye
    goodbye.tStop = globalClock.getTime(format='float')
    goodbye.tStopRefresh = tThisFlipGlobal
    thisExp.addData('goodbye.stopped', goodbye.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if goodbye.maxDurationReached:
        routineTimer.addTime(-goodbye.maxDuration)
    elif goodbye.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-3.000000)
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
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
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
