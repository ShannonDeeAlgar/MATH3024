import json
from pathlib import Path
import tempfile
import unittest

import check_equation_consistency as audit


class EquationConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = self.root / "notebooks/week01/L_Test.ipynb"
        self.path.parent.mkdir(parents=True)
        self.data = {"cells": [
            {"id": "reader", "cell_type": "markdown", "metadata": {"tags": ["reader-only"]},
             "source": ["$$x=y$$\n"]},
            {"id": "slide", "cell_type": "markdown", "metadata": {"tags": ["slides-only"]},
             "source": ["<!-- reader-equation: reader:0 -->\nNotation: $x$ is position.\n"]},
        ]}
        self.write()
        cells = audit.load_cells(self.path)
        self.manifest = self.root / "audit.json"
        self.manifest.write_text(json.dumps({"notebooks": {
            str(self.path.relative_to(self.root)): {
                "math_signatures": {i: audit.math_signature(audit.resolved_source(c, cells))
                                    for i, c in cells.items()},
                "displays": [{"slide": "slide", "index": 0, "mode": "exact",
                              "reader": "reader", "reader_index": 0}],
            }}}))

    def write(self):
        self.path.write_text(json.dumps(self.data))

    def errors(self):
        self.write()
        return audit.check(self.root, self.manifest)

    def test_valid_links(self):
        self.assertEqual(self.errors(), [])

    def test_dropdown_math_is_audited(self):
        source = "```{dropdown} Replication\n$x=1$\n```\n"
        self.assertNotEqual(audit.math_signature(source),
                            audit.math_signature(source.replace('x=1', 'x=2')))

    def test_nested_container_math_is_audited(self):
        source = "::::{note}\n```{dropdown} Details\n$$x=1$$\n```\n::::"
        self.assertNotEqual(audit.math_signature(source),
                            audit.math_signature(source.replace('x=1', 'x=2')))

    def test_code_example_is_not_math(self):
        self.assertIsNone(audit.math_signature('```python\nprint("$x$")\n```'))

    def test_reader_change_updates_render_but_requires_notation_review(self):
        self.data["cells"][0]["source"] = ["$$x=z$$"]
        self.assertTrue(self.errors())
        cells = audit.load_cells(self.path)
        self.assertIn("$$x=z$$", audit.resolved_source(cells["slide"], cells))

    def test_inline_notation_drift(self):
        self.data["cells"][1]["source"][0] += " $z$"
        self.assertTrue(self.errors())

    def test_manual_copy_is_rejected(self):
        self.data["cells"][1]["source"][0] = "$$x=y$$\nNotation: $x$ is position.\n"
        self.assertTrue(self.errors())

    def test_new_equation_requires_audit(self):
        self.data["cells"][1]["source"][0] += "$$a=b$$"
        self.assertTrue(self.errors())

    def test_prose_edit_does_not_require_math_review(self):
        self.data["cells"][1]["source"][0] += "\nA shorter explanation."
        self.assertEqual(self.errors(), [])

    def test_materialized_notebook(self):
        out = self.root / "render.ipynb"
        audit.materialize(self.path, out)
        text = "".join(json.loads(out.read_text())["cells"][1]["source"])
        self.assertIn("$$x=y$$", text)
        self.assertNotIn("reader-equation", text)

    def test_deleted_reader(self):
        self.data["cells"].pop(0)
        self.assertTrue(self.errors())


if __name__ == "__main__":
    unittest.main()
