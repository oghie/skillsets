# Responsive Mobile Frontend

Use this for mobile-first pages, responsive layouts, native-mobile-inspired web UI, or cross-device UI implementation.

## Steps

1. Define device and input targets.
   - Mobile width, tablet, desktop, touch, pointer, keyboard, screen reader.
   - Verify: at least one narrow and one desktop viewport are named.
2. Set content priority.
   - Decide what stays visible, stacks, collapses, truncates, moves, or becomes a separate route.
   - Verify: no critical action disappears into overflow without reason.
3. Define layout rules.
   - Grid, gutters, max width, container queries/breakpoints, aspect ratios, min/max constraints.
   - Verify: dynamic text and media cannot break containers.
4. Design mobile interaction.
   - Touch targets, safe areas, keyboard behavior, one-handed reach, nav pattern, gestures.
   - Verify: hover-only interactions have alternatives.
5. Implement stable dimensions.
   - Boards, cards, buttons, toolbars, counters, media, and fixed-format elements must not shift on hover/loading.
   - Verify: layout shift is minimized.
6. Validate.
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
