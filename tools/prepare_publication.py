"""Restrict the disposable CI checkout to the weeks cleared for publication.

Local previews retain every week. Never run this against an authoring checkout.
"""
import os
from pathlib import Path
import re
import shutil
import yaml

ROOT = Path(__file__).resolve().parents[1]
MAX_WEEK = 7


def allowed(path):
    match = re.search(r"(?:^|/)week(\d+)(?:/|$)", str(path))
    return not match or int(match[1]) <= MAX_WEEK


def filter_toc(entries):
    result = []
    for entry in entries:
        if not allowed(entry.get('file', '')):
            continue
        entry = dict(entry)
        if 'children' in entry:
            entry['children'] = filter_toc(entry['children'])
        result.append(entry)
    return result


def main():
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        raise SystemExit('Publication filtering is CI-only; local weeks are preserved.')
    path = ROOT / 'myst.yml'
    config = yaml.safe_load(path.read_text())
    config['project']['toc'] = filter_toc(config['project']['toc'])
    path.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True))
    for directory in (ROOT / 'notebooks').glob('week[0-9][0-9]'):
        if not allowed(directory.name):
            shutil.rmtree(directory)
    print(f'Publication limited to Weeks 0–{MAX_WEEK}; later weeks excluded from CI output.')


if __name__ == '__main__':
    main()
