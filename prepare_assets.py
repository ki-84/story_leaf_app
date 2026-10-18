#!/usr/bin/env python3
"""Refresh approved book excerpts from the local app checkout (not needed by Pages)."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
APP = ROOT.parent.parent
BOOKS = [
    ("pb-en-0732", "popo"), ("pb-en-0728", "popo"),
    ("pb-en-0708", "mallow"),
]


def main():
    books = []
    for book_id, series in BOOKS:
        folder = APP / "content/books" / book_id
        book = json.loads((folder / "book.json").read_text())
        assert book["source"] == "original"
        destination = ROOT / "assets/books" / book_id
        destination.mkdir(parents=True, exist_ok=True)
        pages = []
        for i, page in enumerate(book["pages"][:4]):
            output = destination / f"{i + 1:02}.webp"
            with Image.open(folder / page["imagePath"]) as image:
                image.thumbnail((960, 960))
                image.convert("RGB").save(output, "WEBP", quality=88, method=6)
            pages.append({"image": f"assets/books/{book_id}/{output.name}",
                          "text": page["text"],
                          "audio": f"assets/audio/{book_id}/{i + 1:02}.mp3"})
        with Image.open(folder / book["coverImagePath"]) as image:
            image.thumbnail((960, 960))
            image.convert("RGB").save(destination / "cover.webp", "WEBP", quality=90, method=6)
        books.append({"id": book_id, "title": book["title"], "series": series,
                      "level": book["level"], "words": book["wordCount"],
                      "cover": f"assets/books/{book_id}/cover.webp", "pages": pages,
                      "author": book["attribution"]["author"],
                      "license": book["attribution"]["license"],
                      "source_sha256": hashlib.sha256((folder / "book.json").read_bytes()).hexdigest()})
    (ROOT / "data/books.json").write_text(json.dumps(books, ensure_ascii=False, indent=2) + "\n")
    with Image.open(APP / "app/StoryLeaf/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png") as image:
        for size in (64, 192):
            image.resize((size, size)).save(ROOT / f"assets/icon-{size}.png")
    # A representative real app screen, localized in every supported language.
    for locale in (APP / "app/fastlane/metadata_src").glob("*.json"):
        source = APP / "app/fastlane/screenshots_raw" / locale.stem / "iphone-4_dictionary.png"
        with Image.open(source) as image:
            image.thumbnail((480, 1100))
            image.convert("RGB").save(ROOT / "assets/screenshots" / f"{locale.stem}.webp", "WEBP", quality=84)
    print(f"Prepared {len(books)} original-book excerpts and 22 localized screenshots")


if __name__ == "__main__":
    main()
