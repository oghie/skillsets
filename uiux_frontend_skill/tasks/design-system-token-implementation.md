# Design System Token Implementation

Use this when converting `theme/` styles or design specs into vanilla CSS, CSS Modules, PostCSS, Linaria, Tailwind, Radix UI, shadcn/ui, MUI, Ant Design, Mantine UI, Bulma, React, React Native, or XR UI tokens/components.

## Steps

1. Pick candidate style.
   - Read `theme/index.yaml`; filter by category, keywords, mood, use cases, and avoid rules.
   - Verify: candidate style id is named.
2. Read exact style file.
   - Use its color, typography, radius, spacing, border, elevation, motion, effects, and component recipes.
   - Verify: selected mode is supported or knowingly off-mode.
3. Choose implementation stack.
   - Use existing project stack first. If choosing a new library, read `references/frontend-stack-and-library-selection.md`.
   - Verify: stack choice names trade-offs for accessibility, theming, bundle, SSR, delivery speed, maintainability, and product density.
4. Create token map.
   - Define semantic tokens before component tokens.
   - Verify: every new variable maps to a source token.
5. Implement components.
   - Start with primitives: button, input, card/container, nav, modal, badge, table/tabs as needed.
   - Verify: variants and states are present.
6. Add accessibility and performance fallbacks.
   - Include contrast checks, focus, reduced motion, lower-cost effects, and readable typography.
   - Verify: fallback is documented for expensive blur/glow/texture.
7. Validate drift.
   - Compare code variables/components against source style.
   - Verify: run `scripts/theme_catalog.py` and relevant tests/lints.

## Token Naming Guidance

Prefer names like:

```text
--ui-bg
--ui-surface
--ui-text
--ui-accent
--ui-border
--ui-radius-md
--ui-space-4
--ui-shadow-md
--ui-duration-base
```

Keep raw palette names private unless the app already has a naming system.

## Stack Notes

- Tailwind is supported, but do not use it as the default answer.
- Radix and headless primitives are strong when the theme needs custom visuals with accessible behavior.
- shadcn is source-owned project code; govern variants, tokens, and accessibility after generation.
- MUI, Ant Design, and Mantine are productive for complex product/admin surfaces but can impose visual language.
- Vanilla CSS, CSS Modules, PostCSS, and Linaria are valid when bespoke art direction, small bundle size, or token fidelity matters.
- Bulma is acceptable for CSS-only/simple server-rendered interfaces, but it does not solve complex JS interaction behavior.
