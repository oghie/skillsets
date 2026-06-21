# skillsets

A personal collection of agent skills for software and research engineering. Each
skill is a self-contained, model-agnostic instruction set that runs on both Claude
(Claude Code) and Codex from the same source.

## About

Every skill encodes a disciplined workflow rather than a prompt: classify the task,
gather evidence, apply domain references, and verify before handoff. The goal is to
keep agent output grounded in explicit forces, trade-offs, and a verification path
instead of surface-level answers.

## Skills

| Skill | Scope |
| --- | --- |
| `software_architecture_skill` | Design, evaluate, document, and modernize software architecture; IAM/auth design; NFR tactics; ADR/RFC; implementation planning. |
| `uiux_frontend_skill` | Research, design, implement, and validate UI/UX and frontend interfaces for web, mobile, responsive apps, design systems, theme tokens, and XR/spatial surfaces. |
| `data_architect_engineering_skill` | Design, review, migrate, optimize, secure, and operate SQL, NoSQL, vector, graph, search, cache, big-data, lakehouse, and warehouse systems. |
| `device_driver_development_skill` | Linux kernel device drivers, modules, device tree bindings, bus clients, DMA/IRQ/memory paths, bring-up, and upstreaming. |
| `realtime_systems_coding_skill` | Concurrent, parallel, distributed, real-time, and network-dataplane systems; locks/monitors, RMS/EDF scheduling, DPDK/XDP, kernel bypass. |
| `academic_research_journal_skill` | Evaluate, design, draft, and revise academic articles, literature/systematic reviews, journal submissions, and source/integrity audits. |

## Layout

Each skill directory follows the same convention:

```
<skill>/
  SKILL.md            # Claude skill manifest (frontmatter: name, description)
  agent.md            # Agent identity and operating model
  agents/openai.yaml  # Codex interface config and default prompt
  tasks/              # Step-by-step task workflows
  references/         # Domain reference material
  scripts/            # Helper scripts (static scans, probes)
  commands/           # Slash commands (where applicable)
```

## Usage

### Claude (Claude Code)

Place or symlink a skill directory where Claude Code discovers skills (for example
`~/.claude/skills/` or a plugin's skills path). Claude reads `SKILL.md`; the
`description` field drives auto-invocation.

### Codex

Skills load from `agents/openai.yaml`. `allow_implicit_invocation: true` lets the
agent trigger a skill from its `default_prompt`, or you can call it explicitly with
`$<skill-name>`, e.g. `$realtime-systems-coding`.

Both runtimes read the same `tasks/`, `references/`, and `scripts/`, so behavior
stays consistent regardless of the host.

## Conventions

- Evidence over assertion: name the forces, trade-offs, and verification path before
  recommending anything.
- Version-sensitive facts (kernel APIs, library behavior) are verified against
  current sources, not assumed.
- `references/` is the source of truth per domain; `tasks/` orchestrates the workflow.
