"""Keep the Week 10 Reader release complete and limited to approved content."""
import json
from pathlib import Path
import re
import tempfile
import unittest

import yaml

import check_publication_assets as assets
import prepare_publication as publication

ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / 'notebooks/week10/L_Game_theory.ipynb'
EXCLUDED = {'slides-only', 'remove-cell', 'archive-only', 'presenter-notes'}


class Week10PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notebook = json.loads(LECTURE.read_text())
        cls.cells = [c for c in notebook['cells'] if not
                     set(c.get('metadata', {}).get('tags', [])) & EXCLUDED]
        cls.ids = [c['id'] for c in cls.cells]
        cls.sources = {c['id']: ''.join(c.get('source', [])) for c in cls.cells}

    def test_release_boundary(self):
        self.assertTrue(publication.allowed('notebooks/week08/L_Critical_phenomena.ipynb'))
        self.assertTrue(publication.allowed(str(LECTURE.relative_to(ROOT))))
        self.assertTrue(publication.allowed('notebooks/week09/L_InformationTheory.ipynb'))
        self.assertFalse(publication.allowed('notebooks/week11/L_Future.ipynb'))

    def test_toc_includes_released_week10_reader_and_linked_example(self):
        toc = yaml.safe_load((ROOT / 'myst.yml').read_text())['project']['toc']
        entry = next(item for item in toc if item['file'].startswith('notebooks/week10/'))
        self.assertEqual(entry['file'], str(LECTURE.relative_to(ROOT)))
        self.assertEqual(entry['children'], [
            {'file': 'notebooks/week10/Slides.md'},
            {'file': 'notebooks/week10/Practice.md'},
            {'file': 'notebooks/week10/WS_Game_theory.ipynb'},
        ])
        self.assertTrue(any('week09/' in item['file'] for item in toc))

    def test_reader_assets_and_local_notebook_links_exist(self):
        for source in self.sources.values():
            for relative in re.findall(r'(?:src|href)="(images/[^"#?]+)', source):
                self.assertTrue((LECTURE.parent / relative).is_file(), relative)
            for relative in re.findall(r'\]\(([^):]+\.ipynb)\)', source):
                self.assertTrue((LECTURE.parent / relative).is_file(), relative)

    def test_week10_citation_overrides_are_included(self):
        bibliography = (ROOT / 'course_references.bib').read_text()
        self.assertIn('author = {Maynard Smith, John and Price, George R.}', bibliography)
        self.assertIn('doi = {10.1038/246015a0}', bibliography)
        self.assertIn('doi = {10.1111/evo.14416}', bibliography)

    def test_simulation_comes_before_analysis(self):
        # The reader introduces the biological RPS example before the two
        # population-model views: first the moving-agent explorable, then its
        # interpretation.  The old test referred to pre-release cell ids and
        # therefore inverted this order after the Week 10 reorganisation.
        sequence = ['w10-lizard-morphs', 'w10-rps-population',
                    'w10-rps-arena', 'w10-rps-population-behaviour']
        positions = [self.ids.index(i) for i in sequence]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(positions[2], positions[1] + 1)
        self.assertEqual(positions[3], positions[2] + 1)

    def test_ordinal_definition_is_with_prisoners_dilemma(self):
        definition = 'a8733185-a037-45a2-b04e-75ac43cedb98'
        self.assertIn('**Ordinal payoffs**', self.sources[definition])
        self.assertLess(self.ids.index(definition), self.ids.index('09fa3a4f'))
        self.assertIn('{dropdown} How many games are shown?', self.sources['f6989099'])

    def test_normal_form_equilibria(self):
        # The four matrices are now a single comparison cell.  Check the
        # canonical entries directly so this guard remains useful after the
        # individual matrix cells were removed from the released reader.
        source = self.sources['w10-game-comparison-matrices']
        expected = {
            'Prisoner’s Dilemma': ['(3,3)', '(1,4)', '(4,1)', '(2,2)'],
            'Stag Hunt': ['(4,4)', '(1,3)', '(3,1)', '(2,2)'],
            'Chicken': ['(3,3)', '(2,4)', '(4,2)', '(1,1)'],
            'Matching Pennies': ['(1,−1)', '(−1,1)', '(−1,1)', '(1,−1)'],
        }
        for title, entries in expected.items():
            self.assertIn(f'>{title}<', source)
            start = source.index(f'>{title}<')
            block = source[start:source.find('</div>', start)]
            for entry in entries:
                self.assertIn(entry, block)
        self.assertIn('Matching Pennies is grey', source)

    def test_generated_site_checker_requires_released_pages(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = assets.check(root)
            self.assertTrue(any('week10/l-game-theory/index.html' in error for error in errors))
            week09 = root / 'notebooks/week09/example/index.html'
            week09.parent.mkdir(parents=True)
            week09.touch()
            self.assertFalse(any('Unreleased material staged' in error for error in assets.check(root)))
            forbidden = root / 'slides/week10/L_Game_theory.slides.html'
            forbidden.parent.mkdir(parents=True)
            forbidden.touch()
            self.assertTrue(any('Reader-only release' in error for error in assets.check(root)))

    def test_reader_has_no_code_or_slide_only_cells(self):
        self.assertFalse(any(c['cell_type'] == 'code' for c in self.cells))
        self.assertNotIn('w10-population-terms-slide', self.ids)


if __name__ == '__main__':
    unittest.main()
