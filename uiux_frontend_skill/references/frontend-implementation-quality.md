# Frontend Implementation Quality

Use this when converting UI/UX decisions into production frontend code.

## Implementation Order

1. Define user task, route/screen, data contract, and states.
2. Select theme/style tokens or existing design system tokens.
3. Build semantic structure and accessible interaction first.
4. Implement layout constraints and responsive behavior.
5. Add visual styling from tokens.
6. Add motion only where it clarifies feedback, continuity, or orientation.
7. Verify with automated checks, screenshots, keyboard path, and data extremes.

## Component Contract

Every reusable component should state:

- Purpose and non-purpose.
- Props and controlled/uncontrolled state.
- Visual variants.
- Interaction states.
- Accessibility role/name/description.
- Keyboard behavior.
- Responsive behavior.
- Data limits: long labels, missing media, many items, zero items.
- Test or story coverage.

## Accessibility Baseline

- Use semantic elements where possible.
- Keep focus visible and ordered.
- Make keyboard access complete.
- Provide labels for controls and icons.
- Ensure status changes are announced when needed.
- Meet contrast requirements for text, icons, focus, borders, and disabled alternatives.
- Do not rely on color alone.
- Support reduced motion.
- Ensure target sizes fit input method.

## Performance Baseline

- Avoid layout shift from images, fonts, dynamic content, and late-loading UI.
- Define stable dimensions for cards, boards, grids, media, and toolbars.
- Lazy-load heavy media below the fold.
- Keep animations GPU-friendly and short.
- Avoid excessive backdrop filters, shadows, gradients, and blur on low-power mobile.
- Measure user-visible latency and response feedback.

## Visual QA

Check:

- Mobile, tablet, desktop, and wide desktop.
- Light/dark mode when supported.
- Loading, empty, error, success, and permission states.
- Long words, long labels, localization, and dynamic data.
- Keyboard focus path.
- Screen reader labels for interactive elements.
- Reduced-motion mode.
- High zoom and narrow viewport.
- Production data density.

## Frontend Mapping

| Design Decision | Web Mapping | Mobile Mapping | XR Mapping |
| --- | --- | --- | --- |
| Token color | CSS variables, utility config, or library theme provider | Theme constants | Material/shader colors |
| Layout grid | CSS grid/flex/container queries | Stack/grid/layout primitives | Spatial anchors and panels |
| Component states | Props, classes, state machine | Component props/state | Object interaction states |
| Motion | CSS/JS animation | Native animation primitives | Object transition, gaze/hand feedback |
| Navigation | Routes, tabs, drawers | Navigation stack/tabs | Spatial menus, wrist/menu panels, portals |
| Accessibility | ARIA/semantics/keyboard | Native accessibility APIs | Comfort, captions, alternatives, safety zones |

## Anti-Patterns

- Styling before task flow is clear.
- Treating Figma screenshots as complete specifications.
- Hardcoding tokens instead of using the selected style system.
- Choosing Tailwind, shadcn, Radix, MUI, Ant Design, Mantine, Bulma, Linaria, PostCSS, or vanilla CSS without naming why that abstraction fits the product and repo.
- Building only the happy path.
- Hiding required labels in placeholders or tooltips.
- Shipping responsive breakpoints without testing real content.
- Adding novelty that breaks familiar expectations without usability evidence.
