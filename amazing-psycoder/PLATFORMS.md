# Platform Adapter Reference

Amazing PsyCoder keeps discovery frontmatter portable by using only `name` and `description`, following the currently supported subset documented by [agentskills.io](https://agentskills.io). Re-check host documentation before publishing because discovery paths, invocation syntax, and optional fields can change.

Host paths and invocation notes were last checked on **2026-07-27** against the
official [Claude Code skills](https://code.claude.com/docs/en/skills),
[OpenAI skill authoring](https://developers.openai.com/codex/skills),
[Hermes skills system](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md),
and [OpenClaw skills](https://docs.openclaw.ai/tools/skills) documentation.

---

## agentskills.io Standard (Baseline)

All platforms below implement this common specification. Key rules:

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | 1-64 chars, `a-z` `0-9` `-` only. Must match directory name. No leading/trailing/consecutive hyphens. |
| `description` | Yes | 1-1024 chars. Must include trigger keywords for agent auto-discovery. |
| `license` | No | Short license name (e.g., `MIT`). |
| `compatibility` | No | 1-500 chars. Environment requirements (system packages, network, intended product). |
| `metadata` | No | String→string key-value map. Extension point for platform-specific data. |
| `allowed-tools` | No | Space-delimited tool names. **Experimental** — support varies by platform. |

### Progressive Disclosure (3-stage loading)

1. **Discovery** (~100 tokens): Only `name` + `description` loaded at startup
2. **Activation** (<5000 tokens): Full `SKILL.md` body loaded when skill matches task
3. **Execution** (on demand): `scripts/`, `references/`, `assets/` loaded only when needed

**Best practice:** Keep `SKILL.md` under 500 lines. Move detailed reference material to `references/`.

---

## Supported Platforms

### Claude Code

| Item | Detail |
|------|--------|
| Personal directory | `${CLAUDE_CONFIG_DIR:-~/.claude}/skills/` |
| Project directory | `<repo>/.claude/skills/` |
| Install | `./install.sh claude` or `./install.sh --scope project --project-dir <repo> claude` |
| Invoke | `/amazing-psycoder` (slash command) |
| Sub-skill execution | Native invocation when available; otherwise the orchestrator reads the nested `SKILL.md` in the same task |
| Status | Installer path documented; actual routing/tool behavior must be verified in the target host version |

Do not infer installation or chain execution from file presence alone. After install, run the drift check, invoke the orchestrator, and smoke-test one experiment and one analysis route in the target host.

---

### Codex (OpenAI)

| Item | Detail |
|------|--------|
| Personal directory | `~/.agents/skills/` |
| Project directory | `<repo>/.agents/skills/` |
| Install (auto) | Type `$skill-installer`, then paste repo URL when prompted |
| Install | `./install.sh codex` or `./install.sh --scope project --project-dir <repo> codex` |
| Invoke (explicit) | `$amazing-psycoder` |
| Invoke (implicit) | Auto-match by `description` field |
| Sub-skill routing | Use `$skill-name` prefix for explicit calls. Auto-match works for implicit routing via description keywords. |

**Important notes:**
- Codex detects skill changes automatically; restart only if a change does not appear.
- The `$skill-installer` is an interactive built-in skill — it prompts for a repo URL, it does not accept the URL as a command argument.
- `$skill-creator` is a built-in skill for generating new skills interactively.

---

### Hermes (Nous Research)

| Item | Detail |
|------|--------|
| Skills directory | `~/.hermes/skills/` |
| Install this complete seven-skill suite | `./install.sh hermes` |
| Install (from catalog) | `hermes skills install official/<category>/<name>` |
| Install (manual) | Copy skill dirs to `~/.hermes/skills/` |
| Invoke | `/amazing-psycoder` or auto-match via description |
| Sub-skill routing | `/skills` slash panel, or `spawn` / `delegate` for sub-agents |
| Status | Paths/invocation shown as integration guidance; verify against the installed Hermes version |

**Hermes-specific frontmatter extensions:**

| Field | Purpose |
|-------|---------|
| top-level `platforms` | Restrict to `[macos, linux, windows]` |
| `metadata.hermes.tags` | Discovery keywords e.g. `[psychology, experiment, psychopy]` |
| `metadata.hermes.category` | Grouping e.g. `research` |
| `metadata.hermes.requires_toolsets` | e.g. `[terminal]` — skill hidden if toolset unavailable |
| `metadata.hermes.fallback_for_toolsets` | e.g. `[web]` — skill shown only when toolset unavailable |

**Known limitation:** Hermes' skill index reads frontmatter but may ignore body sections like "When to Use". Workaround: make `description` more explicit with trigger phrases.

---

### OpenClaw

| Item | Detail |
|------|--------|
| Workspace directory | `<workspace>/skills/` — highest precedence |
| Project-agent directory | `<workspace>/.agents/skills/` |
| Personal directory | `~/.agents/skills/` |
| Shared managed directory | `~/.openclaw/skills/` |
| Install this complete seven-skill suite | `./install.sh openclaw` |
| Project/workspace install | `./install.sh --scope project --project-dir <workspace> openclaw` |
| Native registry install | `openclaw skills install @owner/<slug>` for a published single skill |
| Invoke | Auto-match by description; slash-command visibility follows the installed OpenClaw version and frontmatter |
| Sub-skill routing | `agent` tool for sub-agent delegation |

**OpenClaw-specific frontmatter fields:**

| Field | Purpose |
|-------|---------|
| `user-invocable` | `true` (default) — exposed as slash command |
| `disable-model-invocation` | `true` — AI never auto-triggers, manual only |
| `metadata.openclaw.emoji` | Single emoji for UI display |
| `metadata.openclaw.requires.env` | Required environment variables |
| `metadata.openclaw.requires.bins` | Required CLI tools |
| `metadata.openclaw.requires.config` | Required config keys |
| `metadata.openclaw.os` | `["darwin", "linux", "win32"]` |
| `metadata.openclaw.install` | Auto-install instructions (brew, node, go, uv, shell) |

OpenClaw parses YAML frontmatter first and supports multi-line nested
`metadata.openclaw`. The single-line parser is only a fallback. Legacy
`metadata.clawdbot` remains accepted when `metadata.openclaw` is absent.

---

## Tool Mapping

When a sub-skill references an action, use the capability actually exposed by the current host. The names below are historical/common examples, not an API guarantee:

| Action | Claude Code | Codex | Hermes | OpenClaw |
|--------|-------------|-------|--------|----------|
| Shell command | `Bash` | `shell` | `shell` | `exec` |
| Read file | `Read` | `read` | `read` | `read` |
| Write file | `Write` | `write` | `write` | `write` |
| Edit file | `Edit` | `edit` | `edit` | `edit` |
| Sub-agent | `Agent` | `task` | `spawn` | `agent` |
| Ask user | `AskUserQuestion` | `ask` | `ask` | `prompt` |
| Web search | `WebSearch` | `web_search` | `search` | `search` |
| Web fetch | `WebFetch` | `web_fetch` | `fetch` | `fetch` |

---

## Quick Install (Recommended)

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
./install.sh              # 自动检测平台
./install.sh claude       # 或手动指定
./install.sh --scope project --project-dir /path/to/repo codex
./install.sh --scope project --project-dir /path/to/workspace openclaw
./install.sh --check codex # 只检查安装漂移，不修改文件
```

Auto-detection installs only when one supported host can be identified
unambiguously. Otherwise, pass `claude`, `codex`, `hermes`, or `openclaw`
explicitly.

## Manual Installation (All Platforms)

Pass an absolute skills directory when the host uses a custom location:

```bash
./install.sh /absolute/path/to/skills
./install.sh --check /absolute/path/to/skills
```

The installer validates all seven manifests, stages the complete batch, and
rolls the whole installation back if any replacement fails. Avoid copying only
one sub-skill: the pipeline depends on sibling references and handoff contracts.

---

## Validation Scope and Evidence

Installation compatibility and generated-project runtime compatibility are
different claims:

| Layer | Automated evidence in this repository | Still required on the target system |
|---|---|---|
| Claude Code / Codex / Hermes / OpenClaw installation | Temporary-directory install, rollback, drift, and path tests for all four hosts | Host discovery, invocation, restart, tool mapping, and one routed experiment/analysis smoke test |
| PsychoPy | Python parse plus experiment static-contract checks | PsychoPy dependency install, display/input launch, timing and device smoke tests |
| jsPsych 8.x | Node.js syntax plus experiment static-contract checks | Supported browser deployment, persistence, timing and device tests |
| Psychtoolbox | MATLAB-oriented static-contract checks | MATLAB/Octave `checkcode`, Psychtoolbox sync tests, display/input/audio calibration |
| Python analysis | Python AST/static-contract checks plus a clean paired-analysis fixture whose run/input/output/environment hashes are verified | Clean execution against the user's real schema/data, diagnostics and result review |
| R analysis | R static/parse checks plus a `renv`-restored paired-analysis fixture whose run/input/output/environment hashes are verified | Clean execution against the user's real schema/data, diagnostics and result review |

The installer uses the standard-library-only portable preflight, so installing
the skills does not require Studio services or contributor test dependencies.
Before an analysis Designer/Coder/Reviewer runs `validate_analysis.py`, use an
isolated interpreter with the packaged validation dependencies; do not assume
the host's default `python3` has PyYAML:

```bash
AMAZING_PSYCODER_ROOT="/absolute/path/to/amazing-psycoder"
python3 -m venv .venv-validation
. .venv-validation/bin/activate
python -m pip install -r "$AMAZING_PSYCODER_ROOT/requirements-dev.txt"
export PYTHON_BIN="$(command -v python)"
"$PYTHON_BIN" -c "import yaml"
```

Release and contributor validation remains strict:

```bash
python amazing-psycoder/scripts/validate_skills.py
python -m unittest discover -s amazing-psycoder/tests -v
```

Static success is a gate to runtime testing. It is never evidence by itself for
`ready_for_collection` or `ready_for_publication`.

---

## Platform-Specific Caveats

| Platform | Caveat |
|----------|--------|
| **Claude Code** | Verify discovery, restart behavior, and inter-skill invocation in the installed version. |
| **Codex** | Personal installs use `~/.agents/skills`; project installs use `.agents/skills`. Codex normally detects changes automatically; restart only if needed and use `--check` to detect stale copies. |
| **Hermes** | The hub can install individual GitHub skill paths, but this repository is a coordinated seven-skill suite; use the transactional installer. Description should include explicit trigger phrases. |
| **OpenClaw** | Workspace, `.agents`, personal, and managed roots have different precedence. The installer uses the shared managed root for user scope and `.agents/skills` for project scope. OpenClaw YAML frontmatter supports nested metadata. |

---

## Adding a New Platform

1. Add a section to Supported Platforms above with directory paths, install commands, and invocation methods
2. Add tool mappings to the Tool Mapping table
3. Add manual install commands
4. Document any platform-specific frontmatter extensions or caveats
5. Update all `README.md` installation sections
6. If the platform has a registry, publish the skill there
