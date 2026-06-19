# UI Patterns Catalog

Use this when choosing interface patterns, reviewing visual hierarchy, selecting mobile patterns, or checking whether a familiar pattern is being used ethically and accessibly.

Reusable template: `templates/ui-pattern-decision-table.md`.

## Visual Hierarchy Patterns

| Pattern | Use For | Guardrail |
| --- | --- | --- |
| Z-pattern | Simple landing or promotional screens with a clear start, scan path, and call to action. | Works best for sparse content; do not force it onto dense tools. |
| F-pattern | Text-heavy or list-heavy screens where users scan headings and left-aligned anchors. | Put high-value actions and labels where scan behavior expects them. |
| Size and scale | Making primary content or action noticeable first. | Do not enlarge low-value content because of stakeholder preference. |
| Color and contrast | Priority, grouping, status, and affordance. | Color cannot be the only state signal; verify contrast. |
| Whitespace | Grouping, legibility, pacing, and attention. | Dense operational tools need controlled whitespace, not decorative emptiness. |
| Typography | Reading order, meaning, and tone. | Preserve line length, wrapping, and hierarchy at all supported widths. |
| Style and texture | Brand feel and depth. | Texture must not reduce readability, performance, or accessibility. |

## Web Pattern Decisions

| Pattern | Use When | Guardrail |
| --- | --- | --- |
| Primary action button | One task should clearly dominate. | Only one primary action per decision area unless there are truly peer actions. |
| Forgiving format | Users enter phone, dates, addresses, IDs, or numbers in varied formats. | Normalize input and show parsed result; do not silently misinterpret. |
| Steps left | A multi-step flow needs progress and confidence. | Show position, remaining effort, and recovery/back behavior. |
| Breadcrumbs | Users move through hierarchy or deep categories. | Breadcrumbs complement navigation; they do not replace clear IA. |
| Progressive disclosure | Advanced or optional details would overload the current task. | Never hide required information or critical costs. |
| Lazy registration | Users can experience value before account creation. | Defer signup only where product, security, and privacy constraints allow it. |
| Hover controls | Extra controls would clutter pointer-based UI. | Provide touch and keyboard alternatives; do not hide essential controls. |
| Subscription plans | Users compare tiers, prices, and benefits. | Make costs, renewal, cancellation, limits, and recommended tier transparent. |
| Leaderboard | Competition or contribution rank supports motivation. | Avoid shame, privacy leaks, or unfair comparison. |
| Infinite scroll | Discovery feeds benefit from uninterrupted browsing. | Preserve location, performance, footer access, and keyboard/screen-reader usability. |
| Modal window | A focused task must interrupt the current context. | Trap focus, support escape/dismiss rules, return focus, and avoid modal stacking. |
| Card layout | Repeated content items need scannable summaries. | Define action model, metadata, state, density, and responsive behavior. |
| Search autocomplete | Query assistance can reduce effort and errors. | Handle no results, privacy-sensitive suggestions, keyboard selection, and latency. |
| Sticky navigation | Frequent movement or long content needs persistent wayfinding. | Avoid stealing vertical space or covering content on small screens. |

## Mobile Pattern Groups

| Group | Patterns | Guardrail |
| --- | --- | --- |
| Navigation | Hamburger menu, bottom navigation, tab bar. | Primary tasks should not be hidden without reason; labels reduce ambiguity. |
| Content display | Cards, lists, feeds, sections. | Choose based on scan density, media needs, and action model. |
| Input | Forms, large fields, floating action button. | Keep tap targets large, labels visible, and keyboard type correct. |
| Feedback | Progress indicators, toast messages, inline status. | Feedback must be perceivable and not vanish before users can act. |
| Interaction | Swipe gestures, pull-to-refresh, drag, long press. | Gestures need visible alternatives and should not conflict with OS navigation. |
| Onboarding | Walkthroughs, tutorials, coach marks. | Teach only what users need now; allow skip and later recovery. |

## Dark Pattern Review

Reject patterns that manipulate users or hide material facts:

| Pattern | Risk |
| --- | --- |
| Bait and switch | The apparent action does something unexpected. |
| Roach motel | Signup or opt-in is easy, cancellation or exit is hard. |
| Forced continuity | Trial converts to paid without clear reminder and easy cancellation. |
| Hidden costs | Fees appear late in checkout or commitment. |
| Confirmshaming | Decline copy pressures or insults the user. |
| Sneak into basket | Extra items or donations are added without explicit consent. |
| Privacy zuckering | Defaults or flows push users to disclose more data than intended. |
| Misdirection | Visual priority hides important alternatives or terms. |

Ethical pattern use should improve task success, comprehension, control, and trust, not only conversion.
