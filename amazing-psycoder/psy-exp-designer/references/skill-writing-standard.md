# Skill Writing Standard

This file defines the required rules for writing and modifying Claude Skills.

## 1. Basic Skill Structure

Every Skill must be a self-contained folder.

Each Skill folder must contain one required file:

```text
SKILL.md
```

A minimal Skill has this structure:

```
skill-name/
└── SKILL.md
```

A complex Skill may include references, examples, scripts, or assets:

```
skill-name/
├── SKILL.md
├── references/
├── examples/
├── scripts/
└── assets/
```

Do not put unrelated files into a Skill folder.

## 2. Required YAML Frontmatter

Every SKILL.md must start with YAML frontmatter.

Required fields:

```yaml
---
name: skill-name
description: Clear trigger condition and task boundary.
---
```

The name must match the folder name.

Correct:

```yaml
---
name: psy-exp-designer
description: Use for psychological experiment programming tasks, including designing experiment specifications, trial/window timelines, condition tables, randomization rules, response rules, and data fields. Trigger for 中文/English requests about 心理学实验程序、实验代码、trial/block结构、刺激呈现、随机化、反应时、条件表、Go/No-go、Navon、Stroop、priming.
---
```

Incorrect:

```yaml
---
name: psych-exp
description: This is a useful skill.
---
```

## 3. Description Is a Trigger Rule

The description is not a general introduction. It controls when the Skill should activate.

A good description must include:

1. What the Skill does
2. When to use it
3. Key trigger words or user intents
4. When not to use it, if there is possible ambiguity

For Chinese users, include Chinese trigger terms.

Example:

```yaml
description: Use for generating, modifying, or debugging PsychoPy experiment code. Trigger for PsychoPy代码、psychopy实验、psychopy报错、Builder转代码、刺激呈现、keyboard response、RT计时、中文文本、EEG trigger、data saving.
```

Avoid vague descriptions:

```yaml
description: Helps with coding.
```

Avoid overly broad descriptions:

```yaml
description: Use for all psychology questions.
```

## 4. Naming Rules

Use kebab-case for all Skill folders and Markdown resource files.

Correct:

```
psy-exp-designer
psy-exp-coder
psy-exp-reviewer
go-nogo.md
priming.md
config-schema.md
```

Incorrect:

```
psych_exp_programming
psychExpProgramming
go_nogo.md
primingTarget.md
ExperimentSpecification.md
```

The `name` field in YAML must match the Skill folder name.

Correct:

```
folder: psy-exp-coder
name: psy-exp-coder
```

Incorrect:

```
folder: psy-exp-coder
name: psych-code-generator
```

## 5. Skill Boundary Rule

Each Skill should have one clear responsibility.

Do not make one Skill do everything.

Preferred structure:

```
psy-exp-designer/      # Orchestration and experiment specification
psy-exp-coder/            # Code generation across platforms
psy-exp-reviewer/    # Code review and production-readiness audit
```

The main Skill should coordinate and route. Platform Skills should implement. Review Skills should inspect.

## 6. Recommended SKILL.md Sections

A well-structured SKILL.md should usually include:

```
# Skill Name
## Purpose
## When to Use
## When Not to Use
## Workflow
## Required Inputs
## Missing Information Policy
## Output Format
## Examples
```

Not every Skill needs every section, but complex Skills should include most of them.

## 7. Resource Files

Use resource files when a Skill becomes too long or when knowledge is reusable.

Examples:

```
references/spec-template.md
references/data-recording.md
references/randomization.md
paradigms/go-nogo.md
paradigms/navon.md
```

The main SKILL.md must explicitly say when to read each resource file.

Bad:

> See paradigms folder.

Good:

> If the user mentions Go/No-go, read `paradigms/go-nogo.md` before asking questions or generating code. The paradigm file contains both the paradigm rules and a complete specification example at the end.

## 8. Examples Are Required for Complex Skills

If a Skill handles complex work, include examples.

Examples should show:

1. User input
2. Parsed interpretation
3. Missing information
4. Expected output structure

Examples should be realistic, not toy examples. Complex paradigms should embed a full example at the end of the paradigm file under `## Example`, showing the complete unified workflow from user request to expected code architecture. See `paradigms/go-nogo.md` for the canonical pattern.

## 9. Missing Information Rule

Never silently invent critical task logic.

For psychological experiment programming, do not guess:

- phase structure
- trial window sequence
- timing values
- response mapping
- correctness rule
- feedback logic
- block order
- randomization rule
- data columns

If information is missing, output:

```
## Known Information
...
## Missing Information
...
## Safe Assumptions
...
## Questions
1.
2.
3.
```

Ask no more than 3 questions per round.

## 10. Output Format Rule

Every Skill must define its expected output format.

For new experiment code, use:

```
## Experiment Specification Summary
## Trial Window Timeline
## Missing Information / Assumptions
## Code Architecture
## Full Code
## Data Output Fields
## How to Run
## Pre-collection Checklist
```

For code review, use:

```
## Overall Verdict
## Critical Issues
## Major Issues
## Minor Issues
## Section-by-Section Report
## Suggested Fixes
```

## 11. Do Not Overload SKILL.md

Do not put all details into SKILL.md.

Use this rule:

| File | Purpose |
|------|---------|
| SKILL.md | routing, workflow, core rules |
| references/ | reusable standards |
| paradigms/ | domain-specific rules |
| examples/ | input-output examples |
| scripts/ | executable helper scripts, if needed |
| assets/ | static files, if needed |

## 12. Avoid False Capabilities

Do not write that a Skill can do something unless the instructions actually explain how.

Bad:

```yaml
description: Handles EEG triggers.
```

But the Skill contains no EEG trigger rules.

Good:

```markdown
## EEG Trigger Rule
Use `win.callOnFlip(port.setData, trigger_code)` to synchronize triggers with stimulus onset.
```

## 13. Avoid Over-Prompting

A Skill should not ask the user too many questions at once.

Use priority-based questioning:

1. Ask questions that affect program structure first
2. Ask implementation details later
3. Ask no more than 3 questions per round

## 14. Do Not Assume Cross-Skill Invocation Works Like an API

A main Skill can route to another Skill, but should not assume another Skill is automatically invoked as a function.

Use wording like:

> If the platform is PsychoPy, apply `psy-exp-coder` if available. If not automatically loaded, explicitly read `../psy-exp-coder/SKILL.md`.

Avoid:

> Invoke psy-exp-coder.

## 15. Versioning

When a Skill becomes stable, mark it informally in the file:

```markdown
## Version
v1.2 — stable initial version.
```

When modifying a Skill, preserve existing behavior unless the user explicitly asks for a redesign.

## 16. Final Checklist Before Saving a Skill

Before saving or modifying a Skill, check:

- [ ] Does SKILL.md start with YAML frontmatter?
- [ ] Does YAML include `name` and `description`?
- [ ] Does `name` match the folder name?
- [ ] Is `description` written as a trigger rule?
- [ ] Are Chinese trigger terms included if the user works in Chinese?
- [ ] Is the Skill boundary clear?
- [ ] Is the workflow explicit?
- [ ] Are missing-information rules defined?
- [ ] Is the output format defined?
- [ ] Are resource files referenced explicitly?
- [ ] Are examples included for complex tasks?
- [ ] Are filenames in kebab-case?
- [ ] Are unsupported capabilities removed or fully explained?
