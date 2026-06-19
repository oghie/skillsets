# Visual Interface Composition

Use this when designing screens, components, layout, visual hierarchy, forms, navigation, cards, icons, illustrations, or motion.

## Composition Principles

- Gestalt: use proximity, similarity, continuity, closure, common region, and figure-ground to make structure self-evident.
- Hierarchy: order content by task importance, not by stakeholder politics.
- Whitespace: reserve space to group, separate, and pace content; do not use it as decorative emptiness in dense tools.
- Alignment: use a grid and consistent edge relationships so scanning has rhythm.
- Contrast: distinguish priority, state, and grouping; verify text and controls remain accessible.
- Repetition: use repeated component patterns to teach the interface.
- Balance: choose symmetry for stability and asymmetry for energy only when it serves intent.

## UI Element Taxonomy

| Element | Required Decisions |
| --- | --- |
| Button | Variant, icon use, label, target size, hierarchy, loading, disabled, focus, destructive state. |
| Input | Label, helper text, validation timing, error copy, placeholder role, autofill, keyboard type. |
| Navigation | Primary path, secondary path, current location, overflow, mobile collapse, keyboard access. |
| Card | Purpose, density, action model, media ratio, metadata, empty/loading/error states. |
| Table | Columns, sorting, filtering, bulk action, row state, empty state, responsive fallback. |
| Modal | Trigger, focus trap, dismiss behavior, destructive confirmation, return focus. |
| Tooltip | Short explanation only; never hide required information exclusively in tooltip. |
| Notification | Severity, persistence, action, undo, accessibility announcement. |
| Icon | Meaning, label, hit area, visual weight, fallback text. |

## Component State Matrix

Every interactive component should define:

| State | Purpose |
| --- | --- |
| Default | Normal resting appearance. |
| Hover | Pointer affordance without layout shift. |
| Focus | Keyboard and assistive navigation signal. |
| Active/Pressed | Immediate response to input. |
| Selected | Persistent choice or current item. |
| Disabled | Unavailable action plus reason when needed. |
| Loading | Work in progress; prevent duplicate action. |
| Error | Clear problem and recovery. |
| Success | Confirmation and next step. |
| Empty | Valid lack of data with useful action. |

## Forms

- Label every field; placeholders are examples, not labels.
- Prefer one clear column for complex forms.
- Validate at the moment users can recover effectively.
- Show constraints before submission when they affect input.
- Group related fields and preserve entered data after errors.
- Provide examples for unusual formats and use proper input types.
- Make checkbox/radio labels clickable to expand target area.

## Navigation

- Use familiar structures first: top nav, side nav, tabs, breadcrumbs, stepper, bottom nav on mobile when appropriate.
- Keep navigation labels in user vocabulary.
- Show current location and available next actions.
- Avoid hiding primary tasks behind ambiguous icons.
- For mobile, design menu behavior, thumb reach, and back behavior explicitly.

## Typography

- Establish scale before decoration: display, h1, h2, h3, body, small, caption.
- Set line length, line height, and responsive wrapping deliberately.
- Use weight and size to show hierarchy; reserve all-caps and decorative treatments for short labels.
- Never let text overflow buttons, cards, tabs, or fixed UI.

## Color And Motion

- Color should encode hierarchy, state, and brand mood, not carry meaning alone.
- Pair status color with text/icon shape.
- Use motion for continuity, feedback, orientation, and delight after usability is solid.
- Respect reduced-motion preferences.
- Avoid motion that delays task completion or hides state changes.

## Visual Assets

- Use real product, state, data, place, person, gameplay, or object imagery when the user must inspect the subject.
- Avoid generic atmospheric imagery when specificity matters.
- For icons, use a consistent library before drawing one-off symbols.
- For XR or game-like interfaces, visual assets must fit the spatial/object model, not just screen aesthetics.
