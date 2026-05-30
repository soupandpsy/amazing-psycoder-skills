// Source: wisconsin_card_sorting (demos/wisconsin_card_sorting)
// Project URL: https://gitlab.pavlovia.org/demos/wisconsin_card_sorting
// Original file: Wisconsin Card Sorting Task.js
﻿/************************************ 
 * Wisconsin Card Sorting Task Test *
 ************************************/

import { core, data, sound, util, visual } from './lib/psychojs-2022.1.2.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'Wisconsin Card Sorting Task';  // from the Builder filename that created this script
let expInfo = {'participant': '', 'session': '001'};

// Start code blocks for 'Before Experiment'
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
flowScheduler.add(InstructionsRoutineBegin());
flowScheduler.add(InstructionsRoutineEachFrame());
flowScheduler.add(InstructionsRoutineEnd());
flowScheduler.add(ExampleRoutineBegin());
flowScheduler.add(ExampleRoutineEachFrame());
flowScheduler.add(ExampleRoutineEnd());
const blocksLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(blocksLoopBegin(blocksLoopScheduler));
flowScheduler.add(blocksLoopScheduler);
flowScheduler.add(blocksLoopEnd);
flowScheduler.add(EndRoutineBegin());
flowScheduler.add(EndRoutineEachFrame());
flowScheduler.add(EndRoutineEnd());
flowScheduler.add(quitPsychoJS, '', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, '', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    {'name': 'images/3blueCrosses.jpg', 'path': 'images/3blueCrosses.jpg'},
    {'name': 'images/3yellowCrosses.jpg', 'path': 'images/3yellowCrosses.jpg'},
    {'name': 'images/2greenStars.jpg', 'path': 'images/2greenStars.jpg'},
    {'name': 'images/2redCrosses.jpg', 'path': 'images/2redCrosses.jpg'},
    {'name': 'images/3yellowDots.jpg', 'path': 'images/3yellowDots.jpg'},
    {'name': 'images/4blueTriangles.jpg', 'path': 'images/4blueTriangles.jpg'},
    {'name': 'images/4redCrosses.jpg', 'path': 'images/4redCrosses.jpg'},
    {'name': 'images/2blueStars.jpg', 'path': 'images/2blueStars.jpg'},
    {'name': 'images/3greenStars.jpg', 'path': 'images/3greenStars.jpg'},
    {'name': 'images/1yellowTriangle.jpg', 'path': 'images/1yellowTriangle.jpg'},
    {'name': 'example.jpg', 'path': 'example.jpg'},
    {'name': 'images/1redTriangle.jpg', 'path': 'images/1redTriangle.jpg'},
    {'name': 'images/3redTriangles.jpg', 'path': 'images/3redTriangles.jpg'},
    {'name': 'images/4yellowTriangles.jpg', 'path': 'images/4yellowTriangles.jpg'},
    {'name': 'images/3redStars.jpg', 'path': 'images/3redStars.jpg'},
    {'name': 'images/2greenDots.jpg', 'path': 'images/2greenDots.jpg'},
    {'name': 'images/3yellowStars.jpg', 'path': 'images/3yellowStars.jpg'},
    {'name': 'images/3yellowTriangles.jpg', 'path': 'images/3yellowTriangles.jpg'},
    {'name': 'images/1greenTriangle.jpg', 'path': 'images/1greenTriangle.jpg'},
    {'name': 'images/3greenDots.jpg', 'path': 'images/3greenDots.jpg'},
    {'name': 'images/2blueTriangles.jpg', 'path': 'images/2blueTriangles.jpg'},
    {'name': 'images/4greenDots.jpg', 'path': 'images/4greenDots.jpg'},
    {'name': 'images/2yellowDots.jpg', 'path': 'images/2yellowDots.jpg'},
    {'name': 'images/2yellowStars.jpg', 'path': 'images/2yellowStars.jpg'},
    {'name': 'images/3greenTriangles.jpg', 'path': 'images/3greenTriangles.jpg'},
    {'name': 'images/2greenTriangles.jpg', 'path': 'images/2greenTriangles.jpg'},
    {'name': 'images/4blueCrosses.jpg', 'path': 'images/4blueCrosses.jpg'},
    {'name': 'cards.xlsx', 'path': 'cards.xlsx'},
    {'name': 'images/2redStars.jpg', 'path': 'images/2redStars.jpg'},
    {'name': 'continue.png', 'path': 'continue.png'},
    {'name': 'images/3blueDots.jpg', 'path': 'images/3blueDots.jpg'},
    {'name': 'images/2yellowCrosses.jpg', 'path': 'images/2yellowCrosses.jpg'},
    {'name': 'images/2yellowTriangles.jpg', 'path': 'images/2yellowTriangles.jpg'},
    {'name': 'images/3blueTriangles.jpg', 'path': 'images/3blueTriangles.jpg'},
    {'name': 'images/4yellowStars.jpg', 'path': 'images/4yellowStars.jpg'},
    {'name': 'images/4greenStars.jpg', 'path': 'images/4greenStars.jpg'},
    {'name': 'images/2greenCrosses.jpg', 'path': 'images/2greenCrosses.jpg'},
    {'name': 'images/4blueDots.jpg', 'path': 'images/4blueDots.jpg'},
    {'name': 'images/4redDots.jpg', 'path': 'images/4redDots.jpg'},
    {'name': 'images/4greenTriangles.jpg', 'path': 'images/4greenTriangles.jpg'},
    {'name': 'chooseRule.xlsx', 'path': 'chooseRule.xlsx'},
    {'name': 'images/4greenCrosses.jpg', 'path': 'images/4greenCrosses.jpg'},
    {'name': 'images/4blueStars.jpg', 'path': 'images/4blueStars.jpg'},
    {'name': 'images/1greenCross.jpg', 'path': 'images/1greenCross.jpg'},
    {'name': 'images/3greenCrosses.jpg', 'path': 'images/3greenCrosses.jpg'},
    {'name': 'images/4redTriangles.jpg', 'path': 'images/4redTriangles.jpg'},
    {'name': 'images/1blueDot.jpg', 'path': 'images/1blueDot.jpg'},
    {'name': 'images/1redCross.jpg', 'path': 'images/1redCross.jpg'},
    {'name': 'images/1yellowCross.jpg', 'path': 'images/1yellowCross.jpg'},
    {'name': 'images/1yellowDot.jpg', 'path': 'images/1yellowDot.jpg'},
    {'name': 'images/2blueDots.jpg', 'path': 'images/2blueDots.jpg'},
    {'name': 'images/1redStar.jpg', 'path': 'images/1redStar.jpg'},
    {'name': 'images/1greenStar.jpg', 'path': 'images/1greenStar.jpg'},
    {'name': 'images/1blueCross.jpg', 'path': 'images/1blueCross.jpg'},
    {'name': 'images/1greenDot.jpg', 'path': 'images/1greenDot.jpg'},
    {'name': 'images/1redDot.jpg', 'path': 'images/1redDot.jpg'},
    {'name': 'images/4yellowDots.jpg', 'path': 'images/4yellowDots.jpg'},
    {'name': 'images/1blueStar.jpg', 'path': 'images/1blueStar.jpg'},
    {'name': 'images/3redCrosses.jpg', 'path': 'images/3redCrosses.jpg'},
    {'name': 'images/1yellowStar.jpg', 'path': 'images/1yellowStar.jpg'},
    {'name': 'images/3redDots.jpg', 'path': 'images/3redDots.jpg'},
    {'name': 'images/1blueTriangle.jpg', 'path': 'images/1blueTriangle.jpg'},
    {'name': 'images/2blueCrosses.jpg', 'path': 'images/2blueCrosses.jpg'},
    {'name': 'images/2redTriangles.jpg', 'path': 'images/2redTriangles.jpg'},
    {'name': 'images/4redStars.jpg', 'path': 'images/4redStars.jpg'},
    {'name': 'images/4yellowCrosses.jpg', 'path': 'images/4yellowCrosses.jpg'},
    {'name': 'images/2redDots.jpg', 'path': 'images/2redDots.jpg'},
    {'name': 'images/3blueStars.jpg', 'path': 'images/3blueStars.jpg'}
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.EXP);


var frameDur;
async function updateInfo() {
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2022.1.2';
  expInfo['OS'] = window.navigator.platform;

  psychoJS.experiment.dataFileName = (("." + "/") + `data/${expInfo["participant"]}_${expName}_${expInfo["date"]}`);

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


var InstructionsClock;
var instructions;
var continue_button;
var mouse_2;
var ExampleClock;
var example_text;
var example_image;
var example_text_2;
var mouse;
var TrialsClock;
var fixation;
var one_red_dot;
var two_yellow_triangles;
var three_green_crosses;
var four_blue_stars;
var trial_card;
var response;
var FeedbackClock;
var msg;
var feedback_text;
var EndClock;
var thank_you;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "Instructions"
  InstructionsClock = new util.Clock();
  instructions = new visual.TextStim({
    win: psychoJS.window,
    name: 'instructions',
    text: 'In this task you will be required to sort the presented cards based on a rule i.e. the cards will have to be sorted based on either colour, shape or number. The rule will not be presented, however you will receive feedback on each trial. After a certain amount of trials the rule will change to a different one. To select your response click on one of the four cards presented at the top of the screen. ',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], height: 0.05,  wrapWidth: 0.9, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: 0.0 
  });
  
  continue_button = new visual.ImageStim({
    win : psychoJS.window,
    name : 'continue_button', units : undefined, 
    image : 'continue.png', mask : undefined,
    ori : 0.0, pos : [0, (- 0.4)], size : [0.65, 0.1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -1.0 
  });
  mouse_2 = new core.Mouse({
    win: psychoJS.window,
  });
  mouse_2.mouseClock = new util.Clock();
  // Initialize components for Routine "Example"
  ExampleClock = new util.Clock();
  example_text = new visual.TextStim({
    win: psychoJS.window,
    name: 'example_text',
    text: 'For example, you may see a screen like this:',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0.4], height: 0.04,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: 0.0 
  });
  
  example_image = new visual.ImageStim({
    win : psychoJS.window,
    name : 'example_image', units : undefined, 
    image : 'example.jpg', mask : undefined,
    ori : 0, pos : [0, 0.15], size : [0.7, 0.4],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -1.0 
  });
  example_text_2 = new visual.TextStim({
    win: psychoJS.window,
    name: 'example_text_2',
    text: 'The presented card (bottom centre) can be categorised based on shape (dots), colour (yellow) or number (three). Click on the first card if you want to categorise it by the shape, second if you want categorise it by colour and third if you want to categorise it by number. After you select your response, feedback will be provided. Click on the image to start the experiment.',
    font: 'Arial',
    units: undefined, 
    pos: [0, (- 0.25)], height: 0.04,  wrapWidth: 0.9, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: -2.0 
  });
  
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  // Initialize components for Routine "Trials"
  TrialsClock = new util.Clock();
  fixation = new visual.TextStim({
    win: psychoJS.window,
    name: 'fixation',
    text: '+',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], height: 0.05,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: -1.0 
  });
  
  one_red_dot = new visual.ImageStim({
    win : psychoJS.window,
    name : 'one_red_dot', units : undefined, 
    image : 'images/1redDot.jpg', mask : undefined,
    ori : 0, pos : [(- 0.375), 0.25], size : [0.2, 0.2],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -2.0 
  });
  two_yellow_triangles = new visual.ImageStim({
    win : psychoJS.window,
    name : 'two_yellow_triangles', units : undefined, 
    image : 'images/2yellowTriangles.jpg', mask : undefined,
    ori : 0, pos : [(- 0.125), 0.25], size : [0.2, 0.2],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -3.0 
  });
  three_green_crosses = new visual.ImageStim({
    win : psychoJS.window,
    name : 'three_green_crosses', units : undefined, 
    image : 'images/3greenCrosses.jpg', mask : undefined,
    ori : 0, pos : [0.125, 0.25], size : [0.2, 0.2],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -4.0 
  });
  four_blue_stars = new visual.ImageStim({
    win : psychoJS.window,
    name : 'four_blue_stars', units : undefined, 
    image : 'images/4blueStars.jpg', mask : undefined,
    ori : 0, pos : [0.375, 0.25], size : [0.2, 0.2],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -5.0 
  });
  trial_card = new visual.ImageStim({
    win : psychoJS.window,
    name : 'trial_card', units : undefined, 
    image : undefined, mask : undefined,
    ori : 0, pos : [0, (- 0.2)], size : [0.25, 0.25],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -6.0 
  });
  response = new core.Mouse({
    win: psychoJS.window,
  });
  response.mouseClock = new util.Clock();
  // Initialize components for Routine "Feedback"
  FeedbackClock = new util.Clock();
  msg = "";
  
  feedback_text = new visual.TextStim({
    win: psychoJS.window,
    name: 'feedback_text',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], height: 0.05,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: -1.0 
  });
  
  // Initialize components for Routine "End"
  EndClock = new util.Clock();
  thank_you = new visual.TextStim({
    win: psychoJS.window,
    name: 'thank_you',
    text: 'This is the end of the experiment.\nThank you for your time.',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], height: 0.05,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
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
var gotValidClick;
var InstructionsComponents;
function InstructionsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //------Prepare to start Routine 'Instructions'-------
    t = 0;
    InstructionsClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // update component parameters for each repeat
    // setup some python lists for storing info about the mouse_2
    mouse_2.clicked_name = [];
    gotValidClick = false; // until a click is received
    // keep track of which components have finished
    InstructionsComponents = [];
    InstructionsComponents.push(instructions);
    InstructionsComponents.push(continue_button);
    InstructionsComponents.push(mouse_2);
    
    for (const thisComponent of InstructionsComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var prevButtonState;
var _mouseButtons;
function InstructionsRoutineEachFrame() {
  return async function () {
    //------Loop for each frame of Routine 'Instructions'-------
    // get current time
    t = InstructionsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *instructions* updates
    if (t >= 0.0 && instructions.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instructions.tStart = t;  // (not accounting for frame time here)
      instructions.frameNStart = frameN;  // exact frame index
      
      instructions.setAutoDraw(true);
    }

    
    // *continue_button* updates
    if (t >= 1 && continue_button.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      continue_button.tStart = t;  // (not accounting for frame time here)
      continue_button.frameNStart = frameN;  // exact frame index
      
      continue_button.setAutoDraw(true);
    }

    // *mouse_2* updates
    if (t >= 1 && mouse_2.status === PsychoJS.Status.NOT_STARTED) {
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
          for (const obj of [continue_button]) {
            if (obj.contains(mouse_2)) {
              gotValidClick = true;
              mouse_2.clicked_name.push(obj.name)
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
    for (const thisComponent of InstructionsComponents)
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


function InstructionsRoutineEnd() {
  return async function () {
    //------Ending Routine 'Instructions'-------
    for (const thisComponent of InstructionsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    // store data for psychoJS.experiment (ExperimentHandler)
    // the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    return Scheduler.Event.NEXT;
  };
}


var ExampleComponents;
function ExampleRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //------Prepare to start Routine 'Example'-------
    t = 0;
    ExampleClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // update component parameters for each repeat
    // setup some python lists for storing info about the mouse
    mouse.clicked_name = [];
    gotValidClick = false; // until a click is received
    // keep track of which components have finished
    ExampleComponents = [];
    ExampleComponents.push(example_text);
    ExampleComponents.push(example_image);
    ExampleComponents.push(example_text_2);
    ExampleComponents.push(mouse);
    
    for (const thisComponent of ExampleComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function ExampleRoutineEachFrame() {
  return async function () {
    //------Loop for each frame of Routine 'Example'-------
    // get current time
    t = ExampleClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *example_text* updates
    if (t >= 0.0 && example_text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      example_text.tStart = t;  // (not accounting for frame time here)
      example_text.frameNStart = frameN;  // exact frame index
      
      example_text.setAutoDraw(true);
    }

    
    // *example_image* updates
    if (t >= 0.0 && example_image.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      example_image.tStart = t;  // (not accounting for frame time here)
      example_image.frameNStart = frameN;  // exact frame index
      
      example_image.setAutoDraw(true);
    }

    
    // *example_text_2* updates
    if (t >= 0.0 && example_text_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      example_text_2.tStart = t;  // (not accounting for frame time here)
      example_text_2.frameNStart = frameN;  // exact frame index
      
      example_text_2.setAutoDraw(true);
    }

    // *mouse* updates
    if (t >= 1 && mouse.status === PsychoJS.Status.NOT_STARTED) {
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
          for (const obj of [example_image]) {
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
    for (const thisComponent of ExampleComponents)
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


function ExampleRoutineEnd() {
  return async function () {
    //------Ending Routine 'Example'-------
    for (const thisComponent of ExampleComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    // store data for psychoJS.experiment (ExperimentHandler)
    // the Routine "Example" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    return Scheduler.Event.NEXT;
  };
}


var blocks;
var currentLoop;
function blocksLoopBegin(blocksLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    blocks = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 2, method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: 'chooseRule.xlsx',
      seed: undefined, name: 'blocks'
    });
    psychoJS.experiment.addLoop(blocks); // add the loop to the experiment
    currentLoop = blocks;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisBlock of blocks) {
      const snapshot = blocks.getSnapshot();
      blocksLoopScheduler.add(importConditions(snapshot));
      const trialsLoopScheduler = new Scheduler(psychoJS);
      blocksLoopScheduler.add(trialsLoopBegin(trialsLoopScheduler, snapshot));
      blocksLoopScheduler.add(trialsLoopScheduler);
      blocksLoopScheduler.add(trialsLoopEnd);
      blocksLoopScheduler.add(endLoopIteration(blocksLoopScheduler, snapshot));
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
      trialList: TrialHandler.importConditions(psychoJS.serverManager, 'cards.xlsx', useRows),
      seed: undefined, name: 'trials'
    });
    psychoJS.experiment.addLoop(trials); // add the loop to the experiment
    currentLoop = trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisTrial of trials) {
      const snapshot = trials.getSnapshot();
      trialsLoopScheduler.add(importConditions(snapshot));
      trialsLoopScheduler.add(TrialsRoutineBegin(snapshot));
      trialsLoopScheduler.add(TrialsRoutineEachFrame());
      trialsLoopScheduler.add(TrialsRoutineEnd());
      trialsLoopScheduler.add(FeedbackRoutineBegin(snapshot));
      trialsLoopScheduler.add(FeedbackRoutineEachFrame());
      trialsLoopScheduler.add(FeedbackRoutineEnd());
      trialsLoopScheduler.add(endLoopIteration(trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}


async function trialsLoopEnd() {
  psychoJS.experiment.removeLoop(trials);

  return Scheduler.Event.NEXT;
}


async function blocksLoopEnd() {
  psychoJS.experiment.removeLoop(blocks);

  return Scheduler.Event.NEXT;
}


var corr;
var rt;
var TrialsComponents;
function TrialsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //------Prepare to start Routine 'Trials'-------
    t = 0;
    TrialsClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // update component parameters for each repeat
    corr = 0;
    rt = 0;
    console.log("card", card);
    console.log("corrAns", corrAns);
    
    trial_card.setImage(card);
    // setup some python lists for storing info about the response
    response.clicked_name = [];
    gotValidClick = false; // until a click is received
    // keep track of which components have finished
    TrialsComponents = [];
    TrialsComponents.push(fixation);
    TrialsComponents.push(one_red_dot);
    TrialsComponents.push(two_yellow_triangles);
    TrialsComponents.push(three_green_crosses);
    TrialsComponents.push(four_blue_stars);
    TrialsComponents.push(trial_card);
    TrialsComponents.push(response);
    
    for (const thisComponent of TrialsComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var frameRemains;
function TrialsRoutineEachFrame() {
  return async function () {
    //------Loop for each frame of Routine 'Trials'-------
    // get current time
    t = TrialsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    rt = Math.round((t * 1000));
    
    
    // *fixation* updates
    if (t >= 0.0 && fixation.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fixation.tStart = t;  // (not accounting for frame time here)
      fixation.frameNStart = frameN;  // exact frame index
      
      fixation.setAutoDraw(true);
    }

    frameRemains = 0.0 + 1.0 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
    if (fixation.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      fixation.setAutoDraw(false);
    }
    
    // *one_red_dot* updates
    if (t >= 0 && one_red_dot.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      one_red_dot.tStart = t;  // (not accounting for frame time here)
      one_red_dot.frameNStart = frameN;  // exact frame index
      
      one_red_dot.setAutoDraw(true);
    }

    
    // *two_yellow_triangles* updates
    if (t >= 0 && two_yellow_triangles.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      two_yellow_triangles.tStart = t;  // (not accounting for frame time here)
      two_yellow_triangles.frameNStart = frameN;  // exact frame index
      
      two_yellow_triangles.setAutoDraw(true);
    }

    
    // *three_green_crosses* updates
    if (t >= 0 && three_green_crosses.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      three_green_crosses.tStart = t;  // (not accounting for frame time here)
      three_green_crosses.frameNStart = frameN;  // exact frame index
      
      three_green_crosses.setAutoDraw(true);
    }

    
    // *four_blue_stars* updates
    if (t >= 0 && four_blue_stars.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      four_blue_stars.tStart = t;  // (not accounting for frame time here)
      four_blue_stars.frameNStart = frameN;  // exact frame index
      
      four_blue_stars.setAutoDraw(true);
    }

    
    // *trial_card* updates
    if (t >= 1 && trial_card.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      trial_card.tStart = t;  // (not accounting for frame time here)
      trial_card.frameNStart = frameN;  // exact frame index
      
      trial_card.setAutoDraw(true);
    }

    // *response* updates
    if (t >= 1 && response.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      response.tStart = t;  // (not accounting for frame time here)
      response.frameNStart = frameN;  // exact frame index
      
      response.status = PsychoJS.Status.STARTED;
      response.mouseClock.reset();
      prevButtonState = response.getPressed();  // if button is down already this ISN'T a new click
      }
    if (response.status === PsychoJS.Status.STARTED) {  // only update if started and not finished!
      _mouseButtons = response.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          for (const obj of [one_red_dot, two_yellow_triangles, three_green_crosses, four_blue_stars]) {
            if (obj.contains(response)) {
              gotValidClick = true;
              response.clicked_name.push(obj.name)
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
    for (const thisComponent of TrialsComponents)
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
function TrialsRoutineEnd() {
  return async function () {
    //------Ending Routine 'Trials'-------
    for (const thisComponent of TrialsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    if ((response.clicked_name === corrAns)) {
        corr = 1;
    } else {
        if ((one_red_dot.contains(response) && (corrAns === "one_red_dot"))) {
            corr = 1;
        } else {
            if ((two_yellow_triangles.contains(response) && (corrAns === "two_yellow_triangles"))) {
                corr = 1;
            } else {
                if ((three_green_crosses.contains(response) && (corrAns === "three_green_crosses"))) {
                    corr = 1;
                } else {
                    if ((four_blue_stars.contains(response) && (corrAns === "four_blue_stars"))) {
                        corr = 1;
                    }
                }
            }
        }
    }
    console.log("Response", response.clicked_name);
    psychoJS.experiment.addData("Score", corr);
    psychoJS.experiment.addData("RT", rt);
    
    // store data for psychoJS.experiment (ExperimentHandler)
    _mouseXYs = response.getPos();
    _mouseButtons = response.getPressed();
    psychoJS.experiment.addData('response.x', _mouseXYs[0]);
    psychoJS.experiment.addData('response.y', _mouseXYs[1]);
    psychoJS.experiment.addData('response.leftButton', _mouseButtons[0]);
    psychoJS.experiment.addData('response.midButton', _mouseButtons[1]);
    psychoJS.experiment.addData('response.rightButton', _mouseButtons[2]);
    if (response.clicked_name.length > 0) {
      psychoJS.experiment.addData('response.clicked_name', response.clicked_name[0]);}
    // the Routine "Trials" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    return Scheduler.Event.NEXT;
  };
}


var FeedbackComponents;
function FeedbackRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //------Prepare to start Routine 'Feedback'-------
    t = 0;
    FeedbackClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    routineTimer.add(1.000000);
    // update component parameters for each repeat
    if ((corr === 1)) {
        msg = "Correct! ";
    } else {
        msg = "Incorrect";
    }
    
    feedback_text.setText(msg);
    // keep track of which components have finished
    FeedbackComponents = [];
    FeedbackComponents.push(feedback_text);
    
    for (const thisComponent of FeedbackComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function FeedbackRoutineEachFrame() {
  return async function () {
    //------Loop for each frame of Routine 'Feedback'-------
    // get current time
    t = FeedbackClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *feedback_text* updates
    if (t >= 0 && feedback_text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      feedback_text.tStart = t;  // (not accounting for frame time here)
      feedback_text.frameNStart = frameN;  // exact frame index
      
      feedback_text.setAutoDraw(true);
    }

    frameRemains = 0 + 1.0 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
    if (feedback_text.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      feedback_text.setAutoDraw(false);
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
    for (const thisComponent of FeedbackComponents)
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


function FeedbackRoutineEnd() {
  return async function () {
    //------Ending Routine 'Feedback'-------
    for (const thisComponent of FeedbackComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    if ((trials.thisTrialN === 6)) {
        trials.finished = true;
    }
    
    return Scheduler.Event.NEXT;
  };
}


var EndComponents;
function EndRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //------Prepare to start Routine 'End'-------
    t = 0;
    EndClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    routineTimer.add(3.000000);
    // update component parameters for each repeat
    // keep track of which components have finished
    EndComponents = [];
    EndComponents.push(thank_you);
    
    for (const thisComponent of EndComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function EndRoutineEachFrame() {
  return async function () {
    //------Loop for each frame of Routine 'End'-------
    // get current time
    t = EndClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *thank_you* updates
    if (t >= 0.0 && thank_you.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      thank_you.tStart = t;  // (not accounting for frame time here)
      thank_you.frameNStart = frameN;  // exact frame index
      
      thank_you.setAutoDraw(true);
    }

    frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
    if (thank_you.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      thank_you.setAutoDraw(false);
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
    for (const thisComponent of EndComponents)
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


function EndRoutineEnd() {
  return async function () {
    //------Ending Routine 'End'-------
    for (const thisComponent of EndComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    return Scheduler.Event.NEXT;
  };
}


function endLoopIteration(scheduler, snapshot) {
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
