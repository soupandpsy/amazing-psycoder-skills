# Source: phone_a_friend (demos/phone_a_friend)
# Project URL: https://gitlab.pavlovia.org/demos/phone_a_friend
# Original file: phone_a_friend_lastrun.py
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2025.2.0),
    on Wed  3 Sep 20:34:49 2025
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
psychopyVersion = '2025.2.0'
expName = 'phone_a_friend'  # from the Builder filename that created this script
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
_winSize = (1024, 768)
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
        originPath='/Users/Becca/Desktop/Demos/Cue Task Demo/phone_a_friend_lastrun.py',
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
            monitor='testMonitor', color=(-0.1216, 0.0039, 0.1294), colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = (-0.1216, 0.0039, 0.1294)
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
    # update experiment info
    expInfo['date'] = data.getDateStr()
    expInfo['expName'] = expName
    expInfo['expVersion'] = expVersion
    expInfo['psychopyVersion'] = psychopyVersion
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
    background = visual.ImageStim(
        win=win,
        name='background', 
        image='rudy-issa-jedKD4yaTvk-unsplash.jpg', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(1.7, 1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    intro_resp = keyboard.Keyboard(deviceName='defaultKeyboard')
    instructionsintro = visual.TextBox2(
         win, text="On each trial you will be asked a question. \n\nIf you don't know the answer you can phone a friend. \n\nYou can do this only 10 times.\n\nPress space to start", placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(1, 0.8), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='white', borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instructionsintro',
         depth=-2, autoLog=True,
    )
    
    # --- Initialize components for Routine "trial" ---
    background_2 = visual.ImageStim(
        win=win,
        name='background_2', 
        image='rudy-issa-jedKD4yaTvk-unsplash.jpg', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(1.7, 1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    instr_txt_2 = visual.TextBox2(
         win, text='Type the answer and press enter to submit:', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.4), draggable=False,      letterHeight=0.05,
         size=(1, 0.2), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='white', borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instr_txt_2',
         depth=-1, autoLog=True,
    )
    this_question_text = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.2), draggable=False,      letterHeight=0.05,
         size=(1, 0.2), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[1.0000, 0.9608, 0.8824], borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='this_question_text',
         depth=-2, autoLog=True,
    )
    hint_button = visual.TextBox2(
         win, text='Click here to phone a friend', placeholder='Type here...', font='Arial',
         ori=0.0, pos=[0,0], draggable=False,      letterHeight=0.05,
         size=(1, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=(-0.0667, 0.0667, 0.2000), borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='hint_button',
         depth=-3, autoLog=True,
    )
    answer = visual.TextBox2(
         win, text=None, placeholder=None, font='Arial',
         ori=0.0, pos=(0, -0.05), draggable=False,      letterHeight=0.05,
         size=(1, 0.2), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='white', borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=True,
         name='answer',
         depth=-4, autoLog=True,
    )
    key_resp = keyboard.Keyboard(deviceName='defaultKeyboard')
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()
    call_tracker = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, -0.45), draggable=False,      letterHeight=0.05,
         size=(1, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[0.6078, -0.2784, -0.2784], borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='call_tracker',
         depth=-7, autoLog=True,
    )
    
    # --- Initialize components for Routine "show_hint" ---
    background_3 = visual.ImageStim(
        win=win,
        name='background_3', 
        image='rudy-issa-jedKD4yaTvk-unsplash.jpg', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(1.7, 1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    instr_txt = visual.TextBox2(
         win, text='Type your answer if you know and press enter (if you don’t know just press enter):', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.4), draggable=False,      letterHeight=0.05,
         size=(1, 0.2), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='white', borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instr_txt',
         depth=-1, autoLog=True,
    )
    # Run 'Begin Experiment' code from code
    # track how many times they call a friend
    n_calls = 0
    hint_x =0 #onscreen
    
    # to balance valid and invalid cues
    n_valid = 5
    n_invalid = 5
    limit = 10
    calls_remaining = limit
    
    cue_types = []
    for n in range(n_valid):
        cue_types.append('valid')
    for n in range(n_invalid):
        cue_types.append('invalid')
    
    shuffle(cue_types)
    #cue_types is a list containing the balance of valid and invalid labels
        
    this_question_text_3 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0.2), draggable=False,      letterHeight=0.05,
         size=(1, 0.2), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[1.0000, 0.9608, 0.8824], borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='this_question_text_3',
         depth=-3, autoLog=True,
    )
    friends_hint = visual.TextBox2(
         win, text='', placeholder=None, font='Arial',
         ori=0.0, pos=(0, -0.05), draggable=False,      letterHeight=0.05,
         size=(1, 0.2), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='white', borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='friends_hint',
         depth=-4, autoLog=True,
    )
    answer_2 = visual.TextBox2(
         win, text=None, placeholder=None, font='Arial',
         ori=0.0, pos=(0, -0.2), draggable=False,      letterHeight=0.05,
         size=(1, 0.2), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='white', borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=True,
         name='answer_2',
         depth=-5, autoLog=True,
    )
    key_resp_2 = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "warn_user" ---
    background_4 = visual.ImageStim(
        win=win,
        name='background_4', 
        image='rudy-issa-jedKD4yaTvk-unsplash.jpg', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(1.7, 1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    textbox = visual.TextBox2(
         win, text='YOU HAVE NO CALLS LEFT', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(0.5, 0.5), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[1.0000, -1.0000, -1.0000], borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='textbox',
         depth=-1, autoLog=True,
    )
    
    # --- Initialize components for Routine "bye" ---
    background_5 = visual.ImageStim(
        win=win,
        name='background_5', 
        image='rudy-issa-jedKD4yaTvk-unsplash.jpg', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(1.7, 1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    intro_resp_2 = keyboard.Keyboard(deviceName='defaultKeyboard')
    instructionsintro_2 = visual.TextBox2(
         win, text='Thanks for taking part!', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(1, 0.8), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='white', borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instructionsintro_2',
         depth=-2, autoLog=True,
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
        components=[background, intro_resp, instructionsintro],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for intro_resp
    intro_resp.keys = []
    intro_resp.rt = []
    _intro_resp_allKeys = []
    instructionsintro.reset()
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
    thisExp.currentRoutine = instructions
    instructions.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *background* updates
        
        # if background is starting this frame...
        if background.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            background.frameNStart = frameN  # exact frame index
            background.tStart = t  # local t and not account for scr refresh
            background.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(background, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'background.started')
            # update status
            background.status = STARTED
            background.setAutoDraw(True)
        
        # if background is active this frame...
        if background.status == STARTED:
            # update params
            pass
        
        # *intro_resp* updates
        waitOnFlip = False
        
        # if intro_resp is starting this frame...
        if intro_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            intro_resp.frameNStart = frameN  # exact frame index
            intro_resp.tStart = t  # local t and not account for scr refresh
            intro_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(intro_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'intro_resp.started')
            # update status
            intro_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(intro_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(intro_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if intro_resp.status == STARTED and not waitOnFlip:
            theseKeys = intro_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _intro_resp_allKeys.extend(theseKeys)
            if len(_intro_resp_allKeys):
                intro_resp.keys = _intro_resp_allKeys[-1].name  # just the last key pressed
                intro_resp.rt = _intro_resp_allKeys[-1].rt
                intro_resp.duration = _intro_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # *instructionsintro* updates
        
        # if instructionsintro is starting this frame...
        if instructionsintro.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructionsintro.frameNStart = frameN  # exact frame index
            instructionsintro.tStart = t  # local t and not account for scr refresh
            instructionsintro.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructionsintro, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instructionsintro.started')
            # update status
            instructionsintro.status = STARTED
            instructionsintro.setAutoDraw(True)
        
        # if instructionsintro is active this frame...
        if instructionsintro.status == STARTED:
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
                currentRoutine=instructions,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            instructions.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if instructions.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
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
    if intro_resp.keys in ['', [], None]:  # No response was made
        intro_resp.keys = None
    thisExp.addData('intro_resp.keys',intro_resp.keys)
    if intro_resp.keys != None:  # we had a response
        thisExp.addData('intro_resp.rt', intro_resp.rt)
        thisExp.addData('intro_resp.duration', intro_resp.duration)
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
        trialList=data.importConditions('conditions.xlsx'), 
        seed=None, 
        isTrials=True, 
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
            components=[background_2, instr_txt_2, this_question_text, hint_button, answer, key_resp, mouse, call_tracker],
        )
        trial.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        instr_txt_2.reset()
        this_question_text.reset()
        this_question_text.setText(this_question)
        hint_button.reset()
        hint_button.setPos((hint_x,-0.35))
        answer.reset()
        answer.setText('')
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # setup some python lists for storing info about the mouse
        mouse.x = []
        mouse.y = []
        mouse.leftButton = []
        mouse.midButton = []
        mouse.rightButton = []
        mouse.time = []
        mouse.clicked_name = []
        gotValidClick = False  # until a click is received
        call_tracker.reset()
        call_tracker.setText('Calls remaining: ' + str(calls_remaining))
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
        thisExp.currentRoutine = trial
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
            
            # *background_2* updates
            
            # if background_2 is starting this frame...
            if background_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                background_2.frameNStart = frameN  # exact frame index
                background_2.tStart = t  # local t and not account for scr refresh
                background_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(background_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'background_2.started')
                # update status
                background_2.status = STARTED
                background_2.setAutoDraw(True)
            
            # if background_2 is active this frame...
            if background_2.status == STARTED:
                # update params
                pass
            
            # *instr_txt_2* updates
            
            # if instr_txt_2 is starting this frame...
            if instr_txt_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instr_txt_2.frameNStart = frameN  # exact frame index
                instr_txt_2.tStart = t  # local t and not account for scr refresh
                instr_txt_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instr_txt_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instr_txt_2.started')
                # update status
                instr_txt_2.status = STARTED
                instr_txt_2.setAutoDraw(True)
            
            # if instr_txt_2 is active this frame...
            if instr_txt_2.status == STARTED:
                # update params
                pass
            
            # *this_question_text* updates
            
            # if this_question_text is starting this frame...
            if this_question_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                this_question_text.frameNStart = frameN  # exact frame index
                this_question_text.tStart = t  # local t and not account for scr refresh
                this_question_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(this_question_text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'this_question_text.started')
                # update status
                this_question_text.status = STARTED
                this_question_text.setAutoDraw(True)
            
            # if this_question_text is active this frame...
            if this_question_text.status == STARTED:
                # update params
                pass
            
            # *hint_button* updates
            
            # if hint_button is starting this frame...
            if hint_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                hint_button.frameNStart = frameN  # exact frame index
                hint_button.tStart = t  # local t and not account for scr refresh
                hint_button.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(hint_button, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'hint_button.started')
                # update status
                hint_button.status = STARTED
                hint_button.setAutoDraw(True)
            
            # if hint_button is active this frame...
            if hint_button.status == STARTED:
                # update params
                pass
            
            # *answer* updates
            
            # if answer is starting this frame...
            if answer.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                answer.frameNStart = frameN  # exact frame index
                answer.tStart = t  # local t and not account for scr refresh
                answer.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(answer, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'answer.started')
                # update status
                answer.status = STARTED
                answer.setAutoDraw(True)
            
            # if answer is active this frame...
            if answer.status == STARTED:
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
                theseKeys = key_resp.getKeys(keyList=['return'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    key_resp.duration = _key_resp_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
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
                        clickableList = environmenttools.getFromNames(hint_button, namespace=locals())
                        for obj in clickableList:
                            # is this object clicked on?
                            if obj.contains(mouse):
                                gotValidClick = True
                                mouse.clicked_name.append(obj.name)
                        if not gotValidClick:
                            mouse.clicked_name.append(None)
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
            
            # *call_tracker* updates
            
            # if call_tracker is starting this frame...
            if call_tracker.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                call_tracker.frameNStart = frameN  # exact frame index
                call_tracker.tStart = t  # local t and not account for scr refresh
                call_tracker.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(call_tracker, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'call_tracker.started')
                # update status
                call_tracker.status = STARTED
                call_tracker.setAutoDraw(True)
            
            # if call_tracker is active this frame...
            if call_tracker.status == STARTED:
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
                    currentRoutine=trial,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                trial.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if trial.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
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
        trials.addData('answer.text',answer.text)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
        trials.addData('key_resp.keys',key_resp.keys)
        if key_resp.keys != None:  # we had a response
            trials.addData('key_resp.rt', key_resp.rt)
            trials.addData('key_resp.duration', key_resp.duration)
        # store data for trials (TrialHandler)
        trials.addData('mouse.x', mouse.x)
        trials.addData('mouse.y', mouse.y)
        trials.addData('mouse.leftButton', mouse.leftButton)
        trials.addData('mouse.midButton', mouse.midButton)
        trials.addData('mouse.rightButton', mouse.rightButton)
        trials.addData('mouse.time', mouse.time)
        trials.addData('mouse.clicked_name', mouse.clicked_name)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "show_hint" ---
        # create an object to store info about Routine show_hint
        show_hint = data.Routine(
            name='show_hint',
            components=[background_3, instr_txt, this_question_text_3, friends_hint, answer_2, key_resp_2],
        )
        show_hint.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        instr_txt.reset()
        # Run 'Begin Routine' code from code
        # skip this routine if the participant did press y or n 
        if key_resp.keys: # no key was pressed:
            continueRoutine = False
        else:
            n_calls += 1
            calls_remaining = limit - n_calls
        
        # warn the participant if they run out of calls
        warn = False
        if n_calls >= limit :
            continueRoutine = False
            warn = True
            hint_x = -500 # offscreen
        
        # randomly selecting the cue type 
        # note : later we can balance this 
        #cue_type = ['valid', 'invalid']
        
        # shuffle whole list
        shuffle(cue_types)
        
        cue_type = None
        # sample the last cue type
        if len(cue_types) >0 : # if there are any cues left
            cue_type = cue_types[-1]
            if cue_type == 'valid':
                this_hint = this_cue_valid
            else:
                this_hint = this_cue_invalid
                
            # sample without replacement for balanced sampling
            cue_types.pop()
        
        # save to data file 
        thisExp.addData('cue_type', cue_type)
        thisExp.addData('this_hint', this_hint)
        thisExp.addData('n_calls', n_calls)
        thisExp.addData('calls_remaining', calls_remaining)
        this_question_text_3.reset()
        this_question_text_3.setText(this_question)
        friends_hint.reset()
        friends_hint.setText("Answer: " + this_hint)
        answer_2.reset()
        # create starting attributes for key_resp_2
        key_resp_2.keys = []
        key_resp_2.rt = []
        _key_resp_2_allKeys = []
        # store start times for show_hint
        show_hint.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        show_hint.tStart = globalClock.getTime(format='float')
        show_hint.status = STARTED
        thisExp.addData('show_hint.started', show_hint.tStart)
        show_hint.maxDuration = None
        # keep track of which components have finished
        show_hintComponents = show_hint.components
        for thisComponent in show_hint.components:
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
        
        # --- Run Routine "show_hint" ---
        thisExp.currentRoutine = show_hint
        show_hint.forceEnded = routineForceEnded = not continueRoutine
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
            
            # *background_3* updates
            
            # if background_3 is starting this frame...
            if background_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                background_3.frameNStart = frameN  # exact frame index
                background_3.tStart = t  # local t and not account for scr refresh
                background_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(background_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'background_3.started')
                # update status
                background_3.status = STARTED
                background_3.setAutoDraw(True)
            
            # if background_3 is active this frame...
            if background_3.status == STARTED:
                # update params
                pass
            
            # *instr_txt* updates
            
            # if instr_txt is starting this frame...
            if instr_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instr_txt.frameNStart = frameN  # exact frame index
                instr_txt.tStart = t  # local t and not account for scr refresh
                instr_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instr_txt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instr_txt.started')
                # update status
                instr_txt.status = STARTED
                instr_txt.setAutoDraw(True)
            
            # if instr_txt is active this frame...
            if instr_txt.status == STARTED:
                # update params
                pass
            
            # *this_question_text_3* updates
            
            # if this_question_text_3 is starting this frame...
            if this_question_text_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                this_question_text_3.frameNStart = frameN  # exact frame index
                this_question_text_3.tStart = t  # local t and not account for scr refresh
                this_question_text_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(this_question_text_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'this_question_text_3.started')
                # update status
                this_question_text_3.status = STARTED
                this_question_text_3.setAutoDraw(True)
            
            # if this_question_text_3 is active this frame...
            if this_question_text_3.status == STARTED:
                # update params
                pass
            
            # *friends_hint* updates
            
            # if friends_hint is starting this frame...
            if friends_hint.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                friends_hint.frameNStart = frameN  # exact frame index
                friends_hint.tStart = t  # local t and not account for scr refresh
                friends_hint.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(friends_hint, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'friends_hint.started')
                # update status
                friends_hint.status = STARTED
                friends_hint.setAutoDraw(True)
            
            # if friends_hint is active this frame...
            if friends_hint.status == STARTED:
                # update params
                pass
            
            # *answer_2* updates
            
            # if answer_2 is starting this frame...
            if answer_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                answer_2.frameNStart = frameN  # exact frame index
                answer_2.tStart = t  # local t and not account for scr refresh
                answer_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(answer_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'answer_2.started')
                # update status
                answer_2.status = STARTED
                answer_2.setAutoDraw(True)
            
            # if answer_2 is active this frame...
            if answer_2.status == STARTED:
                # update params
                pass
            
            # *key_resp_2* updates
            waitOnFlip = False
            
            # if key_resp_2 is starting this frame...
            if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.tStart = t  # local t and not account for scr refresh
                key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_2.started')
                # update status
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_2.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_2.getKeys(keyList=['return'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_2_allKeys.extend(theseKeys)
                if len(_key_resp_2_allKeys):
                    key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                    key_resp_2.rt = _key_resp_2_allKeys[-1].rt
                    key_resp_2.duration = _key_resp_2_allKeys[-1].duration
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
                    currentRoutine=show_hint,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                show_hint.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if show_hint.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in show_hint.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "show_hint" ---
        for thisComponent in show_hint.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for show_hint
        show_hint.tStop = globalClock.getTime(format='float')
        show_hint.tStopRefresh = tThisFlipGlobal
        thisExp.addData('show_hint.stopped', show_hint.tStop)
        trials.addData('answer_2.text',answer_2.text)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys = None
        trials.addData('key_resp_2.keys',key_resp_2.keys)
        if key_resp_2.keys != None:  # we had a response
            trials.addData('key_resp_2.rt', key_resp_2.rt)
            trials.addData('key_resp_2.duration', key_resp_2.duration)
        # the Routine "show_hint" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "warn_user" ---
        # create an object to store info about Routine warn_user
        warn_user = data.Routine(
            name='warn_user',
            components=[background_4, textbox],
        )
        warn_user.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        textbox.reset()
        # store start times for warn_user
        warn_user.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        warn_user.tStart = globalClock.getTime(format='float')
        warn_user.status = STARTED
        thisExp.addData('warn_user.started', warn_user.tStart)
        warn_user.maxDuration = None
        # skip Routine warn_user if its 'Skip if' condition is True
        warn_user.skipped = continueRoutine and not (warn == 0)
        continueRoutine = warn_user.skipped
        # keep track of which components have finished
        warn_userComponents = warn_user.components
        for thisComponent in warn_user.components:
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
        
        # --- Run Routine "warn_user" ---
        thisExp.currentRoutine = warn_user
        warn_user.forceEnded = routineForceEnded = not continueRoutine
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
            
            # *background_4* updates
            
            # if background_4 is starting this frame...
            if background_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                background_4.frameNStart = frameN  # exact frame index
                background_4.tStart = t  # local t and not account for scr refresh
                background_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(background_4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'background_4.started')
                # update status
                background_4.status = STARTED
                background_4.setAutoDraw(True)
            
            # if background_4 is active this frame...
            if background_4.status == STARTED:
                # update params
                pass
            
            # if background_4 is stopping this frame...
            if background_4.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > background_4.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    background_4.tStop = t  # not accounting for scr refresh
                    background_4.tStopRefresh = tThisFlipGlobal  # on global time
                    background_4.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'background_4.stopped')
                    # update status
                    background_4.status = FINISHED
                    background_4.setAutoDraw(False)
            
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
                if tThisFlipGlobal > textbox.tStartRefresh + 1.0-frameTolerance:
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
                    timers=[routineTimer, globalClock], 
                    currentRoutine=warn_user,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                warn_user.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if warn_user.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in warn_user.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "warn_user" ---
        for thisComponent in warn_user.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for warn_user
        warn_user.tStop = globalClock.getTime(format='float')
        warn_user.tStopRefresh = tThisFlipGlobal
        thisExp.addData('warn_user.stopped', warn_user.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if warn_user.maxDurationReached:
            routineTimer.addTime(-warn_user.maxDuration)
        elif warn_user.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
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
    
    # --- Prepare to start Routine "bye" ---
    # create an object to store info about Routine bye
    bye = data.Routine(
        name='bye',
        components=[background_5, intro_resp_2, instructionsintro_2],
    )
    bye.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for intro_resp_2
    intro_resp_2.keys = []
    intro_resp_2.rt = []
    _intro_resp_2_allKeys = []
    instructionsintro_2.reset()
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
    thisExp.currentRoutine = bye
    bye.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *background_5* updates
        
        # if background_5 is starting this frame...
        if background_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            background_5.frameNStart = frameN  # exact frame index
            background_5.tStart = t  # local t and not account for scr refresh
            background_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(background_5, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'background_5.started')
            # update status
            background_5.status = STARTED
            background_5.setAutoDraw(True)
        
        # if background_5 is active this frame...
        if background_5.status == STARTED:
            # update params
            pass
        
        # *intro_resp_2* updates
        waitOnFlip = False
        
        # if intro_resp_2 is starting this frame...
        if intro_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            intro_resp_2.frameNStart = frameN  # exact frame index
            intro_resp_2.tStart = t  # local t and not account for scr refresh
            intro_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(intro_resp_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'intro_resp_2.started')
            # update status
            intro_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(intro_resp_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(intro_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if intro_resp_2.status == STARTED and not waitOnFlip:
            theseKeys = intro_resp_2.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _intro_resp_2_allKeys.extend(theseKeys)
            if len(_intro_resp_2_allKeys):
                intro_resp_2.keys = _intro_resp_2_allKeys[-1].name  # just the last key pressed
                intro_resp_2.rt = _intro_resp_2_allKeys[-1].rt
                intro_resp_2.duration = _intro_resp_2_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # *instructionsintro_2* updates
        
        # if instructionsintro_2 is starting this frame...
        if instructionsintro_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructionsintro_2.frameNStart = frameN  # exact frame index
            instructionsintro_2.tStart = t  # local t and not account for scr refresh
            instructionsintro_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructionsintro_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instructionsintro_2.started')
            # update status
            instructionsintro_2.status = STARTED
            instructionsintro_2.setAutoDraw(True)
        
        # if instructionsintro_2 is active this frame...
        if instructionsintro_2.status == STARTED:
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
                currentRoutine=bye,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            bye.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if bye.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
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
    # check responses
    if intro_resp_2.keys in ['', [], None]:  # No response was made
        intro_resp_2.keys = None
    thisExp.addData('intro_resp_2.keys',intro_resp_2.keys)
    if intro_resp_2.keys != None:  # we had a response
        thisExp.addData('intro_resp_2.rt', intro_resp_2.rt)
        thisExp.addData('intro_resp_2.duration', intro_resp_2.duration)
    thisExp.nextEntry()
    # the Routine "bye" was not non-slip safe, so reset the non-slip timer
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
