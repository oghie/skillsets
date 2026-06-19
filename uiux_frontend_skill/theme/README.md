# Theme — UI/UX Style Reference Database

A static, structured database of **23 front-end visual styles**, grouped into 3 categories.
Each style is one YAML file holding a complete design-token system (typography, color for
light **and** dark, radius, spacing, borders, elevation, motion, signature textures/effects,
component recipes, and usage guidance).

The point: **never re-derive a style from scratch.** When building a UI in a given aesthetic,
a skill (or a human) reads the relevant style file and maps its tokens straight to CSS
variables, a Tailwind theme, or design-tool styles.

## Folder structure

```
theme/
├─ README.md                 ← you are here
├─ index.yaml                ← generated registry of all 23 styles (id, name, category, mode, summary, keywords)
├─ _schema/
│   └─ style.schema.yaml     ← the CONTRACT: every field, its type, allowed values, and intent
├─ _shared/                  ← optional palette references (no style is required to use them)
│   ├─ palette-carbon.yaml   ← IBM Carbon palette extracted from /PALETTE
│   └─ palettes-curated.yaml ← 5 curated named palettes extracted from /PALETTE/NEW
├─ sharp/                    ← 10 styles — border-radius 0, hard edges, precision
├─ rounded/                  ← 10 styles — high radius / fluid curves, human-centered
└─ hybrid/                   ← 3 styles  — textured skeuomorphic / immersive
```

## The three categories

- **sharp** — `border-radius: 0` (or chamfered). Rigid, precise, uncompromising.
- **rounded** — high radii (16px → pill 999px) and organic curves. Safe, tactile, human.
- **hybrid** — raster-textured, skeuomorphic, immersive (fantasy / diegetic / grimdark).

## How to consume a style (recommended flow)

1. **Pick a category and style.** Browse `index.yaml` (or the category folders). Match by
   `keywords`, `mood`, `use_cases`, and — importantly — `avoid_when`.
2. **Read the style file.** It is the single source of truth. `_schema/style.schema.yaml`
   explains what each field means; you don't need to re-read the schema every time.
3. **Choose the mode.** Check `identity.primary_mode` (`light` | `dark` | `both`) and the
   `color.<mode>.recommended` flag. If a mode has `recommended: false`, it's a deliberate
   off-mode adaptation — use it knowingly, don't treat it as a first-class design.
4. **Map tokens to your platform.** Every value is already CSS-expressible:
   - Emit `color.*`, `radius.*`, `spacing.*`, `elevation.tokens.*`, `motion.*` as CSS
     custom properties (prefix suggested in `implementation_hints.css_variables_prefix`).
   - Or feed them into a Tailwind `theme.extend` (`colors`, `borderRadius`, `boxShadow`,
     `fontFamily`, `transitionTimingFunction`). See `implementation_hints.tailwind_note`.
5. **Build components from the recipes.** `components.*` (button / input / card / container /
   navbar / sidebar / modal / badge / table / tabs) give concrete shape, radius, border,
   padding, shadow, and state values per style.
6. **Load fonts** from `implementation_hints.font_loading` and apply `typography.*`
   (families, scale, weights, line-height, letter-spacing, and `treatments` for special
   text effects like slanted/outlined/engraved).
7. **Respect the guardrails.** Apply `guidelines.do` / `guidelines.dont`,
   `texture_and_effects` (the distinctive layer), and `implementation_hints.accessibility_note`
   and `motion.reduced_motion_note`.

## Conventions (enforced across all files)

- **Values are CSS-ready, never prose.** Colors are `#rrggbb` / `#rrggbbaa` / `rgba()` / `hsl()`.
  Dimensions are `0px` / `16px` / `1rem` / `999px`. Anything needing explanation lives in a
  sibling `note` field, never inside a value.
- **Light and dark are independent**, not mechanical inverses. Several styles are mode-native
  (e.g. Monospace CRT, Aurora, Dark Fantasy Grunge are dark-native; De Stijl, Retro OS,
  Claymorphism are light-native). The off-mode is marked `recommended: false`.
- **Color is per-style and bespoke.** Each style defines its own palette appropriate to its
  aesthetic (Mondrian's pure primaries, Y2K's chromatic pinks, Wabi-Sabi's earth tones).
  The files in `_shared/` (`palette-carbon.yaml`, `palettes-curated.yaml`) are
  **optional** references, not requirements.
- **`special` / signature effects matter.** `texture_and_effects` is what makes a style
  unfakeable (glass backdrop-blur, neumorphic paired shadows, punk torn-paper + skew,
  HUD chamfers + glow). Don't drop it.

## Where slanted / decorative text lives

Special text treatments are under `typography.treatments`:
`font_style`, `transform` (e.g. `skewX(-7deg) rotate(-2deg)` for Punk Zine), `text_transform`,
`text_decoration`, `text_stroke` (outlined text), `text_shadow`, `highlight`, and `per_role`
overrides (e.g. skew the display font but keep body upright/readable).

## Regenerating the index

`index.yaml` is derived from the style files. After adding or editing a style, regenerate it
(and re-run the audits) rather than hand-editing:

```bash
ruby -ryaml -e '
files = Dir.glob("theme/{sharp,rounded,hybrid}/*.yaml").sort
idx = {"meta"=>{"total"=>files.size,"categories"=>Hash.new(0)},"styles"=>[]}
files.each do |f|
  d = YAML.load_file(f); id=d["identity"]
  idx["meta"]["categories"][id["category"]] += 1
  idx["styles"] << {"id"=>id["id"],"name"=>id["name"],"category"=>id["category"],
    "path"=>f,"primary_mode"=>id["primary_mode"],"summary"=>id["summary"],"keywords"=>id["keywords"]}
end
File.write("theme/index.yaml", idx.to_yaml)'
```

## The 23 styles

**Sharp**
1. Neo-Brutalism · 2. Swiss International Typographic Grid · 3. Monospace CRT Terminal ·
4. Avant-Garde High Editorial · 5. Riot Grrrl Punk Zine · 6. Hyper-Minimalist Wireframe ·
7. Retro OS GUI (Win95 / Mac OS 9) · 8. De Stijl Neoplasticism · 9. Japanese Cyber-Metabolism ·
10. Industrial Sci-Fi HUD

**Rounded**
1. Tactile Claymorphism · 2. Perfect Squircle (Super-Ellipse) · 3. Liquid Glassmorphism ·
4. Chunky Toy UI · 5. Organic Wabi-Sabi · 6. Aurora Holographic · 7. Soft Neumorphism ·
8. Biophilic Fluidity · 9. Y2K Bubblegum Pop · 10. Mid-Century Modern Pill

**Hybrid**
1. High Fantasy Medieval Skeuomorphism · 2. Diegetic Web Design · 3. Dark Fantasy Grunge
