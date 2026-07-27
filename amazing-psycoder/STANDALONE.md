# Standalone Agent Profile

Amazing PsyCoder v1.4.0. This profile uses the same evidence states and
scientific semantics as Studio, while keeping YAML and artifacts in the user's
workspace.

Use this profile when Amazing PsyCoder is installed directly in Claude Code,
Codex, or another Agent Skills host and no PsyCoder Studio generation envelope
is present.

## Contract

1. The user workspace is the artifact store. Save each confirmed config,
   condition table, generated file, validation report, and audit report to disk;
   report every path to the user.
2. YAML is the default editable serialization. JSON is allowed when requested,
   but it must preserve the same semantic experiment or analysis model.
3. Load the selected nested `SKILL.md` and only the relevant platform,
   paradigm, method, or checklist references. Do not assume the host can invoke
   another skill by a product-specific command name.
4. If the host exposes sub-skill invocation, it may be used. Otherwise continue
   the Designer -> Coder -> Reviewer chain in the current task by reading the
   nested skill files directly and preserving the handoff artifacts on disk.
5. Adapt file, shell, search, and user-question actions to the tools actually
   available. Tool names in `PLATFORMS.md` are examples, not dependencies.
6. Run deterministic validators when their runtime is available. If Python or an
   optional parser is unavailable, state which checks were not run; never
   convert an unexecuted check into a pass.
7. Static review may authorize a pilot/smoke-test candidate only. Collection or
   publication readiness still requires the evidence defined by the relevant
   Reviewer skill.
8. Treat templates and paradigm documents as optional references. Persist every
   custom stimulus, condition, correctness, timing, randomization, and data rule
   in the confirmed config before generation. Never infer one Stroop-family
   variant from another.

## Capability Boundary

`runtime/capabilities.json` describes **PsyCoder Studio deployment support**. It
does not prohibit a standalone agent from generating a candidate for a platform
covered by the standalone Coder references. Standalone generation must still:

- state the selected platform reference and its evidence limitations;
- pin the intended framework/runtime version in the config;
- run available static validation;
- route the result through the read-only Reviewer;
- require target-machine smoke evidence before formal use.

## Expected Standalone Handoff

```text
user request
  -> saved confirmed config.yaml + conditions
  -> generated project candidate in a user-visible directory
  -> deterministic validation report
  -> read-only audit report
  -> smoke-test instructions and unresolved evidence list
```

Standalone use requires no Supabase, Redis, Stripe, Worker process, or PsyCoder
Studio account. Provider authentication and tool permissions remain owned by
the host application; this skill must never request that API keys be written
into experiment configs, generated projects, logs, or audit reports.
