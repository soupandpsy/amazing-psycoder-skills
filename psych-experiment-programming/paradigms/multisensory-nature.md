# Multisensory Nature Experience Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/multisensory_nature) · PsychoJS

## When to Use

User mentions: Multisensory nature, nature exposure, audiovisual wellbeing, restorative environments, 多感官自然体验. Measures the interactive effects of visual and auditory nature exposure on self-reported affect (positive and negative) in response to natural vs. urban audiovisual scenes.

## Core Logic

Participants view a series of 15 audiovisual recordings that vary in the proportion of natural vs. urban visual scenes and natural vs. anthropogenic (human-made) soundscapes. Each clip is 60 seconds long. After each clip, participants rate their current positive and negative affect using slider components.

**Design**: The stimuli form a factorial combination of visual nature level (high/medium/low natural content) and sound type (natural sounds, anthropogenic noise, or mixed). Video files use naming conventions indicating scene type: N (nature), T (town/urban), and R (rural/mixed). The condition file (`vids.xlsx`) specifies which video file to play per trial along with its visual nature level and sound type labels.

**Trial structure**: video playback (60 seconds, full audiovisual) → affect rating sliders (positive and negative affect) → next trial. Videos play using `visual.MovieStim` with synchronized audio.

**Pre-task questionnaire**: Before the video trials, participants complete the I-PANAS-SF (International Positive and Negative Affect Schedule — Short Form), a validated brief affect measure, to establish baseline mood. This is loaded from an Excel file (`IPANAS-SF.xlsx`).

**Key prediction**: High visual nature paired with low anthropogenic noise should produce the highest positive affect and lowest negative affect. High visual nature paired with high anthropogenic noise may paradoxically increase negative affect due to sensory conflict. Individual difference moderators (nature connectedness, state anxiety) can be collected.

### Climate Variant

A climate-focused variant (`multisensory_nature_climate`) uses the identical experimental structure, video resources, and condition file, but is framed within climate change research contexts — potentially with adapted instruction text, different questionnaires, or climate-themed debriefing. This variant was developed as part of the 1 in 5 Climate Change Project and can be used to study how multisensory nature experiences influence climate engagement and wellbeing.

## Must Confirm

- **Video content**: Which 15 videos to use? The original N/T/R set or custom recordings? File format (MP4) and resolution?
- **Rating scales**: Positive and negative affect only, or additional dimensions (arousal, perceived restorativeness, aesthetic preference)?
- **Pre-task measures**: I-PANAS-SF only, or additional individual difference measures (nature connectedness/NRS, state anxiety/STAI, environmental attitudes)?
- **Clip duration**: Standard 60 seconds, or shorter/longer per clip?
- **Trial count**: 15 clips, or custom number?
- **Between- or within-subjects**: Single session with all participants viewing all clips, or between-subjects assignment to condition subsets?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Video Playback           │    │ Positive Affect Rating   │    │ Negative Affect Rating   │
│ Content: nature/urban    │    │ Content: slider          │    │ Content: slider          │
│   video (60s)            │    │ Duration: until response │    │ Duration: until response │
│ Duration: 60000 ms       │    │ Response: slider drag    │    │ Response: slider drag    │
│ Response: none           │    │ Condition: {video_id}    │    │ Condition: {video_id}    │
│ Condition: {video_type}  │    │ Data: PA rating          │    │ Data: NA rating          │
│ Data: video_filename     │    └──────────────────────────┘    └──────────────────────────┘
└──────────────────────────┘
```

## Data Analysis

Analyze positive and negative affect ratings as a function of visual nature level, auditory nature level, and their interaction using mixed-effects models or repeated-measures ANOVA. Test individual difference moderators: nature connectedness, state anxiety. Expect a significant visual x auditory interaction; the restorative benefit of visual nature is attenuated or reversed under high anthropogenic noise. Control for baseline mood using I-PANAS-SF pre-task scores.

## References

Aldoh, A., Ungureanu, R., Popescu, S., Eldridge, A., Sandom, C. J., & Rae, C. (2023). How does a multi-sensory experience of nature interact with wellbeing? Effects of visual and auditory nature presence on affect. Part of the 1in5 Climate Change Project initiative. https://www.1in5project.info/
