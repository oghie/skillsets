# Design System Token Implementation

Use this when converting `theme/` styles or design specs into CSS, Tailwind, React, React Native, or XR UI tokens/components.

## Steps

1. Pick candidate style.
   - Read `theme/index.yaml`; filter by category, keywords, mood, use cases, and avoid rules.
   - Verify: candidate style id is named.
2. Read exact style file.
   - Use its color, typography, radius, spacing, border, elevation, motion, effects, and component recipes.
   - Verify: selected mode is supported or knowingly off-mode.
3. Create token map.
   - Define semantic tokens before component tokens.
   - Verify: every new variable maps to a source token.
4. Implement components.
   - Start with primitives: button, input, card/container, nav, modal, badge, table/tabs as needed.
   - Verify: variants and states are present.
5. Add accessibility and performance fallbacks.
   - Include contrast checks, focus, reduced motion, lower-cost effects, and readable typography.
   - Verify: fallback is documented for expensive blur/glow/texture.
6. Validate drift.
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
