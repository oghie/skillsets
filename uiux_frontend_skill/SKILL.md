---
name: uiux-frontend-engineering
description: Use when designing, reviewing, implementing, or validating UI/UX and frontend experiences for web, mobile, responsive apps, design systems, Figma-to-code handoff, accessibility, interaction design, UX research, usability testing, psychology-based UX decisions, theme/token application, or XR/spatial interfaces.
---

# UIUX Frontend Engineering

## Core Rule
Treat UI as a tested product interface, not decoration: connect user goals, business goals, interaction model, visual system, implementation constraints, and validation evidence before shipping screens or components.

## First Pass
1. Classify the task: UX strategy, research, IA/user flow, wireframe, visual UI, design system, frontend implementation, responsive/mobile, accessibility, redesign/review, handoff, or XR/spatial interface.
2. Identify target surface: web, mobile web, native mobile, desktop web app, kiosk, embedded screen, WebXR, VR, AR, MR, or spatial computing.
3. Name users, context, primary jobs, failure modes, conversion or task metric, platform constraints, input method, and trust/safety concerns.
4. Decide fidelity: sketch/flow, low-fidelity wireframe, clickable prototype, high-fidelity visual, coded prototype, production component, or XR graybox.
5. Select validation before implementation: heuristic review, accessibility audit, responsive screenshots, usability test, click/first-impression test, A/B test, performance check, or XR comfort review.

## Required Reads By Task
- End-to-end UX process, discovery, personas, user interviews, analytics, card sorting, surveys, support tickets, wireframes, validation, handoff, or QA: `references/ux-process-and-research.md`.
- Psychology laws, cognitive load, target sizing, choice overload, familiarity, aesthetics, memory, complexity, responsiveness, ethics, or dark-pattern risk: `references/psychology-and-interaction-laws.md`.
- Visual UI composition, Gestalt, hierarchy, color, typography, spacing, affordance, signifiers, navigation, forms, cards, states, icons, illustrations, or motion: `references/visual-interface-composition.md`.
- Figma, design systems, tokens, components, auto layout, constraints, responsive/adaptive design, plugin/handoff flow, or developer collaboration: `references/responsive-design-systems-and-handoff.md`.
- Frontend implementation, accessibility, performance, state coverage, visual QA, component contracts, CSS/Tailwind/React/React Native mapping, or production readiness: `references/frontend-implementation-quality.md`.
- Mobile/touch design, one-handed use, touch targets, mobile navigation, forms, gestures, device preview, or native-app constraints: `references/mobile-and-touch-ux.md`.
- XR, spatial computing, WebXR, VR, AR, MR, 3D UI, spatial objects, OOUX, locomotion, comfort, haptics, voice, gaze, avatars, embodiment, safety, or spatial analytics: `references/xr-spatial-ux-and-3d-interfaces.md`.
- AI-assisted design, generative assets, design copilots, AI disclosure, sourcing, IP, safety, privacy, transparency, or manipulation risk: `references/ai-assisted-and-ethical-design.md`.
- Theme/style selection, static token database, CSS variables, Tailwind theme mapping, or visual style guardrails: `references/theme-token-database.md` and the relevant file under `theme/`.

## Task Playbooks
- Build or redesign a product UI: `tasks/product-ui-build.md`.
- Convert theme/style into implementation tokens and components: `tasks/design-system-token-implementation.md`.
- Review an existing UI/UX or frontend: `tasks/usability-review-and-redesign.md`.
- Build responsive or mobile-first frontend: `tasks/responsive-mobile-frontend.md`.
- Design or review XR/spatial interface: `tasks/xr-spatial-interface-design.md`.
- Prepare prototype validation, handoff, and QA: `tasks/prototype-validation-handoff.md`.

## Theme Contract
- Do not modify `theme/` unless the user explicitly asks for theme authoring.
- Treat `theme/index.yaml` as the registry and each style file as the source of truth.
- Read `theme/_schema/style.schema.yaml` only when field meaning is unclear.
- Prefer a style because its `use_cases`, `mood`, `keywords`, and `avoid_when` match the product, not because it looks novel.
- Map tokens directly into implementation variables; do not invent a parallel palette, radius scale, spacing scale, or motion personality.

## Design Discipline
- Start with the user's task and failure path, then choose UI structure.
- Use familiar patterns by default; depart from convention only when the new pattern improves the core task and can be tested.
- Design every interactive component with states: default, hover, focus, active, disabled, loading, empty, error, success, and reduced-motion where relevant.
- Make accessibility structural: semantic markup, keyboard path, target size, contrast, labels, focus order, captions/alternatives, motion controls, and screen-reader names.
- Treat responsive design as layout behavior, not breakpoint cosmetics: define constraints, grid, content priority, reflow rules, and overflow behavior.
- For XR, design objects, spatial relationships, interaction distance, comfort, onboarding, and safety before polishing panels.
- For AI-generated UI or assets, document sourcing, disclosure, rights risk, user trust, and human review.

## Visual And Diagram Standards
- Use diagrams to clarify process, hierarchy, interaction, object relationships, state transitions, or validation loops.
- Prefer reusable templates in `templates/` for UX process, validation loop, responsive token mapping, component state matrix, and spatial object maps.
- For frontend work, verify rendered output with screenshots at mobile and desktop widths; for XR/WebGL/WebXR, verify the scene is nonblank, framed, and interactive.

## Script Helpers
- Run `scripts/uiux_static_audit.py <file-or-dir>` to scan design plans, UI specs, PR notes, or Markdown docs for missing users, flows, accessibility, responsive behavior, states, validation, handoff, ethics, and XR concerns.
- Run `scripts/theme_catalog.py --root uiux_frontend_skill/theme --list` to list available style ids, or filter with `--category` and `--keyword` before selecting a theme.

## Output Standard
Lead with the design judgment or implementation path. State target surface, users, core task, chosen process depth, style/theme decision, UX laws or heuristics used, component/state coverage, responsive/mobile/XR handling, validation checks, implementation risks, and what remains uncertain.
