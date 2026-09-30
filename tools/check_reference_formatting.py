"""Check all generated Reader citation records, including repeat appearances.

This flags metadata for review, never blindly title-cases names or paper titles.
DOI-specific corrections belong in course_references.bib, not generated HTML.
"""
import argparse
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def check(root):
    errors, dois, count = [], set(), 0
    for path in sorted(root.glob('*.json')):
        data = json.loads(path.read_text())
        if not isinstance(data, dict) or not isinstance(data.get('references'), dict):
            continue
        records = data['references'].get('cite', {}).get('data', {})
        if not isinstance(records, dict):
            continue
        for key, record in records.items():
            count += 1
            doi = record.get('doi', key).lower()
            dois.add(doi)
            markup = record.get('html', '')
            text = html.unescape(re.sub(r'<[^>]+>', '', markup))
            authors = re.split(r'\((?:\d{4}|n\.d\.)', text, maxsplit=1)[0]
            if re.search(r'\b[A-Z][A-Z-]+,\s*[A-Z]\.', authors):
                errors.append(f'{path.name}: all-capital personal name: {text}')
            if '(n.d.)' in text:
                errors.append(f'{path.name}: undated scholarly reference: {text}')
            if re.search(r'\(\d{4}\)\.\s*<i>', markup) and '(Ed' not in authors:
                errors.append(f'{path.name}: missing article title: {text}')
            if re.search(r'\(\d{4}\)\.\s*[–—-]', text):
                errors.append(f'{path.name}: damaged title: {text}')
            if '\\' in text or '<mml:' in markup:
                errors.append(f'{path.name}: unrendered reference markup: {text}')
            if doi == '10.1038/246015a0' and not text.startswith('Maynard Smith, J., & Price, G. R.'):
                errors.append(f'{path.name}: restore Maynard Smith family name: {text}')
    if not count:
        errors.append('No rendered citation records found; build the Reader first.')
    return errors, count, len(dois)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=ROOT / '_build/html')
    args = parser.parse_args()
    errors, count, unique = check(args.root)
    print(f'Checked {count} reference appearances ({unique} unique records).')
    if errors:
        raise SystemExit('\n'.join(errors))
    print('No capitalised personal names, missing dates/titles or raw reference markup found.')
