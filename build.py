#!/usr/bin/env python3
"""Build dependency-free, localized static pages for GitHub Pages."""
import argparse
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DEFAULT_URL = "https://ki-84.github.io/story_leaf_app/"
STORE_URL = "https://apps.apple.com/app/id6799618264"
PUBLIC_BOOK_IDS = ("pb-en-0732", "pb-en-0728", "pb-en-0708")
LOCALE_ORDER = ["ja", "en", "de", "es", "fr", "it", "nl", "pt-BR", "pt-PT", "ru", "uk", "pl", "tr", "ar", "hi", "ko", "zh-Hans", "zh-Hant", "th", "vi", "id", "ms"]


def escape(value):
    return html.escape(str(value), quote=True)


def script_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def render_card(book, summary, ui):
    title = escape(book["title"])
    return f'''<article class="book-card">
      <button class="book-cover" type="button" data-book="{book['id']}" aria-label="{escape(ui['read_sample'])}: {title}"><img src="../{book['cover']}" alt="{title}" width="960" height="{'640' if book['series'] == 'popo' else '960'}" loading="lazy"></button>
      <div class="book-meta" lang="en" dir="ltr"><span>LEVEL {book['level']}</span><span>{book['words']} WORDS</span></div>
      <h4 lang="en" dir="ltr">{title}</h4><p>{escape(summary)}</p>
      <button class="text-button" type="button" data-book="{book['id']}">{escape(ui['read_sample'])}<span aria-hidden="true">↗</span></button>
    </article>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_URL)
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/") + "/"
    assert urlparse(base_url).scheme in ("https", "http")
    output = ROOT / "public"
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    shutil.copytree(ROOT / "assets", output / "assets")
    for file in ("style.css", "app.js"):
        shutil.copyfile(ROOT / "src" / file, output / file)
    locales = {locale: json.loads((ROOT / "locales" / f"{locale}.json").read_text()) for locale in LOCALE_ORDER}
    books = json.loads((ROOT / "data/books.json").read_text())
    assert tuple(book["id"] for book in books) == PUBLIC_BOOK_IDS
    template = (ROOT / "src/index.html").read_text()
    for locale, ui in locales.items():
        fields = {key: escape(value) for key, value in ui.items() if isinstance(value, str)}
        fields.update(locale=locale, direction="rtl" if locale == "ar" else "ltr", store_url=STORE_URL,
                      canonical=base_url + locale + "/", base_url=base_url)
        fields["alternates"] = "\n  ".join(f'<link rel="alternate" hreflang="{loc}" href="{base_url}{loc}/">' for loc in LOCALE_ORDER)
        fields["alternates"] += f'\n  <link rel="alternate" hreflang="x-default" href="{base_url}">'
        fields["language_links"] = "".join('<a href="../{loc}/" lang="{loc}" hreflang="{loc}" dir="auto" {current}>{name}</a>'.format(loc=loc, current='aria-current="page"' if loc == locale else '', name=escape(locales[loc]['language_name'])) for loc in LOCALE_ORDER)
        assert len(ui["summaries"]) == len(books)
        cards = [render_card(book, summary, ui) for book, summary in zip(books, ui["summaries"])]
        fields["popo_cards"] = "\n".join(card for card, book in zip(cards, books) if book["series"] == "popo")
        fields["mallow_cards"] = "\n".join(card for card, book in zip(cards, books) if book["series"] == "mallow")
        fields["features"] = "".join(f'<div class="feature"><span aria-hidden="true">{icon}</span><div><h3>{escape(feature["title"])}</h3><p>{escape(feature["body"])}</p></div></div>' for icon, feature in zip(["♪", "Aa", "↗", "❧"], ui["features"]))
        fields["faqs"] = "".join(f'<details><summary>{escape(ui[f"q{i}"])}</summary><p>{escape(ui[f"a{i}"])}</p></details>' for i in (1, 2, 3))
        fields["site_data"] = script_json({"books": books, "ui": {key: ui[key] for key in ("listen", "pause", "page")}})
        fields["structured_data"] = script_json({"@context": "https://schema.org", "@type": "SoftwareApplication",
            "name": "Story Leaf", "operatingSystem": "iOS 17.0, iPadOS 17.0", "applicationCategory": "EducationalApplication",
            "url": base_url + locale + "/", "downloadUrl": STORE_URL, "inLanguage": locale,
            "description": ui["meta_description"], "image": base_url + "assets/icon-192.png",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "author": {"@type": "Person", "name": "Nobuaki Kuwabara"}})
        fields["credits_body"] = f'''<h3>Popo, Mumu &amp; Nemu / Mallow Town</h3><p>© 2026 Nobuaki Kuwabara. All rights reserved.</p>
          <p>{escape(ui['audio_notice'])} <a href="https://huggingface.co/Supertone/supertonic-3">Supertonic 3</a> / F1.</p>
          <h3>{escape(ui['real_screen'])}</h3><p lang="en">“A very tall man” — Written by Cornelius Gulere. Illustrated by Catherine Groenewald. Published by <a href="https://www.africanstorybook.org/">African Storybook (Saide)</a>. <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Text extracted and images resized for the app. Shown in an app screenshot.</p>
          <p><a href="https://ki-84.github.io/story_leaf_support/en/licenses.html">{escape(ui['credits'])} (English)</a></p>'''
        page = re.sub(r"\{\{([a-z_]+)\}\}", lambda match: fields[match[1]], template)
        assert "{{" not in page
        destination = output / locale
        destination.mkdir()
        (destination / "index.html").write_text(page, encoding="utf-8")
    # All content is available in rendered pages without JavaScript. Only the root
    # negotiates browser language; direct and shared locale URLs never redirect.
    links = "".join(f'<a href="{locale}/" lang="{locale}">{escape(ui["language_name"])}</a> ' for locale, ui in locales.items())
    root = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Story Leaf — Choose your language</title><meta name="description" content="English picture books. Original stories to read and listen to. Choose from 22 languages."><link rel="icon" href="assets/icon-64.png"><link rel="stylesheet" href="style.css"><link rel="canonical" href="BASE_URL"></head><body><main class="wrap" style="padding-block:60px"><a class="brand" href="en/">Story Leaf.</a><h1 style="margin-block:30px">Small stories. A growing world.</h1><nav class="language-grid" aria-label="Choose your language">LINKS</nav></main><script>
    (()=>{const supported=LOCALES;let saved;try{saved=localStorage.getItem('storyleaf-language')}catch(_){}function match(value){const code=value.toLowerCase();const exact=supported.find(x=>x.toLowerCase()===code);if(exact)return exact;if(code.startsWith('zh'))return /hant|tw|hk|mo/.test(code)?'zh-Hant':'zh-Hans';if(code.startsWith('pt'))return code==='pt-pt'?'pt-PT':'pt-BR';return supported.find(x=>x===code.split('-')[0]);}const preferred=supported.includes(saved)?saved:(navigator.languages||[navigator.language||'en']).map(match).find(Boolean)||'en';location.replace(new URL(preferred+'/',location.href).href+location.search+location.hash);})();
    </script></body></html>'''
    root = root.replace("BASE_URL", escape(base_url)).replace("LINKS", links).replace("LOCALES", script_json(LOCALE_ORDER))
    (output / "index.html").write_text(root)
    (output / "404.html").write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Story Leaf — Page not found</title><link rel="stylesheet" href="{base_url}style.css"><main class="wrap" style="padding-block:80px"><p>Story Leaf.</p><h1>Let's find your next story.</h1><p><a class="text-button" href="{base_url}">Choose your language ↗</a></p></main></html>''')
    (output / ".nojekyll").touch()
    (output / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base_url}sitemap.xml\n")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{base_url}{locale}/</loc></url>' for locale in [""] + LOCALE_ORDER) + '</urlset>\n'
    # The root uses the base URL, without an extra path separator.
    sitemap = sitemap.replace(base_url + "/", base_url)
    (output / "sitemap.xml").write_text(sitemap)
    print(f"Built {len(locales)} localized pages, {len(books)} books → {output}")


if __name__ == "__main__":
    main()
