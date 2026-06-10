# Cyberball — PsychoJS (Online)

> **Parent**: [psy-exp-coder](../../SKILL.md) · [jsPsych/JavaScript Index](index.md)
> **Config reference**: [cyberball](../../../psy-exp-designer/paradigms/cyberball.md)
> **Source**: [Pavlovia demos/cyberball](https://gitlab.pavlovia.org/demos/cyberball) · PsychoJS (PsychoPy online export)
> **Platform note**: This is PsychoJS code (PsychoPy's JavaScript runtime for online experiments), NOT jsPsych library code.

## Experiment Logic

Cyberball is a virtual ball-tossing game used to study social exclusion and ostracism. The participant believes they are playing catch online with two other players, but the other players' throws are actually pre-programmed. The key manipulation is whether the participant receives the ball equally often (inclusion condition) or rarely (exclusion condition).

The experiment begins with instructions and a pre-game mood survey. The main task consists of blocks of ball-tossing trials. Three player icons (including the participant at the bottom) are displayed on screen, and a ball image moves between players to simulate throws. The participant clicks on a player icon to throw them the ball.

The task flow is controlled by condition files (`blocks.xlsx`, `equal_throws.xlsx`, `exclusion.xlsx`) that specify each throw: who throws to whom. The participant's own throws (clicking a player) are collected via mouse input. After all throws in a block, the game pauses, and post-block surveys may appear.

The mood survey uses PsychoPy's survey library (JSON-based questionnaire). Player icons and ball images are preloaded as resources. The experiment concludes with a goodbye screen. Data collected includes throw patterns, click locations, reaction times, and survey responses. The primary dependent measure is the change in mood/need-satisfaction scores between pre- and post-game surveys.

## Key Design Patterns

- **Deception paradigm**: pre-programmed throw sequences simulate other players' behavior to manipulate perceived inclusion/exclusion
- **Survey library integration**: mood questionnaire loaded from JSON (`survey_d873dd7b-f146-4baa-9be7-d0b5d5301dd2.json`) via `{'surveyLibrary': true}` resource
- **Mouse-driven interaction**: participant throws the ball by clicking on player icons, with `eventManager.getMousePos()` tracking cursor position
- **Multi-block design**: `blocks` outer loop iterates over game phases (equal throws block, exclusion block), each with separate condition files
- **Player positioning**: three `visual.ImageStim` elements (player1, player2, player3) arranged around the screen with ball image animated between them
- **Pre-post survey design**: mood survey before the game and after each block to measure social exclusion effects

## Code Example

```javascript
// Source: cyberball (demos/cyberball)
// Project URL: https://gitlab.pavlovia.org/demos/cyberball
// Original file: cyberball.js
﻿/****************** 
 * Cyberball *
 ******************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2025.1.0.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'cyberball';  // from the Builder filename that created this script
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
  fullscr: true,
  color: new util.Color([1, 1, 1]),
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
flowScheduler.add(mood_surveyRoutineBegin());
flowScheduler.add(mood_surveyRoutineEachFrame());
flowScheduler.add(mood_surveyRoutineEnd());
const blocksLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(blocksLoopBegin(blocksLoopScheduler));
flowScheduler.add(blocksLoopScheduler);
flowScheduler.add(blocksLoopEnd);







flowScheduler.add(goodbyeRoutineBegin());
flowScheduler.add(goodbyeRoutineEachFrame());
flowScheduler.add(goodbyeRoutineEnd());
flowScheduler.add(quitPsychoJS, 'Thank you for your patience.', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, 'Thank you for your patience.', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    // libraries:
    {'surveyLibrary': true},
    // resources:
    {'name': 'spreadsheets/blocks.xlsx', 'path': 'spreadsheets/blocks.xlsx'},
    {'name': 'spreadsheets/equal_throws.xlsx', 'path': 'spreadsheets/equal_throws.xlsx'},
    {'name': 'spreadsheets/exclusion.xlsx', 'path': 'spreadsheets/exclusion.xlsx'},
    {'name': 'survey_d873dd7b-f146-4baa-9be7-d0b5d5301dd2.json', 'path': 'survey_d873dd7b-f146-4baa-9be7-d0b5d5301dd2.json'},
    {'name': 'images/player3.png', 'path': 'images/player3.png'},
    {'name': 'images/player1.png', 'path': 'images/player1.png'},
    {'name': 'images/player2.png', 'path': 'images/player2.png'},
    {'name': 'images/ball.png', 'path': 'images/ball.png'},
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.INFO);


var currentLoop;
var frameDur;
async function updateInfo() {
  currentLoop = psychoJS.experiment;  // right now there are no loops
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2025.1.0dev167';
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
var instructtxt;
var start_button;
var instructions_2Clock;
var instructtxt_2;
var start_button_2;
var trialClock;
var player3image;
var player1image;
var player2image;
var mouse;
var player_1_ball_count;
var player_2_ball_count;
var player_3_ball_count;
var instructtxtbox;
var player1ball_counttxt;
var player2ball_counttxt;
var player3ball_counttxt;
var ballimage;
var ball_moveClock;
var player3image_2;
var player1image_2;
var player2image_2;
var instructtxtbox_2;
var player1ball_counttxt_2;
var player2ball_counttxt_2;
var player3ball_counttxt_2;
var ballimage_2;
var goodbyeClock;
var instructtxt_3;
var start_button_3;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "instructions"
  instructionsClock = new util.Clock();
  instructtxt = new visual.TextBox({
    win: psychoJS.window,
    name: 'instructtxt',
    text: 'Thank you for participating! In this task, you\'ll play a virtual ball-tossing game with two other players. Here’s what to do:\n\nGame Start: You’ll see three players, including yourself.\nThrow the Ball: When you get the ball, click on a player to throw it to them.\n\nGameplay: Watch as the ball is tossed. You may receive it often or not at all at times.\n\nDuration: The game lasts a few minutes, followed by a short questionnaire.\n\nNote: The game simulates social interactions. Please focus on tossing and catching the ball. Your responses are confidential. If you have questions, ask the researcher before starting.\n\nClick "Start" when you\'re ready!',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.03,
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
    depth: 0.0 
  });
  
  start_button = new visual.ButtonStim({
    win: psychoJS.window,
    name: 'start_button',
    text: 'START',
    fillColor: 'darkgrey',
    borderColor: null,
    color: 'white',
    colorSpace: 'rgb',
    pos: [0, (- 0.4)],
    letterHeight: 0.05,
    size: [0.5, 0.1],
    ori: 0.0
    ,
    depth: -1
  });
  start_button.clock = new util.Clock();
  
  // Initialize components for Routine "instructions_2"
  instructions_2Clock = new util.Clock();
  instructtxt_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'instructtxt_2',
    text: 'Are you ready? \n\nIn a moment you, and the other players, will get to choose who to toss a ball to. If you are chosen to toss the ball click on the player you want to toss the ball to.\n\nClick "Start" when you\'re ready!',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.03,
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
    depth: 0.0 
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
    size: [0.5, 0.1],
    ori: 0.0
    ,
    depth: -1
  });
  start_button_2.clock = new util.Clock();
  
  // Initialize components for Routine "trial"
  trialClock = new util.Clock();
  player3image = new visual.ImageStim({
    win : psychoJS.window,
    name : 'player3image', units : undefined, 
    image : 'images/player3.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, (- 0.3)], 
    draggable: false,
    size : [0.2, 0.2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  player1image = new visual.ImageStim({
    win : psychoJS.window,
    name : 'player1image', units : undefined, 
    image : 'images/player1.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [(- 0.5), 0.3], 
    draggable: false,
    size : [0.2, 0.2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -1.0 
  });
  player2image = new visual.ImageStim({
    win : psychoJS.window,
    name : 'player2image', units : undefined, 
    image : 'images/player2.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0.5, 0.3], 
    draggable: false,
    size : [0.2, 0.2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -2.0 
  });
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  // Run 'Begin Experiment' code from set_paths
  player_1_ball_count = 0;
  player_2_ball_count = 0;
  player_3_ball_count = 0;
  
  instructtxtbox = new visual.TextBox({
    win: psychoJS.window,
    name: 'instructtxtbox',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.03,
    lineSpacing: 1.0,
    size: [1.5, 0.5],  units: undefined, 
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
    depth: -5.0 
  });
  
  player1ball_counttxt = new visual.TextBox({
    win: psychoJS.window,
    name: 'player1ball_counttxt',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [(- 0.5), 0.45], 
    draggable: false,
    letterHeight: 0.03,
    lineSpacing: 1.0,
    size: [0.5, 0.05],  units: undefined, 
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
    depth: -6.0 
  });
  
  player2ball_counttxt = new visual.TextBox({
    win: psychoJS.window,
    name: 'player2ball_counttxt',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0.5, 0.45], 
    draggable: false,
    letterHeight: 0.03,
    lineSpacing: 1.0,
    size: [0.5, 0.05],  units: undefined, 
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
    depth: -7.0 
  });
  
  player3ball_counttxt = new visual.TextBox({
    win: psychoJS.window,
    name: 'player3ball_counttxt',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, (- 0.15)], 
    draggable: false,
    letterHeight: 0.03,
    lineSpacing: 1.0,
    size: [0.5, 0.05],  units: undefined, 
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
    depth: -8.0 
  });
  
  ballimage = new visual.ImageStim({
    win : psychoJS.window,
    name : 'ballimage', units : undefined, 
    image : 'images/ball.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [0.1, 0.1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -9.0 
  });
  // Initialize components for Routine "ball_move"
  ball_moveClock = new util.Clock();
  player3image_2 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'player3image_2', units : undefined, 
    image : 'images/player3.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, (- 0.3)], 
    draggable: false,
    size : [0.2, 0.2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -1.0 
  });
  player1image_2 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'player1image_2', units : undefined, 
    image : 'images/player1.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [(- 0.5), 0.3], 
    draggable: false,
    size : [0.2, 0.2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -2.0 
  });
  player2image_2 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'player2image_2', units : undefined, 
    image : 'images/player2.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0.5, 0.3], 
    draggable: false,
    size : [0.2, 0.2],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -3.0 
  });
  instructtxtbox_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'instructtxtbox_2',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.03,
    lineSpacing: 1.0,
    size: [1.5, 0.5],  units: undefined, 
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
    depth: -4.0 
  });
  
  player1ball_counttxt_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'player1ball_counttxt_2',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [(- 0.5), 0.45], 
    draggable: false,
    letterHeight: 0.03,
    lineSpacing: 1.0,
    size: [0.5, 0.05],  units: undefined, 
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
    depth: -5.0 
  });
  
  player2ball_counttxt_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'player2ball_counttxt_2',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0.5, 0.45], 
    draggable: false,
    letterHeight: 0.03,
    lineSpacing: 1.0,
    size: [0.5, 0.05],  units: undefined, 
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
    depth: -6.0 
  });
  
  player3ball_counttxt_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'player3ball_counttxt_2',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, (- 0.15)], 
    draggable: false,
    letterHeight: 0.03,
    lineSpacing: 1.0,
    size: [0.5, 0.05],  units: undefined, 
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
    depth: -7.0 
  });
  
  ballimage_2 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'ballimage_2', units : undefined, 
    image : 'images/ball.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [0.1, 0.1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -8.0 
  });
  // Initialize components for Routine "goodbye"
  goodbyeClock = new util.Clock();
  instructtxt_3 = new visual.TextBox({
    win: psychoJS.window,
    name: 'instructtxt_3',
    text: 'Thank you for participating in this demonstration of the Cyberball task.\n\nFeel free to adapt this demo for your own research!',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.03,
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
    depth: 0.0 
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
    size: [0.5, 0.1],
    ori: 0.0
    ,
    depth: -1
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
    instructionsComponents.push(instructtxt);
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
    
    // *instructtxt* updates
    if (t >= 0.0 && instructtxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instructtxt.tStart = t;  // (not accounting for frame time here)
      instructtxt.frameNStart = frameN;  // exact frame index
      
      instructtxt.setAutoDraw(true);
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


var mood_survey;
var mood_surveyClock;
function mood_surveyRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'mood_survey' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    //--- Starting Routine 'mood_survey' ---
    mood_survey = new visual.Survey({
        win: psychoJS.window,
        name: 'mood_survey',
        model: 'survey_d873dd7b-f146-4baa-9be7-d0b5d5301dd2.json',
    });
    mood_surveyClock = new util.Clock();
    mood_survey.setAutoDraw(true);
    mood_survey.status = PsychoJS.Status.STARTED;
    mood_survey.isFinished = false;
    mood_survey.tStart = t;  // (not accounting for frame time here)
    mood_survey.frameNStart = frameN;  // exact frame index
    return Scheduler.Event.NEXT;
  }
}


function mood_surveyRoutineEachFrame() {
  return async function () {
    t = mood_surveyClock.getTime();
    frameN = frameN + 1;  // number of completed frames (so 0 is the first frame)
    // if mood_survey is completed, move on
    if (mood_survey.isFinished) {
      mood_survey.setAutoDraw(false);
      mood_survey.status = PsychoJS.Status.FINISHED;
      // survey routines are not non-slip safe, so reset the non-slip timer
      routineTimer.reset();
      return Scheduler.Event.NEXT;
    }
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    return Scheduler.Event.FLIP_REPEAT;
  }
}


function mood_surveyRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'mood_survey' ---
    // get data from mood_survey
    const mood_surveyResponse =  mood_survey.getResponse();
    function addRecursively(resp, name) {
        if (resp.constructor === Object) {
            // if resp is an object, add each part as a column
            for (let subquestion in resp) {
                addRecursively(resp[subquestion], `${name}.${subquestion}`);
            }
        } else {
            psychoJS.experiment.addData(name, resp);
        }
    }
    // recursively add survey responses
    addRecursively(mood_surveyResponse, 'mood_survey');
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var blocks;
function blocksLoopBegin(blocksLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    blocks = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 1, method: TrialHandler.Method.SEQUENTIAL,
      extraInfo: expInfo, originPath: undefined,
      trialList: 'spreadsheets/blocks.xlsx',
      seed: undefined, name: 'blocks'
    });
    psychoJS.experiment.addLoop(blocks); // add the loop to the experiment
    currentLoop = blocks;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisBlock of blocks) {
      snapshot = blocks.getSnapshot();
      blocksLoopScheduler.add(importConditions(snapshot));
      blocksLoopScheduler.add(instructions_2RoutineBegin(snapshot));
      blocksLoopScheduler.add(instructions_2RoutineEachFrame());
      blocksLoopScheduler.add(instructions_2RoutineEnd(snapshot));
      const trialsLoopScheduler = new Scheduler(psychoJS);
      blocksLoopScheduler.add(trialsLoopBegin(trialsLoopScheduler, snapshot));
      blocksLoopScheduler.add(trialsLoopScheduler);
      blocksLoopScheduler.add(trialsLoopEnd);
      blocksLoopScheduler.add(mood_surveyRoutineBegin(snapshot));
      blocksLoopScheduler.add(mood_surveyRoutineEachFrame());
      blocksLoopScheduler.add(mood_surveyRoutineEnd(snapshot));
      blocksLoopScheduler.add(blocksLoopEndIteration(blocksLoopScheduler, snapshot));
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
      trialList: this_sheet,
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
      trialsLoopScheduler.add(ball_moveRoutineBegin(snapshot));
      trialsLoopScheduler.add(ball_moveRoutineEachFrame());
      trialsLoopScheduler.add(ball_moveRoutineEnd(snapshot));
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


async function blocksLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(blocks);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function blocksLoopEndIteration(scheduler, snapshot) {
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
    instructions_2Components.push(instructtxt_2);
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
    
    // *instructtxt_2* updates
    if (t >= 0.0 && instructtxt_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instructtxt_2.tStart = t;  // (not accounting for frame time here)
      instructtxt_2.frameNStart = frameN;  // exact frame index
      
      instructtxt_2.setAutoDraw(true);
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
    trialClock.reset();
    routineTimer.reset();
    trialMaxDurationReached = false;
    // update component parameters for each repeat
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
    instructtxtbox.setText(instruct);
    player1ball_counttxt.setText(("Balls received: " + player_1_ball_count.toString()));
    player2ball_counttxt.setText(("Balls received: " + player_2_ball_count.toString()));
    player3ball_counttxt.setText(("Balls received: " + player_3_ball_count.toString()));
    ballimage.setPos([ball_start_x, ball_start_y]);
    psychoJS.experiment.addData('trial.started', globalClock.getTime());
    trialMaxDuration = null
    // keep track of which components have finished
    trialComponents = [];
    trialComponents.push(player3image);
    trialComponents.push(player1image);
    trialComponents.push(player2image);
    trialComponents.push(mouse);
    trialComponents.push(instructtxtbox);
    trialComponents.push(player1ball_counttxt);
    trialComponents.push(player2ball_counttxt);
    trialComponents.push(player3ball_counttxt);
    trialComponents.push(ballimage);
    
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
    
    // *player3image* updates
    if (t >= 0.0 && player3image.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player3image.tStart = t;  // (not accounting for frame time here)
      player3image.frameNStart = frameN;  // exact frame index
      
      player3image.setAutoDraw(true);
    }
    
    
    // *player1image* updates
    if (t >= 0.0 && player1image.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player1image.tStart = t;  // (not accounting for frame time here)
      player1image.frameNStart = frameN;  // exact frame index
      
      player1image.setAutoDraw(true);
    }
    
    
    // *player2image* updates
    if (t >= 0.0 && player2image.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player2image.tStart = t;  // (not accounting for frame time here)
      player2image.frameNStart = frameN;  // exact frame index
      
      player2image.setAutoDraw(true);
    }
    
    // *mouse* updates
    if (((ball_to == 'choose')) && mouse.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      mouse.tStart = t;  // (not accounting for frame time here)
      mouse.frameNStart = frameN;  // exact frame index
      
      mouse.status = PsychoJS.Status.STARTED;
      mouse.mouseClock.reset();
      prevButtonState = mouse.getPressed();  // if button is down already this ISN'T a new click
    }
    
    // if mouse is active this frame...
    if (mouse.status == PsychoJS.Status.STARTED) {
      _mouseButtons = mouse.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          mouse.clickableObjects = [player1image, player2image]
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
          if (gotValidClick === true) { 
            _mouseXYs = mouse.getPos();
            mouse.x.push(_mouseXYs[0]);
            mouse.y.push(_mouseXYs[1]);
            mouse.leftButton.push(_mouseButtons[0]);
            mouse.midButton.push(_mouseButtons[1]);
            mouse.rightButton.push(_mouseButtons[2]);
            mouse.time.push(mouse.mouseClock.getTime());
          }
          if (gotValidClick === true) { // end routine on response
            continueRoutine = false;
          }
        }
      }
    }
    // Run 'Each Frame' code from set_paths
    if (((ball_to !== "choose") && (t > 1))) {
        continueRoutine = false;
    }
    
    
    // *instructtxtbox* updates
    if (t >= 0.0 && instructtxtbox.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instructtxtbox.tStart = t;  // (not accounting for frame time here)
      instructtxtbox.frameNStart = frameN;  // exact frame index
      
      instructtxtbox.setAutoDraw(true);
    }
    
    
    // *player1ball_counttxt* updates
    if (t >= 0.0 && player1ball_counttxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player1ball_counttxt.tStart = t;  // (not accounting for frame time here)
      player1ball_counttxt.frameNStart = frameN;  // exact frame index
      
      player1ball_counttxt.setAutoDraw(true);
    }
    
    
    // *player2ball_counttxt* updates
    if (t >= 0.0 && player2ball_counttxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player2ball_counttxt.tStart = t;  // (not accounting for frame time here)
      player2ball_counttxt.frameNStart = frameN;  // exact frame index
      
      player2ball_counttxt.setAutoDraw(true);
    }
    
    
    // *player3ball_counttxt* updates
    if (t >= 0.0 && player3ball_counttxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player3ball_counttxt.tStart = t;  // (not accounting for frame time here)
      player3ball_counttxt.frameNStart = frameN;  // exact frame index
      
      player3ball_counttxt.setAutoDraw(true);
    }
    
    
    // *ballimage* updates
    if (t >= 0.0 && ballimage.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      ballimage.tStart = t;  // (not accounting for frame time here)
      ballimage.frameNStart = frameN;  // exact frame index
      
      ballimage.setAutoDraw(true);
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


var start_pos;
var outcome_txt;
var ball_thrown_to;
var end_pos;
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
    
    // Run 'End Routine' code from set_paths
    start_pos = [ball_start_x, ball_start_y];
    outcome_txt = "";
    ball_thrown_to = null;
    if ((ball_to === "choose")) {
        if ((mouse.clicked_name.slice((- 1))[0] === "player1image")) {
            end_pos = player1image.pos;
            outcome_txt = "You chose Player 1";
            player_1_ball_count += 1;
        } else {
            end_pos = player2image.pos;
            outcome_txt = "You chose Player 2";
            player_2_ball_count += 1;
        }
    } else {
        if ((ball_to === "player1")) {
            end_pos = player1image.pos;
            outcome_txt = "Player 2 chose Player 1";
            player_1_ball_count += 1;
        } else {
            if ((ball_to === "player2")) {
                end_pos = player2image.pos;
                outcome_txt = "Player 1 chose Player 2";
                player_2_ball_count += 1;
            } else {
                if (((ball_from === "player1") && (ball_to === "player3"))) {
                    end_pos = player3image.pos;
                    outcome_txt = "Player 1 chose you";
                    player_3_ball_count += 1;
                } else {
                    if (((ball_from === "player2") && (ball_to === "player3"))) {
                        end_pos = player3image.pos;
                        outcome_txt = "Player 2 chose you";
                        player_3_ball_count += 1;
                    }
                }
            }
        }
    }
    psychoJS.experiment.addData("player_1_ball_count ", player_1_ball_count);
    psychoJS.experiment.addData("player_2_ball_count ", player_2_ball_count);
    psychoJS.experiment.addData("player_3_ball_count ", player_3_ball_count);
    
    // the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var ball_moveMaxDurationReached;
var ball_moveMaxDuration;
var ball_moveComponents;
function ball_moveRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'ball_move' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    ball_moveClock.reset(routineTimer.getTime());
    routineTimer.add(3.000000);
    ball_moveMaxDurationReached = false;
    // update component parameters for each repeat
    instructtxtbox_2.setText(outcome_txt);
    player1ball_counttxt_2.setText(("Balls received: " + player_1_ball_count.toString()));
    player2ball_counttxt_2.setText(("Balls received: " + player_2_ball_count.toString()));
    player3ball_counttxt_2.setText(("Balls received: " + player_3_ball_count.toString()));
    ballimage_2.setPos([ball_start_x, ball_start_y]);
    psychoJS.experiment.addData('ball_move.started', globalClock.getTime());
    ball_moveMaxDuration = null
    // keep track of which components have finished
    ball_moveComponents = [];
    ball_moveComponents.push(player3image_2);
    ball_moveComponents.push(player1image_2);
    ball_moveComponents.push(player2image_2);
    ball_moveComponents.push(instructtxtbox_2);
    ball_moveComponents.push(player1ball_counttxt_2);
    ball_moveComponents.push(player2ball_counttxt_2);
    ball_moveComponents.push(player3ball_counttxt_2);
    ball_moveComponents.push(ballimage_2);
    
    for (const thisComponent of ball_moveComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var total_time;
var x;
var y;
var frameRemains;
function ball_moveRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'ball_move' ---
    // get current time
    t = ball_moveClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    // Run 'Each Frame' code from code
    total_time = 3;
    x = (start_pos[0] + (((end_pos[0] - start_pos[0]) / total_time) * t));
    y = (start_pos[1] + (((end_pos[1] - start_pos[1]) / total_time) * t));
    ballimage_2.setPos([x, (y - 0.1)]);
    
    
    // *player3image_2* updates
    if (t >= 0.0 && player3image_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player3image_2.tStart = t;  // (not accounting for frame time here)
      player3image_2.frameNStart = frameN;  // exact frame index
      
      player3image_2.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (player3image_2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      player3image_2.tStop = t;  // not accounting for scr refresh
      player3image_2.frameNStop = frameN;  // exact frame index
      // update status
      player3image_2.status = PsychoJS.Status.FINISHED;
      player3image_2.setAutoDraw(false);
    }
    
    
    // *player1image_2* updates
    if (t >= 0.0 && player1image_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player1image_2.tStart = t;  // (not accounting for frame time here)
      player1image_2.frameNStart = frameN;  // exact frame index
      
      player1image_2.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (player1image_2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      player1image_2.tStop = t;  // not accounting for scr refresh
      player1image_2.frameNStop = frameN;  // exact frame index
      // update status
      player1image_2.status = PsychoJS.Status.FINISHED;
      player1image_2.setAutoDraw(false);
    }
    
    
    // *player2image_2* updates
    if (t >= 0.0 && player2image_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player2image_2.tStart = t;  // (not accounting for frame time here)
      player2image_2.frameNStart = frameN;  // exact frame index
      
      player2image_2.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (player2image_2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      player2image_2.tStop = t;  // not accounting for scr refresh
      player2image_2.frameNStop = frameN;  // exact frame index
      // update status
      player2image_2.status = PsychoJS.Status.FINISHED;
      player2image_2.setAutoDraw(false);
    }
    
    
    // *instructtxtbox_2* updates
    if (t >= 0.0 && instructtxtbox_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instructtxtbox_2.tStart = t;  // (not accounting for frame time here)
      instructtxtbox_2.frameNStart = frameN;  // exact frame index
      
      instructtxtbox_2.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (instructtxtbox_2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      instructtxtbox_2.tStop = t;  // not accounting for scr refresh
      instructtxtbox_2.frameNStop = frameN;  // exact frame index
      // update status
      instructtxtbox_2.status = PsychoJS.Status.FINISHED;
      instructtxtbox_2.setAutoDraw(false);
    }
    
    
    // *player1ball_counttxt_2* updates
    if (t >= 0.0 && player1ball_counttxt_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player1ball_counttxt_2.tStart = t;  // (not accounting for frame time here)
      player1ball_counttxt_2.frameNStart = frameN;  // exact frame index
      
      player1ball_counttxt_2.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (player1ball_counttxt_2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      player1ball_counttxt_2.tStop = t;  // not accounting for scr refresh
      player1ball_counttxt_2.frameNStop = frameN;  // exact frame index
      // update status
      player1ball_counttxt_2.status = PsychoJS.Status.FINISHED;
      player1ball_counttxt_2.setAutoDraw(false);
    }
    
    
    // *player2ball_counttxt_2* updates
    if (t >= 0.0 && player2ball_counttxt_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player2ball_counttxt_2.tStart = t;  // (not accounting for frame time here)
      player2ball_counttxt_2.frameNStart = frameN;  // exact frame index
      
      player2ball_counttxt_2.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (player2ball_counttxt_2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      player2ball_counttxt_2.tStop = t;  // not accounting for scr refresh
      player2ball_counttxt_2.frameNStop = frameN;  // exact frame index
      // update status
      player2ball_counttxt_2.status = PsychoJS.Status.FINISHED;
      player2ball_counttxt_2.setAutoDraw(false);
    }
    
    
    // *player3ball_counttxt_2* updates
    if (t >= 0.0 && player3ball_counttxt_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      player3ball_counttxt_2.tStart = t;  // (not accounting for frame time here)
      player3ball_counttxt_2.frameNStart = frameN;  // exact frame index
      
      player3ball_counttxt_2.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (player3ball_counttxt_2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      player3ball_counttxt_2.tStop = t;  // not accounting for scr refresh
      player3ball_counttxt_2.frameNStop = frameN;  // exact frame index
      // update status
      player3ball_counttxt_2.status = PsychoJS.Status.FINISHED;
      player3ball_counttxt_2.setAutoDraw(false);
    }
    
    
    // *ballimage_2* updates
    if (t >= 0.0 && ballimage_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      ballimage_2.tStart = t;  // (not accounting for frame time here)
      ballimage_2.frameNStart = frameN;  // exact frame index
      
      ballimage_2.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (ballimage_2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      ballimage_2.tStop = t;  // not accounting for scr refresh
      ballimage_2.frameNStop = frameN;  // exact frame index
      // update status
      ballimage_2.status = PsychoJS.Status.FINISHED;
      ballimage_2.setAutoDraw(false);
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
    for (const thisComponent of ball_moveComponents)
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


function ball_moveRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'ball_move' ---
    for (const thisComponent of ball_moveComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('ball_move.stopped', globalClock.getTime());
    if (ball_moveMaxDurationReached) {
        ball_moveClock.add(ball_moveMaxDuration);
    } else {
        ball_moveClock.add(3.000000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var goodbyeMaxDurationReached;
var goodbyeMaxDuration;
var goodbyeComponents;
function goodbyeRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'goodbye' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    goodbyeClock.reset();
    routineTimer.reset();
    goodbyeMaxDurationReached = false;
    // update component parameters for each repeat
    // reset start_button_3 to account for continued clicks & clear times on/off
    start_button_3.reset()
    psychoJS.experiment.addData('goodbye.started', globalClock.getTime());
    goodbyeMaxDuration = null
    // keep track of which components have finished
    goodbyeComponents = [];
    goodbyeComponents.push(instructtxt_3);
    goodbyeComponents.push(start_button_3);
    
    for (const thisComponent of goodbyeComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function goodbyeRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'goodbye' ---
    // get current time
    t = goodbyeClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *instructtxt_3* updates
    if (t >= 0.0 && instructtxt_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instructtxt_3.tStart = t;  // (not accounting for frame time here)
      instructtxt_3.frameNStart = frameN;  // exact frame index
      
      instructtxt_3.setAutoDraw(true);
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
    for (const thisComponent of goodbyeComponents)
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


function goodbyeRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'goodbye' ---
    for (const thisComponent of goodbyeComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('goodbye.stopped', globalClock.getTime());
    psychoJS.experiment.addData('start_button_3.numClicks', start_button_3.numClicks);
    psychoJS.experiment.addData('start_button_3.timesOn', start_button_3.timesOn);
    psychoJS.experiment.addData('start_button_3.timesOff', start_button_3.timesOff);
    // the Routine "goodbye" was not non-slip safe, so reset the non-slip timer
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

```
