#!/usr/bin/env python3
"""Lint a conservative editable SVG profile; not a renderer or security sanitizer."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
XML = "http://www.w3.org/XML/1998/namespace"
MAX_BYTES = 5 * 1024 * 1024
SHAPES = {"rect", "circle", "ellipse", "line", "polyline", "polygon", "path", "text", "use"}
ALLOWED = SHAPES | {
    "svg", "g", "defs", "title", "desc", "tspan", "textPath", "symbol",
    "linearGradient", "radialGradient", "stop", "clipPath", "mask", "pattern",
    "marker", "metadata",
}
NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
DIMENSION = re.compile(rf"({NUMBER})(?:px|pt|pc|mm|cm|in|%)?\Z")
URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    location: str
    message: str


def expanded_name(name: str) -> tuple[str, str]:
    if name.startswith("{"):
        namespace, local = name[1:].split("}", 1)
        return namespace, local
    return "", name


def check_svg(path: Path) -> list[Issue]:
    issues: list[Issue] = []

    def add(severity: str, code: str, location: str, message: str) -> None:
        issues.append(Issue(severity, code, location, message))

    try:
        with path.open("rb") as handle:
            data = handle.read(MAX_BYTES + 1)
    except OSError as exc:
        return [Issue("error", "read", str(path), str(exc))]
    if len(data) > MAX_BYTES:
        return [Issue("error", "size", "document", "File exceeds the 5 MiB profile limit.")]
    try:
        source = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return [Issue("error", "encoding", "document", "Use UTF-8 XML.")]
    # Scan before parsing: ElementTree otherwise discards comments and processing instructions.
    scan = re.sub(r"<!--[\s\S]*?-->", "", source)
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", scan, re.IGNORECASE):
        return [Issue("error", "declaration", "document", "DOCTYPE and entity declarations are excluded.")]
    if re.search(r"<\?(?!xml\s)", scan, re.IGNORECASE):
        add("error", "processing-instruction", "document", "Processing instructions are excluded.")
    try:
        root = ET.fromstring(source)
    except (ET.ParseError, ValueError) as exc:
        add("error", "xml", "document", str(exc))
        return issues
    if root.tag != f"{{{SVG}}}svg":
        add("error", "root", "document", "Root must be svg in the SVG namespace.")
        return issues

    view_box = root.get("viewBox", "")
    values = re.split(r"[\s,]+", view_box.strip())
    if (len(values) != 4 or any(not re.fullmatch(NUMBER, v) for v in values)
            or any(not math.isfinite(float(v)) for v in values)
            or float(values[2]) <= 0 or float(values[3]) <= 0):
        add("error", "viewbox", "svg", "viewBox needs four finite numbers and positive dimensions.")
    for attr in ("width", "height"):
        match = DIMENSION.fullmatch(root.get(attr, ""))
        if not match or not math.isfinite(float(match[1])) or float(match[1]) <= 0:
            add("error", "dimensions", "svg", f"Declare a positive finite {attr}.")

    elements = list(root.iter())
    counts = Counter(el.get("id") for el in elements if el.get("id"))
    by_id = {el.get("id"): el for el in elements if el.get("id")}
    for identifier, count in sorted(counts.items()):
        if count > 1:
            add("error", "duplicate-id", identifier, f"ID occurs {count} times.")
    for tag in ("title", "desc"):
        child = root.find(f"{{{SVG}}}{tag}")
        if child is None or not "".join(child.itertext()).strip():
            add("error", "description", "svg", f"Provide a nonempty root {tag}.")
        elif not child.get("id") or child.get("id") not in root.get("aria-labelledby", "").split():
            add("error", "accessible-name", "svg", f"Link the root {tag} ID in aria-labelledby.")
    for identifier in root.get("aria-labelledby", "").split():
        if identifier not in by_id:
            add("error", "broken-reference", "svg", f"Missing accessible name target #{identifier}.")

    references: list[tuple[str, str, str]] = []
    stack = [(root, 0, "")]
    while stack:
        el, depth, inherited_font = stack.pop()
        namespace, tag = expanded_name(el.tag)
        location = el.get("id") or tag
        if namespace != SVG:
            add("error", "namespace", location, "Foreign elements are excluded from the master.")
        elif tag not in ALLOWED:
            add("error", "element", location, f"<{tag}> is excluded from the editable profile.")
        if tag in SHAPES | {"g"} and not el.get("id"):
            add("error", "missing-id", location, "Name this editable object or group with a unique ID.")
        if el.get("id") is not None and (not el.get("id") or re.search(r"\s", el.get("id", ""))):
            add("error", "invalid-id", location, "IDs must be nonempty and contain no whitespace.")
        if tag in {"use", "symbol", "mask", "textPath"}:
            add("warning", "editor-feature", location, f"Review <{tag}> editing behavior in the target editor.")
        if tag == "g" and depth > 4:
            add("warning", "deep-groups", location, "More than four group levels make editing harder.")
        if tag == "path" and len(el.get("d", "")) > 8000:
            add("warning", "long-path", location, "Review path complexity and independently editable parts.")
        font = el.get("font-family", inherited_font)
        if tag == "text" and not font.strip():
            add("warning", "font", location, "Declare a font family with a fallback, here or on a parent.")
        for attribute, value in el.attrib.items():
            attr_ns, attr = expanded_name(attribute)
            if attr_ns not in {"", XLINK, XML}:
                continue  # Editor metadata is not appearance validation.
            if attr.lower().startswith("on"):
                add("error", "event", location, "Event attributes are excluded.")
            if attr in {"style", "class"}:
                add("error", "css", location, "Use presentation attributes instead of style or class.")
            if (attr_ns == XML and attr == "base") or attr == "src":
                add("error", "external-reference", location, f"{attr} is excluded from the master.")
            if attr == "href":
                if value.startswith("#") and len(value) > 1:
                    references.append((location, attr, value[1:]))
                else:
                    add("error", "external-reference", location, "Use local fragment references only.")
            urls = list(URL.finditer(value))
            if re.search(r"url\s*\(", value, re.IGNORECASE) and not urls:
                add("error", "reference-syntax", location, "Could not parse the URL reference.")
            for match in urls:
                target = match[2].strip()
                if target.startswith("#") and len(target) > 1:
                    references.append((location, attr, target[1:]))
                else:
                    add("error", "external-reference", location, "Use local fragment references only.")
            if "var(" in value.lower():
                add("error", "css", location, "CSS variables are excluded from the master.")
            if attr == "filter" and value.strip().lower() != "none":
                add("error", "filter", location, "Filter effects are excluded from the portable master.")
        stack.extend((child, depth + (tag == "g"), font) for child in reversed(list(el)))

    for location, attr, target in references:
        if target not in by_id:
            add("error", "broken-reference", location, f"Missing local target #{target}.")
            continue
        target_tag = expanded_name(by_id[target].tag)[1]
        expected = {
            "fill": {"linearGradient", "radialGradient", "pattern"},
            "stroke": {"linearGradient", "radialGradient", "pattern"},
            "clip-path": {"clipPath"}, "mask": {"mask"},
            "marker-start": {"marker"}, "marker-mid": {"marker"}, "marker-end": {"marker"},
        }.get(attr)
        if expected is not None and target_tag not in expected:
            add("error", "reference-type", location, f"{attr} points to an incompatible <{target_tag}>.")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", type=Path, nargs="+", help="SVG files to check (read only)")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings as well as errors")
    parser.add_argument("--json", action="store_true", help="Emit a JSON report")
    args = parser.parse_args(argv)
    reports = [{"file": str(path), "issues": [asdict(i) for i in check_svg(path)]} for path in args.files]
    failed = any(i["severity"] == "error" or args.strict for r in reports for i in r["issues"])
    if args.json:
        print(json.dumps({"passed": not failed, "files": reports}, indent=2, ensure_ascii=True))
    else:
        for report in reports:
            print(f"{report['file']}: {len(report['issues'])} issue(s)")
            for issue in report["issues"]:
                print(f"  {issue['severity'].upper()} {issue['code']} [{issue['location']}]: {issue['message']}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
