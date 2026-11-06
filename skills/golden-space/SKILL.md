---
name: golden-space
description: Create and refine posters, images, social graphics, illustrations, diagrams, and icons with deliberate whitespace, proportion, golden ratio where useful, hierarchy, typography, and color. Apply these constraints during generation, review the result, and deliver actual SVG or raster files. Supports direct clean editable SVG creation and PNG, JPEG, or WebP output according to the brief.
license: MIT
---

# Golden Space

Create the requested visual artifact with intentional composition and editable source
where suitable. Respect the brief's content, brand, medium, dimensions, and style.
When asked to make a poster or image, produce the artifact rather than stopping at
design advice, a plan, or an image-generation prompt.

## Choose and deliver the artifact

- Deliver the format the user asks for: editable SVG, or raster such as PNG, JPEG,
  or WebP. These are alternative final outputs; neither requires delivering both.
  When no format is specified, choose SVG for vector-suitable artwork and raster
  for photographic or painterly work. State the choice briefly when useful.
- For vector-suitable posters, social graphics, flat illustrations, diagrams, and
  icons, create and save a complete `.svg` file by default. The user need not ask
  for SVG separately. If rendering is available, also provide a PNG preview without
  replacing the editable master. An explicit request for another format takes priority.
- A raster poster or flat illustration can be composed as an intermediate SVG and
  exported with an available renderer. Deliver the requested raster file; include
  its SVG source only if requested or useful to the handoff. Never change a file's
  extension as a substitute for rendering or encoding the requested format.
- For photography, photorealism, or painterly imagery, apply the same composition
  constraints through the available image-generation or editing tool. Read
  [references/image-direction.md](references/image-direction.md) for that workflow.
  Deliver the requested raster image. If SVG is also requested, create a separate
  vector interpretation when feasible and identify any loss of detail; do not
  silently replace the requested visual style.
- A raster image placed inside an SVG is a hybrid composition, not fully editable
  vector artwork. Offer it only when relevant, clearly label the embedded raster,
  and retain live text and separate vector overlays. Do not present it as the
  portable vector master described below.
- Use the user's output directory and a filename matching the chosen format, such
  as `poster.svg` or `poster.png`.
  Write the file when file tools are available and link it in the handoff. If file
  writing is unavailable, return complete SVG source. A code fence is a fallback,
  not a substitute for a file that the available tools can create.

## Establish the composition

Use the supplied brief. If details are missing, choose reasonable defaults and state
them briefly. Ask only when the missing answer materially changes the result.
For an existing design, preserve its purpose and useful visual language.

Identify the message, the focal element, the reading order, the output size, and the
smallest intended display size. Before generating, form a compact internal design
specification: focal placement, proportion or grid, safe margins, spacing relationships,
type roles, palette, and any protected copy area. Use it to construct the SVG or to
direct the image tool; naming principles in a final explanation is insufficient.
For concrete proportional and optical decisions,
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

## Build the editable SVG master

Read [references/svg-contract.md](references/svg-contract.md) before generating or
editing SVG, including an intermediate source used for raster export. The default
is a static, self-contained, vector-only editable master. This section applies to
SVG authoring; raster output does not need to masquerade as editable vector content.

- Author a complete SVG document, with an SVG namespace and a correctly sized
  `viewBox`. For an SVG final deliverable, save and link the `.svg` file. Never
  substitute a bitmap wrapped in SVG or a preview screenshot.
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

For a final or intermediate SVG, run the bundled structural checker when Python is
available:

```sh
python <skill-directory>/scripts/check_svg.py artwork.svg
```

Fix errors. Review each warning; it is a review request, not automatic evidence of a
bad design. `--strict` also fails on warnings; `--json` emits a machine-readable report.
The checker covers a conservative authoring profile, not all valid SVG. It does not
measure visual quality, contrast, clipping, path geometry, or cross-editor fidelity.
Do not call it a security sanitizer.

For raster delivery, verify the actual encoded format, pixel dimensions, aspect
ratio, and requested background or transparency. PNG or suitable WebP can preserve
alpha; JPEG needs a deliberate opaque background. Inspect compression and edge
quality at delivery size. Do not send a PNG or JPEG through the SVG checker.

Before handoff, review the actual visual against the design specification:

- Is the intended subject or message the entry point, with a clear reading order?
- Do safe margins protect essential content, with purposeful space around the focus?
- Are within-group and between-group gaps distinct, without accidental tangencies?
- Does the chosen proportion fit the content without shrinking or crowding it?
- Are text, color relationships, baselines, and stroke weights legible and coherent
  at the intended size, with no accidental clipping or invented lettering?

Render SVG at delivery size and a smaller preview when possible. Inspect the output
and correct observed problems before delivery; do not merely list the rules followed.
Apply the same visual review to raster output. Formulas and structural lint cannot
guarantee aesthetic quality. If an editor is available, open the SVG master and
verify that text and representative shapes can be selected and changed independently.
If rendering or editor verification is unavailable, report that limit without
claiming it passed.

Deliver the actual file in the chosen format (or full SVG source if file writing
is unavailable for an SVG task) plus a short note on composition, fonts, and checks
actually performed. Include exact dimensions
and the chosen proportion when relevant. Keep a preview separate from the source.
Do not add a design essay unless requested. Respect SVG-only or raster-only handoffs.
