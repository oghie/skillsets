# Information Architecture And Sitemaps

Use this when designing navigation, taxonomy, labels, search, categorization, page hierarchy, content inventory, sitemaps, findability tests, or IA handoff.

Reusable template: `templates/information-architecture-map.mmd`.

## IA Frame

Information architecture sits at the intersection of:

| Lens | Questions |
| --- | --- |
| Users | Who needs to find or act on this content? What vocabulary and mental models do they bring? |
| Content | What exists, what is missing, what changes over time, and what metadata matters? |
| Context | What business goals, technical constraints, compliance rules, devices, and workflows shape the structure? |

## IA Principles

| Principle | Design Rule |
| --- | --- |
| Objects | Treat content as living objects with properties, lifecycle, states, metadata, relationships, and actions. |
| Choices | Present a manageable set of options for the current task; reduce irrelevant branches. |
| Disclosure | Reveal enough to help users predict what comes next, then disclose more as they go deeper. |
| Exemplars | Use examples or representative items to make categories understandable. |
| Front doors | Assume users can land on any page; each page needs context, orientation, and onward navigation. |
| Multiple classification | Support different routes to the same content through category, search, filters, tags, or audience paths. |
| Focused navigation | Keep menus relevant to the task or category; do not mix marketing, utility, and taxonomy without intent. |
| Growth | Design structures that can absorb new content without a full redesign. |

## IA Systems

| System | Purpose | Checks |
| --- | --- | --- |
| Organization | Groups content into categories and relationships. | Categories match user mental models, not internal org charts only. |
| Labeling | Names pages, actions, filters, and groups. | Labels use user vocabulary and are distinguishable. |
| Navigation | Provides global, local, contextual, hidden, main, and secondary movement paths. | Current location, next actions, backtracking, and recovery are visible. |
| Search | Lets users locate items by terms, metadata, filters, and ranking. | Search handles synonyms, empty states, no results, and refinement. |

## IA Process

1. Understand users and define goals.
2. Inventory content and planned content.
3. Create categories and labels from research, not only stakeholder preference.
4. Build hierarchy, navigation, and sitemap.
5. Validate with card sorting, tree testing, usability tests, analytics, and search logs.
6. Document the IA as a sitemap, wireframe, flow, taxonomy, or navigation spec.
7. Keep IA flexible as content and user needs change.

## Card Sorting And Tree Testing

| Method | Use When | Watch For |
| --- | --- | --- |
| Open card sorting | Discover how users naturally group content. | Participants may create overlapping or ambiguous categories. |
| Closed card sorting | Test whether an existing category set makes sense. | Forced categories can hide new mental models. |
| Tree testing | Test whether users can find items in a text-only hierarchy. | It validates findability, not visual design or content quality. |

## Sitemap Decisions

| Sitemap Type | Use For | Guardrail |
| --- | --- | --- |
| HTML sitemap | Human-readable page discovery and fallback navigation. | Keep labels useful and avoid dumping every URL without grouping. |
| XML sitemap | Search engine discovery and indexing. | Validate syntax, update frequency, last modified dates, and canonical URLs. |
| Mobile sitemap | Mobile-specific discovery where mobile URLs or content differ. | Prefer responsive URLs unless the platform really has separate mobile routes. |
| Image/video/news sitemap | Media or news indexing. | Include only indexable, intentional assets and required metadata. |

## Handoff Output

- Taxonomy and labels.
- Navigation model and current-location rules.
- Search and filter behavior.
- Sitemap or hierarchy diagram.
- Entry points for non-homepage landing.
- Content growth assumptions.
- IA validation method and unresolved findability risks.
