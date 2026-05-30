# Source: change_detection (demos/change_detection)
# Project URL: https://gitlab.pavlovia.org/demos/change_detection
# Original file: change_detection_lastrun.py
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.1.5),
    on October 17, 2024, at 00:01
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

import psychopy.iohub as io
from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.1.5'
expName = 'change_detection'  # from the Builder filename that created this script
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
_winSize = (1024, 768)
_loggingLevel = logging.getLevel('warning')
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']
    # override logging level
    _loggingLevel = logging.getLevel(
        prefs.piloting['pilotLoggingLevel']
    )

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
        originPath='G:\\Shared drives\\Science\\Pavlovia Demos\\change detection\\change_detection_lastrun.py',
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
    # this outputs to the screen, not a file
    logging.console.setLevel(_loggingLevel)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=_loggingLevel)
    
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
            winType='pyglet', allowStencil=True,
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
            win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.mouseVisible = False
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
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    ioSession = '1'
    if 'session' in expInfo:
        ioSession = str(expInfo['session'])
    ioServer = io.launchHubServer(window=win, **ioConfig)
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
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
    if deviceManager.getDevice('next_resp') is None:
        # initialise next_resp
        next_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='next_resp',
        )
    if deviceManager.getDevice('localisation_resp') is None:
        # initialise localisation_resp
        localisation_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='localisation_resp',
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
    
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # prevent components from auto-drawing
    win.stashAutoDraw()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # flip the screen
        win.flip()
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # restore auto-drawn components
    win.retrieveAutoDraw()
    # reset any timers
    for timer in timers:
        timer.reset()


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
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
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
    welcometxt = visual.TextBox2(
         win, text='In this task you will see six colored squares. \n\nAfter viewing the squares you will see on colored square in a particular location. \n\nYour task is to judge if that colored square did appear in that location. \n\nPress Y if that color square did occur in that location\nPress N if that color square did not appear in that location\n\nPress space to start', placeholder='Type here...', font='Arial',
         pos=(0, 0),     letterHeight=0.05,
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
         name='welcometxt',
         depth=0, autoLog=True,
    )
    start_resp = keyboard.Keyboard(deviceName='start_resp')
    
    # --- Initialize components for Routine "trial" ---
    square1 = visual.Rect(
        win=win, name='square1',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    square2 = visual.Rect(
        win=win, name='square2',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    square3 = visual.Rect(
        win=win, name='square3',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    square4 = visual.Rect(
        win=win, name='square4',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    square5 = visual.Rect(
        win=win, name='square5',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-4.0, interpolate=True)
    square6 = visual.Rect(
        win=win, name='square6',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-5.0, interpolate=True)
    
    # --- Initialize components for Routine "show_test" ---
    question = visual.TextBox2(
         win, text='Did this color square appear in this location? \n\nPress Y for yes \nPress N for no', placeholder='Type here...', font='Arial',
         pos=(0, 0.45),     letterHeight=0.05,
         size=(1, 0.1), borderWidth=2.0,
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
         depth=-1, autoLog=True,
    )
    test_square = visual.Rect(
        win=win, name='test_square',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
    # --- Initialize components for Routine "feedback" ---
    fbtextbox = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         pos=(0, 0),     letterHeight=0.05,
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
         name='fbtextbox',
         depth=-1, autoLog=True,
    )
    
    # --- Initialize components for Routine "next_instr" ---
    nextinstrtxt = visual.TextBox2(
         win, text='Great! \n\nThis time you will see six squares folowed by another six squares. One of the squares will have changed in color, use the keys 1 - 6 on your keyboard to indicate which has changed. \n\nPress space to start', placeholder='Type here...', font='Arial',
         pos=(0, 0),     letterHeight=0.05,
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
         name='nextinstrtxt',
         depth=0, autoLog=True,
    )
    next_resp = keyboard.Keyboard(deviceName='next_resp')
    
    # --- Initialize components for Routine "trial" ---
    square1 = visual.Rect(
        win=win, name='square1',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    square2 = visual.Rect(
        win=win, name='square2',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    square3 = visual.Rect(
        win=win, name='square3',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    square4 = visual.Rect(
        win=win, name='square4',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    square5 = visual.Rect(
        win=win, name='square5',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-4.0, interpolate=True)
    square6 = visual.Rect(
        win=win, name='square6',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-5.0, interpolate=True)
    
    # --- Initialize components for Routine "localisation_test" ---
    square1_2 = visual.Rect(
        win=win, name='square1_2',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    square2_2 = visual.Rect(
        win=win, name='square2_2',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    square3_2 = visual.Rect(
        win=win, name='square3_2',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    square4_2 = visual.Rect(
        win=win, name='square4_2',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    square5_2 = visual.Rect(
        win=win, name='square5_2',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-4.0, interpolate=True)
    square6_2 = visual.Rect(
        win=win, name='square6_2',
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-5.0, interpolate=True)
    one_label = visual.TextBox2(
         win, text='1', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.05,
         size=(0.1, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='one_label',
         depth=-6, autoLog=True,
    )
    two_label = visual.TextBox2(
         win, text='2', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.05,
         size=(0.1, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='two_label',
         depth=-7, autoLog=True,
    )
    three_label = visual.TextBox2(
         win, text='3', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.05,
         size=(0.1, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='three_label',
         depth=-8, autoLog=True,
    )
    four_label = visual.TextBox2(
         win, text='4', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.05,
         size=(0.1, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='four_label',
         depth=-9, autoLog=True,
    )
    five_label = visual.TextBox2(
         win, text='5', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.05,
         size=(0.1, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='five_label',
         depth=-10, autoLog=True,
    )
    six_label = visual.TextBox2(
         win, text='5', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.05,
         size=(0.1, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='six_label',
         depth=-11, autoLog=True,
    )
    localisation_resp = keyboard.Keyboard(deviceName='localisation_resp')
    textbox_2 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         pos=(0, 0),     letterHeight=0.05,
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
         name='textbox_2',
         depth=-13, autoLog=True,
    )
    
    # --- Initialize components for Routine "localisation_feedback" ---
    fbtextbox_2 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         pos=(0, 0),     letterHeight=0.05,
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
         name='fbtextbox_2',
         depth=-1, autoLog=True,
    )
    
    # --- Initialize components for Routine "bye" ---
    textbox = visual.TextBox2(
         win, text='That is the end - goodbye!', placeholder='Type here...', font='Arial',
         pos=(0, 0),     letterHeight=0.05,
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
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('instructions.started', globalClock.getTime(format='float'))
    welcometxt.reset()
    # create starting attributes for start_resp
    start_resp.keys = []
    start_resp.rt = []
    _start_resp_allKeys = []
    # keep track of which components have finished
    instructionsComponents = [welcometxt, start_resp]
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
    frameN = -1
    
    # --- Run Routine "instructions" ---
    routineForceEnded = not continueRoutine
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
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructionsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructions" ---
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('instructions.stopped', globalClock.getTime(format='float'))
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
    change_trials = data.TrialHandler(nReps=1.0, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('code/sampled_circle_points_with_colors.csv', selection='1'),
        seed=None, name='change_trials')
    thisExp.addLoop(change_trials)  # add the loop to the experiment
    thisChange_trial = change_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisChange_trial.rgb)
    if thisChange_trial != None:
        for paramName in thisChange_trial:
            globals()[paramName] = thisChange_trial[paramName]
    
    for thisChange_trial in change_trials:
        currentLoop = change_trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisChange_trial.rgb)
        if thisChange_trial != None:
            for paramName in thisChange_trial:
                globals()[paramName] = thisChange_trial[paramName]
        
        # --- Prepare to start Routine "trial" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('trial.started', globalClock.getTime(format='float'))
        square1.setFillColor(color1)
        square1.setPos((x1, y1))
        square1.setLineColor(color1)
        square2.setFillColor(color2)
        square2.setPos((x2, y2))
        square2.setLineColor(color2)
        square3.setFillColor(color3)
        square3.setPos((x3, y3))
        square3.setLineColor(color3)
        square4.setFillColor(color4)
        square4.setPos((x4, y4))
        square4.setLineColor(color4)
        square5.setFillColor(color5)
        square5.setPos((x5, y5))
        square5.setLineColor(color5)
        square6.setFillColor(color6)
        square6.setPos((x6, y6))
        square6.setLineColor(color6)
        # keep track of which components have finished
        trialComponents = [square1, square2, square3, square4, square5, square6]
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
        frameN = -1
        
        # --- Run Routine "trial" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *square1* updates
            
            # if square1 is starting this frame...
            if square1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square1.frameNStart = frameN  # exact frame index
                square1.tStart = t  # local t and not account for scr refresh
                square1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square1.started')
                # update status
                square1.status = STARTED
                square1.setAutoDraw(True)
            
            # if square1 is active this frame...
            if square1.status == STARTED:
                # update params
                pass
            
            # if square1 is stopping this frame...
            if square1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square1.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square1.tStop = t  # not accounting for scr refresh
                    square1.tStopRefresh = tThisFlipGlobal  # on global time
                    square1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square1.stopped')
                    # update status
                    square1.status = FINISHED
                    square1.setAutoDraw(False)
            
            # *square2* updates
            
            # if square2 is starting this frame...
            if square2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square2.frameNStart = frameN  # exact frame index
                square2.tStart = t  # local t and not account for scr refresh
                square2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square2.started')
                # update status
                square2.status = STARTED
                square2.setAutoDraw(True)
            
            # if square2 is active this frame...
            if square2.status == STARTED:
                # update params
                pass
            
            # if square2 is stopping this frame...
            if square2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square2.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square2.tStop = t  # not accounting for scr refresh
                    square2.tStopRefresh = tThisFlipGlobal  # on global time
                    square2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square2.stopped')
                    # update status
                    square2.status = FINISHED
                    square2.setAutoDraw(False)
            
            # *square3* updates
            
            # if square3 is starting this frame...
            if square3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square3.frameNStart = frameN  # exact frame index
                square3.tStart = t  # local t and not account for scr refresh
                square3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square3.started')
                # update status
                square3.status = STARTED
                square3.setAutoDraw(True)
            
            # if square3 is active this frame...
            if square3.status == STARTED:
                # update params
                pass
            
            # if square3 is stopping this frame...
            if square3.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square3.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square3.tStop = t  # not accounting for scr refresh
                    square3.tStopRefresh = tThisFlipGlobal  # on global time
                    square3.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square3.stopped')
                    # update status
                    square3.status = FINISHED
                    square3.setAutoDraw(False)
            
            # *square4* updates
            
            # if square4 is starting this frame...
            if square4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square4.frameNStart = frameN  # exact frame index
                square4.tStart = t  # local t and not account for scr refresh
                square4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square4.started')
                # update status
                square4.status = STARTED
                square4.setAutoDraw(True)
            
            # if square4 is active this frame...
            if square4.status == STARTED:
                # update params
                pass
            
            # if square4 is stopping this frame...
            if square4.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square4.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square4.tStop = t  # not accounting for scr refresh
                    square4.tStopRefresh = tThisFlipGlobal  # on global time
                    square4.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square4.stopped')
                    # update status
                    square4.status = FINISHED
                    square4.setAutoDraw(False)
            
            # *square5* updates
            
            # if square5 is starting this frame...
            if square5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square5.frameNStart = frameN  # exact frame index
                square5.tStart = t  # local t and not account for scr refresh
                square5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square5, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square5.started')
                # update status
                square5.status = STARTED
                square5.setAutoDraw(True)
            
            # if square5 is active this frame...
            if square5.status == STARTED:
                # update params
                pass
            
            # if square5 is stopping this frame...
            if square5.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square5.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square5.tStop = t  # not accounting for scr refresh
                    square5.tStopRefresh = tThisFlipGlobal  # on global time
                    square5.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square5.stopped')
                    # update status
                    square5.status = FINISHED
                    square5.setAutoDraw(False)
            
            # *square6* updates
            
            # if square6 is starting this frame...
            if square6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square6.frameNStart = frameN  # exact frame index
                square6.tStart = t  # local t and not account for scr refresh
                square6.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square6, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square6.started')
                # update status
                square6.status = STARTED
                square6.setAutoDraw(True)
            
            # if square6 is active this frame...
            if square6.status == STARTED:
                # update params
                pass
            
            # if square6 is stopping this frame...
            if square6.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square6.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square6.tStop = t  # not accounting for scr refresh
                    square6.tStopRefresh = tThisFlipGlobal  # on global time
                    square6.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square6.stopped')
                    # update status
                    square6.status = FINISHED
                    square6.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial" ---
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('trial.stopped', globalClock.getTime(format='float'))
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.500000)
        
        # --- Prepare to start Routine "show_test" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('show_test.started', globalClock.getTime(format='float'))
        # Run 'Begin Routine' code from code
        possible_sets = [[x1, y1, color1], [x2, y2, color2], [x3, y3, color3],
            [x4, y4, color4], [x5, y5, color5]]
        
        shuffle(possible_sets)
        
        # if the condition is the same set the test such that the color in this location is the same
        if condition_label == 'same':
            xtest = possible_sets[0][0]
            ytest = possible_sets[0][1]
            colortest = possible_sets[0][2]
        else:
            xtest = possible_sets[0][0]
            ytest = possible_sets[0][1]
            colortest = possible_sets[1][2]# else set the color to be different
        # save to the data file
        thisExp.addData('xtest', xtest)
        thisExp.addData('ytest', ytest)
        thisExp.addData('colortest', colortest)
        question.reset()
        test_square.setFillColor(colortest)
        test_square.setPos((xtest, ytest))
        test_square.setLineColor(colortest)
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # keep track of which components have finished
        show_testComponents = [question, test_square, key_resp]
        for thisComponent in show_testComponents:
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
        
        # --- Run Routine "show_test" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *question* updates
            
            # if question is starting this frame...
            if question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
            
            # *test_square* updates
            
            # if test_square is starting this frame...
            if test_square.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                test_square.frameNStart = frameN  # exact frame index
                test_square.tStart = t  # local t and not account for scr refresh
                test_square.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(test_square, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'test_square.started')
                # update status
                test_square.status = STARTED
                test_square.setAutoDraw(True)
            
            # if test_square is active this frame...
            if test_square.status == STARTED:
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
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in show_testComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "show_test" ---
        for thisComponent in show_testComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('show_test.stopped', globalClock.getTime(format='float'))
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
            # was no response the correct answer?!
            if str(answer).lower() == 'none':
               key_resp.corr = 1;  # correct non-response
            else:
               key_resp.corr = 0;  # failed to respond (incorrectly)
        # store data for change_trials (TrialHandler)
        change_trials.addData('key_resp.keys',key_resp.keys)
        change_trials.addData('key_resp.corr', key_resp.corr)
        if key_resp.keys != None:  # we had a response
            change_trials.addData('key_resp.rt', key_resp.rt)
            change_trials.addData('key_resp.duration', key_resp.duration)
        # the Routine "show_test" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "feedback" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('feedback.started', globalClock.getTime(format='float'))
        # Run 'Begin Routine' code from code_2
        if key_resp.corr:
            fbtxt = 'Correct!'
            fbcol = 'green'
        else:
            fbtxt = 'Incorrect'
            fbcol = 'red'
        fbtextbox.reset()
        fbtextbox.setColor(fbcol, colorSpace='rgb')
        fbtextbox.setText(fbtxt)
        # keep track of which components have finished
        feedbackComponents = [fbtextbox]
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
        frameN = -1
        
        # --- Run Routine "feedback" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fbtextbox* updates
            
            # if fbtextbox is starting this frame...
            if fbtextbox.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fbtextbox.frameNStart = frameN  # exact frame index
                fbtextbox.tStart = t  # local t and not account for scr refresh
                fbtextbox.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fbtextbox, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fbtextbox.started')
                # update status
                fbtextbox.status = STARTED
                fbtextbox.setAutoDraw(True)
            
            # if fbtextbox is active this frame...
            if fbtextbox.status == STARTED:
                # update params
                pass
            
            # if fbtextbox is stopping this frame...
            if fbtextbox.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fbtextbox.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    fbtextbox.tStop = t  # not accounting for scr refresh
                    fbtextbox.tStopRefresh = tThisFlipGlobal  # on global time
                    fbtextbox.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fbtextbox.stopped')
                    # update status
                    fbtextbox.status = FINISHED
                    fbtextbox.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in feedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "feedback" ---
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('feedback.stopped', globalClock.getTime(format='float'))
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.500000)
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 1.0 repeats of 'change_trials'
    
    
    # --- Prepare to start Routine "next_instr" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('next_instr.started', globalClock.getTime(format='float'))
    nextinstrtxt.reset()
    # create starting attributes for next_resp
    next_resp.keys = []
    next_resp.rt = []
    _next_resp_allKeys = []
    # keep track of which components have finished
    next_instrComponents = [nextinstrtxt, next_resp]
    for thisComponent in next_instrComponents:
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
    
    # --- Run Routine "next_instr" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *nextinstrtxt* updates
        
        # if nextinstrtxt is starting this frame...
        if nextinstrtxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            nextinstrtxt.frameNStart = frameN  # exact frame index
            nextinstrtxt.tStart = t  # local t and not account for scr refresh
            nextinstrtxt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(nextinstrtxt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'nextinstrtxt.started')
            # update status
            nextinstrtxt.status = STARTED
            nextinstrtxt.setAutoDraw(True)
        
        # if nextinstrtxt is active this frame...
        if nextinstrtxt.status == STARTED:
            # update params
            pass
        
        # *next_resp* updates
        waitOnFlip = False
        
        # if next_resp is starting this frame...
        if next_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            next_resp.frameNStart = frameN  # exact frame index
            next_resp.tStart = t  # local t and not account for scr refresh
            next_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(next_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'next_resp.started')
            # update status
            next_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(next_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(next_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if next_resp.status == STARTED and not waitOnFlip:
            theseKeys = next_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _next_resp_allKeys.extend(theseKeys)
            if len(_next_resp_allKeys):
                next_resp.keys = _next_resp_allKeys[-1].name  # just the last key pressed
                next_resp.rt = _next_resp_allKeys[-1].rt
                next_resp.duration = _next_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in next_instrComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "next_instr" ---
    for thisComponent in next_instrComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('next_instr.stopped', globalClock.getTime(format='float'))
    # check responses
    if next_resp.keys in ['', [], None]:  # No response was made
        next_resp.keys = None
    thisExp.addData('next_resp.keys',next_resp.keys)
    if next_resp.keys != None:  # we had a response
        thisExp.addData('next_resp.rt', next_resp.rt)
        thisExp.addData('next_resp.duration', next_resp.duration)
    thisExp.nextEntry()
    # the Routine "next_instr" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    localisation_trials = data.TrialHandler(nReps=5.0, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('code/localisation_trials_with_test_columns.xlsx'),
        seed=None, name='localisation_trials')
    thisExp.addLoop(localisation_trials)  # add the loop to the experiment
    thisLocalisation_trial = localisation_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisLocalisation_trial.rgb)
    if thisLocalisation_trial != None:
        for paramName in thisLocalisation_trial:
            globals()[paramName] = thisLocalisation_trial[paramName]
    
    for thisLocalisation_trial in localisation_trials:
        currentLoop = localisation_trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisLocalisation_trial.rgb)
        if thisLocalisation_trial != None:
            for paramName in thisLocalisation_trial:
                globals()[paramName] = thisLocalisation_trial[paramName]
        
        # --- Prepare to start Routine "trial" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('trial.started', globalClock.getTime(format='float'))
        square1.setFillColor(color1)
        square1.setPos((x1, y1))
        square1.setLineColor(color1)
        square2.setFillColor(color2)
        square2.setPos((x2, y2))
        square2.setLineColor(color2)
        square3.setFillColor(color3)
        square3.setPos((x3, y3))
        square3.setLineColor(color3)
        square4.setFillColor(color4)
        square4.setPos((x4, y4))
        square4.setLineColor(color4)
        square5.setFillColor(color5)
        square5.setPos((x5, y5))
        square5.setLineColor(color5)
        square6.setFillColor(color6)
        square6.setPos((x6, y6))
        square6.setLineColor(color6)
        # keep track of which components have finished
        trialComponents = [square1, square2, square3, square4, square5, square6]
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
        frameN = -1
        
        # --- Run Routine "trial" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *square1* updates
            
            # if square1 is starting this frame...
            if square1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square1.frameNStart = frameN  # exact frame index
                square1.tStart = t  # local t and not account for scr refresh
                square1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square1.started')
                # update status
                square1.status = STARTED
                square1.setAutoDraw(True)
            
            # if square1 is active this frame...
            if square1.status == STARTED:
                # update params
                pass
            
            # if square1 is stopping this frame...
            if square1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square1.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square1.tStop = t  # not accounting for scr refresh
                    square1.tStopRefresh = tThisFlipGlobal  # on global time
                    square1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square1.stopped')
                    # update status
                    square1.status = FINISHED
                    square1.setAutoDraw(False)
            
            # *square2* updates
            
            # if square2 is starting this frame...
            if square2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square2.frameNStart = frameN  # exact frame index
                square2.tStart = t  # local t and not account for scr refresh
                square2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square2.started')
                # update status
                square2.status = STARTED
                square2.setAutoDraw(True)
            
            # if square2 is active this frame...
            if square2.status == STARTED:
                # update params
                pass
            
            # if square2 is stopping this frame...
            if square2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square2.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square2.tStop = t  # not accounting for scr refresh
                    square2.tStopRefresh = tThisFlipGlobal  # on global time
                    square2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square2.stopped')
                    # update status
                    square2.status = FINISHED
                    square2.setAutoDraw(False)
            
            # *square3* updates
            
            # if square3 is starting this frame...
            if square3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square3.frameNStart = frameN  # exact frame index
                square3.tStart = t  # local t and not account for scr refresh
                square3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square3.started')
                # update status
                square3.status = STARTED
                square3.setAutoDraw(True)
            
            # if square3 is active this frame...
            if square3.status == STARTED:
                # update params
                pass
            
            # if square3 is stopping this frame...
            if square3.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square3.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square3.tStop = t  # not accounting for scr refresh
                    square3.tStopRefresh = tThisFlipGlobal  # on global time
                    square3.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square3.stopped')
                    # update status
                    square3.status = FINISHED
                    square3.setAutoDraw(False)
            
            # *square4* updates
            
            # if square4 is starting this frame...
            if square4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square4.frameNStart = frameN  # exact frame index
                square4.tStart = t  # local t and not account for scr refresh
                square4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square4.started')
                # update status
                square4.status = STARTED
                square4.setAutoDraw(True)
            
            # if square4 is active this frame...
            if square4.status == STARTED:
                # update params
                pass
            
            # if square4 is stopping this frame...
            if square4.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square4.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square4.tStop = t  # not accounting for scr refresh
                    square4.tStopRefresh = tThisFlipGlobal  # on global time
                    square4.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square4.stopped')
                    # update status
                    square4.status = FINISHED
                    square4.setAutoDraw(False)
            
            # *square5* updates
            
            # if square5 is starting this frame...
            if square5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square5.frameNStart = frameN  # exact frame index
                square5.tStart = t  # local t and not account for scr refresh
                square5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square5, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square5.started')
                # update status
                square5.status = STARTED
                square5.setAutoDraw(True)
            
            # if square5 is active this frame...
            if square5.status == STARTED:
                # update params
                pass
            
            # if square5 is stopping this frame...
            if square5.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square5.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square5.tStop = t  # not accounting for scr refresh
                    square5.tStopRefresh = tThisFlipGlobal  # on global time
                    square5.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square5.stopped')
                    # update status
                    square5.status = FINISHED
                    square5.setAutoDraw(False)
            
            # *square6* updates
            
            # if square6 is starting this frame...
            if square6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square6.frameNStart = frameN  # exact frame index
                square6.tStart = t  # local t and not account for scr refresh
                square6.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square6, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square6.started')
                # update status
                square6.status = STARTED
                square6.setAutoDraw(True)
            
            # if square6 is active this frame...
            if square6.status == STARTED:
                # update params
                pass
            
            # if square6 is stopping this frame...
            if square6.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > square6.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    square6.tStop = t  # not accounting for scr refresh
                    square6.tStopRefresh = tThisFlipGlobal  # on global time
                    square6.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'square6.stopped')
                    # update status
                    square6.status = FINISHED
                    square6.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial" ---
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('trial.stopped', globalClock.getTime(format='float'))
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.500000)
        
        # --- Prepare to start Routine "localisation_test" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('localisation_test.started', globalClock.getTime(format='float'))
        square1_2.setFillColor(testcolor1)
        square1_2.setPos((x1, y1))
        square1_2.setLineColor(testcolor1)
        square2_2.setFillColor(testcolor2)
        square2_2.setPos((x2, y2))
        square2_2.setLineColor(testcolor2)
        square3_2.setFillColor(testcolor3)
        square3_2.setPos((x3, y3))
        square3_2.setLineColor(testcolor3)
        square4_2.setFillColor(testcolor4)
        square4_2.setPos((x4, y4))
        square4_2.setLineColor(testcolor4)
        square5_2.setFillColor(testcolor5)
        square5_2.setPos((x5, y5))
        square5_2.setLineColor(testcolor5)
        square6_2.setFillColor(testcolor6)
        square6_2.setPos((x6, y6))
        square6_2.setLineColor(testcolor6)
        one_label.reset()
        one_label.setPos((x1, y1))
        two_label.reset()
        two_label.setPos((x2, y2))
        three_label.reset()
        three_label.setPos((x3, y3))
        four_label.reset()
        four_label.setPos((x4, y4))
        five_label.reset()
        five_label.setPos((x5, y5))
        six_label.reset()
        six_label.setPos((x6, y6))
        # create starting attributes for localisation_resp
        localisation_resp.keys = []
        localisation_resp.rt = []
        _localisation_resp_allKeys = []
        textbox_2.reset()
        textbox_2.setText(changed_color_index)
        # keep track of which components have finished
        localisation_testComponents = [square1_2, square2_2, square3_2, square4_2, square5_2, square6_2, one_label, two_label, three_label, four_label, five_label, six_label, localisation_resp, textbox_2]
        for thisComponent in localisation_testComponents:
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
        
        # --- Run Routine "localisation_test" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *square1_2* updates
            
            # if square1_2 is starting this frame...
            if square1_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square1_2.frameNStart = frameN  # exact frame index
                square1_2.tStart = t  # local t and not account for scr refresh
                square1_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square1_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square1_2.started')
                # update status
                square1_2.status = STARTED
                square1_2.setAutoDraw(True)
            
            # if square1_2 is active this frame...
            if square1_2.status == STARTED:
                # update params
                pass
            
            # *square2_2* updates
            
            # if square2_2 is starting this frame...
            if square2_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square2_2.frameNStart = frameN  # exact frame index
                square2_2.tStart = t  # local t and not account for scr refresh
                square2_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square2_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square2_2.started')
                # update status
                square2_2.status = STARTED
                square2_2.setAutoDraw(True)
            
            # if square2_2 is active this frame...
            if square2_2.status == STARTED:
                # update params
                pass
            
            # *square3_2* updates
            
            # if square3_2 is starting this frame...
            if square3_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square3_2.frameNStart = frameN  # exact frame index
                square3_2.tStart = t  # local t and not account for scr refresh
                square3_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square3_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square3_2.started')
                # update status
                square3_2.status = STARTED
                square3_2.setAutoDraw(True)
            
            # if square3_2 is active this frame...
            if square3_2.status == STARTED:
                # update params
                pass
            
            # *square4_2* updates
            
            # if square4_2 is starting this frame...
            if square4_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square4_2.frameNStart = frameN  # exact frame index
                square4_2.tStart = t  # local t and not account for scr refresh
                square4_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square4_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square4_2.started')
                # update status
                square4_2.status = STARTED
                square4_2.setAutoDraw(True)
            
            # if square4_2 is active this frame...
            if square4_2.status == STARTED:
                # update params
                pass
            
            # *square5_2* updates
            
            # if square5_2 is starting this frame...
            if square5_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square5_2.frameNStart = frameN  # exact frame index
                square5_2.tStart = t  # local t and not account for scr refresh
                square5_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square5_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square5_2.started')
                # update status
                square5_2.status = STARTED
                square5_2.setAutoDraw(True)
            
            # if square5_2 is active this frame...
            if square5_2.status == STARTED:
                # update params
                pass
            
            # *square6_2* updates
            
            # if square6_2 is starting this frame...
            if square6_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                square6_2.frameNStart = frameN  # exact frame index
                square6_2.tStart = t  # local t and not account for scr refresh
                square6_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(square6_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'square6_2.started')
                # update status
                square6_2.status = STARTED
                square6_2.setAutoDraw(True)
            
            # if square6_2 is active this frame...
            if square6_2.status == STARTED:
                # update params
                pass
            
            # *one_label* updates
            
            # if one_label is starting this frame...
            if one_label.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                one_label.frameNStart = frameN  # exact frame index
                one_label.tStart = t  # local t and not account for scr refresh
                one_label.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(one_label, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'one_label.started')
                # update status
                one_label.status = STARTED
                one_label.setAutoDraw(True)
            
            # if one_label is active this frame...
            if one_label.status == STARTED:
                # update params
                pass
            
            # *two_label* updates
            
            # if two_label is starting this frame...
            if two_label.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                two_label.frameNStart = frameN  # exact frame index
                two_label.tStart = t  # local t and not account for scr refresh
                two_label.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(two_label, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'two_label.started')
                # update status
                two_label.status = STARTED
                two_label.setAutoDraw(True)
            
            # if two_label is active this frame...
            if two_label.status == STARTED:
                # update params
                pass
            
            # *three_label* updates
            
            # if three_label is starting this frame...
            if three_label.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                three_label.frameNStart = frameN  # exact frame index
                three_label.tStart = t  # local t and not account for scr refresh
                three_label.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(three_label, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'three_label.started')
                # update status
                three_label.status = STARTED
                three_label.setAutoDraw(True)
            
            # if three_label is active this frame...
            if three_label.status == STARTED:
                # update params
                pass
            
            # *four_label* updates
            
            # if four_label is starting this frame...
            if four_label.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                four_label.frameNStart = frameN  # exact frame index
                four_label.tStart = t  # local t and not account for scr refresh
                four_label.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(four_label, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'four_label.started')
                # update status
                four_label.status = STARTED
                four_label.setAutoDraw(True)
            
            # if four_label is active this frame...
            if four_label.status == STARTED:
                # update params
                pass
            
            # *five_label* updates
            
            # if five_label is starting this frame...
            if five_label.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                five_label.frameNStart = frameN  # exact frame index
                five_label.tStart = t  # local t and not account for scr refresh
                five_label.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(five_label, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'five_label.started')
                # update status
                five_label.status = STARTED
                five_label.setAutoDraw(True)
            
            # if five_label is active this frame...
            if five_label.status == STARTED:
                # update params
                pass
            
            # *six_label* updates
            
            # if six_label is starting this frame...
            if six_label.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                six_label.frameNStart = frameN  # exact frame index
                six_label.tStart = t  # local t and not account for scr refresh
                six_label.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(six_label, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'six_label.started')
                # update status
                six_label.status = STARTED
                six_label.setAutoDraw(True)
            
            # if six_label is active this frame...
            if six_label.status == STARTED:
                # update params
                pass
            
            # *localisation_resp* updates
            waitOnFlip = False
            
            # if localisation_resp is starting this frame...
            if localisation_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                localisation_resp.frameNStart = frameN  # exact frame index
                localisation_resp.tStart = t  # local t and not account for scr refresh
                localisation_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(localisation_resp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'localisation_resp.started')
                # update status
                localisation_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(localisation_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(localisation_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if localisation_resp.status == STARTED and not waitOnFlip:
                theseKeys = localisation_resp.getKeys(keyList=['1', '2', '3', '4', '5', '6'], ignoreKeys=["escape"], waitRelease=False)
                _localisation_resp_allKeys.extend(theseKeys)
                if len(_localisation_resp_allKeys):
                    localisation_resp.keys = _localisation_resp_allKeys[-1].name  # just the last key pressed
                    localisation_resp.rt = _localisation_resp_allKeys[-1].rt
                    localisation_resp.duration = _localisation_resp_allKeys[-1].duration
                    # was this correct?
                    if (localisation_resp.keys == str(changed_color_index)) or (localisation_resp.keys == changed_color_index):
                        localisation_resp.corr = 1
                    else:
                        localisation_resp.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            # *textbox_2* updates
            
            # if textbox_2 is starting this frame...
            if textbox_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                textbox_2.frameNStart = frameN  # exact frame index
                textbox_2.tStart = t  # local t and not account for scr refresh
                textbox_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(textbox_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'textbox_2.started')
                # update status
                textbox_2.status = STARTED
                textbox_2.setAutoDraw(True)
            
            # if textbox_2 is active this frame...
            if textbox_2.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in localisation_testComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "localisation_test" ---
        for thisComponent in localisation_testComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('localisation_test.stopped', globalClock.getTime(format='float'))
        # check responses
        if localisation_resp.keys in ['', [], None]:  # No response was made
            localisation_resp.keys = None
            # was no response the correct answer?!
            if str(changed_color_index).lower() == 'none':
               localisation_resp.corr = 1;  # correct non-response
            else:
               localisation_resp.corr = 0;  # failed to respond (incorrectly)
        # store data for localisation_trials (TrialHandler)
        localisation_trials.addData('localisation_resp.keys',localisation_resp.keys)
        localisation_trials.addData('localisation_resp.corr', localisation_resp.corr)
        if localisation_resp.keys != None:  # we had a response
            localisation_trials.addData('localisation_resp.rt', localisation_resp.rt)
            localisation_trials.addData('localisation_resp.duration', localisation_resp.duration)
        # the Routine "localisation_test" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "localisation_feedback" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('localisation_feedback.started', globalClock.getTime(format='float'))
        # Run 'Begin Routine' code from code_4
        if localisation_resp.corr:
            fbtxt = 'Correct!'
            fbcol = 'green'
        else:
            fbtxt = 'Incorrect'
            fbcol = 'red'
        fbtextbox_2.reset()
        fbtextbox_2.setColor(fbcol, colorSpace='rgb')
        fbtextbox_2.setText(fbtxt)
        # keep track of which components have finished
        localisation_feedbackComponents = [fbtextbox_2]
        for thisComponent in localisation_feedbackComponents:
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
        
        # --- Run Routine "localisation_feedback" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fbtextbox_2* updates
            
            # if fbtextbox_2 is starting this frame...
            if fbtextbox_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fbtextbox_2.frameNStart = frameN  # exact frame index
                fbtextbox_2.tStart = t  # local t and not account for scr refresh
                fbtextbox_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fbtextbox_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fbtextbox_2.started')
                # update status
                fbtextbox_2.status = STARTED
                fbtextbox_2.setAutoDraw(True)
            
            # if fbtextbox_2 is active this frame...
            if fbtextbox_2.status == STARTED:
                # update params
                pass
            
            # if fbtextbox_2 is stopping this frame...
            if fbtextbox_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fbtextbox_2.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    fbtextbox_2.tStop = t  # not accounting for scr refresh
                    fbtextbox_2.tStopRefresh = tThisFlipGlobal  # on global time
                    fbtextbox_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fbtextbox_2.stopped')
                    # update status
                    fbtextbox_2.status = FINISHED
                    fbtextbox_2.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in localisation_feedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "localisation_feedback" ---
        for thisComponent in localisation_feedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('localisation_feedback.stopped', globalClock.getTime(format='float'))
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.500000)
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 5.0 repeats of 'localisation_trials'
    
    
    # --- Prepare to start Routine "bye" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('bye.started', globalClock.getTime(format='float'))
    textbox.reset()
    # keep track of which components have finished
    byeComponents = [textbox]
    for thisComponent in byeComponents:
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
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
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
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in byeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "bye" ---
    for thisComponent in byeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('bye.stopped', globalClock.getTime(format='float'))
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
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
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # shut down eyetracker, if there is one
    if deviceManager.getDevice('eyetracker') is not None:
        deviceManager.removeDevice('eyetracker')
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
    # shut down eyetracker, if there is one
    if deviceManager.getDevice('eyetracker') is not None:
        deviceManager.removeDevice('eyetracker')
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
