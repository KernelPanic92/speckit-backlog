---
version: alpha
name: "[PRODUCT_NAME]"
description: "[DESIGN_ONE_LINER]"
colors:
  primary: "[PRIMARY_HEX]"
  on-primary: "[ON_PRIMARY_HEX]"
  secondary: "[SECONDARY_HEX]"
  neutral: "[NEUTRAL_HEX]"
  surface: "[SURFACE_HEX]"
  on-surface: "[ON_SURFACE_HEX]"
  error: "[ERROR_HEX]"
typography:
  headline-lg:
    fontFamily: "[HEADLINE_FONT]"
    fontSize: "[HEADLINE_LG_SIZE]"
    fontWeight: "[HEADLINE_WEIGHT]"
    lineHeight: "[HEADLINE_LINE_HEIGHT]"
  body-md:
    fontFamily: "[BODY_FONT]"
    fontSize: "[BODY_MD_SIZE]"
    fontWeight: "[BODY_WEIGHT]"
    lineHeight: "[BODY_LINE_HEIGHT]"
  label-md:
    fontFamily: "[LABEL_FONT]"
    fontSize: "[LABEL_MD_SIZE]"
    fontWeight: "[LABEL_WEIGHT]"
    lineHeight: "[LABEL_LINE_HEIGHT]"
rounded:
  sm: "[ROUNDED_SM]"
  md: "[ROUNDED_MD]"
  full: 9999px
spacing:
  xs: "[SPACING_XS]"
  sm: "[SPACING_SM]"
  md: "[SPACING_MD]"
  lg: "[SPACING_LG]"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  input-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
---

<!--
  DESIGN TEMPLATE (preset "backlog") — follows the DESIGN.md format by Google Labs
  (https://github.com/google-labs-code/design.md, spec version "alpha").

  Format rules that keep the file valid:
  - The YAML front matter must stay on line 1. `version: alpha` is the version of the DESIGN.md
    FORMAT, required by its tooling: it is not a version of this document (git is the history).
  - Tokens live only in the front matter. Do not add YAML code fences anywhere in the body: every
    YAML code fence is parsed as tokens and a duplicated top-level key is an error.
  - Quote every value that starts with `#`, `[` or `{`. Colors: any CSS color, hex recommended.
    Dimensions: px, em or rem only. fontWeight: a number. lineHeight: a unitless multiplier.
  - Token names: keep the names used in code or in Figma; the ones above are the recommended
    defaults. Always define `primary` (the main action color), aliasing the code's name if it differs. Variants are separate keys (`button-primary-hover`). Groups may nest (`colors.dark.surface`).
  - Component properties: backgroundColor, textColor, typography, rounded, padding, size, height, width.
  - The `##` sections below must keep this order; omit a section rather than writing "N/A".
    Extension sections (after Do's and Don'ts) are allowed.
  - Prose references tokens inline as {colors.primary}. Describe the visual language with a
    specific reference ("a 1970s graduate lecture handout"), not a list of adjectives.
  - Groups intentionally left out go in an `omitted:` list in the front matter, with a reason.
  - Validate with: npx @google/design.md lint .specify/memory/design.md

  Remove this comment block from the generated design.md.
-->

## Overview

[DESIGN_OVERVIEW]
<!-- The visual identity in a few sentences: the specific reference it evokes, the audience, density, light/dark, the feeling the UI must give. -->

## Colors

[COLORS_RATIONALE]
<!-- One bullet per color role: descriptive name, token ({colors.primary}), where it is used and where it must never be used. -->

## Typography

[TYPOGRAPHY_RATIONALE]
<!-- Font families (with licensing), which level is used where, numeric figures, truncation rules. -->

## Layout

[LAYOUT_RATIONALE]
<!-- Grid, max width, gutters, base unit and spacing rhythm, density rules. -->

## Elevation & Depth

[ELEVATION_RATIONALE]
<!-- How hierarchy is expressed (borders, contrast, shadows); which surfaces cast a shadow and its value. -->

## Shapes

[SHAPES_RATIONALE]
<!-- Corner radius per element type, icon/illustration shape language. -->

## Components

[COMPONENTS_RATIONALE]
<!-- The component library or framework (e.g. shadcn/ui, MUI, Material 3), rules per component, states (hover, focus, disabled, loading, empty, error). -->

## Do's and Don'ts

- Do [DESIGN_DO]
- Don't [DESIGN_DONT]

## Responsive Behavior

[RESPONSIVE_RULES]
<!-- Breakpoints and what changes at each one; touch target sizes. -->

## Motion *(optional)*

[MOTION_RULES]
<!-- Durations and easings in prose (the format has no motion tokens); reduced-motion behaviour. -->

## Accessibility

[ACCESSIBILITY_RULES]
<!-- Target (e.g. WCAG 2.2 AA), contrast, focus visibility, keyboard navigation, screen-reader conventions. Must agree with the constitution's Quality Standards. -->

## Sources & Sync

- **Figma**: [FIGMA_FILE_OR_LIBRARY_LINK]
- **Code tokens**: [CODE_TOKEN_PATHS]
- **Source of truth when they disagree**: [DESIGN_SOURCE_OF_TRUTH]
<!-- Where the tokens came from (Figma file/library, CSS variables, Tailwind theme, tokens.json, framework defaults, interview) and which side wins on conflict. Every source is a link whose text names it (the Figma library by its name, e.g. [Checkout UI kit in Figma](https://…); a code file by what it holds), never a bare URL. No dates: git history records when the file changed. -->

## Known Gaps

- [DESIGN_GAP]
<!-- What is not designed yet (dark mode, data visualization, empty states, ...) and provisional tokens waiting for a designer. -->
