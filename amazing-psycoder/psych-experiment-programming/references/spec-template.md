# Experiment Specification Template

Use this template to formalize an experiment before coding. Fill in what is known; flag what is missing.

> **Note**: For active use, the [experiment config YAML](config-schema.md) is the primary artifact. This template serves as a reference for the full specification structure — all fields here correspond to config YAML sections. The unified workflow progressively fills the config YAML through 5 phases.

## 1. Meta

| Field | Value |
|-------|-------|
| Experiment name | |
| Platform | PsychoPy / Psychtoolbox / jsPsych |
| Task type | Go/No-go / Navon / Priming / Stroop / Eriksen Flanker / Simon / Rating / Stop-signal / IAT / N-back / Dot-probe / Visual search / Task switching / EAST |

## 2. Phase Structure

| Phase | Duration / Trials | Description |
|-------|-------------------|-------------|
| Instruction | | Welcome screen, task explanation |
| Practice | | Trials with feedback, can repeat |
| Formal Block 1 | | |
| Rest | | |
| Formal Block 2 | | |

## 3. Block Structure

- Blocks per phase:
- Trials per block:
- Block order: fixed / randomized / counterbalanced
- Block randomization: [describe]

## 4. Trial Event Sequence

Represent as a **box timeline** (per Trial Window Timeline Rule). Window name centered above the box, content centered inside, fields centered below. Box columns 24 chars wide with 6-space gaps. Arrow (→) between boxes in content row.

```text
   Window 1: Fixation            Window 2: Stimulus            Window 3: Response   
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│                      │      │                      │      │                      │
│          +           │  →   │       [MISSING]      │  →   │       [MISSING]      │
│                      │      │                      │      │                      │
└──────────────────────┘      └──────────────────────┘      └──────────────────────┘
     Duration: [MISSING]           Duration: [MISSING]          Duration: [MISSING]  
      Response: none                Response: [MISSING]          Response: [MISSING]  
        File: none                  File: [MISSING]              Condition: [MISSING]  
                                Condition: [MISSING]              Data: [MISSING]     
                                  Data: none                                          

  Window 4: Feedback           Window 5: ITI     
┌──────────────────────┐      ┌──────────────────────┐
│                      │      │                      │
│       [MISSING]      │  →   │                      │
│                      │      │                      │
└──────────────────────┘      └──────────────────────┘
     Duration: [MISSING]           Duration: [MISSING]
      Response: none                Response: none    
     Condition: none               Condition: none    
        Data: none                   Data: none       
```

Then fill the supporting table:

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Fixation | | | none | none | none | none |
| Stimulus | | | | | | |
| Response | | | | | | |
| Feedback | | | none | none | none | none |
| ITI | | | none | none | none | none |

Mark unclear items as `[MISSING]` directly in the box and table. Do not invent values silently.

## 5. Stimulus

- Source: image files / text / shapes / generated
- File path / naming convention:
- Image size / position:
- Preload or generate per trial:

## 6. Response Rules

| Rule | Value |
|------|-------|
| Allowed keys | |
| Response deadline (ms) | |
| Correct answer mapping | |
| No-go rule (if applicable) | |
| Timeout handling | |

## 7. Randomization

- Within-block trial order: random / fixed / pseudorandom
- Between-block: same / re-randomize
- Counterbalancing: none / across subjects / within subject
- Constraints: no more than N consecutive same-condition trials

## 8. Data Output Columns

| Column | Type | Description |
|--------|------|-------------|
| subject_id | str | Subject identifier |
| block | int | Block number |
| trial | int | Trial number within block |
| condition | str | Condition label |
| stimulus | str | Stimulus filename or ID |
| correct_response | str | Expected key |
| response | str | Actual key pressed |
| rt | float | Reaction time (ms) |
| accuracy | int | 1=correct, 0=incorrect, -1=timeout |
| timestamp | str | ISO timestamp |
