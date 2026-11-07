#!/usr/bin/env python3
"""Build hybrid SVG promo layouts from the saved, unmodified imagegen artwork.

Uses only Python's standard library. PNG exports are rendered separately; this
script never calls an image API and does not regenerate the artwork.
"""

import base64
import hashlib
import json
from pathlib import Path
import struct
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
VARIANTS = ("without-golden-space", "with-golden-space")


def png_data(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def poster(variant):
    image = png_data(ROOT / "assets" / f"{variant}-artwork.png")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350" role="img" aria-labelledby="art-title art-desc">
  <title id="art-title">Golden Space repository promotion</title>
  <desc id="art-desc">Hybrid promo layout with one embedded AI-generated raster artwork layer and separately editable text and vector controls. Variant: {variant}.</desc>
  <g id="artwork-layer">
    <image id="generated-artwork" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" href="{image}"/>
  </g>
  <g id="identity-copy" fill="#17372e">
    <text id="eyebrow" x="76" y="108" font-family="Arial, Helvetica, sans-serif" font-size="20" letter-spacing="2.1">DESIGN SKILL FOR AI AGENTS</text>
    <text id="headline" x="68" y="263" font-family="Georgia, 'Times New Roman', serif" font-size="132" letter-spacing="-4">
      <tspan x="68" y="263">Golden</tspan>
      <tspan x="68" y="394">Space.</tspan>
    </text>
    <text id="tagline" x="76" y="481" font-family="Arial, Helvetica, sans-serif" font-size="36">
      <tspan x="76" y="481">Better space.</tspan>
      <tspan x="76" y="526">Clearer design.</tspan>
    </text>
  </g>
  <g id="feature-copy" fill="#17372e" font-family="Arial, Helvetica, sans-serif" font-size="24" letter-spacing="1.6">
    <text id="feature-whitespace" x="76" y="707">WHITESPACE</text>
    <text id="feature-proportion" x="76" y="747">PROPORTION</text>
    <text id="feature-svg" x="76" y="787">EDITABLE SVG</text>
  </g>
  <g id="call-to-action">
    <rect id="cta-background" x="76" y="1114" width="276" height="58" rx="4" fill="#17372e"/>
    <text id="cta-copy" x="100" y="1152" font-family="Arial, Helvetica, sans-serif" font-size="26" fill="#f6f0e6">Explore the repo</text>
  </g>
  <g id="repository-footer">
    <rect id="footer-background" x="0" y="1210" width="1080" height="140" fill="#f6f0e6"/>
    <line id="footer-rule" x1="76" y1="1210" x2="1004" y2="1210" stroke="#17372e" stroke-width="1"/>
    <text id="license-copy" x="76" y="1253" font-family="Arial, Helvetica, sans-serif" font-size="16" letter-spacing="1.6" fill="#17372e">OPEN SOURCE / MIT</text>
    <text id="repository-url" x="76" y="1300" font-family="Arial, Helvetica, sans-serif" font-size="28" fill="#17372e">github.com/guardyanz/golden-space</text>
  </g>
</svg>
'''


def comparison():
    baseline = png_data(ROOT / "without-golden-space.png")
    guided = png_data(ROOT / "with-golden-space.png")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="2280" height="1600" viewBox="0 0 2280 1600" role="img" aria-labelledby="art-title art-desc">
  <title id="art-title">Imagegen with and without Golden Space</title>
  <desc id="art-desc">Two promotional posts from the same brief. The left uses baseline imagegen direction. The right adds Golden Space art direction. Both use an identical live-text layout. This is a one-sample illustration, not a benchmark.</desc>
  <rect id="background" width="2280" height="1600" fill="#e9e6df"/>
  <g id="comparison-labels" fill="#17372e" font-family="Arial, Helvetica, sans-serif">
    <text id="baseline-label" x="40" y="65" font-size="31" font-weight="700">Tanpa Golden Space</text>
    <text id="baseline-subtitle" x="40" y="103" font-size="20">Imagegen · brief dasar</text>
    <text id="guided-label" x="1160" y="65" font-size="31" font-weight="700">Dengan Golden Space</text>
    <text id="guided-subtitle" x="1160" y="103" font-size="20">Imagegen · tambahan arahan komposisi</text>
  </g>
  <g id="posts">
    <image id="baseline-post" x="40" y="140" width="1080" height="1350" href="{baseline}"/>
    <image id="guided-post" x="1160" y="140" width="1080" height="1350" href="{guided}"/>
  </g>
  <text id="method-note" x="40" y="1549" font-family="Arial, Helvetica, sans-serif" font-size="22" fill="#17372e">Brief, palet, teks, dan layout teks sama. Satu sampel per versi; hasil generasi dapat bervariasi.</text>
</svg>
'''


def vector_poster(variant):
    """A deliberate vector interpretation, not automatic tracing of the raster."""
    ns = "http://www.w3.org/2000/svg"
    ET.register_namespace("", ns)
    svg = ET.fromstring(poster(variant))
    svg.find(f"{{{ns}}}desc").text = (
        "Fully vector interpretation of the imagegen promo composition, with live "
        "text, independent shapes, and editable gradients. Raster surface texture "
        "is simplified. Variant: " + variant + "."
    )
    artwork = svg.find(f"{{{ns}}}g")
    artwork.remove(artwork[0])
    common = '''<g xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="arch-paint" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#3c6250"/><stop offset="1" stop-color="#1a3b2d"/>
        </linearGradient>
        <linearGradient id="inner-paint" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#162d20"/><stop offset="1" stop-color="#294332"/>
        </linearGradient>
        <radialGradient id="sphere-paint" cx="0.3" cy="0.23" r="0.8">
          <stop offset="0" stop-color="#e9a16c"/><stop offset="0.55" stop-color="#c4713d"/>
          <stop offset="1" stop-color="#7d3a1c"/>
        </radialGradient>
        <linearGradient id="podium-paint" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#e9dac5"/><stop offset="1" stop-color="#c8b59a"/>
        </linearGradient>
      </defs>
      <rect id="vector-paper" width="1080" height="1350" fill="#f6f0e6"/>
    </g>'''
    fragment = ET.fromstring(common)
    for child in list(fragment):
        artwork.append(child)
    if variant == "without-golden-space":
        shapes = '''<g xmlns="http://www.w3.org/2000/svg" id="sculptural-scene">
          <path id="terracotta-ground" d="M0 1170 C400 1150 650 950 1080 820 V1210 H0Z" fill="#bf754a"/>
          <path id="arch-front" d="M632 1110 V540 C632 250 870 72 1150 72 V250 C990 250 858 400 858 540 V1110Z" fill="url(#arch-paint)"/>
          <path id="arch-inner-face" d="M858 1110 V540 C858 390 1000 246 1150 246 V325 C1020 325 916 420 916 550 V1110Z" fill="url(#inner-paint)"/>
          <path id="podium-side" d="M425 1090 H1080 V1230 H425Z" fill="url(#podium-paint)"/>
          <ellipse id="podium-top" cx="753" cy="1090" rx="328" ry="48" fill="#e9ddcc"/>
          <ellipse id="sphere-contact" cx="849" cy="1110" rx="115" ry="14" fill="#7e644c" opacity="0.3"/>
          <circle id="terracotta-sphere" cx="850" cy="966" r="154" fill="url(#sphere-paint)"/>
          <path id="green-foreground" d="M0 1100 C220 1132 408 1193 590 1230 H0Z" fill="#2f4e3b"/>
        </g>'''
    else:
        shapes = '''<g xmlns="http://www.w3.org/2000/svg" id="sculptural-scene">
          <ellipse id="arch-contact" cx="820" cy="1092" rx="212" ry="21" fill="#a2937d" opacity="0.2"/>
          <path id="arch-front" d="M585 1062 V815 C585 665 688 583 810 583 C931 583 1020 674 1020 819 V1105 L928 1091 V828 C928 744 882 700 813 700 C738 700 678 752 678 832 V1074Z" fill="url(#arch-paint)"/>
          <path id="arch-inner-face" d="M678 1074 V832 C678 752 738 700 813 700 C818 700 825 701 832 703 C745 724 724 779 724 845 V1069Z" fill="url(#inner-paint)"/>
          <ellipse id="sphere-contact" cx="512" cy="1092" rx="61" ry="10" fill="#a2937d" opacity="0.3"/>
          <circle id="terracotta-sphere" cx="510" cy="1030" r="62" fill="url(#sphere-paint)"/>
        </g>'''
    artwork.append(ET.fromstring(shapes))
    ET.indent(svg, space="  ")
    return ET.tostring(svg, encoding="unicode") + "\n"


def manifest():
    return {
        "created": "2026-11-07",
        "generation_mode": "built-in image_gen",
        "tool_calls": 2,
        "samples_per_variant": 1,
        "reference_images": [],
        "seed_control": "not exposed",
        "model_version": "not exposed",
        "final_canvas": [1080, 1350],
        "layout": "Identical live-text and vector overlay in both variants.",
        "svg_type": "Hybrid: embedded generated raster artwork with editable text and vector overlays.",
        "artwork_files": {
            v: {
                "path": f"assets/{v}-artwork.png",
                "dimensions": list(struct.unpack(">II", (ROOT / "assets" / f"{v}-artwork.png").read_bytes()[16:24])),
                "sha256": hashlib.sha256((ROOT / "assets" / f"{v}-artwork.png").read_bytes()).hexdigest(),
                "prompt": f"prompts/{v}.txt",
                "prompt_sha256": hashlib.sha256((ROOT / "prompts" / f"{v}.txt").read_bytes()).hexdigest(),
            }
            for v in VARIANTS
        },
    }


if __name__ == "__main__":
    for variant in VARIANTS:
        (ROOT / f"{variant}.svg").write_text(poster(variant), encoding="utf-8")
        (ROOT / f"{variant}-vector.svg").write_text(vector_poster(variant), encoding="utf-8")
    (ROOT / "generation.json").write_text(json.dumps(manifest(), indent=2) + "\n", encoding="utf-8")
    if all((ROOT / f"{variant}.png").exists() for variant in VARIANTS):
        (ROOT / "comparison.svg").write_text(comparison(), encoding="utf-8")
    print("Built hybrid promo SVGs and generation record.")
