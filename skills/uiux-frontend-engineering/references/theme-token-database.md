# Theme Token Database

Use this to consume the existing `theme/` directory. Do not edit `theme/` unless the user explicitly asks for theme authoring.

## Selection Flow

1. Read `theme/index.yaml` to identify candidate styles.
2. Match product context against `summary`, `keywords`, `mood`, `use_cases`, and `avoid_when`.
3. Read the chosen style file.
4. Choose light or dark mode based on `identity.primary_mode` and `color.<mode>.recommended`.
5. Map tokens into platform variables and components.
6. Preserve the style's signature texture/effects only when performance and accessibility remain acceptable.

## Categories

| Category | Use For | Guardrail |
| --- | --- | --- |
| Sharp | Precision, editorial, tools, dashboards, technical systems, brutalist or grid-heavy UIs. | Can feel harsh; test readability and density. |
| Rounded | Friendly, tactile, consumer, education, onboarding, wellness, approachable apps. | Can reduce density; avoid if data work needs compact scanning. |
| Hybrid | Immersive, diegetic, fantasy, narrative, game-like, XR-like interfaces. | High texture cost; avoid for austere enterprise unless intent justifies it. |

## Token Mapping

| Theme Field | CSS / Vanilla / Modules / PostCSS / Linaria | Utility CSS / Tailwind | Component Libraries | Native / XR |
| --- | --- | --- | --- | --- |
| `color.*` | CSS variables or compiled constants | `theme.extend.colors` | provider theme palette/tokens | theme constants or material colors |
| `typography.*` | font-family, font-size, line-height | fontFamily/fontSize | typography theme override | text styles or distance-aware text |
| `spacing.*` | margin, padding, gap variables | spacing scale | spacing token/provider override | spacing constants or world units |
| `radius.*` | border-radius variables | borderRadius scale | shape/radius theme override | borderRadius or panel mesh shape |
| `border.*` | border variables/classes | borderWidth/color utilities | component style overrides | border styles, outlines, strokes |
| `elevation.*` | box-shadow/filter variables | boxShadow scale | shadow/elevation overrides | shadow, light, depth, occlusion |
| `motion.*` | transition/animation variables | transition tokens | motion/default prop overrides | animation config or tween timing |
| `texture_and_effects.*` | overlays/filter/background | custom utilities/plugins | wrapper components or slots | textures/post-process/material layers |

## Implementation Rules

- Emit semantic variables first, then component variables.
- Do not hardcode one-off colors outside the selected style unless a state is missing and documented.
- Keep typography readable even when the style has decorative display treatment.
- Treat `avoid_when` as a real constraint.
- For dark/light support, do not mechanically invert; use the mode values defined by the style.
- Check `implementation_hints.accessibility_note` and `motion.reduced_motion_note`.
- If a style uses expensive blur, glow, noise, or texture, define a lower-cost fallback.
- For Radix/headless UI, map tokens to styled parts and states.
- For shadcn/ui, rewrite generated variants/classes to consume selected tokens.
- For MUI, Ant Design, and Mantine, map tokens through their theme providers and component overrides.
- For Bulma, override Sass variables or wrap with project CSS variables; do not expect complex JS behavior.

## Style Selection Rubric

Score 0-2:

| Criterion | Question |
| --- | --- |
| Product fit | Does mood/use case match user task and brand? |
| Density fit | Can the style support information density? |
| Accessibility | Can contrast, motion, text, and target size pass? |
| Performance | Can effects run on target devices? |
| Maintainability | Can tokens map cleanly to the stack? |
| Differentiation | Does the style add useful identity without harming familiarity? |

Choose the highest safe score, not the loudest style.
