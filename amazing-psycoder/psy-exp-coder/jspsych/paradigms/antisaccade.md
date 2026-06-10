# Antisaccade — PsychoJS (Online)

> **Parent**: [psy-exp-coder](../../SKILL.md) · [jsPsych/JavaScript Index](index.md)
> **Config reference**: [antisaccade](../../../psy-exp-designer/paradigms/antisaccade.md)
> **Source**: [Pavlovia demos/antisaccade](https://gitlab.pavlovia.org/demos/antisaccade) · PsychoJS (PsychoPy online export)
> **Platform note**: This is PsychoJS code (PsychoPy's JavaScript runtime for online experiments), NOT jsPsych library code.

## Experiment Logic

The antisaccade task measures executive control by requiring participants to suppress a reflexive saccade toward a peripheral cue and instead look in the opposite direction. The experiment begins with an instruction screen where participants select their response mode (keyboard, mouse click, or hover).

Each trial presents a central fixation cross, followed by a brief peripheral cue flash on one side of the screen. After the cue disappears, a target stimulus appears on the opposite side. Participants must rapidly identify the target (often a letter or arrow) by responding with the correct key. The critical measure is the ability to inhibit the prepotent response of looking toward the cue.

The trial loop is driven by a condition file (`conditions.xlsx`) that specifies cue position, target identity, and correct answer for each trial. Trials are randomly shuffled. The cue-target asynchrony and stimulus durations are precisely controlled using the PsychoJS Scheduler with frame-accurate timing via `psychoJS.window.callOnFlip()`.

Accuracy is determined by comparing the participant's key response to the `corr_ans` column from the condition file. Response time is measured from target onset using a keyboard clock reset on the flip where the target appears. The experiment concludes with a thank-you screen.

## Key Design Patterns

- **Custom `MultiStairHandler`-style loop** with `begin`, `EachFrame`, and `End` routines managed by the PsychoJS `Scheduler` for frame-accurate sequencing
- **Response mode selection** via experiment info dialog (`['keyboard', 'mouse click', 'hover']`), demonstrating multi-modal input
- **`psychoJS.window.callOnFlip()`** for clock reset and event clearing on stimulus onset, ensuring accurate RT measurement
- **Code-driven stimulus positioning**: cue and target positions are set via code components that manipulate `visual.ImageStim.pos` based on trial parameters from the condition file
- **Condition file import** via `psychoJS.importAttributes()` within the trial loop, mapping spreadsheet columns to global variables
- **Pilot mode support** via `util.getUrlParameters().has('__pilotToken')` for testing without data collection

## Code Example

```javascript
// Source: antisaccade (demos/antisaccade)
// Project URL: https://gitlab.pavlovia.org/demos/antisaccade
// Original file: antisaccade.js
﻿/******************** 
 * Antisaccade *
 ********************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2025.1.0.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'antisaccade';  // from the Builder filename that created this script
let expInfo = {
    'participant': `${util.pad(Number.parseFloat(util.randint(0, 999999)).toFixed(0), 6)}`,
    'response mode': ["keyboard", "mouse click", "hover"],
};
let PILOTING = util.getUrlParameters().has('__pilotToken');

// Start code blocks for 'Before Experiment'
// init psychoJS:
const psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: true,
  color: new util.Color([0,0,0]),
  units: 'height',
  waitBlanking: true,
  backgroundImage: '',
  backgroundFit: 'none',
});
// schedule the experiment:
psychoJS.schedule(psychoJS.gui.DlgFromDict({
  dictionary: expInfo,
  title: expName
}));

const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); },flowScheduler, dialogCancelScheduler);

// flowScheduler gets run if the participants presses OK
flowScheduler.add(updateInfo); // add timeStamp
flowScheduler.add(experimentInit);
flowScheduler.add(instructionsRoutineBegin());
flowScheduler.add(instructionsRoutineEachFrame());
flowScheduler.add(instructionsRoutineEnd());
const trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trialsLoopBegin(trialsLoopScheduler));
flowScheduler.add(trialsLoopScheduler);
flowScheduler.add(trialsLoopEnd);



flowScheduler.add(thanksRoutineBegin());
flowScheduler.add(thanksRoutineEachFrame());
flowScheduler.add(thanksRoutineEnd());
flowScheduler.add(quitPsychoJS, 'Thank you for your patience.', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, 'Thank you for your patience.', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    // resources:
    {'name': 'conditions.xlsx', 'path': 'conditions.xlsx'},
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.INFO);


var currentLoop;
var frameDur;
async function updateInfo() {
  currentLoop = psychoJS.experiment;  // right now there are no loops
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2025.1.0';
  expInfo['OS'] = window.navigator.platform;


  // store frame rate of monitor if we can measure it successfully
  expInfo['frameRate'] = psychoJS.window.getActualFrameRate();
  if (typeof expInfo['frameRate'] !== 'undefined')
    frameDur = 1.0 / Math.round(expInfo['frameRate']);
  else
    frameDur = 1.0 / 60.0; // couldn't get a reliable measure so guess

  // add info from the URL:
  util.addInfoFromUrl(expInfo);
  

  
  psychoJS.experiment.dataFileName = (("." + "/") + `data/${expInfo["participant"]}_${expName}_${expInfo["date"]}`);
  psychoJS.experiment.field_separator = '\t';


  return Scheduler.Event.NEXT;
}


var instructionsClock;
var instructions_txt;
var start_resp;
var trialClock;
var target;
var key_resp;
var opposite_location;
var mouse;
var feedbackClock;
var fb_txt;
var thanksClock;
var thanks_text;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "instructions"
  instructionsClock = new util.Clock();
  instructions_txt = new visual.TextBox({
    win: psychoJS.window,
    name: 'instructions_txt',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1.5, 1],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: undefined, borderColor: undefined,
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: false,
    multiline: true,
    anchor: 'center',
    depth: -1.0 
  });
  
  start_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "trial"
  trialClock = new util.Clock();
  target = new visual.Polygon({
    win: psychoJS.window, name: 'target', 
    edges: 100, size:[0.2, 0.2],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: 0, 
    interpolate: true, 
  });
  
  key_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  opposite_location = new visual.Polygon({
    win: psychoJS.window, name: 'opposite_location', 
    edges: 100, size:[0.2, 0.2],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: 0.1, 
    depth: -2, 
    interpolate: true, 
  });
  
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  // Initialize components for Routine "feedback"
  feedbackClock = new util.Clock();
  fb_txt = new visual.TextBox({
    win: psychoJS.window,
    name: 'fb_txt',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.5],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: undefined, borderColor: undefined,
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: false,
    multiline: true,
    anchor: 'center',
    depth: -1.0 
  });
  
  // Initialize components for Routine "thanks"
  thanksClock = new util.Clock();
  thanks_text = new visual.TextBox({
    win: psychoJS.window,
    name: 'thanks_text',
    text: 'Thanks! Goodbye!',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.5],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: undefined, borderColor: undefined,
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: false,
    multiline: true,
    anchor: 'center',
    depth: 0.0 
  });
  
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}


var t;
var frameN;
var continueRoutine;
var routineForceEnded;
var instructionsMaxDurationReached;
var instructions_text;
var _start_resp_allKeys;
var instructionsMaxDuration;
var instructionsComponents;
function instructionsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'instructions' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    instructionsClock.reset();
    routineTimer.reset();
    instructionsMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from set_txt
    if ((expInfo["response mode"] === "keyboard")) {
        instructions_text = "In this task, a cue will appear on either the left or right side of the screen.\n\nIf the cue is red, press the arrow key for the opposite side of the screen.\n\nIf the cue is green, press the arrow key for the same side as the cue.\n\nPress Start when you're ready.";
    } else {
        if ((expInfo["response mode"] === "mouse click")) {
            instructions_text = "In this task, a cue will appear on either the left or right side of the screen.\n\nIf the cue is red, click on the opposite side of the screen from the cue.\n\nIf the cue is green, click on the same side as the cue.\n\nPress Start when you're ready.";
        } else {
            if ((expInfo["response mode"] === "hover")) {
                instructions_text = "In this task, a cue will appear on either the left or right side of the screen.\n\nIf the cue is red, move your mouse toward the opposite side of the screen from the cue.\n\nIf the cue is green, move your mouse toward the same side as the cue.\n\nPress Start when you're ready.";
            }
        }
    }
    
    instructions_txt.setText(instructions_text);
    start_resp.keys = undefined;
    start_resp.rt = undefined;
    _start_resp_allKeys = [];
    psychoJS.experiment.addData('instructions.started', globalClock.getTime());
    instructionsMaxDuration = null
    // keep track of which components have finished
    instructionsComponents = [];
    instructionsComponents.push(instructions_txt);
    instructionsComponents.push(start_resp);
    
    for (const thisComponent of instructionsComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function instructionsRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'instructions' ---
    // get current time
    t = instructionsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *instructions_txt* updates
    if (t >= 0.0 && instructions_txt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instructions_txt.tStart = t;  // (not accounting for frame time here)
      instructions_txt.frameNStart = frameN;  // exact frame index
      
      instructions_txt.setAutoDraw(true);
    }
    
    
    // if instructions_txt is active this frame...
    if (instructions_txt.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *start_resp* updates
    if (t >= 0.0 && start_resp.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      start_resp.tStart = t;  // (not accounting for frame time here)
      start_resp.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { start_resp.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { start_resp.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { start_resp.clearEvents(); });
    }
    
    // if start_resp is active this frame...
    if (start_resp.status === PsychoJS.Status.STARTED) {
      let theseKeys = start_resp.getKeys({keyList: 'space', waitRelease: false});
      _start_resp_allKeys = _start_resp_allKeys.concat(theseKeys);
      if (_start_resp_allKeys.length > 0) {
        start_resp.keys = _start_resp_allKeys[_start_resp_allKeys.length - 1].name;  // just the last key pressed
        start_resp.rt = _start_resp_allKeys[_start_resp_allKeys.length - 1].rt;
        start_resp.duration = _start_resp_allKeys[_start_resp_allKeys.length - 1].duration;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of instructionsComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function instructionsRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'instructions' ---
    for (const thisComponent of instructionsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('instructions.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(start_resp.corr, level);
    }
    psychoJS.experiment.addData('start_resp.keys', start_resp.keys);
    if (typeof start_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('start_resp.rt', start_resp.rt);
        psychoJS.experiment.addData('start_resp.duration', start_resp.duration);
        routineTimer.reset();
        }
    
    start_resp.stop();
    // the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var trials;
function trialsLoopBegin(trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 1, method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: 'conditions.xlsx',
      seed: undefined, name: 'trials'
    });
    psychoJS.experiment.addLoop(trials); // add the loop to the experiment
    currentLoop = trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisTrial of trials) {
      snapshot = trials.getSnapshot();
      trialsLoopScheduler.add(importConditions(snapshot));
      trialsLoopScheduler.add(trialRoutineBegin(snapshot));
      trialsLoopScheduler.add(trialRoutineEachFrame());
      trialsLoopScheduler.add(trialRoutineEnd(snapshot));
      trialsLoopScheduler.add(feedbackRoutineBegin(snapshot));
      trialsLoopScheduler.add(feedbackRoutineEachFrame());
      trialsLoopScheduler.add(feedbackRoutineEnd(snapshot));
      trialsLoopScheduler.add(trialsLoopEndIteration(trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}


async function trialsLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(trials);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function trialsLoopEndIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return async function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      } else {
        psychoJS.experiment.nextEntry(snapshot);
      }
    return Scheduler.Event.NEXT;
    }
  };
}


var trialMaxDurationReached;
var _key_resp_allKeys;
var gotValidClick;
var hover_correct;
var response_time;
var trialMaxDuration;
var trialComponents;
function trialRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'trial' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    trialClock.reset();
    routineTimer.reset();
    trialMaxDurationReached = false;
    // update component parameters for each repeat
    target.setFillColor(new util.Color(target_color));
    target.setPos([target_x, 0]);
    target.setLineColor(new util.Color(target_color));
    key_resp.keys = undefined;
    key_resp.rt = undefined;
    _key_resp_allKeys = [];
    opposite_location.setPos([opposite_location_x, 0]);
    // setup some python lists for storing info about the mouse
    // current position of the mouse:
    mouse.x = [];
    mouse.y = [];
    mouse.leftButton = [];
    mouse.midButton = [];
    mouse.rightButton = [];
    mouse.time = [];
    mouse.corr = [];
    mouse.clicked_name = [];
    gotValidClick = false; // until a click is received
    // Run 'Begin Routine' code from hover_code
    hover_correct = 0;
    response_time = 0;
    
    psychoJS.experiment.addData('trial.started', globalClock.getTime());
    trialMaxDuration = null
    // keep track of which components have finished
    trialComponents = [];
    trialComponents.push(target);
    trialComponents.push(key_resp);
    trialComponents.push(opposite_location);
    trialComponents.push(mouse);
    
    for (const thisComponent of trialComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var prevButtonState;
var _mouseButtons;
var corr;
var corrAns;
var _mouseXYs;
function trialRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'trial' ---
    // get current time
    t = trialClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *target* updates
    if (t >= 0.0 && target.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      target.tStart = t;  // (not accounting for frame time here)
      target.frameNStart = frameN;  // exact frame index
      
      target.setAutoDraw(true);
    }
    
    
    // if target is active this frame...
    if (target.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *key_resp* updates
    if (t >= 0.0 && key_resp.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      key_resp.tStart = t;  // (not accounting for frame time here)
      key_resp.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { key_resp.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { key_resp.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { key_resp.clearEvents(); });
    }
    
    // if key_resp is active this frame...
    if (key_resp.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_resp.getKeys({keyList: ['left','right'], waitRelease: false});
      _key_resp_allKeys = _key_resp_allKeys.concat(theseKeys);
      if (_key_resp_allKeys.length > 0) {
        key_resp.keys = _key_resp_allKeys[_key_resp_allKeys.length - 1].name;  // just the last key pressed
        key_resp.rt = _key_resp_allKeys[_key_resp_allKeys.length - 1].rt;
        key_resp.duration = _key_resp_allKeys[_key_resp_allKeys.length - 1].duration;
        // was this correct?
        if (key_resp.keys == answer) {
            key_resp.corr = 1;
        } else {
            key_resp.corr = 0;
        }
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    
    // *opposite_location* updates
    if (t >= 0.0 && opposite_location.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      opposite_location.tStart = t;  // (not accounting for frame time here)
      opposite_location.frameNStart = frameN;  // exact frame index
      
      opposite_location.setAutoDraw(true);
    }
    
    
    // if opposite_location is active this frame...
    if (opposite_location.status === PsychoJS.Status.STARTED) {
    }
    
    // *mouse* updates
    if (t >= 0.0 && mouse.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      mouse.tStart = t;  // (not accounting for frame time here)
      mouse.frameNStart = frameN;  // exact frame index
      
      mouse.status = PsychoJS.Status.STARTED;
      mouse.mouseClock.reset();
      prevButtonState = mouse.getPressed();  // if button is down already this ISN'T a new click
    }
    
    // if mouse is active this frame...
    if (mouse.status === PsychoJS.Status.STARTED) {
      _mouseButtons = mouse.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          mouse.clickableObjects = eval([target, opposite_location])
          ;// make sure the mouse's clickable objects are an array
          if (!Array.isArray(mouse.clickableObjects)) {
              mouse.clickableObjects = [mouse.clickableObjects];
          }
          // iterate through clickable objects and check each
          for (const obj of mouse.clickableObjects) {
              if (obj.contains(mouse)) {
                  gotValidClick = true;
                  mouse.clicked_name.push(obj.name);
              }
          }
          if (!gotValidClick) {
              mouse.clicked_name.push(null);
          }
          // check whether click was in correct object
          if (gotValidClick) {
              corr = 0;
              corrAns = eval( answer_mouse);
              for (let obj of [corrAns]) {
                  if (obj.contains(mouse)) {
                      corr = 1;
                  };
              };
              mouse.corr.push(corr);
          };
          _mouseXYs = mouse.getPos();
          mouse.x.push(_mouseXYs[0]);
          mouse.y.push(_mouseXYs[1]);
          mouse.leftButton.push(_mouseButtons[0]);
          mouse.midButton.push(_mouseButtons[1]);
          mouse.rightButton.push(_mouseButtons[2]);
          mouse.time.push(mouse.mouseClock.getTime());
          if (gotValidClick === true) { // end routine on response
            continueRoutine = false;
          }
        }
      }
    }
    // Run 'Each Frame' code from hover_code
    if (target.contains(mouse)) {
        continueRoutine = false;
        response_time = t;
        if ((answer_mouse === "target")) {
            hover_correct = 1;
        }
    }
    if (opposite_location.contains(mouse)) {
        continueRoutine = false;
        response_time = t;
        if ((answer_mouse === "opposite_location")) {
            hover_correct = 1;
        }
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of trialComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function trialRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'trial' ---
    for (const thisComponent of trialComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('trial.stopped', globalClock.getTime());
    // was no response the correct answer?!
    if (key_resp.keys === undefined) {
      if (['None','none',undefined].includes(answer)) {
         key_resp.corr = 1;  // correct non-response
      } else {
         key_resp.corr = 0;  // failed to respond (incorrectly)
      }
    }
    // store data for current loop
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(key_resp.corr, level);
    }
    psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
    psychoJS.experiment.addData('key_resp.corr', key_resp.corr);
    if (typeof key_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
        psychoJS.experiment.addData('key_resp.duration', key_resp.duration);
        routineTimer.reset();
        }
    
    key_resp.stop();
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse.x', mouse.x);
    psychoJS.experiment.addData('mouse.y', mouse.y);
    psychoJS.experiment.addData('mouse.leftButton', mouse.leftButton);
    psychoJS.experiment.addData('mouse.midButton', mouse.midButton);
    psychoJS.experiment.addData('mouse.rightButton', mouse.rightButton);
    psychoJS.experiment.addData('mouse.time', mouse.time);
    psychoJS.experiment.addData('mouse.corr', mouse.corr);
    psychoJS.experiment.addData('mouse.clicked_name', mouse.clicked_name);
    
    // the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var feedbackMaxDurationReached;
var correct;
var fb;
var feedbackMaxDuration;
var feedbackComponents;
function feedbackRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'feedback' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    feedbackClock.reset(routineTimer.getTime());
    routineTimer.add(1.000000);
    feedbackMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from code
    correct = 0;
    if ((expInfo["response mode"] === "mouse click")) {
        response_time = mouse.time[0];
        if (mouse.corr[0]) {
            correct = 1;
        }
    }
    if ((expInfo["response mode"] === "keyboard")) {
        response_time = key_resp.rt;
        if (key_resp.corr) {
            correct = 1;
        }
    }
    if ((expInfo["response mode"] === "hover")) {
        if (hover_correct) {
            correct = 1;
        }
    }
    psychoJS.experiment.addData("correct", correct);
    psychoJS.experiment.addData("response_time", response_time);
    if (correct) {
        fb = "Correct!";
    } else {
        fb = "Incorrect";
    }
    
    fb_txt.setText(fb);
    psychoJS.experiment.addData('feedback.started', globalClock.getTime());
    feedbackMaxDuration = null
    // keep track of which components have finished
    feedbackComponents = [];
    feedbackComponents.push(fb_txt);
    
    for (const thisComponent of feedbackComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var frameRemains;
function feedbackRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'feedback' ---
    // get current time
    t = feedbackClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *fb_txt* updates
    if (t >= 0.0 && fb_txt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fb_txt.tStart = t;  // (not accounting for frame time here)
      fb_txt.frameNStart = frameN;  // exact frame index
      
      fb_txt.setAutoDraw(true);
    }
    
    
    // if fb_txt is active this frame...
    if (fb_txt.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 1.0 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (fb_txt.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      fb_txt.tStop = t;  // not accounting for scr refresh
      fb_txt.frameNStop = frameN;  // exact frame index
      // update status
      fb_txt.status = PsychoJS.Status.FINISHED;
      fb_txt.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of feedbackComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine && routineTimer.getTime() > 0) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function feedbackRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'feedback' ---
    for (const thisComponent of feedbackComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('feedback.stopped', globalClock.getTime());
    if (routineForceEnded) {
        routineTimer.reset();} else if (feedbackMaxDurationReached) {
        feedbackClock.add(feedbackMaxDuration);
    } else {
        feedbackClock.add(1.000000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var thanksMaxDurationReached;
var thanksMaxDuration;
var thanksComponents;
function thanksRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'thanks' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    thanksClock.reset(routineTimer.getTime());
    routineTimer.add(1.000000);
    thanksMaxDurationReached = false;
    // update component parameters for each repeat
    psychoJS.experiment.addData('thanks.started', globalClock.getTime());
    thanksMaxDuration = null
    // keep track of which components have finished
    thanksComponents = [];
    thanksComponents.push(thanks_text);
    
    for (const thisComponent of thanksComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function thanksRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'thanks' ---
    // get current time
    t = thanksClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *thanks_text* updates
    if (t >= 0.0 && thanks_text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      thanks_text.tStart = t;  // (not accounting for frame time here)
      thanks_text.frameNStart = frameN;  // exact frame index
      
      thanks_text.setAutoDraw(true);
    }
    
    
    // if thanks_text is active this frame...
    if (thanks_text.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 1.0 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (thanks_text.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      thanks_text.tStop = t;  // not accounting for scr refresh
      thanks_text.frameNStop = frameN;  // exact frame index
      // update status
      thanks_text.status = PsychoJS.Status.FINISHED;
      thanks_text.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of thanksComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine && routineTimer.getTime() > 0) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function thanksRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'thanks' ---
    for (const thisComponent of thanksComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('thanks.stopped', globalClock.getTime());
    if (routineForceEnded) {
        routineTimer.reset();} else if (thanksMaxDurationReached) {
        thanksClock.add(thanksMaxDuration);
    } else {
        thanksClock.add(1.000000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


function importConditions(currentLoop) {
  return async function () {
    psychoJS.importAttributes(currentLoop.getCurrentTrial());
    return Scheduler.Event.NEXT;
    };
}


async function quitPsychoJS(message, isCompleted) {
  // Check for and save orphaned data
  if (psychoJS.experiment.isEntryEmpty()) {
    psychoJS.experiment.nextEntry();
  }
  psychoJS.window.close();
  psychoJS.quit({message: message, isCompleted: isCompleted});
  
  return Scheduler.Event.QUIT;
}

```
