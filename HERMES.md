# skillsets for Hermes

This repository is a single plugin that bundles eight self-contained engineering and research skills compatible with Hermes Agent. Each skill is a model-agnostic instruction set: it classifies the task, gathers evidence, applies domain references, and verifies before handoff.

## Install for Hermes

```bash
hermes skills tap add https://github.com/oghie/skillsets
```

Then restart Hermes or run `/reload-skills`. Skills auto-surface by name and description.

## Skills

- `skills/android-offsec` — Android offensive security, forensic extraction, mobile app exploitation.
- `skills/academic-research-journal` — Evaluate, design, draft, revise academic articles and reviews.
- `skills/data-architect-engineering` — Design, review, migrate, optimize SQL/NoSQL/vector/graph systems.
- `skills/device-driver-development` — Linux kernel device drivers, modules, device tree, DMA/IRQ.
- `skills/realtime-systems-coding` — Concurrent, parallel, distributed, real-time, network-dataplane systems.
- `skills/software-architecture-engineering-uap` — Software architecture design, evaluation, modernization.
- `skills/tech-leadership` — CTO and technology leadership: strategy, people, delivery, risk, governance.
- `skills/uiux-frontend-engineering` — UI/UX design, frontend implementation, design systems, XR interfaces.

## Usage

When a task matches a skill's description, Hermes loads that skill's `SKILL.md` automatically. Each skill's `tasks/`, `references/`, and `scripts/` provide detailed workflows and domain knowledge.
