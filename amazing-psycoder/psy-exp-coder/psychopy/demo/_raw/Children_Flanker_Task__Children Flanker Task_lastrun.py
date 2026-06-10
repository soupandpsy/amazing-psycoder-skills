# Source: Children Flanker Task (demos/children-flanker-task)
# Project URL: https://gitlab.pavlovia.org/demos/children-flanker-task
# Original file: Children Flanker Task_lastrun.py
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2025.2.3),
    on December 08, 2025, at 13:46
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
psychopyVersion = '2025.2.3'
expName = 'Children Flanker Task'  # from the Builder filename that created this script
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
_winSize = [1366, 768]
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
        originPath='C:\\Users\\morys\\Documents\\Pavlovia\\Demos\\Children Flanker Task\\Children Flanker Task_lastrun.py',
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
            logging.getLevel('exp')
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
            monitor='testMonitor', color=[-1.000,-0.380,0.231], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [-1.000,-0.380,0.231]
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
    
    # --- Initialize components for Routine "Instructions" ---
    instructions = visual.TextBox2(
         win, text='Please observe which way the fish in the centre is facing. If the fish is facing left press left arrow. If the fish is facing right press right arrow. Ignore the fish around the central fish. You are about to start practice trials and feedback will be provided. Please answer as quickly as possible. \n\nPress space to begin practice trials.', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(1, 0.8), borderWidth=0.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center-left',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instructions',
         depth=0, autoLog=True,
    )
    key_start = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "Flanker" ---
    fixation_2 = visual.TextStim(win=win, name='fixation_2',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    Fish_1 = visual.ImageStim(
        win=win,
        name='Fish_1', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(-0.6, 0), draggable=False, size=(0.25, 0.15),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-1.0)
    Fish_2 = visual.ImageStim(
        win=win,
        name='Fish_2', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(-0.3, 0), draggable=False, size=(0.25, 0.15),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-2.0)
    TargetFish = visual.ImageStim(
        win=win,
        name='TargetFish', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(0, 0), draggable=False, size=(0.25, 0.15),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-3.0)
    Fish_3 = visual.ImageStim(
        win=win,
        name='Fish_3', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(0.3, 0), draggable=False, size=(0.25, 0.15),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-4.0)
    Fish_4 = visual.ImageStim(
        win=win,
        name='Fish_4', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(0.6, 0), draggable=False, size=(0.25, 0.15),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-5.0)
    response = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "Feedback" ---
    feedback_text = visual.TextStim(win=win, name='feedback_text',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "Gap" ---
    gap_text = visual.TextBox2(
         win, text='This is the end of the practice trials. Feedback will no longer be provided on experimental trials.\n\nPress space to continue to experimental trials.', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(1, 0.8), borderWidth=0.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center-left',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='gap_text',
         depth=0, autoLog=True,
    )
    key_continue = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "Flanker" ---
    fixation_2 = visual.TextStim(win=win, name='fixation_2',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    Fish_1 = visual.ImageStim(
        win=win,
        name='Fish_1', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(-0.6, 0), draggable=False, size=(0.25, 0.15),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-1.0)
    Fish_2 = visual.ImageStim(
        win=win,
        name='Fish_2', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(-0.3, 0), draggable=False, size=(0.25, 0.15),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-2.0)
    TargetFish = visual.ImageStim(
        win=win,
        name='TargetFish', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(0, 0), draggable=False, size=(0.25, 0.15),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-3.0)
    Fish_3 = visual.ImageStim(
        win=win,
        name='Fish_3', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(0.3, 0), draggable=False, size=(0.25, 0.15),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-4.0)
    Fish_4 = visual.ImageStim(
        win=win,
        name='Fish_4', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(0.6, 0), draggable=False, size=(0.25, 0.15),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-5.0)
    response = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "End" ---
    thank_you = visual.TextStim(win=win, name='thank_you',
        text='This is the end of the experiment.\nThank you for your time.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    
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
    if eyetracker is not None:
        eyetracker.enableEventReporting()
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "Instructions" ---
    # create an object to store info about Routine Instructions
    Instructions = data.Routine(
        name='Instructions',
        components=[instructions, key_start],
    )
    Instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    instructions.reset()
    # create starting attributes for key_start
    key_start.keys = []
    key_start.rt = []
    _key_start_allKeys = []
    # store start times for Instructions
    Instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Instructions.tStart = globalClock.getTime(format='float')
    Instructions.status = STARTED
    thisExp.addData('Instructions.started', Instructions.tStart)
    Instructions.maxDuration = None
    # keep track of which components have finished
    InstructionsComponents = Instructions.components
    for thisComponent in Instructions.components:
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
    
    # --- Run Routine "Instructions" ---
    thisExp.currentRoutine = Instructions
    Instructions.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instructions* updates
        
        # if instructions is starting this frame...
        if instructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructions.frameNStart = frameN  # exact frame index
            instructions.tStart = t  # local t and not account for scr refresh
            instructions.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructions, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instructions.started')
            # update status
            instructions.status = STARTED
            instructions.setAutoDraw(True)
        
        # if instructions is active this frame...
        if instructions.status == STARTED:
            # update params
            pass
        
        # *key_start* updates
        waitOnFlip = False
        
        # if key_start is starting this frame...
        if key_start.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_start.frameNStart = frameN  # exact frame index
            key_start.tStart = t  # local t and not account for scr refresh
            key_start.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_start, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_start.started')
            # update status
            key_start.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_start.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_start.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_start.status == STARTED and not waitOnFlip:
            theseKeys = key_start.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_start_allKeys.extend(theseKeys)
            if len(_key_start_allKeys):
                key_start.keys = _key_start_allKeys[-1].name  # just the last key pressed
                key_start.rt = _key_start_allKeys[-1].rt
                key_start.duration = _key_start_allKeys[-1].duration
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
                currentRoutine=Instructions,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            Instructions.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if Instructions.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in Instructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Instructions" ---
    for thisComponent in Instructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Instructions
    Instructions.tStop = globalClock.getTime(format='float')
    Instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Instructions.stopped', Instructions.tStop)
    thisExp.nextEntry()
    # the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    practice_trials = data.TrialHandler2(
        name='practice_trials',
        nReps=1, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions(
        'conditions.csv', 
        selection='0:6'
    )
    , 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(practice_trials)  # add the loop to the experiment
    thisPractice_trial = practice_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPractice_trial.rgb)
    if thisPractice_trial != None:
        for paramName in thisPractice_trial:
            globals()[paramName] = thisPractice_trial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisPractice_trial in practice_trials:
        practice_trials.status = STARTED
        if hasattr(thisPractice_trial, 'status'):
            thisPractice_trial.status = STARTED
        currentLoop = practice_trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisPractice_trial.rgb)
        if thisPractice_trial != None:
            for paramName in thisPractice_trial:
                globals()[paramName] = thisPractice_trial[paramName]
        
        # --- Prepare to start Routine "Flanker" ---
        # create an object to store info about Routine Flanker
        Flanker = data.Routine(
            name='Flanker',
            components=[fixation_2, Fish_1, Fish_2, TargetFish, Fish_3, Fish_4, response],
        )
        Flanker.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        Fish_1.setImage(Fish1)
        Fish_2.setImage(Fish2)
        TargetFish.setImage(targetFish)
        Fish_3.setImage(Fish3)
        Fish_4.setImage(Fish4)
        # create starting attributes for response
        response.keys = []
        response.rt = []
        _response_allKeys = []
        # store start times for Flanker
        Flanker.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Flanker.tStart = globalClock.getTime(format='float')
        Flanker.status = STARTED
        thisExp.addData('Flanker.started', Flanker.tStart)
        Flanker.maxDuration = None
        # keep track of which components have finished
        FlankerComponents = Flanker.components
        for thisComponent in Flanker.components:
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
        
        # --- Run Routine "Flanker" ---
        thisExp.currentRoutine = Flanker
        Flanker.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisPractice_trial, 'status') and thisPractice_trial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation_2* updates
            
            # if fixation_2 is starting this frame...
            if fixation_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_2.frameNStart = frameN  # exact frame index
                fixation_2.tStart = t  # local t and not account for scr refresh
                fixation_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_2.started')
                # update status
                fixation_2.status = STARTED
                fixation_2.setAutoDraw(True)
            
            # if fixation_2 is active this frame...
            if fixation_2.status == STARTED:
                # update params
                pass
            
            # if fixation_2 is stopping this frame...
            if fixation_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_2.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_2.tStop = t  # not accounting for scr refresh
                    fixation_2.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_2.stopped')
                    # update status
                    fixation_2.status = FINISHED
                    fixation_2.setAutoDraw(False)
            
            # *Fish_1* updates
            
            # if Fish_1 is starting this frame...
            if Fish_1.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                Fish_1.frameNStart = frameN  # exact frame index
                Fish_1.tStart = t  # local t and not account for scr refresh
                Fish_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fish_1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fish_1.started')
                # update status
                Fish_1.status = STARTED
                Fish_1.setAutoDraw(True)
            
            # if Fish_1 is active this frame...
            if Fish_1.status == STARTED:
                # update params
                pass
            
            # *Fish_2* updates
            
            # if Fish_2 is starting this frame...
            if Fish_2.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                Fish_2.frameNStart = frameN  # exact frame index
                Fish_2.tStart = t  # local t and not account for scr refresh
                Fish_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fish_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fish_2.started')
                # update status
                Fish_2.status = STARTED
                Fish_2.setAutoDraw(True)
            
            # if Fish_2 is active this frame...
            if Fish_2.status == STARTED:
                # update params
                pass
            
            # *TargetFish* updates
            
            # if TargetFish is starting this frame...
            if TargetFish.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                TargetFish.frameNStart = frameN  # exact frame index
                TargetFish.tStart = t  # local t and not account for scr refresh
                TargetFish.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(TargetFish, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'TargetFish.started')
                # update status
                TargetFish.status = STARTED
                TargetFish.setAutoDraw(True)
            
            # if TargetFish is active this frame...
            if TargetFish.status == STARTED:
                # update params
                pass
            
            # *Fish_3* updates
            
            # if Fish_3 is starting this frame...
            if Fish_3.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                Fish_3.frameNStart = frameN  # exact frame index
                Fish_3.tStart = t  # local t and not account for scr refresh
                Fish_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fish_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fish_3.started')
                # update status
                Fish_3.status = STARTED
                Fish_3.setAutoDraw(True)
            
            # if Fish_3 is active this frame...
            if Fish_3.status == STARTED:
                # update params
                pass
            
            # *Fish_4* updates
            
            # if Fish_4 is starting this frame...
            if Fish_4.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                Fish_4.frameNStart = frameN  # exact frame index
                Fish_4.tStart = t  # local t and not account for scr refresh
                Fish_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fish_4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fish_4.started')
                # update status
                Fish_4.status = STARTED
                Fish_4.setAutoDraw(True)
            
            # if Fish_4 is active this frame...
            if Fish_4.status == STARTED:
                # update params
                pass
            
            # *response* updates
            waitOnFlip = False
            
            # if response is starting this frame...
            if response.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                response.frameNStart = frameN  # exact frame index
                response.tStart = t  # local t and not account for scr refresh
                response.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(response, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'response.started')
                # update status
                response.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(response.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(response.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if response.status == STARTED and not waitOnFlip:
                theseKeys = response.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
                _response_allKeys.extend(theseKeys)
                if len(_response_allKeys):
                    response.keys = _response_allKeys[-1].name  # just the last key pressed
                    response.rt = _response_allKeys[-1].rt
                    response.duration = _response_allKeys[-1].duration
                    # was this correct?
                    if (response.keys == str(corrAns)) or (response.keys == corrAns):
                        response.corr = 1
                    else:
                        response.corr = 0
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
                    currentRoutine=Flanker,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                Flanker.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if Flanker.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in Flanker.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Flanker" ---
        for thisComponent in Flanker.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Flanker
        Flanker.tStop = globalClock.getTime(format='float')
        Flanker.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Flanker.stopped', Flanker.tStop)
        # check responses
        if response.keys in ['', [], None]:  # No response was made
            response.keys = None
            # was no response the correct answer?!
            if str(corrAns).lower() == 'none':
               response.corr = 1;  # correct non-response
            else:
               response.corr = 0;  # failed to respond (incorrectly)
        # store data for practice_trials (TrialHandler)
        practice_trials.addData('response.keys',response.keys)
        practice_trials.addData('response.corr', response.corr)
        if response.keys != None:  # we had a response
            practice_trials.addData('response.rt', response.rt)
            practice_trials.addData('response.duration', response.duration)
        # the Routine "Flanker" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "Feedback" ---
        # create an object to store info about Routine Feedback
        Feedback = data.Routine(
            name='Feedback',
            components=[feedback_text],
        )
        Feedback.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from feedback_code
        if response.corr:
            msg = f"Correct! RT = {(round(response.rt,2))} s"
        else:
            msg = "Incorrect"
        feedback_text.setText(msg)
        # store start times for Feedback
        Feedback.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Feedback.tStart = globalClock.getTime(format='float')
        Feedback.status = STARTED
        thisExp.addData('Feedback.started', Feedback.tStart)
        Feedback.maxDuration = None
        # keep track of which components have finished
        FeedbackComponents = Feedback.components
        for thisComponent in Feedback.components:
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
        
        # --- Run Routine "Feedback" ---
        thisExp.currentRoutine = Feedback
        Feedback.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # if trial has changed, end Routine now
            if hasattr(thisPractice_trial, 'status') and thisPractice_trial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *feedback_text* updates
            
            # if feedback_text is starting this frame...
            if feedback_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                feedback_text.frameNStart = frameN  # exact frame index
                feedback_text.tStart = t  # local t and not account for scr refresh
                feedback_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(feedback_text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'feedback_text.started')
                # update status
                feedback_text.status = STARTED
                feedback_text.setAutoDraw(True)
            
            # if feedback_text is active this frame...
            if feedback_text.status == STARTED:
                # update params
                pass
            
            # if feedback_text is stopping this frame...
            if feedback_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > feedback_text.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    feedback_text.tStop = t  # not accounting for scr refresh
                    feedback_text.tStopRefresh = tThisFlipGlobal  # on global time
                    feedback_text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'feedback_text.stopped')
                    # update status
                    feedback_text.status = FINISHED
                    feedback_text.setAutoDraw(False)
            
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
                    currentRoutine=Feedback,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                Feedback.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if Feedback.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in Feedback.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Feedback" ---
        for thisComponent in Feedback.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Feedback
        Feedback.tStop = globalClock.getTime(format='float')
        Feedback.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Feedback.stopped', Feedback.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if Feedback.maxDurationReached:
            routineTimer.addTime(-Feedback.maxDuration)
        elif Feedback.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        # mark thisPractice_trial as finished
        if hasattr(thisPractice_trial, 'status'):
            thisPractice_trial.status = FINISHED
        # if awaiting a pause, pause now
        if practice_trials.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            practice_trials.status = STARTED
        thisExp.nextEntry()
        
    # completed 1 repeats of 'practice_trials'
    practice_trials.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "Gap" ---
    # create an object to store info about Routine Gap
    Gap = data.Routine(
        name='Gap',
        components=[gap_text, key_continue],
    )
    Gap.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    gap_text.reset()
    # create starting attributes for key_continue
    key_continue.keys = []
    key_continue.rt = []
    _key_continue_allKeys = []
    # store start times for Gap
    Gap.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Gap.tStart = globalClock.getTime(format='float')
    Gap.status = STARTED
    thisExp.addData('Gap.started', Gap.tStart)
    Gap.maxDuration = None
    # keep track of which components have finished
    GapComponents = Gap.components
    for thisComponent in Gap.components:
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
    
    # --- Run Routine "Gap" ---
    thisExp.currentRoutine = Gap
    Gap.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *gap_text* updates
        
        # if gap_text is starting this frame...
        if gap_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            gap_text.frameNStart = frameN  # exact frame index
            gap_text.tStart = t  # local t and not account for scr refresh
            gap_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(gap_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'gap_text.started')
            # update status
            gap_text.status = STARTED
            gap_text.setAutoDraw(True)
        
        # if gap_text is active this frame...
        if gap_text.status == STARTED:
            # update params
            pass
        
        # *key_continue* updates
        waitOnFlip = False
        
        # if key_continue is starting this frame...
        if key_continue.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_continue.frameNStart = frameN  # exact frame index
            key_continue.tStart = t  # local t and not account for scr refresh
            key_continue.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_continue, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_continue.started')
            # update status
            key_continue.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_continue.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_continue.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_continue.status == STARTED and not waitOnFlip:
            theseKeys = key_continue.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_continue_allKeys.extend(theseKeys)
            if len(_key_continue_allKeys):
                key_continue.keys = _key_continue_allKeys[-1].name  # just the last key pressed
                key_continue.rt = _key_continue_allKeys[-1].rt
                key_continue.duration = _key_continue_allKeys[-1].duration
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
                currentRoutine=Gap,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            Gap.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if Gap.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in Gap.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Gap" ---
    for thisComponent in Gap.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Gap
    Gap.tStop = globalClock.getTime(format='float')
    Gap.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Gap.stopped', Gap.tStop)
    thisExp.nextEntry()
    # the Routine "Gap" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler2(
        name='trials',
        nReps=1, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions(
        'conditions.csv', 
        selection='6:12'
    )
    , 
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
        
        # --- Prepare to start Routine "Flanker" ---
        # create an object to store info about Routine Flanker
        Flanker = data.Routine(
            name='Flanker',
            components=[fixation_2, Fish_1, Fish_2, TargetFish, Fish_3, Fish_4, response],
        )
        Flanker.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        Fish_1.setImage(Fish1)
        Fish_2.setImage(Fish2)
        TargetFish.setImage(targetFish)
        Fish_3.setImage(Fish3)
        Fish_4.setImage(Fish4)
        # create starting attributes for response
        response.keys = []
        response.rt = []
        _response_allKeys = []
        # store start times for Flanker
        Flanker.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Flanker.tStart = globalClock.getTime(format='float')
        Flanker.status = STARTED
        thisExp.addData('Flanker.started', Flanker.tStart)
        Flanker.maxDuration = None
        # keep track of which components have finished
        FlankerComponents = Flanker.components
        for thisComponent in Flanker.components:
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
        
        # --- Run Routine "Flanker" ---
        thisExp.currentRoutine = Flanker
        Flanker.forceEnded = routineForceEnded = not continueRoutine
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
            
            # *fixation_2* updates
            
            # if fixation_2 is starting this frame...
            if fixation_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_2.frameNStart = frameN  # exact frame index
                fixation_2.tStart = t  # local t and not account for scr refresh
                fixation_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_2.started')
                # update status
                fixation_2.status = STARTED
                fixation_2.setAutoDraw(True)
            
            # if fixation_2 is active this frame...
            if fixation_2.status == STARTED:
                # update params
                pass
            
            # if fixation_2 is stopping this frame...
            if fixation_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_2.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_2.tStop = t  # not accounting for scr refresh
                    fixation_2.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_2.stopped')
                    # update status
                    fixation_2.status = FINISHED
                    fixation_2.setAutoDraw(False)
            
            # *Fish_1* updates
            
            # if Fish_1 is starting this frame...
            if Fish_1.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                Fish_1.frameNStart = frameN  # exact frame index
                Fish_1.tStart = t  # local t and not account for scr refresh
                Fish_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fish_1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fish_1.started')
                # update status
                Fish_1.status = STARTED
                Fish_1.setAutoDraw(True)
            
            # if Fish_1 is active this frame...
            if Fish_1.status == STARTED:
                # update params
                pass
            
            # *Fish_2* updates
            
            # if Fish_2 is starting this frame...
            if Fish_2.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                Fish_2.frameNStart = frameN  # exact frame index
                Fish_2.tStart = t  # local t and not account for scr refresh
                Fish_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fish_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fish_2.started')
                # update status
                Fish_2.status = STARTED
                Fish_2.setAutoDraw(True)
            
            # if Fish_2 is active this frame...
            if Fish_2.status == STARTED:
                # update params
                pass
            
            # *TargetFish* updates
            
            # if TargetFish is starting this frame...
            if TargetFish.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                TargetFish.frameNStart = frameN  # exact frame index
                TargetFish.tStart = t  # local t and not account for scr refresh
                TargetFish.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(TargetFish, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'TargetFish.started')
                # update status
                TargetFish.status = STARTED
                TargetFish.setAutoDraw(True)
            
            # if TargetFish is active this frame...
            if TargetFish.status == STARTED:
                # update params
                pass
            
            # *Fish_3* updates
            
            # if Fish_3 is starting this frame...
            if Fish_3.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                Fish_3.frameNStart = frameN  # exact frame index
                Fish_3.tStart = t  # local t and not account for scr refresh
                Fish_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fish_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fish_3.started')
                # update status
                Fish_3.status = STARTED
                Fish_3.setAutoDraw(True)
            
            # if Fish_3 is active this frame...
            if Fish_3.status == STARTED:
                # update params
                pass
            
            # *Fish_4* updates
            
            # if Fish_4 is starting this frame...
            if Fish_4.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                Fish_4.frameNStart = frameN  # exact frame index
                Fish_4.tStart = t  # local t and not account for scr refresh
                Fish_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fish_4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fish_4.started')
                # update status
                Fish_4.status = STARTED
                Fish_4.setAutoDraw(True)
            
            # if Fish_4 is active this frame...
            if Fish_4.status == STARTED:
                # update params
                pass
            
            # *response* updates
            waitOnFlip = False
            
            # if response is starting this frame...
            if response.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                response.frameNStart = frameN  # exact frame index
                response.tStart = t  # local t and not account for scr refresh
                response.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(response, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'response.started')
                # update status
                response.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(response.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(response.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if response.status == STARTED and not waitOnFlip:
                theseKeys = response.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
                _response_allKeys.extend(theseKeys)
                if len(_response_allKeys):
                    response.keys = _response_allKeys[-1].name  # just the last key pressed
                    response.rt = _response_allKeys[-1].rt
                    response.duration = _response_allKeys[-1].duration
                    # was this correct?
                    if (response.keys == str(corrAns)) or (response.keys == corrAns):
                        response.corr = 1
                    else:
                        response.corr = 0
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
                    currentRoutine=Flanker,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                Flanker.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if Flanker.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in Flanker.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Flanker" ---
        for thisComponent in Flanker.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Flanker
        Flanker.tStop = globalClock.getTime(format='float')
        Flanker.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Flanker.stopped', Flanker.tStop)
        # check responses
        if response.keys in ['', [], None]:  # No response was made
            response.keys = None
            # was no response the correct answer?!
            if str(corrAns).lower() == 'none':
               response.corr = 1;  # correct non-response
            else:
               response.corr = 0;  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('response.keys',response.keys)
        trials.addData('response.corr', response.corr)
        if response.keys != None:  # we had a response
            trials.addData('response.rt', response.rt)
            trials.addData('response.duration', response.duration)
        # the Routine "Flanker" was not non-slip safe, so reset the non-slip timer
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
        
    # completed 1 repeats of 'trials'
    trials.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "End" ---
    # create an object to store info about Routine End
    End = data.Routine(
        name='End',
        components=[thank_you],
    )
    End.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for End
    End.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    End.tStart = globalClock.getTime(format='float')
    End.status = STARTED
    thisExp.addData('End.started', End.tStart)
    End.maxDuration = None
    # keep track of which components have finished
    EndComponents = End.components
    for thisComponent in End.components:
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
    
    # --- Run Routine "End" ---
    thisExp.currentRoutine = End
    End.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 3.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *thank_you* updates
        
        # if thank_you is starting this frame...
        if thank_you.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            thank_you.frameNStart = frameN  # exact frame index
            thank_you.tStart = t  # local t and not account for scr refresh
            thank_you.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(thank_you, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'thank_you.started')
            # update status
            thank_you.status = STARTED
            thank_you.setAutoDraw(True)
        
        # if thank_you is active this frame...
        if thank_you.status == STARTED:
            # update params
            pass
        
        # if thank_you is stopping this frame...
        if thank_you.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > thank_you.tStartRefresh + 3-frameTolerance:
                # keep track of stop time/frame for later
                thank_you.tStop = t  # not accounting for scr refresh
                thank_you.tStopRefresh = tThisFlipGlobal  # on global time
                thank_you.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'thank_you.stopped')
                # update status
                thank_you.status = FINISHED
                thank_you.setAutoDraw(False)
        
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
                currentRoutine=End,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            End.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if End.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in End.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "End" ---
    for thisComponent in End.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for End
    End.tStop = globalClock.getTime(format='float')
    End.tStopRefresh = tThisFlipGlobal
    thisExp.addData('End.stopped', End.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if End.maxDurationReached:
        routineTimer.addTime(-End.maxDuration)
    elif End.forceEnded:
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
