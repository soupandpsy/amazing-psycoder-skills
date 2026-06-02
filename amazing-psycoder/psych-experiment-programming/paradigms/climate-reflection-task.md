# Climate Reflection Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/climate_reflection_task) · PsychoJS

## When to Use

User mentions: Climate reflection, environmental attitudes, climate change engagement, climate beliefs, 气候反思任务, 环境态度. A two-phase questionnaire paradigm designed to explore how exposure to climate information influences participants' engagement with and attitudes toward climate change issues.

## Core Logic

This is a reflection-and-reassessment paradigm, not a reaction-time task. It consists of three sequential phases:

**Phase 1 — Free Response**: Participants are presented with a series of open-ended questions about climate change from a spreadsheet (`climate_change_questions.xlsx`). Each question appears individually, and participants type their answer using a text input box (Enter to submit). All typed answers are stored as `answer.text`.

**Phase 2 — Information Exposure**: Participants read an informational passage about climate change, presented as a static text screen. This serves as the experimental manipulation — the content can be varied (e.g., scientific consensus information, personal impact narratives, solutions-focused messages) to test different intervention framings.

**Phase 3 — Reflection**: An introduction screen explains that participants will now review their previous answers. The second loop (`response_loop`) re-presents each original question alongside the participant's own Phase 1 answer. A slider component allows participants to rate how much they agree with their previous response on a continuous scale. This measures whether exposure to the informational passage shifted their attitudes toward their prior beliefs.

**Cross-phase data linkage**: The participant's typed answer from Phase 1 is stored and re-displayed during Phase 2/3. This requires tracking which answer corresponds to which question across experimental phases — a design pattern for any reflection/reassessment paradigm regardless of topic.

**Key measures**:
- Agreement ratings (do participants still stand by their original answers?)
- Pre-post shift in agreement (reflection ratings as a function of information exposure)
- Answer content analysis (qualitative coding of Phase 1 free responses)
- Individual differences in receptivity to climate information

## Must Confirm

- **Questions**: What climate change questions to ask? (e.g., beliefs about causes, personal concern, policy support, behavioral intentions)
- **Informational passage**: What content to present between phases? Scientific consensus text, narrative stories, statistical data, or multiple conditions?
- **Number of questions**: How many? (typically 5–10 for reasonable task duration)
- **Rating scale**: Continuous slider (0–100) or Likert scale (e.g., 1–7)?
- **Topic flexibility**: Climate change topic only, or adaptable to other attitude domains (vaccine beliefs, political attitudes, etc.)?
- **Control condition**: Include a no-information control group, or within-subjects pre-post only?

## Trial Window Timeline

```text
Phase 1 — Free Response:
┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │
│ Question                 │    │ Text Response            │
│ Content: question text   │    │ Content: text input box  │
│ Duration: until Enter    │    │ Duration: until Enter    │
│ Response: none           │    │ Response: free text      │
│ Data: this_question      │    │ Data: answer.text        │
└──────────────────────────┘    └──────────────────────────┘

Phase 2 — Information:
┌──────────────────────────┐
│ Information Passage      │
│ Content: climate text    │
│ Duration: self-paced     │
│   (press key to continue)│
│ Response: any key        │
│ Data: reading_time       │
└──────────────────────────┘

Phase 3 — Reflection:
┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │
│ Question + Prior Answer  │    │ Agreement Rating         │
│ Content: question +      │    │ Content: slider          │
│   "You answered: {text}" │    │   (0 = completely disagree│
│ Duration: self-paced     │    │    100 = completely agree)│
│ Response: none           │    │ Duration: until response │
│ Data: this_question,     │    │ Response: slider drag    │
│   previous_answer        │    │ Data: slider.response    │
└──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

Primary analysis compares agreement ratings across questions. Examine whether agreement shifts systematically after information exposure. Analyze free-text responses (Phase 1) using qualitative content analysis or NLP topic modeling. Test individual difference moderators (political orientation, environmental values, science literacy) on agreement change. Compare different information conditions (if multiple passages are used between subjects).

## References

Developed as part of climate change engagement research using the PsychoJS platform. Adaptable to any domain requiring reflection on prior beliefs after information exposure.
