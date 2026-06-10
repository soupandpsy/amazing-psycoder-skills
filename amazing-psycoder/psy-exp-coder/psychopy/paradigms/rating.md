# Rating — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [rating](../../../psy-exp-designer/paradigms/rating.md)
> **Source**: [Pavlovia demos/emotion_rating](https://gitlab.pavlovia.org/demos/emotion_rating) · PsychoPy 2024.1.5

## Experiment Logic

The Emotion Rating task presents participants with facial expression images and asks them to make two judgments per image: first, a categorical emotion classification, then a continuous age estimate via a slider.

On each trial, a face image is displayed in the upper half of the screen. Below it, six emotion labels (Happiness, Anger, Fear, Sadness, Neutral, Disgust) are shown as colored button-like boxes. The horizontal positions of these six labels are randomly shuffled on each trial to prevent position-based response biases. The participant clicks one of the six labels to indicate the primary emotion expressed. A highlight rectangle (a `visual.Rect`) is drawn around the selected label to provide visual feedback. The selection can be changed by clicking a different label; the highlight rectangle moves accordingly. Once satisfied, the participant clicks a "Continue" button below the labels to confirm their choice and advance.

After the emotion classification, the same face image appears again with the question "How old is this person?" and a horizontal visual analog scale (`visual.Slider`, style='slider') ranging from 0 to 100 years. The slider has labeled anchors ("0 Years" and "100 Years") and tick marks at 0, 50, and 100. The participant drags the slider marker to their estimate. The "Continue" button is conditionally hidden until the slider has been interacted with (`slider.rating` evaluates to a truthy value). The confirmatory click on the Continue button ends the routine and records both the slider rating value and the slider response time (measured internally by the Slider component from its first interaction).

Data is saved via PsychoPy's `ExperimentHandler` and `TrialHandler`. For the emotion_selection routine, the chosen emotion label name is saved as the `answer` column. For the age_rating routine, `slider.response` (the rating value, 0-100) and `slider.rt` (response time on the slider) are recorded. In addition, full mouse interaction data (x, y, button states, timestamps, and which objects were clicked) is logged for every routine with clickable elements. Trials are driven by a CSV file (`images/image_metadata.csv`) that lists image filenames; the TrialHandler randomizes order with 1 repetition.

## Variants

### Heart Throb Slider

The Heart Throb Slider demo (PsychoPy 2023.1.3) uses a `visual.Slider` with `style='rating'` (a click-to-set scale with discrete numbered ticks 1-6) to control a real-time animation. The slider is labeled "Slower" to "Faster" and its current marker position is read every frame. That value drives a sinusoidal heartbeat animation: `heart.setSize([.25 + .125 * (sin(t*thisRating))**4])`, where `thisRating` comes from `slider.markerPos`. Unlike the discrete two-step emotion/age rating above, this variant is a continuous rating paradigm -- the participant adjusts the slider and sees the effect in real time for a fixed 20-second duration. No confirmatory button press is used; the trial simply times out. Per-frame data (heart height, timestamp) is logged via `nextEntry()`, and the final rating is saved in the end-routine code.

## Key Design Patterns

- **Randomized button positions**: The six emotion labels are shuffled to different x-positions each trial via `shuffle(response_x_positions)`, eliminating spatial response bias.
- **Highlight rectangle for feedback**: A `visual.Rect` component (`response_highlight`) is repositioned to match the x-position of whichever emotion label was last clicked, giving clear visual feedback about the current selection.
- **Conditional Continue button**: In the age_rating routine, `continue_button_2` only becomes visible after the slider has been rated: `if continue_button_2.status == NOT_STARTED and slider.rating:` -- this enforces that a rating must be made before advancing.
- **Each-frame code for multi-step response**: The emotion_selection routine uses Builder "Each Frame" code blocks to check `mouse.clicked_name` on every frame, update the highlight position, and detect when the participant clicks the Continue button after having made a selection.
- **TrialHandler with CSV conditions**: Stimuli are loaded from `image_metadata.csv` via `data.importConditions()`, with the column `Image_Name` used to set each trial's image. Randomization is handled by `TrialHandler(nReps=1.0, method='random')`.
- **Full mouse-event logging**: Each mouse-equipped routine captures lists of x, y, button states, timestamps, and clicked object names, then flushes them to the data file via `addData()` / `trials.addData()` at routine end.

## Code Example (Emotion Rating)

Complete runnable PsychoPy code for Emotion Rating task:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.1.5),
    on Thu Jan  2 16:14:37 2025
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
psychopyVersion = '2024.1.5'
expName = 'emotion_rating'  # from the Builder filename that created this script
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
        originPath='/Users/Becca/Library/CloudStorage/GoogleDrive-becca@opensciencetools.org/Shared drives/Science/Pavlovia Demos/Emotion Rating/emotion_rating_lastrun.py',
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
            win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
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
            backend='PsychToolbox',
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
         win, text='Welcome! \n\nIn this task you will see some faces. you will be asked what emotion each face primarily shows, then you will be asked to judge the age of the person in the picture. \n\nClick below to start', placeholder='Type here...', font='Arial',
         pos=(0, 0),     letterHeight=0.05,
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
         name='instrtxt',
         depth=0, autoLog=True,
    )
    continue_button_3 = visual.TextBox2(
         win, text='Continue', placeholder='Type here...', font='Arial',
         pos=(0, -0.42),     letterHeight=0.04,
         size=(0.5, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[-0.6314, -0.3804, -0.3804], borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='continue_button_3',
         depth=-1, autoLog=True,
    )
    start_mouse = event.Mouse(win=win)
    x, y = [None, None]
    start_mouse.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "emotion_selection" ---
    happy = visual.TextBox2(
         win, text='Happiness', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.04,
         size=(0.2, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[0.0588, 0.6157, 0.8431], borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='happy',
         depth=-2, autoLog=True,
    )
    anger = visual.TextBox2(
         win, text='Anger', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.04,
         size=(0.2, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[0.0588, 0.6157, 0.8431], borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='anger',
         depth=-3, autoLog=True,
    )
    fear = visual.TextBox2(
         win, text='Fear', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.04,
         size=(0.2, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[0.0588, 0.6157, 0.8431], borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='fear',
         depth=-4, autoLog=True,
    )
    sadness = visual.TextBox2(
         win, text='Sadness', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.04,
         size=(0.2, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[0.0588, 0.6157, 0.8431], borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='sadness',
         depth=-5, autoLog=True,
    )
    neutral = visual.TextBox2(
         win, text='Neutral', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.04,
         size=(0.2, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[0.0588, 0.6157, 0.8431], borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='neutral',
         depth=-6, autoLog=True,
    )
    disgust = visual.TextBox2(
         win, text='Disgust', placeholder='Type here...', font='Arial',
         pos=[0,0],     letterHeight=0.04,
         size=(0.2, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[0.0588, 0.6157, 0.8431], borderColor='black',
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='disgust',
         depth=-7, autoLog=True,
    )
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()
    continue_button = visual.TextBox2(
         win, text='Continue', placeholder='Type here...', font='Arial',
         pos=(0, -0.42),     letterHeight=0.04,
         size=(0.5, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[-0.6314, -0.3804, -0.3804], borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='continue_button',
         depth=-9, autoLog=True,
    )
    emotionq = visual.TextBox2(
         win, text='Which facial expression does this person primarily show?', placeholder='Type here...', font='Arial',
         pos=(0, -0.15),     letterHeight=0.04,
         size=(1.5, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='emotionq',
         depth=-10, autoLog=True,
    )
    image = visual.ImageStim(
        win=win,
        name='image', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0.15), size=(0.4, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-11.0)
    response_highlight = visual.Rect(
        win=win, name='response_highlight',
        width=(0.2, 0.1)[0], height=(0.2, 0.1)[1],
        ori=0.0, pos=[0,0], anchor='center',
        lineWidth=6.0,     colorSpace='rgb',  lineColor=[-0.6314, -0.3804, -0.3804], fillColor=None,
        opacity=None, depth=-12.0, interpolate=True)
    
    # --- Initialize components for Routine "age_rating" ---
    image_2 = visual.ImageStim(
        win=win,
        name='image_2', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0.15), size=(0.4, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    ageq = visual.TextBox2(
         win, text='How old is this person?', placeholder='Type here...', font='Arial',
         pos=(0, -0.15),     letterHeight=0.04,
         size=(1.5, 0.1), borderWidth=2.0,
         color='black', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='ageq',
         depth=-1, autoLog=True,
    )
    slider = visual.Slider(win=win, name='slider',
        startValue=None, size=(1.0, 0.05), pos=(0, -0.25), units=win.units,
        labels=['0 Years', '100 Years'], ticks=(0,50, 100), granularity=0.0,
        style='slider', styleTweaks=(), opacity=None,
        labelColor='LightGray', markerColor='Red', lineColor=[0.0588, 0.6157, 0.8431], colorSpace='rgb',
        font='Open Sans', labelHeight=0.05,
        flip=False, ori=0.0, depth=-2, readOnly=False)
    continue_button_2 = visual.TextBox2(
         win, text='Continue', placeholder='Type here...', font='Arial',
         pos=(0, -0.42),     letterHeight=0.04,
         size=(0.5, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[-0.6314, -0.3804, -0.3804], borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='continue_button_2',
         depth=-3, autoLog=True,
    )
    mouse_2 = event.Mouse(win=win)
    x, y = [None, None]
    mouse_2.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "thanks" ---
    thankstxt = visual.TextBox2(
         win, text='Thank you for taking part!\n\nClick below to exit the task.', placeholder='Type here...', font='Arial',
         pos=(0, 0),     letterHeight=0.05,
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
         name='thankstxt',
         depth=0, autoLog=True,
    )
    continue_button_4 = visual.TextBox2(
         win, text='Exit task', placeholder='Type here...', font='Arial',
         pos=(0, -0.42),     letterHeight=0.04,
         size=(0.5, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=[-0.6314, -0.3804, -0.3804], borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='continue_button_4',
         depth=-1, autoLog=True,
    )
    end_mouse = event.Mouse(win=win)
    x, y = [None, None]
    end_mouse.mouseClock = core.Clock()
    
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
    instrtxt.reset()
    continue_button_3.reset()
    # setup some python lists for storing info about the start_mouse
    start_mouse.x = []
    start_mouse.y = []
    start_mouse.leftButton = []
    start_mouse.midButton = []
    start_mouse.rightButton = []
    start_mouse.time = []
    start_mouse.clicked_name = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    instructionsComponents = [instrtxt, continue_button_3, start_mouse]
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
        
        # *continue_button_3* updates
        
        # if continue_button_3 is starting this frame...
        if continue_button_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            continue_button_3.frameNStart = frameN  # exact frame index
            continue_button_3.tStart = t  # local t and not account for scr refresh
            continue_button_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(continue_button_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'continue_button_3.started')
            # update status
            continue_button_3.status = STARTED
            continue_button_3.setAutoDraw(True)
        
        # if continue_button_3 is active this frame...
        if continue_button_3.status == STARTED:
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
                    clickableList = environmenttools.getFromNames(continue_button_3, namespace=locals())
                    for obj in clickableList:
                        # is this object clicked on?
                        if obj.contains(start_mouse):
                            gotValidClick = True
                            start_mouse.clicked_name.append(obj.name)
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
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('start_mouse.x', start_mouse.x)
    thisExp.addData('start_mouse.y', start_mouse.y)
    thisExp.addData('start_mouse.leftButton', start_mouse.leftButton)
    thisExp.addData('start_mouse.midButton', start_mouse.midButton)
    thisExp.addData('start_mouse.rightButton', start_mouse.rightButton)
    thisExp.addData('start_mouse.time', start_mouse.time)
    thisExp.addData('start_mouse.clicked_name', start_mouse.clicked_name)
    thisExp.nextEntry()
    # the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1.0, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('images/image_metadata.csv'),
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
        
        # --- Prepare to start Routine "emotion_selection" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('emotion_selection.started', globalClock.getTime(format='float'))
        # Run 'Begin Routine' code from show_response
        answer = None
        
        responses = [happy, anger, fear, sadness, neutral, disgust]
        
        # Run 'Begin Routine' code from rand_locations
        #randomise the locations of the response options
        response_x_positions = [-0.5, -0.3, -0.1, 0.1, 0.3, 0.5]
        shuffle(response_x_positions)
        happy.reset()
        happy.setPos((response_x_positions[0], -0.25))
        anger.reset()
        anger.setPos((response_x_positions[1], -0.25))
        fear.reset()
        fear.setPos((response_x_positions[2], -0.25))
        sadness.reset()
        sadness.setPos((response_x_positions[3], -0.25))
        neutral.reset()
        neutral.setPos((response_x_positions[4], -0.25))
        disgust.reset()
        disgust.setPos((response_x_positions[5], -0.25))
        # setup some python lists for storing info about the mouse
        mouse.x = []
        mouse.y = []
        mouse.leftButton = []
        mouse.midButton = []
        mouse.rightButton = []
        mouse.time = []
        mouse.clicked_name = []
        gotValidClick = False  # until a click is received
        continue_button.reset()
        emotionq.reset()
        image.setImage('images/'+Image_Name)
        response_highlight.setPos((-500, 0))
        # keep track of which components have finished
        emotion_selectionComponents = [happy, anger, fear, sadness, neutral, disgust, mouse, continue_button, emotionq, image, response_highlight]
        for thisComponent in emotion_selectionComponents:
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
        
        # --- Run Routine "emotion_selection" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from show_response
            # controls changing the color of response options depending on what was selected
            if mouse.clicked_name:
                for this_response in responses:
                    if mouse.clicked_name[-1] == this_response.name:
                        response_highlight.setPos([this_response.pos[0], this_response.pos[1]])
                        answer = this_response
            
            if answer:
                if mouse.isPressedIn(continue_button):
                    continueRoutine = False
                
            
            # *happy* updates
            
            # if happy is starting this frame...
            if happy.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                happy.frameNStart = frameN  # exact frame index
                happy.tStart = t  # local t and not account for scr refresh
                happy.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(happy, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'happy.started')
                # update status
                happy.status = STARTED
                happy.setAutoDraw(True)
            
            # if happy is active this frame...
            if happy.status == STARTED:
                # update params
                pass
            
            # *anger* updates
            
            # if anger is starting this frame...
            if anger.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                anger.frameNStart = frameN  # exact frame index
                anger.tStart = t  # local t and not account for scr refresh
                anger.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(anger, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'anger.started')
                # update status
                anger.status = STARTED
                anger.setAutoDraw(True)
            
            # if anger is active this frame...
            if anger.status == STARTED:
                # update params
                pass
            
            # *fear* updates
            
            # if fear is starting this frame...
            if fear.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fear.frameNStart = frameN  # exact frame index
                fear.tStart = t  # local t and not account for scr refresh
                fear.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fear, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fear.started')
                # update status
                fear.status = STARTED
                fear.setAutoDraw(True)
            
            # if fear is active this frame...
            if fear.status == STARTED:
                # update params
                pass
            
            # *sadness* updates
            
            # if sadness is starting this frame...
            if sadness.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                sadness.frameNStart = frameN  # exact frame index
                sadness.tStart = t  # local t and not account for scr refresh
                sadness.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(sadness, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'sadness.started')
                # update status
                sadness.status = STARTED
                sadness.setAutoDraw(True)
            
            # if sadness is active this frame...
            if sadness.status == STARTED:
                # update params
                pass
            
            # *neutral* updates
            
            # if neutral is starting this frame...
            if neutral.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                neutral.frameNStart = frameN  # exact frame index
                neutral.tStart = t  # local t and not account for scr refresh
                neutral.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(neutral, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'neutral.started')
                # update status
                neutral.status = STARTED
                neutral.setAutoDraw(True)
            
            # if neutral is active this frame...
            if neutral.status == STARTED:
                # update params
                pass
            
            # *disgust* updates
            
            # if disgust is starting this frame...
            if disgust.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                disgust.frameNStart = frameN  # exact frame index
                disgust.tStart = t  # local t and not account for scr refresh
                disgust.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(disgust, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'disgust.started')
                # update status
                disgust.status = STARTED
                disgust.setAutoDraw(True)
            
            # if disgust is active this frame...
            if disgust.status == STARTED:
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
                        clickableList = environmenttools.getFromNames([happy, anger, sadness, fear, neutral, disgust], namespace=locals())
                        for obj in clickableList:
                            # is this object clicked on?
                            if obj.contains(mouse):
                                gotValidClick = True
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
            
            # *continue_button* updates
            
            # if continue_button is starting this frame...
            if continue_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                continue_button.frameNStart = frameN  # exact frame index
                continue_button.tStart = t  # local t and not account for scr refresh
                continue_button.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(continue_button, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'continue_button.started')
                # update status
                continue_button.status = STARTED
                continue_button.setAutoDraw(True)
            
            # if continue_button is active this frame...
            if continue_button.status == STARTED:
                # update params
                pass
            
            # *emotionq* updates
            
            # if emotionq is starting this frame...
            if emotionq.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                emotionq.frameNStart = frameN  # exact frame index
                emotionq.tStart = t  # local t and not account for scr refresh
                emotionq.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(emotionq, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'emotionq.started')
                # update status
                emotionq.status = STARTED
                emotionq.setAutoDraw(True)
            
            # if emotionq is active this frame...
            if emotionq.status == STARTED:
                # update params
                pass
            
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
            
            # *response_highlight* updates
            
            # if response_highlight is starting this frame...
            if response_highlight.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                response_highlight.frameNStart = frameN  # exact frame index
                response_highlight.tStart = t  # local t and not account for scr refresh
                response_highlight.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(response_highlight, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'response_highlight.started')
                # update status
                response_highlight.status = STARTED
                response_highlight.setAutoDraw(True)
            
            # if response_highlight is active this frame...
            if response_highlight.status == STARTED:
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
            for thisComponent in emotion_selectionComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "emotion_selection" ---
        for thisComponent in emotion_selectionComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('emotion_selection.stopped', globalClock.getTime(format='float'))
        # Run 'End Routine' code from show_response
        thisExp.addData('answer', answer)
        # store data for trials (TrialHandler)
        trials.addData('mouse.x', mouse.x)
        trials.addData('mouse.y', mouse.y)
        trials.addData('mouse.leftButton', mouse.leftButton)
        trials.addData('mouse.midButton', mouse.midButton)
        trials.addData('mouse.rightButton', mouse.rightButton)
        trials.addData('mouse.time', mouse.time)
        trials.addData('mouse.clicked_name', mouse.clicked_name)
        # the Routine "emotion_selection" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "age_rating" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('age_rating.started', globalClock.getTime(format='float'))
        image_2.setImage('images/'+Image_Name)
        ageq.reset()
        slider.reset()
        continue_button_2.reset()
        # setup some python lists for storing info about the mouse_2
        mouse_2.x = []
        mouse_2.y = []
        mouse_2.leftButton = []
        mouse_2.midButton = []
        mouse_2.rightButton = []
        mouse_2.time = []
        mouse_2.clicked_name = []
        gotValidClick = False  # until a click is received
        # keep track of which components have finished
        age_ratingComponents = [image_2, ageq, slider, continue_button_2, mouse_2]
        for thisComponent in age_ratingComponents:
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
        
        # --- Run Routine "age_rating" ---
        routineForceEnded = not continueRoutine
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
                pass
            
            # *ageq* updates
            
            # if ageq is starting this frame...
            if ageq.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                ageq.frameNStart = frameN  # exact frame index
                ageq.tStart = t  # local t and not account for scr refresh
                ageq.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(ageq, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'ageq.started')
                # update status
                ageq.status = STARTED
                ageq.setAutoDraw(True)
            
            # if ageq is active this frame...
            if ageq.status == STARTED:
                # update params
                pass
            
            # *slider* updates
            
            # if slider is starting this frame...
            if slider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                slider.frameNStart = frameN  # exact frame index
                slider.tStart = t  # local t and not account for scr refresh
                slider.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(slider, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'slider.started')
                # update status
                slider.status = STARTED
                slider.setAutoDraw(True)
            
            # if slider is active this frame...
            if slider.status == STARTED:
                # update params
                pass
            
            # *continue_button_2* updates
            
            # if continue_button_2 is starting this frame...
            if continue_button_2.status == NOT_STARTED and slider.rating:
                # keep track of start time/frame for later
                continue_button_2.frameNStart = frameN  # exact frame index
                continue_button_2.tStart = t  # local t and not account for scr refresh
                continue_button_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(continue_button_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'continue_button_2.started')
                # update status
                continue_button_2.status = STARTED
                continue_button_2.setAutoDraw(True)
            
            # if continue_button_2 is active this frame...
            if continue_button_2.status == STARTED:
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
                        clickableList = environmenttools.getFromNames(continue_button_2, namespace=locals())
                        for obj in clickableList:
                            # is this object clicked on?
                            if obj.contains(mouse_2):
                                gotValidClick = True
                                mouse_2.clicked_name.append(obj.name)
                        if gotValidClick:
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
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in age_ratingComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "age_rating" ---
        for thisComponent in age_ratingComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('age_rating.stopped', globalClock.getTime(format='float'))
        trials.addData('slider.response', slider.getRating())
        trials.addData('slider.rt', slider.getRT())
        # store data for trials (TrialHandler)
        trials.addData('mouse_2.x', mouse_2.x)
        trials.addData('mouse_2.y', mouse_2.y)
        trials.addData('mouse_2.leftButton', mouse_2.leftButton)
        trials.addData('mouse_2.midButton', mouse_2.midButton)
        trials.addData('mouse_2.rightButton', mouse_2.rightButton)
        trials.addData('mouse_2.time', mouse_2.time)
        trials.addData('mouse_2.clicked_name', mouse_2.clicked_name)
        # the Routine "age_rating" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 1.0 repeats of 'trials'
    
    
    # --- Prepare to start Routine "thanks" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('thanks.started', globalClock.getTime(format='float'))
    thankstxt.reset()
    continue_button_4.reset()
    # setup some python lists for storing info about the end_mouse
    end_mouse.x = []
    end_mouse.y = []
    end_mouse.leftButton = []
    end_mouse.midButton = []
    end_mouse.rightButton = []
    end_mouse.time = []
    end_mouse.clicked_name = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    thanksComponents = [thankstxt, continue_button_4, end_mouse]
    for thisComponent in thanksComponents:
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
    
    # --- Run Routine "thanks" ---
    routineForceEnded = not continueRoutine
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
        
        # *continue_button_4* updates
        
        # if continue_button_4 is starting this frame...
        if continue_button_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            continue_button_4.frameNStart = frameN  # exact frame index
            continue_button_4.tStart = t  # local t and not account for scr refresh
            continue_button_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(continue_button_4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'continue_button_4.started')
            # update status
            continue_button_4.status = STARTED
            continue_button_4.setAutoDraw(True)
        
        # if continue_button_4 is active this frame...
        if continue_button_4.status == STARTED:
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
                    clickableList = environmenttools.getFromNames(continue_button_4, namespace=locals())
                    for obj in clickableList:
                        # is this object clicked on?
                        if obj.contains(end_mouse):
                            gotValidClick = True
                            end_mouse.clicked_name.append(obj.name)
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
        for thisComponent in thanksComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "thanks" ---
    for thisComponent in thanksComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('thanks.stopped', globalClock.getTime(format='float'))
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('end_mouse.x', end_mouse.x)
    thisExp.addData('end_mouse.y', end_mouse.y)
    thisExp.addData('end_mouse.leftButton', end_mouse.leftButton)
    thisExp.addData('end_mouse.midButton', end_mouse.midButton)
    thisExp.addData('end_mouse.rightButton', end_mouse.rightButton)
    thisExp.addData('end_mouse.time', end_mouse.time)
    thisExp.addData('end_mouse.clicked_name', end_mouse.clicked_name)
    thisExp.nextEntry()
    # the Routine "thanks" was not non-slip safe, so reset the non-slip timer
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
