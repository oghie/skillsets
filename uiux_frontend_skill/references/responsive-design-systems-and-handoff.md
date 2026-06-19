# Responsive Design Systems And Handoff

Use this for Figma-to-code work, tokens, component systems, responsive/adaptive layouts, handoff, collaboration, and frontend consistency.

## Design System Core

| Layer | Content | Frontend Mapping |
| --- | --- | --- |
| Principles | What trade-offs the UI optimizes. | Product constraints and review rules. |
| Tokens | Color, type, spacing, radius, border, elevation, motion. | CSS variables, Tailwind theme, native constants, shader/material params. |
| Components | Buttons, inputs, cards, nav, dialogs, tables, tabs. | Reusable UI components with state props. |
| Patterns | Search, checkout, onboarding, dashboard, settings, auth. | Composed flows and route templates. |
| Guidelines | Do/dont, accessibility, density, content rules. | PR checklist and acceptance criteria. |

## Figma Concepts To Preserve In Code

- Frames become layout containers with explicit sizing constraints.
- Auto Layout maps to flex, grid, stack, or layout primitives.
- Constraints map to anchoring, stretching, fill, hug, min/max, and aspect-ratio behavior.
- Components and variants map to component props and state machines.
- Styles map to tokens, not hardcoded values.
- Prototype links map to route, state, modal, drawer, or transition behavior.
- Comments and design review notes map to implementation tasks or acceptance criteria.

## Responsive Strategy

| Concern | Rule |
| --- | --- |
| Viewports | Define mobile, tablet, desktop, wide, and any embedded/kiosk constraints. |
| Fluid grids | Use grid columns, gutters, margins, and max-width from tokens or product constraints. |
| Adaptive behavior | Decide what changes at breakpoints: hierarchy, density, nav, media, sidebars, tables. |
| Content priority | Decide what stays visible, collapses, truncates, stacks, or moves. |
| Typography | Use stable type steps with responsive line length; avoid viewport-width font scaling. |
| Images/media | Define aspect ratios, object fit, safe cropping, and fallback state. |
| Interaction | Pointer, touch, keyboard, screen reader, and controller/gaze paths may differ. |

## Handoff Requirements

- Provide the selected theme/style id and mode.
- Export or document tokens by semantic name.
- Include component variants and state matrix.
- Include responsive rules, not only static screenshots.
- Include copy and content constraints.
- Include accessibility requirements: labels, roles, focus order, target size, contrast, reduced motion.
- Include performance notes for media, animation, fonts, and heavy visual effects.
- Include QA scenarios: viewport widths, data extremes, empty/error/loading, localization, auth/permission states.

## Developer Collaboration

- Use named versions or changelogs for major design changes.
- Resolve comments or convert them into tasks.
- Avoid ambiguous "match design" handoff; specify measurable differences that matter.
- Keep design tokens and code tokens aligned through a single source of truth.
- In implementation PRs, include screenshots or recordings for changed states and breakpoints.

## Plugin And Tool Use

Plugins can help with contrast checking, content population, motion, handoff, and asset export. Treat plugin output as assistive, not authoritative. Validate generated tokens, assets, and code before shipping.
