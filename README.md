# KILF Honorifics

A small companion font of the Arabic honorific ligatures (ﷺ ﵁ ﵂ ﵄ …) for English text, designed
to sit beside **EB Garamond**. It's maintained by Knowledge Is Light Foundation (KILF) and used in
its publications, and released separately so every book, website and document can share one
version.

- **Glyphs:** from Noto Naskh Arabic, which is compact enough for a Latin line. Scheherazade New's honorifics, by contrast, are drawn tall.
- **Sized for EB Garamond:** ﷺ runs from just below the baseline to about the ascender.
- **Optically centred:** the bottom-heavy raḍiya-llāhu ʿanhu family is raised so it doesn't look sunk beside English text.
- **EB Garamond's line metrics:** the font never makes a line taller, in print or in EPUB readers.
- **Licence:** SIL Open Font License 1.1 (`OFL.txt`).

## The glyphs

| Glyph | Code point | Meaning |
|---|---|---|
| ﷺ | U+FDFA | ṣalla-llāhu ʿalayhi wa sallam |
| ﵁ | U+FD41 | raḍiya-llāhu ʿanhu |
| ﵂ | U+FD42 | raḍiya-llāhu ʿanhā |
| ﵄ | U+FD44 | raḍiya-llāhu ʿanhumā |
| ﵃ | U+FD43 | raḍiya-llāhu ʿanhum |
| ﵅ | U+FD45 | raḍiya-llāhu ʿanhunna |
| ﵀ | U+FD40 | raḥimahu-llāh |
| ﵏ | U+FD4F | raḥimahumu-llāh |
| ﵇ | U+FD47 | ʿalayhi-s-salām |
| ﵈ | U+FD48 | ʿalayhimu-s-salām |
| ﵉ | U+FD49 | ʿalayhimā-s-salām |
| ﵍ | U+FD4D | ʿalayhā-s-salām |
| ﵊ | U+FD4A | ʿalayhi-ṣ-ṣalātu wa-s-salām |
| ﵆ ﵌ | U+FD46, U+FD4C | ṣalla-llāhu ʿalayhi wa-ālih (wa sallam) |
| ﵋ | U+FD4B | quddisa sirruh |
| ﵎ | U+FD4E | tabāraka wa taʿālā |
| ﷻ | U+FDFB | jalla jalāluh |
| ﷾ | U+FDFE | subḥānahu wa taʿālā |
| ﷿ | U+FDFF | ʿazza wa jall |
| ﷲ | U+FDF2 | Allāh |

## Using it
The font has no Latin letters. List it **after** your text font, so it is used only for the honorifics:

- **Typst:** `#set text(font: ("EB Garamond", "KILF Honorifics"))`, with `dist/` on the font path.
- **CSS / EPUB:** embed `dist/KILFHonorifics-Regular.ttf` with `@font-face { font-family: "KILF Honorifics"; src: url(KILFHonorifics-Regular.ttf); }`. For EPUB, also wrap each honorific in a span whose `font-family` is set to it, so readers that swap the body font still show it: `<span class="hon" role="img" aria-label="raḍiya-llāhu ʿanhu">﵁</span>`.
- **Word processors:** install the font. EB Garamond will fall back to it for these characters on most systems; if not, set them in KILF Honorifics by hand.

Arabic text should keep its own Arabic font, which has its own honorifics drawn to match.

## Building
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python build.py                                       # writes dist/KILFHonorifics-Regular.ttf
.venv/bin/python build.py --strength 0.5 --out /tmp/test.ttf    # try a setting without touching dist/
```
The settings are at the top of `build.py`:
- `SCALE`: glyph size.
- `RAISE`: shifts every glyph up or down.
- `STRENGTH`: how strongly the raḍiya family is optically centred (0 = not at all, 1 = fully).
- `SIDE`: spacing either side of each glyph.

To use other glyph designs (for example, commissioned calligraphy), replace `sources/NotoNaskhArabic-Regular.ttf` with a font that has the same code points.

## Releasing
1. Change the settings or sources, and run `build.py`.
2. Bump `VERSION` in `build.py` (it goes into the font's name table) and add an entry to `FONTLOG.txt`.
3. Commit `dist/KILFHonorifics-Regular.ttf` along with the change, and tag the release (e.g. `v1.001`).
4. Copy the new `dist/KILFHonorifics-Regular.ttf` into each project that uses it. For the publications, that's `fazail/template/fonts/`.

## Layout
```
build.py        builds the font
dist/           the released font
sources/        Noto Naskh Arabic (glyphs) and EB Garamond (metrics), with their licences
OFL.txt         licence for KILF Honorifics
FONTLOG.txt     changes, version by version
```
