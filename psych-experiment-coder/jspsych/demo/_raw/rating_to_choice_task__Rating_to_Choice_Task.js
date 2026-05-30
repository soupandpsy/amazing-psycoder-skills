// Source: rating_to_choice_task (demos/rating_to_choice_task)
// Project URL: https://gitlab.pavlovia.org/demos/rating_to_choice_task
// Original file: Rating_to_Choice_Task.js
﻿/****************************** 
 * Rating_To_Choice_Task *
 ******************************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2025.2.0.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'Rating_to_Choice_Task';  // from the Builder filename that created this script
let expInfo = {
    'participant': `${util.pad(Number.parseFloat(util.randint(0, 999999)).toFixed(0), 6)}`,
    'session': '001',
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
  color: new util.Color([0.9843, 0.9216, 0.8039]),
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
flowScheduler.add(instructRoutineBegin());
flowScheduler.add(instructRoutineEachFrame());
flowScheduler.add(instructRoutineEnd());
const trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trialsLoopBegin(trialsLoopScheduler));
flowScheduler.add(trialsLoopScheduler);
flowScheduler.add(trialsLoopEnd);


flowScheduler.add(instruct2RoutineBegin());
flowScheduler.add(instruct2RoutineEachFrame());
flowScheduler.add(instruct2RoutineEnd());
const choice_trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(choice_trialsLoopBegin(choice_trialsLoopScheduler));
flowScheduler.add(choice_trialsLoopScheduler);
flowScheduler.add(choice_trialsLoopEnd);


flowScheduler.add(byeRoutineBegin());
flowScheduler.add(byeRoutineEachFrame());
flowScheduler.add(byeRoutineEnd());
flowScheduler.add(quitPsychoJS, 'Thank you for your patience.', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, 'Thank you for your patience.', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    // resources:
    {'name': 'conditions.xlsx', 'path': 'conditions.xlsx'},
    {'name': 'images/catherine-kay-greenup-k_gmZfU9bTg-unsplash.jpg', 'path': 'images/catherine-kay-greenup-k_gmZfU9bTg-unsplash.jpg'},
    {'name': 'images/europeana-oFh0eTEupTE-unsplash.jpg', 'path': 'images/europeana-oFh0eTEupTE-unsplash.jpg'},
    {'name': 'images/henrik-donnestad-t2Sai-AqIpI-unsplash.jpg', 'path': 'images/henrik-donnestad-t2Sai-AqIpI-unsplash.jpg'},
    {'name': 'images/laya-clode-hnDQb0pPt9o-unsplash.jpg', 'path': 'images/laya-clode-hnDQb0pPt9o-unsplash.jpg'},
    {'name': 'images/usgs-3F2YdXjJMCI-unsplash.jpg', 'path': 'images/usgs-3F2YdXjJMCI-unsplash.jpg'},
    {'name': 'images/usgs-Yi06GUt3rA4-unsplash.jpg', 'path': 'images/usgs-Yi06GUt3rA4-unsplash.jpg'},
    {'name': 'conditions_choice_phase.xlsx', 'path': 'conditions_choice_phase.xlsx'},
    {'name': 'default.png', 'path': 'https://pavlovia.org/assets/default/default.png'},
    {'name': 'images/catherine-kay-greenup-k_gmZfU9bTg-unsplash.jpg', 'path': 'images/catherine-kay-greenup-k_gmZfU9bTg-unsplash.jpg'},
    {'name': 'images/europeana-oFh0eTEupTE-unsplash.jpg', 'path': 'images/europeana-oFh0eTEupTE-unsplash.jpg'},
    {'name': 'images/europeana-ORNK84pznIs-unsplash.jpg', 'path': 'images/europeana-ORNK84pznIs-unsplash.jpg'},
    {'name': 'images/henrik-donnestad-t2Sai-AqIpI-unsplash.jpg', 'path': 'images/henrik-donnestad-t2Sai-AqIpI-unsplash.jpg'},
    {'name': 'images/laya-clode-hnDQb0pPt9o-unsplash.jpg', 'path': 'images/laya-clode-hnDQb0pPt9o-unsplash.jpg'},
    {'name': 'images/museum-of-new-zealand-te-papa-tongarewa-SJfPfXCIHx0-unsplash.jpg', 'path': 'images/museum-of-new-zealand-te-papa-tongarewa-SJfPfXCIHx0-unsplash.jpg'},
    {'name': 'images/museum-of-new-zealand-te-papa-tongarewa-W_inwSSIqp8-unsplash.jpg', 'path': 'images/museum-of-new-zealand-te-papa-tongarewa-W_inwSSIqp8-unsplash.jpg'},
    {'name': 'images/usgs-3F2YdXjJMCI-unsplash.jpg', 'path': 'images/usgs-3F2YdXjJMCI-unsplash.jpg'},
    {'name': 'images/usgs-Yi06GUt3rA4-unsplash.jpg', 'path': 'images/usgs-Yi06GUt3rA4-unsplash.jpg'},
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.INFO);


var currentLoop;
var frameDur;
async function updateInfo() {
  currentLoop = psychoJS.experiment;  // right now there are no loops
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2025.2.0';
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


var instructClock;
var instruct1;
var start_resp;
var trialClock;
var image;
var text;
var key_resp;
var rated_1;
var rated_2;
var rated_3;
var instruct2Clock;
var instruct1_2;
var start_resp_2;
var chooseClock;
var leftim;
var rightim;
var choose_q;
var key_resp_2;
var byeClock;
var instruct1_3;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "instruct"
  instructClock = new util.Clock();
  instruct1 = new visual.TextBox({
    win: psychoJS.window,
    name: 'instruct1',
    text: 'In this first part of the task, you will see a series of paintings, one at a time.\nYour job is to rate each painting on a scale from 1 to 3:\n\n1 = I don’t like it\n\n2 = It’s okay\n\n3 = I really like it\nPress the corresponding number key on your keyboard for each painting.\nTake your time and respond honestly. There is no right or wrong answer.\n\nPress Space to start',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.8],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: 'white', borderColor: undefined,
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
  
  start_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "trial"
  trialClock = new util.Clock();
  image = new visual.ImageStim({
    win : psychoJS.window,
    name : 'image', units : undefined, 
    image : 'default.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [0.5, 0.5],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  text = new visual.TextStim({
    win: psychoJS.window,
    name: 'text',
    text: 'How much do you like this painting?\nPlease rate 1 - 3 using your keyboard',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0.4], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('black'),  opacity: undefined,
    depth: -1.0 
  });
  
  key_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Run 'Begin Experiment' code from code
  rated_1 = [];
  rated_2 = [];
  rated_3 = [];
  
  // Initialize components for Routine "instruct2"
  instruct2Clock = new util.Clock();
  instruct1_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'instruct1_2',
    text: 'Now you will see pairs of paintings side by side.\nYour task is to choose the painting you prefer from each pair.\n\nPress 1 if you prefer the left painting.\n\nPress 2 if you prefer the right painting.\nTry to choose the painting you like most in each comparison.\nIf a painting is missing, a placeholder image may appear.\nRespond as quickly and accurately as you can.\n\nPress Space to start',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.8],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: 'white', borderColor: undefined,
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
  
  start_resp_2 = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "choose"
  chooseClock = new util.Clock();
  leftim = new visual.ImageStim({
    win : psychoJS.window,
    name : 'leftim', units : undefined, 
    image : 'default.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [(- 0.4), 0], 
    draggable: false,
    size : [0.5, 0.5],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -1.0 
  });
  rightim = new visual.ImageStim({
    win : psychoJS.window,
    name : 'rightim', units : undefined, 
    image : 'default.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0.4, 0], 
    draggable: false,
    size : [0.5, 0.5],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -2.0 
  });
  choose_q = new visual.TextStim({
    win: psychoJS.window,
    name: 'choose_q',
    text: 'Choose 1 or 2 using your keyboard',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0.4], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('black'),  opacity: undefined,
    depth: -3.0 
  });
  
  key_resp_2 = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "bye"
  byeClock = new util.Clock();
  instruct1_3 = new visual.TextBox({
    win: psychoJS.window,
    name: 'instruct1_3',
    text: 'Thanks for taking part!',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.8],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: 'white', borderColor: undefined,
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
var instructMaxDurationReached;
var _start_resp_allKeys;
var instructMaxDuration;
var instructComponents;
function instructRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'instruct' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    instructClock.reset();
    routineTimer.reset();
    instructMaxDurationReached = false;
    // update component parameters for each repeat
    start_resp.keys = undefined;
    start_resp.rt = undefined;
    _start_resp_allKeys = [];
    psychoJS.experiment.addData('instruct.started', globalClock.getTime());
    instructMaxDuration = null
    // keep track of which components have finished
    instructComponents = [];
    instructComponents.push(instruct1);
    instructComponents.push(start_resp);
    
    for (const thisComponent of instructComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function instructRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'instruct' ---
    // get current time
    t = instructClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *instruct1* updates
    if (t >= 0.0 && instruct1.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instruct1.tStart = t;  // (not accounting for frame time here)
      instruct1.frameNStart = frameN;  // exact frame index
      
      instruct1.setAutoDraw(true);
    }
    
    
    // if instruct1 is active this frame...
    if (instruct1.status === PsychoJS.Status.STARTED) {
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
      let theseKeys = start_resp.getKeys({
        keyList: typeof 'space' === 'string' ? ['space'] : 'space', 
        waitRelease: false
      });
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
    for (const thisComponent of instructComponents)
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


function instructRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'instruct' ---
    for (const thisComponent of instructComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('instruct.stopped', globalClock.getTime());
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
    // the Routine "instruct" was not non-slip safe, so reset the non-slip timer
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


var choice_trials;
function choice_trialsLoopBegin(choice_trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    choice_trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 5, method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: 'conditions_choice_phase.xlsx',
      seed: undefined, name: 'choice_trials'
    });
    psychoJS.experiment.addLoop(choice_trials); // add the loop to the experiment
    currentLoop = choice_trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisChoice_trial of choice_trials) {
      snapshot = choice_trials.getSnapshot();
      choice_trialsLoopScheduler.add(importConditions(snapshot));
      choice_trialsLoopScheduler.add(chooseRoutineBegin(snapshot));
      choice_trialsLoopScheduler.add(chooseRoutineEachFrame());
      choice_trialsLoopScheduler.add(chooseRoutineEnd(snapshot));
      choice_trialsLoopScheduler.add(choice_trialsLoopEndIteration(choice_trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}


async function choice_trialsLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(choice_trials);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function choice_trialsLoopEndIteration(scheduler, snapshot) {
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
    image.setImage(this_image);
    key_resp.keys = undefined;
    key_resp.rt = undefined;
    _key_resp_allKeys = [];
    psychoJS.experiment.addData('trial.started', globalClock.getTime());
    trialMaxDuration = null
    // keep track of which components have finished
    trialComponents = [];
    trialComponents.push(image);
    trialComponents.push(text);
    trialComponents.push(key_resp);
    
    for (const thisComponent of trialComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function trialRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'trial' ---
    // get current time
    t = trialClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *image* updates
    if (t >= 0.5 && image.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      image.tStart = t;  // (not accounting for frame time here)
      image.frameNStart = frameN;  // exact frame index
      
      image.setAutoDraw(true);
    }
    
    
    // if image is active this frame...
    if (image.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *text* updates
    if (t >= 0.5 && text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      text.tStart = t;  // (not accounting for frame time here)
      text.frameNStart = frameN;  // exact frame index
      
      text.setAutoDraw(true);
    }
    
    
    // if text is active this frame...
    if (text.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *key_resp* updates
    if (t >= 0.5 && key_resp.status === PsychoJS.Status.NOT_STARTED) {
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
      let theseKeys = key_resp.getKeys({
        keyList: typeof ['1','2','3'] === 'string' ? [['1','2','3']] : ['1','2','3'], 
        waitRelease: false
      });
      _key_resp_allKeys = _key_resp_allKeys.concat(theseKeys);
      if (_key_resp_allKeys.length > 0) {
        key_resp.keys = _key_resp_allKeys[_key_resp_allKeys.length - 1].name;  // just the last key pressed
        key_resp.rt = _key_resp_allKeys[_key_resp_allKeys.length - 1].rt;
        key_resp.duration = _key_resp_allKeys[_key_resp_allKeys.length - 1].duration;
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
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(key_resp.corr, level);
    }
    psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
    if (typeof key_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
        psychoJS.experiment.addData('key_resp.duration', key_resp.duration);
        routineTimer.reset();
        }
    
    key_resp.stop();
    // Run 'End Routine' code from code
    if ((key_resp.keys === "1")) {
        rated_1.push(this_image);
    }
    if ((key_resp.keys === "2")) {
        rated_2.push(this_image);
    }
    if ((key_resp.keys === "3")) {
        rated_3.push(this_image);
    }
    
    // the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var instruct2MaxDurationReached;
var _start_resp_2_allKeys;
var instruct2MaxDuration;
var instruct2Components;
function instruct2RoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'instruct2' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    instruct2Clock.reset();
    routineTimer.reset();
    instruct2MaxDurationReached = false;
    // update component parameters for each repeat
    start_resp_2.keys = undefined;
    start_resp_2.rt = undefined;
    _start_resp_2_allKeys = [];
    psychoJS.experiment.addData('instruct2.started', globalClock.getTime());
    instruct2MaxDuration = null
    // keep track of which components have finished
    instruct2Components = [];
    instruct2Components.push(instruct1_2);
    instruct2Components.push(start_resp_2);
    
    for (const thisComponent of instruct2Components)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function instruct2RoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'instruct2' ---
    // get current time
    t = instruct2Clock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *instruct1_2* updates
    if (t >= 0.0 && instruct1_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instruct1_2.tStart = t;  // (not accounting for frame time here)
      instruct1_2.frameNStart = frameN;  // exact frame index
      
      instruct1_2.setAutoDraw(true);
    }
    
    
    // if instruct1_2 is active this frame...
    if (instruct1_2.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *start_resp_2* updates
    if (t >= 0.0 && start_resp_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      start_resp_2.tStart = t;  // (not accounting for frame time here)
      start_resp_2.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { start_resp_2.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { start_resp_2.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { start_resp_2.clearEvents(); });
    }
    
    // if start_resp_2 is active this frame...
    if (start_resp_2.status === PsychoJS.Status.STARTED) {
      let theseKeys = start_resp_2.getKeys({
        keyList: typeof 'space' === 'string' ? ['space'] : 'space', 
        waitRelease: false
      });
      _start_resp_2_allKeys = _start_resp_2_allKeys.concat(theseKeys);
      if (_start_resp_2_allKeys.length > 0) {
        start_resp_2.keys = _start_resp_2_allKeys[_start_resp_2_allKeys.length - 1].name;  // just the last key pressed
        start_resp_2.rt = _start_resp_2_allKeys[_start_resp_2_allKeys.length - 1].rt;
        start_resp_2.duration = _start_resp_2_allKeys[_start_resp_2_allKeys.length - 1].duration;
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
    for (const thisComponent of instruct2Components)
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


function instruct2RoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'instruct2' ---
    for (const thisComponent of instruct2Components) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('instruct2.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(start_resp_2.corr, level);
    }
    psychoJS.experiment.addData('start_resp_2.keys', start_resp_2.keys);
    if (typeof start_resp_2.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('start_resp_2.rt', start_resp_2.rt);
        psychoJS.experiment.addData('start_resp_2.duration', start_resp_2.duration);
        routineTimer.reset();
        }
    
    start_resp_2.stop();
    // the Routine "instruct2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var chooseMaxDurationReached;
var im1;
var im2;
var _key_resp_2_allKeys;
var chooseMaxDuration;
var chooseComponents;
function chooseRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'choose' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    chooseClock.reset();
    routineTimer.reset();
    chooseMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from pickims
    if ((comparison === "1 vs 2")) {
        if ((rated_1.length > 0)) {
            im1 = rated_1.slice((- 1))[0];
        } else {
            im1 = "images/museum-of-new-zealand-te-papa-tongarewa-SJfPfXCIHx0-unsplash.jpg";
        }
        if ((rated_2.length > 0)) {
            im2 = rated_2.slice((- 1))[0];
        } else {
            im2 = "images/museum-of-new-zealand-te-papa-tongarewa-W_inwSSIqp8-unsplash.jpg";
        }
    } else {
        if ((comparison === "2 vs 3")) {
            if ((rated_2.length > 0)) {
                im1 = rated_2.slice((- 1))[0];
            } else {
                im2 = "images/museum-of-new-zealand-te-papa-tongarewa-W_inwSSIqp8-unsplash.jpg";
            }
            if ((rated_3.length > 0)) {
                im2 = rated_3.slice((- 1))[0];
            } else {
                im2 = "images/europeana-ORNK84pznIs-unsplash.jpg";
            }
        } else {
            if ((comparison === "1 vs 3")) {
                if ((rated_1.length > 0)) {
                    im1 = rated_1.slice((- 1))[0];
                } else {
                    im2 = "images/museum-of-new-zealand-te-papa-tongarewa-SJfPfXCIHx0-unsplash.jpg";
                }
                if ((rated_3.length > 0)) {
                    im2 = rated_3.slice((- 1))[0];
                } else {
                    im2 = "images/europeana-ORNK84pznIs-unsplash.jpg";
                }
            }
        }
    }
    psychoJS.experiment.addData("im1", im1);
    psychoJS.experiment.addData("im2", im2);
    
    leftim.setImage(im1);
    rightim.setImage(im2);
    key_resp_2.keys = undefined;
    key_resp_2.rt = undefined;
    _key_resp_2_allKeys = [];
    psychoJS.experiment.addData('choose.started', globalClock.getTime());
    chooseMaxDuration = null
    // keep track of which components have finished
    chooseComponents = [];
    chooseComponents.push(leftim);
    chooseComponents.push(rightim);
    chooseComponents.push(choose_q);
    chooseComponents.push(key_resp_2);
    
    for (const thisComponent of chooseComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function chooseRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'choose' ---
    // get current time
    t = chooseClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *leftim* updates
    if (t >= 0.5 && leftim.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      leftim.tStart = t;  // (not accounting for frame time here)
      leftim.frameNStart = frameN;  // exact frame index
      
      leftim.setAutoDraw(true);
    }
    
    
    // if leftim is active this frame...
    if (leftim.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *rightim* updates
    if (t >= 0.5 && rightim.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      rightim.tStart = t;  // (not accounting for frame time here)
      rightim.frameNStart = frameN;  // exact frame index
      
      rightim.setAutoDraw(true);
    }
    
    
    // if rightim is active this frame...
    if (rightim.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *choose_q* updates
    if (t >= 0.5 && choose_q.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      choose_q.tStart = t;  // (not accounting for frame time here)
      choose_q.frameNStart = frameN;  // exact frame index
      
      choose_q.setAutoDraw(true);
    }
    
    
    // if choose_q is active this frame...
    if (choose_q.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *key_resp_2* updates
    if (t >= 0.5 && key_resp_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      key_resp_2.tStart = t;  // (not accounting for frame time here)
      key_resp_2.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { key_resp_2.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { key_resp_2.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { key_resp_2.clearEvents(); });
    }
    
    // if key_resp_2 is active this frame...
    if (key_resp_2.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_resp_2.getKeys({
        keyList: typeof ['1','2'] === 'string' ? [['1','2']] : ['1','2'], 
        waitRelease: false
      });
      _key_resp_2_allKeys = _key_resp_2_allKeys.concat(theseKeys);
      if (_key_resp_2_allKeys.length > 0) {
        key_resp_2.keys = _key_resp_2_allKeys[_key_resp_2_allKeys.length - 1].name;  // just the last key pressed
        key_resp_2.rt = _key_resp_2_allKeys[_key_resp_2_allKeys.length - 1].rt;
        key_resp_2.duration = _key_resp_2_allKeys[_key_resp_2_allKeys.length - 1].duration;
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
    for (const thisComponent of chooseComponents)
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


function chooseRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'choose' ---
    for (const thisComponent of chooseComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('choose.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(key_resp_2.corr, level);
    }
    psychoJS.experiment.addData('key_resp_2.keys', key_resp_2.keys);
    if (typeof key_resp_2.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_resp_2.rt', key_resp_2.rt);
        psychoJS.experiment.addData('key_resp_2.duration', key_resp_2.duration);
        routineTimer.reset();
        }
    
    key_resp_2.stop();
    // the Routine "choose" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var byeMaxDurationReached;
var byeMaxDuration;
var byeComponents;
function byeRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'bye' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    byeClock.reset(routineTimer.getTime());
    routineTimer.add(3.000000);
    byeMaxDurationReached = false;
    // update component parameters for each repeat
    psychoJS.experiment.addData('bye.started', globalClock.getTime());
    byeMaxDuration = null
    // keep track of which components have finished
    byeComponents = [];
    byeComponents.push(instruct1_3);
    
    for (const thisComponent of byeComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var frameRemains;
function byeRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'bye' ---
    // get current time
    t = byeClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *instruct1_3* updates
    if (t >= 0.0 && instruct1_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instruct1_3.tStart = t;  // (not accounting for frame time here)
      instruct1_3.frameNStart = frameN;  // exact frame index
      
      instruct1_3.setAutoDraw(true);
    }
    
    
    // if instruct1_3 is active this frame...
    if (instruct1_3.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (instruct1_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      instruct1_3.tStop = t;  // not accounting for scr refresh
      instruct1_3.frameNStop = frameN;  // exact frame index
      // update status
      instruct1_3.status = PsychoJS.Status.FINISHED;
      instruct1_3.setAutoDraw(false);
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
    for (const thisComponent of byeComponents)
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


function byeRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'bye' ---
    for (const thisComponent of byeComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('bye.stopped', globalClock.getTime());
    if (routineForceEnded) {
        routineTimer.reset();} else if (byeMaxDurationReached) {
        byeClock.add(byeMaxDuration);
    } else {
        byeClock.add(3.000000);
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
