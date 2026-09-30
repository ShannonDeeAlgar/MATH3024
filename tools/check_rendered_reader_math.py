"""After a Reader build, flag literal TeX and renderer errors in its pages."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / '_build/html'
LITERAL_MATH = re.compile(
    r'\\(?:frac|mathrm|mathbf|displaystyle|sum|mathcal|begin|leq|geq)\b'
    r'|\$[^$\n]+\$|\(\(u_1,u_2\)\)')


def check(root=ROOT):
    errors, counts = [], {'pages': 0, 'math': 0}

    def walk(node, page):
        if not isinstance(node, dict):
            return
        kind = node.get('type')
        if kind in ('math', 'inlineMath'):
            counts['math'] += 1
        if kind == 'text' and LITERAL_MATH.search(node.get('value', '')):
            errors.append(f"{page}: literal math in ordinary text: {node['value'][:180]}")
        for child in node.get('children', []):
            walk(child, page)

    for path in root.glob('*.json'):
        data = json.loads(path.read_text())
        if 'mdast' in data:
            counts['pages'] += 1
            walk(data['mdast'], path.name)
    for path in (root / 'notebooks').rglob('index.html'):
        if re.search(r'class=["\'][^"\']*\bkatex-error\b', path.read_text()):
            errors.append(f'{path.relative_to(root)}: KaTeX rendering error')
    if not counts['pages'] or not counts['math']:
        errors.append('No built Reader mathematics found; build the Reader first.')
    return counts, errors


if __name__ == '__main__':
    counts, errors = check()
    print(f"Checked {counts['pages']} pages and {counts['math']} math nodes.")
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print('No literal TeX or KaTeX rendering errors found.')
    sys.exit(bool(errors))
