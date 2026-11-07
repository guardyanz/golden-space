# Contributing

Use English for all repository content, including documentation, sample prompts,
code comments, image labels, SVG text, captions, and metadata. When changing text
in an image, update its editable source and regenerate every affected raster export.

Include a concrete design brief or SVG that demonstrates the proposed improvement.
Explain the observable result: clearer grouping, preserved text editing, a corrected
reference, or another specific outcome. Avoid adding a universal rule from a single
example or imposing one visual style on all briefs.

Keep common instructions in `SKILL.md` and conditional technical detail in its linked
references. Preserve a complete installable skill directory. Use original or clearly
licensed example assets and identify font dependencies.

For checker changes, run `python -m unittest discover -s tests -v` and add a meaningful
case when behavior changes. For composition changes, render the relevant SVG at its
intended size and a smaller preview. State which renderer or editor was actually
used. Do not equate structural lint with visual or editor validation.

For instruction changes, exercise relevant [evaluation scenarios](evals/scenarios.md)
with an agent and report the generated artifacts and observed limitations. The
scenarios are a manual behavioral evaluation, not a claim that every agent has passed.
