# Corsi Block-Tapping Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/corsi_blocks) · PsychoJS

## When to Use

User mentions: Corsi blocks, Corsi span, spatial working memory, visuospatial span, 科西方块, 空间工作记忆. Measures visuospatial short-term/working memory span by requiring participants to reproduce a sequence of spatial locations.

## Core Logic

Nine blocks are arranged in an irregular spatial pattern on screen (the classic Corsi board layout, avoiding a regular grid to prevent verbal encoding). On each trial, a subset of blocks is highlighted (flashed) one at a time in a random sequence. The participant must reproduce the sequence by clicking the blocks in the same order (forward span).

**Two-phase within-trial structure**:
1. **Presentation phase**: Blocks flash in sequence with a fixed stimulus onset asynchrony. Each block briefly changes color (e.g., from dark to light) to indicate selection.
2. **Recall phase**: The participant clicks blocks with the mouse to reproduce the sequence. Mouse position is tracked via `eventManager.getMousePos()` to detect clicks on block locations.

**Adaptive sequencing**: The task is self-contained in a single routine that programmatically generates sequences. Sequence length starts at 2 and increases with successful reproduction (span increases) or decreases with failure (span decreases). The task continues until a stopping criterion is met (e.g., failure on both attempts at a given span length).

**Span scoring**: The traditional method gives two attempts at each sequence length. The span score is the longest sequence length for which at least one trial was correctly reproduced. An alternative is the total correct trials score (sum of all correctly reproduced sequences). Typical forward spans are 5–7 items for healthy young adults; backward spans (reverse order recall) are typically 1–2 items shorter and tap the central executive.

**No condition files**: Unlike most PsychoJS experiments, the Corsi task does not use a condition spreadsheet. All sequence generation, presentation timing, and response collection logic is implemented programmatically in code components.

## Must Confirm

- **Direction**: Forward span (same order) or backward span (reverse order), or both?
- **Block count**: Classic 9-block Corsi board or custom arrangement?
- **Scoring method**: Strict span (longest length with at least 1 correct) or total correct?
- **Stopping rule**: Two attempts per span, or different rule?
- **Starting length**: Sequence length 2, or custom?
- **Recall modality**: Mouse click on screen, or touchscreen tap (different hit detection)?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │
│ Presentation Phase       │    │ Recall Phase             │
│ Content: blocks flash    │    │ Content: 9 blocks static │
│   in sequence            │    │ Duration: until click    │
│ Duration: N * SOA        │    │   (self-paced)           │
│   (SOA ~750-1000 ms)     │    │ Response: mouse clicks   │
│ Response: none           │    │   on blocks              │
│ Condition: {seq_length}  │    │ Condition: none          │
│ Data: sequence presented │    │ Data: sequence clicked,  │
└──────────────────────────┘    │   accuracy               │
                                └──────────────────────────┘
```

## Data Analysis

Primary measures: Corsi span (forward, backward, or both), total correct trials score. Compare to digit span for domain-specific working memory dissociations. Clinical populations (e.g., patients with right-hemisphere lesions, neglect, or ADHD) often show disproportionate Corsi deficits relative to verbal spans. Analyze error types: order errors vs. item omissions vs. intrusions.

## References

Corsi, P. M. (1972). Human memory and the medial temporal region of the brain. *Dissertation Abstracts International, 34*(2-B), 891.

Kessels, R. P. C., van Zandvoort, M. J. E., Postma, A., Kappelle, L. J., & de Haan, E. H. F. (2000). The Corsi block-tapping task: Standardization and normative data. *Applied Neuropsychology, 7*(4), 252–258. https://doi.org/10.1207/S15324826AN0704_8
