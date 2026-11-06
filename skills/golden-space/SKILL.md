---
name: golden-space
description: Compose visual designs using proportion, whitespace, hierarchy, typography, color, and optical balance; create or refine clean, fully editable SVG artwork. Use for posters, diagrams, icons, illustrations, identity studies, and layout reviews that need explicit design decisions or vector source files.
license: MIT
---

# Golden Space

Create intentional compositions and editable vector source. Respect the brief's
content, brand, medium, dimensions, and requested style. Apply the design guidance
to the requested artifact; do not convert an unrelated task into an SVG task.

## Establish the composition

Use the supplied brief. If details are missing, choose reasonable defaults and state
them briefly. Ask only when the missing answer materially changes the result.
For an existing design, preserve its purpose and useful visual language.

Identify the message, the focal element, the reading order, the output size, and the
smallest intended display size. Choose a coherent type, color, spacing, and stroke
system before placing details. For concrete proportional and optical decisions,
read [references/composition.md](references/composition.md).

- Treat golden ratio `phi = (1 + sqrt(5)) / 2`, about `1.618`, as an optional
  relationship. A usable split is approximately `61.8% / 38.2%` **after** margins
  and gutters. Compare it with equal columns, thirds, or a content-led layout.
  Keep it only when the content and optical balance benefit. Never claim a ratio
  proves beauty or add a spiral merely to signal sophistication.
- Give whitespace a job: separate topics, connect related items, protect legibility,
  or create focus. Internal spacing should usually be smaller than spacing between
  groups. Do not enforce a universal percentage of empty canvas.
- Build hierarchy with deliberate differences in size, weight, position, and space.
  Use alignment and repeated intervals to make relationships visible. Adjust
  geometrically aligned circles, diagonals, and lettering when they look off-center.
- Make palette and type serve the subject. Keep body copy legible at delivery size;
  do not shrink text to rescue a crowded composition. Do not invent copy to fill space.
- For information graphics and interfaces, communicate meaning with labels or shape
  as well as color. Check contrast against the actual background. Color thresholds
  and applicability are in the composition reference.

## Produce editable SVG when requested

Read [references/svg-contract.md](references/svg-contract.md) before generating or
editing SVG. The default is a static, self-contained, vector-only editable master.

- Deliver a complete `.svg` file, with an SVG namespace and a correctly sized
  `viewBox`. Never substitute a bitmap wrapped in SVG or a preview screenshot.
- Keep independent objects independently selectable. Use descriptive unique IDs,
  shallow semantic groups, primitive shapes where suitable, and compact paths only
  where curves require them. Do not turn a whole design into a compound path.
- Keep text as live `<text>` / `<tspan>` in the master. Declare a font family and
  fallback, and disclose substitution risk. An optional outlined distribution copy
  is a separate artifact; outlining loses text editability.
- Prefer presentation attributes and simple transforms. Avoid external dependencies,
  scripts, embedded raster content, HTML, animation, filter effects, and CSS-driven
  appearance in the portable master. Use local gradient or clipping definitions only
  when they serve a visible purpose. Compatibility-sensitive features need inspection
  in the intended editor, not an untested compatibility claim.
- Keep IDs, live text, groups, and useful precision when cleaning an existing file.
  Do not silently run destructive optimization or flatten a source master.

Adapt [assets/starter.svg](assets/starter.svg) only when its structure fits the
brief. Its ratio, orientation, colors, and style are examples, not defaults to copy
into every output.

## Check and hand off

Run the bundled structural checker when Python is available:

```sh
python <skill-directory>/scripts/check_svg.py artwork.svg
```

Fix errors. Review each warning; it is a review request, not automatic evidence of a
bad design. `--strict` also fails on warnings; `--json` emits a machine-readable report.
The checker covers a conservative authoring profile, not all valid SVG. It does not
measure visual quality, contrast, clipping, path geometry, or cross-editor fidelity.
Do not call it a security sanitizer.

Render the file at delivery size and a smaller preview. Inspect reading order,
crowding, whitespace, baseline alignment, stroke consistency, overflow, and text
substitution. If an editor is available, open the master and verify that text and
representative shapes can be selected and changed independently. If rendering or
editor verification is unavailable, report that limit without claiming it passed.

Deliver the file (or full SVG source if attachments are unavailable) plus a short
note on composition, fonts, and checks actually performed. Include exact dimensions
and the chosen proportion when relevant. Keep a preview separate from the source.
Do not add a design essay unless requested. Respect an explicit SVG-only response.
