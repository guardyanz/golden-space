"""Observable checks for the portable SVG profile and read-only CLI."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/golden-space/scripts/check_svg.py"
sys.path.insert(0, str(SCRIPT.parent))
from check_svg import check_svg  # noqa: E402


def document(body='', attrs='', font='font-family="Arial, sans-serif"'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200"
        viewBox="0 0 300 200" aria-labelledby="title description" {attrs}>
      <title id="title">Example</title><desc id="description">A simple graphic.</desc>
      <text id="heading" x="20" y="40" {font}>Editable text</text>{body}</svg>'''


class SvgProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / "art.svg"

    def check(self, source):
        self.file.write_text(source, encoding="utf-8")
        return check_svg(self.file)

    def codes(self, source):
        return {i.code for i in self.check(source)}

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              text=True, capture_output=True, check=False)

    def test_live_text_and_primitives_pass(self):
        self.assertEqual(self.check(document('<circle id="disc" cx="100" cy="100" r="30"/>')), [])

    def test_distributed_examples_pass_without_warnings(self):
        files = [ROOT / "skills/golden-space/assets/starter.svg", *sorted((ROOT / "examples").glob("*.svg"))]
        self.assertGreaterEqual(len(files), 3)
        for path in files:
            with self.subTest(path=path):
                self.assertEqual(check_svg(path), [])

    def test_missing_file_is_reported(self):
        self.assertEqual(check_svg(self.file)[0].code, "read")

    def test_malformed_xml_is_reported(self):
        self.assertIn("xml", self.codes("<svg>"))

    def test_namespace_is_required(self):
        self.assertIn("root", self.codes(document().replace('xmlns="http://www.w3.org/2000/svg"', '')))

    def test_viewbox_rejects_missing_nonfinite_and_nonpositive_values(self):
        for value in ('', '0 0 300', '0 0 0 20', '0 0 30 -1', '0 0 NaN 30', '0 0 1e309 20', 'a b c d'):
            with self.subTest(value=value):
                self.assertIn("viewbox", self.codes(document().replace('0 0 300 200', value)))
        self.assertNotIn("viewbox", self.codes(document().replace('0 0 300 200', '-10,-5,3e2,200')))

    def test_dimensions_require_positive_finite_values(self):
        for value in ('0', '-2', 'auto', 'NaN', '1e309', ''):
            with self.subTest(value=value):
                self.assertIn("dimensions", self.codes(document().replace('width="300"', f'width="{value}"')))

    def test_duplicate_and_missing_object_ids(self):
        self.assertIn("duplicate-id", self.codes(document('<rect id="heading" width="10" height="10"/>')))
        self.assertIn("missing-id", self.codes(document('<rect width="10" height="10"/>')))
        self.assertIn("invalid-id", self.codes(document('<g id="bad id"/>')))

    def test_excluded_content_is_reported(self):
        for tag in ('image', 'script', 'style', 'filter', 'foreignObject', 'animate', 'set', 'feImage'):
            with self.subTest(tag=tag):
                self.assertIn("element", self.codes(document(f'<{tag} id="excluded"/>')))
        self.assertIn("namespace", self.codes(document('<div xmlns="http://www.w3.org/1999/xhtml"/>')))

    def test_event_handlers_are_excluded(self):
        self.assertIn("event", self.codes(document(attrs='onload="alert(1)"')))

    def test_external_links_and_resources_are_excluded(self):
        for target in ('https://example.com/a.svg#art', 'file:///a.svg', 'data:image/png;base64,AAAA', '//example.com', ''):
            with self.subTest(target=target):
                self.assertIn("external-reference", self.codes(document(f'<use id="copy" href="{target}"/>')))
        self.assertIn("external-reference", self.codes(document('<rect id="box" fill="url(https://example.com/a.svg#x)"/>')))
        self.assertIn("external-reference", self.codes(document(attrs='xml:base="https://example.com/"')))

    def test_local_gradients_and_clips_pass(self):
        body = '''<defs><linearGradient id="paint"><stop offset="0" stop-color="#123456"/>
        <stop offset="1" stop-color="#ffffff"/></linearGradient>
        <clipPath id="crop"><circle id="crop-circle" cx="50" cy="50" r="20"/></clipPath></defs>
        <rect id="box" width="100" height="100" fill="url('#paint')" clip-path="url(#crop)"/>'''
        self.assertEqual(self.check(document(body)), [])

    def test_broken_and_wrong_type_references_are_reported(self):
        self.assertIn("broken-reference", self.codes(document('<rect id="box" fill="url(#missing)"/>')))
        self.assertIn("reference-type", self.codes(document('<rect id="box" fill="url(#heading)"/>')))
        self.assertIn("broken-reference", self.codes(document('<use xmlns:xlink="http://www.w3.org/1999/xlink" id="copy" xlink:href="#missing"/>')))

    def test_css_and_filters_are_excluded(self):
        for attrs, code in [('style="fill:red"', 'css'), ('class="red"', 'css'),
                            ('fill="var(--ink)"', 'css'), ('filter="blur(2px)"', 'filter')]:
            with self.subTest(attrs=attrs):
                self.assertIn(code, self.codes(document(f'<rect id="box" {attrs}/>')))

    def test_font_inheritance_avoids_false_warning(self):
        self.assertNotIn("font", self.codes(document(attrs='font-family="Arial, sans-serif"', font='')))
        issues = self.check(document(font=''))
        self.assertEqual([(i.severity, i.code) for i in issues], [('warning', 'font')])

    def test_warnings_and_strict_exit_status(self):
        self.check(document('<use id="copy" href="#heading"/>'))
        ordinary = self.cli(self.file)
        strict = self.cli('--strict', self.file)
        self.assertEqual(ordinary.returncode, 0, ordinary.stderr)
        self.assertEqual(strict.returncode, 1, strict.stderr)

    def test_declarations_and_stylesheet_instructions_are_excluded(self):
        for prefix, code in [('<!DOCTYPE svg>', 'declaration'),
                             ('<?xml-stylesheet href="external.css"?>', 'processing-instruction')]:
            with self.subTest(prefix=prefix):
                self.assertIn(code, self.codes(prefix + document()))
        self.assertEqual(self.check('<?xml version="1.0" encoding="UTF-8"?>' + document()), [])
        self.assertEqual(self.check('<!-- Example: <!DOCTYPE svg> -->' + document()), [])

    def test_non_utf8_is_reported(self):
        self.file.write_bytes(b'\xff\xfe<svg/>')
        self.assertEqual(check_svg(self.file)[0].code, 'encoding')

    def test_oversized_file_is_reported(self):
        self.file.write_bytes(b' ' * (5 * 1024 * 1024 + 1))
        self.assertEqual(check_svg(self.file)[0].code, 'size')

    def test_accessible_description_targets_must_exist(self):
        self.assertIn('description', self.codes(document().replace('<title id="title">Example</title>', '')))
        self.assertIn('accessible-name', self.codes(document().replace('title description', 'title')))
        self.assertIn('broken-reference', self.codes(document().replace('title description', 'title description ghost')))

    def test_json_cli_reports_multiple_files_without_modifying_them(self):
        source = document()
        self.file.write_text(source, encoding='utf-8')
        before = self.file.read_bytes()
        result = self.cli('--json', self.file, Path(self.temp.name) / 'absent.svg')
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report['passed'])
        self.assertEqual(len(report['files']), 2)
        self.assertEqual(report['files'][0]['issues'], [])
        self.assertEqual(report['files'][1]['issues'][0]['code'], 'read')
        self.assertEqual(self.file.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
