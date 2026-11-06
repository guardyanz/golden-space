# Portable editable SVG master

This authoring profile favors simple editing and predictable exchange. It is a
project convention, not the full SVG specification. SVG features outside it may be
valid and useful in a specialized deliverable. If the brief needs one, describe the
tradeoff and provide a portable master or companion version when appropriate.

## Document and object structure

- Use UTF-8 XML, `xmlns="http://www.w3.org/2000/svg"`, a finite four-number
  `viewBox` with positive width and height, and explicit output dimensions.
  Avoid a DOCTYPE or processing instructions. Preserve a transparent background
  when requested; otherwise a separately selectable background is acceptable.
- Use `<title>` and `<desc>` for the informative artwork and connect their IDs
  through `aria-labelledby`. `role="img"` is suitable for an informative standalone
  image. Decorative embedding needs context-appropriate accessibility handling
  in the host document instead. Describe the result without making visual claims
  that have not been verified.
- Name meaningful groups and visible objects with unique stable IDs such as
  `headline`, `orbit-ring`, and `caption-copy`. IDs are portable structure; an
  editor's proprietary layer labels are optional metadata, not a requirement.
- Group by what a person will edit: background, copy, illustration, annotations.
  Start with shallow groups; do not nest a group around every object.
- Prefer `rect`, `circle`, `ellipse`, `line`, `polyline`, and `polygon` for their
  corresponding shapes. Use paths for custom silhouettes and curves. Keep unrelated
  parts separate. Avoid path tracing noise, redundant points, and excessive decimals.
- Allow normal geometric transforms; avoid long transform chains that make
  individual objects difficult to reason about. Keep stroke behavior intentional.

## Appearance and references

Use presentation attributes such as `fill`, `stroke`, `stroke-width`,
`font-family`, and `font-size`, including inheritance on groups. This profile
excludes inline `style`, `<style>`, CSS classes used for appearance, CSS variables,
and stylesheet imports so that appearance stays inspectable at the object level.

Keep gradients and clipping paths in local `<defs>` with IDs. Reference them with
`url(#id)` and verify that the target exists and has the right type. Shared gradients
are convenient but changing one may recolor multiple objects; disclose that when
it matters. Avoid masks or clipping used only to hide poorly constructed geometry.

Avoid `<use>` / `<symbol>` for the master when each instance must be independently
editable; the checker warns on these. A local instance is valid vector content,
but some editors keep it linked until expanded. Do not claim expansion was tested
unless it was. References to a URL, file, data URI, or external font are excluded.

## Text and fonts

Use real `<text>` and `<tspan>` with deliberate coordinates and line breaks. Keep
the wording intact. Declare a font family plus a practical fallback. A fallback
does not guarantee equal metrics or appearance. System fonts can vary by machine.
Avoid `textLength` used to squeeze paragraphs into a fixed box.

If typography is essential, identify the exact font and license, and verify that
it is available in the target editor. Do not download or bundle fonts without a
need and an appropriate license. Provide an optional outlined copy only when
requested or needed for distribution. Keep the live-text master alongside it.

## Excluded from the default master

No raster `<image>` / `<feImage>`, script, event handler, HTML `<foreignObject>`,
animation, external link or resource, or filter effect. Effects such as blur and
drop shadow may be rasterized during exchange even when their input is vector.
Build simple depth with editable shapes when useful. Do not silently approximate
a required visual effect; state the compromise or produce a separate effect version.

Do not flatten groups, outline text, merge independent paths, strip useful IDs,
or collapse references as a generic cleanup step. File-size reduction is secondary
to preserving an editable master. Keep a minified delivery copy separate if needed.

## Verification and limits

The checker reports XML/profile errors, missing or duplicate IDs, invalid viewBox,
missing title/description links, broken local references, excluded content, and
review warnings for instances, masks, text-on-path, missing font declarations,
deep grouping, and unusually long paths. It uses only Python's standard library.

It does **not** parse path geometry, calculate bounds or contrast, prove that
anything is visible, detect every outlined letter, validate every SVG attribute,
enforce design quality, or certify a file safe to embed. Treat an SVG from an
untrusted source according to the host application's security policy.

Render first, then test edits in the target editor when available. Check for clipped
strokes and text, unexpected font fallback, unsupported features, and independently
selectable shapes. Browser rendering alone does not prove Illustrator, Inkscape,
Figma, or CorelDRAW import fidelity. Report which checks actually ran.

Technical basis: [W3C SVG specification](https://www.w3.org/TR/SVG2/).
