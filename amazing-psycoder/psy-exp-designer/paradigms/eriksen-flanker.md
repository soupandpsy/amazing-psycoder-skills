# Eriksen Flanker Paradigm

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)

## When to Use

User mentions: Flanker task, Eriksen flanker, flanker interference, response interference, 侧抑制任务, 艾里克森侧翼. Measures the ability to suppress interference from task-irrelevant distractors by responding to a central target while ignoring flanking stimuli.

**This file covers the Eriksen Flanker paradigm (center-surround distractor interference). For the Stroop paradigm (color-word interference), see [stroop.md](stroop.md). For the Simon paradigm (spatial compatibility), see [simon.md](simon.md).**

## Core Logic

Participants respond to the direction of a central arrow target (left or right arrow key) while ignoring surrounding flanker arrows. Flankers can be:
- **Congruent**: Pointing the same direction as the target (e.g., `>>>>>`)
- **Incongruent**: Pointing the opposite direction from the target (e.g., `>><>>`)
- **Neutral** (optional): Non-directional stimuli (e.g., lines or squares)

The flanker interference effect = RT_incongruent − RT_congruent. This indexes the efficiency of selective attention and conflict resolution.

The classic version (Eriksen & Eriksen, 1974) uses letter stimuli (target letter flanked by response-compatible, response-incompatible, or neutral letters). The arrow version is more widely used today, especially with children and clinical populations, due to lower reading demands.

Typical design: 200–400 total trials, equally split between congruent and incongruent (and optionally neutral). The target and flankers appear simultaneously. Trial structure: fixation (500–1000 ms) → target + flankers (until response, deadline ~1000–1500 ms) → ITI.

## Must Confirm

1. **Stimulus type**: Arrows (`<<><<`) or letter stimuli (`SSHSS`)?
2. **Congruency conditions**: Congruent, incongruent, and neutral? What proportion of each?
3. **Number of flankers**: How many on each side? (typically 2, making a 5-item array)
4. **Response mapping**: Which key = left direction? Which key = right direction?
5. **Timing**: Fixation duration, stimulus duration, response deadline?
6. **Practice**: Include practice block with feedback before the main task?
7. **Trial count**: How many trials per congruency condition?
8. **Flanker spacing**: 刺激间距（视觉角度）？间距影响干扰效应强度
9. **ITI duration**: 试次间隔时间和变化范围？
10. **OS & font**: 在什么操作系统运行？如使用中文指导语，确认字体
11. **Display**: 全屏还是窗口？刺激大小和屏幕位置？
12. **Instruction text**: 指导语内容？如何向被试说明忽略两侧箭头？

## Do Not Assume

- Do not assume arrow stimuli — the original Eriksen paradigm used letters
- Do not assume 50:50 ratio — many studies include neutral conditions (33:33:33)
- Do not assume 2 flankers per side — 1, 2, or 3 flankers vary attentional demands
- Do not assume adult participants — the children's variant uses fish/bird images

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| target_dir | str | Direction of central target: `"left"` or `"right"` |
| flanker_type | str | `"congruent"`, `"incongruent"`, or `"neutral"` |
| corrAns | str | Correct key name (`"left"` or `"right"`) |

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Fixation                 │    │ Target + Flankers        │    │ ITI                      │
│ Content: + at center     │    │ Content: arrow array     │    │ Content: blank           │
│ Duration: 500-1000 ms    │    │ (e.g., <<><< or <<<<<)   │    │ Duration: 500-1000 ms    │
│ Response: none           │    │ Duration: until response │    │ Response: none           │
│ Condition: none          │    │ (deadline 1000-1500 ms)  │    │ Condition: none          │
│ Data: none               │    │ Response: left/right key │    │ Data: none               │
│                          │    │ Condition: {congruency}  │    │                           │
│                          │    │ Data: rt, key, acc       │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | Condition | Data |
|--------|---------|----------|----------|-----------|------|
| Fixation | + | 500-1000 ms | none | none | none |
| Target+Flankers | arrow array | until key (deadline 1000-1500 ms) | left/right | {target_dir}, {flanker_type} | rt, key, acc |
| ITI | blank | 500-1000 ms | none | none | none |

## Child-Friendly Variant

See [children-flanker-task.md](children-flanker-task.md). Uses fish images (`leftFish.png`, `rightFish.png`) instead of arrows, with a colorful nature-themed background and progress counter. The task logic is identical: respond to the central fish's direction while ignoring surrounding fish. Key differences: longer response deadline (~3000 ms), child-appropriate instructions, and engaging visual design. Practice trials include feedback; main trials do not.

## Data Analysis

Compute flanker interference scores separately for RT and accuracy:
- **Flanker interference effect** (RT): RT_incongruent − RT_congruent
- **Flanker interference effect** (accuracy): Accuracy_congruent − Accuracy_incongruent

Use paired t-tests or repeated-measures ANOVA to test the congruency effect. Individual differences in flanker interference correlate with executive function, self-control, and are sensitive to clinical conditions (ADHD, anxiety, aging). Error-related slowing (post-error trials) is also commonly analyzed. The flanker task is a core measure of executive control in the NIH Toolbox and the Attention Network Test (ANT).

## Randomization Checks

- No more than 3–4 consecutive same-response trials (prevents response repetition confound)
- Equal condition count per block

## References

Eriksen, B. A., & Eriksen, C. W. (1974). Effects of noise letters upon the identification of a target letter in a nonsearch task. *Perception & Psychophysics*, *16*(1), 143–149. https://doi.org/10.3758/BF03203267

## Example

### User Request

> "我想做一个箭头Flanker实验。屏幕中央呈现一排5个箭头，中间箭头是目标，两侧箭头是干扰。中间箭头向左按F键，向右按J键。一致条件（两侧箭头与中间同向）、不一致条件（两侧箭头与中间反向）各半。20个练习trial（有反馈）+ 4个正式block各48个trial。注视点500-1000ms随机，刺激呈现直到按键（deadline 1500ms），ITI 500-1000ms随机。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Fixation                 │    │ Target + Flankers        │    │ ITI                      │
│ Content: +               │    │ Content: 箭头阵列        │    │ Content: empty           │
│ Duration: 500-1000 ms    │    │ Duration: until key      │    │ Duration: 500-1000 ms    │
│ Response: none           │    │ Response: f/j            │    │ Response: none           │
│ Condition: none          │    │ Condition: {target_dir}/ │    │ Condition: none          │
│ Data: none               │    │   {flanker_type}         │    │ Data: none               │
│                          │    │ Data: rt, key, acc       │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Arrow Flanker Task |
| Platform | PsychoPy |
| Stimulus type | Arrows (5-item array: <<><< or <<<<<) |
| Response mapping | F=left, J=right |
| Congruency ratio | 50:50 congruent:incongruent |
| Conditions | 2 target_dir × 2 flanker_type = 4 conditions |
| Blocks | Practice(20) → Block1-4(48 each) |
| Data columns | target_dir, flanker_type, correct_response, rt, key, acc |
