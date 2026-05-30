// Source: phone_a_friend (demos/phone_a_friend)
// Project URL: https://gitlab.pavlovia.org/demos/phone_a_friend
// Original file: phone_a_friend.js
﻿/*********************** 
 * Phone_A_Friend *
 ***********************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2025.2.0.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'phone_a_friend';  // from the Builder filename that created this script
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
  color: new util.Color([-0.1216, 0.0039, 0.1294]),
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
    {'name': 'rudy-issa-jedKD4yaTvk-unsplash.jpg', 'path': 'rudy-issa-jedKD4yaTvk-unsplash.jpg'},
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


var instructionsClock;
var background;
var intro_resp;
var instructionsintro;
var trialClock;
var background_2;
var instr_txt_2;
var this_question_text;
var hint_button;
var answer;
var key_resp;
var mouse;
var call_tracker;
var show_hintClock;
var background_3;
var instr_txt;
var n_calls;
var hint_x;
var n_valid;
var n_invalid;
var limit;
var calls_remaining;
var cue_types;
var this_question_text_3;
var friends_hint;
var answer_2;
var key_resp_2;
var warn_userClock;
var background_4;
var textbox;
var byeClock;
var background_5;
var intro_resp_2;
var instructionsintro_2;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "instructions"
  instructionsClock = new util.Clock();
  background = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background', units : undefined, 
    image : 'rudy-issa-jedKD4yaTvk-unsplash.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  intro_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  instructionsintro = new visual.TextBox({
    win: psychoJS.window,
    name: 'instructionsintro',
    text: "On each trial you will be asked a question. \n\nIf you don't know the answer you can phone a friend. \n\nYou can do this only 10 times.\n\nPress space to start",
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
    depth: -2.0 
  });
  
  // Initialize components for Routine "trial"
  trialClock = new util.Clock();
  background_2 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background_2', units : undefined, 
    image : 'rudy-issa-jedKD4yaTvk-unsplash.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  instr_txt_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'instr_txt_2',
    text: 'Type the answer and press enter to submit:',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0.4], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.2],  units: undefined, 
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
    depth: -1.0 
  });
  
  this_question_text = new visual.TextBox({
    win: psychoJS.window,
    name: 'this_question_text',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0.2], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.2],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: [1.0000, 0.9608, 0.8824], borderColor: undefined,
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: false,
    multiline: true,
    anchor: 'center',
    depth: -2.0 
  });
  
  hint_button = new visual.TextBox({
    win: psychoJS.window,
    name: 'hint_button',
    text: 'Click here to phone a friend',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.1],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: (-0.0667, 0.0667, 0.2000), borderColor: undefined,
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: false,
    multiline: true,
    anchor: 'center',
    depth: -3.0 
  });
  
  answer = new visual.TextBox({
    win: psychoJS.window,
    name: 'answer',
    text: '',
    placeholder: undefined,
    font: 'Arial',
    pos: [0, (- 0.05)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.2],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: 'white', borderColor: 'black',
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: true,
    multiline: true,
    anchor: 'center',
    depth: -4.0 
  });
  
  key_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  call_tracker = new visual.TextBox({
    win: psychoJS.window,
    name: 'call_tracker',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, (- 0.45)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.1],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: [0.6078, -0.2784, -0.2784], borderColor: undefined,
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: false,
    multiline: true,
    anchor: 'center',
    depth: -7.0 
  });
  
  // Initialize components for Routine "show_hint"
  show_hintClock = new util.Clock();
  background_3 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background_3', units : undefined, 
    image : 'rudy-issa-jedKD4yaTvk-unsplash.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  instr_txt = new visual.TextBox({
    win: psychoJS.window,
    name: 'instr_txt',
    text: 'Type your answer if you know and press enter (if you don’t know just press enter):',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0.4], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.2],  units: undefined, 
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
    depth: -1.0 
  });
  
  // Run 'Begin Experiment' code from code
  n_calls = 0;
  hint_x = 0;
  n_valid = 5;
  n_invalid = 5;
  limit = 10;
  calls_remaining = limit;
  cue_types = [];
  for (var n, _pj_c = 0, _pj_a = util.range(n_valid), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
      n = _pj_a[_pj_c];
      cue_types.push("valid");
  }
  for (var n, _pj_c = 0, _pj_a = util.range(n_invalid), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
      n = _pj_a[_pj_c];
      cue_types.push("invalid");
  }
  util.shuffle(cue_types);
  
  this_question_text_3 = new visual.TextBox({
    win: psychoJS.window,
    name: 'this_question_text_3',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0.2], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.2],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: [1.0000, 0.9608, 0.8824], borderColor: undefined,
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: false,
    multiline: true,
    anchor: 'center',
    depth: -3.0 
  });
  
  friends_hint = new visual.TextBox({
    win: psychoJS.window,
    name: 'friends_hint',
    text: '',
    placeholder: undefined,
    font: 'Arial',
    pos: [0, (- 0.05)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.2],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: 'white', borderColor: 'black',
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: false,
    multiline: true,
    anchor: 'center',
    depth: -4.0 
  });
  
  answer_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'answer_2',
    text: '',
    placeholder: undefined,
    font: 'Arial',
    pos: [0, (- 0.2)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 0.2],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: 'white', borderColor: 'black',
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: true,
    multiline: true,
    anchor: 'center',
    depth: -5.0 
  });
  
  key_resp_2 = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "warn_user"
  warn_userClock = new util.Clock();
  background_4 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background_4', units : undefined, 
    image : 'rudy-issa-jedKD4yaTvk-unsplash.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  textbox = new visual.TextBox({
    win: psychoJS.window,
    name: 'textbox',
    text: 'YOU HAVE NO CALLS LEFT',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.5],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: [1.0000, -1.0000, -1.0000], borderColor: undefined,
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
  
  // Initialize components for Routine "bye"
  byeClock = new util.Clock();
  background_5 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background_5', units : undefined, 
    image : 'rudy-issa-jedKD4yaTvk-unsplash.jpg', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  intro_resp_2 = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  instructionsintro_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'instructionsintro_2',
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
    depth: -2.0 
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
var _intro_resp_allKeys;
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
    intro_resp.keys = undefined;
    intro_resp.rt = undefined;
    _intro_resp_allKeys = [];
    psychoJS.experiment.addData('instructions.started', globalClock.getTime());
    instructionsMaxDuration = null
    // keep track of which components have finished
    instructionsComponents = [];
    instructionsComponents.push(background);
    instructionsComponents.push(intro_resp);
    instructionsComponents.push(instructionsintro);
    
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
    
    
    // if background is active this frame...
    if (background.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *intro_resp* updates
    if (t >= 0.0 && intro_resp.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      intro_resp.tStart = t;  // (not accounting for frame time here)
      intro_resp.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { intro_resp.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { intro_resp.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { intro_resp.clearEvents(); });
    }
    
    // if intro_resp is active this frame...
    if (intro_resp.status === PsychoJS.Status.STARTED) {
      let theseKeys = intro_resp.getKeys({
        keyList: typeof 'space' === 'string' ? ['space'] : 'space', 
        waitRelease: false
      });
      _intro_resp_allKeys = _intro_resp_allKeys.concat(theseKeys);
      if (_intro_resp_allKeys.length > 0) {
        intro_resp.keys = _intro_resp_allKeys[_intro_resp_allKeys.length - 1].name;  // just the last key pressed
        intro_resp.rt = _intro_resp_allKeys[_intro_resp_allKeys.length - 1].rt;
        intro_resp.duration = _intro_resp_allKeys[_intro_resp_allKeys.length - 1].duration;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    
    // *instructionsintro* updates
    if (t >= 0.0 && instructionsintro.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instructionsintro.tStart = t;  // (not accounting for frame time here)
      instructionsintro.frameNStart = frameN;  // exact frame index
      
      instructionsintro.setAutoDraw(true);
    }
    
    
    // if instructionsintro is active this frame...
    if (instructionsintro.status === PsychoJS.Status.STARTED) {
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
      currentLoop.addResponse(intro_resp.corr, level);
    }
    psychoJS.experiment.addData('intro_resp.keys', intro_resp.keys);
    if (typeof intro_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('intro_resp.rt', intro_resp.rt);
        psychoJS.experiment.addData('intro_resp.duration', intro_resp.duration);
        routineTimer.reset();
        }
    
    intro_resp.stop();
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
      trialsLoopScheduler.add(show_hintRoutineBegin(snapshot));
      trialsLoopScheduler.add(show_hintRoutineEachFrame());
      trialsLoopScheduler.add(show_hintRoutineEnd(snapshot));
      trialsLoopScheduler.add(warn_userRoutineBegin(snapshot));
      trialsLoopScheduler.add(warn_userRoutineEachFrame());
      trialsLoopScheduler.add(warn_userRoutineEnd(snapshot));
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
    this_question_text.setText(this_question);
    hint_button.setPos([hint_x, (- 0.35)]);
    answer.setText('');
    answer.refresh();
    answer.setText('');
    key_resp.keys = undefined;
    key_resp.rt = undefined;
    _key_resp_allKeys = [];
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
    call_tracker.setText(("Calls remaining: " + calls_remaining.toString()));
    psychoJS.experiment.addData('trial.started', globalClock.getTime());
    trialMaxDuration = null
    // keep track of which components have finished
    trialComponents = [];
    trialComponents.push(background_2);
    trialComponents.push(instr_txt_2);
    trialComponents.push(this_question_text);
    trialComponents.push(hint_button);
    trialComponents.push(answer);
    trialComponents.push(key_resp);
    trialComponents.push(mouse);
    trialComponents.push(call_tracker);
    
    for (const thisComponent of trialComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var prevButtonState;
var _mouseButtons;
var _mouseXYs;
function trialRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'trial' ---
    // get current time
    t = trialClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background_2* updates
    if (t >= 0.0 && background_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background_2.tStart = t;  // (not accounting for frame time here)
      background_2.frameNStart = frameN;  // exact frame index
      
      background_2.setAutoDraw(true);
    }
    
    
    // if background_2 is active this frame...
    if (background_2.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *instr_txt_2* updates
    if (t >= 0.0 && instr_txt_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instr_txt_2.tStart = t;  // (not accounting for frame time here)
      instr_txt_2.frameNStart = frameN;  // exact frame index
      
      instr_txt_2.setAutoDraw(true);
    }
    
    
    // if instr_txt_2 is active this frame...
    if (instr_txt_2.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *this_question_text* updates
    if (t >= 0.0 && this_question_text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      this_question_text.tStart = t;  // (not accounting for frame time here)
      this_question_text.frameNStart = frameN;  // exact frame index
      
      this_question_text.setAutoDraw(true);
    }
    
    
    // if this_question_text is active this frame...
    if (this_question_text.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *hint_button* updates
    if (t >= 0.0 && hint_button.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      hint_button.tStart = t;  // (not accounting for frame time here)
      hint_button.frameNStart = frameN;  // exact frame index
      
      hint_button.setAutoDraw(true);
    }
    
    
    // if hint_button is active this frame...
    if (hint_button.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *answer* updates
    if (t >= 0.0 && answer.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      answer.tStart = t;  // (not accounting for frame time here)
      answer.frameNStart = frameN;  // exact frame index
      
      answer.setAutoDraw(true);
    }
    
    
    // if answer is active this frame...
    if (answer.status === PsychoJS.Status.STARTED) {
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
      let theseKeys = key_resp.getKeys({
        keyList: typeof 'return' === 'string' ? ['return'] : 'return', 
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
          mouse.clickableObjects = eval(hint_button)
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
    
    // *call_tracker* updates
    if (t >= 0.0 && call_tracker.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      call_tracker.tStart = t;  // (not accounting for frame time here)
      call_tracker.frameNStart = frameN;  // exact frame index
      
      call_tracker.setAutoDraw(true);
    }
    
    
    // if call_tracker is active this frame...
    if (call_tracker.status === PsychoJS.Status.STARTED) {
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
    psychoJS.experiment.addData('answer.text',answer.text)
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
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse.x', mouse.x);
    psychoJS.experiment.addData('mouse.y', mouse.y);
    psychoJS.experiment.addData('mouse.leftButton', mouse.leftButton);
    psychoJS.experiment.addData('mouse.midButton', mouse.midButton);
    psychoJS.experiment.addData('mouse.rightButton', mouse.rightButton);
    psychoJS.experiment.addData('mouse.time', mouse.time);
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


var show_hintMaxDurationReached;
var warn;
var cue_type;
var this_hint;
var _key_resp_2_allKeys;
var show_hintMaxDuration;
var show_hintComponents;
function show_hintRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'show_hint' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    show_hintClock.reset();
    routineTimer.reset();
    show_hintMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from code
    if (key_resp.keys) {
        continueRoutine = false;
    } else {
        n_calls += 1;
        calls_remaining = (limit - n_calls);
    }
    warn = false;
    if ((n_calls >= limit)) {
        continueRoutine = false;
        warn = true;
        hint_x = (- 500);
    }
    util.shuffle(cue_types);
    cue_type = null;
    if ((cue_types.length > 0)) {
        cue_type = cue_types.slice((- 1))[0];
        if ((cue_type === "valid")) {
            this_hint = this_cue_valid;
        } else {
            this_hint = this_cue_invalid;
        }
        cue_types.splice((cue_types.length - 1), 1);
    }
    psychoJS.experiment.addData("cue_type", cue_type);
    psychoJS.experiment.addData("this_hint", this_hint);
    psychoJS.experiment.addData("n_calls", n_calls);
    psychoJS.experiment.addData("calls_remaining", calls_remaining);
    
    this_question_text_3.setText(this_question);
    friends_hint.setText(("Hint: " + this_hint));
    answer_2.setText('');
    answer_2.refresh();
    key_resp_2.keys = undefined;
    key_resp_2.rt = undefined;
    _key_resp_2_allKeys = [];
    psychoJS.experiment.addData('show_hint.started', globalClock.getTime());
    show_hintMaxDuration = null
    // keep track of which components have finished
    show_hintComponents = [];
    show_hintComponents.push(background_3);
    show_hintComponents.push(instr_txt);
    show_hintComponents.push(this_question_text_3);
    show_hintComponents.push(friends_hint);
    show_hintComponents.push(answer_2);
    show_hintComponents.push(key_resp_2);
    
    for (const thisComponent of show_hintComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function show_hintRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'show_hint' ---
    // get current time
    t = show_hintClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background_3* updates
    if (t >= 0.0 && background_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background_3.tStart = t;  // (not accounting for frame time here)
      background_3.frameNStart = frameN;  // exact frame index
      
      background_3.setAutoDraw(true);
    }
    
    
    // if background_3 is active this frame...
    if (background_3.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *instr_txt* updates
    if (t >= 0.0 && instr_txt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instr_txt.tStart = t;  // (not accounting for frame time here)
      instr_txt.frameNStart = frameN;  // exact frame index
      
      instr_txt.setAutoDraw(true);
    }
    
    
    // if instr_txt is active this frame...
    if (instr_txt.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *this_question_text_3* updates
    if (t >= 0.0 && this_question_text_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      this_question_text_3.tStart = t;  // (not accounting for frame time here)
      this_question_text_3.frameNStart = frameN;  // exact frame index
      
      this_question_text_3.setAutoDraw(true);
    }
    
    
    // if this_question_text_3 is active this frame...
    if (this_question_text_3.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *friends_hint* updates
    if (t >= 0.0 && friends_hint.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      friends_hint.tStart = t;  // (not accounting for frame time here)
      friends_hint.frameNStart = frameN;  // exact frame index
      
      friends_hint.setAutoDraw(true);
    }
    
    
    // if friends_hint is active this frame...
    if (friends_hint.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *answer_2* updates
    if (t >= 0.0 && answer_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      answer_2.tStart = t;  // (not accounting for frame time here)
      answer_2.frameNStart = frameN;  // exact frame index
      
      answer_2.setAutoDraw(true);
    }
    
    
    // if answer_2 is active this frame...
    if (answer_2.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *key_resp_2* updates
    if (t >= 0.0 && key_resp_2.status === PsychoJS.Status.NOT_STARTED) {
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
        keyList: typeof 'return' === 'string' ? ['return'] : 'return', 
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
    for (const thisComponent of show_hintComponents)
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


function show_hintRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'show_hint' ---
    for (const thisComponent of show_hintComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('show_hint.stopped', globalClock.getTime());
    psychoJS.experiment.addData('answer_2.text',answer_2.text)
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
    // the Routine "show_hint" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var warn_userMaxDurationReached;
var maxDurationReached;
var warn_userMaxDuration;
var warn_userComponents;
function warn_userRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'warn_user' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    warn_userClock.reset(routineTimer.getTime());
    routineTimer.add(1.000000);
    warn_userMaxDurationReached = false;
    // update component parameters for each repeat
    psychoJS.experiment.addData('warn_user.started', globalClock.getTime());
    // skip this Routine if its 'Skip if' condition is True
    continueRoutine = continueRoutine && !((warn == 0));
    maxDurationReached = false
    warn_userMaxDuration = null
    // keep track of which components have finished
    warn_userComponents = [];
    warn_userComponents.push(background_4);
    warn_userComponents.push(textbox);
    
    for (const thisComponent of warn_userComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var frameRemains;
function warn_userRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'warn_user' ---
    // get current time
    t = warn_userClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background_4* updates
    if (t >= 0.0 && background_4.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background_4.tStart = t;  // (not accounting for frame time here)
      background_4.frameNStart = frameN;  // exact frame index
      
      background_4.setAutoDraw(true);
    }
    
    
    // if background_4 is active this frame...
    if (background_4.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 1 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (background_4.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      background_4.tStop = t;  // not accounting for scr refresh
      background_4.frameNStop = frameN;  // exact frame index
      // update status
      background_4.status = PsychoJS.Status.FINISHED;
      background_4.setAutoDraw(false);
    }
    
    
    // *textbox* updates
    if (t >= 0.0 && textbox.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      textbox.tStart = t;  // (not accounting for frame time here)
      textbox.frameNStart = frameN;  // exact frame index
      
      textbox.setAutoDraw(true);
    }
    
    
    // if textbox is active this frame...
    if (textbox.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 1.0 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (textbox.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      textbox.tStop = t;  // not accounting for scr refresh
      textbox.frameNStop = frameN;  // exact frame index
      // update status
      textbox.status = PsychoJS.Status.FINISHED;
      textbox.setAutoDraw(false);
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
    for (const thisComponent of warn_userComponents)
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


function warn_userRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'warn_user' ---
    for (const thisComponent of warn_userComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('warn_user.stopped', globalClock.getTime());
    if (routineForceEnded) {
        routineTimer.reset();} else if (warn_userMaxDurationReached) {
        warn_userClock.add(warn_userMaxDuration);
    } else {
        warn_userClock.add(1.000000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var byeMaxDurationReached;
var _intro_resp_2_allKeys;
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
    byeClock.reset();
    routineTimer.reset();
    byeMaxDurationReached = false;
    // update component parameters for each repeat
    intro_resp_2.keys = undefined;
    intro_resp_2.rt = undefined;
    _intro_resp_2_allKeys = [];
    psychoJS.experiment.addData('bye.started', globalClock.getTime());
    byeMaxDuration = null
    // keep track of which components have finished
    byeComponents = [];
    byeComponents.push(background_5);
    byeComponents.push(intro_resp_2);
    byeComponents.push(instructionsintro_2);
    
    for (const thisComponent of byeComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function byeRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'bye' ---
    // get current time
    t = byeClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background_5* updates
    if (t >= 0.0 && background_5.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background_5.tStart = t;  // (not accounting for frame time here)
      background_5.frameNStart = frameN;  // exact frame index
      
      background_5.setAutoDraw(true);
    }
    
    
    // if background_5 is active this frame...
    if (background_5.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *intro_resp_2* updates
    if (t >= 0.0 && intro_resp_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      intro_resp_2.tStart = t;  // (not accounting for frame time here)
      intro_resp_2.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { intro_resp_2.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { intro_resp_2.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { intro_resp_2.clearEvents(); });
    }
    
    // if intro_resp_2 is active this frame...
    if (intro_resp_2.status === PsychoJS.Status.STARTED) {
      let theseKeys = intro_resp_2.getKeys({
        keyList: typeof 'space' === 'string' ? ['space'] : 'space', 
        waitRelease: false
      });
      _intro_resp_2_allKeys = _intro_resp_2_allKeys.concat(theseKeys);
      if (_intro_resp_2_allKeys.length > 0) {
        intro_resp_2.keys = _intro_resp_2_allKeys[_intro_resp_2_allKeys.length - 1].name;  // just the last key pressed
        intro_resp_2.rt = _intro_resp_2_allKeys[_intro_resp_2_allKeys.length - 1].rt;
        intro_resp_2.duration = _intro_resp_2_allKeys[_intro_resp_2_allKeys.length - 1].duration;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    
    // *instructionsintro_2* updates
    if (t >= 0.0 && instructionsintro_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instructionsintro_2.tStart = t;  // (not accounting for frame time here)
      instructionsintro_2.frameNStart = frameN;  // exact frame index
      
      instructionsintro_2.setAutoDraw(true);
    }
    
    
    // if instructionsintro_2 is active this frame...
    if (instructionsintro_2.status === PsychoJS.Status.STARTED) {
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
    if (continueRoutine) {
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
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(intro_resp_2.corr, level);
    }
    psychoJS.experiment.addData('intro_resp_2.keys', intro_resp_2.keys);
    if (typeof intro_resp_2.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('intro_resp_2.rt', intro_resp_2.rt);
        psychoJS.experiment.addData('intro_resp_2.duration', intro_resp_2.duration);
        routineTimer.reset();
        }
    
    intro_resp_2.stop();
    // the Routine "bye" was not non-slip safe, so reset the non-slip timer
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
