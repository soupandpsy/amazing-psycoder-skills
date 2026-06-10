# Platform Adapter Reference

Amazing PsyCoder follows the [agentskills.io](https://agentskills.io) open standard (v2026). All `SKILL.md` files use standard frontmatter fields (`name`, `description`) plus optional fields (`version`, `status`, `compatibility`) and work across platforms without modification.

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
| Skills directory | `~/.claude/skills/` |
| Install (auto) | `Install Amazing PsyCoder for me: https://github.com/soupandpsy/amazing-psycoder-skills` |
| Invoke | `/amazing-psycoder` (slash command) |
| Sub-skill invocation | `Skill` tool or `Agent` tool with sub-agent routing |
| Status | **Fully tested** — both experiment (3-skill) and analysis (3-skill) chains work natively |

Claude Code auto-clones the repo and registers skill files. The one-line install command triggers this flow. All sub-skills (Experiment: Designer → Coder → Reviewer; Analysis: Designer → Coder → Reviewer) are invoked via the orchestrator's routing tree.

---

### Codex (OpenAI)

| Item | Detail |
|------|--------|
| Skills directory (current) | `$HOME/.agents/skills/` (user) or `.agents/skills/` (project) |
| Skills directory (legacy) | `~/.codex/skills/` (still supported, migration encouraged) |
| Install (auto) | Type `$skill-installer`, then paste repo URL when prompted |
| Install (manual) | Copy skill dirs to skills directory, restart Codex |
| Invoke (explicit) | `$amazing-psycoder` |
| Invoke (implicit) | Auto-match by `description` field |
| Sub-skill routing | Use `$skill-name` prefix for explicit calls. Auto-match works for implicit routing via description keywords. |

**Important notes:**
- Codex must be **restarted** after installing new skills for discovery to pick them up.
- The `$skill-installer` is an interactive built-in skill — it prompts for a repo URL, it does not accept the URL as a command argument.
- Codex searches skills in priority order: bundled → admin → user → repo root → repo local.
- `$skill-creator` is a built-in skill for generating new skills interactively.

---

### Hermes (Nous Research)

| Item | Detail |
|------|--------|
| Skills directory | `~/.hermes/skills/` |
| Install (auto) | `hermes skills install https://github.com/soupandpsy/amazing-psycoder-skills` |
| Install (from catalog) | `hermes skills install official/<category>/<name>` |
| Install (manual) | Copy skill dirs to `~/.hermes/skills/` |
| Invoke | `/amazing-psycoder` or auto-match via description |
| Sub-skill routing | `/skills` slash panel, or `spawn` / `delegate` for sub-agents |
| Status | Slash-command invocation supported. Skills auto-improve after use. |

**Hermes-specific frontmatter extensions** (under `metadata`):

| Field | Purpose |
|-------|---------|
| `tags` | Discovery keywords e.g. `[psychology, experiment, psychoPy]` |
| `category` | Grouping e.g. `research` |
| `platforms` | Restrict to `[macos, linux, windows]` |
| `requires_toolsets` | e.g. `[terminal]` — skill hidden if toolset unavailable |
| `fallback_for_toolsets` | e.g. `[web]` — skill shown only when toolset unavailable |

**Known limitation:** Hermes' skill index reads frontmatter but may ignore body sections like "When to Use". Workaround: make `description` more explicit with trigger phrases.

---

### OpenClaw

| Item | Detail |
|------|--------|
| Skills directory (workspace) | `~/.openclaw/workspace/skills/` — highest priority, manual install |
| Skills directory (ClawHub) | `~/.openclaw/skills/` — from `clawhub install` |
| Install (ClawHub) | `npm i -g clawhub && clawhub install amazing-psycoder` |
| Install (manual) | Copy to `~/.openclaw/workspace/skills/`, restart gateway |
| Invoke | Auto-match by description; or `/amazing-psycoder` if `user-invocable: true` |
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

**Important:** `metadata` must be a **single-line JSON string** in OpenClaw (parser limitation). The keys `metadata.clawdbot` and `metadata.clawdis` are accepted as aliases for `metadata.openclaw`.

---

## Tool Mapping

When a sub-skill references a tool, adapt to the platform's equivalent:

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
```

## Manual Installation (All Platforms)

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills /tmp/amazing-psycoder-skills

# Claude Code
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder ~/.claude/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-designer ~/.claude/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-coder ~/.claude/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-reviewer ~/.claude/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-designer ~/.claude/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-coder ~/.claude/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-reviewer ~/.claude/skills/

# Codex (current path: $HOME/.agents/skills/)
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder ~/.agents/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-designer ~/.agents/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-coder ~/.agents/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-reviewer ~/.agents/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-designer ~/.agents/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-coder ~/.agents/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-reviewer ~/.agents/skills/
# Restart Codex after install

# Hermes
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder ~/.hermes/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-designer ~/.hermes/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-coder ~/.hermes/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-reviewer ~/.hermes/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-designer ~/.hermes/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-coder ~/.hermes/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-reviewer ~/.hermes/skills/

# OpenClaw (workspace path)
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder ~/.openclaw/workspace/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-designer ~/.openclaw/workspace/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-coder ~/.openclaw/workspace/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-exp-reviewer ~/.openclaw/workspace/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-designer ~/.openclaw/workspace/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-coder ~/.openclaw/workspace/skills/
cp -r /tmp/amazing-psycoder-skills/amazing-psycoder/psy-ana-reviewer ~/.openclaw/workspace/skills/
# Restart gateway: openclaw gateway restart
```

---

## Platform-Specific Caveats

| Platform | Caveat |
|----------|--------|
| **Claude Code** | Fully tested. Native inter-skill communication. No restart needed after install. |
| **Codex** | Must **restart** after install. `~/.codex/skills/` is legacy — prefer `~/.agents/skills/`. Sub-skill chaining needs `$skill-name` prefix. |
| **Hermes** | `hermes skills install` supports GitHub URLs directly. Frontmatter `tags` field recommended for discovery. Description should include explicit trigger phrases. |
| **OpenClaw** | Published on [ClawHub](https://clawhub.ai/soupandpsy/amazing-psycoder). `clawhub install amazing-psycoder` works directly. Restart gateway after install. `metadata` must be single-line JSON. |

---

## Adding a New Platform

1. Add a section to Supported Platforms above with directory paths, install commands, and invocation methods
2. Add tool mappings to the Tool Mapping table
3. Add manual install commands
4. Document any platform-specific frontmatter extensions or caveats
5. Update all `README.md` installation sections
6. If the platform has a registry, publish the skill there
