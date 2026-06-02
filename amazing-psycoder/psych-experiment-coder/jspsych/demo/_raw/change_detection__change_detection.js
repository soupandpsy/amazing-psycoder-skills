// Source: change_detection (demos/change_detection)
// Project URL: https://gitlab.pavlovia.org/demos/change_detection
// Original file: change_detection.js
﻿/************************* 
 * Change_Detection *
 *************************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2024.2.4.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'change_detection';  // from the Builder filename that created this script
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
const change_trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(change_trialsLoopBegin(change_trialsLoopScheduler));
flowScheduler.add(change_trialsLoopScheduler);
flowScheduler.add(change_trialsLoopEnd);






flowScheduler.add(next_instrRoutineBegin());
flowScheduler.add(next_instrRoutineEachFrame());
flowScheduler.add(next_instrRoutineEnd());
const localisation_trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(localisation_trialsLoopBegin(localisation_trialsLoopScheduler));
flowScheduler.add(localisation_trialsLoopScheduler);
flowScheduler.add(localisation_trialsLoopEnd);






flowScheduler.add(byeRoutineBegin());
flowScheduler.add(byeRoutineEachFrame());
flowScheduler.add(byeRoutineEnd());
flowScheduler.add(quitPsychoJS, '', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, '', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    // resources:
    {'name': 'code/sampled_circle_points_with_colors.csv', 'path': 'code/sampled_circle_points_with_colors.csv'},
    {'name': 'code/localisation_trials_with_test_columns.xlsx', 'path': 'code/localisation_trials_with_test_columns.xlsx'},
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
var welcometxt;
var start_resp;
var fixationClock;
var fix;
var trialClock;
var square1;
var square2;
var square3;
var square4;
var square5;
var square6;
var retentionClock;
var blank;
var show_testClock;
var question;
var test_square;
var key_resp;
var feedbackClock;
var fbtextbox;
var next_instrClock;
var nextinstrtxt;
var next_resp;
var localisation_testClock;
var square1_2;
var square2_2;
var square3_2;
var square4_2;
var square5_2;
var square6_2;
var one_label;
var two_label;
var three_label;
var four_label;
var five_label;
var six_label;
var localisation_resp;
var question_2;
var localisation_feedbackClock;
var fbtextbox_2;
var byeClock;
var textbox;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "instructions"
  instructionsClock = new util.Clock();
  welcometxt = new visual.TextBox({
    win: psychoJS.window,
    name: 'welcometxt',
    text: 'In this task you will see six colored squares. \n\nAfter viewing the squares you will see on colored square in a particular location. \n\nYour task is to judge if that colored square did appear in that location. \n\nPress Y if that color square did occur in that location\nPress N if that color square did not appear in that location\n\nPress space to start',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 1],  units: 'height', 
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
  
  start_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "fixation"
  fixationClock = new util.Clock();
  fix = new visual.TextStim({
    win: psychoJS.window,
    name: 'fix',
    text: '+',
    font: 'Arial',
    units: 'height', 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  // Initialize components for Routine "trial"
  trialClock = new util.Clock();
  square1 = new visual.Rect ({
    win: psychoJS.window, name: 'square1', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
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
  
  square2 = new visual.Rect ({
    win: psychoJS.window, name: 'square2', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -1, 
    interpolate: true, 
  });
  
  square3 = new visual.Rect ({
    win: psychoJS.window, name: 'square3', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -2, 
    interpolate: true, 
  });
  
  square4 = new visual.Rect ({
    win: psychoJS.window, name: 'square4', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -3, 
    interpolate: true, 
  });
  
  square5 = new visual.Rect ({
    win: psychoJS.window, name: 'square5', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -4, 
    interpolate: true, 
  });
  
  square6 = new visual.Rect ({
    win: psychoJS.window, name: 'square6', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -5, 
    interpolate: true, 
  });
  
  // Initialize components for Routine "retention"
  retentionClock = new util.Clock();
  blank = new visual.TextStim({
    win: psychoJS.window,
    name: 'blank',
    text: 'offscreen',
    font: 'Arial',
    units: 'height', 
    pos: [0, (- 500)], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  // Initialize components for Routine "show_test"
  show_testClock = new util.Clock();
  question = new visual.TextBox({
    win: psychoJS.window,
    name: 'question',
    text: 'Did this color square appear in this location? \n\nPress Y for yes \nPress N for no',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.03,
    lineSpacing: 1.0,
    size: [0.5, 0.3],  units: 'height', 
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
  
  test_square = new visual.Rect ({
    win: psychoJS.window, name: 'test_square', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -2, 
    interpolate: true, 
  });
  
  key_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "feedback"
  feedbackClock = new util.Clock();
  fbtextbox = new visual.TextBox({
    win: psychoJS.window,
    name: 'fbtextbox',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.5],  units: 'height', 
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
  
  // Initialize components for Routine "next_instr"
  next_instrClock = new util.Clock();
  nextinstrtxt = new visual.TextBox({
    win: psychoJS.window,
    name: 'nextinstrtxt',
    text: 'Great! \n\nThis time you will see six squares folowed by another six squares. One of the squares will have changed in color, use the keys 1 - 6 on your keyboard to indicate which has changed. \n\nPress space to start',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1, 1],  units: 'height', 
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
  
  next_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "localisation_test"
  localisation_testClock = new util.Clock();
  square1_2 = new visual.Rect ({
    win: psychoJS.window, name: 'square1_2', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
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
  
  square2_2 = new visual.Rect ({
    win: psychoJS.window, name: 'square2_2', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -1, 
    interpolate: true, 
  });
  
  square3_2 = new visual.Rect ({
    win: psychoJS.window, name: 'square3_2', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -2, 
    interpolate: true, 
  });
  
  square4_2 = new visual.Rect ({
    win: psychoJS.window, name: 'square4_2', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -3, 
    interpolate: true, 
  });
  
  square5_2 = new visual.Rect ({
    win: psychoJS.window, name: 'square5_2', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -4, 
    interpolate: true, 
  });
  
  square6_2 = new visual.Rect ({
    win: psychoJS.window, name: 'square6_2', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -5, 
    interpolate: true, 
  });
  
  one_label = new visual.TextBox({
    win: psychoJS.window,
    name: 'one_label',
    text: '1',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.1, 0.1],  units: 'height', 
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
    depth: -6.0 
  });
  
  two_label = new visual.TextBox({
    win: psychoJS.window,
    name: 'two_label',
    text: '2',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.1, 0.1],  units: 'height', 
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
    depth: -7.0 
  });
  
  three_label = new visual.TextBox({
    win: psychoJS.window,
    name: 'three_label',
    text: '3',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.1, 0.1],  units: 'height', 
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
    depth: -8.0 
  });
  
  four_label = new visual.TextBox({
    win: psychoJS.window,
    name: 'four_label',
    text: '4',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.1, 0.1],  units: 'height', 
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
    depth: -9.0 
  });
  
  five_label = new visual.TextBox({
    win: psychoJS.window,
    name: 'five_label',
    text: '5',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.1, 0.1],  units: 'height', 
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
    depth: -10.0 
  });
  
  six_label = new visual.TextBox({
    win: psychoJS.window,
    name: 'six_label',
    text: '6',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.1, 0.1],  units: 'height', 
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
    depth: -11.0 
  });
  
  localisation_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  question_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'question_2',
    text: 'Which square changed? \n\nPress 1 - 6',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.03,
    lineSpacing: 1.0,
    size: [1, 0.3],  units: 'height', 
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
    depth: -13.0 
  });
  
  // Initialize components for Routine "localisation_feedback"
  localisation_feedbackClock = new util.Clock();
  fbtextbox_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'fbtextbox_2',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.5],  units: 'height', 
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
  
  // Initialize components for Routine "bye"
  byeClock = new util.Clock();
  textbox = new visual.TextBox({
    win: psychoJS.window,
    name: 'textbox',
    text: 'That is the end - goodbye!',
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
var instructionsMaxDurationReached;
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
    instructionsClock.reset();
    routineTimer.reset();
    instructionsMaxDurationReached = false;
    // update component parameters for each repeat
    start_resp.keys = undefined;
    start_resp.rt = undefined;
    _start_resp_allKeys = [];
    psychoJS.experiment.addData('instructions.started', globalClock.getTime());
    instructionsMaxDuration = null
    // keep track of which components have finished
    instructionsComponents = [];
    instructionsComponents.push(welcometxt);
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
    
    // *welcometxt* updates
    if (t >= 0.0 && welcometxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      welcometxt.tStart = t;  // (not accounting for frame time here)
      welcometxt.frameNStart = frameN;  // exact frame index
      
      welcometxt.setAutoDraw(true);
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


var change_trials;
function change_trialsLoopBegin(change_trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    change_trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 1, method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: 'code/sampled_circle_points_with_colors.csv',
      seed: undefined, name: 'change_trials'
    });
    psychoJS.experiment.addLoop(change_trials); // add the loop to the experiment
    currentLoop = change_trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisChange_trial of change_trials) {
      snapshot = change_trials.getSnapshot();
      change_trialsLoopScheduler.add(importConditions(snapshot));
      change_trialsLoopScheduler.add(fixationRoutineBegin(snapshot));
      change_trialsLoopScheduler.add(fixationRoutineEachFrame());
      change_trialsLoopScheduler.add(fixationRoutineEnd(snapshot));
      change_trialsLoopScheduler.add(trialRoutineBegin(snapshot));
      change_trialsLoopScheduler.add(trialRoutineEachFrame());
      change_trialsLoopScheduler.add(trialRoutineEnd(snapshot));
      change_trialsLoopScheduler.add(retentionRoutineBegin(snapshot));
      change_trialsLoopScheduler.add(retentionRoutineEachFrame());
      change_trialsLoopScheduler.add(retentionRoutineEnd(snapshot));
      change_trialsLoopScheduler.add(show_testRoutineBegin(snapshot));
      change_trialsLoopScheduler.add(show_testRoutineEachFrame());
      change_trialsLoopScheduler.add(show_testRoutineEnd(snapshot));
      change_trialsLoopScheduler.add(feedbackRoutineBegin(snapshot));
      change_trialsLoopScheduler.add(feedbackRoutineEachFrame());
      change_trialsLoopScheduler.add(feedbackRoutineEnd(snapshot));
      change_trialsLoopScheduler.add(change_trialsLoopEndIteration(change_trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}


async function change_trialsLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(change_trials);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function change_trialsLoopEndIteration(scheduler, snapshot) {
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


var localisation_trials;
function localisation_trialsLoopBegin(localisation_trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    localisation_trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 5, method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: 'code/localisation_trials_with_test_columns.xlsx',
      seed: undefined, name: 'localisation_trials'
    });
    psychoJS.experiment.addLoop(localisation_trials); // add the loop to the experiment
    currentLoop = localisation_trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisLocalisation_trial of localisation_trials) {
      snapshot = localisation_trials.getSnapshot();
      localisation_trialsLoopScheduler.add(importConditions(snapshot));
      localisation_trialsLoopScheduler.add(fixationRoutineBegin(snapshot));
      localisation_trialsLoopScheduler.add(fixationRoutineEachFrame());
      localisation_trialsLoopScheduler.add(fixationRoutineEnd(snapshot));
      localisation_trialsLoopScheduler.add(trialRoutineBegin(snapshot));
      localisation_trialsLoopScheduler.add(trialRoutineEachFrame());
      localisation_trialsLoopScheduler.add(trialRoutineEnd(snapshot));
      localisation_trialsLoopScheduler.add(retentionRoutineBegin(snapshot));
      localisation_trialsLoopScheduler.add(retentionRoutineEachFrame());
      localisation_trialsLoopScheduler.add(retentionRoutineEnd(snapshot));
      localisation_trialsLoopScheduler.add(localisation_testRoutineBegin(snapshot));
      localisation_trialsLoopScheduler.add(localisation_testRoutineEachFrame());
      localisation_trialsLoopScheduler.add(localisation_testRoutineEnd(snapshot));
      localisation_trialsLoopScheduler.add(localisation_feedbackRoutineBegin(snapshot));
      localisation_trialsLoopScheduler.add(localisation_feedbackRoutineEachFrame());
      localisation_trialsLoopScheduler.add(localisation_feedbackRoutineEnd(snapshot));
      localisation_trialsLoopScheduler.add(localisation_trialsLoopEndIteration(localisation_trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}


async function localisation_trialsLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(localisation_trials);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function localisation_trialsLoopEndIteration(scheduler, snapshot) {
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


var fixationMaxDurationReached;
var fixationMaxDuration;
var fixationComponents;
function fixationRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'fixation' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    fixationClock.reset(routineTimer.getTime());
    routineTimer.add(0.500000);
    fixationMaxDurationReached = false;
    // update component parameters for each repeat
    psychoJS.experiment.addData('fixation.started', globalClock.getTime());
    fixationMaxDuration = null
    // keep track of which components have finished
    fixationComponents = [];
    fixationComponents.push(fix);
    
    for (const thisComponent of fixationComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var frameRemains;
function fixationRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'fixation' ---
    // get current time
    t = fixationClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *fix* updates
    if (t >= 0.0 && fix.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fix.tStart = t;  // (not accounting for frame time here)
      fix.frameNStart = frameN;  // exact frame index
      
      fix.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (fix.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      fix.setAutoDraw(false);
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
    for (const thisComponent of fixationComponents)
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


function fixationRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'fixation' ---
    for (const thisComponent of fixationComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('fixation.stopped', globalClock.getTime());
    if (fixationMaxDurationReached) {
        fixationClock.add(fixationMaxDuration);
    } else {
        fixationClock.add(0.500000);
    }
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
    trialClock.reset(routineTimer.getTime());
    routineTimer.add(0.500000);
    trialMaxDurationReached = false;
    // update component parameters for each repeat
    square1.setFillColor(new util.Color(color1));
    square1.setPos([x1, y1]);
    square1.setLineColor(new util.Color(color1));
    square2.setFillColor(new util.Color(color2));
    square2.setPos([x2, y2]);
    square2.setLineColor(new util.Color(color2));
    square3.setFillColor(new util.Color(color3));
    square3.setPos([x3, y3]);
    square3.setLineColor(new util.Color(color3));
    square4.setFillColor(new util.Color(color4));
    square4.setPos([x4, y4]);
    square4.setLineColor(new util.Color(color4));
    square5.setFillColor(new util.Color(color5));
    square5.setPos([x5, y5]);
    square5.setLineColor(new util.Color(color5));
    square6.setFillColor(new util.Color(color6));
    square6.setPos([x6, y6]);
    square6.setLineColor(new util.Color(color6));
    psychoJS.experiment.addData('trial.started', globalClock.getTime());
    trialMaxDuration = null
    // keep track of which components have finished
    trialComponents = [];
    trialComponents.push(square1);
    trialComponents.push(square2);
    trialComponents.push(square3);
    trialComponents.push(square4);
    trialComponents.push(square5);
    trialComponents.push(square6);
    
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
    
    // *square1* updates
    if (t >= 0.0 && square1.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square1.tStart = t;  // (not accounting for frame time here)
      square1.frameNStart = frameN;  // exact frame index
      
      square1.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (square1.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      square1.setAutoDraw(false);
    }
    
    
    // *square2* updates
    if (t >= 0.0 && square2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square2.tStart = t;  // (not accounting for frame time here)
      square2.frameNStart = frameN;  // exact frame index
      
      square2.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (square2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      square2.setAutoDraw(false);
    }
    
    
    // *square3* updates
    if (t >= 0.0 && square3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square3.tStart = t;  // (not accounting for frame time here)
      square3.frameNStart = frameN;  // exact frame index
      
      square3.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (square3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      square3.setAutoDraw(false);
    }
    
    
    // *square4* updates
    if (t >= 0.0 && square4.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square4.tStart = t;  // (not accounting for frame time here)
      square4.frameNStart = frameN;  // exact frame index
      
      square4.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (square4.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      square4.setAutoDraw(false);
    }
    
    
    // *square5* updates
    if (t >= 0.0 && square5.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square5.tStart = t;  // (not accounting for frame time here)
      square5.frameNStart = frameN;  // exact frame index
      
      square5.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (square5.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      square5.setAutoDraw(false);
    }
    
    
    // *square6* updates
    if (t >= 0.0 && square6.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square6.tStart = t;  // (not accounting for frame time here)
      square6.frameNStart = frameN;  // exact frame index
      
      square6.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (square6.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      square6.setAutoDraw(false);
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
    if (continueRoutine && routineTimer.getTime() > 0) {
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
    if (trialMaxDurationReached) {
        trialClock.add(trialMaxDuration);
    } else {
        trialClock.add(0.500000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var retentionMaxDurationReached;
var retentionMaxDuration;
var retentionComponents;
function retentionRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'retention' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    retentionClock.reset(routineTimer.getTime());
    routineTimer.add(1.000000);
    retentionMaxDurationReached = false;
    // update component parameters for each repeat
    psychoJS.experiment.addData('retention.started', globalClock.getTime());
    retentionMaxDuration = null
    // keep track of which components have finished
    retentionComponents = [];
    retentionComponents.push(blank);
    
    for (const thisComponent of retentionComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function retentionRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'retention' ---
    // get current time
    t = retentionClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *blank* updates
    if (t >= 0.0 && blank.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blank.tStart = t;  // (not accounting for frame time here)
      blank.frameNStart = frameN;  // exact frame index
      
      blank.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 1.0 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (blank.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      blank.setAutoDraw(false);
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
    for (const thisComponent of retentionComponents)
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


function retentionRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'retention' ---
    for (const thisComponent of retentionComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('retention.stopped', globalClock.getTime());
    if (retentionMaxDurationReached) {
        retentionClock.add(retentionMaxDuration);
    } else {
        retentionClock.add(1.000000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var show_testMaxDurationReached;
var possible_sets;
var xtest;
var ytest;
var colortest;
var _key_resp_allKeys;
var show_testMaxDuration;
var show_testComponents;
function show_testRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'show_test' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    show_testClock.reset();
    routineTimer.reset();
    show_testMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from code
    possible_sets = [[x1, y1, color1], [x2, y2, color2], [x3, y3, color3], [x4, y4, color4], [x5, y5, color5]];
    util.shuffle(possible_sets);
    if ((condition_label === "same")) {
        xtest = possible_sets[0][0];
        ytest = possible_sets[0][1];
        colortest = possible_sets[0][2];
    } else {
        xtest = possible_sets[0][0];
        ytest = possible_sets[0][1];
        colortest = possible_sets[1][2];
    }
    psychoJS.experiment.addData("xtest", xtest);
    psychoJS.experiment.addData("ytest", ytest);
    psychoJS.experiment.addData("colortest", colortest);
    
    test_square.setFillColor(new util.Color(colortest));
    test_square.setPos([xtest, ytest]);
    test_square.setLineColor(new util.Color(colortest));
    key_resp.keys = undefined;
    key_resp.rt = undefined;
    _key_resp_allKeys = [];
    psychoJS.experiment.addData('show_test.started', globalClock.getTime());
    show_testMaxDuration = null
    // keep track of which components have finished
    show_testComponents = [];
    show_testComponents.push(question);
    show_testComponents.push(test_square);
    show_testComponents.push(key_resp);
    
    for (const thisComponent of show_testComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function show_testRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'show_test' ---
    // get current time
    t = show_testClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *question* updates
    if (t >= 0.0 && question.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      question.tStart = t;  // (not accounting for frame time here)
      question.frameNStart = frameN;  // exact frame index
      
      question.setAutoDraw(true);
    }
    
    
    // *test_square* updates
    if (t >= 0.0 && test_square.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      test_square.tStart = t;  // (not accounting for frame time here)
      test_square.frameNStart = frameN;  // exact frame index
      
      test_square.setAutoDraw(true);
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
      let theseKeys = key_resp.getKeys({keyList: ['y', 'n'], waitRelease: false});
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
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of show_testComponents)
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


function show_testRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'show_test' ---
    for (const thisComponent of show_testComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('show_test.stopped', globalClock.getTime());
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
    // the Routine "show_test" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var feedbackMaxDurationReached;
var fbtxt;
var fbcol;
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
    if (key_resp.corr) {
        fbtxt = "Correct!";
        fbcol = "green";
    } else {
        fbtxt = "Incorrect";
        fbcol = "red";
    }
    
    fbtextbox.setColor(new util.Color(fbcol));
    fbtextbox.setText(fbtxt);
    psychoJS.experiment.addData('feedback.started', globalClock.getTime());
    feedbackMaxDuration = null
    // keep track of which components have finished
    feedbackComponents = [];
    feedbackComponents.push(fbtextbox);
    
    for (const thisComponent of feedbackComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function feedbackRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'feedback' ---
    // get current time
    t = feedbackClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *fbtextbox* updates
    if (t >= 0.0 && fbtextbox.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fbtextbox.tStart = t;  // (not accounting for frame time here)
      fbtextbox.frameNStart = frameN;  // exact frame index
      
      fbtextbox.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (fbtextbox.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      fbtextbox.setAutoDraw(false);
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


var next_instrMaxDurationReached;
var _next_resp_allKeys;
var next_instrMaxDuration;
var next_instrComponents;
function next_instrRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'next_instr' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    next_instrClock.reset();
    routineTimer.reset();
    next_instrMaxDurationReached = false;
    // update component parameters for each repeat
    next_resp.keys = undefined;
    next_resp.rt = undefined;
    _next_resp_allKeys = [];
    psychoJS.experiment.addData('next_instr.started', globalClock.getTime());
    next_instrMaxDuration = null
    // keep track of which components have finished
    next_instrComponents = [];
    next_instrComponents.push(nextinstrtxt);
    next_instrComponents.push(next_resp);
    
    for (const thisComponent of next_instrComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function next_instrRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'next_instr' ---
    // get current time
    t = next_instrClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *nextinstrtxt* updates
    if (t >= 0.0 && nextinstrtxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      nextinstrtxt.tStart = t;  // (not accounting for frame time here)
      nextinstrtxt.frameNStart = frameN;  // exact frame index
      
      nextinstrtxt.setAutoDraw(true);
    }
    
    
    // *next_resp* updates
    if (t >= 0.0 && next_resp.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      next_resp.tStart = t;  // (not accounting for frame time here)
      next_resp.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { next_resp.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { next_resp.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { next_resp.clearEvents(); });
    }
    
    if (next_resp.status === PsychoJS.Status.STARTED) {
      let theseKeys = next_resp.getKeys({keyList: ['space'], waitRelease: false});
      _next_resp_allKeys = _next_resp_allKeys.concat(theseKeys);
      if (_next_resp_allKeys.length > 0) {
        next_resp.keys = _next_resp_allKeys[_next_resp_allKeys.length - 1].name;  // just the last key pressed
        next_resp.rt = _next_resp_allKeys[_next_resp_allKeys.length - 1].rt;
        next_resp.duration = _next_resp_allKeys[_next_resp_allKeys.length - 1].duration;
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
    for (const thisComponent of next_instrComponents)
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


function next_instrRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'next_instr' ---
    for (const thisComponent of next_instrComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('next_instr.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(next_resp.corr, level);
    }
    psychoJS.experiment.addData('next_resp.keys', next_resp.keys);
    if (typeof next_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('next_resp.rt', next_resp.rt);
        psychoJS.experiment.addData('next_resp.duration', next_resp.duration);
        routineTimer.reset();
        }
    
    next_resp.stop();
    // the Routine "next_instr" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var localisation_testMaxDurationReached;
var _localisation_resp_allKeys;
var localisation_testMaxDuration;
var localisation_testComponents;
function localisation_testRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'localisation_test' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    localisation_testClock.reset();
    routineTimer.reset();
    localisation_testMaxDurationReached = false;
    // update component parameters for each repeat
    square1_2.setFillColor(new util.Color(testcolor1));
    square1_2.setPos([x1, y1]);
    square1_2.setLineColor(new util.Color(testcolor1));
    square2_2.setFillColor(new util.Color(testcolor2));
    square2_2.setPos([x2, y2]);
    square2_2.setLineColor(new util.Color(testcolor2));
    square3_2.setFillColor(new util.Color(testcolor3));
    square3_2.setPos([x3, y3]);
    square3_2.setLineColor(new util.Color(testcolor3));
    square4_2.setFillColor(new util.Color(testcolor4));
    square4_2.setPos([x4, y4]);
    square4_2.setLineColor(new util.Color(testcolor4));
    square5_2.setFillColor(new util.Color(testcolor5));
    square5_2.setPos([x5, y5]);
    square5_2.setLineColor(new util.Color(testcolor5));
    square6_2.setFillColor(new util.Color(testcolor6));
    square6_2.setPos([x6, y6]);
    square6_2.setLineColor(new util.Color(testcolor6));
    one_label.setPos([x1, y1]);
    two_label.setPos([x2, y2]);
    three_label.setPos([x3, y3]);
    four_label.setPos([x4, y4]);
    five_label.setPos([x5, y5]);
    six_label.setPos([x6, y6]);
    localisation_resp.keys = undefined;
    localisation_resp.rt = undefined;
    _localisation_resp_allKeys = [];
    psychoJS.experiment.addData('localisation_test.started', globalClock.getTime());
    localisation_testMaxDuration = null
    // keep track of which components have finished
    localisation_testComponents = [];
    localisation_testComponents.push(square1_2);
    localisation_testComponents.push(square2_2);
    localisation_testComponents.push(square3_2);
    localisation_testComponents.push(square4_2);
    localisation_testComponents.push(square5_2);
    localisation_testComponents.push(square6_2);
    localisation_testComponents.push(one_label);
    localisation_testComponents.push(two_label);
    localisation_testComponents.push(three_label);
    localisation_testComponents.push(four_label);
    localisation_testComponents.push(five_label);
    localisation_testComponents.push(six_label);
    localisation_testComponents.push(localisation_resp);
    localisation_testComponents.push(question_2);
    
    for (const thisComponent of localisation_testComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function localisation_testRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'localisation_test' ---
    // get current time
    t = localisation_testClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *square1_2* updates
    if (t >= 0.0 && square1_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square1_2.tStart = t;  // (not accounting for frame time here)
      square1_2.frameNStart = frameN;  // exact frame index
      
      square1_2.setAutoDraw(true);
    }
    
    
    // *square2_2* updates
    if (t >= 0.0 && square2_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square2_2.tStart = t;  // (not accounting for frame time here)
      square2_2.frameNStart = frameN;  // exact frame index
      
      square2_2.setAutoDraw(true);
    }
    
    
    // *square3_2* updates
    if (t >= 0.0 && square3_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square3_2.tStart = t;  // (not accounting for frame time here)
      square3_2.frameNStart = frameN;  // exact frame index
      
      square3_2.setAutoDraw(true);
    }
    
    
    // *square4_2* updates
    if (t >= 0.0 && square4_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square4_2.tStart = t;  // (not accounting for frame time here)
      square4_2.frameNStart = frameN;  // exact frame index
      
      square4_2.setAutoDraw(true);
    }
    
    
    // *square5_2* updates
    if (t >= 0.0 && square5_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square5_2.tStart = t;  // (not accounting for frame time here)
      square5_2.frameNStart = frameN;  // exact frame index
      
      square5_2.setAutoDraw(true);
    }
    
    
    // *square6_2* updates
    if (t >= 0.0 && square6_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      square6_2.tStart = t;  // (not accounting for frame time here)
      square6_2.frameNStart = frameN;  // exact frame index
      
      square6_2.setAutoDraw(true);
    }
    
    
    // *one_label* updates
    if (t >= 0.0 && one_label.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      one_label.tStart = t;  // (not accounting for frame time here)
      one_label.frameNStart = frameN;  // exact frame index
      
      one_label.setAutoDraw(true);
    }
    
    
    // *two_label* updates
    if (t >= 0.0 && two_label.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      two_label.tStart = t;  // (not accounting for frame time here)
      two_label.frameNStart = frameN;  // exact frame index
      
      two_label.setAutoDraw(true);
    }
    
    
    // *three_label* updates
    if (t >= 0.0 && three_label.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      three_label.tStart = t;  // (not accounting for frame time here)
      three_label.frameNStart = frameN;  // exact frame index
      
      three_label.setAutoDraw(true);
    }
    
    
    // *four_label* updates
    if (t >= 0.0 && four_label.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      four_label.tStart = t;  // (not accounting for frame time here)
      four_label.frameNStart = frameN;  // exact frame index
      
      four_label.setAutoDraw(true);
    }
    
    
    // *five_label* updates
    if (t >= 0.0 && five_label.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      five_label.tStart = t;  // (not accounting for frame time here)
      five_label.frameNStart = frameN;  // exact frame index
      
      five_label.setAutoDraw(true);
    }
    
    
    // *six_label* updates
    if (t >= 0.0 && six_label.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      six_label.tStart = t;  // (not accounting for frame time here)
      six_label.frameNStart = frameN;  // exact frame index
      
      six_label.setAutoDraw(true);
    }
    
    
    // *localisation_resp* updates
    if (t >= 0.0 && localisation_resp.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      localisation_resp.tStart = t;  // (not accounting for frame time here)
      localisation_resp.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { localisation_resp.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { localisation_resp.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { localisation_resp.clearEvents(); });
    }
    
    if (localisation_resp.status === PsychoJS.Status.STARTED) {
      let theseKeys = localisation_resp.getKeys({keyList: ['1', '2', '3', '4', '5', '6'], waitRelease: false});
      _localisation_resp_allKeys = _localisation_resp_allKeys.concat(theseKeys);
      if (_localisation_resp_allKeys.length > 0) {
        localisation_resp.keys = _localisation_resp_allKeys[_localisation_resp_allKeys.length - 1].name;  // just the last key pressed
        localisation_resp.rt = _localisation_resp_allKeys[_localisation_resp_allKeys.length - 1].rt;
        localisation_resp.duration = _localisation_resp_allKeys[_localisation_resp_allKeys.length - 1].duration;
        // was this correct?
        if (localisation_resp.keys == changed_color_index) {
            localisation_resp.corr = 1;
        } else {
            localisation_resp.corr = 0;
        }
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    
    // *question_2* updates
    if (t >= 0.0 && question_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      question_2.tStart = t;  // (not accounting for frame time here)
      question_2.frameNStart = frameN;  // exact frame index
      
      question_2.setAutoDraw(true);
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
    for (const thisComponent of localisation_testComponents)
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


function localisation_testRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'localisation_test' ---
    for (const thisComponent of localisation_testComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('localisation_test.stopped', globalClock.getTime());
    // was no response the correct answer?!
    if (localisation_resp.keys === undefined) {
      if (['None','none',undefined].includes(changed_color_index)) {
         localisation_resp.corr = 1;  // correct non-response
      } else {
         localisation_resp.corr = 0;  // failed to respond (incorrectly)
      }
    }
    // store data for current loop
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(localisation_resp.corr, level);
    }
    psychoJS.experiment.addData('localisation_resp.keys', localisation_resp.keys);
    psychoJS.experiment.addData('localisation_resp.corr', localisation_resp.corr);
    if (typeof localisation_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('localisation_resp.rt', localisation_resp.rt);
        psychoJS.experiment.addData('localisation_resp.duration', localisation_resp.duration);
        routineTimer.reset();
        }
    
    localisation_resp.stop();
    // the Routine "localisation_test" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var localisation_feedbackMaxDurationReached;
var localisation_feedbackMaxDuration;
var localisation_feedbackComponents;
function localisation_feedbackRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'localisation_feedback' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    localisation_feedbackClock.reset(routineTimer.getTime());
    routineTimer.add(0.500000);
    localisation_feedbackMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from code_4
    if (localisation_resp.corr) {
        fbtxt = "Correct!";
        fbcol = "green";
    } else {
        fbtxt = "Incorrect";
        fbcol = "red";
    }
    
    fbtextbox_2.setColor(new util.Color(fbcol));
    fbtextbox_2.setText(fbtxt);
    psychoJS.experiment.addData('localisation_feedback.started', globalClock.getTime());
    localisation_feedbackMaxDuration = null
    // keep track of which components have finished
    localisation_feedbackComponents = [];
    localisation_feedbackComponents.push(fbtextbox_2);
    
    for (const thisComponent of localisation_feedbackComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function localisation_feedbackRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'localisation_feedback' ---
    // get current time
    t = localisation_feedbackClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *fbtextbox_2* updates
    if (t >= 0.0 && fbtextbox_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fbtextbox_2.tStart = t;  // (not accounting for frame time here)
      fbtextbox_2.frameNStart = frameN;  // exact frame index
      
      fbtextbox_2.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (fbtextbox_2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      fbtextbox_2.setAutoDraw(false);
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
    for (const thisComponent of localisation_feedbackComponents)
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


function localisation_feedbackRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'localisation_feedback' ---
    for (const thisComponent of localisation_feedbackComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('localisation_feedback.stopped', globalClock.getTime());
    if (localisation_feedbackMaxDurationReached) {
        localisation_feedbackClock.add(localisation_feedbackMaxDuration);
    } else {
        localisation_feedbackClock.add(0.500000);
    }
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
    byeClock.reset(routineTimer.getTime());
    routineTimer.add(1.000000);
    byeMaxDurationReached = false;
    // update component parameters for each repeat
    psychoJS.experiment.addData('bye.started', globalClock.getTime());
    byeMaxDuration = null
    // keep track of which components have finished
    byeComponents = [];
    byeComponents.push(textbox);
    
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
    
    // *textbox* updates
    if (t >= 0.0 && textbox.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      textbox.tStart = t;  // (not accounting for frame time here)
      textbox.frameNStart = frameN;  // exact frame index
      
      textbox.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 1.0 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (textbox.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      textbox.setAutoDraw(false);
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
    if (byeMaxDurationReached) {
        byeClock.add(byeMaxDuration);
    } else {
        byeClock.add(1.000000);
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
