// Source: staircase_demo (demos/staircase_demo)
// Project URL: https://gitlab.pavlovia.org/demos/staircase_demo
// Original file: orientation_staircase.js
﻿/****************************** 
 * Orientation_Staircase Test *
 ******************************/

import { PsychoJS } from './lib/core-2020.2.js';
import * as core from './lib/core-2020.2.js';
import { TrialHandler } from './lib/data-2020.2.js';
import { Scheduler } from './lib/util-2020.2.js';
import * as visual from './lib/visual-2020.2.js';
import * as sound from './lib/sound-2020.2.js';
import * as util from './lib/util-2020.2.js';
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;

// init psychoJS:
const psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: true,
  color: new util.Color([0, 0, 0]),
  units: 'height',
  waitBlanking: true
});

// store info about the experiment session:
let expName = 'orientation_staircase';  // from the Builder filename that created this script
let expInfo = {'participant': '', 'session': '001', 'startOri': ['left', 'right']};

// Start code blocks for 'Before Experiment'
/*
stair params similar to stairhandler class
but simplified for basic online task*/
var currentDirection, maxVal, minVal, nDown, nReversals, nTrials, nUp, reversalVals, startVal, stepSizes, trialCount;
trialCount = 0;
startVal = 70;
nReversals = 5;
stepSizes = [10, 5, 2, 1, 0.5];
nUp = 1;
nDown = 1;
maxVal = 90;
minVal = 0;
nTrials = 100;
currentDirection = "down";
reversalVals = [];

// schedule the experiment:
psychoJS.schedule(psychoJS.gui.DlgFromDict({
  dictionary: expInfo,
  title: expName
}));

const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); }, flowScheduler, dialogCancelScheduler);

// flowScheduler gets run if the participants presses OK
flowScheduler.add(updateInfo); // add timeStamp
flowScheduler.add(experimentInit);
flowScheduler.add(instructionsRoutineBegin());
flowScheduler.add(instructionsRoutineEachFrame());
flowScheduler.add(instructionsRoutineEnd());
const trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trialsLoopBegin, trialsLoopScheduler);
flowScheduler.add(trialsLoopScheduler);
flowScheduler.add(trialsLoopEnd);
flowScheduler.add(endRoutineBegin());
flowScheduler.add(endRoutineEachFrame());
flowScheduler.add(endRoutineEnd());
flowScheduler.add(quitPsychoJS, '', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, '', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    {'name': 'Stimuli/grating_cropped.png', 'path': 'Stimuli/grating_cropped.png'}
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.EXP);


var frameDur;
function updateInfo() {
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2020.2.8';
  expInfo['OS'] = window.navigator.platform;

  // store frame rate of monitor if we can measure it successfully
  expInfo['frameRate'] = psychoJS.window.getActualFrameRate();
  if (typeof expInfo['frameRate'] !== 'undefined')
    frameDur = 1.0 / Math.round(expInfo['frameRate']);
  else
    frameDur = 1.0 / 60.0; // couldn't get a reliable measure so guess

  // add info from the URL:
  util.addInfoFromUrl(expInfo);
  
  return Scheduler.Event.NEXT;
}


var instructionsClock;
var instrTxt;
var start_resp;
var shuffle;
var average;
var trialClock;
var leftGrating;
var rightGrating;
var key_resp;
var incrementText;
var fixation;
var endClock;
var feedbackTxt;
var orientedGrating;
var threshGratingText;
var endButton;
var mouse;
var globalClock;
var routineTimer;
function experimentInit() {
  // Initialize components for Routine "instructions"
  instructionsClock = new util.Clock();
  instrTxt = new visual.TextStim({
    win: psychoJS.window,
    name: 'instrTxt',
    text: 'This is a demo of a basic orientation discrimination staricase. \n\nPress left or right to identify the 0 degree probe\n\npress space to start',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], height: 0.05,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: 0.0 
  });
  
  start_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  Array.prototype.append = [].push;
  shuffle = util.shuffle;
  average = (arr) => (arr.reduce((a, b) => (a + b), 0)) / arr.length
  // Initialize components for Routine "trial"
  trialClock = new util.Clock();
  /* Syntax Error: Fix Python code */
  leftGrating = new visual.ImageStim({
    win : psychoJS.window,
    name : 'leftGrating', units : undefined, 
    image : 'Stimuli/grating_cropped.png', mask : undefined,
    ori : 1.0, pos : [(- 0.3), 0], size : undefined,
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -2.0 
  });
  rightGrating = new visual.ImageStim({
    win : psychoJS.window,
    name : 'rightGrating', units : undefined, 
    image : 'Stimuli/grating_cropped.png', mask : undefined,
    ori : 1.0, pos : [0.3, 0], size : undefined,
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -3.0 
  });
  key_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  incrementText = new visual.TextStim({
    win: psychoJS.window,
    name: 'incrementText',
    text: 'default text',
    font: 'Arial',
    units: undefined, 
    pos: [0, (- 0.4)], height: 0.02,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: -5.0 
  });
  
  fixation = new visual.TextStim({
    win: psychoJS.window,
    name: 'fixation',
    text: '+',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], height: 0.02,  wrapWidth: undefined, ori: 0,
    color: new util.Color('black'),  opacity: 1,
    depth: -6.0 
  });
  
  // Initialize components for Routine "end"
  endClock = new util.Clock();
  feedbackTxt = new visual.TextStim({
    win: psychoJS.window,
    name: 'feedbackTxt',
    text: 'default text',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0.4], height: 0.05,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: -1.0 
  });
  
  orientedGrating = new visual.ImageStim({
    win : psychoJS.window,
    name : 'orientedGrating', units : undefined, 
    image : 'Stimuli/grating_cropped.png', mask : undefined,
    ori : 1.0, pos : [0, 0], size : undefined,
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -2.0 
  });
  threshGratingText = new visual.TextStim({
    win: psychoJS.window,
    name: 'threshGratingText',
    text: 'That looks like this!',
    font: 'Arial',
    units: undefined, 
    pos: [0, (- 0.2)], height: 0.02,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: -3.0 
  });
  
  endButton = new visual.TextStim({
    win: psychoJS.window,
    name: 'endButton',
    text: 'click here to end',
    font: 'Arial',
    units: undefined, 
    pos: [0.4, (- 0.4)], height: 0.05,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: -4.0 
  });
  
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}


var t;
var frameN;
var _start_resp_allKeys;
var instructionsComponents;
function instructionsRoutineBegin(snapshot) {
  return function () {
    //------Prepare to start Routine 'instructions'-------
    t = 0;
    instructionsClock.reset(); // clock
    frameN = -1;
    // update component parameters for each repeat
    start_resp.keys = undefined;
    start_resp.rt = undefined;
    _start_resp_allKeys = [];
    // keep track of which components have finished
    instructionsComponents = [];
    instructionsComponents.push(instrTxt);
    instructionsComponents.push(start_resp);
    
    for (const thisComponent of instructionsComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      return Scheduler.Event.NEXT;
    }
  };
}


var continueRoutine;
function instructionsRoutineEachFrame(snapshot) {
  return function () {
    //------Loop for each frame of Routine 'instructions'-------
    let continueRoutine = true; // until we're told otherwise
    // get current time
    t = instructionsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *instrTxt* updates
    if (t >= 0.0 && instrTxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instrTxt.tStart = t;  // (not accounting for frame time here)
      instrTxt.frameNStart = frameN;  // exact frame index
      
      instrTxt.setAutoDraw(true);
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

    if (start_resp.status === PsychoJS.Status.STARTED) {
      let theseKeys = start_resp.getKeys({keyList: ['space'], waitRelease: false});
      _start_resp_allKeys = _start_resp_allKeys.concat(theseKeys);
      if (_start_resp_allKeys.length > 0) {
        start_resp.keys = _start_resp_allKeys[_start_resp_allKeys.length - 1].name;  // just the last key pressed
        start_resp.rt = _start_resp_allKeys[_start_resp_allKeys.length - 1].rt;
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
  return function () {
    //------Ending Routine 'instructions'-------
    for (const thisComponent of instructionsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('start_resp.keys', start_resp.keys);
    if (typeof start_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('start_resp.rt', start_resp.rt);
        routineTimer.reset();
        }
    
    start_resp.stop();
    // the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    return Scheduler.Event.NEXT;
  };
}


var trials;
var currentLoop;
function trialsLoopBegin(trialsLoopScheduler) {
  // set up handler to look after randomisation of conditions etc
  trials = new TrialHandler({
    psychoJS: psychoJS,
    nReps: 100, method: TrialHandler.Method.RANDOM,
    extraInfo: expInfo, originPath: undefined,
    trialList: undefined,
    seed: undefined, name: 'trials'
  });
  psychoJS.experiment.addLoop(trials); // add the loop to the experiment
  currentLoop = trials;  // we're now the current loop

  // Schedule all the trials in the trialList:
  for (const thisTrial of trials) {
    const snapshot = trials.getSnapshot();
    trialsLoopScheduler.add(importConditions(snapshot));
    trialsLoopScheduler.add(trialRoutineBegin(snapshot));
    trialsLoopScheduler.add(trialRoutineEachFrame(snapshot));
    trialsLoopScheduler.add(trialRoutineEnd(snapshot));
    trialsLoopScheduler.add(endLoopIteration(trialsLoopScheduler, snapshot));
  }

  return Scheduler.Event.NEXT;
}


function trialsLoopEnd() {
  psychoJS.experiment.removeLoop(trials);

  return Scheduler.Event.NEXT;
}


var this_ori;
var thisStep;
var stepSize;
var these_oris;
var corrAns;
var _key_resp_allKeys;
var trialComponents;
function trialRoutineBegin(snapshot) {
  return function () {
    //------Prepare to start Routine 'trial'-------
    t = 0;
    trialClock.reset(); // clock
    frameN = -1;
    // update component parameters for each repeat
    if ((trialCount === 0)) {
        this_ori = startVal;
        thisStep = 0;
    }
    console.log(stepSizes);
    console.log(thisStep);
    console.log(trialCount);
    stepSize = stepSizes[thisStep];
    if ((expInfo["startOri"] === "left")) {
        this_ori = (this_ori * (- 1));
    }
    these_oris = [this_ori, 0];
    shuffle(these_oris);
    if ((these_oris[1] === 0)) {
        corrAns = "right";
    } else {
        if ((these_oris[0] === 0)) {
            corrAns = "left";
        }
    }
    
    leftGrating.setOri(these_oris[0]);
    rightGrating.setOri(these_oris[1]);
    key_resp.keys = undefined;
    key_resp.rt = undefined;
    _key_resp_allKeys = [];
    incrementText.setText(("(for debugging/teaching only) current stepSize is: " + stepSize.toString()));
    // keep track of which components have finished
    trialComponents = [];
    trialComponents.push(leftGrating);
    trialComponents.push(rightGrating);
    trialComponents.push(key_resp);
    trialComponents.push(incrementText);
    trialComponents.push(fixation);
    
    for (const thisComponent of trialComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      return Scheduler.Event.NEXT;
    }
  };
}


var frameRemains;
function trialRoutineEachFrame(snapshot) {
  return function () {
    //------Loop for each frame of Routine 'trial'-------
    let continueRoutine = true; // until we're told otherwise
    // get current time
    t = trialClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *leftGrating* updates
    if (t >= 0.5 && leftGrating.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      leftGrating.tStart = t;  // (not accounting for frame time here)
      leftGrating.frameNStart = frameN;  // exact frame index
      
      leftGrating.setAutoDraw(true);
    }

    frameRemains = 0.5 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
    if ((leftGrating.status === PsychoJS.Status.STARTED || leftGrating.status === PsychoJS.Status.FINISHED) && t >= frameRemains) {
      leftGrating.setAutoDraw(false);
    }
    
    // *rightGrating* updates
    if (t >= 0.5 && rightGrating.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      rightGrating.tStart = t;  // (not accounting for frame time here)
      rightGrating.frameNStart = frameN;  // exact frame index
      
      rightGrating.setAutoDraw(true);
    }

    frameRemains = 0.5 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
    if ((rightGrating.status === PsychoJS.Status.STARTED || rightGrating.status === PsychoJS.Status.FINISHED) && t >= frameRemains) {
      rightGrating.setAutoDraw(false);
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

    if (key_resp.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_resp.getKeys({keyList: ['left', 'right'], waitRelease: false});
      _key_resp_allKeys = _key_resp_allKeys.concat(theseKeys);
      if (_key_resp_allKeys.length > 0) {
        key_resp.keys = _key_resp_allKeys[_key_resp_allKeys.length - 1].name;  // just the last key pressed
        key_resp.rt = _key_resp_allKeys[_key_resp_allKeys.length - 1].rt;
        // was this correct?
        if (key_resp.keys == 'corrAns') {
            key_resp.corr = 1;
        } else {
            key_resp.corr = 0;
        }
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    
    // *incrementText* updates
    if (t >= 0.0 && incrementText.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      incrementText.tStart = t;  // (not accounting for frame time here)
      incrementText.frameNStart = frameN;  // exact frame index
      
      incrementText.setAutoDraw(true);
    }

    
    // *fixation* updates
    if (t >= 0.0 && fixation.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fixation.tStart = t;  // (not accounting for frame time here)
      fixation.frameNStart = frameN;  // exact frame index
      
      fixation.setAutoDraw(true);
    }

    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
    if ((fixation.status === PsychoJS.Status.STARTED || fixation.status === PsychoJS.Status.FINISHED) && t >= frameRemains) {
      fixation.setAutoDraw(false);
    }
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
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
  return function () {
    //------Ending Routine 'trial'-------
    for (const thisComponent of trialComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    console.log("Orientation was: ", this_ori);
    console.log("Correct answer was: ", corrAns);
    console.log("This resp was: ", key_resp.keys);
    trials.addData("this_ori", this_ori);
    trials.addData("Response", key_resp.keys);
    trials.addData("currentDirection", currentDirection);
    trials.addData("corrAns", corrAns);
    trials.addData("currentStepSize", thisStep);
    if ((expInfo["startOri"] === "left")) {
        this_ori = (this_ori * (- 1));
    }
    if ((key_resp.keys === corrAns)) {
        console.log("Answer correct!");
        trials.addData("corr", 1);
        if ((currentDirection === "down")) {
            if ((this_ori > minVal)) {
                this_ori -= stepSize;
            } else {
                console.log("minimal value reached maintaining current val");
            }
        } else {
            currentDirection = "down";
            reversalVals.append(this_ori);
            if ((stepSize !== stepSizes.slice((- 1))[0])) {
                thisStep += 1;
            }
        }
    } else {
        trials.addData("corr", 0);
        if ((currentDirection === "down")) {
            currentDirection = "up";
            reversalVals.append(this_ori);
            if ((stepSize !== stepSizes.slice((- 1))[0])) {
                thisStep += 1;
            }
        }
        if ((this_ori < maxVal)) {
            this_ori += stepSize;
        } else {
            console.log("max value reached. keeping current value");
        }
    }
    if ((reversalVals.length === nReversals)) {
        continueRoutine = false;
        trials.finished = true;
        console.log("nReversals reached, ending staircase");
    }
    trialCount += 1;
    
    // was no response the correct answer?!
    if (key_resp.keys === undefined) {
      if (['None','none',undefined].includes('corrAns')) {
         key_resp.corr = 1;  // correct non-response
      } else {
         key_resp.corr = 0;  // failed to respond (incorrectly)
      }
    }
    // store data for thisExp (ExperimentHandler)
    psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
    psychoJS.experiment.addData('key_resp.corr', key_resp.corr);
    if (typeof key_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
        routineTimer.reset();
        }
    
    key_resp.stop();
    // the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    return Scheduler.Event.NEXT;
  };
}


var avRevs;
var threshold;
var gotValidClick;
var endComponents;
function endRoutineBegin(snapshot) {
  return function () {
    //------Prepare to start Routine 'end'-------
    t = 0;
    endClock.reset(); // clock
    frameN = -1;
    // update component parameters for each repeat
    //can't use np.average in JS so use average
    //(see 'initializeJS' component in first routine)
    avRevs = 3;
    threshold = average(reversalVals.slice((- avRevs)));
    console.log("Threshold was: ", threshold);
    
    feedbackTxt.setText((("Your threshold was " + util.round(threshold, 3).toString()) + " degrees!"));
    orientedGrating.setOri(threshold);
    // setup some python lists for storing info about the mouse
    mouse.clicked_name = [];
    gotValidClick = false; // until a click is received
    // keep track of which components have finished
    endComponents = [];
    endComponents.push(feedbackTxt);
    endComponents.push(orientedGrating);
    endComponents.push(threshGratingText);
    endComponents.push(endButton);
    endComponents.push(mouse);
    
    for (const thisComponent of endComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      return Scheduler.Event.NEXT;
    }
  };
}


var prevButtonState;
var _mouseButtons;
function endRoutineEachFrame(snapshot) {
  return function () {
    //------Loop for each frame of Routine 'end'-------
    let continueRoutine = true; // until we're told otherwise
    // get current time
    t = endClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *feedbackTxt* updates
    if (t >= 0.0 && feedbackTxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      feedbackTxt.tStart = t;  // (not accounting for frame time here)
      feedbackTxt.frameNStart = frameN;  // exact frame index
      
      feedbackTxt.setAutoDraw(true);
    }

    
    // *orientedGrating* updates
    if (t >= 0.0 && orientedGrating.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      orientedGrating.tStart = t;  // (not accounting for frame time here)
      orientedGrating.frameNStart = frameN;  // exact frame index
      
      orientedGrating.setAutoDraw(true);
    }

    
    // *threshGratingText* updates
    if (t >= 0.0 && threshGratingText.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      threshGratingText.tStart = t;  // (not accounting for frame time here)
      threshGratingText.frameNStart = frameN;  // exact frame index
      
      threshGratingText.setAutoDraw(true);
    }

    
    // *endButton* updates
    if (t >= 0.0 && endButton.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      endButton.tStart = t;  // (not accounting for frame time here)
      endButton.frameNStart = frameN;  // exact frame index
      
      endButton.setAutoDraw(true);
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
    if (mouse.status === PsychoJS.Status.STARTED) {  // only update if started and not finished!
      _mouseButtons = mouse.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          for (const obj of [endButton]) {
            if (obj.contains(mouse)) {
              gotValidClick = true;
              mouse.clicked_name.push(obj.name)
            }
          }
          if (gotValidClick === true) { // abort routine on response
            continueRoutine = false;
          }
        }
      }
    }
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of endComponents)
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


var _mouseXYs;
function endRoutineEnd(snapshot) {
  return function () {
    //------Ending Routine 'end'-------
    for (const thisComponent of endComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    // store data for thisExp (ExperimentHandler)
    _mouseXYs = mouse.getPos();
    _mouseButtons = mouse.getPressed();
    psychoJS.experiment.addData('mouse.x', _mouseXYs[0]);
    psychoJS.experiment.addData('mouse.y', _mouseXYs[1]);
    psychoJS.experiment.addData('mouse.leftButton', _mouseButtons[0]);
    psychoJS.experiment.addData('mouse.midButton', _mouseButtons[1]);
    psychoJS.experiment.addData('mouse.rightButton', _mouseButtons[2]);
    if (mouse.clicked_name.length > 0) {
      psychoJS.experiment.addData('mouse.clicked_name', mouse.clicked_name[0]);}
    // the Routine "end" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    return Scheduler.Event.NEXT;
  };
}


function endLoopIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      } else {
        const thisTrial = snapshot.getCurrentTrial();
        if (typeof thisTrial === 'undefined' || !('isTrials' in thisTrial) || thisTrial.isTrials) {
          psychoJS.experiment.nextEntry(snapshot);
        }
      }
    return Scheduler.Event.NEXT;
    }
  };
}


function importConditions(currentLoop) {
  return function () {
    psychoJS.importAttributes(currentLoop.getCurrentTrial());
    return Scheduler.Event.NEXT;
    };
}


function quitPsychoJS(message, isCompleted) {
  // Check for and save orphaned data
  if (psychoJS.experiment.isEntryEmpty()) {
    psychoJS.experiment.nextEntry();
  }
  
  
  
  
  
  
  
  
  psychoJS.window.close();
  psychoJS.quit({message: message, isCompleted: isCompleted});
  
  return Scheduler.Event.QUIT;
}
