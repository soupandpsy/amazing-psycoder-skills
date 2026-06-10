# Ultimatum Game — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [ultimatum-game](../../../psy-exp-designer/paradigms/ultimatum-game.md)
> **Source**: [Pavlovia demos/ultimatum_game](https://gitlab.pavlovia.org/demos/ultimatum_game) · PsychoPy 2024.2.4

## Experiment Logic

The Ultimatum Game is a two-player economic decision-making paradigm where participants take alternating roles as proposer and responder across a series of trials. The experiment begins with a welcome screen ("welcome" routine) where the participant enters their name using an editable `TextBox2` component. A "START GAME" button (`name_submit`) becomes visible once the name field contains text; clicking it advances the experiment. The name is then used throughout to personalize instructions and earning displays.

A simulated connecting sequence ("connecting" routine) runs for 6 seconds to increase believability of a live multiplayer setup. A loading icon (`ImageStim` displaying `images/load-icon.png`) rotates continuously via `image.setOri(45*t, log=False)` while "We are connecting with another player... please wait." is shown for 4 seconds, followed by "Connected!" for the remaining 2 seconds. The instructions routine ("instructions" routine) then explains the game rules: on each trial, one player is randomly assigned as proposer and one as responder; the proposer splits 10 pounds; the responder accepts or rejects; if accepted both receive their shares, if rejected neither receives money. A START button advances to the trial loop.

The trial loop is driven by a condition file (`roles_spreadsheet.xlsx`) loaded via `data.importConditions()` into a `TrialHandler2`. Each row defines the role assignment for a trial via the `participant_role` column (either "PROPOSER" or "RESPONDENT") and a `role_text` column for on-screen announcements. The loop begins with a role assignment display ("decide_roles" routine), which shows a spinning loading icon and "Selecting roles. Please wait." for 4 seconds, then reveals the assigned role (e.g., "You have been assigned as PROPOSER") with a START button. Earnings trackers (`your_earnings` and `other_earnings`, initialized to 0 at experiment start) are displayed as persistent text boxes in the corner of the screen throughout the trial loop.

The trial then branches based on role. If the participant is the **PROPOSER**, the "make_offer" routine runs: an editable text box accepts a numeric offer (0-10), with per-frame input validation that only allows digit characters and values between 0 and 10 inclusive. A warning message ("You can only submit numeric values between 0 and 10.") is shown in red if input is invalid, and the SUBMIT OFFER button is only clickable (via `offer_submit_mouse.isPressedIn(offer_submit)`) when the validation flag `submittable` is True. The submitted offer value is captured as `this_offer`. If the participant is the **RESPONDENT**, the "make_offer" routine is skipped entirely (via `decide.skipped` condition), and instead the "wait_for_offer" routine shows a waiting screen for a randomized duration (`duration = 3 + (random()*4)`) to simulate the other player deliberating.

The complement routine then fires. If the participant is the **PROPOSER**, the "decide" routine is skipped; if they are the **RESPONDENT**, the "decide" routine shows the offer (e.g., "Joshua has offered you 3") with Accept and Reject buttons (colored `TextBox2` components). Mouse click detection uses `event.Mouse` with `getPressed()` state tracking and `obj.contains(mouse)` hit testing on both buttons. The clicked button name is recorded in `mouse.clicked_name`.

The final trial routine ("outcome") computes earnings based on the interaction. A `Begin Routine` code block sets `amount_on_offer = 10` and branches on participant role and the decision outcome. For responders: if `mouse.clicked_name[-1] == 'accept'`, they earn the offered amount and the proposer earns the remainder; otherwise both earn nothing. For proposers: if the offer was at least half the total (`this_offer >= amount_on_offer/2`), it is treated as accepted; otherwise rejected. Earnings are accumulated and stored via `thisExp.addData()`. The outcome text is displayed for 3 seconds.

After all trials complete, a thank-you screen ("thankyou" routine) shows final earnings for both players and an EXIT GAME button that ends the experiment. All per-trial data (mouse clicks, offer values, role assignments, earnings) is saved to the `TrialHandler` and the `ExperimentHandler` automatically writes wide-format CSV and pickle output.

## Key Design Patterns

- `data.Routine()` objects with `maxDuration`, `.skipped`, and `.forceEnded` for structured routine lifecycle (2024.2.4+ style)
- Role-based routine skipping via `continueRoutine = not (<condition>)` -- `make_offer` skips for RESPONDENT, `decide` skips for PROPOSER
- Editable `TextBox2` for participant text entry (name, offer) with `editable=True` and `fillColor='white', borderColor='black'` for visible input field
- Per-frame input validation with character whitelist (`allowed_characters = ['0'-'9']`) and range checking (0-10) controlling a `submittable` flag
- `event.Mouse` with `getPressed()` state-tracking pattern and `obj.contains(mouse)` for click hit-testing on `TextBox2` targets
- `isClicked`/`wasClicked` pattern on `ButtonStim` for detecting new button clicks in instructions/role screens
- Accumulator variables (`your_earnings`, `other_earnings`) initialized at experiment start, updated in outcome routine's Begin Routine code
- `visual.ImageStim` with per-frame rotation (`setOri(45*t, log=False)`) for animated loading spinner
- Randomized wait duration (`3 + random()*4`) for believability in the waiting screen, with dynamic component stop timing using variable `duration`
- `deviceManager` with `hardware.DeviceManager()` for centralized hardware management (2024.2.4+ pattern)
- `globalClock='float'` format for convenient global time handling

## Code Example

Complete runnable PsychoPy code for the Ultimatum Game task:

```python
# Source: ultimatum_game (demos/ultimatum_game)
# Project URL: https://gitlab.pavlovia.org/demos/ultimatum_game
# Original file: ultimatum_game_lastrun.py
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on Thu Jan  2 12:35:12 2025
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
expName = 'ultimatum_game'  # from the Builder filename that created this script
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
        originPath='/Users/Becca/Library/CloudStorage/GoogleDrive-becca@opensciencetools.org/Shared drives/Science/Pavlovia Demos/ultimatium_game/ultimatum_game_lastrun.py',
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
    
    # --- Initialize components for Routine "welcome" ---
    welcometxt = visual.TextBox2(
         win, text='Welcome to the Ultimatum game. Please type your name below so that we can introduce you to your team mate:', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.3), draggable=False,      letterHeight=0.05,
         size=(1, 0.2), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='welcometxt',
         depth=0, autoLog=True,
    )
    player_name = visual.TextBox2(
         win, text=None, placeholder=None, font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(0.5, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='white', borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=True,
         name='player_name',
         depth=-1, autoLog=True,
    )
    name_submit = visual.TextBox2(
         win, text='START GAME', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, -0.4), draggable=False,      letterHeight=0.05,
         size=(0.5, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='darkgrey', borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='name_submit',
         depth=-2, autoLog=True,
    )
    start_mouse = event.Mouse(win=win)
    x, y = [None, None]
    start_mouse.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "connecting" ---
    image = visual.ImageStim(
        win=win,
        name='image', 
        image='images/load-icon.png', mask=None, anchor='center',
        ori=1.0, pos=(0, 0), draggable=False, size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    connecting_txt = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.2), draggable=False,      letterHeight=0.03,
         size=(0.5, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='connecting_txt',
         depth=-1, autoLog=True,
    )
    connecting_txt_2 = visual.TextBox2(
         win, text='Connected!', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.03,
         size=(0.5, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='connecting_txt_2',
         depth=-2, autoLog=True,
    )
    
    # --- Initialize components for Routine "instructions" ---
    instructionstxt = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.04,
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
         name='instructionstxt',
         depth=0, autoLog=True,
    )
    start_button = visual.ButtonStim(win, 
        text='START', font='Arial',
        pos=(0, -0.4),
        letterHeight=0.05,
        size=(0.3, 0.1), 
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
    
    # --- Initialize components for Routine "decide_roles" ---
    image_2 = visual.ImageStim(
        win=win,
        name='image_2', 
        image='images/load-icon.png', mask=None, anchor='center',
        ori=1.0, pos=(0, 0), draggable=False, size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    connecting_txt_3 = visual.TextBox2(
         win, text='Selecting roles. Please wait.', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.2), draggable=False,      letterHeight=0.03,
         size=(0.5, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='connecting_txt_3',
         depth=-1, autoLog=True,
    )
    connecting_txt_4 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.03,
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
         name='connecting_txt_4',
         depth=-2, autoLog=True,
    )
    start_button_2 = visual.ButtonStim(win, 
        text='START', font='Arial',
        pos=(0, -0.4),
        letterHeight=0.05,
        size=(0.3, 0.1), 
        ori=0.0
        ,borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='start_button_2',
        depth=-3
    )
    start_button_2.buttonClock = core.Clock()
    your_earning_txt_2 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(-0.4, 0.4), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='your_earning_txt_2',
         depth=-4, autoLog=True,
    )
    other_earning_txt_2 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0.4, 0.4), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='other_earning_txt_2',
         depth=-5, autoLog=True,
    )
    
    # --- Initialize components for Routine "make_offer" ---
    offer_instr = visual.TextBox2(
         win, text='You have £10 to split. Type the ammount below that you would like to offer Joshua. ', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.2), draggable=False,      letterHeight=0.05,
         size=(1, 0.15), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='offer_instr',
         depth=-1, autoLog=True,
    )
    participant_offer = visual.TextBox2(
         win, text=None, placeholder=None, font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(0.5, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='white', borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=True,
         name='participant_offer',
         depth=-2, autoLog=True,
    )
    offer_submit = visual.TextBox2(
         win, text='SUBMIT OFFER', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, -0.4), draggable=False,      letterHeight=0.05,
         size=(0.5, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='darkgrey', borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='offer_submit',
         depth=-3, autoLog=True,
    )
    offer_submit_mouse = event.Mouse(win=win)
    x, y = [None, None]
    offer_submit_mouse.mouseClock = core.Clock()
    your_earning_txt_3 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(-0.4, 0.4), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='your_earning_txt_3',
         depth=-6, autoLog=True,
    )
    other_earning_txt_3 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0.4, 0.4), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='other_earning_txt_3',
         depth=-7, autoLog=True,
    )
    warning = visual.TextBox2(
         win, text='You can only submit numeric values between 0 and 10.', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, -0.2), draggable=False,      letterHeight=0.03,
         size=(0.5, 0.1), borderWidth=2.0,
         color='red', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='warning',
         depth=-8, autoLog=True,
    )
    coin_stack = visual.ImageStim(
        win=win,
        name='coin_stack', 
        image='images/coin_stack.png', mask=None, anchor='center',
        ori=0.0, pos=(0.35, 0), draggable=False, size=(0.1, 0.3),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-9.0)
    
    # --- Initialize components for Routine "wait_for_offer" ---
    waitscreen = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
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
         name='waitscreen',
         depth=-1, autoLog=True,
    )
    your_earning_txt_4 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(-0.4, 0.4), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='your_earning_txt_4',
         depth=-2, autoLog=True,
    )
    other_earning_txt_4 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0.4, 0.4), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='other_earning_txt_4',
         depth=-3, autoLog=True,
    )
    coin_stack_2 = visual.ImageStim(
        win=win,
        name='coin_stack_2', 
        image='images/coin_stack.png', mask=None, anchor='center',
        ori=0.0, pos=(0.35, 0), draggable=False, size=(0.1, 0.3),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-4.0)
    
    # --- Initialize components for Routine "decide" ---
    offer_txt = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
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
         name='offer_txt',
         depth=0, autoLog=True,
    )
    accept = visual.TextBox2(
         win, text='Accept', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(-0.2, -0.2), draggable=False,      letterHeight=0.05,
         size=(0.3, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[-0.2549, 0.2392, 0.2549], borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='accept',
         depth=-1, autoLog=True,
    )
    reject = visual.TextBox2(
         win, text='Reject', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0.2, -0.2), draggable=False,      letterHeight=0.05,
         size=(0.3, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[0.4745, 0.1216, 0.1216], borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='reject',
         depth=-2, autoLog=True,
    )
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()
    your_earning_txt_5 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(-0.4, 0.4), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='your_earning_txt_5',
         depth=-4, autoLog=True,
    )
    other_earning_txt_5 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0.4, 0.4), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='other_earning_txt_5',
         depth=-5, autoLog=True,
    )
    
    # --- Initialize components for Routine "outcome" ---
    # Run 'Begin Experiment' code from set_feedback
    your_earnings = 0
    other_earnings = 0
    fbtxtbox = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
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
         name='fbtxtbox',
         depth=-1, autoLog=True,
    )
    your_earning_txt = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(-0.4, 0.4), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='your_earning_txt',
         depth=-2, autoLog=True,
    )
    other_earning_txt = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0.4, 0.4), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='other_earning_txt',
         depth=-3, autoLog=True,
    )
    
    # --- Initialize components for Routine "thankyou" ---
    thankstxt = visual.TextBox2(
         win, text='Thank you for playing the Ultimatum game! Your final earnings are below. Click the button below to exit the game.', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.3), draggable=False,      letterHeight=0.05,
         size=(1, 0.2), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='thankstxt',
         depth=0, autoLog=True,
    )
    exit_button = visual.TextBox2(
         win, text='EXIT GAME', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, -0.4), draggable=False,      letterHeight=0.05,
         size=(0.5, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='darkgrey', borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='exit_button',
         depth=-1, autoLog=True,
    )
    end_mouse = event.Mouse(win=win)
    x, y = [None, None]
    end_mouse.mouseClock = core.Clock()
    your_earning_txt_6 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, -0.2), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='your_earning_txt_6',
         depth=-3, autoLog=True,
    )
    other_earning_txt_6 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, -0.3), draggable=False,      letterHeight=0.03,
         size=(0.4, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='other_earning_txt_6',
         depth=-4, autoLog=True,
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
    
    # --- Prepare to start Routine "welcome" ---
    # create an object to store info about Routine welcome
    welcome = data.Routine(
        name='welcome',
        components=[welcometxt, player_name, name_submit, start_mouse],
    )
    welcome.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    welcometxt.reset()
    player_name.reset()
    name_submit.reset()
    # setup some python lists for storing info about the start_mouse
    start_mouse.x = []
    start_mouse.y = []
    start_mouse.leftButton = []
    start_mouse.midButton = []
    start_mouse.rightButton = []
    start_mouse.time = []
    start_mouse.clicked_name = []
    gotValidClick = False  # until a click is received
    # store start times for welcome
    welcome.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    welcome.tStart = globalClock.getTime(format='float')
    welcome.status = STARTED
    thisExp.addData('welcome.started', welcome.tStart)
    welcome.maxDuration = None
    # keep track of which components have finished
    welcomeComponents = welcome.components
    for thisComponent in welcome.components:
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
    
    # --- Run Routine "welcome" ---
    welcome.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *welcometxt* updates
        
        # if welcometxt is starting this frame...
        if welcometxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            welcometxt.frameNStart = frameN  # exact frame index
            welcometxt.tStart = t  # local t and not account for scr refresh
            welcometxt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(welcometxt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'welcometxt.started')
            # update status
            welcometxt.status = STARTED
            welcometxt.setAutoDraw(True)
        
        # if welcometxt is active this frame...
        if welcometxt.status == STARTED:
            # update params
            pass
        
        # *player_name* updates
        
        # if player_name is starting this frame...
        if player_name.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            player_name.frameNStart = frameN  # exact frame index
            player_name.tStart = t  # local t and not account for scr refresh
            player_name.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(player_name, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'player_name.started')
            # update status
            player_name.status = STARTED
            player_name.setAutoDraw(True)
        
        # if player_name is active this frame...
        if player_name.status == STARTED:
            # update params
            pass
        
        # *name_submit* updates
        
        # if name_submit is starting this frame...
        if name_submit.status == NOT_STARTED and player_name.text:
            # keep track of start time/frame for later
            name_submit.frameNStart = frameN  # exact frame index
            name_submit.tStart = t  # local t and not account for scr refresh
            name_submit.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(name_submit, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'name_submit.started')
            # update status
            name_submit.status = STARTED
            name_submit.setAutoDraw(True)
        
        # if name_submit is active this frame...
        if name_submit.status == STARTED:
            # update params
            pass
        # *start_mouse* updates
        
        # if start_mouse is starting this frame...
        if start_mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            start_mouse.frameNStart = frameN  # exact frame index
            start_mouse.tStart = t  # local t and not account for scr refresh
            start_mouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_mouse, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('start_mouse.started', t)
            # update status
            start_mouse.status = STARTED
            start_mouse.mouseClock.reset()
            prevButtonState = start_mouse.getPressed()  # if button is down already this ISN'T a new click
        if start_mouse.status == STARTED:  # only update if started and not finished!
            buttons = start_mouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    clickableList = environmenttools.getFromNames(name_submit, namespace=locals())
                    for obj in clickableList:
                        # is this object clicked on?
                        if obj.contains(start_mouse):
                            gotValidClick = True
                            start_mouse.clicked_name.append(obj.name)
                            start_mouse.clicked_name.append(obj.name)
                    if gotValidClick:
                        x, y = start_mouse.getPos()
                        start_mouse.x.append(x)
                        start_mouse.y.append(y)
                        buttons = start_mouse.getPressed()
                        start_mouse.leftButton.append(buttons[0])
                        start_mouse.midButton.append(buttons[1])
                        start_mouse.rightButton.append(buttons[2])
                        start_mouse.time.append(start_mouse.mouseClock.getTime())
                    if gotValidClick:
                        continueRoutine = False  # end routine on response
        
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
            welcome.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in welcome.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "welcome" ---
    for thisComponent in welcome.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for welcome
    welcome.tStop = globalClock.getTime(format='float')
    welcome.tStopRefresh = tThisFlipGlobal
    thisExp.addData('welcome.stopped', welcome.tStop)
    thisExp.addData('player_name.text',player_name.text)
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('start_mouse.x', start_mouse.x)
    thisExp.addData('start_mouse.y', start_mouse.y)
    thisExp.addData('start_mouse.leftButton', start_mouse.leftButton)
    thisExp.addData('start_mouse.midButton', start_mouse.midButton)
    thisExp.addData('start_mouse.rightButton', start_mouse.rightButton)
    thisExp.addData('start_mouse.time', start_mouse.time)
    thisExp.addData('start_mouse.clicked_name', start_mouse.clicked_name)
    thisExp.nextEntry()
    # the Routine "welcome" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "connecting" ---
    # create an object to store info about Routine connecting
    connecting = data.Routine(
        name='connecting',
        components=[image, connecting_txt, connecting_txt_2],
    )
    connecting.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    connecting_txt.reset()
    connecting_txt.setText("Welcome " + player_name.text + "! We are connecting with another player... please wait.")
    connecting_txt_2.reset()
    # store start times for connecting
    connecting.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    connecting.tStart = globalClock.getTime(format='float')
    connecting.status = STARTED
    thisExp.addData('connecting.started', connecting.tStart)
    connecting.maxDuration = None
    # keep track of which components have finished
    connectingComponents = connecting.components
    for thisComponent in connecting.components:
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
    
    # --- Run Routine "connecting" ---
    connecting.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 6.0:
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
            image.setOri(45*t, log=False)
        
        # if image is stopping this frame...
        if image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > image.tStartRefresh + 4-frameTolerance:
                # keep track of stop time/frame for later
                image.tStop = t  # not accounting for scr refresh
                image.tStopRefresh = tThisFlipGlobal  # on global time
                image.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'image.stopped')
                # update status
                image.status = FINISHED
                image.setAutoDraw(False)
        
        # *connecting_txt* updates
        
        # if connecting_txt is starting this frame...
        if connecting_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            connecting_txt.frameNStart = frameN  # exact frame index
            connecting_txt.tStart = t  # local t and not account for scr refresh
            connecting_txt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(connecting_txt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'connecting_txt.started')
            # update status
            connecting_txt.status = STARTED
            connecting_txt.setAutoDraw(True)
        
        # if connecting_txt is active this frame...
        if connecting_txt.status == STARTED:
            # update params
            pass
        
        # if connecting_txt is stopping this frame...
        if connecting_txt.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > connecting_txt.tStartRefresh + 4-frameTolerance:
                # keep track of stop time/frame for later
                connecting_txt.tStop = t  # not accounting for scr refresh
                connecting_txt.tStopRefresh = tThisFlipGlobal  # on global time
                connecting_txt.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'connecting_txt.stopped')
                # update status
                connecting_txt.status = FINISHED
                connecting_txt.setAutoDraw(False)
        
        # *connecting_txt_2* updates
        
        # if connecting_txt_2 is starting this frame...
        if connecting_txt_2.status == NOT_STARTED and tThisFlip >= 4-frameTolerance:
            # keep track of start time/frame for later
            connecting_txt_2.frameNStart = frameN  # exact frame index
            connecting_txt_2.tStart = t  # local t and not account for scr refresh
            connecting_txt_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(connecting_txt_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'connecting_txt_2.started')
            # update status
            connecting_txt_2.status = STARTED
            connecting_txt_2.setAutoDraw(True)
        
        # if connecting_txt_2 is active this frame...
        if connecting_txt_2.status == STARTED:
            # update params
            pass
        
        # if connecting_txt_2 is stopping this frame...
        if connecting_txt_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > connecting_txt_2.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                connecting_txt_2.tStop = t  # not accounting for scr refresh
                connecting_txt_2.tStopRefresh = tThisFlipGlobal  # on global time
                connecting_txt_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'connecting_txt_2.stopped')
                # update status
                connecting_txt_2.status = FINISHED
                connecting_txt_2.setAutoDraw(False)
        
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
            connecting.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in connecting.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "connecting" ---
    for thisComponent in connecting.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for connecting
    connecting.tStop = globalClock.getTime(format='float')
    connecting.tStopRefresh = tThisFlipGlobal
    thisExp.addData('connecting.stopped', connecting.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if connecting.maxDurationReached:
        routineTimer.addTime(-connecting.maxDuration)
    elif connecting.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-6.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "instructions" ---
    # create an object to store info about Routine instructions
    instructions = data.Routine(
        name='instructions',
        components=[instructionstxt, start_button],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    instructionstxt.reset()
    instructionstxt.setText(player_name.text + ', you are connected with Joshua.\n In a moment we and Joshua will get the chance to earn some money.\nOn each trial the game will randomly choose one of you to be the "proposer" and one of you to be the "responder".\nThe proposer will make an offer on how to split some money. \nThe responder will decide whether to accept that offer.\nIf that offer is accepted, both of you will receive your agreed upon amounts. If you do not agree and the responder rejects the proposer’s offer, then nobody receives any money.')
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
        
        # *instructionstxt* updates
        
        # if instructionstxt is starting this frame...
        if instructionstxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructionstxt.frameNStart = frameN  # exact frame index
            instructionstxt.tStart = t  # local t and not account for scr refresh
            instructionstxt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructionstxt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instructionstxt.started')
            # update status
            instructionstxt.status = STARTED
            instructionstxt.setAutoDraw(True)
        
        # if instructionstxt is active this frame...
        if instructionstxt.status == STARTED:
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
                timers=[routineTimer], 
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
        trialList=data.importConditions('roles_spreadsheet.xlsx'), 
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
        
        # --- Prepare to start Routine "decide_roles" ---
        # create an object to store info about Routine decide_roles
        decide_roles = data.Routine(
            name='decide_roles',
            components=[image_2, connecting_txt_3, connecting_txt_4, start_button_2, your_earning_txt_2, other_earning_txt_2],
        )
        decide_roles.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        connecting_txt_3.reset()
        connecting_txt_4.reset()
        connecting_txt_4.setText(role_text)
        # reset start_button_2 to account for continued clicks & clear times on/off
        start_button_2.reset()
        your_earning_txt_2.reset()
        your_earning_txt_2.setText(player_name.text + 's (You) earnings: £' + str(your_earnings))
        other_earning_txt_2.reset()
        other_earning_txt_2.setText('Joshuas earnings: £' + str(other_earnings))
        # store start times for decide_roles
        decide_roles.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        decide_roles.tStart = globalClock.getTime(format='float')
        decide_roles.status = STARTED
        thisExp.addData('decide_roles.started', decide_roles.tStart)
        decide_roles.maxDuration = None
        # keep track of which components have finished
        decide_rolesComponents = decide_roles.components
        for thisComponent in decide_roles.components:
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
        
        # --- Run Routine "decide_roles" ---
        # if trial has changed, end Routine now
        if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
            continueRoutine = False
        decide_roles.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *image_2* updates
            
            # if image_2 is starting this frame...
            if image_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                image_2.frameNStart = frameN  # exact frame index
                image_2.tStart = t  # local t and not account for scr refresh
                image_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(image_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'image_2.started')
                # update status
                image_2.status = STARTED
                image_2.setAutoDraw(True)
            
            # if image_2 is active this frame...
            if image_2.status == STARTED:
                # update params
                image_2.setOri(45*t, log=False)
            
            # if image_2 is stopping this frame...
            if image_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > image_2.tStartRefresh + 4-frameTolerance:
                    # keep track of stop time/frame for later
                    image_2.tStop = t  # not accounting for scr refresh
                    image_2.tStopRefresh = tThisFlipGlobal  # on global time
                    image_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'image_2.stopped')
                    # update status
                    image_2.status = FINISHED
                    image_2.setAutoDraw(False)
            
            # *connecting_txt_3* updates
            
            # if connecting_txt_3 is starting this frame...
            if connecting_txt_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                connecting_txt_3.frameNStart = frameN  # exact frame index
                connecting_txt_3.tStart = t  # local t and not account for scr refresh
                connecting_txt_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(connecting_txt_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'connecting_txt_3.started')
                # update status
                connecting_txt_3.status = STARTED
                connecting_txt_3.setAutoDraw(True)
            
            # if connecting_txt_3 is active this frame...
            if connecting_txt_3.status == STARTED:
                # update params
                pass
            
            # if connecting_txt_3 is stopping this frame...
            if connecting_txt_3.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > connecting_txt_3.tStartRefresh + 4-frameTolerance:
                    # keep track of stop time/frame for later
                    connecting_txt_3.tStop = t  # not accounting for scr refresh
                    connecting_txt_3.tStopRefresh = tThisFlipGlobal  # on global time
                    connecting_txt_3.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'connecting_txt_3.stopped')
                    # update status
                    connecting_txt_3.status = FINISHED
                    connecting_txt_3.setAutoDraw(False)
            
            # *connecting_txt_4* updates
            
            # if connecting_txt_4 is starting this frame...
            if connecting_txt_4.status == NOT_STARTED and tThisFlip >= 4-frameTolerance:
                # keep track of start time/frame for later
                connecting_txt_4.frameNStart = frameN  # exact frame index
                connecting_txt_4.tStart = t  # local t and not account for scr refresh
                connecting_txt_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(connecting_txt_4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'connecting_txt_4.started')
                # update status
                connecting_txt_4.status = STARTED
                connecting_txt_4.setAutoDraw(True)
            
            # if connecting_txt_4 is active this frame...
            if connecting_txt_4.status == STARTED:
                # update params
                pass
            # *start_button_2* updates
            
            # if start_button_2 is starting this frame...
            if start_button_2.status == NOT_STARTED and tThisFlip >= 4-frameTolerance:
                # keep track of start time/frame for later
                start_button_2.frameNStart = frameN  # exact frame index
                start_button_2.tStart = t  # local t and not account for scr refresh
                start_button_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(start_button_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'start_button_2.started')
                # update status
                start_button_2.status = STARTED
                win.callOnFlip(start_button_2.buttonClock.reset)
                start_button_2.setAutoDraw(True)
            
            # if start_button_2 is active this frame...
            if start_button_2.status == STARTED:
                # update params
                pass
                # check whether start_button_2 has been pressed
                if start_button_2.isClicked:
                    if not start_button_2.wasClicked:
                        # if this is a new click, store time of first click and clicked until
                        start_button_2.timesOn.append(start_button_2.buttonClock.getTime())
                        start_button_2.timesOff.append(start_button_2.buttonClock.getTime())
                    elif len(start_button_2.timesOff):
                        # if click is continuing from last frame, update time of clicked until
                        start_button_2.timesOff[-1] = start_button_2.buttonClock.getTime()
                    if not start_button_2.wasClicked:
                        # end routine when start_button_2 is clicked
                        continueRoutine = False
                    if not start_button_2.wasClicked:
                        # run callback code when start_button_2 is clicked
                        pass
            # take note of whether start_button_2 was clicked, so that next frame we know if clicks are new
            start_button_2.wasClicked = start_button_2.isClicked and start_button_2.status == STARTED
            
            # *your_earning_txt_2* updates
            
            # if your_earning_txt_2 is starting this frame...
            if your_earning_txt_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                your_earning_txt_2.frameNStart = frameN  # exact frame index
                your_earning_txt_2.tStart = t  # local t and not account for scr refresh
                your_earning_txt_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(your_earning_txt_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'your_earning_txt_2.started')
                # update status
                your_earning_txt_2.status = STARTED
                your_earning_txt_2.setAutoDraw(True)
            
            # if your_earning_txt_2 is active this frame...
            if your_earning_txt_2.status == STARTED:
                # update params
                pass
            
            # *other_earning_txt_2* updates
            
            # if other_earning_txt_2 is starting this frame...
            if other_earning_txt_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                other_earning_txt_2.frameNStart = frameN  # exact frame index
                other_earning_txt_2.tStart = t  # local t and not account for scr refresh
                other_earning_txt_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(other_earning_txt_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'other_earning_txt_2.started')
                # update status
                other_earning_txt_2.status = STARTED
                other_earning_txt_2.setAutoDraw(True)
            
            # if other_earning_txt_2 is active this frame...
            if other_earning_txt_2.status == STARTED:
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
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                decide_roles.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in decide_roles.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "decide_roles" ---
        for thisComponent in decide_roles.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for decide_roles
        decide_roles.tStop = globalClock.getTime(format='float')
        decide_roles.tStopRefresh = tThisFlipGlobal
        thisExp.addData('decide_roles.stopped', decide_roles.tStop)
        trials.addData('start_button_2.numClicks', start_button_2.numClicks)
        if start_button_2.numClicks:
           trials.addData('start_button_2.timesOn', start_button_2.timesOn)
           trials.addData('start_button_2.timesOff', start_button_2.timesOff)
        else:
           trials.addData('start_button_2.timesOn', "")
           trials.addData('start_button_2.timesOff', "")
        # the Routine "decide_roles" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "make_offer" ---
        # create an object to store info about Routine make_offer
        make_offer = data.Routine(
            name='make_offer',
            components=[offer_instr, participant_offer, offer_submit, offer_submit_mouse, your_earning_txt_3, other_earning_txt_3, warning, coin_stack],
        )
        make_offer.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from limit_numeric
        submittable = False
        
        
        offer_instr.reset()
        participant_offer.reset()
        offer_submit.reset()
        # setup some python lists for storing info about the offer_submit_mouse
        offer_submit_mouse.x = []
        offer_submit_mouse.y = []
        offer_submit_mouse.leftButton = []
        offer_submit_mouse.midButton = []
        offer_submit_mouse.rightButton = []
        offer_submit_mouse.time = []
        gotValidClick = False  # until a click is received
        # Run 'Begin Routine' code from fetch_offer
        this_offer = 0
        your_earning_txt_3.reset()
        your_earning_txt_3.setText(player_name.text + 's (You) earnings: £' + str(your_earnings))
        other_earning_txt_3.reset()
        other_earning_txt_3.setText('Joshuas earnings: £' + str(other_earnings))
        warning.reset()
        # store start times for make_offer
        make_offer.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        make_offer.tStart = globalClock.getTime(format='float')
        make_offer.status = STARTED
        thisExp.addData('make_offer.started', make_offer.tStart)
        make_offer.maxDuration = None
        # skip Routine make_offer if its 'Skip if' condition is True
        make_offer.skipped = continueRoutine and not (participant_role == "RESPONDENT")
        continueRoutine = make_offer.skipped
        # keep track of which components have finished
        make_offerComponents = make_offer.components
        for thisComponent in make_offer.components:
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
        
        # --- Run Routine "make_offer" ---
        # if trial has changed, end Routine now
        if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
            continueRoutine = False
        make_offer.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from limit_numeric
            # limit answers to numeric answers only
            allowed_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            if participant_offer.text:
                # if the characters are not in allowed characters - do not allow submit
                submittable = True
                for character in participant_offer.text:
                    if character not in allowed_characters:
                        submittable = False
                
                # do not allow offers less than 0 or more than 10
                if submittable:
                    if int(participant_offer.text) <0 or int(participant_offer.text) >10:
                        submittable = False
            
            
            # watches for mouse clicks on the submit button only 
            # when the conditions above have been met. 
            if submittable:
                if offer_submit_mouse.isPressedIn(offer_submit):
                    continueRoutine = False
            
            # *offer_instr* updates
            
            # if offer_instr is starting this frame...
            if offer_instr.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                offer_instr.frameNStart = frameN  # exact frame index
                offer_instr.tStart = t  # local t and not account for scr refresh
                offer_instr.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(offer_instr, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'offer_instr.started')
                # update status
                offer_instr.status = STARTED
                offer_instr.setAutoDraw(True)
            
            # if offer_instr is active this frame...
            if offer_instr.status == STARTED:
                # update params
                pass
            
            # *participant_offer* updates
            
            # if participant_offer is starting this frame...
            if participant_offer.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                participant_offer.frameNStart = frameN  # exact frame index
                participant_offer.tStart = t  # local t and not account for scr refresh
                participant_offer.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(participant_offer, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'participant_offer.started')
                # update status
                participant_offer.status = STARTED
                participant_offer.setAutoDraw(True)
            
            # if participant_offer is active this frame...
            if participant_offer.status == STARTED:
                # update params
                pass
            
            # *offer_submit* updates
            
            # if offer_submit is starting this frame...
            if offer_submit.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                offer_submit.frameNStart = frameN  # exact frame index
                offer_submit.tStart = t  # local t and not account for scr refresh
                offer_submit.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(offer_submit, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'offer_submit.started')
                # update status
                offer_submit.status = STARTED
                offer_submit.setAutoDraw(True)
            
            # if offer_submit is active this frame...
            if offer_submit.status == STARTED:
                # update params
                pass
            # *offer_submit_mouse* updates
            
            # if offer_submit_mouse is starting this frame...
            if offer_submit_mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                offer_submit_mouse.frameNStart = frameN  # exact frame index
                offer_submit_mouse.tStart = t  # local t and not account for scr refresh
                offer_submit_mouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(offer_submit_mouse, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('offer_submit_mouse.started', t)
                # update status
                offer_submit_mouse.status = STARTED
                offer_submit_mouse.mouseClock.reset()
                prevButtonState = offer_submit_mouse.getPressed()  # if button is down already this ISN'T a new click
            if offer_submit_mouse.status == STARTED:  # only update if started and not finished!
                buttons = offer_submit_mouse.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        pass
                        x, y = offer_submit_mouse.getPos()
                        offer_submit_mouse.x.append(x)
                        offer_submit_mouse.y.append(y)
                        buttons = offer_submit_mouse.getPressed()
                        offer_submit_mouse.leftButton.append(buttons[0])
                        offer_submit_mouse.midButton.append(buttons[1])
                        offer_submit_mouse.rightButton.append(buttons[2])
                        offer_submit_mouse.time.append(offer_submit_mouse.mouseClock.getTime())
            
            # *your_earning_txt_3* updates
            
            # if your_earning_txt_3 is starting this frame...
            if your_earning_txt_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                your_earning_txt_3.frameNStart = frameN  # exact frame index
                your_earning_txt_3.tStart = t  # local t and not account for scr refresh
                your_earning_txt_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(your_earning_txt_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'your_earning_txt_3.started')
                # update status
                your_earning_txt_3.status = STARTED
                your_earning_txt_3.setAutoDraw(True)
            
            # if your_earning_txt_3 is active this frame...
            if your_earning_txt_3.status == STARTED:
                # update params
                pass
            
            # *other_earning_txt_3* updates
            
            # if other_earning_txt_3 is starting this frame...
            if other_earning_txt_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                other_earning_txt_3.frameNStart = frameN  # exact frame index
                other_earning_txt_3.tStart = t  # local t and not account for scr refresh
                other_earning_txt_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(other_earning_txt_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'other_earning_txt_3.started')
                # update status
                other_earning_txt_3.status = STARTED
                other_earning_txt_3.setAutoDraw(True)
            
            # if other_earning_txt_3 is active this frame...
            if other_earning_txt_3.status == STARTED:
                # update params
                pass
            
            # *warning* updates
            
            # if warning is starting this frame...
            if warning.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                warning.frameNStart = frameN  # exact frame index
                warning.tStart = t  # local t and not account for scr refresh
                warning.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(warning, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'warning.started')
                # update status
                warning.status = STARTED
                warning.setAutoDraw(True)
            
            # if warning is active this frame...
            if warning.status == STARTED:
                # update params
                pass
            
            # *coin_stack* updates
            
            # if coin_stack is starting this frame...
            if coin_stack.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                coin_stack.frameNStart = frameN  # exact frame index
                coin_stack.tStart = t  # local t and not account for scr refresh
                coin_stack.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(coin_stack, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'coin_stack.started')
                # update status
                coin_stack.status = STARTED
                coin_stack.setAutoDraw(True)
            
            # if coin_stack is active this frame...
            if coin_stack.status == STARTED:
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
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                make_offer.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in make_offer.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "make_offer" ---
        for thisComponent in make_offer.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for make_offer
        make_offer.tStop = globalClock.getTime(format='float')
        make_offer.tStopRefresh = tThisFlipGlobal
        thisExp.addData('make_offer.stopped', make_offer.tStop)
        trials.addData('participant_offer.text',participant_offer.text)
        # store data for trials (TrialHandler)
        trials.addData('offer_submit_mouse.x', offer_submit_mouse.x)
        trials.addData('offer_submit_mouse.y', offer_submit_mouse.y)
        trials.addData('offer_submit_mouse.leftButton', offer_submit_mouse.leftButton)
        trials.addData('offer_submit_mouse.midButton', offer_submit_mouse.midButton)
        trials.addData('offer_submit_mouse.rightButton', offer_submit_mouse.rightButton)
        trials.addData('offer_submit_mouse.time', offer_submit_mouse.time)
        # Run 'End Routine' code from fetch_offer
        # if the participant is a respondent, and therefore typed something in the offer box
        # fetch this value to pipe in to the following routines.
        if participant_role != 'RESPONDENT':
            this_offer = int(participant_offer.text)
        # the Routine "make_offer" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "wait_for_offer" ---
        # create an object to store info about Routine wait_for_offer
        wait_for_offer = data.Routine(
            name='wait_for_offer',
            components=[waitscreen, your_earning_txt_4, other_earning_txt_4, coin_stack_2],
        )
        wait_for_offer.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from set_duration
        # randomly set the duration of the wait period to increase believability
        # random() produces a random value between 0 and 1
        duration = 3 + (random()*4)
        waitscreen.reset()
        waitscreen.setText(wait_text)
        your_earning_txt_4.reset()
        your_earning_txt_4.setText(player_name.text + 's (You) earnings: £' + str(your_earnings))
        other_earning_txt_4.reset()
        other_earning_txt_4.setText('Joshuas earnings: £' + str(other_earnings))
        # store start times for wait_for_offer
        wait_for_offer.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        wait_for_offer.tStart = globalClock.getTime(format='float')
        wait_for_offer.status = STARTED
        thisExp.addData('wait_for_offer.started', wait_for_offer.tStart)
        wait_for_offer.maxDuration = None
        # keep track of which components have finished
        wait_for_offerComponents = wait_for_offer.components
        for thisComponent in wait_for_offer.components:
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
        
        # --- Run Routine "wait_for_offer" ---
        # if trial has changed, end Routine now
        if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
            continueRoutine = False
        wait_for_offer.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *waitscreen* updates
            
            # if waitscreen is starting this frame...
            if waitscreen.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                waitscreen.frameNStart = frameN  # exact frame index
                waitscreen.tStart = t  # local t and not account for scr refresh
                waitscreen.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(waitscreen, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'waitscreen.started')
                # update status
                waitscreen.status = STARTED
                waitscreen.setAutoDraw(True)
            
            # if waitscreen is active this frame...
            if waitscreen.status == STARTED:
                # update params
                pass
            
            # if waitscreen is stopping this frame...
            if waitscreen.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > waitscreen.tStartRefresh + duration-frameTolerance:
                    # keep track of stop time/frame for later
                    waitscreen.tStop = t  # not accounting for scr refresh
                    waitscreen.tStopRefresh = tThisFlipGlobal  # on global time
                    waitscreen.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'waitscreen.stopped')
                    # update status
                    waitscreen.status = FINISHED
                    waitscreen.setAutoDraw(False)
            
            # *your_earning_txt_4* updates
            
            # if your_earning_txt_4 is starting this frame...
            if your_earning_txt_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                your_earning_txt_4.frameNStart = frameN  # exact frame index
                your_earning_txt_4.tStart = t  # local t and not account for scr refresh
                your_earning_txt_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(your_earning_txt_4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'your_earning_txt_4.started')
                # update status
                your_earning_txt_4.status = STARTED
                your_earning_txt_4.setAutoDraw(True)
            
            # if your_earning_txt_4 is active this frame...
            if your_earning_txt_4.status == STARTED:
                # update params
                pass
            
            # if your_earning_txt_4 is stopping this frame...
            if your_earning_txt_4.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > your_earning_txt_4.tStartRefresh + duration-frameTolerance:
                    # keep track of stop time/frame for later
                    your_earning_txt_4.tStop = t  # not accounting for scr refresh
                    your_earning_txt_4.tStopRefresh = tThisFlipGlobal  # on global time
                    your_earning_txt_4.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'your_earning_txt_4.stopped')
                    # update status
                    your_earning_txt_4.status = FINISHED
                    your_earning_txt_4.setAutoDraw(False)
            
            # *other_earning_txt_4* updates
            
            # if other_earning_txt_4 is starting this frame...
            if other_earning_txt_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                other_earning_txt_4.frameNStart = frameN  # exact frame index
                other_earning_txt_4.tStart = t  # local t and not account for scr refresh
                other_earning_txt_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(other_earning_txt_4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'other_earning_txt_4.started')
                # update status
                other_earning_txt_4.status = STARTED
                other_earning_txt_4.setAutoDraw(True)
            
            # if other_earning_txt_4 is active this frame...
            if other_earning_txt_4.status == STARTED:
                # update params
                pass
            
            # if other_earning_txt_4 is stopping this frame...
            if other_earning_txt_4.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > other_earning_txt_4.tStartRefresh + duration-frameTolerance:
                    # keep track of stop time/frame for later
                    other_earning_txt_4.tStop = t  # not accounting for scr refresh
                    other_earning_txt_4.tStopRefresh = tThisFlipGlobal  # on global time
                    other_earning_txt_4.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'other_earning_txt_4.stopped')
                    # update status
                    other_earning_txt_4.status = FINISHED
                    other_earning_txt_4.setAutoDraw(False)
            
            # *coin_stack_2* updates
            
            # if coin_stack_2 is starting this frame...
            if coin_stack_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                coin_stack_2.frameNStart = frameN  # exact frame index
                coin_stack_2.tStart = t  # local t and not account for scr refresh
                coin_stack_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(coin_stack_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'coin_stack_2.started')
                # update status
                coin_stack_2.status = STARTED
                coin_stack_2.setAutoDraw(True)
            
            # if coin_stack_2 is active this frame...
            if coin_stack_2.status == STARTED:
                # update params
                pass
            
            # if coin_stack_2 is stopping this frame...
            if coin_stack_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > coin_stack_2.tStartRefresh + duration-frameTolerance:
                    # keep track of stop time/frame for later
                    coin_stack_2.tStop = t  # not accounting for scr refresh
                    coin_stack_2.tStopRefresh = tThisFlipGlobal  # on global time
                    coin_stack_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'coin_stack_2.stopped')
                    # update status
                    coin_stack_2.status = FINISHED
                    coin_stack_2.setAutoDraw(False)
            
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
                wait_for_offer.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in wait_for_offer.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "wait_for_offer" ---
        for thisComponent in wait_for_offer.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for wait_for_offer
        wait_for_offer.tStop = globalClock.getTime(format='float')
        wait_for_offer.tStopRefresh = tThisFlipGlobal
        thisExp.addData('wait_for_offer.stopped', wait_for_offer.tStop)
        # the Routine "wait_for_offer" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "decide" ---
        # create an object to store info about Routine decide
        decide = data.Routine(
            name='decide',
            components=[offer_txt, accept, reject, mouse, your_earning_txt_5, other_earning_txt_5],
        )
        decide.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        offer_txt.reset()
        offer_txt.setText('Joshua has offered you £' + str(offer))
        accept.reset()
        reject.reset()
        # setup some python lists for storing info about the mouse
        mouse.x = []
        mouse.y = []
        mouse.leftButton = []
        mouse.midButton = []
        mouse.rightButton = []
        mouse.time = []
        mouse.clicked_name = []
        gotValidClick = False  # until a click is received
        your_earning_txt_5.reset()
        your_earning_txt_5.setText(player_name.text + 's (You) earnings: £' + str(your_earnings))
        other_earning_txt_5.reset()
        other_earning_txt_5.setText('Joshuas earnings: £' + str(other_earnings))
        # store start times for decide
        decide.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        decide.tStart = globalClock.getTime(format='float')
        decide.status = STARTED
        thisExp.addData('decide.started', decide.tStart)
        decide.maxDuration = None
        # skip Routine decide if its 'Skip if' condition is True
        decide.skipped = continueRoutine and not (participant_role == "PROPOSER")
        continueRoutine = decide.skipped
        # keep track of which components have finished
        decideComponents = decide.components
        for thisComponent in decide.components:
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
        
        # --- Run Routine "decide" ---
        # if trial has changed, end Routine now
        if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
            continueRoutine = False
        decide.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *offer_txt* updates
            
            # if offer_txt is starting this frame...
            if offer_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                offer_txt.frameNStart = frameN  # exact frame index
                offer_txt.tStart = t  # local t and not account for scr refresh
                offer_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(offer_txt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'offer_txt.started')
                # update status
                offer_txt.status = STARTED
                offer_txt.setAutoDraw(True)
            
            # if offer_txt is active this frame...
            if offer_txt.status == STARTED:
                # update params
                pass
            
            # *accept* updates
            
            # if accept is starting this frame...
            if accept.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                accept.frameNStart = frameN  # exact frame index
                accept.tStart = t  # local t and not account for scr refresh
                accept.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(accept, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'accept.started')
                # update status
                accept.status = STARTED
                accept.setAutoDraw(True)
            
            # if accept is active this frame...
            if accept.status == STARTED:
                # update params
                pass
            
            # *reject* updates
            
            # if reject is starting this frame...
            if reject.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                reject.frameNStart = frameN  # exact frame index
                reject.tStart = t  # local t and not account for scr refresh
                reject.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(reject, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'reject.started')
                # update status
                reject.status = STARTED
                reject.setAutoDraw(True)
            
            # if reject is active this frame...
            if reject.status == STARTED:
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
                        clickableList = environmenttools.getFromNames([accept, reject], namespace=locals())
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
                        
                        continueRoutine = False  # end routine on response
            
            # *your_earning_txt_5* updates
            
            # if your_earning_txt_5 is starting this frame...
            if your_earning_txt_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                your_earning_txt_5.frameNStart = frameN  # exact frame index
                your_earning_txt_5.tStart = t  # local t and not account for scr refresh
                your_earning_txt_5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(your_earning_txt_5, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'your_earning_txt_5.started')
                # update status
                your_earning_txt_5.status = STARTED
                your_earning_txt_5.setAutoDraw(True)
            
            # if your_earning_txt_5 is active this frame...
            if your_earning_txt_5.status == STARTED:
                # update params
                pass
            
            # *other_earning_txt_5* updates
            
            # if other_earning_txt_5 is starting this frame...
            if other_earning_txt_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                other_earning_txt_5.frameNStart = frameN  # exact frame index
                other_earning_txt_5.tStart = t  # local t and not account for scr refresh
                other_earning_txt_5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(other_earning_txt_5, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'other_earning_txt_5.started')
                # update status
                other_earning_txt_5.status = STARTED
                other_earning_txt_5.setAutoDraw(True)
            
            # if other_earning_txt_5 is active this frame...
            if other_earning_txt_5.status == STARTED:
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
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                decide.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in decide.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "decide" ---
        for thisComponent in decide.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for decide
        decide.tStop = globalClock.getTime(format='float')
        decide.tStopRefresh = tThisFlipGlobal
        thisExp.addData('decide.stopped', decide.tStop)
        # store data for trials (TrialHandler)
        trials.addData('mouse.x', mouse.x)
        trials.addData('mouse.y', mouse.y)
        trials.addData('mouse.leftButton', mouse.leftButton)
        trials.addData('mouse.midButton', mouse.midButton)
        trials.addData('mouse.rightButton', mouse.rightButton)
        trials.addData('mouse.time', mouse.time)
        trials.addData('mouse.clicked_name', mouse.clicked_name)
        # the Routine "decide" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "outcome" ---
        # create an object to store info about Routine outcome
        outcome = data.Routine(
            name='outcome',
            components=[fbtxtbox, your_earning_txt, other_earning_txt],
        )
        outcome.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from set_feedback
        # set the feedback text dependant on the 
        # participants role (respondent or proposer) and if the offer was accepted or rejected)
        amount_on_offer = 10
        if participant_role == 'RESPONDENT':
            if mouse.clicked_name[-1] == 'accept':
                fbtxt = 'You accepted this offer. \nYou receive £'+str(offer)+'\n Joshua receives £' + str(amount_on_offer  - offer)
                your_earnings += offer
                other_earnings += (amount_on_offer  - offer)
            else:
                fbtxt = 'You rejected this offer. \nNeither you nor Joshua receive any money'
        else:
            if this_offer >= (amount_on_offer/2):
                fbtxt = 'Joshua accepted this offer. \nYou receive £'+str(amount_on_offer  - this_offer)+'\n Joshua receives £' + str(this_offer)
                your_earnings += (amount_on_offer  - this_offer)
                other_earnings += this_offer
            else:
                fbtxt = 'Joshua rejected this offer. \nNeither you nor Joshua receive any money'
        
        
        # store some custom variables to the data output
        thisExp.addData('this_offer', this_offer)
        thisExp.addData('your_earnings', your_earnings)
        thisExp.addData('other_earnings', other_earnings)
        fbtxtbox.reset()
        fbtxtbox.setText(fbtxt)
        your_earning_txt.reset()
        your_earning_txt.setText(player_name.text + 's (You) earnings: £' + str(your_earnings))
        other_earning_txt.reset()
        other_earning_txt.setText('Joshuas earnings: £' + str(other_earnings))
        # store start times for outcome
        outcome.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        outcome.tStart = globalClock.getTime(format='float')
        outcome.status = STARTED
        thisExp.addData('outcome.started', outcome.tStart)
        outcome.maxDuration = None
        # keep track of which components have finished
        outcomeComponents = outcome.components
        for thisComponent in outcome.components:
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
        
        # --- Run Routine "outcome" ---
        # if trial has changed, end Routine now
        if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
            continueRoutine = False
        outcome.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 3.0:
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
                if tThisFlipGlobal > fbtxtbox.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    fbtxtbox.tStop = t  # not accounting for scr refresh
                    fbtxtbox.tStopRefresh = tThisFlipGlobal  # on global time
                    fbtxtbox.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fbtxtbox.stopped')
                    # update status
                    fbtxtbox.status = FINISHED
                    fbtxtbox.setAutoDraw(False)
            
            # *your_earning_txt* updates
            
            # if your_earning_txt is starting this frame...
            if your_earning_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                your_earning_txt.frameNStart = frameN  # exact frame index
                your_earning_txt.tStart = t  # local t and not account for scr refresh
                your_earning_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(your_earning_txt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'your_earning_txt.started')
                # update status
                your_earning_txt.status = STARTED
                your_earning_txt.setAutoDraw(True)
            
            # if your_earning_txt is active this frame...
            if your_earning_txt.status == STARTED:
                # update params
                pass
            
            # if your_earning_txt is stopping this frame...
            if your_earning_txt.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > your_earning_txt.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    your_earning_txt.tStop = t  # not accounting for scr refresh
                    your_earning_txt.tStopRefresh = tThisFlipGlobal  # on global time
                    your_earning_txt.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'your_earning_txt.stopped')
                    # update status
                    your_earning_txt.status = FINISHED
                    your_earning_txt.setAutoDraw(False)
            
            # *other_earning_txt* updates
            
            # if other_earning_txt is starting this frame...
            if other_earning_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                other_earning_txt.frameNStart = frameN  # exact frame index
                other_earning_txt.tStart = t  # local t and not account for scr refresh
                other_earning_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(other_earning_txt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'other_earning_txt.started')
                # update status
                other_earning_txt.status = STARTED
                other_earning_txt.setAutoDraw(True)
            
            # if other_earning_txt is active this frame...
            if other_earning_txt.status == STARTED:
                # update params
                pass
            
            # if other_earning_txt is stopping this frame...
            if other_earning_txt.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > other_earning_txt.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    other_earning_txt.tStop = t  # not accounting for scr refresh
                    other_earning_txt.tStopRefresh = tThisFlipGlobal  # on global time
                    other_earning_txt.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'other_earning_txt.stopped')
                    # update status
                    other_earning_txt.status = FINISHED
                    other_earning_txt.setAutoDraw(False)
            
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
                outcome.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in outcome.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "outcome" ---
        for thisComponent in outcome.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for outcome
        outcome.tStop = globalClock.getTime(format='float')
        outcome.tStopRefresh = tThisFlipGlobal
        thisExp.addData('outcome.stopped', outcome.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if outcome.maxDurationReached:
            routineTimer.addTime(-outcome.maxDuration)
        elif outcome.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-3.000000)
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'trials'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "thankyou" ---
    # create an object to store info about Routine thankyou
    thankyou = data.Routine(
        name='thankyou',
        components=[thankstxt, exit_button, end_mouse, your_earning_txt_6, other_earning_txt_6],
    )
    thankyou.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    thankstxt.reset()
    exit_button.reset()
    # setup some python lists for storing info about the end_mouse
    end_mouse.x = []
    end_mouse.y = []
    end_mouse.leftButton = []
    end_mouse.midButton = []
    end_mouse.rightButton = []
    end_mouse.time = []
    end_mouse.clicked_name = []
    gotValidClick = False  # until a click is received
    your_earning_txt_6.reset()
    your_earning_txt_6.setText(player_name.text + 's (You) earnings: £' + str(your_earnings))
    other_earning_txt_6.reset()
    other_earning_txt_6.setText('Joshuas earnings: £' + str(other_earnings))
    # store start times for thankyou
    thankyou.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    thankyou.tStart = globalClock.getTime(format='float')
    thankyou.status = STARTED
    thisExp.addData('thankyou.started', thankyou.tStart)
    thankyou.maxDuration = None
    # keep track of which components have finished
    thankyouComponents = thankyou.components
    for thisComponent in thankyou.components:
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
    
    # --- Run Routine "thankyou" ---
    thankyou.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *thankstxt* updates
        
        # if thankstxt is starting this frame...
        if thankstxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            thankstxt.frameNStart = frameN  # exact frame index
            thankstxt.tStart = t  # local t and not account for scr refresh
            thankstxt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(thankstxt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'thankstxt.started')
            # update status
            thankstxt.status = STARTED
            thankstxt.setAutoDraw(True)
        
        # if thankstxt is active this frame...
        if thankstxt.status == STARTED:
            # update params
            pass
        
        # *exit_button* updates
        
        # if exit_button is starting this frame...
        if exit_button.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            exit_button.frameNStart = frameN  # exact frame index
            exit_button.tStart = t  # local t and not account for scr refresh
            exit_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(exit_button, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'exit_button.started')
            # update status
            exit_button.status = STARTED
            exit_button.setAutoDraw(True)
        
        # if exit_button is active this frame...
        if exit_button.status == STARTED:
            # update params
            pass
        # *end_mouse* updates
        
        # if end_mouse is starting this frame...
        if end_mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            end_mouse.frameNStart = frameN  # exact frame index
            end_mouse.tStart = t  # local t and not account for scr refresh
            end_mouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(end_mouse, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('end_mouse.started', t)
            # update status
            end_mouse.status = STARTED
            end_mouse.mouseClock.reset()
            prevButtonState = end_mouse.getPressed()  # if button is down already this ISN'T a new click
        if end_mouse.status == STARTED:  # only update if started and not finished!
            buttons = end_mouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    clickableList = environmenttools.getFromNames(exit_button, namespace=locals())
                    for obj in clickableList:
                        # is this object clicked on?
                        if obj.contains(end_mouse):
                            gotValidClick = True
                            end_mouse.clicked_name.append(obj.name)
                            end_mouse.clicked_name.append(obj.name)
                    if gotValidClick:
                        x, y = end_mouse.getPos()
                        end_mouse.x.append(x)
                        end_mouse.y.append(y)
                        buttons = end_mouse.getPressed()
                        end_mouse.leftButton.append(buttons[0])
                        end_mouse.midButton.append(buttons[1])
                        end_mouse.rightButton.append(buttons[2])
                        end_mouse.time.append(end_mouse.mouseClock.getTime())
                    if gotValidClick:
                        continueRoutine = False  # end routine on response
        
        # *your_earning_txt_6* updates
        
        # if your_earning_txt_6 is starting this frame...
        if your_earning_txt_6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            your_earning_txt_6.frameNStart = frameN  # exact frame index
            your_earning_txt_6.tStart = t  # local t and not account for scr refresh
            your_earning_txt_6.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(your_earning_txt_6, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'your_earning_txt_6.started')
            # update status
            your_earning_txt_6.status = STARTED
            your_earning_txt_6.setAutoDraw(True)
        
        # if your_earning_txt_6 is active this frame...
        if your_earning_txt_6.status == STARTED:
            # update params
            pass
        
        # *other_earning_txt_6* updates
        
        # if other_earning_txt_6 is starting this frame...
        if other_earning_txt_6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            other_earning_txt_6.frameNStart = frameN  # exact frame index
            other_earning_txt_6.tStart = t  # local t and not account for scr refresh
            other_earning_txt_6.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(other_earning_txt_6, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'other_earning_txt_6.started')
            # update status
            other_earning_txt_6.status = STARTED
            other_earning_txt_6.setAutoDraw(True)
        
        # if other_earning_txt_6 is active this frame...
        if other_earning_txt_6.status == STARTED:
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
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            thankyou.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in thankyou.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "thankyou" ---
    for thisComponent in thankyou.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for thankyou
    thankyou.tStop = globalClock.getTime(format='float')
    thankyou.tStopRefresh = tThisFlipGlobal
    thisExp.addData('thankyou.stopped', thankyou.tStop)
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('end_mouse.x', end_mouse.x)
    thisExp.addData('end_mouse.y', end_mouse.y)
    thisExp.addData('end_mouse.leftButton', end_mouse.leftButton)
    thisExp.addData('end_mouse.midButton', end_mouse.midButton)
    thisExp.addData('end_mouse.rightButton', end_mouse.rightButton)
    thisExp.addData('end_mouse.time', end_mouse.time)
    thisExp.addData('end_mouse.clicked_name', end_mouse.clicked_name)
    thisExp.nextEntry()
    # the Routine "thankyou" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
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
