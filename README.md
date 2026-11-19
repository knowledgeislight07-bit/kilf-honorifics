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

**KILF Garamond** is the one to use for English text: it's **EB Garamond with these honorifics built in**, in all eight styles (Regular, Italic, Medium, SemiBold and Bold, each with its italic). Text set in KILF Garamond needs no fallback font for the honorifics, so they can't come out in the wrong font, and the glyphs, sizes and centring are exactly those of KILF Honorifics. KILF Honorifics itself stays available on its own, for pairing with other typefaces.

A third font, **KILF Naskh**, covers the rarer case of a whole Arabic word or phrase inside English
text. It's Noto Naskh Arabic unchanged except for its line metrics, which come from EB Garamond, so
an Arabic word no longer makes its line taller. Plain and vocalised Arabic sits within EB Garamond's
line spacing; only stacked Quranic marks come close to the line above.

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

For Arabic words inside English text, add KILF Naskh after it: `("EB Garamond", "KILF Honorifics",
"KILF Naskh")` in Typst, and the same list in CSS with a second `@font-face` for
`dist/KILFNaskh-Regular.ttf`. Honorifics still come from KILF Honorifics; other Arabic falls through
to KILF Naskh. In EPUB, wrap the Arabic in `<span lang="ar">` with `font-family: "KILF Naskh"`. The
gain is largest in browsers and EPUB readers: in a test at 24 px, a line holding Arabic in Noto Naskh
grew by 10 px, and by nothing in KILF Naskh. Typst spaces lines by cap height and baseline, so it
was less affected to begin with.

Arabic paragraphs should keep a real Arabic font such as Noto Naskh Arabic, with its taller line
spacing and its own honorifics drawn to match.

## KILF Garamond
Use it in place of EB Garamond:
- **Typst:** `#set text(font: "KILF Garamond")`, with `dist/` on the font path.
- **CSS / EPUB:** embed `dist/KILFGaramond-Regular.ttf`, `-Italic` and `-SemiBold` (or whichever styles you use) as `font-family: "KILF Garamond"`. It's still worth wrapping honorifics in a span with an `aria-label`, so screen readers say them properly.

It's built by `build_garamond.py`, from the EB Garamond styles in `sources/eb-garamond/` and the current `dist/KILFHonorifics-Regular.ttf`. Rebuild it whenever KILF Honorifics changes:
```bash
.venv/bin/python build.py && .venv/bin/python build_garamond.py
```

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

KILF Naskh is built separately, by `build_naskh.py`, which writes `dist/KILFNaskh-Regular.ttf`.
It keeps all of Noto's joining, ligature and mark-positioning rules, and only changes the line
metrics and names. Its one setting, `SCALE` (default 1.0), resizes the glyphs; try one with
`.venv/bin/python build_naskh.py --scale 0.9 --out /tmp/test.ttf`.

To use other glyph designs (for example, commissioned calligraphy), replace `sources/NotoNaskhArabic-Regular.ttf` with a font that has the same code points.

## Releasing
1. Change the settings or sources, and run `build.py` (or `build_naskh.py` for KILF Naskh).
2. Bump `VERSION` in that script (it goes into the font's name table) and add an entry to `FONTLOG.txt`.
3. Commit the font in `dist/` along with the change, and tag the release. Each font has its own
   version, so its own tags: `v1.001` for KILF Honorifics, `naskh-v1.001` for KILF Naskh, `garamond-v1.000` for KILF Garamond.
4. Push the commit and tag, and make a GitHub release from the tag with the font attached:
   `gh release create naskh-v1.001 --title "KILF Naskh 1.001" dist/KILFNaskh-Regular.ttf`.
5. Copy the new font from `dist/` into each project that uses it. For the publications, that's `fazail/template/fonts/`.

## Layout
```
build.py        builds KILF Honorifics
build_naskh.py  builds KILF Naskh
build_garamond.py  builds KILF Garamond (EB Garamond + the honorifics)
dist/           the released fonts
sources/        Noto Naskh Arabic (honorific glyphs) and EB Garamond (all styles, in eb-garamond/), with their licences
OFL.txt         licence for all three fonts
FONTLOG.txt     changes, version by version
```
