# skillsets

A personal collection of agent skills for software and research engineering, packaged
as a single cross-platform plugin. Each skill is a self-contained, model-agnostic
instruction set that runs on Claude (Claude Code), Codex, and Antigravity (Gemini) from
the same source.

## About

Every skill encodes a disciplined workflow rather than a prompt: classify the task,
gather evidence, apply domain references, and verify before handoff. The goal is to
keep agent output grounded in explicit forces, trade-offs, and a verification path
instead of surface-level answers.

## Skills

| Skill | Scope |
| --- | --- |
| `skills/software-architecture-engineering-uap` | Design, evaluate, document, and modernize software architecture; IAM/auth design; NFR tactics; ADR/RFC; implementation planning. |
| `skills/uiux-frontend-engineering` | Research, design, implement, and validate UI/UX and frontend interfaces for web, mobile, responsive apps, design systems, theme tokens, and XR/spatial surfaces. |
| `skills/data-architect-engineering` | Design, review, migrate, optimize, secure, and operate SQL, NoSQL, vector, graph, search, cache, big-data, lakehouse, and warehouse systems. |
| `skills/device-driver-development` | Linux kernel device drivers, modules, device tree bindings, bus clients, DMA/IRQ/memory paths, bring-up, and upstreaming. |
| `skills/realtime-systems-coding` | Concurrent, parallel, distributed, real-time, and network-dataplane systems; locks/monitors, RMS/EDF scheduling, DPDK/XDP, kernel bypass. |
| `skills/tech-leadership` | CTO and technology leadership: strategy, cybersecurity, requirements, framework selection, people, delivery, risk, KPIs, roadmap, budgeting, and governance. |
| `skills/academic-research-journal` | Evaluate, design, draft, and revise academic articles, literature/systematic reviews, journal submissions, and source/integrity audits. |

## Layout

The repository is one plugin. Skills live under `skills/`, and each platform reads its
own manifest:

```
.claude-plugin/
  plugin.json         # Claude Code plugin metadata
  marketplace.json    # Claude Code marketplace entry
.codex-plugin/
  plugin.json         # Codex plugin metadata + interface
gemini-extension.json # Antigravity (Gemini) extension manifest
GEMINI.md             # Antigravity context file (includes AGENTS.md)
AGENTS.md             # Cross-platform agent orientation
hooks/
  hooks.json          # SessionStart orientation hook (Claude Code)
  session-start.sh    # emits the skillset orientation as additionalContext
.mcp.json             # MCP servers (empty)
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

### Antigravity (Gemini)

Install this repository as a Gemini extension. Antigravity reads
`gemini-extension.json` and loads `GEMINI.md`, which pulls in `AGENTS.md` for shared
agent orientation.

## Usage

Each skill auto-surfaces by name and description. When a task matches a skill's
description, the agent reads that skill's `skills/<name>/SKILL.md` and follows its
workflow. All runtimes read the same `tasks/`, `references/`, and `scripts/`, so
behavior stays consistent regardless of the host.

## Conventions

- Evidence over assertion: name the forces, trade-offs, and verification path before
  recommending anything.
- Version-sensitive facts (kernel APIs, library behavior) are verified against
  current sources, not assumed.
- `references/` is the source of truth per domain; `tasks/` orchestrates the workflow.
