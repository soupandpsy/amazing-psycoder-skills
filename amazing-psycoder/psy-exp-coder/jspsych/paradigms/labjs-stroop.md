# Stroop Task (lab.js) — PsychoJS (Online)

> **Parent**: [psy-exp-coder](../../SKILL.md) · [jsPsych/JavaScript Index](index.md)
> **Config reference**: [stroop](../../../psy-exp-designer/paradigms/stroop.md)
> **Source**: [Pavlovia demos/labjs_stroop](https://gitlab.pavlovia.org/demos/labjs_stroop) · PsychoJS (PsychoPy online export)
> **Platform note**: This is PsychoJS code (PsychoPy's JavaScript runtime for online experiments), NOT jsPsych library code.

## Experiment Logic

This is a Stroop task implemented using lab.js, a JavaScript library for building web-based experiments. Unlike the PsychoJS examples, this uses the lab.js framework with its HTML-based templating system for stimulus presentation and response collection.

The experiment presents color words (red, green, blue, orange) displayed in colored text. On congruent trials, the word matches its ink color (e.g., "red" in red); on incongruent trials, the word conflicts with its ink color (e.g., "red" in green). Participants press keys (r, g, b, o) to indicate the ink color while ignoring the word meaning.

Each trial consists of three screens: a fixation cross (500ms), the Stroop stimulus (1500ms max, response-terminated), and a feedback screen (variable duration). The paradigm uses a lab.js `Loop` with `templateParameters` defining all 16 possible color-word combinations. Practice trials include feedback; experimental trials do not.

The experiment flow includes welcome, summary, practice, interlude, main trials, and thank-you screens. The lab.js `Pavlovia` plugin handles data storage. The template pattern separates stimulus logic from experiment flow, with `messageHandlers` for dynamic content generation and `datacommit` control for selective data logging.

## Key Design Patterns

- **lab.js framework** (not PsychoJS): uses `lab.flow.Sequence`, `lab.html.Screen`, and `lab.flow.Loop` for experiment structure
- **HTML template-based rendering**: stimuli displayed via `contentUrl: 'pages/3-trial.html'` with dynamic `parameters` passed to HTML templates
- **`messageHandlers` pattern**: `before:prepare` callback dynamically sets correct response based on trial parameters
- **Template reuse**: same trial template used for practice and experimental blocks with different `parameters` (feedback: true/false)
- **`Pavlovia` plugin** for data storage integration with the Pavlovia platform
- **Selective data logging**: `datacommit: false` on fixation and feedback screens to exclude non-trial data from output

## Code Example

```javascript
// Source: labjs_stroop (demos/labjs_stroop)
// Project URL: https://gitlab.pavlovia.org/demos/labjs_stroop
// Original file: experiment.js
// Stroop task example with lab.js
// Initial implementation by Felix Henninger


// Define a template for a stroop trial
var trialTemplate = new lab.flow.Sequence({
  datacommit: false,
  content: [
    // Fixation cross ----------------------------------------------------------
    // This screen uses the trial page template,
    // but substitutes a gray plus as a fixation cross
    new lab.html.Screen({
      contentUrl: 'pages/3-trial.html',
      parameters: {
        color: 'gray',
        word: '+',
        weight: 'normal',
      },
      // Don't log data from this screen
      datacommit: false,
      // Display the fixation cross for 500ms
      timeout: 500,
    }),
    // Trial screen ------------------------------------------------------------
    // This is the central screen in the experiment:
    // the display that participants respond to.
    new lab.html.Screen({
      // This screen is assigned a title,
      // so that we can recognize it more easily
      // in the dataset.
      title: 'StroopScreen',
      // Again, we use the trial page template
      contentUrl: 'pages/3-trial.html',
      parameters: {
        // Color and displayed word
        // are determined by the trial
        weight: 'bold',
      },
      // Each possible color response is
      // associated with a key
      responses: {
        'keypress(r)': 'red',
        'keypress(g)': 'green',
        'keypress(b)': 'blue',
        'keypress(o)': 'orange',
      },
      // The display terminates after 1500ms
      timeout: 1500,
      // Because the color is set dynamically,
      // we need to set the correct response by hand
      messageHandlers: {
        'before:prepare': function() {
          // Set the correct response
          // before the component is prepared
          this.options.correctResponse = this.aggregateParameters.color
        },
      }
    }),
    // Feedback (or empty) screen ----------------------------------------------
    new lab.html.Screen({
      contentUrl: 'pages/3-trial.html',
      parameters: {
        color: 'gray',
        word: '', // This is a placeholder, we generate the word below
        weight: 'normal',
      },
      datacommit: false,
      // Because feedback can only be given after
      // the choice has been recorded, this component
      // is prepared at the last possible moment.
      tardy: true,
      // Generate feedback
      messageHandlers: {
        'before:prepare': function() {
          if (this.aggregateParameters.feedback) {
            // Generate feedback if requested
            this.options.timeout = 1000;

            // First, check if the participant responded in time at all
            if (this.options.datastore.state['ended_on'] === 'response') {
              // If there is a response, check its veracity
              if (this.options.datastore.state['correct'] === true) {
                this.options.parameters.word = 'Well done!'
              } else {
                this.options.parameters.word = 'Please respond as quickly and accurately as you can!'
              }
            } else {
              // If no response was given, poke participants to speed up
              this.options.parameters.word = 'Can you go faster?'
            }
          } else {
            // If no feedback is shown, shorten the inter-trial interval
            this.options.timeout = 500
          }
        }
      },
    }),
  ]
})

// Define the trials in terms of the central parameters:
// The word shown on screen, and its color
var trials = [
  { color: 'red', word: 'red' },
  { color: 'red', word: 'green' },
  { color: 'red', word: 'blue' },
  { color: 'red', word: 'orange' },
  { color: 'green', word: 'red' },
  { color: 'green', word: 'green' },
  { color: 'green', word: 'blue' },
  { color: 'green', word: 'orange' },
  { color: 'blue', word: 'red' },
  { color: 'blue', word: 'green' },
  { color: 'blue', word: 'blue' },
  { color: 'blue', word: 'orange' },
  { color: 'orange', word: 'red' },
  { color: 'orange', word: 'green' },
  { color: 'orange', word: 'blue' },
  { color: 'orange', word: 'orange' },
]

// With the individual components in place,
// now put together the entire experiment
var experiment = new lab.flow.Sequence({
  // pavlovia plugin
  plugins: [ new Pavlovia() ],

  content: [
    // Initial instructions
    new lab.html.Screen({
      contentUrl: 'pages/1-welcome.html',
      responses: {
        'keypress(Space)': 'continue'
      },
    }),
    // Instruction summary
    new lab.html.Screen({
      contentUrl: 'pages/2-summary.html',
      responses: {
        'keypress(Space)': 'continue'
      },
    }),
    // Practice trials
    new lab.flow.Loop({
      template: trialTemplate,
      templateParameters: trials,
      shuffle: true,
      parameters: {
        feedback: true,
      },
    }),
    // Interlude
    new lab.html.Screen({
      contentUrl: 'pages/4-interlude.html',
      responses: {
        'keypress(Space)': 'continue',
      },
    }),
    // Actual trials
    new lab.flow.Loop({
      template: trialTemplate,
      templateParameters: trials,
      shuffle: true,
      parameters: {
        feedback: false,
      },
    }),
    // Thank-you page
    new lab.html.Screen({
      contentUrl: 'pages/5-thanks.html',
      // Respond to clicks on the download button
      events: {
        'click button#download': function() {
          //this.options.datastore.download();

          // the component must end so the experiment can end and alert the pavlovia plugin:
          this.end();
        },
      }
    }),
  ],
  datastore: new lab.data.Store()
});

// Go!
experiment.run();

```
