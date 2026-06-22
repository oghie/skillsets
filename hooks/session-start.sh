#!/usr/bin/env bash
# SessionStart hook for the skillsets plugin.
# Emits a brief orientation so the agent knows the 7 skills exist and reads the
# matching skills/<name>/SKILL.md when a task fits. No-ops safely if jq is absent
# (the skills still auto-surface natively without this hint).
set -euo pipefail

command -v jq >/dev/null 2>&1 || exit 0

ctx=$(printf '%s\n' \
"skillsets plugin is active. It bundles 7 engineering and research skills." \
"When a task matches one of these, read skills/<name>/SKILL.md first and follow its workflow:" \
"- software-architecture-engineering-uap: architecture design, evaluation, modernization, IAM/auth, NFR, ADR/RFC." \
"- uiux-frontend-engineering: UI/UX and frontend, design systems, accessibility, responsive, XR/spatial." \
"- data-architect-engineering: SQL/NoSQL/vector/graph/warehouse design, migration, optimization, operations." \
"- device-driver-development: Linux kernel drivers, modules, device tree, DMA/IRQ, bring-up, upstreaming." \
"- realtime-systems-coding: concurrency, real-time, dataplane; locks/monitors, RMS/EDF, DPDK/XDP, kernel bypass." \
"- tech-leadership: CTO and technology leadership; strategy, delivery, risk, KPIs, roadmap, governance." \
"- academic-research-journal: academic articles, literature/systematic reviews, journal submissions, source audits.")

jq -n --arg ctx "$ctx" \
  '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}'
