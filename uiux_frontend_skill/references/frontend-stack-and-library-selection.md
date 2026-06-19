# Frontend Stack And Library Selection

Use this before choosing or adding UI frameworks, component libraries, styling systems, or design-system infrastructure. Do not default to Tailwind, shadcn, MUI, Ant Design, Mantine, Bulma, Linaria, PostCSS, Radix, or vanilla CSS. Start from the existing repo stack and the product constraints.

## Core Rule

Choose the lowest abstraction that gives the team accessible, maintainable, themeable, and performant UI for the product shape. A stack is a production constraint, not a taste preference.

## First Questions

- What is already installed and used consistently?
- Is this a product app, data-heavy admin tool, marketing surface, editor, mobile app, or XR/webGL interface?
- Does the UI need strong custom art direction from `theme/`, or is a prebuilt design language acceptable?
- How much accessibility behavior must the library provide?
- Does the team need source-owned components or vendor-owned components?
- What are bundle, SSR, performance, theming, and long-term maintenance constraints?
- Is the primary risk speed of delivery, visual differentiation, accessibility correctness, or component complexity?

## Selection Matrix

| Option | Use When | Avoid When | Notes |
| --- | --- | --- | --- |
| Existing app stack | The repo already has a coherent UI system. | It is abandoned, inaccessible, or blocks the requested UX. | Prefer continuity over novelty. |
| Vanilla CSS | You need maximum control, tiny footprint, simple UI, or design-token fidelity. | Large app needs many complex accessible widgets quickly. | Pair with semantic HTML and strong CSS organization. |
| CSS Modules | Component-scoped styling is needed without runtime CSS-in-JS. | Global theming and cross-component token orchestration are weak. | Good default for custom React/Vite/Next components. |
| PostCSS | You need custom CSS pipeline, nesting, autoprefixing, custom media, or token transforms. | You expect it to provide components or interaction behavior. | It is infrastructure, not a UI library. |
| Linaria | You want CSS-in-JS ergonomics with zero runtime CSS extraction. | Build config complexity is not acceptable. | Good for design-token-heavy React apps that care about runtime cost. |
| Tailwind CSS | Utility workflow, fast iteration, tokenized spacing/color, and local component composition fit the team. | Default utility look replaces product-specific design, classes become unreadable, or existing system conflicts. | Keep it as one option, not the default recommendation. |
| Radix UI | You need accessible unstyled primitives for custom design systems. | Team expects finished visual components out of the box. | Strong for dialogs, popovers, tabs, menus, tooltips, and custom themes. |
| shadcn/ui | React app wants editable source-owned components built on Radix and commonly styled with Tailwind. | You need framework-agnostic UI, vendor package updates, or no Tailwind dependency. | Treat generated components as project code that must be governed. |
| MUI | Material-style enterprise/product UI, strong accessibility, theming, data components, and mature React ecosystem fit. | Custom brand must avoid Material feel or bundle/style constraints are strict. | Good for complex forms, dashboards, and admin surfaces. |
| Ant Design | Data-heavy enterprise apps need tables, forms, date pickers, layout, and admin conventions quickly. | Product needs distinctive bespoke UI or minimal bundle surface. | Highly productive but visually opinionated. |
| Mantine UI | React app needs broad components, hooks, forms, notifications, dates, theming, and good DX. | Team wants strict design-language neutrality or minimal dependency surface. | Practical for SaaS/admin/product tools. |
| Bulma CSS | CSS-only responsive layout and simple components are enough. | You need complex accessible JS widgets or modern design-token governance. | Useful for static/server-rendered pages with minimal JS. |
| Headless/custom hybrid | You need custom visuals but reliable behavior. | The team lacks time to implement styling and tests. | Combine Radix/headless behavior with custom CSS/theme tokens. |

## Decision Heuristics

- If the repo already has a mature UI kit, extend it before adding another.
- If the UI is highly bespoke, start with vanilla/CSS Modules/PostCSS/Linaria plus headless primitives.
- If accessibility behavior for complex overlays/menus/tabs matters, prefer Radix or a mature component library over hand-rolled widgets.
- If speed matters more than unique visual identity in enterprise admin, consider Ant Design, MUI, or Mantine.
- If source ownership and editability matter in React, shadcn is attractive, but it becomes your code.
- If token fidelity to `theme/` is critical, avoid libraries that fight radius, spacing, typography, or motion tokens.
- If the project targets mobile or XR, do not assume web component libraries transfer cleanly.
- If Tailwind is selected, configure it from product tokens and avoid default-looking components.

## Theme Integration By Stack

| Stack | Token Strategy |
| --- | --- |
| Vanilla/CSS Modules/PostCSS | Emit `:root` CSS variables and component-level variables. |
| Linaria | Import token constants and compile static styles; keep dynamic variants explicit. |
| Tailwind | Map theme colors, spacing, radius, shadows, fonts, and motion into `theme.extend`. |
| Radix UI | Use primitives for behavior; style parts with CSS variables/classes from the selected theme. |
| shadcn/ui | Rewrite generated component classes/variants to consume selected tokens. |
| MUI | Create `createTheme` palette, typography, spacing, shape, shadows, and component overrides. |
| Ant Design | Map tokens through `ConfigProvider` theme tokens and component overrides. |
| Mantine | Map colors, radius, spacing, font families, shadows, and component default props through `MantineProvider`. |
| Bulma | Override Sass variables or wrap Bulma with project CSS variables and custom components. |

## Anti-Patterns

- Adding a second component library because one component is missing.
- Picking Tailwind only because it is common.
- Picking shadcn and treating generated code as an external package.
- Using MUI/Ant/Mantine while fighting their design language on every component.
- Hand-rolling dialogs, menus, popovers, comboboxes, or date pickers without accessibility tests.
- Mapping only colors while ignoring typography, spacing, radius, elevation, and motion.
- Choosing a library before knowing density, accessibility, theming, SSR, and performance requirements.
