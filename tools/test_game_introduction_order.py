"""Teach the example before relying on its actions or strategic structure."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GameIntroductionOrderTests(unittest.TestCase):
    def test_action_profiles_precede_payoff_listing(self):
        path = ROOT / 'notebooks/week10/L_Game_theory.ipynb'
        ids = [c['id'] for c in json.loads(path.read_text())['cells']]
        for suffix in ('', '-notation-slide'):
            self.assertLess(ids.index('185e0fc7-41d0-47a3-b5e9-cdedc9619297' + suffix),
                            ids.index('e190c160-09b7-46d5-8983-6aa6f397daf4' + suffix))

    def test_complete_prisoner_story_before_formal_specification(self):
        path = ROOT / 'notebooks/week10/L_Game_theory.ipynb'
        cells = json.loads(path.read_text())['cells']
        for audience in ('reader', 'slides'):
            excluded = {'remove-cell', 'archive-only', 'presenter-notes',
                        'slides-only' if audience == 'reader' else 'reader-only'}
            ids = [c['id'] for c in cells
                   if not set(c.get('metadata', {}).get('tags', [])) & excluded
                   and (audience != 'slides' or c.get('metadata', {}).get('slideshow', {}).get('slide_type') not in {'skip', 'notes'})]
            intro = ids.index('d9bf6664')
            formal = ids.index('8309b600-a5e3-4836-853a-d685bf85dd2f')
            self.assertLess(intro, formal, audience)

            intro_text = ''.join(next(c['source'] for c in cells if c['id'] == 'd9bf6664'))
            formal_text = ''.join(next(c['source'] for c in cells if c['id'] == '8309b600-a5e3-4836-853a-d685bf85dd2f'))
            self.assertIn('questioned separately', intro_text)
            self.assertIn('one choice', intro_text)
            self.assertIn('Actions', formal_text)
            self.assertIn('cooperate', formal_text.lower())
            self.assertIn('defect', formal_text.lower())

    def test_payoff_and_cost_conventions_are_distinguished(self):
        path = ROOT / 'notebooks/week10/L_Game_theory.ipynb'
        cells = {c['id']: ''.join(c.get('source', []))
                 for c in json.loads(path.read_text())['cells']}
        for suffix in ('', '-notation-slide'):
            source = cells['e190c160-09b7-46d5-8983-6aa6f397daf4' + suffix]
            self.assertIn('$t_i$', source)
            self.assertIn('prison', source.lower())
            self.assertIn('$u_i=-t_i$', source)
            self.assertIn('$u_i=3-t_i$', source)
            self.assertIn('Minimise', source)
            self.assertIn('Maximise', source)

    def test_prisoners_dilemma_defined_before_explanatory_use(self):
        for audience in ('reader', 'slides'):
            introduced = False
            for path in sorted((ROOT / 'notebooks').glob('week*/L_*.ipynb')):
                for cell in json.loads(path.read_text())['cells']:
                    if cell['cell_type'] != 'markdown':
                        continue
                    metadata = cell.get('metadata', {})
                    tags = set(metadata.get('tags', []))
                    excluded = {'archive-only', 'remove-cell', 'presenter-notes'}
                    excluded.add('slides-only' if audience == 'reader' else 'reader-only')
                    if tags & excluded:
                        continue
                    if audience == 'slides' and metadata.get('slideshow', {}).get('slide_type') in {'skip', 'notes'}:
                        continue
                    source = ''.join(cell['source'])
                    if cell['id'] == 'd9bf6664':
                        self.assertIn('questioned separately', source)
                        introduced = True
                    if not introduced and cell['id'] not in {'w10-model-banner', 'w10-canonical-model-section-slide'}:
                        # Section markers intentionally name the canonical model;
                        # the following slide supplies the concrete story.
                        source = re.sub(r'<div class="canonical-model-marker">.*?</div>', '', source, flags=re.S)
                        self.assertNotRegex(source.lower(), r'prisoner.{0,3}dilemma',
                                            f'{audience}: {path.parent.name}: {cell["id"]}')
            self.assertTrue(introduced, audience)


if __name__ == '__main__':
    unittest.main()
