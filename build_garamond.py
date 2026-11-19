#!/usr/bin/env python3
"""Build KILF Garamond: EB Garamond with the KILF honorifics built in. Writes dist/KILFGaramond-*.ttf.

    .venv/bin/python build.py            # first, if KILF Honorifics changed
    .venv/bin/python build_garamond.py

Each EB Garamond style in sources/eb-garamond/ gets the 21 honorific ligatures (ﷺ ﵁ ﵂ ﵄ …) from
dist/KILFHonorifics-Regular.ttf, unchanged: same outlines, sizes, optical centring and spacing.
Everything else is EB Garamond's, untouched. The family is renamed (the OFL requires a new name
for a modified font), so text set in KILF Garamond needs no fallback font for the honorifics.
Bump VERSION and add a FONTLOG.txt entry on every release.
"""
import copy
import pathlib

from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent
SOURCES = ROOT / "sources" / "eb-garamond"
HONORIFICS = ROOT / "dist" / "KILFHonorifics-Regular.ttf"
DIST = ROOT / "dist"

FAMILY = "KILF Garamond"
PS_FAMILY = "KILFGaramond"
VERSION = "1.000"   # bump on every release, and add a FONTLOG.txt entry

# name records that carry the family name (the rest, such as copyright, designer and licence, are kept)
NAME_IDS = (1, 3, 4, 6, 16, 17, 18, 21, 22, 25)


def merge(src_path, hon):
    font = TTFont(src_path)
    upm = font["head"].unitsPerEm
    assert upm == hon["head"].unitsPerEm, "unitsPerEm must match"
    hon_glyf, hon_hmtx = hon["glyf"], hon["hmtx"]
    glyf, hmtx = font["glyf"], font["hmtx"]
    order = list(font.getGlyphOrder())
    cmaps = [t for t in font["cmap"].tables if t.isUnicode()]
    added = 0
    for cp, gname in sorted(hon.getBestCmap().items()):
        if cp == 0x20:
            continue
        if cp in font.getBestCmap():
            raise SystemExit(f"{src_path.name} already has U+{cp:04X}; refusing to overwrite it")
        new = f"kilf.{gname}"
        g = hon_glyf[gname]
        g.expand(hon_glyf)
        glyf.glyphs[new] = copy.deepcopy(g)
        hmtx.metrics[new] = hon_hmtx[gname]
        order.append(new)
        for t in cmaps:
            t.cmap[cp] = new
        added += 1
    font.setGlyphOrder(order)
    glyf.setGlyphOrder(order)
    for tag in ("hdmx", "LTSH", "VDMX", "DSIG"):   # per-glyph caches that would go stale
        if tag in font:
            del font[tag]

    name = font["name"]
    for rec in name.names:
        if rec.nameID in NAME_IDS:
            s = rec.toUnicode()
            s = s.replace("EB Garamond", FAMILY).replace("EBGaramond", PS_FAMILY)
            rec.string = s
        elif rec.nameID == 0:
            rec.string = (rec.toUnicode() + ". Honorific glyphs from KILF Honorifics (Noto Naskh Arabic, "
                          "Copyright 2022 The Noto Project Authors). Modified 2026 by Knowledge Is Light Foundation.")
        elif rec.nameID == 5:
            rec.string = f"Version {VERSION}; {FAMILY}, from EB Garamond {rec.toUnicode().split()[1].rstrip(';')}"
        elif rec.nameID == 7:   # trademark notice of the original, if any
            rec.string = ""
    name.names = [r for r in name.names if r.toUnicode() != ""]
    font["head"].fontRevision = float(VERSION)
    os2 = font["OS/2"]
    os2.achVendID = "KILF"
    os2.ulUnicodeRange2 |= 1 << (63 - 32)   # Arabic Presentation Forms-A
    return font, added


def main():
    hon = TTFont(HONORIFICS)
    DIST.mkdir(exist_ok=True)
    for src in sorted(SOURCES.glob("EBGaramond-*.ttf")):
        font, added = merge(src, hon)
        out = DIST / src.name.replace("EBGaramond", PS_FAMILY)
        font.save(out)
        f = TTFont(out)
        print(f"{out.relative_to(ROOT)}: {f['name'].getDebugName(4)}, +{added} honorifics, "
              f"{len(f.getGlyphOrder())} glyphs, {out.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
