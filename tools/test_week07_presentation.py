"""Source regressions; follow with a rendered reader/slide inspection."""
import json
from pathlib import Path
import re
import unittest
import tempfile
from prepare_publication import allowed, filter_toc
from check_publication_assets import check as check_assets

ROOT = Path(__file__).resolve().parents[1]
CELLS = json.loads((ROOT / 'notebooks/week07/L_Intelligent_systems.ipynb').read_text())['cells']
READER = '\n'.join(''.join(c.get('source', [])) for c in CELLS
                   if not set(c.get('metadata', {}).get('tags', [])) &
                   {'slides-only', 'remove-cell', 'archive-only', 'presenter-notes'})


class PresentationTests(unittest.TestCase):
    def test_published_explorable_routes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = ''.join(f'<iframe src="images/{name}"></iframe>' for name in
                              ['aco_network_explorer.html', 'pso_explorer.html'])
            for page in ['notebooks/week07/l-intelligent-systems/index.html',
                         'slides/week07/L_Intelligent_systems.slides.html']:
                target = root / page; target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            for route in ['notebooks/week07/images',
                          'notebooks/week07/l-intelligent-systems/images', 'slides/week07/images']:
                for name in ['aco_network_explorer.html', 'pso_explorer.html']:
                    target = root / route / name
                    target.parent.mkdir(parents=True, exist_ok=True); target.write_text('explorable')
            self.assertEqual(check_assets(root), [])
            (root / 'notebooks/week07/images/pso_explorer.html').unlink()
            self.assertTrue(any('not staged' in error for error in check_assets(root)))
            (root / 'notebooks/week08').mkdir()
            self.assertTrue(any('Unreleased' in error for error in check_assets(root)))

    def test_independent_figure_numbers(self):
        self.assertEqual(re.findall(r'(?:<strong>|\*\*)Figure 7\.(\d+)\.(?:</strong>|\*\*)', READER),
                         [str(i) for i in range(1, 12)])

    def test_no_double_numbering(self):
        for figure in re.findall(r'<figure\b.*?</figure>', READER, re.S):
            self.assertNotRegex(figure, r'Figure 7\.\d+')

    def test_table_uses_myst_not_raw_html(self):
        self.assertIn('```{list-table}\n:class: pso-measurements-table', READER)
        self.assertNotIn('<div class="pso-measurements-table">', READER)

    def test_ensemble_is_independent(self):
        self.assertNotIn('Panel C', READER)
        slides = [''.join(c.get('source', [])) for c in CELLS
                  if 'slides-only' in c.get('metadata', {}).get('tags', [])]
        self.assertTrue(any('pso_ensemble.svg' in s for s in slides))
        self.assertFalse(any('pso_analysis_levels.png' in s for s in slides))

    def test_referenced_figure_assets_exist(self):
        sources = '\n'.join(''.join(c.get('source', [])) for c in CELLS)
        paths = re.findall(r'(?:src="|\]\()(images/[^"\s)]+)', sources)
        self.assertTrue(paths)
        for path in paths:
            self.assertTrue((ROOT / 'notebooks/week07' / path).is_file(), path)

    def test_publication_boundary(self):
        self.assertTrue(allowed('notebooks/week07/Slides.md'))
        self.assertFalse(allowed('notebooks/week08/Slides.md'))
        self.assertFalse(allowed('week10'))
        original = [{'file': 'intro.md', 'children': [{'file': 'notebooks/week08/L.ipynb'}]},
                    {'file': 'notebooks/week07/L.ipynb'}, {'file': 'notebooks/week10/L.ipynb'}]
        result = filter_toc(original)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['children'], [])
        self.assertEqual(len(original[0]['children']), 1)


if __name__ == '__main__':
    unittest.main()
