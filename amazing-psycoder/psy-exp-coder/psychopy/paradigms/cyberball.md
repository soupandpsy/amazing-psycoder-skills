# Cyberball

**Config reference**: [cyberball](../../../psy-exp-designer/paradigms/cyberball.md)
**Source:** [Pavlovia cyberball demo](https://gitlab.pavlovia.org/demos/cyberball) (PsychoPy 2025.1.0dev167)

## Experiment Logic

The Cyberball task is a virtual ball-tossing game designed to study social exclusion and ostracism. Participants are led to believe they are playing catch with two other participants over the internet, but in reality, the other players are computer-controlled. The experiment measures how participants respond to being included or excluded from social interaction, making it a powerful tool for studying social pain, belonging, and rejection sensitivity.

The experiment begins with an instructions screen explaining the game rules: three players are shown on screen (the participant at the bottom center, plus two virtual players at the top left and right), and the participant should click on the player they want to throw the ball to when they receive it. A "START" button (using `visual.ButtonStim`) advances past the instructions. Player images are displayed using `visual.ImageStim`, and the ball is represented by a separate ball image. A `visual.TextBox2` component displays instructional text during each trial based on the `instruct` column from the conditions file.

The main experiment uses a single `trials` loop (`data.TrialHandler2`) with 5 repetitions and conditions loaded from `spreadsheets/equal_throws.xlsx`. The conditions file contains columns: `ball_start_x`, `ball_start_y`, `instruct`, `ball_from`, and `ball_to`. Each trial consists of two routines: a **trial** routine where the participant may need to throw the ball (when `ball_to == "choose"`), and a **ball_move** routine that animates the ball's journey. If `ball_to` is not "choose" (meaning another player is already specified as the target), the trial routine ends after 1 second without requiring a participant response.

In the trial routine, the ball is positioned at `(ball_start_x, ball_start_y)` based on the conditions data, and the participant sees three players plus the ball. Mouse responses are collected using `event.Mouse` with `prevButtonState` debouncing: each frame checks whether the button state has changed and, if a new click is detected, verifies whether the mouse position falls within either `player1image` or `player2image` using `obj.contains(mouse)`. Clickable objects are gathered via `environmenttools.getFromNames([player1image, player2image], namespace=locals())`. When a valid click is recorded, the routine ends.

After the trial routine, End Routine code in the `set_paths` code component determines the `end_pos` (target coordinates for the ball animation) and `outcome_txt` (feedback text like "You chose Player 1" or "Player 2 chose you"). The logic handles five cases: participant choosing (`ball_to == "choose"`), other players throwing to each other (`ball_to == "player1"` or `"player2"`), or other players throwing to the participant (`ball_to == "player3"`). The ball_move routine then runs a 3-second animation where the ball's position is updated each frame using linear interpolation: `x = start_pos[0] + ((end_pos[0] - start_pos[0]) / total_time) * t` and `y = start_pos[1] + ((end_pos[1] - start_pos[1]) / total_time) * t`. An `instructtxtbox_2` displays the outcome text throughout the animation. The experiment concludes after all 5 repetitions of the trials loop, with data saved via `saveAsWideText` and `saveAsPickle`.

## Key Design Patterns

- **Modular function-based experiment structure:** The experiment is organized into discrete functions (`showExpInfoDlg`, `setupData`, `setupLogging`, `setupWindow`, `setupDevices`, `pauseExperiment`, `run`, `saveData`, `endExperiment`, `quit`), each handling a specific aspect of the experiment lifecycle. The `run` function contains all trial presentation logic.
- **`data.Routine` objects for timeline tracking:** Each routine (instructions, trial, ball_move) is wrapped in a `data.Routine` object that stores start/stop times, component lists, and status. This modern PsychoPy pattern (v2025+) replaces older inline timing management.
- **Animated ball movement via per-frame position updates:** In the ball_move routine, the ball's position is recalculated every frame using linear interpolation between start and end positions over 3 seconds. This creates smooth animated motion without relying on pre-built animation components.
- **Mouse click detection with button state debouncing:** Uses `event.Mouse` with `prevButtonState = mouse.getPressed()` at mouse start, comparing against current button state each frame. Only new clicks (`buttons != prevButtonState` and `sum(buttons) > 0`) are processed, preventing repeated detections. Valid clicks must fall within clickable objects as determined by `obj.contains(mouse)`.
- **Condition-driven trial behavior:** The same trial routine handles both active participant throws (`ball_to == "choose"`) and passive observation trials (`ball_to != "choose"`) by checking the condition variable. The End Routine `set_paths` code resolves the ball's destination and feedback text based on all combinations of `ball_from` and `ball_to` values.
- **Pilot mode support via `core.setPilotModeFromArgs()`:** When running with `--pilot` flag, window settings are adjusted (forced windowed mode, custom size), logging levels are modified, and the participant ID is replaced with 'pilot'. A visual indicator is shown on screen if configured.

## Code Example

```python
# Source: cyberball (demos/cyberball)
# Project URL: https://gitlab.pavlovia.org/demos/cyberball
# Original file: cyberball.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2025.1.0dev167),
    on Mon Jan 20 16:24:28 2025
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
psychopyVersion = '2025.1.0dev167'
expName = 'cyberball'  # from the Builder filename that created this script
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
        originPath='/Users/Becca/Library/CloudStorage/GoogleDrive-becca@opensciencetools.org/Shared drives/Science/Pavlovia Demos/cyberball/cyberball.py',
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
            monitor='testMonitor', color=[1, 1, 1], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [1, 1, 1]
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
    instructtxt = visual.TextBox2(
         win, text='Thank you for participating! In this task, you\'ll play a virtual ball-tossing game with two other players. Here\'s what to do:\n\nGame Start: You\'ll see three players, including yourself.\nThrow the Ball: When you get the ball, click on a player to throw it to them.\n\nGameplay: Watch as the ball is tossed. You may receive it often or not at all at times.\n\nDuration: The game lasts a few minutes, followed by a short questionnaire.\n\nNote: The game simulates social interactions. Please focus on tossing and catching the ball. Your responses are confidential. If you have questions, ask the researcher before starting.\n\nClick "Start" when you\'re ready!', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.03,
         size=(1.5, 1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instructtxt',
         depth=0, autoLog=True,
    )
    start_button = visual.ButtonStim(win, 
        text='START', font='Arvo',
        pos=(0, -0.4),
        letterHeight=0.05,
        size=(0.5, 0.1), 
        ori=0.0
        ,borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='start_button',
        depth=-1
    )
    start_button.buttonClock = core.Clock()
    
    # --- Initialize components for Routine "trial" ---
    player3image = visual.ImageStim(
        win=win,
        name='player3image', 
        image='images/player3.png', mask=None, anchor='center',
        ori=0.0, pos=(0, -0.3), draggable=False, size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    player1image = visual.ImageStim(
        win=win,
        name='player1image', 
        image='images/player1.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.5, 0.3), draggable=False, size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    player2image = visual.ImageStim(
        win=win,
        name='player2image', 
        image='images/player2.png', mask=None, anchor='center',
        ori=0.0, pos=(0.5, 0.3), draggable=False, size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-2.0)
    ballimage = visual.ImageStim(
        win=win,
        name='ballimage', 
        image='images/ball.png', mask=None, anchor='center',
        ori=0.0, pos=[0,0], draggable=False, size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-3.0)
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()
    instructtxtbox = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.03,
         size=(1.5, 0.5), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instructtxtbox',
         depth=-6, autoLog=True,
    )
    
    # --- Initialize components for Routine "ball_move" ---
    player3image_2 = visual.ImageStim(
        win=win,
        name='player3image_2', 
        image='images/player3.png', mask=None, anchor='center',
        ori=0.0, pos=(0, -0.3), draggable=False, size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    player1image_2 = visual.ImageStim(
        win=win,
        name='player1image_2', 
        image='images/player1.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.5, 0.3), draggable=False, size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-2.0)
    player2image_2 = visual.ImageStim(
        win=win,
        name='player2image_2', 
        image='images/player2.png', mask=None, anchor='center',
        ori=0.0, pos=(0.5, 0.3), draggable=False, size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-3.0)
    ballimage_2 = visual.ImageStim(
        win=win,
        name='ballimage_2', 
        image='images/ball.png', mask=None, anchor='center',
        ori=0.0, pos=[0,0], draggable=False, size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-4.0)
    instructtxtbox_2 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.03,
         size=(1.5, 0.5), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instructtxtbox_2',
         depth=-5, autoLog=True,
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
        components=[instructtxt, start_button],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    instructtxt.reset()
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
        nReps=5.0, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('spreadsheets/equal_throws.xlsx'), 
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
        
        # --- Prepare to start Routine "trial" ---
        # create an object to store info about Routine trial
        trial = data.Routine(
            name='trial',
            components=[player3image, player1image, player2image, ballimage, mouse, instructtxtbox],
        )
        trial.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        ballimage.setPos((ball_start_x, ball_start_y))
        # setup some python lists for storing info about the mouse
        mouse.x = []
        mouse.y = []
        mouse.leftButton = []
        mouse.midButton = []
        mouse.rightButton = []
        mouse.time = []
        mouse.clicked_name = []
        gotValidClick = False  # until a click is received
        instructtxtbox.reset()
        instructtxtbox.setText(instruct)
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
            
            # *player3image* updates
            
            # if player3image is starting this frame...
            if player3image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                player3image.frameNStart = frameN  # exact frame index
                player3image.tStart = t  # local t and not account for scr refresh
                player3image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(player3image, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'player3image.started')
                # update status
                player3image.status = STARTED
                player3image.setAutoDraw(True)
            
            # if player3image is active this frame...
            if player3image.status == STARTED:
                # update params
                pass
            
            # *player1image* updates
            
            # if player1image is starting this frame...
            if player1image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                player1image.frameNStart = frameN  # exact frame index
                player1image.tStart = t  # local t and not account for scr refresh
                player1image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(player1image, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'player1image.started')
                # update status
                player1image.status = STARTED
                player1image.setAutoDraw(True)
            
            # if player1image is active this frame...
            if player1image.status == STARTED:
                # update params
                pass
            
            # *player2image* updates
            
            # if player2image is starting this frame...
            if player2image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                player2image.frameNStart = frameN  # exact frame index
                player2image.tStart = t  # local t and not account for scr refresh
                player2image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(player2image, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'player2image.started')
                # update status
                player2image.status = STARTED
                player2image.setAutoDraw(True)
            
            # if player2image is active this frame...
            if player2image.status == STARTED:
                # update params
                pass
            
            # *ballimage* updates
            
            # if ballimage is starting this frame...
            if ballimage.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                ballimage.frameNStart = frameN  # exact frame index
                ballimage.tStart = t  # local t and not account for scr refresh
                ballimage.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(ballimage, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'ballimage.started')
                # update status
                ballimage.status = STARTED
                ballimage.setAutoDraw(True)
            
            # if ballimage is active this frame...
            if ballimage.status == STARTED:
                # update params
                pass
            # *mouse* updates
            
            # if mouse is starting this frame...
            if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                mouse.frameNStart = frameN  # exact frame index
                mouse.tStart = t  # local t and not account for scr refresh
                mouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('mouse.started', t)
                # update status
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
                        clickableList = environmenttools.getFromNames([player1image, player2image], namespace=locals())
                        for obj in clickableList:
                            # is this object clicked on?
                            if obj.contains(mouse):
                                gotValidClick = True
                                mouse.clicked_name.append(obj.name)
                                mouse.clicked_name.append(obj.name)
                        if gotValidClick:
                            x, y = mouse.getPos()
                            mouse.x.append(x)
                            mouse.y.append(y)
                            buttons = mouse.getPressed()
                            mouse.leftButton.append(buttons[0])
                            mouse.midButton.append(buttons[1])
                            mouse.rightButton.append(buttons[2])
                            mouse.time.append(mouse.mouseClock.getTime())
                        if gotValidClick:
                            continueRoutine = False  # end routine on response
            # Run 'Each Frame' code from set_paths
            if ball_to != "choose" and t > 1:
                continueRoutine = False
            
            # *instructtxtbox* updates
            
            # if instructtxtbox is starting this frame...
            if instructtxtbox.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructtxtbox.frameNStart = frameN  # exact frame index
                instructtxtbox.tStart = t  # local t and not account for scr refresh
                instructtxtbox.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructtxtbox, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructtxtbox.started')
                # update status
                instructtxtbox.status = STARTED
                instructtxtbox.setAutoDraw(True)
            
            # if instructtxtbox is active this frame...
            if instructtxtbox.status == STARTED:
                # update params
                pass
            
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
        # store data for trials (TrialHandler)
        trials.addData('mouse.x', mouse.x)
        trials.addData('mouse.y', mouse.y)
        trials.addData('mouse.leftButton', mouse.leftButton)
        trials.addData('mouse.midButton', mouse.midButton)
        trials.addData('mouse.rightButton', mouse.rightButton)
        trials.addData('mouse.time', mouse.time)
        trials.addData('mouse.clicked_name', mouse.clicked_name)
        # Run 'End Routine' code from set_paths
        
        start_pos = [ball_start_x, ball_start_y]
        outcome_txt = ''
        
        if ball_to == "choose":
            
            # ball end location the selected player
            if mouse.clicked_name[-1] == "player1image":
                end_pos = player1image.pos
                
                outcome_txt = 'You chose Player 1'
                
            else:
                end_pos = player2image.pos
                
                outcome_txt = 'You chose Player 2'
            
            
        elif ball_to == "player1":
            
            # ball end location player1
            end_pos = player1image.pos
            
            outcome_txt = 'Player 2 chose Player 1'
            
        elif ball_to == "player2":
            
            # ball end location player2
            end_pos = player2image.pos
            
            outcome_txt = 'Player 1 chose Player 2'
            
        elif ball_from == "player1" and ball_to == "player3":
            
            # ball end location player2
            end_pos = player3image.pos
            
            outcome_txt = 'Player 1 chose you'
            
        elif ball_from == "player2" and ball_to == "player3":
            
            # ball end location player3
            end_pos = player3image.pos
            
            outcome_txt = 'Player 2 chose you'
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "ball_move" ---
        # create an object to store info about Routine ball_move
        ball_move = data.Routine(
            name='ball_move',
            components=[player3image_2, player1image_2, player2image_2, ballimage_2, instructtxtbox_2],
        )
        ball_move.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        ballimage_2.setPos((ball_start_x, ball_start_y))
        instructtxtbox_2.reset()
        instructtxtbox_2.setText(outcome_txt)
        # store start times for ball_move
        ball_move.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        ball_move.tStart = globalClock.getTime(format='float')
        ball_move.status = STARTED
        thisExp.addData('ball_move.started', ball_move.tStart)
        ball_move.maxDuration = None
        # keep track of which components have finished
        ball_moveComponents = ball_move.components
        for thisComponent in ball_move.components:
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
        
        # --- Run Routine "ball_move" ---
        ball_move.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 3.0:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from code
            total_time = 3
            x = start_pos[0] + ((end_pos[0] - start_pos[0]) / total_time) * t;
            y = start_pos[1] + ((end_pos[1] - start_pos[1]) / total_time) * t;
            ballimage_2.setPos([x, y-0.1])
            
            # *player3image_2* updates
            
            # if player3image_2 is starting this frame...
            if player3image_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                player3image_2.frameNStart = frameN  # exact frame index
                player3image_2.tStart = t  # local t and not account for scr refresh
                player3image_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(player3image_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'player3image_2.started')
                # update status
                player3image_2.status = STARTED
                player3image_2.setAutoDraw(True)
            
            # if player3image_2 is active this frame...
            if player3image_2.status == STARTED:
                # update params
                pass
            
            # if player3image_2 is stopping this frame...
            if player3image_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > player3image_2.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    player3image_2.tStop = t  # not accounting for scr refresh
                    player3image_2.tStopRefresh = tThisFlipGlobal  # on global time
                    player3image_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'player3image_2.stopped')
                    # update status
                    player3image_2.status = FINISHED
                    player3image_2.setAutoDraw(False)
            
            # *player1image_2* updates
            
            # if player1image_2 is starting this frame...
            if player1image_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                player1image_2.frameNStart = frameN  # exact frame index
                player1image_2.tStart = t  # local t and not account for scr refresh
                player1image_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(player1image_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'player1image_2.started')
                # update status
                player1image_2.status = STARTED
                player1image_2.setAutoDraw(True)
            
            # if player1image_2 is active this frame...
            if player1image_2.status == STARTED:
                # update params
                pass
            
            # if player1image_2 is stopping this frame...
            if player1image_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > player1image_2.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    player1image_2.tStop = t  # not accounting for scr refresh
                    player1image_2.tStopRefresh = tThisFlipGlobal  # on global time
                    player1image_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'player1image_2.stopped')
                    # update status
                    player1image_2.status = FINISHED
                    player1image_2.setAutoDraw(False)
            
            # *player2image_2* updates
            
            # if player2image_2 is starting this frame...
            if player2image_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                player2image_2.frameNStart = frameN  # exact frame index
                player2image_2.tStart = t  # local t and not account for scr refresh
                player2image_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(player2image_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'player2image_2.started')
                # update status
                player2image_2.status = STARTED
                player2image_2.setAutoDraw(True)
            
            # if player2image_2 is active this frame...
            if player2image_2.status == STARTED:
                # update params
                pass
            
            # if player2image_2 is stopping this frame...
            if player2image_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > player2image_2.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    player2image_2.tStop = t  # not accounting for scr refresh
                    player2image_2.tStopRefresh = tThisFlipGlobal  # on global time
                    player2image_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'player2image_2.stopped')
                    # update status
                    player2image_2.status = FINISHED
                    player2image_2.setAutoDraw(False)
            
            # *ballimage_2* updates
            
            # if ballimage_2 is starting this frame...
            if ballimage_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                ballimage_2.frameNStart = frameN  # exact frame index
                ballimage_2.tStart = t  # local t and not account for scr refresh
                ballimage_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(ballimage_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'ballimage_2.started')
                # update status
                ballimage_2.status = STARTED
                ballimage_2.setAutoDraw(True)
            
            # if ballimage_2 is active this frame...
            if ballimage_2.status == STARTED:
                # update params
                pass
            
            # if ballimage_2 is stopping this frame...
            if ballimage_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > ballimage_2.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    ballimage_2.tStop = t  # not accounting for scr refresh
                    ballimage_2.tStopRefresh = tThisFlipGlobal  # on global time
                    ballimage_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'ballimage_2.stopped')
                    # update status
                    ballimage_2.status = FINISHED
                    ballimage_2.setAutoDraw(False)
            
            # *instructtxtbox_2* updates
            
            # if instructtxtbox_2 is starting this frame...
            if instructtxtbox_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructtxtbox_2.frameNStart = frameN  # exact frame index
                instructtxtbox_2.tStart = t  # local t and not account for scr refresh
                instructtxtbox_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructtxtbox_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructtxtbox_2.started')
                # update status
                instructtxtbox_2.status = STARTED
                instructtxtbox_2.setAutoDraw(True)
            
            # if instructtxtbox_2 is active this frame...
            if instructtxtbox_2.status == STARTED:
                # update params
                pass
            
            # if instructtxtbox_2 is stopping this frame...
            if instructtxtbox_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > instructtxtbox_2.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    instructtxtbox_2.tStop = t  # not accounting for scr refresh
                    instructtxtbox_2.tStopRefresh = tThisFlipGlobal  # on global time
                    instructtxtbox_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'instructtxtbox_2.stopped')
                    # update status
                    instructtxtbox_2.status = FINISHED
                    instructtxtbox_2.setAutoDraw(False)
            
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
                ball_move.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in ball_move.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "ball_move" ---
        for thisComponent in ball_move.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for ball_move
        ball_move.tStop = globalClock.getTime(format='float')
        ball_move.tStopRefresh = tThisFlipGlobal
        thisExp.addData('ball_move.stopped', ball_move.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if ball_move.maxDurationReached:
            routineTimer.addTime(-ball_move.maxDuration)
        elif ball_move.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-3.000000)
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
        
    # completed 5.0 repeats of 'trials'
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
