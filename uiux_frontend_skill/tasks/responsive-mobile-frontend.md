# Responsive Mobile Frontend

Use this for mobile-first pages, responsive layouts, native-mobile-inspired web UI, or cross-device UI implementation.

## Steps

1. Define users, task flow, device, and input targets.
   - Name target users, primary task, entry path, completion path, recovery path, and likely mobile context.
   - Verify: responsive decisions trace back to a user goal and task flow.
2. Select viewport strategy.
   - Choose responsive, adaptive, or mobile-first responsive strategy; name mobile width, tablet, desktop, touch, pointer, keyboard, screen reader.
   - Verify: at least one narrow and one desktop viewport are named; adaptive layouts have explicit ownership and QA cost.
3. Set content priority.
   - Decide what stays visible, stacks, collapses, truncates, moves, or becomes a separate route.
   - Verify: no critical action disappears into overflow without reason.
4. Define layout rules.
   - Grid, gutters, max width, container queries/breakpoints, aspect ratios, min/max constraints.
   - Verify: dynamic text and media cannot break containers.
5. Design mobile interaction.
   - Touch targets, safe areas, keyboard behavior, one-handed reach, nav pattern, gestures.
   - Verify: hover-only interactions have alternatives.
6. Implement stable dimensions.
   - Boards, cards, buttons, toolbars, counters, media, and fixed-format elements must not shift on hover/loading.
   - Verify: layout shift is minimized.
7. Validate.
   - Screenshot mobile and desktop; test long content, zoom, keyboard, and reduced motion.
   - Verify: record commands or manual checks.

## Common Responsive Decisions

| Pattern | Mobile Behavior |
| --- | --- |
| Data table | Cards, priority columns, or horizontal scroll with sticky labels. |
| Sidebar | Drawer, bottom sheet, or collapsible rail. |
| Toolbar | Icon buttons with tooltips/labels where needed. |
| Multi-column cards | Stack or 2-column grid based on content density. |
| Hero/product view | Preserve first-viewport signal and reveal next section when applicable. |
| Separate adaptive layout | Use only when device-specific behavior is worth the maintenance and QA cost. |
