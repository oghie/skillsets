# skillsets

This repository is a single plugin that bundles eight self-contained engineering and research skills compatible with Hermes, Claude Code, Codex, OpenCode, and Antigravity (Gemini). Each skill is a model-agnostic instruction set: it classifies the task, gathers evidence, applies domain references, and verifies before handoff.

Each skill auto-surfaces by its name and description. When a task matches a skill's description, read that skill's `skills/<name>/SKILL.md` first and follow its workflow. The detailed `tasks/`, `references/`, and `scripts/` under each skill directory are the source of truth.

Hermes reads `HERMES.md` for project context and discovers skills through the plugin manifest at `.hermes-plugin/plugin.json`. OpenCode reads `AGENTS.md` and discovers skills through `.opencode/skills/`, which points back to `skills/`. Do not duplicate skill source material across platform-specific mirrors.

## Skills

- `skills/android-offsec` — Android offensive security, forensic extraction, mobile app exploitation: lock screen bypass, APK reversing, deeplink fuzzing, kernel/GPU exploit research, rogue WiFi attacks, deepfake social engineering, and chain-of-custody device investigation.
- `skills/academic-research-journal` — Evaluate, design, draft, revise, and stress-test academic articles, literature and systematic reviews, journal submissions, reviewer responses, and source/integrity audits.
- `skills/data-architect-engineering` — Design, review, migrate, optimize, secure, and operate SQL, NoSQL, vector, graph, document, time-series, search, cache, big-data, lakehouse, and warehouse systems, including DBMS internals.
- `skills/device-driver-development` — Develop, review, debug, port, and engineer Linux kernel device drivers, kernel modules, device tree bindings, bus clients, DMA/IRQ/memory paths, userspace ABIs, and hardware bring-up.
- `skills/realtime-systems-coding` — Build concurrent, parallel, distributed, real-time, and network-dataplane software: locks, monitors, MPI/CSP, DPDK/VPP, eBPF/XDP/AF_XDP, SR-IOV, RDMA, and RMS/EDF scheduling.
- `skills/software-architecture-engineering-uap` — Design, evaluate, document, modernize, refactor, and implement software architecture and code structure: requirements, context, style selection, architecture views, clean code, NFR tactics, IAM/auth, security patterns, cost, fitness functions, and ADR/RFC work.
- `skills/tech-leadership` — Advise, plan, review, and operate CTO and technology leadership work across strategy, cybersecurity, requirements, framework selection, people, delivery, risk, KPIs, roadmap, budgeting, governance, and stakeholder communication.
- `skills/uiux-frontend-engineering` — Design, review, implement, and validate UI/UX and frontend experiences for web, mobile, responsive apps, design systems, accessibility, theme/token application, and XR/spatial interfaces.
