# Source: butterfly_simon (demos/butterfly_simon)
# Project URL: https://gitlab.pavlovia.org/demos/butterfly_simon
# Original file: Simon.py
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2025.1.0dev137),
    on Thu Jan  9 15:25:59 2025
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
psychopyVersion = '2025.1.0dev137'
expName = 'Simon'  # from the Builder filename that created this script
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
_fullScr = False
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
        originPath='/Users/Becca/Library/CloudStorage/GoogleDrive-becca@opensciencetools.org/Shared drives/Science/Pavlovia Demos/simon_task/Simon.py',
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
            logging.getLevel('warning')
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
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=1,
            winType='pyglet', allowGUI=True, allowStencil=True,
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
    instr_textbox = visual.TextBox2(
         win, text="Welcome!\n\nIn this game you will see two circles onscreen. \n\nWhen you see a RED circle, select the left of the two circles. \n\nWhen you see a GREEN circle, select the right of the two circles. \n\nIt doesn't matter where the red and green circles are located, the colored circle only indicates which side to select. \n", placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(1, 0.8), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instr_textbox',
         depth=0, autoLog=True,
    )
    start_button = visual.ButtonStim(win, 
        text='NEXT', font='Arvo',
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
    
    # --- Initialize components for Routine "practice_trial" ---
    left_circle_2 = visual.ShapeStim(
        win=win, name='left_circle_2',
        size=(0.25, 0.25), vertices='circle',
        ori=0.0, pos=(0.5, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    right_circle_2 = visual.ShapeStim(
        win=win, name='right_circle_2',
        size=(0.25, 0.25), vertices='circle',
        ori=0.0, pos=(-0.5, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    mouse_2 = event.Mouse(win=win)
    x, y = [None, None]
    mouse_2.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "feedback" ---
    fb_txt = visual.TextStim(win=win, name='fb_txt',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "instructions_2" ---
    instr_textbox_2 = visual.TextBox2(
         win, text="OK let's start the real thing!\n", placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(1, 0.8), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='instr_textbox_2',
         depth=0, autoLog=True,
    )
    start_button_2 = visual.ButtonStim(win, 
        text='START', font='Arvo',
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
        depth=-1
    )
    start_button_2.buttonClock = core.Clock()
    
    # --- Initialize components for Routine "trial" ---
    left_circle = visual.ShapeStim(
        win=win, name='left_circle',
        size=(0.25, 0.25), vertices='circle',
        ori=0.0, pos=(0.5, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    right_circle = visual.ShapeStim(
        win=win, name='right_circle',
        size=(0.25, 0.25), vertices='circle',
        ori=0.0, pos=(-0.5, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "feedback" ---
    fb_txt = visual.TextStim(win=win, name='fb_txt',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
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
        components=[instr_textbox, start_button],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    instr_textbox.reset()
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
        
        # *instr_textbox* updates
        
        # if instr_textbox is starting this frame...
        if instr_textbox.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instr_textbox.frameNStart = frameN  # exact frame index
            instr_textbox.tStart = t  # local t and not account for scr refresh
            instr_textbox.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_textbox, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instr_textbox.started')
            # update status
            instr_textbox.status = STARTED
            instr_textbox.setAutoDraw(True)
        
        # if instr_textbox is active this frame...
        if instr_textbox.status == STARTED:
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
    trials_2 = data.TrialHandler2(
        name='trials_2',
        nReps=1.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('practice_conditions.xlsx'), 
        seed=None, 
    )
    thisExp.addLoop(trials_2)  # add the loop to the experiment
    thisTrial_2 = trials_2.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
    if thisTrial_2 != None:
        for paramName in thisTrial_2:
            globals()[paramName] = thisTrial_2[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisTrial_2 in trials_2:
        trials_2.status = STARTED
        if hasattr(thisTrial_2, 'status'):
            thisTrial_2.status = STARTED
        currentLoop = trials_2
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
        if thisTrial_2 != None:
            for paramName in thisTrial_2:
                globals()[paramName] = thisTrial_2[paramName]
        
        # set up handler to look after randomisation of conditions etc
        loop_until_correct = data.TrialHandler2(
            name='loop_until_correct',
            nReps=10.0, 
            method='random', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=[None], 
            seed=None, 
        )
        thisExp.addLoop(loop_until_correct)  # add the loop to the experiment
        thisLoop_until_correct = loop_until_correct.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisLoop_until_correct.rgb)
        if thisLoop_until_correct != None:
            for paramName in thisLoop_until_correct:
                globals()[paramName] = thisLoop_until_correct[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisLoop_until_correct in loop_until_correct:
            loop_until_correct.status = STARTED
            if hasattr(thisLoop_until_correct, 'status'):
                thisLoop_until_correct.status = STARTED
            currentLoop = loop_until_correct
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisLoop_until_correct.rgb)
            if thisLoop_until_correct != None:
                for paramName in thisLoop_until_correct:
                    globals()[paramName] = thisLoop_until_correct[paramName]
            
            # --- Prepare to start Routine "practice_trial" ---
            # create an object to store info about Routine practice_trial
            practice_trial = data.Routine(
                name='practice_trial',
                components=[left_circle_2, right_circle_2, mouse_2],
            )
            practice_trial.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            left_circle_2.setFillColor(left_color)
            left_circle_2.setLineColor(left_color)
            right_circle_2.setFillColor(right_color)
            right_circle_2.setLineColor(right_color)
            # setup some python lists for storing info about the mouse_2
            mouse_2.x = []
            mouse_2.y = []
            mouse_2.leftButton = []
            mouse_2.midButton = []
            mouse_2.rightButton = []
            mouse_2.time = []
            mouse_2.clicked_name = []
            gotValidClick = False  # until a click is received
            # store start times for practice_trial
            practice_trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            practice_trial.tStart = globalClock.getTime(format='float')
            practice_trial.status = STARTED
            thisExp.addData('practice_trial.started', practice_trial.tStart)
            practice_trial.maxDuration = None
            # keep track of which components have finished
            practice_trialComponents = practice_trial.components
            for thisComponent in practice_trial.components:
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
            
            # --- Run Routine "practice_trial" ---
            practice_trial.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # if trial has changed, end Routine now
                if hasattr(thisLoop_until_correct, 'status') and thisLoop_until_correct.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *left_circle_2* updates
                
                # if left_circle_2 is starting this frame...
                if left_circle_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    left_circle_2.frameNStart = frameN  # exact frame index
                    left_circle_2.tStart = t  # local t and not account for scr refresh
                    left_circle_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(left_circle_2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'left_circle_2.started')
                    # update status
                    left_circle_2.status = STARTED
                    left_circle_2.setAutoDraw(True)
                
                # if left_circle_2 is active this frame...
                if left_circle_2.status == STARTED:
                    # update params
                    pass
                
                # *right_circle_2* updates
                
                # if right_circle_2 is starting this frame...
                if right_circle_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    right_circle_2.frameNStart = frameN  # exact frame index
                    right_circle_2.tStart = t  # local t and not account for scr refresh
                    right_circle_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(right_circle_2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'right_circle_2.started')
                    # update status
                    right_circle_2.status = STARTED
                    right_circle_2.setAutoDraw(True)
                
                # if right_circle_2 is active this frame...
                if right_circle_2.status == STARTED:
                    # update params
                    pass
                # *mouse_2* updates
                
                # if mouse_2 is starting this frame...
                if mouse_2.status == NOT_STARTED and t >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    mouse_2.frameNStart = frameN  # exact frame index
                    mouse_2.tStart = t  # local t and not account for scr refresh
                    mouse_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mouse_2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.addData('mouse_2.started', t)
                    # update status
                    mouse_2.status = STARTED
                    mouse_2.mouseClock.reset()
                    prevButtonState = mouse_2.getPressed()  # if button is down already this ISN'T a new click
                if mouse_2.status == STARTED:  # only update if started and not finished!
                    buttons = mouse_2.getPressed()
                    if buttons != prevButtonState:  # button state changed?
                        prevButtonState = buttons
                        if sum(buttons) > 0:  # state changed to a new click
                            # check if the mouse was inside our 'clickable' objects
                            gotValidClick = False
                            clickableList = environmenttools.getFromNames([left_circle_2, right_circle_2], namespace=locals())
                            for obj in clickableList:
                                # is this object clicked on?
                                if obj.contains(mouse_2):
                                    gotValidClick = True
                                    mouse_2.clicked_name.append(obj.name)
                            if not gotValidClick:
                                mouse_2.clicked_name.append(None)
                            x, y = mouse_2.getPos()
                            mouse_2.x.append(x)
                            mouse_2.y.append(y)
                            buttons = mouse_2.getPressed()
                            mouse_2.leftButton.append(buttons[0])
                            mouse_2.midButton.append(buttons[1])
                            mouse_2.rightButton.append(buttons[2])
                            mouse_2.time.append(mouse_2.mouseClock.getTime())
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
                        timers=[routineTimer, globalClock], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    practice_trial.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in practice_trial.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "practice_trial" ---
            for thisComponent in practice_trial.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for practice_trial
            practice_trial.tStop = globalClock.getTime(format='float')
            practice_trial.tStopRefresh = tThisFlipGlobal
            thisExp.addData('practice_trial.stopped', practice_trial.tStop)
            # store data for loop_until_correct (TrialHandler)
            loop_until_correct.addData('mouse_2.x', mouse_2.x)
            loop_until_correct.addData('mouse_2.y', mouse_2.y)
            loop_until_correct.addData('mouse_2.leftButton', mouse_2.leftButton)
            loop_until_correct.addData('mouse_2.midButton', mouse_2.midButton)
            loop_until_correct.addData('mouse_2.rightButton', mouse_2.rightButton)
            loop_until_correct.addData('mouse_2.time', mouse_2.time)
            loop_until_correct.addData('mouse_2.clicked_name', mouse_2.clicked_name)
            # Run 'End Routine' code from check_correct1
            # check if the participant was correct
            if mouse_2.clicked_name[-1] == correct_response:
                correct = 1
                # end this inner loop and move onto the next example
                loop_until_correct.finished = True
            else:
                correct = 0
            
            thisExp.addData('correct', correct)
            # the Routine "practice_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # --- Prepare to start Routine "feedback" ---
            # create an object to store info about Routine feedback
            feedback = data.Routine(
                name='feedback',
                components=[fb_txt],
            )
            feedback.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_2
            if correct:
                fb = 'Correct!'
            else:
                fb = 'Incorrect'
            fb_txt.setText(fb)
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
                if hasattr(thisLoop_until_correct, 'status') and thisLoop_until_correct.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *fb_txt* updates
                
                # if fb_txt is starting this frame...
                if fb_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    fb_txt.frameNStart = frameN  # exact frame index
                    fb_txt.tStart = t  # local t and not account for scr refresh
                    fb_txt.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(fb_txt, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fb_txt.started')
                    # update status
                    fb_txt.status = STARTED
                    fb_txt.setAutoDraw(True)
                
                # if fb_txt is active this frame...
                if fb_txt.status == STARTED:
                    # update params
                    pass
                
                # if fb_txt is stopping this frame...
                if fb_txt.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > fb_txt.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        fb_txt.tStop = t  # not accounting for scr refresh
                        fb_txt.tStopRefresh = tThisFlipGlobal  # on global time
                        fb_txt.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'fb_txt.stopped')
                        # update status
                        fb_txt.status = FINISHED
                        fb_txt.setAutoDraw(False)
                
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
            # mark thisLoop_until_correct as finished
            if hasattr(thisLoop_until_correct, 'status'):
                thisLoop_until_correct.status = FINISHED
            # if awaiting a pause, pause now
            if loop_until_correct.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                loop_until_correct.status = STARTED
            thisExp.nextEntry()
            
        # completed 10.0 repeats of 'loop_until_correct'
        loop_until_correct.status = FINISHED
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # mark thisTrial_2 as finished
        if hasattr(thisTrial_2, 'status'):
            thisTrial_2.status = FINISHED
        # if awaiting a pause, pause now
        if trials_2.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            trials_2.status = STARTED
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'trials_2'
    trials_2.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "instructions_2" ---
    # create an object to store info about Routine instructions_2
    instructions_2 = data.Routine(
        name='instructions_2',
        components=[instr_textbox_2, start_button_2],
    )
    instructions_2.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    instr_textbox_2.reset()
    # reset start_button_2 to account for continued clicks & clear times on/off
    start_button_2.reset()
    # store start times for instructions_2
    instructions_2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructions_2.tStart = globalClock.getTime(format='float')
    instructions_2.status = STARTED
    thisExp.addData('instructions_2.started', instructions_2.tStart)
    instructions_2.maxDuration = None
    # keep track of which components have finished
    instructions_2Components = instructions_2.components
    for thisComponent in instructions_2.components:
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
    
    # --- Run Routine "instructions_2" ---
    instructions_2.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instr_textbox_2* updates
        
        # if instr_textbox_2 is starting this frame...
        if instr_textbox_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instr_textbox_2.frameNStart = frameN  # exact frame index
            instr_textbox_2.tStart = t  # local t and not account for scr refresh
            instr_textbox_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_textbox_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instr_textbox_2.started')
            # update status
            instr_textbox_2.status = STARTED
            instr_textbox_2.setAutoDraw(True)
        
        # if instr_textbox_2 is active this frame...
        if instr_textbox_2.status == STARTED:
            # update params
            pass
        # *start_button_2* updates
        
        # if start_button_2 is starting this frame...
        if start_button_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
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
            instructions_2.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructions_2.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructions_2" ---
    for thisComponent in instructions_2.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instructions_2
    instructions_2.tStop = globalClock.getTime(format='float')
    instructions_2.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructions_2.stopped', instructions_2.tStop)
    thisExp.addData('start_button_2.numClicks', start_button_2.numClicks)
    if start_button_2.numClicks:
       thisExp.addData('start_button_2.timesOn', start_button_2.timesOn)
       thisExp.addData('start_button_2.timesOff', start_button_2.timesOff)
    else:
       thisExp.addData('start_button_2.timesOn', "")
       thisExp.addData('start_button_2.timesOff', "")
    thisExp.nextEntry()
    # the Routine "instructions_2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler2(
        name='trials',
        nReps=5.0, 
        method='random', 
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
            components=[left_circle, right_circle, mouse],
        )
        trial.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        left_circle.setFillColor(left_color)
        left_circle.setLineColor(left_color)
        right_circle.setFillColor(right_color)
        right_circle.setLineColor(right_color)
        # setup some python lists for storing info about the mouse
        mouse.x = []
        mouse.y = []
        mouse.leftButton = []
        mouse.midButton = []
        mouse.rightButton = []
        mouse.time = []
        mouse.clicked_name = []
        gotValidClick = False  # until a click is received
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
            
            # *left_circle* updates
            
            # if left_circle is starting this frame...
            if left_circle.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                left_circle.frameNStart = frameN  # exact frame index
                left_circle.tStart = t  # local t and not account for scr refresh
                left_circle.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(left_circle, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'left_circle.started')
                # update status
                left_circle.status = STARTED
                left_circle.setAutoDraw(True)
            
            # if left_circle is active this frame...
            if left_circle.status == STARTED:
                # update params
                pass
            
            # *right_circle* updates
            
            # if right_circle is starting this frame...
            if right_circle.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                right_circle.frameNStart = frameN  # exact frame index
                right_circle.tStart = t  # local t and not account for scr refresh
                right_circle.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(right_circle, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'right_circle.started')
                # update status
                right_circle.status = STARTED
                right_circle.setAutoDraw(True)
            
            # if right_circle is active this frame...
            if right_circle.status == STARTED:
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
                        clickableList = environmenttools.getFromNames([left_circle, right_circle], namespace=locals())
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
        # Run 'End Routine' code from check_correct2
        if mouse.clicked_name[-1] == correct_response:
            correct = 1
        else:
            correct = 0
        
        thisExp.addData('correct', correct)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "feedback" ---
        # create an object to store info about Routine feedback
        feedback = data.Routine(
            name='feedback',
            components=[fb_txt],
        )
        feedback.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_2
        if correct:
            fb = 'Correct!'
        else:
            fb = 'Incorrect'
        fb_txt.setText(fb)
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
            
            # *fb_txt* updates
            
            # if fb_txt is starting this frame...
            if fb_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fb_txt.frameNStart = frameN  # exact frame index
                fb_txt.tStart = t  # local t and not account for scr refresh
                fb_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fb_txt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fb_txt.started')
                # update status
                fb_txt.status = STARTED
                fb_txt.setAutoDraw(True)
            
            # if fb_txt is active this frame...
            if fb_txt.status == STARTED:
                # update params
                pass
            
            # if fb_txt is stopping this frame...
            if fb_txt.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fb_txt.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    fb_txt.tStop = t  # not accounting for scr refresh
                    fb_txt.tStopRefresh = tThisFlipGlobal  # on global time
                    fb_txt.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fb_txt.stopped')
                    # update status
                    fb_txt.status = FINISHED
                    fb_txt.setAutoDraw(False)
            
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
