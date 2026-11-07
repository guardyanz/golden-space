# Verification record

Recorded on 2026-11-07. The authoring agent manually exercised the updated workflow
using the supplied briefs, local file tools, Chromium rendering, SVG DOM inspection,
and Pillow decoding. This is a development self-check, not an independent benchmark
of automatic skill selection or compliance across different AI products.

## Completed checks

| Check | Artifact or method | Observed result |
| --- | --- | --- |
| Installable skill structure | Skill Creator's `quick_validate.py` | Valid name, description, frontmatter, and completed instructions |
| Checker regression coverage | `python -m unittest discover -s tests -v` | 21 tests passed, including strict mode, JSON reports, broken references, external assets, live text, and all distributed SVG examples |
| Actual vector poster | [plant-swap.svg](../examples/plant-swap.svg), following the plant-swap brief | Complete 1080 x 1350 SVG, with three live-text objects, independent plant parts, named groups, and no raster or HTML elements |
| SVG structural profile | Bundled checker in strict mode | No errors or warnings for the plant-swap poster |
| Independent source edits | Clone the SVG DOM; change the event time and one leaf's fill | Both changes affected only their targets; original content and object count were preserved |
| Text bounds | Chromium `getBBox()` on all three text objects | All text bounds stayed within the 1080 x 1350 viewBox |
| Actual raster poster | [plant-swap.png](../examples/plant-swap.png), exported from the SVG with Chromium | Pillow decoded a genuine RGB PNG at exactly 1080 x 1350; not renamed XML |
| Transparent raster output | [balanced-mark.png](../examples/balanced-mark.png) | Genuine 256 x 256 RGBA PNG, nonempty artwork, alpha values spanning 0 to 255, and a transparent corner |
| Visual review | Poster at 1080 x 1350 and a fitted 360 x 450 preview | Checked title prominence, content grouping, safe margins, copy visibility, whitespace, and unclipped plant geometry |
| Built-in imagegen integration | [Promo comparison](../examples/promo-comparison/README.md) | Two actual artwork-generation calls, matching PNG/hybrid-SVG posts, identical live-text overlays, source artwork and prompts retained; separate fully vector interpretations also pass the strict SVG profile |

The plant-swap composition uses a content-led arrangement: prominent copy at the
upper-left and a supporting plant lower-right. A forced ratio split was not needed.
The type stack is Arial, Helvetica, sans-serif; another system may substitute a
font with different metrics. The vector file remains the live-text source; the
PNG is a flattened raster rendition.

## Scope of the evidence

- Independent SVG edits were checked through the browser DOM. Importing and editing
  in Illustrator, Inkscape, Figma, or CorelDRAW was not tested.
- PNG creation, decoding, dimensions, and transparency were exercised. JPEG and WebP
  are supported workflow choices when encoding tools are available, but those
  encoding paths were not exercised in this check.
- Photo-specific realism checks were not exercised. The separate promo comparison
  uses built-in imagegen for tactile sculptural artwork; other image providers were
  not tested. The host agent must supply its available generation tool.
- The tests verify structural behavior and concrete artifacts. They do not prove
  that every future composition is attractive or that an agent will always select
  and follow the skill automatically. The remaining [scenarios](scenarios.md) are
  available for further behavioral evaluation.
