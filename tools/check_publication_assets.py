"""Fail publication if required pages are missing or later weeks are staged."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit

EXPLORERS = {'aco_network_explorer.html', 'pso_explorer.html'}
PREFIX = '/MATH3024'


class Frames(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == 'iframe':
            self.sources.append(dict(attrs).get('src', ''))


def check(root):
    errors = []
    for path in root.rglob('*'):
        if re.search(r'(?:^|/)week(?:09|10)(?:/|\.|$)', str(path.relative_to(root))):
            errors.append(f'Unreleased material staged: {path.relative_to(root)}')
    required_pages = [
        'notebooks/week08/l-critical-phenomena/index.html',
        'slides/week08/L_Critical_phenomena.slides.html',
    ]
    for file in required_pages:
        if not (root / file).is_file():
            errors.append(f'Missing published page: {file}')
    pages = [
        ('notebooks/week07/l-intelligent-systems/index.html',
         ['notebooks/week07/l-intelligent-systems', 'notebooks/week07/l-intelligent-systems/']),
        ('slides/week07/L_Intelligent_systems.slides.html',
         ['slides/week07/L_Intelligent_systems.slides.html']),
    ]
    for file, routes in pages:
        page = root / file
        if not page.is_file():
            errors.append(f'Missing page: {file}')
            continue
        parser = Frames(); parser.feed(page.read_text())
        frames = [src for src in parser.sources if src.split('/')[-1] in EXPLORERS]
        if {src.split('/')[-1] for src in frames} != EXPLORERS:
            errors.append(f'Expected both ACO and PSO explorables in {file}')
        for route in routes:
            for src in frames:
                url = urljoin('https://shannondeealgar.github.io' + PREFIX + '/' + route, src)
                path = unquote(urlsplit(url).path)
                if not path.startswith(PREFIX + '/'):
                    errors.append(f'Explorable loses repository prefix: {url}')
                elif not (root / path[len(PREFIX)+1:]).is_file():
                    errors.append(f'Explorable target was not staged: {url}')
    return errors


if __name__ == '__main__':
    errors = check(Path(sys.argv[1] if len(sys.argv) > 1 else '_build/html'))
    if errors:
        raise SystemExit('\n'.join(errors))
    print('Week 8 reader and slides are present; Weeks 9–10 are absent; Week 7 explorables resolve under /MATH3024.')
