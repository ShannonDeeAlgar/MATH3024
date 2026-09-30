"""Check that numbered captions immediately follow media in the built Reader."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / '_build/html'


def text(node):
    return node.get('value', '') + ''.join(text(c) for c in node.get('children', []))


def has_media(node):
    if node.get('type') in {'image', 'img', 'video', 'iframe', 'embed'}:
        return not re.search(r'marker\.svg', str(node))
    return any(has_media(c) for c in node.get('children', []))


def check(root=ROOT):
    errors, total = [], 0

    def walk(node, page):
        nonlocal total
        children = node.get('children', [])
        for i, child in enumerate(children):
            label = re.match(r'^Figure\s+\d+\.\d+\.', text(child).strip())
            # Only the caption's paragraph/div, not its strong label or ancestor.
            if label and child.get('type') in {'paragraph', 'p', 'div'} and not has_media(child):
                total += 1
                if i == 0 or not has_media(children[i - 1]):
                    errors.append(f'{page}: {label[0]} is separated from its media')
            walk(child, page)

    for path in root.glob('*.json'):
        data = json.loads(path.read_text())
        if 'mdast' in data:
            walk(data['mdast'], path.name)
    if total == 0:
        errors.append('No numbered figure captions found; build the Reader first.')
    return total, errors


if __name__ == '__main__':
    total, errors = check()
    print(f'Checked {total} numbered figure captions.')
    for error in errors:
        print(error, file=sys.stderr)
    sys.exit(bool(errors))
