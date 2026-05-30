# Ultimatum Game

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/ultimatum) · reference

## When to Use

User mentions: Ultimatum game, UG, fairness, social decision-making, economic game, 最后通牒游戏, 公平博弈. A two-player economic game that measures fairness preferences and the willingness to incur personal costs to punish unfair treatment.

## Core Logic

The participant (Responder) is told they are paired with another player (Proposer), who has been given a sum of money to split. The Proposer makes an offer specifying how much the Responder receives (e.g., "Proposer gets $7, you get $3"). The Responder can either accept the offer (both players receive the proposed amounts) or reject it (neither player receives anything). The rational self-interest prediction is that Responders should accept any non-zero offer. In reality, low offers (typically below 20-30% of the total) are rejected at high rates, demonstrating fairness-driven punishment.

Key manipulations: the stake size (total amount to split), the identity of the Proposer (human vs. computer), the context (e.g., earned vs. windfall endowment), and whether the game is one-shot or repeated. Offers are typically presented as pre-determined splits (e.g., $5:$5 fair, $8:$2 unfair, $9:$1 very unfair), though some versions involve real-time human proposers.

This implementation frames the participant as the Responder. A simulated "connection" sequence (6 s total: 4 s "connecting to other player..." + 2 s "Connected!") enhances the cover story. On each trial, the proposed split is displayed (amount out of 10 pounds total), and the participant clicks an "Accept" or "Reject" button (mouse-based ButtonStim). After the choice, the outcome is displayed: both players' earnings if accepted, or "You rejected the offer. Nobody gets anything." if rejected. A fairness check (`offer >= amount/2`) is used to categorize offers as fair or unfair.

Typical design: offers range from 0 to the full stake, with standard offers being 5:5 (fair), 7:3/8:2 (unfair), and 9:1/10:0 (very unfair). Earnings accumulate across trials. The key behavioral measure is the rejection rate at each offer level.

## Must Confirm

- **Stake amount**: How much money to split? (typically 10 units, e.g., $10 or 10 pounds)
- **Offer set**: Which specific offer splits to present? (e.g., 5:5, 7:3, 8:2, 9:1)
- **Player role**: Participant always as Responder, or does the role alternate?
- **Cover story**: "Connected to another player" simulation, or transparent about pre-programmed offers?
- **Proposer identity**: Human (with photo/name), computer algorithm, or anonymous?
- **Response mode**: Mouse click on Accept/Reject buttons, or keyboard response?
- **Outcome display**: Show earnings after each trial, or only at the end?
- **Post-trial ratings**: Collect fairness judgments or emotion ratings after each offer?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Connection Simulation    │    │ Offer + Decision         │    │ Outcome Display          │
│ Content: "Connecting to  │    │ Content: proposed split  │    │ Content: earnings or     │
│ other player..." (4 s)   │    │ (e.g., "Proposer: £7     │    │ "Nobody gets anything"   │
│ then "Connected!" (2 s)  │    │ You: £3") + Accept/      │    │ Duration: ~2 s            │
│ Duration: 6 s total      │    │ Reject buttons           │    │ Response: none            │
│ Response: none           │    │ Duration: until click    │    │ Data: none                │
│ Data: none               │    │ Response: mouse click    │    │                           │
│                          │    │ Data: choice, RT, offer  │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

The primary dependent variable is the acceptance rate as a function of offer amount. Plot acceptance rate against offer size (or fairness level). Typically, acceptance rates increase with offer size, with a sharp drop-off below 30-40%. Compare acceptance rates between conditions (e.g., human vs. computer proposer — higher rejection of unfair human offers indexes social preferences). Individual differences (e.g., trait agreeableness, psychopathy, autism) correlate with rejection rates. Rejection rates are also used to index negative reciprocity and anger-driven punishment.

## References

Guth, W., Schmittberger, R., & Schwarze, B. (1982). An experimental analysis of ultimatum bargaining. *Journal of Economic Behavior & Organization, 3*(4), 367–388. https://doi.org/10.1016/0167-2681(82)90011-7

Camerer, C. F. (2003). *Behavioral game theory: Experiments in strategic interaction*. Princeton University Press.
