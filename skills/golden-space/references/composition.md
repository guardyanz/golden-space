# Composition decisions

These are working heuristics. Content, medium, and the user's brief decide when to
override them. Ratios and spacing scales are tools for consistency, not aesthetic laws.

## Proportion without numerology

The golden ratio solves `phi = 1 + 1/phi`; `phi = 1.6180339887...`.
For two regions sharing available span `S`, choose `large = S / phi` and
`small = S - large`. Subtract outer margins and the intervening gutter first.

Example: a 1200-unit canvas, two 64-unit margins, and a 32-unit gutter leave
`S = 1040`. The regions are about `642.76` and `397.24` units. Do not split the
full 1200 and then add padding; that exceeds the available area. Round to useful
coordinates after the overall layout is resolved.

Compare candidates at their actual output size:

| Relationship | Useful when | Reconsider when |
| --- | --- | --- |
| Equal halves | Two subjects have equal importance | The message needs a clear lead |
| Thirds | A focal point needs offset and breathing room | It causes awkward text wrapping |
| 61.8 / 38.2 | One region should clearly lead a second | The small region cannot fit its content |
| Content-led | Text, data, or a fixed asset dictates the shape | Ad hoc dimensions destroy consistency |

Do not imply historical provenance, natural universality, conversion uplift, or
scientific proof of preference from the presence of phi. Do not force each heading,
radius, gutter, and icon onto a golden scale.

## Whitespace and grouping

Distinguish outer margins, between-section gaps, within-group gaps, and text line
spacing. Choose a small spacing family; `8, 16, 24, 32, 48, 64` is one starting
point for a large illustration or poster, not a mandatory pixel scale.

Use proximity to express belonging. As a starting relationship, a label-to-value
gap can be one interval and a gap between separate groups two or three intervals.
Then assess actual glyph shapes, density, and object silhouettes. Equal bounding-box
gaps can look unequal beside a diagonal or a circle.

At thumbnail size, check whether the focal element is visible and groups remain
distinct. At intended size, check line lengths, comfortable text spacing, and edge
clearance. Enlarge the canvas, simplify the content, or reorganize groups before
reducing all text. Dense technical diagrams can use less whitespace than an editorial
cover. The canvas need not be literally white.

## Hierarchy, rhythm, and optical balance

Choose a primary message and make its entry point clear. Use a restrained set of
type roles, align edges or baselines intentionally, and repeat a few dimensions.
For type scaling, modest steps such as 1.2 or 1.25 can be more practical than 1.618.
Measure text using the actual font or inspect a render; character count is not a
reliable width measurement. SVG text does not automatically wrap like HTML.

Balance visible weight: area, darkness, saturation, complexity, and position all
matter. A small dark form can counter a larger pale one. Make optical corrections
to center placement, rounded shape overshoot, and letter spacing after the geometry
is settled. Avoid tangent collisions and almost-aligned edges that look accidental.
Keep line caps, joins, corner treatments, and stroke families consistent unless the
contrast is deliberate. Confirm that thin details survive the smallest use size.

Texture, gradients, illustrations, and decoration should have a compositional role.
Do not enforce a particular palette, editorial style, minimalism, or ornament count.

## Color and readable information

Assign colors by role: background, primary content, secondary content, and accent.
Check actual foreground/background pairs, including transparency and gradients.
Use color together with text, symbols, patterns, or positions for essential meaning.

For web information subject to WCAG 2.2 AA, normal text needs at least `4.5:1`;
large text needs `3:1`. Large means at least 18 pt, or 14 pt bold, at the rendered
size (roughly 24 CSS px or 18.67 CSS px). A large SVG font-size in a scaled-down
image does not automatically qualify. Do not round a failing ratio upward.
Meaningful graphical parts and UI cues generally need `3:1` against adjacent colors,
subject to the criterion's exceptions. Decorative shapes do not all need that ratio.
These are specific readability checks, not a complete accessibility certification
or a general requirement for every artwork or logo.

Sources: [W3C text contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
and [W3C non-text contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

## Reviewing a composition

Identify the most consequential visible problem and revise it first. Explain a
change through its effect: for example, increasing a group gap makes the reading
order clearer. Do not score a design by how many formulas it obeys. Confirm the
result visually after revising; a lint pass cannot assess composition.
