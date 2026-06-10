# Writing Distraction — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [writing-distraction](../../../psy-exp-designer/paradigms/writing-distraction.md)
> **Source**: [Pavlovia demos/writing_distraction](https://gitlab.pavlovia.org/demos/writing_distraction) · PsychoPy 2025.1.1

## Experiment Logic

The Writing Distraction Task is a dual-task paradigm that measures the effect of visual distraction on an ongoing typing task. Participants see a target word, type it letter by letter, experience a brief visual distractor at a predetermined letter position, continue typing to complete the word, then answer a yes/no probe question about the distractor. The experiment begins with an instruction screen ("instructions" routine) that explains all task phases. The participant presses the spacebar to begin, with the keyboard clock reset frame-accurately via `win.callOnFlip(start_resp.clock.reset)`.

The trial loop is driven by a condition file (`writing_distraction_task_example.csv`) loaded via `data.importConditions()` into a `TrialHandler2`. Each row defines one trial with four key columns: `this_word` (the target word to type), `n_distract` (the letter position at which the distractor appears), `distractor` (the image file name for the distractor), and `question` (the yes/no probe question about the distractor). Trials are shuffled randomly with `nReps=1.0`.

Each trial has four sequential routines. First, the "show_word" routine displays the target word at the top of the screen for 2 seconds, then reveals an editable `TextBox2` response field where the participant types the word one letter at a time. A per-frame code block monitors `len(response.text)` -- when the number of characters typed equals `n_distract`, the routine ends immediately (`continueRoutine = False`) and captures the typed prefix as `current_text = response.text`. The word stimulus auto-stops after 2 seconds using `tThisFlipGlobal > word.tStartRefresh + 2 - frameTolerance`.

Second, the "show_distractor" routine presents a visual distractor image for exactly 1 second. The image is loaded dynamically from the condition file column via `image.setImage(distractor)`. The routine uses non-slip timing (`while continueRoutine and routineTimer.getTime() < 1.0`) with frame-accurate onset and offset via `tThisFlipGlobal > image.tStartRefresh + 1.0 - frameTolerance`. The distractor appears abruptly regardless of what the participant is doing, simulating an unexpected interruption.

Third, the "continue_writing" routine allows the participant to finish typing the word. The previously typed prefix is displayed in an `existing_text` text box (non-editable, set via `existing_text.text = current_text` in Begin Routine code), and a new editable `full_response` text box is positioned adjacent for typing the remaining letters. This routine runs for a maximum of 5 seconds with non-slip timing (`while continueRoutine and routineTimer.getTime() < 5.0`). The completed word text is saved via `trials.addData('full_response.text', full_response.text)`.

Fourth, the "question_response" routine displays the yes/no question about the distractor (e.g., "Was the picture of an animal? Press Y or N"). A `keyboard.Keyboard` component begins listening for 'y' or 'n' key presses simultaneously with text onset, with frame-accurate clock reset via `win.callOnFlip(key_resp.clock.reset)`. The routine is response-terminated -- the first valid key press ends the routine, and the key name, RT, and duration are stored via `trials.addData()`. If no response is made, `key_resp.keys` is set to `None`.

There is no per-trial feedback or cumulative scoring. The experiment ends automatically after all trials complete, with no final thank-you screen. Per-trial data saved includes: the typed word prefix (`response.text`), the complete typed word (`full_response.text`), the question response key (`key_resp.keys`), reaction time (`key_resp.rt`), and key press duration (`key_resp.duration`). Routine-level start/stop timestamps are stored for each of the four trial sub-routines.

## Key Design Patterns

- `data.Routine()` objects for all four trial sub-routines (show_word, show_distractor, continue_writing, question_response) with structured lifecycle management (2025.1.1 style)
- `TrialHandler2` with `data.importConditions('writing_distraction_task_example.csv')` for CSV-driven trial parameterization with `method='random'`
- Per-frame monitoring of editable `TextBox2.text` length (`len(response.text) == n_distract`) to trigger the distractor at a precise letter position
- Cross-routine variable passing: `current_text` captured in "show_word" and consumed in "continue_writing" via `existing_text.text = current_text`
- Non-slip timing with `while continueRoutine and routineTimer.getTime() < duration` and post-routine `routineTimer.addTime(-duration)` for the distractor and continue-writing phases
- `keyboard.Keyboard` with `win.callOnFlip(key_resp.clock.reset)` and `win.callOnFlip(key_resp.clearEvents, eventType='keyboard')` for frame-accurate RT measurement
- Dynamic image loading via `image.setImage(distractor)` where `distractor` is a column from the condition file
- `deviceManager` with named keyboards (`start_resp`, `key_resp`) registered in `setupDevices()` and retrieved by device name (2025.1.1 pattern)
- Trial-level pause handling with `currentRoutine` parameter for dispatching messages during pause
- `globalClock='float'` format for convenient global time handling

## Code Example

Complete runnable PsychoPy code for the Writing Distraction task:

```python
# Source: writing_distraction (demos/writing_distraction)
# Project URL: https://gitlab.pavlovia.org/demos/writing_distraction
# Original file: writing_distraction_lastrun.py
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2025.1.1),
    on Wed  3 Sep 18:46:03 2025
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
psychopyVersion = '2025.1.1'
expName = 'writing_distraction'  # from the Builder filename that created this script
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
        originPath='/Users/Becca/Desktop/Demos/Writing Distraction/writing_distraction_lastrun.py',
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
            monitor='testMonitor', color=[0.7412, 0.4431, 0.0588], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0.7412, 0.4431, 0.0588]
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
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
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
    if deviceManager.getDevice('start_resp') is None:
        # initialise start_resp
        start_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='start_resp',
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
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
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
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
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
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
    instructtxt = visual.TextBox2(
         win, text='Welcome to the Writing Distraction Task.\n\nYou will see a word and type it one letter at a time.\n\nAt a certain letter, a picture will briefly appear.\n\nAfter finishing the word, you will answer a yes/no question about the picture.\n\nType carefully, keep going when the picture appears, and answer the question as accurately as you can.\n\nPress Space to begin.', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(1.5, 0.8), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='white', borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instructtxt',
         depth=0, autoLog=True,
    )
    start_resp = keyboard.Keyboard(deviceName='start_resp')
    
    # --- Initialize components for Routine "show_word" ---
    word = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.3), draggable=False,      letterHeight=0.1,
         size=(0.5, 0.5), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='word',
         depth=0, autoLog=True,
    )
    response = visual.TextBox2(
         win, text=None, placeholder=None, font='Arial',
         ori=0.0, pos=(0, -0.2), draggable=False,      letterHeight=0.05,
         size=(0.5, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='white', borderColor='white',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=True,
         name='response',
         depth=-1, autoLog=True,
    )
    
    # --- Initialize components for Routine "show_distractor" ---
    image = visual.ImageStim(
        win=win,
        name='image', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    
    # --- Initialize components for Routine "continue_writing" ---
    instruct = visual.TextBox2(
         win, text='Continue typing the word:', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.3), draggable=False,      letterHeight=0.05,
         size=(1, 0.5), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instruct',
         depth=0, autoLog=True,
    )
    existing_text = visual.TextBox2(
         win, text=None, placeholder=None, font='Arial',
         ori=0.0, pos=(-0.15, -0.2), draggable=False,      letterHeight=0.05,
         size=(0.3, 0.1), borderWidth=2.0,
         color=[0.0000, 0.0000, 0.0000], colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center-right',
         anchor='center', overflow='visible',
         fillColor='white', borderColor='white',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='existing_text',
         depth=-1, autoLog=True,
    )
    full_response = visual.TextBox2(
         win, text=None, placeholder=None, font='Arial',
         ori=0.0, pos=(0.15, -0.2), draggable=False,      letterHeight=0.05,
         size=(0.3, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center-left',
         anchor='center', overflow='visible',
         fillColor='white', borderColor='white',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=True,
         name='full_response',
         depth=-2, autoLog=True,
    )
    
    # --- Initialize components for Routine "question_response" ---
    this_question = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.3), draggable=False,      letterHeight=0.05,
         size=(1, 0.5), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='this_question',
         depth=0, autoLog=True,
    )
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
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
        components=[instructtxt, start_resp],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    instructtxt.reset()
    # create starting attributes for start_resp
    start_resp.keys = []
    start_resp.rt = []
    _start_resp_allKeys = []
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
        
        # *instructtxt* updates
        
        # if instructtxt is starting this frame...
        if instructtxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructtxt.frameNStart = frameN  # exact frame index
            instructtxt.tStart = t  # local t and not account for scr refresh
            instructtxt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructtxt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instructtxt.started')
            # update status
            instructtxt.status = STARTED
            instructtxt.setAutoDraw(True)
        
        # if instructtxt is active this frame...
        if instructtxt.status == STARTED:
            # update params
            pass
        
        # *start_resp* updates
        waitOnFlip = False
        
        # if start_resp is starting this frame...
        if start_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            start_resp.frameNStart = frameN  # exact frame index
            start_resp.tStart = t  # local t and not account for scr refresh
            start_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_resp.started')
            # update status
            start_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(start_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(start_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if start_resp.status == STARTED and not waitOnFlip:
            theseKeys = start_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _start_resp_allKeys.extend(theseKeys)
            if len(_start_resp_allKeys):
                start_resp.keys = _start_resp_allKeys[-1].name  # just the last key pressed
                start_resp.rt = _start_resp_allKeys[-1].rt
                start_resp.duration = _start_resp_allKeys[-1].duration
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
                timers=[routineTimer, globalClock], 
                currentRoutine=instructions,
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
    # check responses
    if start_resp.keys in ['', [], None]:  # No response was made
        start_resp.keys = None
    thisExp.addData('start_resp.keys',start_resp.keys)
    if start_resp.keys != None:  # we had a response
        thisExp.addData('start_resp.rt', start_resp.rt)
        thisExp.addData('start_resp.duration', start_resp.duration)
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
        trialList=data.importConditions('writing_distraction_task_example.csv'), 
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
        
        # --- Prepare to start Routine "show_word" ---
        # create an object to store info about Routine show_word
        show_word = data.Routine(
            name='show_word',
            components=[word, response],
        )
        show_word.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        word.reset()
        word.setText(this_word)
        response.reset()
        # store start times for show_word
        show_word.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        show_word.tStart = globalClock.getTime(format='float')
        show_word.status = STARTED
        thisExp.addData('show_word.started', show_word.tStart)
        show_word.maxDuration = None
        # keep track of which components have finished
        show_wordComponents = show_word.components
        for thisComponent in show_word.components:
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
        
        # --- Run Routine "show_word" ---
        show_word.forceEnded = routineForceEnded = not continueRoutine
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
            
            # *word* updates
            
            # if word is starting this frame...
            if word.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                word.frameNStart = frameN  # exact frame index
                word.tStart = t  # local t and not account for scr refresh
                word.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(word, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'word.started')
                # update status
                word.status = STARTED
                word.setAutoDraw(True)
            
            # if word is active this frame...
            if word.status == STARTED:
                # update params
                pass
            
            # if word is stopping this frame...
            if word.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > word.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    word.tStop = t  # not accounting for scr refresh
                    word.tStopRefresh = tThisFlipGlobal  # on global time
                    word.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'word.stopped')
                    # update status
                    word.status = FINISHED
                    word.setAutoDraw(False)
            
            # *response* updates
            
            # if response is starting this frame...
            if response.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
                # keep track of start time/frame for later
                response.frameNStart = frameN  # exact frame index
                response.tStart = t  # local t and not account for scr refresh
                response.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(response, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'response.started')
                # update status
                response.status = STARTED
                response.setAutoDraw(True)
            
            # if response is active this frame...
            if response.status == STARTED:
                # update params
                pass
            # Run 'Each Frame' code from code
            # end the routine when n_distract letters are typed
            if len(response.text) ==n_distract:
                continueRoutine = False
                current_text = response.text
            
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
                    currentRoutine=show_word,
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                show_word.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in show_word.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "show_word" ---
        for thisComponent in show_word.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for show_word
        show_word.tStop = globalClock.getTime(format='float')
        show_word.tStopRefresh = tThisFlipGlobal
        thisExp.addData('show_word.stopped', show_word.tStop)
        trials.addData('response.text',response.text)
        # the Routine "show_word" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "show_distractor" ---
        # create an object to store info about Routine show_distractor
        show_distractor = data.Routine(
            name='show_distractor',
            components=[image],
        )
        show_distractor.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        image.setImage(distractor)
        # store start times for show_distractor
        show_distractor.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        show_distractor.tStart = globalClock.getTime(format='float')
        show_distractor.status = STARTED
        thisExp.addData('show_distractor.started', show_distractor.tStart)
        show_distractor.maxDuration = None
        # keep track of which components have finished
        show_distractorComponents = show_distractor.components
        for thisComponent in show_distractor.components:
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
        
        # --- Run Routine "show_distractor" ---
        show_distractor.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *image* updates
            
            # if image is starting this frame...
            if image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                image.frameNStart = frameN  # exact frame index
                image.tStart = t  # local t and not account for scr refresh
                image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(image, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'image.started')
                # update status
                image.status = STARTED
                image.setAutoDraw(True)
            
            # if image is active this frame...
            if image.status == STARTED:
                # update params
                pass
            
            # if image is stopping this frame...
            if image.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > image.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    image.tStop = t  # not accounting for scr refresh
                    image.tStopRefresh = tThisFlipGlobal  # on global time
                    image.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'image.stopped')
                    # update status
                    image.status = FINISHED
                    image.setAutoDraw(False)
            
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
                    currentRoutine=show_distractor,
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                show_distractor.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in show_distractor.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "show_distractor" ---
        for thisComponent in show_distractor.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for show_distractor
        show_distractor.tStop = globalClock.getTime(format='float')
        show_distractor.tStopRefresh = tThisFlipGlobal
        thisExp.addData('show_distractor.stopped', show_distractor.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if show_distractor.maxDurationReached:
            routineTimer.addTime(-show_distractor.maxDuration)
        elif show_distractor.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        
        # --- Prepare to start Routine "continue_writing" ---
        # create an object to store info about Routine continue_writing
        continue_writing = data.Routine(
            name='continue_writing',
            components=[instruct, existing_text, full_response],
        )
        continue_writing.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        instruct.reset()
        existing_text.reset()
        full_response.reset()
        # Run 'Begin Routine' code from code_2
        existing_text.text = current_text
        # store start times for continue_writing
        continue_writing.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        continue_writing.tStart = globalClock.getTime(format='float')
        continue_writing.status = STARTED
        thisExp.addData('continue_writing.started', continue_writing.tStart)
        continue_writing.maxDuration = None
        # keep track of which components have finished
        continue_writingComponents = continue_writing.components
        for thisComponent in continue_writing.components:
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
        
        # --- Run Routine "continue_writing" ---
        continue_writing.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 5.0:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *instruct* updates
            
            # if instruct is starting this frame...
            if instruct.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instruct.frameNStart = frameN  # exact frame index
                instruct.tStart = t  # local t and not account for scr refresh
                instruct.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instruct, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instruct.started')
                # update status
                instruct.status = STARTED
                instruct.setAutoDraw(True)
            
            # if instruct is active this frame...
            if instruct.status == STARTED:
                # update params
                pass
            
            # if instruct is stopping this frame...
            if instruct.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > instruct.tStartRefresh + 5-frameTolerance:
                    # keep track of stop time/frame for later
                    instruct.tStop = t  # not accounting for scr refresh
                    instruct.tStopRefresh = tThisFlipGlobal  # on global time
                    instruct.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'instruct.stopped')
                    # update status
                    instruct.status = FINISHED
                    instruct.setAutoDraw(False)
            
            # *existing_text* updates
            
            # if existing_text is starting this frame...
            if existing_text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                existing_text.frameNStart = frameN  # exact frame index
                existing_text.tStart = t  # local t and not account for scr refresh
                existing_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(existing_text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'existing_text.started')
                # update status
                existing_text.status = STARTED
                existing_text.setAutoDraw(True)
            
            # if existing_text is active this frame...
            if existing_text.status == STARTED:
                # update params
                pass
            
            # if existing_text is stopping this frame...
            if existing_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > existing_text.tStartRefresh + 5-frameTolerance:
                    # keep track of stop time/frame for later
                    existing_text.tStop = t  # not accounting for scr refresh
                    existing_text.tStopRefresh = tThisFlipGlobal  # on global time
                    existing_text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'existing_text.stopped')
                    # update status
                    existing_text.status = FINISHED
                    existing_text.setAutoDraw(False)
            
            # *full_response* updates
            
            # if full_response is starting this frame...
            if full_response.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                full_response.frameNStart = frameN  # exact frame index
                full_response.tStart = t  # local t and not account for scr refresh
                full_response.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(full_response, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'full_response.started')
                # update status
                full_response.status = STARTED
                full_response.setAutoDraw(True)
            
            # if full_response is active this frame...
            if full_response.status == STARTED:
                # update params
                pass
            
            # if full_response is stopping this frame...
            if full_response.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > full_response.tStartRefresh + 5-frameTolerance:
                    # keep track of stop time/frame for later
                    full_response.tStop = t  # not accounting for scr refresh
                    full_response.tStopRefresh = tThisFlipGlobal  # on global time
                    full_response.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'full_response.stopped')
                    # update status
                    full_response.status = FINISHED
                    full_response.setAutoDraw(False)
            
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
                    currentRoutine=continue_writing,
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                continue_writing.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in continue_writing.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "continue_writing" ---
        for thisComponent in continue_writing.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for continue_writing
        continue_writing.tStop = globalClock.getTime(format='float')
        continue_writing.tStopRefresh = tThisFlipGlobal
        thisExp.addData('continue_writing.stopped', continue_writing.tStop)
        trials.addData('full_response.text',full_response.text)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if continue_writing.maxDurationReached:
            routineTimer.addTime(-continue_writing.maxDuration)
        elif continue_writing.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-5.000000)
        
        # --- Prepare to start Routine "question_response" ---
        # create an object to store info about Routine question_response
        question_response = data.Routine(
            name='question_response',
            components=[this_question, key_resp],
        )
        question_response.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        this_question.reset()
        this_question.setText(question + "\n Press Y or N")
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # store start times for question_response
        question_response.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        question_response.tStart = globalClock.getTime(format='float')
        question_response.status = STARTED
        thisExp.addData('question_response.started', question_response.tStart)
        question_response.maxDuration = None
        # keep track of which components have finished
        question_responseComponents = question_response.components
        for thisComponent in question_response.components:
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
        
        # --- Run Routine "question_response" ---
        question_response.forceEnded = routineForceEnded = not continueRoutine
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
            
            # *this_question* updates
            
            # if this_question is starting this frame...
            if this_question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                this_question.frameNStart = frameN  # exact frame index
                this_question.tStart = t  # local t and not account for scr refresh
                this_question.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(this_question, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'this_question.started')
                # update status
                this_question.status = STARTED
                this_question.setAutoDraw(True)
            
            # if this_question is active this frame...
            if this_question.status == STARTED:
                # update params
                pass
            
            # *key_resp* updates
            waitOnFlip = False
            
            # if key_resp is starting this frame...
            if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
                theseKeys = key_resp.getKeys(keyList=['y','n'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    key_resp.duration = _key_resp_allKeys[-1].duration
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
                    timers=[routineTimer, globalClock], 
                    currentRoutine=question_response,
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                question_response.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in question_response.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "question_response" ---
        for thisComponent in question_response.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for question_response
        question_response.tStop = globalClock.getTime(format='float')
        question_response.tStopRefresh = tThisFlipGlobal
        thisExp.addData('question_response.stopped', question_response.tStop)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
        trials.addData('key_resp.keys',key_resp.keys)
        if key_resp.keys != None:  # we had a response
            trials.addData('key_resp.rt', key_resp.rt)
            trials.addData('key_resp.duration', key_resp.duration)
        # the Routine "question_response" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
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
