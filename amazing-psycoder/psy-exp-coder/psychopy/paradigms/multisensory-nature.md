# Multisensory Nature — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [multisensory-nature](../../../psy-exp-designer/paradigms/multisensory-nature.md)
> **Source**: [Pavlovia demos/multisensory_nature](https://gitlab.pavlovia.org/demos/multisensory_nature) · PsychoPy 2024.1.5

## Experiment Logic

The experiment presents nature video clips to participants and collects mood ratings using the I-PANAS-SF (International Positive and Negative Affect Schedule Short Form) questionnaire. It is built with a nested two-loop design where each outer trial displays a video and the inner loop presents mood rating questions one at a time.

The outer loop loads trial conditions from `vids.xlsx` via `data.importConditions()`. Each row represents a video to play, with a column `this_vid` specifying the video filename. The `TrialHandler` runs with `nReps=1.0` and `method='random'`. Inside each outer trial, an inner loop loads `I-PANAS-SF.xlsx`, which contains the questionnaire items -- each row defines a mood question (`this_q`) with its associated text. The inner loop also uses `nReps=1.0` and `method='random'` (the 20 PANAS items are presented in random order).

The single routine "play_vid" handles everything: the video plays via `visual.MovieStim` with `movie.setMovie(this_vid)`, the current question is displayed via `visual.TextBox2` (`slider_qs_2.setText(this_q)`), and the participant responds on a `visual.Slider` component. The slider uses `style='radio'` with labels `('Never', 'Always')` and `granularity=1`, making it a 5-point Likert-type scale (values 1-5). All three components start simultaneously at time 0 and have a maximum duration of 60 seconds. The routine ends when the participant provides a rating, detected by checking `slider_2.getRating() is not None`, or when the 60-second timeout elapses.

The video plays in a continuous loop using the movie component's built-in playback. The movie component's lifecycle is managed through status tracking: it transitions from NOT_STARTED to STARTED (with `movie.play()` called at onset), and to FINISHED after 60 seconds (with `movie.stop()`). Per-rating data including `slider_2.response` (the rating value) and `slider_2.rt` (reaction time) is stored to the inner loop handler. The experiment uses ioHub for keyboard device management and supports pilot mode via `core.setPilotModeFromArgs()` with windowed overrides. The background uses a warm beige color `[0.9608, 0.8431, 0.6863]` in RGB space.

## Key Design Patterns

- Nested `data.TrialHandler` loops: outer loop (vids.xlsx, video clips) containing inner loop (I-PANAS-SF.xlsx, questionnaire items), each with `nReps=1.0` and `method='random'`
- `visual.MovieStim` for video playback with dynamic filename via `movie.setMovie(this_vid)` from condition file column
- `visual.Slider` with `style='radio'` and `labels=('Never', 'Always')` for Likert-scale rating collection with `granularity=1`
- Non-slip timing with 60-second maximum duration per routine via `routineTimer.getTime() < 60.0`
- Movie component lifecycle: `setAutoDraw(True)`, `play()`, `stop()` with STARTED/FINISHED state tracking and frame-accurate start/stop via `tStartRefresh`
- Slider response check via `slider_2.getRating() is not None` to end the routine early when participant provides a rating
- Component-level data storage: `slider_questions.addData('slider_2.response', slider_2.getRating())` and `slider_2.getRT()`
- ioHub backend for keyboard device management via `psychopy.iohub` and `deviceManager`
- PILOTING mode support via `core.setPilotModeFromArgs()` with forced windowed mode and size overrides
- Component stop timing via `tThisFlipGlobal > component.tStartRefresh + duration - frameTolerance` for frame-accurate offset

## Code Example

Complete runnable PsychoPy code for Multisensory Nature task:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.1.5),
    on Fri Aug 23 13:00:43 2024
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
expName = 'multisensory_nature'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
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
        originPath='/Users/kimdundas/Library/CloudStorage/GoogleDrive-kim@opensciencetools.org/Shared drives/Science/Conferences/ECVP 2024/1 in 5 project demos/multisensory_nature/multisensory_nature.py',
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
            monitor='testMonitor', color=[0.9608, 0.8431, 0.6863], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height', 
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0.9608, 0.8431, 0.6863]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win.getActualFrameRate(infoMsg='Loading, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.mouseVisible = True
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
    
    # --- Initialize components for Routine "play_vid" ---
    movie = visual.MovieStim(
        win, name='movie',
        filename=None, movieLib='ffpyplayer',
        loop=False, volume=1.0, noAudio=False,
        pos=(0, 0.1), size=(1.23, 0.7), units=win.units,
        ori=0.0, anchor='center',opacity=None, contrast=1.0,
        depth=0
    )
    slider_qs_2 = visual.TextBox2(
         win, text='', placeholder='Type here...', font='Arial',
         pos=(0, -0.35),     letterHeight=0.05,
         size=(1.4, 0.2), borderWidth=2.0,
         color=[-0.6314, -0.3804, -0.3804], colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='slider_qs_2',
         depth=-1, autoLog=True,
    )
    slider_2 = visual.Slider(win=win, name='slider_2',
        startValue=None, size=(1.0, 0.1), pos=(0, -0.4), units=win.units,
        labels=('Never', 'Always'),ticks=None, granularity=1,
        style='radio', styleTweaks=(), opacity=None,
        labelColor=[-0.2549, 0.2392, 0.2549], markerColor=[-0.2157, 0.1686, 0.8588], lineColor=[-0.6314, -0.3804, -0.3804], colorSpace='rgb',
        font='Open Sans', labelHeight=0.03,
        flip=False, ori=0.0, depth=-2, readOnly=False)
    
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
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1.0, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('vids.xlsx'),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]
    
    for thisTrial in trials:
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        # set up handler to look after randomisation of conditions etc
        slider_questions = data.TrialHandler(nReps=1.0, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=data.importConditions('I-PANAS-SF.xlsx'),
            seed=None, name='slider_questions')
        thisExp.addLoop(slider_questions)  # add the loop to the experiment
        thisSlider_question = slider_questions.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSlider_question.rgb)
        if thisSlider_question != None:
            for paramName in thisSlider_question:
                globals()[paramName] = thisSlider_question[paramName]
        
        for thisSlider_question in slider_questions:
            currentLoop = slider_questions
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
            )
            # abbreviate parameter names if possible (e.g. rgb = thisSlider_question.rgb)
            if thisSlider_question != None:
                for paramName in thisSlider_question:
                    globals()[paramName] = thisSlider_question[paramName]
            
            # --- Prepare to start Routine "play_vid" ---
            continueRoutine = True
            # update component parameters for each repeat
            thisExp.addData('play_vid.started', globalClock.getTime(format='float'))
            movie.setMovie(this_vid)
            slider_qs_2.reset()
            slider_qs_2.setText(this_q)
            slider_2.reset()
            # keep track of which components have finished
            play_vidComponents = [movie, slider_qs_2, slider_2]
            for thisComponent in play_vidComponents:
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
            
            # --- Run Routine "play_vid" ---
            routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 60.0:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *movie* updates
                
                # if movie is starting this frame...
                if movie.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    movie.frameNStart = frameN  # exact frame index
                    movie.tStart = t  # local t and not account for scr refresh
                    movie.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(movie, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'movie.started')
                    # update status
                    movie.status = STARTED
                    movie.setAutoDraw(True)
                    movie.play()
                
                # if movie is stopping this frame...
                if movie.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > movie.tStartRefresh + 60-frameTolerance:
                        # keep track of stop time/frame for later
                        movie.tStop = t  # not accounting for scr refresh
                        movie.tStopRefresh = tThisFlipGlobal  # on global time
                        movie.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'movie.stopped')
                        # update status
                        movie.status = FINISHED
                        movie.setAutoDraw(False)
                        movie.stop()
                
                # *slider_qs_2* updates
                
                # if slider_qs_2 is starting this frame...
                if slider_qs_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    slider_qs_2.frameNStart = frameN  # exact frame index
                    slider_qs_2.tStart = t  # local t and not account for scr refresh
                    slider_qs_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(slider_qs_2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'slider_qs_2.started')
                    # update status
                    slider_qs_2.status = STARTED
                    slider_qs_2.setAutoDraw(True)
                
                # if slider_qs_2 is active this frame...
                if slider_qs_2.status == STARTED:
                    # update params
                    pass
                
                # if slider_qs_2 is stopping this frame...
                if slider_qs_2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > slider_qs_2.tStartRefresh + 60-frameTolerance:
                        # keep track of stop time/frame for later
                        slider_qs_2.tStop = t  # not accounting for scr refresh
                        slider_qs_2.tStopRefresh = tThisFlipGlobal  # on global time
                        slider_qs_2.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'slider_qs_2.stopped')
                        # update status
                        slider_qs_2.status = FINISHED
                        slider_qs_2.setAutoDraw(False)
                
                # *slider_2* updates
                
                # if slider_2 is starting this frame...
                if slider_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    slider_2.frameNStart = frameN  # exact frame index
                    slider_2.tStart = t  # local t and not account for scr refresh
                    slider_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(slider_2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'slider_2.started')
                    # update status
                    slider_2.status = STARTED
                    slider_2.setAutoDraw(True)
                
                # if slider_2 is active this frame...
                if slider_2.status == STARTED:
                    # update params
                    pass
                
                # if slider_2 is stopping this frame...
                if slider_2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > slider_2.tStartRefresh + 60-frameTolerance:
                        # keep track of stop time/frame for later
                        slider_2.tStop = t  # not accounting for scr refresh
                        slider_2.tStopRefresh = tThisFlipGlobal  # on global time
                        slider_2.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'slider_2.stopped')
                        # update status
                        slider_2.status = FINISHED
                        slider_2.setAutoDraw(False)
                
                # Check slider_2 for response to end Routine
                if slider_2.getRating() is not None and slider_2.status == STARTED:
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
                for thisComponent in play_vidComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "play_vid" ---
            for thisComponent in play_vidComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            thisExp.addData('play_vid.stopped', globalClock.getTime(format='float'))
            slider_questions.addData('slider_2.response', slider_2.getRating())
            slider_questions.addData('slider_2.rt', slider_2.getRT())
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if routineForceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-60.000000)
            thisExp.nextEntry()
            
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
        # completed 1.0 repeats of 'slider_questions'
        
    # completed 1.0 repeats of 'trials'
    
    
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
```
