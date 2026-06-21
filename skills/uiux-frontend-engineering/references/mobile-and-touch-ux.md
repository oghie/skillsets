# Mobile And Touch UX

Use this for mobile web, responsive web, native mobile, touch-first UI, or small-screen redesigns.

## Mobile Constraints

- Attention is fragmented.
- Screen width is scarce.
- Input is imprecise compared with pointer and keyboard.
- Network and device performance vary.
- One-handed use changes reach.
- System navigation, keyboard, safe areas, and permissions affect flow.

## Touch Rules

- Make frequent controls large and near the active task.
- Separate adjacent actions enough to avoid accidental taps.
- Increase effective hit area with labels and row targets.
- Keep destructive actions away from common navigation and submit paths.
- Provide pressed feedback immediately.
- Avoid hover-only affordances.

## Mobile Navigation

| Pattern | Use When | Guardrail |
| --- | --- | --- |
| Bottom nav | 3-5 top-level destinations. | Keep labels; avoid hidden meaning icons. |
| Tabs | Peer views inside one area. | Keep content persistent and stateful. |
| Drawer | Secondary navigation or many destinations. | Do not hide the primary task there. |
| Stepper | Linear completion flow. | Show progress and allow recovery. |
| Search-first | Large content catalog. | Make filters and recent queries easy. |

## Forms On Mobile

- Use correct keyboard/input type.
- Keep labels visible.
- Use autofill and defaults carefully.
- Place primary action after inputs.
- Split long forms only when it reduces cognitive load.
- Preserve data on navigation, validation errors, and connection failure.
- Use inline errors with recovery guidance.

## Responsive Content Priority

For small screens, decide:

- What is essential above the fold.
- What collapses into summary or disclosure.
- What becomes a carousel, stack, accordion, or separate route.
- What data table becomes cards, columns, or horizontal scroll.
- Which media can crop, resize, or disappear.

## Testing

- Test at narrow widths, common device widths, and high zoom.
- Test touch, keyboard, screen reader, and reduced motion.
- Test with slow network and low-end device assumptions.
- Test long labels, dynamic data, and validation errors.
