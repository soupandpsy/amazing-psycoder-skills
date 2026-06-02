# Bilingual (Blocked) Stroop Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/bilingual_stroop) · PsychoJS

## When to Use

User mentions: Bilingual Stroop, blocked Stroop, cross-language Stroop, 双语斯特鲁普. A variant of the classic Stroop task using blocked language conditions to compare the magnitude of Stroop interference across a participant's native and non-native languages.

## Core Logic

Participants report the display color of words while ignoring their semantic meaning, which may be congruent or incongruent with the ink color. The bilingual blocked version presents two language blocks — one in each language (e.g., English and Maori). The key prediction is that the Stroop effect (incongruent RT – congruent RT) will be larger in the more fluent language, because word reading is more automatic in that language, producing greater interference with color naming.

**Counterbalancing**: Participants are assigned to Group A or Group B at experiment start. Group A sees Language 1 first, then Language 2; Group B sees the reverse order. This controls for order effects.

**Block structure**: For each language, a block-level instruction screen explains the task in that language. Then a trial loop presents the stimuli. Two separate condition files (`english.xlsx` and `maori.xlsx`, or equivalent for your languages) define the stimuli for each language block.

**Trial structure**: fixation → color-word stimulus (the word in its ink color) → keypress response → ITI. Participants press one of three keys to indicate the ink color (e.g., 'r' for red, 'g' for green, 'b' for blue). The same three-key mapping is used across both language blocks; only the word language changes.

**Stimuli**: Color words (e.g., RED, GREEN, BLUE) presented in colored ink. Each trial is classified by: language (L1 vs L2), word meaning (color name), ink color, and congruency (congruent: word = ink; incongruent: word != ink).

## Must Confirm

- **Language pair**: Which two languages? (e.g., English/Maori, Chinese/English, French/German)
- **Color set**: Which ink colors? How many? (typically 3: red, green, blue)
- **Response keys**: Which keys map to which colors? (e.g., r/g/b for red/green/blue)
- **Counterbalancing**: Between-subjects (Group A/B) or within-subjects (all participants do both orders)?
- **Trial count per block**: How many trials per language? Congruency ratio? (50:50 or with neutral trials?)
- **Practice**: Practice before each language block, or one combined practice at the start?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Stroop Stimulus          │    │ Feedback (optional)      │    │ ITI                      │
│ Content: +               │    │ Content: color word       │    │ Content: correct/incorrect│   │ Content: blank           │
│ Duration: 500-1000 ms    │    │ Duration: until key      │    │ Duration: 500 ms         │    │ Duration: 500-1000 ms    │
│ Response: none           │    │ Response: r/g/b keys     │    │ Response: none           │    │ Response: none           │
│ Condition: none          │    │ Condition: {lang, word,  │    │ Condition: none          │    │ Condition: none          │
│ Data: none               │    │  ink_color, congruency}  │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    │ Data: rt, key, acc       │    └──────────────────────────┘    └──────────────────────────┘
                                └──────────────────────────┘
```

## Data Analysis

Compare the Stroop interference effect (incongruent RT – congruent RT) between language conditions. Use a 2 (language: fluent vs. less fluent) x 2 (congruency: congruent vs. incongruent) repeated-measures ANOVA. The interaction term tests whether the Stroop effect differs by language. Follow up with simple effects tests. Also report accuracy (error rate) as a secondary measure.

## References

Stroop, J. R. (1935). Studies of interference in serial verbal reactions. *Journal of Experimental Psychology, 18*(6), 643–662. https://doi.org/10.1037/h0054651
