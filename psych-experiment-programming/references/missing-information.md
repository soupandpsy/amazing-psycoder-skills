# Missing Information Policy

This policy defines what must NOT be invented silently and how to surface gaps to the user.

## Rule

**Do not silently invent critical experiment logic.** The cost of a wrong assumption is an unusable dataset. When information is missing, flag it explicitly — never fill it in with a guess and move on.

## Critical Information (Must Confirm)

These items must be confirmed before any code is generated:

1. **Phase structure** — What phases exist? Instruction, practice, formal, rest, break?
2. **Trial event sequence** — What happens in each trial? Fixation → stimulus → response → feedback → ITI?
3. **Timing values** — Duration of each event in ms
4. **Response mapping** — Which keys mean what? What about unmatched stimuli?
5. **Correctness rule** — What makes a response "correct" for every possible trial type?
6. **No-go rule** — Is "no response" correct or incorrect? Under what conditions?
7. **Feedback logic** — When is feedback shown? Practice only? Formal trials? Never?
8. **Block order** — Fixed or counterbalanced? If counterbalanced, how?
9. **Randomization rule** — Full random, pseudorandom with constraints, or blocked?
10. **Data columns** — What must be saved? Are there paradigm-specific columns?

## When Information Is Missing

Present a structured summary, never skip ahead to code:

1. **Known information** — what is clear from the user's description
2. **Missing information** — what must be decided before coding (be specific)
3. **Safe assumptions** — what can be reasonably defaulted, with brief justification
4. **Next questions** — 2–3 highest-priority questions. Not an exhaustive list — the user should not feel interrogated

## Example

**User says:** "我想做一个情绪Stroop实验，用情绪面孔图片和中性面孔，判断面孔的情绪效价"

**Response:**

1. **Known**: Emotional Stroop variant, face stimuli, valence judgment task
2. **Missing**:
   - What are the specific emotion categories? (happy, fearful, angry, neutral?)
   - Which keys map to which valence? Are there more than 2 options?
   - Are images pre-selected or do you need help finding them?
3. **Design assumptions (flagged)**: Fixation 500ms, stimulus until response (deadline 3000ms), 48 trials per condition — these are placeholders; confirm or replace before collecting data
4. **Questions:**
   - "面孔情绪有几类？分别对应哪个按键？"
   - "每类面孔有多少张图片？是否有标准化图片集？"

## What IS Safe to Default

These can be filled in without asking — they don't affect the experiment's scientific validity:

**Implementation-level defaults:**
- Data directory: `data/` (create if missing)
- Filename includes subject ID and timestamp
- Emergency quit on Escape always enabled
- Stimulus files validated at startup
- Editable parameters centralized at top of script
- Fixation cross style: `+`
- Background color: PsychoPy gray `(-0.5, -0.5, -0.5)` in normalized units
- Instruction text font size: 28pt
- CSV encoding: UTF-8

**Design-level defaults — mark these explicitly as assumptions and flag them to the user:**

These may be used when the user asks for a quick draft, but must be clearly called out as assumptions:
- Fixation duration (do not default to a specific ms without noting it)
- Response deadline (varies widely by paradigm)
- ITI range or jitter
- Number of trials per condition
- Whether feedback appears in practice, formal, or neither
- Block count and trials per block

The distinction: implementation defaults affect code structure and reliability; design defaults affect the experimental design and statistical power. Only the first category is safe to use silently.
