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
        self.assertFalse(publication.allowed('notebooks/week09/L_InformationTheory.ipynb'))
        self.assertFalse(publication.allowed('notebooks/week11/L_Future.ipynb'))

    def test_toc_includes_only_week10_reader_and_linked_example(self):
        toc = yaml.safe_load((ROOT / 'myst.yml').read_text())['project']['toc']
        entry = next(item for item in toc if item['file'].startswith('notebooks/week10/'))
        self.assertEqual(entry['file'], str(LECTURE.relative_to(ROOT)))
        self.assertEqual(entry['children'], [{'file': 'notebooks/week10/Axelrod_tournament.ipynb'}])
        self.assertFalse(any('week09/' in item['file'] for item in toc))

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
        sequence = ['w10-rps-population', 'w10-rps-arena',
                    'w10-rps-population-behaviour', 'w10-lizard-morphs']
        positions = [self.ids.index(i) for i in sequence]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(positions[2], positions[1] + 1)

    def test_ordinal_definition_is_with_prisoners_dilemma(self):
        definition = 'a8733185-a037-45a2-b04e-75ac43cedb98'
        self.assertIn('**Ordinal payoffs**', self.sources[definition])
        self.assertLess(self.ids.index(definition), self.ids.index('09fa3a4f'))
        self.assertIn('{dropdown} How many games are shown?', self.sources['f6989099'])

    def test_normal_form_equilibria(self):
        for cell_id, expected in [
            ('w10-stag-hunt-normal-form', {(0, 0), (1, 1)}),
            ('w10-chicken-normal-form', {(0, 1), (1, 0)}),
            ('w10-matching-pennies-normal-form', set()),
        ]:
            source = self.sources[cell_id]
            rows = '\n'.join(line for line in source.replace('−', '-').splitlines()
                             if line.startswith('| '))
            pairs = [tuple(map(int, pair)) for pair in re.findall(r'\((-?\d+),\s*(-?\d+)\)', rows)]
            self.assertEqual(len(pairs), 4)
            matrix = [pairs[:2], pairs[2:]]
            actual = {(i, j) for i in range(2) for j in range(2)
                      if matrix[i][j][0] >= matrix[1-i][j][0]
                      and matrix[i][j][1] >= matrix[i][1-j][1]}
            self.assertEqual(actual, expected)
        self.assertIn('not an exact entry', self.sources['w10-matching-pennies-normal-form'])

    def test_generated_site_checker_requires_week10_and_rejects_week9(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = assets.check(root)
            self.assertTrue(any('week10/l-game-theory/index.html' in error for error in errors))
            forbidden = root / 'notebooks/week09/example/index.html'
            forbidden.parent.mkdir(parents=True)
            forbidden.touch()
            self.assertTrue(any('Unreleased material staged' in error for error in assets.check(root)))
            forbidden = root / 'slides/week10/L_Game_theory.slides.html'
            forbidden.parent.mkdir(parents=True)
            forbidden.touch()
            self.assertTrue(any('Reader-only release' in error for error in assets.check(root)))

    def test_reader_has_no_code_or_slide_only_cells(self):
        self.assertFalse(any(c['cell_type'] == 'code' for c in self.cells))
        self.assertNotIn('w10-population-terms-slide', self.ids)


if __name__ == '__main__':
    unittest.main()
