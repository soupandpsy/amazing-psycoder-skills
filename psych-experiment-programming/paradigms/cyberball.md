# Cyberball (Social Exclusion Paradigm)

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/cyberball) · reference

## When to Use

User mentions: Cyberball, ostracism, social exclusion, social rejection, 赛博球, 社会排斥. A virtual ball-tossing game used to experimentally induce feelings of social inclusion or exclusion (ostracism).

## Core Logic

Participants are told they are playing an online ball-tossing game with two or three other participants (actually computer-controlled confederates). The game appears as a simple interface showing player icons. When a participant receives the ball, they click on one of the other players to throw the ball to them. Unbeknownst to the participant, the computer players follow a predetermined script dictating how often they toss the ball to the participant.

In the inclusion condition, the participant receives the ball roughly one-third of the time (equal participation). In the exclusion (ostracism) condition, the participant initially receives the ball a few times but is then excluded from play — the computer players toss the ball only among themselves. The paradigm is powerful: even brief (2-5 minute) exclusion reliably induces feelings of distress, lowered belonging, reduced self-esteem, reduced sense of meaningful existence, and reduced perceived control.

Typical design: 30-60 total throws, with the participant receiving 2-4 initial throws in the exclusion condition then none thereafter. Post-experiment, participants complete the Need-Threat Scale (assessing belonging, self-esteem, meaningful existence, and control) and a mood questionnaire. The Cyberball effect is remarkably robust — participants report distress even when told the other players are computer-controlled or from a despised outgroup.

## Must Confirm

- **Condition**: Inclusion, exclusion, or both? What percentage of throws does the participant receive in each condition?
- **Number of players**: 2 virtual players (total 3 including participant) or 3 virtual players?
- **Total throws**: How many total ball tosses? (typically 30-60)
- **Participant throw mechanism**: Mouse click on player icons, or keyboard selection?
- **Ball animation**: Animated ball movement between players, or instantaneous teleport?
- **Cover story**: Is the participant told they are playing with real people over the internet, or with a computer program?
- **Post-game measures**: Which questionnaires follow the game (Need-Threat Scale, mood, manipulation check)?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────────────────┐
│ Participant's Turn        │    │ Other Player's Turn (passive)        │
│ (ball_to == "choose")     │    │ (ball_to != "choose")                │
│                           │    │                                      │
│ Content: 3 player icons   │    │ Content: 3 player icons + ball at   │
│ + ball at participant     │    │ thrower position                     │
│ Duration: until click     │    │ Duration: 1 s (observation)          │
│ Response: click target    │    │ Response: none                       │
│ Data: chosen_player, RT   │    │ Data: ball_from, ball_to             │
├───────────────────────────┤    ├──────────────────────────────────────┤
│            ↓              │    │            ↓                         │
└───────────────────────────┘    └──────────────────────────────────────┘
                 ↓                              ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Ball Animation (both trial types)                                     │
│ Content: 3 player icons + ball moving from start to end position      │
│ Duration: 3 s (linear interpolation per frame)                        │
│ Display: "You threw to Player X" or "Player X threw to Player Y"     │
│ Response: none                                                        │
│ Data: none                                                            │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Analysis

Primary analyses compare inclusion vs. exclusion conditions on the Need-Threat Scale subscales and mood measures. Manipulation checks: perceived percentage of throws received, feelings of being ignored/excluded. Behavioral analyses (throw latency, choice of recipient) are secondary. Individual difference moderators (rejection sensitivity, social anxiety, attachment style) are often examined.

## References

Williams, K. D., Cheung, C. K. T., & Choi, W. (2000). Cyberostracism: Effects of being ignored over the Internet. *Journal of Personality and Social Psychology, 79*(5), 748–762. https://doi.org/10.1037/0022-3514.79.5.748

Williams, K. D., & Jarvis, B. (2006). Cyberball: A program for use in research on interpersonal ostracism and acceptance. *Behavior Research Methods, 38*(1), 174–180. https://doi.org/10.3758/BF03192765
