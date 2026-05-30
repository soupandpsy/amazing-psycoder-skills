# Phone a Friend Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/phone_a_friend) · reference

## When to Use

User mentions: Phone a friend, hint task, cue validity, general knowledge task, ECSoP, 朋友求助任务. A general knowledge task where participants can optionally request hints ("phone a friend"), with half of the hints being correct and half incorrect. Measures trust in external information and the influence of cue validity on belief updating.

## Core Logic

Participants are presented with a series of general knowledge questions and respond by typing an answer. On each question, they may choose to "phone a friend" to receive a hint. Each participant has exactly 10 hint opportunities across the entire task, of which 5 hints are valid (correct) and 5 are invalid (incorrect), randomly interleaved. After receiving a hint, the participant may revise their answer.

The critical manipulation is the validity of the hints: participants do not know in advance whether a given hint is correct or incorrect, so they must decide when to trust external information. The task tracks whether participants are more likely to request hints for difficult questions, whether they incorporate hints into their answers, and whether they detect that some hints are systematically incorrect.

On each trial, participants see a question, an editable textbox for typing their answer, a "Phone a friend" button, and a call tracker showing remaining hints. The trial is open-ended: participants can either type an answer and press Enter to submit, or click the hint button to request a hint. If a hint is requested, the trial transitions to a hint display screen showing the question, the hint text (labeled as a friend's answer), and a new editable textbox. The participant then submits their final answer by pressing Enter.

The cue validity list is pre-shuffled at experiment start: exactly 5 valid and 5 invalid hints are randomly ordered. On each hint request, the next cue type is popped from this list (sampling without replacement), and the corresponding valid or invalid hint text from the condition file is displayed. After all 10 hints are exhausted, a warning screen ("YOU HAVE NO CALLS LEFT") is shown for 1 second, and the hint button is disabled. Key variables: number of hints used, willingness to use hints for difficult vs. easy questions, answer accuracy before and after hints, how often participants follow valid vs. invalid hints, and individual differences in hint-seeking behavior. This task was developed following discussions at ESCOP 2025.

## Must Confirm

- **Question content**: General knowledge trivia, domain-specific questions, or custom item set?
- **Total hints**: 10 hints (5 valid + 5 invalid), or different count/ratio?
- **Answer format**: Free-text entry, or multiple choice?
- **Hint presentation**: Display as "friend's answer" text, or other framing?
- **Hint timing**: Is the pre-hint answer collected before the hint is shown, or is the answer only collected after?
- **Trial count**: Total number of questions (should exceed hint count so participants must choose when to use hints)?

## Trial Window Timeline

```text
┌─────────────────────────────────┐     ┌──────────────────────────────────┐
│ Window 1: Question + Answer     │     │ Window 2: Hint + Revised Answer  │
│ (if participant submits         │     │ (if participant clicks           │
│  without hint)                  │     │  "Phone a friend" button)        │
│                                 │     │                                  │
│ Content: question text +        │     │ Content: question text +         │
│ editable answer box +           │ ──→ │ hint text + new answer box +    │
│ "Phone a friend" button +       │     │ calls remaining counter          │
│ calls remaining counter         │     │ Duration: until Enter pressed    │
│ Duration: until Enter pressed   │     │ Response: free-text entry        │
│ Response: free-text entry       │     │ Data: answer_2.text, hint_shown, │
│ Data: answer.text, key_resp     │     │ cue_type, this_hint, n_calls     │
└─────────────────────────────────┘     └──────────────────────────────────┘
                                                 │
                    ┌────────────────────────────┘
                    ↓
     ┌──────────────────────────────────┐
     │ Window 3: No Calls Left          │
     │ (when n_calls >= 10)             │
     │                                  │
     │ Content: "YOU HAVE NO CALLS      │
     │ LEFT" warning                    │
     │ Duration: 1 s                    │
     │ Response: none                   │
     └──────────────────────────────────┘
```

## Data Analysis

Analyze hint usage rate, accuracy change after hints (comparing valid vs. invalid hint trials), and whether participants show differential weighting of valid vs. invalid hints. Examine individual differences in hint-seeking (e.g., related to overconfidence, trust, or need for cognition). Compare pre-hint and post-hint accuracy.

## References

Developed based on discussions with Paulina Pietrak at ESCOP 2025. Images by Rudy Issa.
