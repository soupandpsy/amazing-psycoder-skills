// Source: butterfly_simon (demos/butterfly_simon)
// Project URL: https://gitlab.pavlovia.org/demos/butterfly_simon
// Original file: Simon.js
﻿/************** 
 * Simon *
 **************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2024.2.4.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'Simon';  // from the Builder filename that created this script
let expInfo = {
    'participant': `${util.pad(Number.parseFloat(util.randint(0, 999999)).toFixed(0), 6)}`,
    'session': '001',
};

// Start code blocks for 'Before Experiment'
// init psychoJS:
const psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: false,
  color: new util.Color([0.3569, 0.6941, 0.8039]),
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
const prac_trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(prac_trialsLoopBegin(prac_trialsLoopScheduler));
flowScheduler.add(prac_trialsLoopScheduler);
flowScheduler.add(prac_trialsLoopEnd);





flowScheduler.add(instructions_2RoutineBegin());
flowScheduler.add(instructions_2RoutineEachFrame());
flowScheduler.add(instructions_2RoutineEnd());
const trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trialsLoopBegin(trialsLoopScheduler));
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
    // resources:
    {'name': 'practice_conditions.xlsx', 'path': 'practice_conditions.xlsx'},
    {'name': 'images/purple_butterfly.png', 'path': 'images/purple_butterfly.png'},
    {'name': 'images/white_butterfly.png', 'path': 'images/white_butterfly.png'},
    {'name': 'images/yellow_butterfly.png', 'path': 'images/yellow_butterfly.png'},
    {'name': 'conditions.xlsx', 'path': 'conditions.xlsx'},
    {'name': 'images/purple_butterfly.png', 'path': 'images/purple_butterfly.png'},
    {'name': 'images/white_butterfly.png', 'path': 'images/white_butterfly.png'},
    {'name': 'images/yellow_butterfly.png', 'path': 'images/yellow_butterfly.png'},
    {'name': 'images/background-1877877_1280.jpg', 'path': 'images/background-1877877_1280.jpg'},
    {'name': 'default.png', 'path': 'https://pavlovia.org/assets/default/default.png'},
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.WARNING);


var currentLoop;
var frameDur;
async function updateInfo() {
  currentLoop = psychoJS.experiment;  // right now there are no loops
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2024.2.4';
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
var background;
var instr_textbox;
var start_button;
var practice_trialClock;
var background_2;
var practxt;
var left_image_2;
var right_image_2;
var mouse_2;
var feedbackClock;
var background_6;
var background_3;
var fb_txt;
var instructions_2Clock;
var background_4;
var instr_textbox_2;
var start_button_2;
var trialClock;
var background_5;
var left_image;
var right_image;
var mouse;
var endClock;
var background_7;
var instr_textbox_3;
var start_button_3;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "instructions"
  instructionsClock = new util.Clock();
  background = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background', units : 'norm', 
    image : 'images/background-1877877_1280.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [2, 2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  instr_textbox = new visual.TextBox({
    win: psychoJS.window,
    name: 'instr_textbox',
    text: "Welcome!\n\nIn this game you will see two butterflies.\n\nWhen you see a PURPLE butterfly, select the left butterfly. \n\nWhen you see a YELLOW butterfly, select the right butterfly.\n\nIt doesn't matter where the butterflies are located, the colors indicate which side to select. \n",
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.8],  units: undefined, 
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
  
  start_button = new visual.ButtonStim({
    win: psychoJS.window,
    name: 'start_button',
    text: 'NEXT',
    fillColor: 'darkgrey',
    borderColor: null,
    color: 'white',
    colorSpace: 'rgb',
    pos: [0, (- 0.4)],
    letterHeight: 0.05,
    size: [0.3, 0.1],
    ori: 0.0
    ,
    depth: -2
  });
  start_button.clock = new util.Clock();
  
  // Initialize components for Routine "practice_trial"
  practice_trialClock = new util.Clock();
  background_2 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background_2', units : 'norm', 
    image : 'images/background-1877877_1280.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [2, 2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  practxt = new visual.TextBox({
    win: psychoJS.window,
    name: 'practxt',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0.4], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1.5, 0.1],  units: undefined, 
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
  
  left_image_2 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'left_image_2', units : undefined, 
    image : 'default.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [(- 0.2), 0], 
    draggable: false,
    size : [0.3, 0.3],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -2.0 
  });
  right_image_2 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'right_image_2', units : undefined, 
    image : 'default.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0.2, 0], 
    draggable: false,
    size : [0.3, 0.3],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -3.0 
  });
  mouse_2 = new core.Mouse({
    win: psychoJS.window,
  });
  mouse_2.mouseClock = new util.Clock();
  // Initialize components for Routine "feedback"
  feedbackClock = new util.Clock();
  background_6 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background_6', units : 'norm', 
    image : 'images/background-1877877_1280.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [2, 2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  background_3 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background_3', units : 'norm', 
    image : 'images/background-1877877_1280.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [2, 2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -1.0 
  });
  fb_txt = new visual.TextStim({
    win: psychoJS.window,
    name: 'fb_txt',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('black'),  opacity: undefined,
    depth: -3.0 
  });
  
  // Initialize components for Routine "instructions_2"
  instructions_2Clock = new util.Clock();
  background_4 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background_4', units : 'norm', 
    image : 'images/background-1877877_1280.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [2, 2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  instr_textbox_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'instr_textbox_2',
    text: "OK let's start the real thing!\n",
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.8],  units: undefined, 
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
  
  start_button_2 = new visual.ButtonStim({
    win: psychoJS.window,
    name: 'start_button_2',
    text: 'START',
    fillColor: 'darkgrey',
    borderColor: null,
    color: 'white',
    colorSpace: 'rgb',
    pos: [0, (- 0.4)],
    letterHeight: 0.05,
    size: [0.3, 0.1],
    ori: 0.0
    ,
    depth: -2
  });
  start_button_2.clock = new util.Clock();
  
  // Initialize components for Routine "trial"
  trialClock = new util.Clock();
  background_5 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background_5', units : 'norm', 
    image : 'images/background-1877877_1280.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [2, 2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  left_image = new visual.ImageStim({
    win : psychoJS.window,
    name : 'left_image', units : undefined, 
    image : 'default.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [(- 0.2), 0], 
    draggable: false,
    size : [0.3, 0.3],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -1.0 
  });
  right_image = new visual.ImageStim({
    win : psychoJS.window,
    name : 'right_image', units : undefined, 
    image : 'default.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0.2, 0], 
    draggable: false,
    size : [0.3, 0.3],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -2.0 
  });
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  // Initialize components for Routine "end"
  endClock = new util.Clock();
  background_7 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background_7', units : 'norm', 
    image : 'images/background-1877877_1280.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [2, 2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  instr_textbox_3 = new visual.TextBox({
    win: psychoJS.window,
    name: 'instr_textbox_3',
    text: 'That is the end! ',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.8],  units: undefined, 
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
  
  start_button_3 = new visual.ButtonStim({
    win: psychoJS.window,
    name: 'start_button_3',
    text: 'EXIT',
    fillColor: 'darkgrey',
    borderColor: null,
    color: 'white',
    colorSpace: 'rgb',
    pos: [0, (- 0.4)],
    letterHeight: 0.05,
    size: [0.3, 0.1],
    ori: 0.0
    ,
    depth: -2
  });
  start_button_3.clock = new util.Clock();
  
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}


var t;
var frameN;
var continueRoutine;
var instructionsMaxDurationReached;
var instructionsMaxDuration;
var instructionsComponents;
function instructionsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'instructions' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    instructionsClock.reset();
    routineTimer.reset();
    instructionsMaxDurationReached = false;
    // update component parameters for each repeat
    // reset start_button to account for continued clicks & clear times on/off
    start_button.reset()
    psychoJS.experiment.addData('instructions.started', globalClock.getTime());
    instructionsMaxDuration = null
    // keep track of which components have finished
    instructionsComponents = [];
    instructionsComponents.push(background);
    instructionsComponents.push(instr_textbox);
    instructionsComponents.push(start_button);
    
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
    
    // *background* updates
    if (t >= 0.0 && background.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background.tStart = t;  // (not accounting for frame time here)
      background.frameNStart = frameN;  // exact frame index
      
      background.setAutoDraw(true);
    }
    
    
    // *instr_textbox* updates
    if (t >= 0.0 && instr_textbox.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instr_textbox.tStart = t;  // (not accounting for frame time here)
      instr_textbox.frameNStart = frameN;  // exact frame index
      
      instr_textbox.setAutoDraw(true);
    }
    
    
    // *start_button* updates
    if (t >= 0 && start_button.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      start_button.tStart = t;  // (not accounting for frame time here)
      start_button.frameNStart = frameN;  // exact frame index
      
      start_button.setAutoDraw(true);
    }
    
    if (start_button.status === PsychoJS.Status.STARTED) {
      // check whether start_button has been pressed
      if (start_button.isClicked) {
        if (!start_button.wasClicked) {
          // store time of first click
          start_button.timesOn.push(start_button.clock.getTime());
          // store time clicked until
          start_button.timesOff.push(start_button.clock.getTime());
        } else {
          // update time clicked until;
          start_button.timesOff[start_button.timesOff.length - 1] = start_button.clock.getTime();
        }
        if (!start_button.wasClicked) {
          // end routine when start_button is clicked
          continueRoutine = false;
          
        }
        // if start_button is still clicked next frame, it is not a new click
        start_button.wasClicked = true;
      } else {
        // if start_button is clicked next frame, it is a new click
        start_button.wasClicked = false;
      }
    } else {
      // keep clock at 0 if start_button hasn't started / has finished
      start_button.clock.reset();
      // if start_button is clicked next frame, it is a new click
      start_button.wasClicked = false;
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
  return async function () {
    //--- Ending Routine 'instructions' ---
    for (const thisComponent of instructionsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('instructions.stopped', globalClock.getTime());
    psychoJS.experiment.addData('start_button.numClicks', start_button.numClicks);
    psychoJS.experiment.addData('start_button.timesOn', start_button.timesOn);
    psychoJS.experiment.addData('start_button.timesOff', start_button.timesOff);
    // the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var prac_trials;
function prac_trialsLoopBegin(prac_trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    prac_trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 1, method: TrialHandler.Method.SEQUENTIAL,
      extraInfo: expInfo, originPath: undefined,
      trialList: 'practice_conditions.xlsx',
      seed: undefined, name: 'prac_trials'
    });
    psychoJS.experiment.addLoop(prac_trials); // add the loop to the experiment
    currentLoop = prac_trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisPrac_trial of prac_trials) {
      snapshot = prac_trials.getSnapshot();
      prac_trialsLoopScheduler.add(importConditions(snapshot));
      const loop_until_correctLoopScheduler = new Scheduler(psychoJS);
      prac_trialsLoopScheduler.add(loop_until_correctLoopBegin(loop_until_correctLoopScheduler, snapshot));
      prac_trialsLoopScheduler.add(loop_until_correctLoopScheduler);
      prac_trialsLoopScheduler.add(loop_until_correctLoopEnd);
      prac_trialsLoopScheduler.add(prac_trialsLoopEndIteration(prac_trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}


var loop_until_correct;
function loop_until_correctLoopBegin(loop_until_correctLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    loop_until_correct = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 10, method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: undefined,
      seed: undefined, name: 'loop_until_correct'
    });
    psychoJS.experiment.addLoop(loop_until_correct); // add the loop to the experiment
    currentLoop = loop_until_correct;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisLoop_until_correct of loop_until_correct) {
      snapshot = loop_until_correct.getSnapshot();
      loop_until_correctLoopScheduler.add(importConditions(snapshot));
      loop_until_correctLoopScheduler.add(practice_trialRoutineBegin(snapshot));
      loop_until_correctLoopScheduler.add(practice_trialRoutineEachFrame());
      loop_until_correctLoopScheduler.add(practice_trialRoutineEnd(snapshot));
      loop_until_correctLoopScheduler.add(feedbackRoutineBegin(snapshot));
      loop_until_correctLoopScheduler.add(feedbackRoutineEachFrame());
      loop_until_correctLoopScheduler.add(feedbackRoutineEnd(snapshot));
      loop_until_correctLoopScheduler.add(loop_until_correctLoopEndIteration(loop_until_correctLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}


async function loop_until_correctLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(loop_until_correct);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function loop_until_correctLoopEndIteration(scheduler, snapshot) {
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


async function prac_trialsLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(prac_trials);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function prac_trialsLoopEndIteration(scheduler, snapshot) {
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


var trials;
function trialsLoopBegin(trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 5, method: TrialHandler.Method.RANDOM,
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


var practice_trialMaxDurationReached;
var gotValidClick;
var practice_trialMaxDuration;
var practice_trialComponents;
function practice_trialRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'practice_trial' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    practice_trialClock.reset();
    routineTimer.reset();
    practice_trialMaxDurationReached = false;
    // update component parameters for each repeat
    practxt.setText(top_txt);
    left_image_2.setImage(left_color);
    right_image_2.setImage(right_color);
    // setup some python lists for storing info about the mouse_2
    // current position of the mouse:
    mouse_2.x = [];
    mouse_2.y = [];
    mouse_2.leftButton = [];
    mouse_2.midButton = [];
    mouse_2.rightButton = [];
    mouse_2.time = [];
    mouse_2.clicked_name = [];
    gotValidClick = false; // until a click is received
    psychoJS.experiment.addData('practice_trial.started', globalClock.getTime());
    practice_trialMaxDuration = null
    // keep track of which components have finished
    practice_trialComponents = [];
    practice_trialComponents.push(background_2);
    practice_trialComponents.push(practxt);
    practice_trialComponents.push(left_image_2);
    practice_trialComponents.push(right_image_2);
    practice_trialComponents.push(mouse_2);
    
    for (const thisComponent of practice_trialComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var prevButtonState;
var _mouseButtons;
var _mouseXYs;
function practice_trialRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'practice_trial' ---
    // get current time
    t = practice_trialClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background_2* updates
    if (t >= 0.0 && background_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background_2.tStart = t;  // (not accounting for frame time here)
      background_2.frameNStart = frameN;  // exact frame index
      
      background_2.setAutoDraw(true);
    }
    
    
    // *practxt* updates
    if (t >= 0.0 && practxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      practxt.tStart = t;  // (not accounting for frame time here)
      practxt.frameNStart = frameN;  // exact frame index
      
      practxt.setAutoDraw(true);
    }
    
    
    // *left_image_2* updates
    if (t >= 0.0 && left_image_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      left_image_2.tStart = t;  // (not accounting for frame time here)
      left_image_2.frameNStart = frameN;  // exact frame index
      
      left_image_2.setAutoDraw(true);
    }
    
    
    // *right_image_2* updates
    if (t >= 0.0 && right_image_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      right_image_2.tStart = t;  // (not accounting for frame time here)
      right_image_2.frameNStart = frameN;  // exact frame index
      
      right_image_2.setAutoDraw(true);
    }
    
    // *mouse_2* updates
    if (t >= 0.0 && mouse_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      mouse_2.tStart = t;  // (not accounting for frame time here)
      mouse_2.frameNStart = frameN;  // exact frame index
      
      mouse_2.status = PsychoJS.Status.STARTED;
      mouse_2.mouseClock.reset();
      prevButtonState = mouse_2.getPressed();  // if button is down already this ISN'T a new click
      }
    if (mouse_2.status === PsychoJS.Status.STARTED) {  // only update if started and not finished!
      _mouseButtons = mouse_2.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          mouse_2.clickableObjects = eval([left_image_2, right_image_2])
          ;// make sure the mouse's clickable objects are an array
          if (!Array.isArray(mouse_2.clickableObjects)) {
              mouse_2.clickableObjects = [mouse_2.clickableObjects];
          }
          // iterate through clickable objects and check each
          for (const obj of mouse_2.clickableObjects) {
              if (obj.contains(mouse_2)) {
                  gotValidClick = true;
                  mouse_2.clicked_name.push(obj.name);
              }
          }
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          mouse_2.clickableObjects = eval([left_image_2, right_image_2])
          ;// make sure the mouse's clickable objects are an array
          if (!Array.isArray(mouse_2.clickableObjects)) {
              mouse_2.clickableObjects = [mouse_2.clickableObjects];
          }
          // iterate through clickable objects and check each
          for (const obj of mouse_2.clickableObjects) {
              if (obj.contains(mouse_2)) {
                  gotValidClick = true;
                  mouse_2.clicked_name.push(obj.name);
              }
          }
          if (gotValidClick === true) { 
            _mouseXYs = mouse_2.getPos();
            mouse_2.x.push(_mouseXYs[0]);
            mouse_2.y.push(_mouseXYs[1]);
            mouse_2.leftButton.push(_mouseButtons[0]);
            mouse_2.midButton.push(_mouseButtons[1]);
            mouse_2.rightButton.push(_mouseButtons[2]);
            mouse_2.time.push(mouse_2.mouseClock.getTime());
          }
          if (gotValidClick === true) { // end routine on response
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
    for (const thisComponent of practice_trialComponents)
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


var correct;
function practice_trialRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'practice_trial' ---
    for (const thisComponent of practice_trialComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('practice_trial.stopped', globalClock.getTime());
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse_2.x', mouse_2.x);
    psychoJS.experiment.addData('mouse_2.y', mouse_2.y);
    psychoJS.experiment.addData('mouse_2.leftButton', mouse_2.leftButton);
    psychoJS.experiment.addData('mouse_2.midButton', mouse_2.midButton);
    psychoJS.experiment.addData('mouse_2.rightButton', mouse_2.rightButton);
    psychoJS.experiment.addData('mouse_2.time', mouse_2.time);
    psychoJS.experiment.addData('mouse_2.clicked_name', mouse_2.clicked_name);
    
    // Run 'End Routine' code from check_correct1
    console.log(mouse_2.clicked_name.slice((- 1))[0]);
    if ((mouse_2.clicked_name.slice((- 1))[0] === correct_response)) {
        correct = 1;
        loop_until_correct.finished = true;
    } else {
        correct = 0;
    }
    psychoJS.experiment.addData("correct", correct);
    
    // the Routine "practice_trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var feedbackMaxDurationReached;
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
    feedbackClock.reset(routineTimer.getTime());
    routineTimer.add(0.500000);
    feedbackMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from code_2
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
    feedbackComponents.push(background_6);
    feedbackComponents.push(background_3);
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
    
    // *background_6* updates
    if (t >= 0.0 && background_6.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background_6.tStart = t;  // (not accounting for frame time here)
      background_6.frameNStart = frameN;  // exact frame index
      
      background_6.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (background_6.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      background_6.setAutoDraw(false);
    }
    
    
    // *background_3* updates
    if (t >= 0.0 && background_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background_3.tStart = t;  // (not accounting for frame time here)
      background_3.frameNStart = frameN;  // exact frame index
      
      background_3.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (background_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      background_3.setAutoDraw(false);
    }
    
    
    // *fb_txt* updates
    if (t >= 0.0 && fb_txt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fb_txt.tStart = t;  // (not accounting for frame time here)
      fb_txt.frameNStart = frameN;  // exact frame index
      
      fb_txt.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (fb_txt.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      fb_txt.setAutoDraw(false);
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
    if (feedbackMaxDurationReached) {
        feedbackClock.add(feedbackMaxDuration);
    } else {
        feedbackClock.add(0.500000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var instructions_2MaxDurationReached;
var instructions_2MaxDuration;
var instructions_2Components;
function instructions_2RoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'instructions_2' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    instructions_2Clock.reset();
    routineTimer.reset();
    instructions_2MaxDurationReached = false;
    // update component parameters for each repeat
    // reset start_button_2 to account for continued clicks & clear times on/off
    start_button_2.reset()
    psychoJS.experiment.addData('instructions_2.started', globalClock.getTime());
    instructions_2MaxDuration = null
    // keep track of which components have finished
    instructions_2Components = [];
    instructions_2Components.push(background_4);
    instructions_2Components.push(instr_textbox_2);
    instructions_2Components.push(start_button_2);
    
    for (const thisComponent of instructions_2Components)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function instructions_2RoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'instructions_2' ---
    // get current time
    t = instructions_2Clock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background_4* updates
    if (t >= 0.0 && background_4.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background_4.tStart = t;  // (not accounting for frame time here)
      background_4.frameNStart = frameN;  // exact frame index
      
      background_4.setAutoDraw(true);
    }
    
    
    // *instr_textbox_2* updates
    if (t >= 0.0 && instr_textbox_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instr_textbox_2.tStart = t;  // (not accounting for frame time here)
      instr_textbox_2.frameNStart = frameN;  // exact frame index
      
      instr_textbox_2.setAutoDraw(true);
    }
    
    
    // *start_button_2* updates
    if (t >= 0 && start_button_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      start_button_2.tStart = t;  // (not accounting for frame time here)
      start_button_2.frameNStart = frameN;  // exact frame index
      
      start_button_2.setAutoDraw(true);
    }
    
    if (start_button_2.status === PsychoJS.Status.STARTED) {
      // check whether start_button_2 has been pressed
      if (start_button_2.isClicked) {
        if (!start_button_2.wasClicked) {
          // store time of first click
          start_button_2.timesOn.push(start_button_2.clock.getTime());
          // store time clicked until
          start_button_2.timesOff.push(start_button_2.clock.getTime());
        } else {
          // update time clicked until;
          start_button_2.timesOff[start_button_2.timesOff.length - 1] = start_button_2.clock.getTime();
        }
        if (!start_button_2.wasClicked) {
          // end routine when start_button_2 is clicked
          continueRoutine = false;
          
        }
        // if start_button_2 is still clicked next frame, it is not a new click
        start_button_2.wasClicked = true;
      } else {
        // if start_button_2 is clicked next frame, it is a new click
        start_button_2.wasClicked = false;
      }
    } else {
      // keep clock at 0 if start_button_2 hasn't started / has finished
      start_button_2.clock.reset();
      // if start_button_2 is clicked next frame, it is a new click
      start_button_2.wasClicked = false;
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
    for (const thisComponent of instructions_2Components)
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


function instructions_2RoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'instructions_2' ---
    for (const thisComponent of instructions_2Components) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('instructions_2.stopped', globalClock.getTime());
    psychoJS.experiment.addData('start_button_2.numClicks', start_button_2.numClicks);
    psychoJS.experiment.addData('start_button_2.timesOn', start_button_2.timesOn);
    psychoJS.experiment.addData('start_button_2.timesOff', start_button_2.timesOff);
    // the Routine "instructions_2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var trialMaxDurationReached;
var trialMaxDuration;
var trialComponents;
function trialRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'trial' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    trialClock.reset();
    routineTimer.reset();
    trialMaxDurationReached = false;
    // update component parameters for each repeat
    left_image.setImage(left_color);
    right_image.setImage(right_color);
    // setup some python lists for storing info about the mouse
    // current position of the mouse:
    mouse.x = [];
    mouse.y = [];
    mouse.leftButton = [];
    mouse.midButton = [];
    mouse.rightButton = [];
    mouse.time = [];
    mouse.clicked_name = [];
    gotValidClick = false; // until a click is received
    psychoJS.experiment.addData('trial.started', globalClock.getTime());
    trialMaxDuration = null
    // keep track of which components have finished
    trialComponents = [];
    trialComponents.push(background_5);
    trialComponents.push(left_image);
    trialComponents.push(right_image);
    trialComponents.push(mouse);
    
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
    
    // *background_5* updates
    if (t >= 0.0 && background_5.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background_5.tStart = t;  // (not accounting for frame time here)
      background_5.frameNStart = frameN;  // exact frame index
      
      background_5.setAutoDraw(true);
    }
    
    
    // *left_image* updates
    if (t >= 0.0 && left_image.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      left_image.tStart = t;  // (not accounting for frame time here)
      left_image.frameNStart = frameN;  // exact frame index
      
      left_image.setAutoDraw(true);
    }
    
    
    // *right_image* updates
    if (t >= 0.0 && right_image.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      right_image.tStart = t;  // (not accounting for frame time here)
      right_image.frameNStart = frameN;  // exact frame index
      
      right_image.setAutoDraw(true);
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
          mouse.clickableObjects = eval([left_image, right_image])
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
  return async function () {
    //--- Ending Routine 'trial' ---
    for (const thisComponent of trialComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('trial.stopped', globalClock.getTime());
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse.x', mouse.x);
    psychoJS.experiment.addData('mouse.y', mouse.y);
    psychoJS.experiment.addData('mouse.leftButton', mouse.leftButton);
    psychoJS.experiment.addData('mouse.midButton', mouse.midButton);
    psychoJS.experiment.addData('mouse.rightButton', mouse.rightButton);
    psychoJS.experiment.addData('mouse.time', mouse.time);
    psychoJS.experiment.addData('mouse.clicked_name', mouse.clicked_name);
    
    // Run 'End Routine' code from check_correct2
    if ((mouse.clicked_name.slice((- 1))[0] === correct_response)) {
        correct = 1;
    } else {
        correct = 0;
    }
    psychoJS.experiment.addData("correct", correct);
    
    // the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var endMaxDurationReached;
var endMaxDuration;
var endComponents;
function endRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'end' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    endClock.reset();
    routineTimer.reset();
    endMaxDurationReached = false;
    // update component parameters for each repeat
    // reset start_button_3 to account for continued clicks & clear times on/off
    start_button_3.reset()
    psychoJS.experiment.addData('end.started', globalClock.getTime());
    endMaxDuration = null
    // keep track of which components have finished
    endComponents = [];
    endComponents.push(background_7);
    endComponents.push(instr_textbox_3);
    endComponents.push(start_button_3);
    
    for (const thisComponent of endComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function endRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'end' ---
    // get current time
    t = endClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background_7* updates
    if (t >= 0.0 && background_7.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background_7.tStart = t;  // (not accounting for frame time here)
      background_7.frameNStart = frameN;  // exact frame index
      
      background_7.setAutoDraw(true);
    }
    
    
    // *instr_textbox_3* updates
    if (t >= 0.0 && instr_textbox_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instr_textbox_3.tStart = t;  // (not accounting for frame time here)
      instr_textbox_3.frameNStart = frameN;  // exact frame index
      
      instr_textbox_3.setAutoDraw(true);
    }
    
    
    // *start_button_3* updates
    if (t >= 0 && start_button_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      start_button_3.tStart = t;  // (not accounting for frame time here)
      start_button_3.frameNStart = frameN;  // exact frame index
      
      start_button_3.setAutoDraw(true);
    }
    
    if (start_button_3.status === PsychoJS.Status.STARTED) {
      // check whether start_button_3 has been pressed
      if (start_button_3.isClicked) {
        if (!start_button_3.wasClicked) {
          // store time of first click
          start_button_3.timesOn.push(start_button_3.clock.getTime());
          // store time clicked until
          start_button_3.timesOff.push(start_button_3.clock.getTime());
        } else {
          // update time clicked until;
          start_button_3.timesOff[start_button_3.timesOff.length - 1] = start_button_3.clock.getTime();
        }
        if (!start_button_3.wasClicked) {
          // end routine when start_button_3 is clicked
          continueRoutine = false;
          
        }
        // if start_button_3 is still clicked next frame, it is not a new click
        start_button_3.wasClicked = true;
      } else {
        // if start_button_3 is clicked next frame, it is a new click
        start_button_3.wasClicked = false;
      }
    } else {
      // keep clock at 0 if start_button_3 hasn't started / has finished
      start_button_3.clock.reset();
      // if start_button_3 is clicked next frame, it is a new click
      start_button_3.wasClicked = false;
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


function endRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'end' ---
    for (const thisComponent of endComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('end.stopped', globalClock.getTime());
    psychoJS.experiment.addData('start_button_3.numClicks', start_button_3.numClicks);
    psychoJS.experiment.addData('start_button_3.timesOn', start_button_3.timesOn);
    psychoJS.experiment.addData('start_button_3.timesOff', start_button_3.timesOff);
    // the Routine "end" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
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
