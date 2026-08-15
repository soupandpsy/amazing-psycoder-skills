# Amazing PsyCoder Skill Writing Standard

Use this reference when creating, modifying, or reviewing any skill in the Amazing PsyCoder package.

## Contents

1. [Keep each skill responsible for one stage](#1-keep-each-skill-responsible-for-one-stage)
2. [Use portable frontmatter](#2-use-portable-frontmatter)
3. [Design descriptions as routing rules](#3-design-descriptions-as-routing-rules)
4. [Keep activation context lean](#4-keep-activation-context-lean)
5. [Use progressive disclosure](#5-use-progressive-disclosure)
6. [Use imperative instructions and explicit gates](#6-use-imperative-instructions-and-explicit-gates)
7. [Define handoff artifacts](#7-define-handoff-artifacts)
8. [Define evidence-bounded outputs](#8-define-evidence-bounded-outputs)
9. [Maintain UI metadata](#9-maintain-ui-metadata)
10. [Validate before delivery](#10-validate-before-delivery)

## 1. Keep each skill responsible for one stage

- `amazing-psycoder`: route broad, ambiguous, multi-stage, and cross-pipeline requests.
- `psy-exp-designer`: resolve experiment-design decisions and produce experiment config.
- `psy-exp-coder`: implement or debug experiment code from confirmed config/code.
- `psy-exp-reviewer`: audit experiment artifacts without modifying them.
- `psy-ana-designer`: resolve analysis decisions and produce analysis config.
- `psy-ana-coder`: implement or debug R/Python analysis code.
- `psy-ana-reviewer`: audit analysis artifacts without modifying them.

Do not duplicate an entire neighboring workflow. Route to it and define the handoff artifact.

## 2. Use portable frontmatter

Start every `SKILL.md` with only `name` and `description`:

```yaml
---
name: psy-exp-coder
description: >-
  Generate, modify, or debug runnable psychological experiment code when a
  completed experiment config YAML or concrete existing code is available.
  Do not design unresolved experiment logic or issue readiness verdicts.
---
```

Requirements:

- Match `name` to the skill directory exactly.
- Use lowercase letters, digits, and hyphens only.
- Keep the description within 1024 characters.
- State what the skill does, concrete trigger contexts, required input state, and adjacent skills to use instead.
- Quote or fold descriptions that contain colons so YAML remains valid.
- Put version/status information in the body, not frontmatter.

## 3. Design descriptions as routing rules

Avoid broad keyword lists that make several skills activate for the same request. Prefer intent and artifact state:

| User state | Route |
|------------|-------|
| Idea or incomplete protocol | Designer |
| Confirmed config or existing code needing implementation/debugging | Coder |
| Artifact needing assessment/readiness judgment | Reviewer |
| Ambiguous, multi-stage, or cross-pipeline request | Orchestrator |

Include Chinese trigger phrases when they materially improve discovery, but do not repeat long multilingual synonym lists when the intent is already clear.

## 4. Keep activation context lean

- Keep the `SKILL.md` body under 500 lines.
- Keep routing, required inputs, core workflow, red lines, resource-loading rules, and output contract in `SKILL.md`.
- Move detailed schemas, examples, API mappings, checklists, and platform/paradigm knowledge into `references/`, `paradigms/`, or platform folders.
- Link every resource directly from `SKILL.md` and state exactly when to load it.
- Avoid duplicating the same rule in multiple files; identify one authoritative source.
- Add a table of contents to reference files over 100 lines.

## 5. Use progressive disclosure

Load only the resources needed for the current task:

1. Detect pipeline and stage.
2. Detect platform, paradigm, method, or chart type.
3. Load the matching platform contract and any exact optional design reference.
4. Avoid loading demos unless a lower-priority logic example is needed.

For experiment code generation, preserve priority:

```text
confirmed standalone config or frozen Studio ExperimentModel@4 > platform spec > config/Model mapping > exact optional design reference > raw demos
```

For review, use the same authoritative platform spec as the coder rather than maintaining a second anti-pattern list.

## 6. Use imperative instructions and explicit gates

- Write operational rules as commands: “Load…”, “Verify…”, “Do not…”, “Route…”.
- Distinguish blocking gates from recommendations.
- Define what evidence is required to pass a gate.
- Never claim runtime success from static inspection alone.
- Never silently infer critical design or analysis choices.
- Ask at most three focused questions per round when user input is genuinely required.

## 7. Define handoff artifacts

Every transition must name its artifact and precondition:

| Handoff | Required artifact | Precondition |
|---------|-------------------|--------------|
| Experiment Designer → Coder | experiment config + condition files | Gate 5 confirmed |
| Experiment Coder → Reviewer | code + conditions + run instructions | coder Quality Gate passed |
| Analysis Designer → Coder | `analysis_config.yaml` | analysis Gate 5 confirmed |
| Analysis Coder → Reviewer | script + report/notebook | coder Quality Gate passed |

Direct review of existing code may enter at Reviewer without replaying upstream stages. End-to-end generation must still pass the full pipeline.

## 8. Define evidence-bounded outputs

- Designer: confirmed decision registry + internal config + generated condition artifacts when required.
- Coder: runnable files + run instructions + Quality Gate results.
- Reviewer: scope, mode, evidence-backed findings, severity, readiness label, and recovery path.
- Do not let a reviewer fix code in the same role; send fixes to the matching Coder and re-audit afterward.

## 9. Maintain UI metadata

Add `agents/openai.yaml` with quoted strings:

```yaml
interface:
  display_name: "Experiment Coder"
  short_description: "Generate and debug cross-platform experiment code"
  default_prompt: "Use $psy-exp-coder to generate experiment code from my confirmed config."
```

Keep `short_description` between 25 and 64 characters. Make `default_prompt` one short sentence that explicitly names `$skill-name`.

## 10. Validate before delivery

- Run `python3 amazing-psycoder/scripts/validate_skills.py` from the repository root.
- Run the official `quick_validate.py` against every skill directory.
- Parse all frontmatter as YAML and verify directory/name equality.
- Verify all local Markdown links resolve.
- Verify every `SKILL.md` body stays under 500 lines.
- Verify every skill has matching `agents/openai.yaml` metadata.
- Search for stale counts, versions, contradictory gates, and duplicated authoritative rules.
- Preserve unrelated user changes and review the final diff.
