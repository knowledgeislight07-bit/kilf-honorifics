#!/usr/bin/env python3
"""Build KILF Naskh: dist/KILFNaskh-Regular.ttf.

    .venv/bin/python build_naskh.py                                  # build the release
    .venv/bin/python build_naskh.py --scale 0.9 --out /tmp/test.ttf  # try a setting without touching dist/

Noto Naskh Arabic (sources/, SIL Open Font License) with EB Garamond's line metrics, for the
rare Arabic word or phrase inside English text: it never makes a line taller. Unlike build.py,
this keeps the whole font (its joining, ligature and mark-positioning tables) and changes only
the line metrics, the names and, optionally, the size. Use real Noto Naskh Arabic for Arabic
paragraphs, which need its taller line spacing. Bump VERSION and add an entry to FONTLOG.txt.
"""
import argparse
import pathlib

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.ttLib.scaleUpem import scale_upem

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "sources" / "NotoNaskhArabic-Regular.ttf"   # the font
METRICS = ROOT / "sources" / "eb-garamond" / "EBGaramond-Regular.ttf"       # line metrics
OUT = ROOT / "dist" / "KILFNaskh-Regular.ttf"

FAMILY = "KILF Naskh"
PS_NAME = "KILFNaskh-Regular"
VERSION = "1.001"   # bump on every release, and add a FONTLOG.txt entry
SCALE = 1.0         # glyph size relative to Noto; at 1.0 alif (0.67 em) is close to EB Garamond's ascender

# Arabic, Arabic Supplement, Arabic Extended-A (which holds Quranic marks), both presentation-form
# blocks (legacy text, and the honorifics), and the spaces, joiners, direction marks and
# punctuation that occur inside Arabic text. Rarer blocks (Extended-B and -C) are left out.
UNICODES = [
    *range(0x0600, 0x0700), *range(0x0750, 0x0780), *range(0x08A0, 0x0900),
    *range(0xFB50, 0xFE00), *range(0xFE70, 0xFF00),
    0x0020, 0x0021, 0x002C, 0x002E, *range(0x0030, 0x003B), 0x00A0, 0x00AB, 0x00BB,
    0x2009, *range(0x200B, 0x2011), 0x202F, 0x204F, 0x25CC, 0x2E41,
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", type=float, default=SCALE)
    ap.add_argument("--out", type=pathlib.Path, default=OUT)
    a = ap.parse_args()
    font = TTFont(SOURCE)
    met = TTFont(METRICS)
    upm = font["head"].unitsPerEm
    assert upm == met["head"].unitsPerEm == 1000

    opts = subset.Options()
    opts.layout_features = ["*"]        # keep every OpenType feature (joining, marks, ligatures, …)
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    opts.glyph_names = True
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=UNICODES)
    sub.subset(font)

    if a.scale != 1:
        # scale outlines, advances and GPOS together, then declare the old em: glyphs shrink or grow
        scale_upem(font, round(upm * a.scale))
        font["head"].unitsPerEm = upm

    h, o = met["hhea"], met["OS/2"]
    font["hhea"].ascent, font["hhea"].descent, font["hhea"].lineGap = h.ascent, h.descent, h.lineGap
    fo = font["OS/2"]
    fo.sTypoAscender, fo.sTypoDescender, fo.sTypoLineGap = o.sTypoAscender, o.sTypoDescender, o.sTypoLineGap
    fo.usWinAscent, fo.usWinDescent = o.usWinAscent, o.usWinDescent
    fo.sCapHeight, fo.sxHeight = o.sCapHeight, o.sxHeight   # Typst spaces lines from the cap height; 0 falls back to the ascender
    fo.fsSelection |= 1 << 7            # USE_TYPO_METRICS
    fo.achVendID = "KILF"
    font["head"].fontRevision = float(VERSION)

    name = font["name"]
    copyright_ = name.getDebugName(0)
    designer = name.getDebugName(9)
    name.names = []
    for nid, text in {
        0: f"{copyright_}. Line metrics changed 2026 by Knowledge Is Light Foundation.",
        1: FAMILY,
        2: "Regular",
        3: f"{FAMILY} Regular {VERSION}",
        4: f"{FAMILY} Regular",
        5: f"Version {VERSION}",
        6: PS_NAME,
        9: designer,
        13: "This Font Software is licensed under the SIL Open Font License, Version 1.1.",
        14: "https://openfontlicense.org",
    }.items():
        name.setName(text, nid, 3, 1, 0x409)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    font.save(a.out)
    f = TTFont(a.out)
    print(f"{a.out}: {FAMILY} {VERSION}, {len(f.getBestCmap())} characters, {len(f.getGlyphOrder())} glyphs, "
          f"{a.out.stat().st_size / 1024:.0f} KB; scale {a.scale}, line box {f['hhea'].ascent} / {f['hhea'].descent}")


if __name__ == "__main__":
    main()
