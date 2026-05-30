// Source: drag_and_drop (demos/drag_and_drop)
// Project URL: https://gitlab.pavlovia.org/demos/drag_and_drop
// Original file: dragAndDrop.js
﻿/******************** 
 * Draganddrop Test *
 ********************/

import { core, data, sound, util, visual } from './lib/psychojs-2021.2.3.js';
const { PsychoJS } = core;
const { TrialHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'dragAndDrop';  // from the Builder filename that created this script
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
  units: 'pix',
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
flowScheduler.add(InstructionsRoutineRoutineBegin());
flowScheduler.add(InstructionsRoutineRoutineEachFrame());
flowScheduler.add(InstructionsRoutineRoutineEnd());
const trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trialsLoopBegin(trialsLoopScheduler));
flowScheduler.add(trialsLoopScheduler);
flowScheduler.add(trialsLoopEnd);
flowScheduler.add(quitPsychoJS, '', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, '', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    {'name': 'design_92.png', 'path': 'design_92.png'},
    {'name': 'white.png', 'path': 'white.png'},
    {'name': 'design_91.png', 'path': 'design_91.png'},
    {'name': 'conditions.xlsx', 'path': 'conditions.xlsx'},
    {'name': 'design_41.png', 'path': 'design_41.png'},
    {'name': 'design_43.png', 'path': 'design_43.png'},
    {'name': 'design_93.png', 'path': 'design_93.png'},
    {'name': 'design_42.png', 'path': 'design_42.png'},
    {'name': 'black.png', 'path': 'black.png'},
    {'name': 'continueButton.png', 'path': 'continueButton.png'}
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.EXP);


var frameDur;
async function updateInfo() {
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2021.2.3';
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


var InstructionsRoutineClock;
var introText;
var start;
var startMouse;
var designAClock;
var masterPatternA;
var key_resp;
var polygon;
var whitePiece;
var blackPiece;
var mouse;
var createPiece;
var drawPicked;
var movePicked;
var createGrid;
var drawGrid;
var checkAnswer;
var picNameDict;
var end;
var resultClock;
var resultAccuracy;
var resultTextA;
var endFB;
var trialEnd;
var endTrialMouse;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "InstructionsRoutine"
  InstructionsRoutineClock = new util.Clock();
  introText = new visual.TextStim({
    win: psychoJS.window,
    name: 'introText',
    text: 'This task shows you the drag and drop capabilities of PsychoPy and PsychoJS.\n\nThe demonstration uses a drag and drop puzzle game. \nThe task requires you to drag and drop the black and white\npieces into the empty square, in order to match the \npuzzle design above.\n\nWhen you have finished, press the "END" button to \nsee whether or not you were correct, and how long the\nthe trial took.\n\nClick or tap continue to begin.',
    font: 'Arial',
    units: 'pix', 
    pos: [0, 0], height: 25,  wrapWidth: 800, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: 0.0 
  });
  
  start = new visual.ImageStim({
    win : psychoJS.window,
    name : 'start', units : 'pix', 
    image : 'continueButton.png', mask : undefined,
    ori : 0, pos : [0, (- 350)], size : [110, 40],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -1.0 
  });
  startMouse = new core.Mouse({
    win: psychoJS.window,
  });
  startMouse.mouseClock = new util.Clock();
  // Initialize components for Routine "designA"
  designAClock = new util.Clock();
  masterPatternA = new visual.ImageStim({
    win : psychoJS.window,
    name : 'masterPatternA', units : undefined, 
    image : undefined, mask : undefined,
    ori : 0, pos : [0, 200], size : 1.0,
    color : new util.Color([1.0, 1.0, 1.0]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 512, interpolate : true, depth : 0.0 
  });
  key_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  polygon = new visual.Rect ({
    win: psychoJS.window, name: 'polygon', units : 'pix', 
    width: [1.0, 1.0][0], height: [1.0, 1.0][1],
    ori: 0, pos: [0, (- 100)],
    lineWidth: 1, lineColor: new util.Color([1, 1, 1]),
    fillColor: new util.Color([0, 0, 0]),
    opacity: 1, depth: -2, interpolate: true,
  });
  
  whitePiece = new visual.ImageStim({
    win : psychoJS.window,
    name : 'whitePiece', units : undefined, 
    image : 'white.png', mask : undefined,
    ori : 0, pos : [0, 0], size : 1.0,
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -3.0 
  });
  blackPiece = new visual.ImageStim({
    win : psychoJS.window,
    name : 'blackPiece', units : undefined, 
    image : 'black.png', mask : undefined,
    ori : 0, pos : [0, 0], size : 1.0,
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -4.0 
  });
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  createPiece = function(piece, pos, name){
    return new visual.ImageStim({win : psychoJS.window,
                                  image: piece.image, 
                                  name: name,
                                  size: piece.size, 
                                  pos: pos})
  }
  
  drawPicked = function(picked, draw) {
    if (picked.length > 0) {
      for(let each of picked) {
        each.autoDraw = draw;
      }
    }
  }
  
  movePicked = function(picked, mouse, grabbed) {
    if (grabbed != 'undefined' &&  mouse.getPressed()[0] === 1) {
      grabbed.pos = mouse.getPos();
      return grabbed
    } else {
        for (let piece of picked) {
          if (piece.contains(mouse) &&  mouse.getPressed()[0] === 1 && grabbed === 'undefined'){
            piece.pos = mouse.getPos();
            return piece;
          }
        }
     return 'undefined'
    }
  }
  
  createGrid = function(rows, size, pos, names) {
      var inc = (size/rows);
      var rowStart = pos[0] - size/2;
      var colStart = pos[1] + size/2;
      var row = rowStart  + inc/2;
      var col = colStart - inc/2;
      var counter = 0;
      var grid = [];
      
      for (let i = 0; i < rows; i++) {
          for (let j = 0; j < rows; j++) {
              grid.push(new visual.Rect({win : psychoJS.window,
                                          name: names[counter], 
                                          units: 'pix',
                                          lineColor: new util.Color([1,1,0]),
                                          size: [size/rows, size/rows], 
                                          pos: [row,col]}))
              row += inc
              counter += 1
          }
          col -= inc
          row = rowStart + inc/2
      }
      return grid
  }
  
  
  drawGrid = function(grid, draw) {
      for (let i of grid) {
          i.autoDraw = draw;
      }
  }
  
  checkAnswer = function(grid, pieces) {
      var picNames = pieces.map((pic) => pic.name)
      var correctPieces = []
      for (let cell of grid) {
          if (picNames.includes(cell.name)) {
              for (let name = 0; name < picNames.length; name++) {
                  if (cell.name === picNames[name]) {
                      if (cell.contains(pieces[name])) {
                          correctPieces.push(true)
                          break
                      }
                  }
              }
          } else {
              return false
          }
      }
      return correctPieces.length === grid.length
  } 
  
  picNameDict = {whitePiece: "white.png",
                 blackPiece: "black.png"}
  end = new visual.ImageStim({
    win : psychoJS.window,
    name : 'end', units : 'pix', 
    image : 'continueButton.png', mask : undefined,
    ori : 0, pos : [0, (- 350)], size : [110, 40],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -7.0 
  });
  // Initialize components for Routine "result"
  resultClock = new util.Clock();
  resultAccuracy = new visual.TextStim({
    win: psychoJS.window,
    name: 'resultAccuracy',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 200], height: 20,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: 0.0 
  });
  
  resultTextA = new visual.TextStim({
    win: psychoJS.window,
    name: 'resultTextA',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], height: 25,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: -1.0 
  });
  
  endFB = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  trialEnd = new visual.ImageStim({
    win : psychoJS.window,
    name : 'trialEnd', units : 'pix', 
    image : 'continueButton.png', mask : undefined,
    ori : 0, pos : [0, (- 350)], size : [110, 40],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -4.0 
  });
  endTrialMouse = new core.Mouse({
    win: psychoJS.window,
  });
  endTrialMouse.mouseClock = new util.Clock();
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}


var t;
var frameN;
var continueRoutine;
var gotValidClick;
var InstructionsRoutineComponents;
function InstructionsRoutineRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //------Prepare to start Routine 'InstructionsRoutine'-------
    t = 0;
    InstructionsRoutineClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // update component parameters for each repeat
    // setup some python lists for storing info about the startMouse
    startMouse.clicked_name = [];
    gotValidClick = false; // until a click is received
    // keep track of which components have finished
    InstructionsRoutineComponents = [];
    InstructionsRoutineComponents.push(introText);
    InstructionsRoutineComponents.push(start);
    InstructionsRoutineComponents.push(startMouse);
    
    for (const thisComponent of InstructionsRoutineComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var prevButtonState;
var _mouseButtons;
function InstructionsRoutineRoutineEachFrame() {
  return async function () {
    //------Loop for each frame of Routine 'InstructionsRoutine'-------
    // get current time
    t = InstructionsRoutineClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *introText* updates
    if (t >= 0.0 && introText.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      introText.tStart = t;  // (not accounting for frame time here)
      introText.frameNStart = frameN;  // exact frame index
      
      introText.setAutoDraw(true);
    }

    
    // *start* updates
    if (t >= 0.0 && start.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      start.tStart = t;  // (not accounting for frame time here)
      start.frameNStart = frameN;  // exact frame index
      
      start.setAutoDraw(true);
    }

    // *startMouse* updates
    if (t >= 0.0 && startMouse.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      startMouse.tStart = t;  // (not accounting for frame time here)
      startMouse.frameNStart = frameN;  // exact frame index
      
      startMouse.status = PsychoJS.Status.STARTED;
      startMouse.mouseClock.reset();
      prevButtonState = startMouse.getPressed();  // if button is down already this ISN'T a new click
      }
    if (startMouse.status === PsychoJS.Status.STARTED) {  // only update if started and not finished!
      _mouseButtons = startMouse.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          for (const obj of [start]) {
            if (obj.contains(startMouse)) {
              gotValidClick = true;
              startMouse.clicked_name.push(obj.name)
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
    for (const thisComponent of InstructionsRoutineComponents)
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


function InstructionsRoutineRoutineEnd() {
  return async function () {
    //------Ending Routine 'InstructionsRoutine'-------
    for (const thisComponent of InstructionsRoutineComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    // store data for psychoJS.experiment (ExperimentHandler)
    // the Routine "InstructionsRoutine" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    return Scheduler.Event.NEXT;
  };
}


var trials;
var currentLoop;
function trialsLoopBegin(trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 1, method: TrialHandler.Method.SEQUENTIAL,
      extraInfo: expInfo, originPath: undefined,
      trialList: 'conditions.xlsx',
      seed: undefined, name: 'trials'
    });
    psychoJS.experiment.addLoop(trials); // add the loop to the experiment
    currentLoop = trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisTrial of trials) {
      const snapshot = trials.getSnapshot();
      trialsLoopScheduler.add(importConditions(snapshot));
      trialsLoopScheduler.add(designARoutineBegin(snapshot));
      trialsLoopScheduler.add(designARoutineEachFrame());
      trialsLoopScheduler.add(designARoutineEnd());
      trialsLoopScheduler.add(resultRoutineBegin(snapshot));
      trialsLoopScheduler.add(resultRoutineEachFrame());
      trialsLoopScheduler.add(resultRoutineEnd());
      trialsLoopScheduler.add(endLoopIteration(trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}


async function trialsLoopEnd() {
  psychoJS.experiment.removeLoop(trials);

  return Scheduler.Event.NEXT;
}


var _key_resp_allKeys;
var pieces;
var answers;
var picked;
var newPiece;
var movingPiece;
var grid;
var designAComponents;
function designARoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //------Prepare to start Routine 'designA'-------
    t = 0;
    designAClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // update component parameters for each repeat
    masterPatternA.setSize(size_design);
    masterPatternA.setImage(design1);
    key_resp.keys = undefined;
    key_resp.rt = undefined;
    _key_resp_allKeys = [];
    polygon.setSize(size);
    whitePiece.setPos([(- 400), 0]);
    whitePiece.setSize((size / nRows1));
    blackPiece.setPos([400, 0]);
    blackPiece.setSize((size / nRows1));
    // setup some python lists for storing info about the mouse
    mouse.clicked_name = [];
    gotValidClick = false; // until a click is received
    pieces = [whitePiece, blackPiece]
    answers = [a1,a2,a3,a4,a5,a6,a7,a8,a9]
    picked = []
    newPiece = 'undefined'
    movingPiece = 'undefined'
    grid = createGrid(nRows1, size, polygon.pos, answers)
    
    
    
    // keep track of which components have finished
    designAComponents = [];
    designAComponents.push(masterPatternA);
    designAComponents.push(key_resp);
    designAComponents.push(polygon);
    designAComponents.push(whitePiece);
    designAComponents.push(blackPiece);
    designAComponents.push(mouse);
    designAComponents.push(end);
    
    for (const thisComponent of designAComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function designARoutineEachFrame() {
  return async function () {
    //------Loop for each frame of Routine 'designA'-------
    // get current time
    t = designAClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *masterPatternA* updates
    if (t >= 0.0 && masterPatternA.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      masterPatternA.tStart = t;  // (not accounting for frame time here)
      masterPatternA.frameNStart = frameN;  // exact frame index
      
      masterPatternA.setAutoDraw(true);
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
      let theseKeys = key_resp.getKeys({keyList: ['y', 'n', 'left', 'right', 'space'], waitRelease: false});
      _key_resp_allKeys = _key_resp_allKeys.concat(theseKeys);
      if (_key_resp_allKeys.length > 0) {
        key_resp.keys = _key_resp_allKeys[_key_resp_allKeys.length - 1].name;  // just the last key pressed
        key_resp.rt = _key_resp_allKeys[_key_resp_allKeys.length - 1].rt;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    
    // *polygon* updates
    if (t >= 0.0 && polygon.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      polygon.tStart = t;  // (not accounting for frame time here)
      polygon.frameNStart = frameN;  // exact frame index
      
      polygon.setAutoDraw(true);
    }

    
    // *whitePiece* updates
    if (t >= 0.0 && whitePiece.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      whitePiece.tStart = t;  // (not accounting for frame time here)
      whitePiece.frameNStart = frameN;  // exact frame index
      
      whitePiece.setAutoDraw(true);
    }

    
    // *blackPiece* updates
    if (t >= 0.0 && blackPiece.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blackPiece.tStart = t;  // (not accounting for frame time here)
      blackPiece.frameNStart = frameN;  // exact frame index
      
      blackPiece.setAutoDraw(true);
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
          for (const obj of [end]) {
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
    for (let piece of pieces) {
        if (piece.contains(mouse) && mouse.getPressed()[0] === 1 && newPiece === 'undefined') {
            newPiece = createPiece(piece, mouse.getPos(), picNameDict[piece.name])
            picked.push(newPiece)
        }
    }
            
        
    if (newPiece !== 'undefined' && mouse.getPressed()[0] === 0) {
        newPiece = 'undefined'
    }
    
    movingPiece = movePicked(picked, mouse, movingPiece)
    drawGrid(grid, true)
    drawPicked(picked, true)
    
    // *end* updates
    if (t >= 0.0 && end.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      end.tStart = t;  // (not accounting for frame time here)
      end.frameNStart = frameN;  // exact frame index
      
      end.setAutoDraw(true);
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
    for (const thisComponent of designAComponents)
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


var designATime;
var correctA;
function designARoutineEnd() {
  return async function () {
    //------Ending Routine 'designA'-------
    for (const thisComponent of designAComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
    if (typeof key_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
        routineTimer.reset();
        }
    
    key_resp.stop();
    // store data for psychoJS.experiment (ExperimentHandler)
    designATime = parseInt(designAClock.getTime())
    correctA = checkAnswer(grid, picked)
    drawPicked(picked, false)
    drawGrid(grid, false)
    // the Routine "designA" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    return Scheduler.Event.NEXT;
  };
}


var _endFB_allKeys;
var resultComponents;
function resultRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //------Prepare to start Routine 'result'-------
    t = 0;
    resultClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // update component parameters for each repeat
    resultAccuracy.text = correctA ? "Correct!\n" : "Incorrect!\n" 
    
    
    resultTextA.text = "Time taken: " + designATime + " seconds\n"
    
    psychoJS.experiment.addData('correctA', correctA);
    psychoJS.experiment.addData('p1Actual', designATime);
    
    endFB.keys = undefined;
    endFB.rt = undefined;
    _endFB_allKeys = [];
    // setup some python lists for storing info about the endTrialMouse
    endTrialMouse.clicked_name = [];
    gotValidClick = false; // until a click is received
    // keep track of which components have finished
    resultComponents = [];
    resultComponents.push(resultAccuracy);
    resultComponents.push(resultTextA);
    resultComponents.push(endFB);
    resultComponents.push(trialEnd);
    resultComponents.push(endTrialMouse);
    
    for (const thisComponent of resultComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function resultRoutineEachFrame() {
  return async function () {
    //------Loop for each frame of Routine 'result'-------
    // get current time
    t = resultClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *resultAccuracy* updates
    if (t >= 0.0 && resultAccuracy.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      resultAccuracy.tStart = t;  // (not accounting for frame time here)
      resultAccuracy.frameNStart = frameN;  // exact frame index
      
      resultAccuracy.setAutoDraw(true);
    }

    
    // *resultTextA* updates
    if (t >= 0.0 && resultTextA.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      resultTextA.tStart = t;  // (not accounting for frame time here)
      resultTextA.frameNStart = frameN;  // exact frame index
      
      resultTextA.setAutoDraw(true);
    }

    
    // *endFB* updates
    if (t >= 0.0 && endFB.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      endFB.tStart = t;  // (not accounting for frame time here)
      endFB.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { endFB.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { endFB.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { endFB.clearEvents(); });
    }

    if (endFB.status === PsychoJS.Status.STARTED) {
      let theseKeys = endFB.getKeys({keyList: ['space'], waitRelease: false});
      _endFB_allKeys = _endFB_allKeys.concat(theseKeys);
      if (_endFB_allKeys.length > 0) {
        endFB.keys = _endFB_allKeys[_endFB_allKeys.length - 1].name;  // just the last key pressed
        endFB.rt = _endFB_allKeys[_endFB_allKeys.length - 1].rt;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    
    // *trialEnd* updates
    if (t >= 0.0 && trialEnd.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      trialEnd.tStart = t;  // (not accounting for frame time here)
      trialEnd.frameNStart = frameN;  // exact frame index
      
      trialEnd.setAutoDraw(true);
    }

    // *endTrialMouse* updates
    if (t >= 0.0 && endTrialMouse.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      endTrialMouse.tStart = t;  // (not accounting for frame time here)
      endTrialMouse.frameNStart = frameN;  // exact frame index
      
      endTrialMouse.status = PsychoJS.Status.STARTED;
      endTrialMouse.mouseClock.reset();
      prevButtonState = endTrialMouse.getPressed();  // if button is down already this ISN'T a new click
      }
    if (endTrialMouse.status === PsychoJS.Status.STARTED) {  // only update if started and not finished!
      _mouseButtons = endTrialMouse.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          for (const obj of [trialEnd]) {
            if (obj.contains(endTrialMouse)) {
              gotValidClick = true;
              endTrialMouse.clicked_name.push(obj.name)
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
    for (const thisComponent of resultComponents)
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


function resultRoutineEnd() {
  return async function () {
    //------Ending Routine 'result'-------
    for (const thisComponent of resultComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('endFB.keys', endFB.keys);
    if (typeof endFB.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('endFB.rt', endFB.rt);
        routineTimer.reset();
        }
    
    endFB.stop();
    // store data for psychoJS.experiment (ExperimentHandler)
    // the Routine "result" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
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
