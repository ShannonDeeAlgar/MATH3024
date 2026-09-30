"""Audit maths delimiters in the active Reader, including tables and captions."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'slides-only', 'remove-cell', 'archive-only', 'presenter-notes'}


def reader_sources():
    for name in re.findall(r'file: (\S+)', (ROOT / 'myst.yml').read_text()):
        path = ROOT / name
        if path.suffix == '.ipynb':
            for i, cell in enumerate(json.loads(path.read_text())['cells']):
                if cell['cell_type'] == 'markdown' and not EXCLUDED & set(cell.get('metadata', {}).get('tags', [])):
                    yield f"{name}:{cell.get('id', i)}", ''.join(cell.get('source', []))
        else:
            yield name, path.read_text()


def without_code(source):
    kept, fences = [], []
    for line in source.splitlines(keepends=True):
        fence = re.match(r'^\s*([`~]{3,})(.*)$', line)
        literal = bool(fences and fences[-1][1])
        if fence:
            marker, info = fence.groups()
            if fences and not info.strip() and marker[0] == fences[-1][0][0] and len(marker) >= len(fences[-1][0]):
                fences.pop()
            elif not literal:
                fences.append((marker, not info.lstrip().startswith('{')))
            if literal or (fences and fences[-1][1]):
                continue
        elif literal:
            continue
        kept.append(line)
    return re.sub(r'(?<!`)`(?!`)[^`\n]+`', '', ''.join(kept))


class ReaderMathFormattingTests(unittest.TestCase):
    def test_delimiters_and_html_contexts(self):
        for label, source in reader_sources():
            with self.subTest(source=label):
                source = without_code(source)
                self.assertEqual(len(re.findall(r'(?<!\\)\$', source)) % 2, 0,
                                 'Unpaired dollar delimiter')
                self.assertNotRegex(source, r'\(\(u_1,u_2\)\)',
                                    'Payoff pair needs math delimiters')
                for line in source.splitlines():
                    self.assertNotRegex(line, r'<(?:p|span|td|summary)[ >].*?(?<!\\)\$',
                                        'Math inside raw inline HTML may render literally')
                for expr in re.findall(r'(?<!\\)\$(?!\$)(.*?)(?<!\\)\$', source, re.S):
                    self.assertNotRegex(expr, r'\\[_^]', 'Escaped sub/superscript inside maths')


if __name__ == '__main__':
    unittest.main()
