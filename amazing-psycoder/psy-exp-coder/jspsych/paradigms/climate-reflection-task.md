# Climate Reflection Task — PsychoJS (Online)

> **Parent**: [psy-exp-coder](../../SKILL.md) · [jsPsych/JavaScript Index](index.md)
> **Config reference**: [climate-reflection-task](../../../psy-exp-designer/paradigms/climate-reflection-task.md)
> **Source**: [Pavlovia demos/climate_reflection_task](https://gitlab.pavlovia.org/demos/climate_reflection_task) · PsychoJS (PsychoPy online export)
> **Platform note**: This is PsychoJS code (PsychoPy's JavaScript runtime for online experiments), NOT jsPsych library code.

## Experiment Logic

The Climate Reflection Task is designed to explore how cognitive tasks can encourage engagement with climate change issues. Participants first type answers to a series of open-ended questions about climate change, then read an informational passage, and finally review their previous answers while rating how much they agree with each original response.

The experiment begins with a welcome screen. The first trial loop presents climate change questions from a spreadsheet (`climate_change_questions.xlsx`), and participants type their answers using a text input component. Each answer is stored as `answer.text` in the data output.

After answering all questions, participants read an informational passage about climate change presented as a text stimulus. Then an introduction screen explains the reflection phase. The second loop (`response_loop`) re-presents each question alongside the participant's original answer. A slider component allows participants to rate their agreement with their previous response on a continuous scale.

The experiment concludes with a thank-you screen. The primary data output includes: the original question text, the participant's typed answer, and the agreement rating. This design allows researchers to examine how exposure to climate information may shift participants' attitudes toward their own prior beliefs.

## Key Design Patterns

- **Two-phase reflection design**: typing phase followed by agreement-rating phase, with an informational passage between them
- **Text input component** (`visual.TextBox`) for collecting open-ended typed responses, with Enter key to submit
- **Slider component** for continuous agreement ratings, configured with min/max/start values and visible labels
- **Cross-phase data linkage**: participant's typed answer from phase 1 is stored and re-displayed during phase 2 for reflection
- **Informational passage** presented as a static text routine between phases, serving as the experimental manipulation
- **Comprehensive data logging**: `this_question`, `previous_answer`, and `slider.response` columns saved for each trial

## Code Example

```javascript
// Source: climate_reflection_task (demos/climate_reflection_task)
// Project URL: https://gitlab.pavlovia.org/demos/climate_reflection_task
// Original file: Climate_Reflection_Task.js
﻿/******************************** 
 * Climate_Reflection_Task *
 ********************************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2025.2.0.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'Climate_Reflection_Task';  // from the Builder filename that created this script
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
  color: new util.Color([0.2941, -0.6706, -0.6706]),
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
flowScheduler.add(welcomeRoutineBegin());
flowScheduler.add(welcomeRoutineEachFrame());
flowScheduler.add(welcomeRoutineEnd());
const trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trialsLoopBegin(trialsLoopScheduler));
flowScheduler.add(trialsLoopScheduler);
flowScheduler.add(trialsLoopEnd);


flowScheduler.add(thankyouRoutineBegin());
flowScheduler.add(thankyouRoutineEachFrame());
flowScheduler.add(thankyouRoutineEnd());
flowScheduler.add(passageRoutineBegin());
flowScheduler.add(passageRoutineEachFrame());
flowScheduler.add(passageRoutineEnd());
flowScheduler.add(introRoutineBegin());
flowScheduler.add(introRoutineEachFrame());
flowScheduler.add(introRoutineEnd());
const response_loopLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(response_loopLoopBegin(response_loopLoopScheduler));
flowScheduler.add(response_loopLoopScheduler);
flowScheduler.add(response_loopLoopEnd);


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
    {'name': 'climate_change_questions.xlsx', 'path': 'climate_change_questions.xlsx'},
    {'name': 'background.png', 'path': 'background.png'},
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


var welcomeClock;
var background1;
var welcometxt;
var start_button;
var mouse_5;
var ask_opinionsClock;
var prompt;
var background1_2;
var textbox;
var questiontxt;
var responses;
var submit_button;
var mouse;
var thankyouClock;
var background1_3;
var thankyoutxt;
var next_button;
var mouse_2;
var passageClock;
var background1_4;
var info;
var next_button_2;
var mouse_3;
var introClock;
var background1_5;
var intro3_txt;
var next_button_3;
var mouse_4;
var show_responsesClock;
var background1_6;
var prompt_2;
var questiontxt_2;
var show_textbox_text;
var slider;
var thanksClock;
var background1_7;
var bye_txt;
var end_button;
var mouse_6;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "welcome"
  welcomeClock = new util.Clock();
  background1 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background1', units : undefined, 
    image : 'background.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  welcometxt = new visual.TextBox({
    win: psychoJS.window,
    name: 'welcometxt',
    text: 'Introduction\n\nIn this activity, we will ask you some questions about climate change and your views on the topic. After that, you’ll read a short passage about climate change. Then, we will show you your original answers and ask how much you agree with them, to see if reading the passage has changed your perspective.',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1.5, 0.5],  units: undefined, 
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
    depth: -1.0 
  });
  
  start_button = new visual.TextBox({
    win: psychoJS.window,
    name: 'start_button',
    text: 'START',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, (- 0.4)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.4, 0.1],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: [0.2941, (- 0.6706), (- 0.6706)], borderColor: undefined,
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
  
  mouse_5 = new core.Mouse({
    win: psychoJS.window,
  });
  mouse_5.mouseClock = new util.Clock();
  // Initialize components for Routine "ask_opinions"
  ask_opinionsClock = new util.Clock();
  prompt = new visual.TextBox({
    win: psychoJS.window,
    name: 'prompt',
    text: 'Please type an answer below:',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0.4], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.1],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: 'white', borderColor: 'white',
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
  
  background1_2 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background1_2', units : undefined, 
    image : 'background.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : -1.0 
  });
  textbox = new visual.TextBox({
    win: psychoJS.window,
    name: 'textbox',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0.3, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.5],  units: undefined, 
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
    depth: -2.0 
  });
  
  questiontxt = new visual.TextBox({
    win: psychoJS.window,
    name: 'questiontxt',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [(- 0.3), 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.5],  units: undefined, 
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
    depth: -3.0 
  });
  
  // Run 'Begin Experiment' code from track_responses
  responses = [];
  
  submit_button = new visual.TextBox({
    win: psychoJS.window,
    name: 'submit_button',
    text: 'Click to submit',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, (- 0.4)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.4, 0.1],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: [0.2941, (- 0.6706), (- 0.6706)], borderColor: undefined,
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
  
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  // Initialize components for Routine "thankyou"
  thankyouClock = new util.Clock();
  background1_3 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background1_3', units : undefined, 
    image : 'background.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  thankyoutxt = new visual.TextBox({
    win: psychoJS.window,
    name: 'thankyoutxt',
    text: 'Thank you for answering the questions.\nNow we will show you a brief passage to read about climate change.',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1.5, 0.5],  units: undefined, 
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
    depth: -1.0 
  });
  
  next_button = new visual.TextBox({
    win: psychoJS.window,
    name: 'next_button',
    text: 'NEXT',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, (- 0.4)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.4, 0.1],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: [0.2941, (- 0.6706), (- 0.6706)], borderColor: undefined,
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
  
  mouse_2 = new core.Mouse({
    win: psychoJS.window,
  });
  mouse_2.mouseClock = new util.Clock();
  // Initialize components for Routine "passage"
  passageClock = new util.Clock();
  background1_4 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background1_4', units : undefined, 
    image : 'background.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  info = new visual.TextBox({
    win: psychoJS.window,
    name: 'info',
    text: 'What is Climate Change?\n\nClimate change refers to long-term shifts in global temperatures and weather patterns. While natural factors can influence the climate, today’s rapid changes are largely driven by human activities—especially the burning of fossil fuels, which release greenhouse gases into the atmosphere. These gases trap heat, causing the planet to warm. The effects include more extreme weather events, rising sea levels, disruptions to ecosystems, and risks to human health and livelihoods. Scientists agree that addressing climate change requires both reducing emissions and adapting to the changes already underway.',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1.5, 0.8],  units: undefined, 
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
    depth: -1.0 
  });
  
  next_button_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'next_button_2',
    text: 'NEXT',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, (- 0.4)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.4, 0.1],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: [0.2941, (- 0.6706), (- 0.6706)], borderColor: undefined,
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
  
  mouse_3 = new core.Mouse({
    win: psychoJS.window,
  });
  mouse_3.mouseClock = new util.Clock();
  // Initialize components for Routine "intro"
  introClock = new util.Clock();
  background1_5 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background1_5', units : undefined, 
    image : 'background.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  intro3_txt = new visual.TextBox({
    win: psychoJS.window,
    name: 'intro3_txt',
    text: 'Before, we asked you some questions about climate change.\n\nNow, we will show you the answers you gave. For each one, please tell us how much you agree with your earlier response after reading the passage.',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1.5, 0.5],  units: undefined, 
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
    depth: -1.0 
  });
  
  next_button_3 = new visual.TextBox({
    win: psychoJS.window,
    name: 'next_button_3',
    text: 'NEXT',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, (- 0.4)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.4, 0.1],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: [0.2941, (- 0.6706), (- 0.6706)], borderColor: undefined,
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
  
  mouse_4 = new core.Mouse({
    win: psychoJS.window,
  });
  mouse_4.mouseClock = new util.Clock();
  // Initialize components for Routine "show_responses"
  show_responsesClock = new util.Clock();
  background1_6 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background1_6', units : undefined, 
    image : 'background.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  prompt_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'prompt_2',
    text: 'How much do you agree with your previous statement?',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0.4], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1.5, 0.1],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: 'white', borderColor: 'white',
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
  
  questiontxt_2 = new visual.TextBox({
    win: psychoJS.window,
    name: 'questiontxt_2',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [(- 0.3), (- 0.2)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.5],  units: undefined, 
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
    depth: -2.0 
  });
  
  show_textbox_text = new visual.TextBox({
    win: psychoJS.window,
    name: 'show_textbox_text',
    text: '',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0.3, (- 0.2)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.5],  units: undefined, 
    ori: 0.0,
    color: 'black', colorSpace: 'rgb',
    fillColor: [0.8824, 0.9451, 1.0], borderColor: 'black',
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
  
  slider = new visual.Slider({
    win: psychoJS.window, name: 'slider',
    startValue: undefined,
    size: [1.0, 0.1], pos: [0, 0.3], ori: 0.0, units: psychoJS.window.units,
    labels: ["Strongly \nDisagree", "Strongly\n Agree"], fontSize: 0.03, ticks: [1, 2, 3, 4, 5],
    granularity: 1.0, style: ["RATING"],
    color: new util.Color('black'), markerColor: new util.Color([0.2941, (- 0.6706), (- 0.6706)]), lineColor: new util.Color('White'), 
    opacity: undefined, fontFamily: 'Noto Sans', bold: true, italic: false, depth: -4, 
    flip: false,
  });
  
  // Initialize components for Routine "thanks"
  thanksClock = new util.Clock();
  background1_7 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'background1_7', units : undefined, 
    image : 'background.png', mask : undefined,
    anchor : 'center',
    ori : 0.0, 
    pos : [0, 0], 
    draggable: false,
    size : [1.7, 1],
    color : new util.Color([1,1,1]), opacity : undefined,
    flipHoriz : false, flipVert : false,
    texRes : 128.0, interpolate : true, depth : 0.0 
  });
  bye_txt = new visual.TextBox({
    win: psychoJS.window,
    name: 'bye_txt',
    text: 'Thanks for taking part!',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, 0], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [1.5, 0.5],  units: undefined, 
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
    depth: -1.0 
  });
  
  end_button = new visual.TextBox({
    win: psychoJS.window,
    name: 'end_button',
    text: 'END',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0, (- 0.4)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.4, 0.1],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: [0.2941, (- 0.6706), (- 0.6706)], borderColor: undefined,
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
  
  mouse_6 = new core.Mouse({
    win: psychoJS.window,
  });
  mouse_6.mouseClock = new util.Clock();
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}


var t;
var frameN;
var continueRoutine;
var routineForceEnded;
var welcomeMaxDurationReached;
var gotValidClick;
var welcomeMaxDuration;
var welcomeComponents;
function welcomeRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'welcome' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    welcomeClock.reset();
    routineTimer.reset();
    welcomeMaxDurationReached = false;
    // update component parameters for each repeat
    // setup some python lists for storing info about the mouse_5
    // current position of the mouse:
    mouse_5.x = [];
    mouse_5.y = [];
    mouse_5.leftButton = [];
    mouse_5.midButton = [];
    mouse_5.rightButton = [];
    mouse_5.time = [];
    mouse_5.clicked_name = [];
    gotValidClick = false; // until a click is received
    psychoJS.experiment.addData('welcome.started', globalClock.getTime());
    welcomeMaxDuration = null
    // keep track of which components have finished
    welcomeComponents = [];
    welcomeComponents.push(background1);
    welcomeComponents.push(welcometxt);
    welcomeComponents.push(start_button);
    welcomeComponents.push(mouse_5);
    
    for (const thisComponent of welcomeComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var prevButtonState;
var _mouseButtons;
var _mouseXYs;
function welcomeRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'welcome' ---
    // get current time
    t = welcomeClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background1* updates
    if (t >= 0.0 && background1.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background1.tStart = t;  // (not accounting for frame time here)
      background1.frameNStart = frameN;  // exact frame index
      
      background1.setAutoDraw(true);
    }
    
    
    // if background1 is active this frame...
    if (background1.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *welcometxt* updates
    if (t >= 0.0 && welcometxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      welcometxt.tStart = t;  // (not accounting for frame time here)
      welcometxt.frameNStart = frameN;  // exact frame index
      
      welcometxt.setAutoDraw(true);
    }
    
    
    // if welcometxt is active this frame...
    if (welcometxt.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *start_button* updates
    if (t >= 0.0 && start_button.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      start_button.tStart = t;  // (not accounting for frame time here)
      start_button.frameNStart = frameN;  // exact frame index
      
      start_button.setAutoDraw(true);
    }
    
    
    // if start_button is active this frame...
    if (start_button.status === PsychoJS.Status.STARTED) {
    }
    
    // *mouse_5* updates
    if (t >= 0.0 && mouse_5.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      mouse_5.tStart = t;  // (not accounting for frame time here)
      mouse_5.frameNStart = frameN;  // exact frame index
      
      mouse_5.status = PsychoJS.Status.STARTED;
      mouse_5.mouseClock.reset();
      prevButtonState = mouse_5.getPressed();  // if button is down already this ISN'T a new click
    }
    
    // if mouse_5 is active this frame...
    if (mouse_5.status === PsychoJS.Status.STARTED) {
      _mouseButtons = mouse_5.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          mouse_5.clickableObjects = eval(start_button)
          ;// make sure the mouse's clickable objects are an array
          if (!Array.isArray(mouse_5.clickableObjects)) {
              mouse_5.clickableObjects = [mouse_5.clickableObjects];
          }
          // iterate through clickable objects and check each
          for (const obj of mouse_5.clickableObjects) {
              if (obj.contains(mouse_5)) {
                  gotValidClick = true;
                  mouse_5.clicked_name.push(obj.name);
              }
          }
          if (!gotValidClick) {
              mouse_5.clicked_name.push(null);
          }
          _mouseXYs = mouse_5.getPos();
          mouse_5.x.push(_mouseXYs[0]);
          mouse_5.y.push(_mouseXYs[1]);
          mouse_5.leftButton.push(_mouseButtons[0]);
          mouse_5.midButton.push(_mouseButtons[1]);
          mouse_5.rightButton.push(_mouseButtons[2]);
          mouse_5.time.push(mouse_5.mouseClock.getTime());
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
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of welcomeComponents)
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


function welcomeRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'welcome' ---
    for (const thisComponent of welcomeComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('welcome.stopped', globalClock.getTime());
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse_5.x', mouse_5.x);
    psychoJS.experiment.addData('mouse_5.y', mouse_5.y);
    psychoJS.experiment.addData('mouse_5.leftButton', mouse_5.leftButton);
    psychoJS.experiment.addData('mouse_5.midButton', mouse_5.midButton);
    psychoJS.experiment.addData('mouse_5.rightButton', mouse_5.rightButton);
    psychoJS.experiment.addData('mouse_5.time', mouse_5.time);
    psychoJS.experiment.addData('mouse_5.clicked_name', mouse_5.clicked_name);
    
    // the Routine "welcome" was not non-slip safe, so reset the non-slip timer
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
      trialList: 'climate_change_questions.xlsx',
      seed: undefined, name: 'trials'
    });
    psychoJS.experiment.addLoop(trials); // add the loop to the experiment
    currentLoop = trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisTrial of trials) {
      snapshot = trials.getSnapshot();
      trialsLoopScheduler.add(importConditions(snapshot));
      trialsLoopScheduler.add(ask_opinionsRoutineBegin(snapshot));
      trialsLoopScheduler.add(ask_opinionsRoutineEachFrame());
      trialsLoopScheduler.add(ask_opinionsRoutineEnd(snapshot));
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


var response_loop;
function response_loopLoopBegin(response_loopLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    response_loop = new TrialHandler({
      psychoJS: psychoJS,
      nReps: n_responses , method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: undefined,
      seed: undefined, name: 'response_loop'
    });
    psychoJS.experiment.addLoop(response_loop); // add the loop to the experiment
    currentLoop = response_loop;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisResponse_loop of response_loop) {
      snapshot = response_loop.getSnapshot();
      response_loopLoopScheduler.add(importConditions(snapshot));
      response_loopLoopScheduler.add(show_responsesRoutineBegin(snapshot));
      response_loopLoopScheduler.add(show_responsesRoutineEachFrame());
      response_loopLoopScheduler.add(show_responsesRoutineEnd(snapshot));
      response_loopLoopScheduler.add(response_loopLoopEndIteration(response_loopLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}


async function response_loopLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(response_loop);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function response_loopLoopEndIteration(scheduler, snapshot) {
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


var ask_opinionsMaxDurationReached;
var ask_opinionsMaxDuration;
var ask_opinionsComponents;
function ask_opinionsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'ask_opinions' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    ask_opinionsClock.reset();
    routineTimer.reset();
    ask_opinionsMaxDurationReached = false;
    // update component parameters for each repeat
    textbox.setText('');
    textbox.refresh();
    questiontxt.setText(this_question);
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
    psychoJS.experiment.addData('ask_opinions.started', globalClock.getTime());
    ask_opinionsMaxDuration = null
    // keep track of which components have finished
    ask_opinionsComponents = [];
    ask_opinionsComponents.push(prompt);
    ask_opinionsComponents.push(background1_2);
    ask_opinionsComponents.push(textbox);
    ask_opinionsComponents.push(questiontxt);
    ask_opinionsComponents.push(submit_button);
    ask_opinionsComponents.push(mouse);
    
    for (const thisComponent of ask_opinionsComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function ask_opinionsRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'ask_opinions' ---
    // get current time
    t = ask_opinionsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *prompt* updates
    if (t >= 0.0 && prompt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      prompt.tStart = t;  // (not accounting for frame time here)
      prompt.frameNStart = frameN;  // exact frame index
      
      prompt.setAutoDraw(true);
    }
    
    
    // if prompt is active this frame...
    if (prompt.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *background1_2* updates
    if (t >= 0.0 && background1_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background1_2.tStart = t;  // (not accounting for frame time here)
      background1_2.frameNStart = frameN;  // exact frame index
      
      background1_2.setAutoDraw(true);
    }
    
    
    // if background1_2 is active this frame...
    if (background1_2.status === PsychoJS.Status.STARTED) {
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
    
    
    // *questiontxt* updates
    if (t >= 0.0 && questiontxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      questiontxt.tStart = t;  // (not accounting for frame time here)
      questiontxt.frameNStart = frameN;  // exact frame index
      
      questiontxt.setAutoDraw(true);
    }
    
    
    // if questiontxt is active this frame...
    if (questiontxt.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *submit_button* updates
    if (t >= 0.0 && submit_button.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      submit_button.tStart = t;  // (not accounting for frame time here)
      submit_button.frameNStart = frameN;  // exact frame index
      
      submit_button.setAutoDraw(true);
    }
    
    
    // if submit_button is active this frame...
    if (submit_button.status === PsychoJS.Status.STARTED) {
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
          mouse.clickableObjects = eval(submit_button)
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
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of ask_opinionsComponents)
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


var n_responses;
function ask_opinionsRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'ask_opinions' ---
    for (const thisComponent of ask_opinionsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('ask_opinions.stopped', globalClock.getTime());
    psychoJS.experiment.addData('textbox.text',textbox.text)
    // Run 'End Routine' code from track_responses
    responses.push({"question": this_question, "answer": textbox.text});
    n_responses = responses.length;
    
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse.x', mouse.x);
    psychoJS.experiment.addData('mouse.y', mouse.y);
    psychoJS.experiment.addData('mouse.leftButton', mouse.leftButton);
    psychoJS.experiment.addData('mouse.midButton', mouse.midButton);
    psychoJS.experiment.addData('mouse.rightButton', mouse.rightButton);
    psychoJS.experiment.addData('mouse.time', mouse.time);
    psychoJS.experiment.addData('mouse.clicked_name', mouse.clicked_name);
    
    // the Routine "ask_opinions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var thankyouMaxDurationReached;
var thankyouMaxDuration;
var thankyouComponents;
function thankyouRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'thankyou' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    thankyouClock.reset();
    routineTimer.reset();
    thankyouMaxDurationReached = false;
    // update component parameters for each repeat
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
    psychoJS.experiment.addData('thankyou.started', globalClock.getTime());
    thankyouMaxDuration = null
    // keep track of which components have finished
    thankyouComponents = [];
    thankyouComponents.push(background1_3);
    thankyouComponents.push(thankyoutxt);
    thankyouComponents.push(next_button);
    thankyouComponents.push(mouse_2);
    
    for (const thisComponent of thankyouComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function thankyouRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'thankyou' ---
    // get current time
    t = thankyouClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background1_3* updates
    if (t >= 0.0 && background1_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background1_3.tStart = t;  // (not accounting for frame time here)
      background1_3.frameNStart = frameN;  // exact frame index
      
      background1_3.setAutoDraw(true);
    }
    
    
    // if background1_3 is active this frame...
    if (background1_3.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *thankyoutxt* updates
    if (t >= 0.0 && thankyoutxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      thankyoutxt.tStart = t;  // (not accounting for frame time here)
      thankyoutxt.frameNStart = frameN;  // exact frame index
      
      thankyoutxt.setAutoDraw(true);
    }
    
    
    // if thankyoutxt is active this frame...
    if (thankyoutxt.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *next_button* updates
    if (t >= 0.0 && next_button.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      next_button.tStart = t;  // (not accounting for frame time here)
      next_button.frameNStart = frameN;  // exact frame index
      
      next_button.setAutoDraw(true);
    }
    
    
    // if next_button is active this frame...
    if (next_button.status === PsychoJS.Status.STARTED) {
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
    
    // if mouse_2 is active this frame...
    if (mouse_2.status === PsychoJS.Status.STARTED) {
      _mouseButtons = mouse_2.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          mouse_2.clickableObjects = eval(next_button)
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
          if (!gotValidClick) {
              mouse_2.clicked_name.push(null);
          }
          _mouseXYs = mouse_2.getPos();
          mouse_2.x.push(_mouseXYs[0]);
          mouse_2.y.push(_mouseXYs[1]);
          mouse_2.leftButton.push(_mouseButtons[0]);
          mouse_2.midButton.push(_mouseButtons[1]);
          mouse_2.rightButton.push(_mouseButtons[2]);
          mouse_2.time.push(mouse_2.mouseClock.getTime());
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
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of thankyouComponents)
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


function thankyouRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'thankyou' ---
    for (const thisComponent of thankyouComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('thankyou.stopped', globalClock.getTime());
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse_2.x', mouse_2.x);
    psychoJS.experiment.addData('mouse_2.y', mouse_2.y);
    psychoJS.experiment.addData('mouse_2.leftButton', mouse_2.leftButton);
    psychoJS.experiment.addData('mouse_2.midButton', mouse_2.midButton);
    psychoJS.experiment.addData('mouse_2.rightButton', mouse_2.rightButton);
    psychoJS.experiment.addData('mouse_2.time', mouse_2.time);
    psychoJS.experiment.addData('mouse_2.clicked_name', mouse_2.clicked_name);
    
    // the Routine "thankyou" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var passageMaxDurationReached;
var passageMaxDuration;
var passageComponents;
function passageRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'passage' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    passageClock.reset();
    routineTimer.reset();
    passageMaxDurationReached = false;
    // update component parameters for each repeat
    // setup some python lists for storing info about the mouse_3
    // current position of the mouse:
    mouse_3.x = [];
    mouse_3.y = [];
    mouse_3.leftButton = [];
    mouse_3.midButton = [];
    mouse_3.rightButton = [];
    mouse_3.time = [];
    mouse_3.clicked_name = [];
    gotValidClick = false; // until a click is received
    psychoJS.experiment.addData('passage.started', globalClock.getTime());
    passageMaxDuration = null
    // keep track of which components have finished
    passageComponents = [];
    passageComponents.push(background1_4);
    passageComponents.push(info);
    passageComponents.push(next_button_2);
    passageComponents.push(mouse_3);
    
    for (const thisComponent of passageComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function passageRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'passage' ---
    // get current time
    t = passageClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background1_4* updates
    if (t >= 0.0 && background1_4.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background1_4.tStart = t;  // (not accounting for frame time here)
      background1_4.frameNStart = frameN;  // exact frame index
      
      background1_4.setAutoDraw(true);
    }
    
    
    // if background1_4 is active this frame...
    if (background1_4.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *info* updates
    if (t >= 0.0 && info.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      info.tStart = t;  // (not accounting for frame time here)
      info.frameNStart = frameN;  // exact frame index
      
      info.setAutoDraw(true);
    }
    
    
    // if info is active this frame...
    if (info.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *next_button_2* updates
    if (t >= 0.0 && next_button_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      next_button_2.tStart = t;  // (not accounting for frame time here)
      next_button_2.frameNStart = frameN;  // exact frame index
      
      next_button_2.setAutoDraw(true);
    }
    
    
    // if next_button_2 is active this frame...
    if (next_button_2.status === PsychoJS.Status.STARTED) {
    }
    
    // *mouse_3* updates
    if (t >= 0.0 && mouse_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      mouse_3.tStart = t;  // (not accounting for frame time here)
      mouse_3.frameNStart = frameN;  // exact frame index
      
      mouse_3.status = PsychoJS.Status.STARTED;
      mouse_3.mouseClock.reset();
      prevButtonState = mouse_3.getPressed();  // if button is down already this ISN'T a new click
    }
    
    // if mouse_3 is active this frame...
    if (mouse_3.status === PsychoJS.Status.STARTED) {
      _mouseButtons = mouse_3.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          mouse_3.clickableObjects = eval(next_button_2)
          ;// make sure the mouse's clickable objects are an array
          if (!Array.isArray(mouse_3.clickableObjects)) {
              mouse_3.clickableObjects = [mouse_3.clickableObjects];
          }
          // iterate through clickable objects and check each
          for (const obj of mouse_3.clickableObjects) {
              if (obj.contains(mouse_3)) {
                  gotValidClick = true;
                  mouse_3.clicked_name.push(obj.name);
              }
          }
          if (!gotValidClick) {
              mouse_3.clicked_name.push(null);
          }
          _mouseXYs = mouse_3.getPos();
          mouse_3.x.push(_mouseXYs[0]);
          mouse_3.y.push(_mouseXYs[1]);
          mouse_3.leftButton.push(_mouseButtons[0]);
          mouse_3.midButton.push(_mouseButtons[1]);
          mouse_3.rightButton.push(_mouseButtons[2]);
          mouse_3.time.push(mouse_3.mouseClock.getTime());
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
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of passageComponents)
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


function passageRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'passage' ---
    for (const thisComponent of passageComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('passage.stopped', globalClock.getTime());
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse_3.x', mouse_3.x);
    psychoJS.experiment.addData('mouse_3.y', mouse_3.y);
    psychoJS.experiment.addData('mouse_3.leftButton', mouse_3.leftButton);
    psychoJS.experiment.addData('mouse_3.midButton', mouse_3.midButton);
    psychoJS.experiment.addData('mouse_3.rightButton', mouse_3.rightButton);
    psychoJS.experiment.addData('mouse_3.time', mouse_3.time);
    psychoJS.experiment.addData('mouse_3.clicked_name', mouse_3.clicked_name);
    
    // the Routine "passage" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var introMaxDurationReached;
var introMaxDuration;
var introComponents;
function introRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'intro' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    introClock.reset();
    routineTimer.reset();
    introMaxDurationReached = false;
    // update component parameters for each repeat
    // setup some python lists for storing info about the mouse_4
    // current position of the mouse:
    mouse_4.x = [];
    mouse_4.y = [];
    mouse_4.leftButton = [];
    mouse_4.midButton = [];
    mouse_4.rightButton = [];
    mouse_4.time = [];
    mouse_4.clicked_name = [];
    gotValidClick = false; // until a click is received
    psychoJS.experiment.addData('intro.started', globalClock.getTime());
    introMaxDuration = null
    // keep track of which components have finished
    introComponents = [];
    introComponents.push(background1_5);
    introComponents.push(intro3_txt);
    introComponents.push(next_button_3);
    introComponents.push(mouse_4);
    
    for (const thisComponent of introComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function introRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'intro' ---
    // get current time
    t = introClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background1_5* updates
    if (t >= 0.0 && background1_5.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background1_5.tStart = t;  // (not accounting for frame time here)
      background1_5.frameNStart = frameN;  // exact frame index
      
      background1_5.setAutoDraw(true);
    }
    
    
    // if background1_5 is active this frame...
    if (background1_5.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *intro3_txt* updates
    if (t >= 0.0 && intro3_txt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      intro3_txt.tStart = t;  // (not accounting for frame time here)
      intro3_txt.frameNStart = frameN;  // exact frame index
      
      intro3_txt.setAutoDraw(true);
    }
    
    
    // if intro3_txt is active this frame...
    if (intro3_txt.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *next_button_3* updates
    if (t >= 0.0 && next_button_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      next_button_3.tStart = t;  // (not accounting for frame time here)
      next_button_3.frameNStart = frameN;  // exact frame index
      
      next_button_3.setAutoDraw(true);
    }
    
    
    // if next_button_3 is active this frame...
    if (next_button_3.status === PsychoJS.Status.STARTED) {
    }
    
    // *mouse_4* updates
    if (t >= 0.0 && mouse_4.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      mouse_4.tStart = t;  // (not accounting for frame time here)
      mouse_4.frameNStart = frameN;  // exact frame index
      
      mouse_4.status = PsychoJS.Status.STARTED;
      mouse_4.mouseClock.reset();
      prevButtonState = mouse_4.getPressed();  // if button is down already this ISN'T a new click
    }
    
    // if mouse_4 is active this frame...
    if (mouse_4.status === PsychoJS.Status.STARTED) {
      _mouseButtons = mouse_4.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          mouse_4.clickableObjects = eval(next_button)
          ;// make sure the mouse's clickable objects are an array
          if (!Array.isArray(mouse_4.clickableObjects)) {
              mouse_4.clickableObjects = [mouse_4.clickableObjects];
          }
          // iterate through clickable objects and check each
          for (const obj of mouse_4.clickableObjects) {
              if (obj.contains(mouse_4)) {
                  gotValidClick = true;
                  mouse_4.clicked_name.push(obj.name);
              }
          }
          if (!gotValidClick) {
              mouse_4.clicked_name.push(null);
          }
          _mouseXYs = mouse_4.getPos();
          mouse_4.x.push(_mouseXYs[0]);
          mouse_4.y.push(_mouseXYs[1]);
          mouse_4.leftButton.push(_mouseButtons[0]);
          mouse_4.midButton.push(_mouseButtons[1]);
          mouse_4.rightButton.push(_mouseButtons[2]);
          mouse_4.time.push(mouse_4.mouseClock.getTime());
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
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of introComponents)
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


function introRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'intro' ---
    for (const thisComponent of introComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('intro.stopped', globalClock.getTime());
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse_4.x', mouse_4.x);
    psychoJS.experiment.addData('mouse_4.y', mouse_4.y);
    psychoJS.experiment.addData('mouse_4.leftButton', mouse_4.leftButton);
    psychoJS.experiment.addData('mouse_4.midButton', mouse_4.midButton);
    psychoJS.experiment.addData('mouse_4.rightButton', mouse_4.rightButton);
    psychoJS.experiment.addData('mouse_4.time', mouse_4.time);
    psychoJS.experiment.addData('mouse_4.clicked_name', mouse_4.clicked_name);
    
    // the Routine "intro" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var show_responsesMaxDurationReached;
var show_responsesMaxDuration;
var show_responsesComponents;
function show_responsesRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'show_responses' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    show_responsesClock.reset();
    routineTimer.reset();
    show_responsesMaxDurationReached = false;
    // update component parameters for each repeat
    questiontxt_2.setText(responses[response_loop.thisN]["question"]);
    show_textbox_text.setText(responses[response_loop.thisN]["answer"]);
    slider.reset()
    // Run 'Begin Routine' code from code
    psychoJS.experiment.addData("previous_answer", responses[response_loop.thisN]["answer"]);
    
    psychoJS.experiment.addData('show_responses.started', globalClock.getTime());
    show_responsesMaxDuration = null
    // keep track of which components have finished
    show_responsesComponents = [];
    show_responsesComponents.push(background1_6);
    show_responsesComponents.push(prompt_2);
    show_responsesComponents.push(questiontxt_2);
    show_responsesComponents.push(show_textbox_text);
    show_responsesComponents.push(slider);
    
    for (const thisComponent of show_responsesComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function show_responsesRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'show_responses' ---
    // get current time
    t = show_responsesClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *background1_6* updates
    if (t >= 0.0 && background1_6.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background1_6.tStart = t;  // (not accounting for frame time here)
      background1_6.frameNStart = frameN;  // exact frame index
      
      background1_6.setAutoDraw(true);
    }
    
    
    // if background1_6 is active this frame...
    if (background1_6.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *prompt_2* updates
    if (t >= 0.0 && prompt_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      prompt_2.tStart = t;  // (not accounting for frame time here)
      prompt_2.frameNStart = frameN;  // exact frame index
      
      prompt_2.setAutoDraw(true);
    }
    
    
    // if prompt_2 is active this frame...
    if (prompt_2.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *questiontxt_2* updates
    if (t >= 0.0 && questiontxt_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      questiontxt_2.tStart = t;  // (not accounting for frame time here)
      questiontxt_2.frameNStart = frameN;  // exact frame index
      
      questiontxt_2.setAutoDraw(true);
    }
    
    
    // if questiontxt_2 is active this frame...
    if (questiontxt_2.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *show_textbox_text* updates
    if (t >= 0.0 && show_textbox_text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      show_textbox_text.tStart = t;  // (not accounting for frame time here)
      show_textbox_text.frameNStart = frameN;  // exact frame index
      
      show_textbox_text.setAutoDraw(true);
    }
    
    
    // if show_textbox_text is active this frame...
    if (show_textbox_text.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *slider* updates
    if (t >= 0.0 && slider.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      slider.tStart = t;  // (not accounting for frame time here)
      slider.frameNStart = frameN;  // exact frame index
      
      slider.setAutoDraw(true);
    }
    
    
    // if slider is active this frame...
    if (slider.status === PsychoJS.Status.STARTED) {
    }
    
    
    // Check slider for response to end Routine
    if (slider.getRating() !== undefined && slider.status === PsychoJS.Status.STARTED) {
      continueRoutine = false; }
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
    for (const thisComponent of show_responsesComponents)
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


function show_responsesRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'show_responses' ---
    for (const thisComponent of show_responsesComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('show_responses.stopped', globalClock.getTime());
    psychoJS.experiment.addData('slider.response', slider.getRating());
    psychoJS.experiment.addData('slider.rt', slider.getRT());
    // the Routine "show_responses" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
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
    thanksClock.reset();
    routineTimer.reset();
    thanksMaxDurationReached = false;
    // update component parameters for each repeat
    // setup some python lists for storing info about the mouse_6
    // current position of the mouse:
    mouse_6.x = [];
    mouse_6.y = [];
    mouse_6.leftButton = [];
    mouse_6.midButton = [];
    mouse_6.rightButton = [];
    mouse_6.time = [];
    mouse_6.clicked_name = [];
    gotValidClick = false; // until a click is received
    psychoJS.experiment.addData('thanks.started', globalClock.getTime());
    thanksMaxDuration = null
    // keep track of which components have finished
    thanksComponents = [];
    thanksComponents.push(background1_7);
    thanksComponents.push(bye_txt);
    thanksComponents.push(end_button);
    thanksComponents.push(mouse_6);
    
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
    
    // *background1_7* updates
    if (t >= 0.0 && background1_7.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      background1_7.tStart = t;  // (not accounting for frame time here)
      background1_7.frameNStart = frameN;  // exact frame index
      
      background1_7.setAutoDraw(true);
    }
    
    
    // if background1_7 is active this frame...
    if (background1_7.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *bye_txt* updates
    if (t >= 0.0 && bye_txt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      bye_txt.tStart = t;  // (not accounting for frame time here)
      bye_txt.frameNStart = frameN;  // exact frame index
      
      bye_txt.setAutoDraw(true);
    }
    
    
    // if bye_txt is active this frame...
    if (bye_txt.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *end_button* updates
    if (t >= 0.0 && end_button.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      end_button.tStart = t;  // (not accounting for frame time here)
      end_button.frameNStart = frameN;  // exact frame index
      
      end_button.setAutoDraw(true);
    }
    
    
    // if end_button is active this frame...
    if (end_button.status === PsychoJS.Status.STARTED) {
    }
    
    // *mouse_6* updates
    if (t >= 0.0 && mouse_6.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      mouse_6.tStart = t;  // (not accounting for frame time here)
      mouse_6.frameNStart = frameN;  // exact frame index
      
      mouse_6.status = PsychoJS.Status.STARTED;
      mouse_6.mouseClock.reset();
      prevButtonState = mouse_6.getPressed();  // if button is down already this ISN'T a new click
    }
    
    // if mouse_6 is active this frame...
    if (mouse_6.status === PsychoJS.Status.STARTED) {
      _mouseButtons = mouse_6.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          mouse_6.clickableObjects = eval(end_button)
          ;// make sure the mouse's clickable objects are an array
          if (!Array.isArray(mouse_6.clickableObjects)) {
              mouse_6.clickableObjects = [mouse_6.clickableObjects];
          }
          // iterate through clickable objects and check each
          for (const obj of mouse_6.clickableObjects) {
              if (obj.contains(mouse_6)) {
                  gotValidClick = true;
                  mouse_6.clicked_name.push(obj.name);
              }
          }
          if (!gotValidClick) {
              mouse_6.clicked_name.push(null);
          }
          _mouseXYs = mouse_6.getPos();
          mouse_6.x.push(_mouseXYs[0]);
          mouse_6.y.push(_mouseXYs[1]);
          mouse_6.leftButton.push(_mouseButtons[0]);
          mouse_6.midButton.push(_mouseButtons[1]);
          mouse_6.rightButton.push(_mouseButtons[2]);
          mouse_6.time.push(mouse_6.mouseClock.getTime());
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
    if (continueRoutine) {
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
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse_6.x', mouse_6.x);
    psychoJS.experiment.addData('mouse_6.y', mouse_6.y);
    psychoJS.experiment.addData('mouse_6.leftButton', mouse_6.leftButton);
    psychoJS.experiment.addData('mouse_6.midButton', mouse_6.midButton);
    psychoJS.experiment.addData('mouse_6.rightButton', mouse_6.rightButton);
    psychoJS.experiment.addData('mouse_6.time', mouse_6.time);
    psychoJS.experiment.addData('mouse_6.clicked_name', mouse_6.clicked_name);
    
    // the Routine "thanks" was not non-slip safe, so reset the non-slip timer
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
