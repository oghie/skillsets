# skillsets

A personal collection of agent skills for software and research engineering, packaged
as a single cross-platform plugin. Each skill is a self-contained, model-agnostic
instruction set that runs on Claude (Claude Code), Codex, OpenCode, Antigravity
(Gemini), and Hermes from the same source.

## About

Every skill encodes a disciplined workflow rather than a prompt: classify the task,
gather evidence, apply domain references, and verify before handoff. The goal is to
keep agent output grounded in explicit forces, trade-offs, and a verification path
instead of surface-level answers.

## Skills

| Skill | Scope |
| --- | --- |
| `skills/android-offsec` | Android offensive security, forensic extraction, mobile app exploitation, APK reversing, lock screen bypass, deeplink exploitation, rogue network attacks, deepfake social engineering, and mobile device investigation with chain of custody. |
| `skills/software-architecture-engineering-uap` | Design, evaluate, document, modernize, and refactor software architecture and code structure; microservices patterns; clean code; IAM/auth; NFR tactics; ADR/RFC; implementation planning. |
| `skills/uiux-frontend-engineering` | Research, design, implement, and validate UI/UX and frontend interfaces for web, mobile, responsive apps, design systems, theme tokens, and XR/spatial surfaces. |
| `skills/data-architect-engineering` | Design, review, migrate, optimize, secure, and operate SQL, NoSQL, vector, graph, search, cache, big-data, lakehouse, and warehouse systems. |
| `skills/device-driver-development` | Linux kernel device drivers, modules, device tree bindings, bus clients, DMA/IRQ/memory paths, bring-up, and upstreaming. |
| `skills/realtime-systems-coding` | Concurrent, parallel, distributed, real-time, and network-dataplane systems; locks/monitors, RMS/EDF scheduling, DPDK/XDP, kernel bypass. |
| `skills/tech-leadership` | CTO and technology leadership: strategy, cybersecurity, requirements, framework selection, people, delivery, risk, KPIs, roadmap, budgeting, and governance. |
| `skills/academic-research-journal` | Evaluate, design, draft, and revise academic articles, literature/systematic reviews, journal submissions, and source/integrity audits. |
| `skills/cyber-security-operations` | Cyber security operations: detection/hunting, DFIR/forensics, incident response, vulnerability management, supply chain security, DevSecOps, crypto/AI emerging threats, and offensive security. |

## Layout

The repository is one plugin. Skills live under `skills/`, and each platform reads its
own manifest:

```
.claude-plugin/
  plugin.json         # Claude Code plugin metadata
  marketplace.json    # Claude Code marketplace entry
.codex-plugin/
  plugin.json         # Codex plugin metadata + interface
.opencode/
  skills/             # OpenCode project-local skill mirror (symlinks to skills/)
opencode.json         # OpenCode config and project instruction wiring
gemini-extension.json # Antigravity (Gemini) extension manifest
GEMINI.md             # Antigravity context file (includes AGENTS.md)
AGENTS.md             # Cross-platform agent orientation
hooks/
  hooks.json          # SessionStart orientation hook (Claude Code)
  session-start.sh    # emits the skillset orientation as additionalContext
.mcp.json             # MCP servers (Context7, GitHub, Postgres, arXiv)
LICENSE               # MIT
skills/
  <skill>/
    SKILL.md            # Claude skill manifest (frontmatter: name, description)
    agent.md            # Agent identity and operating model
    agents/openai.yaml  # Codex interface config and default prompt
    tasks/              # Step-by-step task workflows
    references/         # Domain reference material
    scripts/            # Helper scripts (static scans, probes)
    commands/           # Slash commands (where applicable)
```

## Install

### Claude (Claude Code)

```
claude plugin marketplace add oghie/skillsets
claude plugin install skillsets
```

Skills under `skills/` auto-discover; Claude reads each `SKILL.md` and the
`description` field drives auto-invocation.

### Codex

Install the plugin from the same repository (`oghie/skillsets`). Codex reads
`.codex-plugin/plugin.json`, which points at `./skills/` and exposes the bundled
skills through its interface block.

### OpenCode

Clone this repository and run OpenCode from the repo root:

```
opencode
```

OpenCode reads `AGENTS.md`, `opencode.json`, and the project-local
`.opencode/skills/<name>/SKILL.md` paths. The `.opencode/skills/` entries are symlinks
to the committed `skills/` directories, so Claude, Codex, OpenCode, and Antigravity use
the same source material.

### Antigravity (Gemini)

Install this repository as a Gemini extension. Antigravity reads
`gemini-extension.json` and loads `GEMINI.md`, which pulls in `AGENTS.md` for shared
agent orientation.

## MCP servers

The plugin ships a `.mcp.json` with four optional MCP servers. They are lazy-loaded
and only matter for skills that benefit from live external data; each needs its own
runtime and, where noted, configuration. A server that is not configured simply fails
to start and shows up in `/mcp` — it does not block a session.

| Server | Backs | Runtime | Configuration |
| --- | --- | --- | --- |
| `context7` | All engineering skills (current library/API docs) | Node 18+ (`npx`) | None required; set `CONTEXT7_API_KEY` for higher rate limits. |
| `github` | tech-leadership, software-architecture (repos, issues, PRs) | none (remote HTTP) | OAuth on first use against `https://api.githubcopilot.com/mcp/`. |
| `postgres` | data-architect-engineering (schema, EXPLAIN, index tuning) | `uv` (`uvx postgres-mcp`) | Optional. Set `DATABASE_URI` to your connection string to activate it; if unset it stays inactive and the plugin loads normally. Runs in `restricted` (read-only) mode. |
| `arxiv` | academic-research-journal (paper search, source audits) | `uv` (`uvx arxiv-mcp-server`) | None required. |

Notes:
- `postgres` uses Postgres MCP Pro (`postgres-mcp`), not the archived
  `@modelcontextprotocol/server-postgres`. `restricted` access mode wraps queries in
  read-only transactions.
- Install `uv` (https://docs.astral.sh/uv/) for the `postgres` and `arxiv` servers, and
  Node 18+ for `context7`.
- Remove any server you do not use by deleting its entry from `.mcp.json`.

## Usage

Each skill auto-surfaces by name and description. When a task matches a skill's
description, the agent reads that skill's `skills/<name>/SKILL.md` or platform-local
mirror and follows its workflow. All runtimes read the same `tasks/`, `references/`,
and `scripts/`, so behavior stays consistent regardless of the host.

### For newbies (install from scratch)

If you have none of these tools yet, pick a platform and follow two steps: install the
CLI, then install skillsets.

**Claude Code**

1. Install the CLI:
   - macOS / Linux: `curl -fsSL https://claude.ai/install.sh | bash`
   - Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`
   - Any OS with Node 18+: `npm install -g @anthropic-ai/claude-code`
   - Check it works: `claude --version`
2. Install skillsets:
   ```
   claude plugin marketplace add oghie/skillsets
   claude plugin install skillsets
   ```

**Codex**

1. Install the CLI:
   - Any OS with Node 18+: `npm install -g @openai/codex`
   - macOS (Homebrew): `brew install codex`
   - Check it works: `codex --version`
2. Install skillsets:
   ```
   codex plugin marketplace add oghie/skillsets
   codex plugin install skillsets
   ```
   Or run `/plugins` inside Codex to browse and install it.

**OpenCode**

1. Install the CLI:
   - macOS / Linux: `curl -fsSL https://opencode.ai/install | bash`
   - Any OS with Node 18+: `npm install -g opencode-ai`
   - macOS (Homebrew): `brew install anomalyco/tap/opencode`
   - Check it works: `opencode --version`
2. Use skillsets:
   ```
   git clone https://github.com/oghie/skillsets.git
   cd skillsets
   opencode
   ```
   OpenCode loads `AGENTS.md`, `opencode.json`, and `.opencode/skills/*`.

**Antigravity**

1. Download and install the Antigravity desktop app for Windows, macOS, or Linux from
   https://antigravity.google, then sign in.
2. Install skillsets as a Gemini extension:
   ```
   gemini extensions install https://github.com/oghie/skillsets
   ```
   Antigravity loads the repo's `gemini-extension.json` and `GEMINI.md`. Update later
   with `gemini extensions update skillsets`.

**Hermes**

1. Install Hermes Agent:
   - macOS / Linux: `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`
   - Check it works: `hermes --version`
2. Install skillsets:
   ```
   hermes skills tap add https://github.com/oghie/skillsets
   ```
   Then restart Hermes or run `/reload-skills`. Skills auto-surface by name and description.

**After installing (all platforms)**

- Restart the CLI or app so the skills load, then start a session and ask about one of
  the skill domains; the matching skill loads on its own.
- The optional MCP servers need extra runtimes — Node 18+ for `context7`, and `uv` for
  `postgres` and `arxiv` (see [MCP servers](#mcp-servers)). Quick installs:
  - macOS: `brew install node uv`
  - Linux: Node from your package manager or nvm; uv via `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): install Node from nodejs.org; uv via `irm https://astral.sh/uv/install.ps1 | iex`

## Conventions

- Evidence over assertion: name the forces, trade-offs, and verification path before
  recommending anything.
- Version-sensitive facts (kernel APIs, library behavior) are verified against
  current sources, not assumed.
- `references/` is the source of truth per domain; `tasks/` orchestrates the workflow.
- Shipped skills are self-contained and carry no external runtime dependencies.
