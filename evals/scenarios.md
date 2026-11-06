# Behavioral evaluation briefs

Use an isolated output directory. Give the agent `skills/golden-space/SKILL.md`
and one brief below. Inspect the actual output rather than matching its wording.
Record the agent, available tools, artifacts, checks performed, and shortcomings.
These are evaluation fixtures, not a record of completed multi-agent testing.

## Editorial poster

> Create an editable 1200 x 742 SVG exhibition poster. Copy: "Clay / Form / Space",
> "Ceramics exhibition", "12-14 June", "Studio 04". Use a warm palette. Consider
> a golden split, but choose the composition that best fits the copy.

Check that the agent accounts for margins and gutters before a ratio split, uses
a visible hierarchy and purposeful space, retains the wording as live text, and
delivers a complete SVG with separately editable illustration parts. Inspect a render.

## Dense diagram

> Make a monochrome editable SVG flow diagram for intake, review, revise, and
> publish. Review can return to revise, and revise returns to review. Labels must
> be legible at 800 px wide. Use equal importance for all process steps.

Check accurate flow and labels, meaningful grouping, readable connectors, and a
layout suited to the content. The agent should not force a golden split or fill
the diagram with decorative geometry. Check arrowheads and return paths visually.

## Preserve a different style

> Review a supplied maximalist event poster. Keep its bright palette, decorative
> style, all copy, and dimensions. Improve only hierarchy and whitespace.

Check that the agent improves relationships within the chosen style. Replacing it
with the bundled arch poster or a minimalist aesthetic fails the brief.

## Repair SVG structure

> Clean a supplied SVG containing duplicate IDs, a broken local gradient reference,
> a linked bitmap, and live text. Preserve the wording and important appearance.

Check that duplicates and references are repaired, text remains live, and the agent
does not relabel a bitmap as vector or silently remove essential imagery. If a
faithful vector replacement cannot be made from the available source, it should
report the limitation and request only what is needed to finish.

## Typography tradeoff

> Deliver an editable wordmark master and a separate outlined distribution copy
> using the provided licensed font file.

Check that the master retains text. Outlining requires a real font-to-path tool;
invented glyph paths or an unconverted file labeled "outlined" fail. If the tool
is unavailable, the agent should state what it could produce and what remains.

## Limited tools and constrained handoff

> Return only complete SVG source for a 256 x 256 transparent abstract mark. You
> cannot run Python, render images, or use a vector editor.

Check a full SVG document, transparent background, separate geometry, descriptive
IDs, and no extra prose. The agent should not claim to have run checks. Lack of a
renderer should not prevent producing the requested source.
