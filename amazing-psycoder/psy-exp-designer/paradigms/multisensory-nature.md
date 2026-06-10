# Multisensory Nature Experience Task

> **Parent**: [psy-exp-designer](../SKILL.md)
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

## Do Not Assume

- Do not assume all 15 videos are available without verification — 确认视频文件是否齐全，原始 N/T/R 视频集还是自定义素材？文件格式（MP4）和分辨率是否匹配呈现需求？
- Do not assume audio and video tracks are inherently synchronized — MovieStim 的音画同步依赖硬件解码性能，需在目标设备上实测确认延迟
- Do not assume the rating scale is self-explanatory to participants — 确认滑块锚定标签（如 1=非常轻微, 9=非常强烈）、量表范围以及 PA 和 NA 是否使用相同量尺
- Do not assume clip presentation order should be fully randomized — 确认是否允许同一视觉等级或声音类型连续出现，是否需要拉丁方平衡
- Do not assume I-PANAS-SF is the only pre-task measure needed — 确认是否还需自然关联度量表（NR-6/NRS）、状态焦虑量表（STAI）或其他个体差异测量
- Do not assume the 60-second clip duration is fixed for all trials — 部分变体可能使用更短（30s）或更长（120s）的片段，需明确确认

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| video_file | str | 视频文件名，含扩展名（如 `N01.mp4`） |
| visual_level | str | 视觉自然度等级：`high`（高）、`medium`（中）、`low`（低） |
| sound_type | str | 声音类型：`natural`（自然声）、`anthropogenic`（人造噪声）、`mixed`（混合） |

## Variants

**气候变体 (Climate Variant)** — `multisensory_nature_climate`：使用相同的 2x3 因子实验结构和视频资源，但以气候变化研究为框架，包含气候相关指导语、气候焦虑问卷或环保行为意向测量。适用于研究多感官自然体验如何影响气候参与度。详见本文件 [Climate Variant](#climate-variant) 小节。

**单感官对照变体 (Unimodal Control Variant)**：分离视觉与听觉通道，仅呈现视觉（无声视频）或仅呈现听觉（黑屏 + 自然声音），用于量化各感官通道对情绪影响的独立贡献。需额外准备静音视频或纯音频刺激文件。可交叉引用 `audiovisual-stimuli.md`。

**长时暴露变体 (Extended Exposure Variant)**：将每个片段延长至 3-5 分钟，试次减少至 5-6 个，适用于考察长时间自然暴露的累积恢复效应。需准备更长时长的视频素材，并考虑疲劳效应和注意力检查。

## Example

### 用户请求

> "我要做一个多感官自然体验实验。用15个视频片段，每个60秒。视频有高自然度（全是森林、海滩）、中自然度（乡村田野）、低自然度（城市街景）三种，声音有自然声（鸟叫、水声）、人造噪声（交通、施工）、混合声三种。每个视频放完后让被试评价当前积极情绪和消极情绪，用1到9的滑块打分。实验开始前先做I-PANAS-SF基线情绪问卷。试次随机呈现。视频文件在 stimuli/videos/ 文件夹里。用PsychoPy 2024。"

### 试次窗口时间线

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ 窗口 1                    │ →  │ 窗口 2                    │ →  │ 窗口 3                    │
│ 注视点                    │    │ 视频播放                  │    │ 情绪评分                  │
│ 内容: +                   │    │ 内容: 自然/城市场景视频    │    │ 内容: PA + NA 滑块        │
│ 持续时间: 500 ms          │    │ 持续时间: 60000 ms        │    │ 持续时间: 直至反应         │
│ 反应: 无                  │    │ 反应: 无                  │    │ 反应: 鼠标拖动滑块         │
│ 条件: 无                  │    │ 条件: {video_file}        │    │ 条件: {visual_level},     │
│ 数据: 无                  │    │ 数据: video_filename      │    │       {sound_type}        │
└──────────────────────────┘    └──────────────────────────┘    │ 数据: PA_rating, NA_rating│
                                                                └──────────────────────────┘
```

| 窗口 | 内容 | 持续时间 | 反应 | 文件 | 条件 | 数据 |
|------|------|----------|------|------|------|------|
| 注视点 | + | 500 ms | 无 | 无 | 无 | 无 |
| 视频播放 | 自然/城市场景视频 | 60000 ms | 无 | stimuli/videos/{video_file} | {video_file} | video_filename |
| 情绪评分 | PA + NA 滑块 | 直至反应 | 鼠标拖动 | 无 | {visual_level}, {sound_type} | PA_rating, NA_rating |

### 解析后的实验规格

| 字段 | 值 |
|------|-----|
| 实验名称 | 多感官自然体验任务 |
| 平台 | PsychoPy 2024 |
| 任务类型 | 多感官情绪评定（被试内设计） |
| 视觉因素 | 3 水平：高自然度 / 中自然度 / 低自然度 |
| 听觉因素 | 3 水平：自然声 / 人造噪声 / 混合声 |
| 试次数量 | 15（3x3 因子设计，部分组合可能重复或空缺） |
| 每试次时长 | 60 秒视频 + 评分（不限时） |
| 预实验问卷 | I-PANAS-SF（积极消极情绪量表简版） |
| 评分方式 | 滑块 1-9（积极情绪 + 消极情绪分别评定） |
| 试次顺序 | 完全随机 |
| 视频来源 | stimuli/videos/ 文件夹 |

### 待确认信息

1. **量表锚定标签**：滑块 1 和 9 分别对应什么文字描述？（如 "几乎没有" 到 "非常强烈"）PA 和 NA 量表是否使用相同的锚定标签？
2. **练习试次**：是否需要练习试次（如 2-3 个示例视频）让被试熟悉评分流程？练习数据是否保存？
3. **指导语语言**：指导语使用中文/英文/双语？实验结束后是否需要事后说明（debriefing）？

### 关键假设

- 视频文件命名遵循 N/T/R 约定（如 N01.mp4 为高自然度），条件文件中已包含 visual_level 和 sound_type 标签
- 积极情绪和消极情绪评分分别显示在两个独立界面（先 PA 后 NA），而非同一屏幕
- I-PANAS-SF 问卷使用标准 10 题版本，以 Excel 文件加载，5 点 Likert 量表
- 试次间无 ITI，视频结束后直接进入评分界面

### 代码架构

```
multisensory_nature.py
├── 参数配置（视频时长、评分范围、文件路径）
├── 窗口设置（全屏/窗口、分辨率）
├── I-PANAS-SF 预实验问卷加载（xlsx）
├── 条件文件加载（vids.xlsx → 试次列表）
├── 视频刺激预加载检查（MovieStim3）
├── 指导语界面
├── 试次循环：
│   ├── 注视点（500 ms）
│   ├── 视频播放（60000 ms，MovieStim3 + 音频同步）
│   ├── 积极情绪评分（滑块 1-9）
│   ├── 消极情绪评分（滑块 1-9）
│   └── 数据记录
├── 数据保存：try/finally CSV 增量写入
└── 事后说明
```

### 预期数据列

| 列名 | 类型 | 描述 |
|------|------|------|
| participant | str | 被试编号 |
| trial_index | int | 试次序号（0-14） |
| video_file | str | 视频文件名 |
| visual_level | str | 视觉自然度等级 |
| sound_type | str | 声音类型 |
| PA_rating | int | 积极情绪评分（1-9） |
| NA_rating | int | 消极情绪评分（1-9） |
| PA_RT | float | 积极情绪评分反应时（秒） |
| NA_RT | float | 消极情绪评分反应时（秒） |
| ipanas_PA_baseline | float | I-PANAS-SF 积极情绪基线得分 |
| ipanas_NA_baseline | float | I-PANAS-SF 消极情绪基线得分 |
