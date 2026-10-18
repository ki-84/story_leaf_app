#!/usr/bin/env python3
"""Check the generated locale routes, metadata, previews and narration assets."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

from build import LOCALE_ORDER, PUBLIC_BOOK_IDS, script_json

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.metadata = {}
        self.scripts = {}
        self.active_script = None
        self.heading_count = 0
        self.lang = None
        self.direction = None
        self.alternates = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang, self.direction = a.get("lang"), a.get("dir")
        if tag == "h1":
            self.heading_count += 1
        if "id" in a:
            assert a["id"] not in self.ids, f"Duplicate id {a['id']}"
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if key in a:
                self.links.append(a[key])
        if tag == "img":
            assert "alt" in a and "width" in a and "height" in a
        if tag == "meta":
            self.metadata[a.get("name", a.get("property"))] = a.get("content")
        if tag == "link" and a.get("rel") == "alternate":
            self.alternates.add(a.get("hreflang"))
        if tag == "script" and not a.get("src"):
            self.active_script = a.get("id", a.get("type"))
            self.scripts[self.active_script] = ""

    def handle_data(self, text):
        if self.active_script:
            self.scripts[self.active_script] += text

    def handle_endtag(self, tag):
        if tag == "script":
            self.active_script = None


def main():
    assert PUBLIC.is_dir(), "Run build.py first"
    books = json.loads((ROOT / "data/books.json").read_text())
    manifest = json.loads((ROOT / "data/audio-manifest.json").read_text())
    assert tuple(book['id'] for book in books) == PUBLIC_BOOK_IDS
    assert all(book['license'] == 'All Rights Reserved' for book in books)
    assert sum(len(book['pages']) for book in books) == len(manifest) == 12
    for root in (ROOT, PUBLIC):
        for kind in ('books', 'audio'):
            assert {p.name for p in (root / 'assets' / kind).iterdir() if p.is_dir()} == set(PUBLIC_BOOK_IDS), f'Unexpected published assets in {root}/assets/{kind}'
    expected_audio = {p['audio'] for b in books for p in b['pages']}
    assert set(manifest) == expected_audio
    for book in books:
        for page in book['pages']:
            audio = PUBLIC / page['audio']
            assert audio.stat().st_size > 2000
            entry = manifest[page['audio']]
            assert entry['text'] == page['text']
            assert entry['sha256'] == hashlib.sha256(audio.read_bytes()).hexdigest()
            assert 1 < entry['duration'] < 60
    for locale in LOCALE_ORDER:
        source = (PUBLIC / locale / "index.html")
        content = source.read_text()
        assert "{{" not in content
        assert 'href="../style.css"' not in content, 'Styles must have versioned filenames to avoid stale layouts'
        assert 'class="book-grid collection-grid"' in content
        assert content.count('class="book-card"') == len(PUBLIC_BOOK_IDS)
        page = Page()
        page.feed(content)
        assert page.lang == locale
        assert page.direction == ('rtl' if locale == 'ar' else 'ltr')
        assert page.heading_count == 1
        assert page.alternates == set(LOCALE_ORDER) | {"x-default"}
        assert page.metadata['description'] and page.metadata['og:image']
        assert 'app-id=6799618264' == page.metadata['apple-itunes-app']
        data = json.loads(page.scripts['site-data'])
        assert data['books'] == books
        assert json.loads(page.scripts['application/ld+json'])['downloadUrl'].endswith('id6799618264')
        for target in page.links:
            parsed = urlparse(target)
            if parsed.scheme or parsed.netloc:
                continue
            if parsed.path:
                asset = (source.parent / unquote(parsed.path)).resolve()
                assert asset.is_relative_to(PUBLIC.resolve()), f"Escaping URL {target}"
                assert asset.exists(), f"Missing {locale}: {target}"
            elif parsed.fragment:
                assert unquote(parsed.fragment) in page.ids, f"Missing anchor {target}"
        for book in books:
            for entry in [book['cover']] + [p['image'] for p in book['pages']]:
                assert (PUBLIC / entry).is_file()
    sitemap = ET.parse(PUBLIC / 'sitemap.xml')
    assert len(sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')) == 23
    assert '\\u003c' in script_json({'text':'</script>'})
    print('PASS: 22 locales, all links/assets, SEO metadata, only 3 approved books and 12 matching audio files')


if __name__ == '__main__':
    main()
