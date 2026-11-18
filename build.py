#!/usr/bin/env python3
"""Build KILF Honorifics: dist/KILFHonorifics-Regular.ttf.

    .venv/bin/python build.py                                        # build the release
    .venv/bin/python build.py --strength 0.5 --out /tmp/test.ttf     # try a setting without touching dist/

The font holds only the Arabic honorific ligatures (ﷺ ﵁ ﵂ ﵄ ﷻ …), taken from Noto Naskh Arabic
(sources/, SIL Open Font License), scaled to sit with EB Garamond, and given EB Garamond's line
metrics so it never makes a line taller (that matters in e-readers). Rerun after changing SCALE,
RAISE or STRENGTH, bump VERSION, and add an entry to FONTLOG.txt.
"""
import argparse
import pathlib

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.statisticsPen import StatisticsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.misc.timeTools import timestampNow
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "sources" / "NotoNaskhArabic-Regular.ttf"   # the glyphs
METRICS = ROOT / "sources" / "EBGaramond-Regular.ttf"       # line metrics and optical target
OUT = ROOT / "dist" / "KILFHonorifics-Regular.ttf"

FAMILY = "KILF Honorifics"
VERSION = "1.000"   # bump on every release, and add a FONTLOG.txt entry
SCALE = 0.85      # ﷺ then runs from just below the baseline to about EB Garamond's ascender
RAISE = 0         # vertical shift for every glyph, in font units (1000 = 1 em)
SIDE = 30         # extra space either side of each glyph, in font units

# every honorific ligature in Unicode
CODEPOINTS = [0xFDFA, 0xFDFB, 0xFDFE, 0xFDFF, 0xFDF2] + list(range(0xFD40, 0xFD50))

# Optical centring. Noto's raḍiya-llāhu ʿanhu family (﵁ ﵂ ﵄ …) carries most of its ink at or below the
# baseline, so beside English it looks sunk. Each glyph listed here is raised so that its ink centre
# moves toward the ink centre of EB Garamond text; STRENGTH 1 = all the way, 0 = not at all.
# ﷺ and the other tall ligatures already sit well and are left alone.
OPTICAL = range(0xFD40, 0xFD50)
STRENGTH = 0.75
SAMPLE = "the narrated Messenger said"   # English text whose ink centre is the target


def ink_centre(glyphset, glyph_name):
    p = StatisticsPen(glyphset=glyphset)
    glyphset[glyph_name].draw(p)
    return p.meanY


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strength", type=float, default=STRENGTH)
    ap.add_argument("--out", type=pathlib.Path, default=OUT)
    a = ap.parse_args()
    src = TTFont(SOURCE)
    met = TTFont(METRICS)
    upm = src["head"].unitsPerEm
    assert upm == met["head"].unitsPerEm == 1000
    cmap_src = src.getBestCmap()
    gs = src.getGlyphSet()
    mgs, mcmap = met.getGlyphSet(), met.getBestCmap()
    target = sum(ink_centre(mgs, mcmap[ord(c)]) for c in SAMPLE if c != " ") / len(SAMPLE.replace(" ", ""))

    order = [".notdef", "space"]
    glyphs = {".notdef": TTGlyphPen(None).glyph(), "space": TTGlyphPen(None).glyph()}
    widths = {".notdef": 500, "space": 250}
    cmap = {0x20: "space"}
    for cp in CODEPOINTS:
        if cp not in cmap_src:
            continue
        name = f"uni{cp:04X}"
        pen = TTGlyphPen(None)
        # decompose components, scale, and shift so the ink starts SIDE units from the origin
        bp = BoundsPen(gs)
        gs[cmap_src[cp]].draw(bp)
        x0 = bp.bounds[0]
        rec = DecomposingRecordingPen(gs)
        gs[cmap_src[cp]].draw(rec)
        lift = RAISE
        if cp in OPTICAL:
            lift += round((target - ink_centre(gs, cmap_src[cp]) * SCALE) * a.strength)
        rec.replay(TransformPen(pen, (SCALE, 0, 0, SCALE, SIDE - x0 * SCALE, lift)))
        glyphs[name] = pen.glyph()
        ink_w = (bp.bounds[2] - x0) * SCALE
        widths[name] = round(ink_w + 2 * SIDE)
        cmap[cp] = name
        order.append(name)

    fb = FontBuilder(upm, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    glyf = fb.font["glyf"]
    fb.setupHorizontalMetrics({g: (widths[g], getattr(glyf[g], "xMin", 0)) for g in order})
    h, o = met["hhea"], met["OS/2"]
    fb.setupHorizontalHeader(ascent=h.ascent, descent=h.descent, lineGap=h.lineGap)
    fb.setupOS2(
        sTypoAscender=o.sTypoAscender, sTypoDescender=o.sTypoDescender, sTypoLineGap=o.sTypoLineGap,
        usWinAscent=o.usWinAscent, usWinDescent=o.usWinDescent,
        usWeightClass=400, fsType=0, achVendID="KILF",
        ulUnicodeRange1=1 << 13, ulUnicodeRange2=1 << (63 - 32),   # Arabic, Arabic Presentation Forms-A
    )
    fb.setupNameTable({
        "familyName": FAMILY,
        "styleName": "Regular",
        "uniqueFontIdentifier": f"{FAMILY} Regular {VERSION}",
        "fullName": f"{FAMILY} Regular",
        "psName": "KILFHonorifics-Regular",
        "version": f"Version {VERSION}",
        "copyright": "Glyphs from Noto Naskh Arabic, Copyright 2022 The Noto Project Authors "
                     "(https://github.com/notofonts/arabic). Scaled and re-spaced 2026 by Knowledge Is Light Foundation.",
        "licenseDescription": "This Font Software is licensed under the SIL Open Font License, Version 1.1.",
        "licenseInfoURL": "https://openfontlicense.org",
    })
    fb.setupPost()
    fb.setupHead(unitsPerEm=upm, created=timestampNow(), modified=timestampNow())
    a.out.parent.mkdir(parents=True, exist_ok=True)
    fb.save(a.out)

    f = TTFont(a.out)
    print(f"{a.out}: {FAMILY} {VERSION}, {len(cmap) - 1} honorifics, {a.out.stat().st_size / 1024:.0f} KB; "
          f"English ink centre {target / upm:+.3f} em, optical strength {a.strength}")
    for cp in (0xFDFA, 0xFD41, 0xFD42, 0xFD44):
        bp = BoundsPen(f.getGlyphSet())
        f.getGlyphSet()[f"uni{cp:04X}"].draw(bp)
        c = ink_centre(f.getGlyphSet(), f"uni{cp:04X}")
        print(f"  {chr(cp)} U+{cp:04X}: ink {bp.bounds[1] / upm:+.2f} to {bp.bounds[3] / upm:+.2f} em, centre {c / upm:+.3f} em")


if __name__ == "__main__":
    main()
