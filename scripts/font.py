#!/usr/bin/env python3
"""Google Sans Flex, embedded into the SVG cards as a base64 data URI.

GitHub proxies README images through camo and renders them in an isolated
context, so an SVG can't fetch a webfont over the network. The only way to use
a non-system typeface is to inline it. `subset()` below produces the committed
`assets/fonts/google-sans-flex.woff2`; `face_css()` inlines it at build time.

Re-subset with:  python3 scripts/font.py
"""

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "assets" / "fonts" / "google-sans-flex.woff2"

FAMILY = "Google Sans Flex"
STACK = '"Google Sans Flex", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif'

# every character the cards can render, so the subset stays small
CHARS = (
    "".join(chr(c) for c in range(0x20, 0x7F))  # printable ASCII
    + "·—–→↗★☆…’‘“”×≥≤"
)


def face_css():
    """@font-face rule with the font inlined — safe inside GitHub's sandbox."""
    if not FONT.exists():
        return ""
    b64 = base64.b64encode(FONT.read_bytes()).decode()
    return (
        f"@font-face{{font-family:'{FAMILY}';"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2');"
        "font-weight:100 900;font-style:normal;font-display:block}"
    )


def subset():
    """Cut the downloaded latin face down to the glyphs the cards actually use."""
    from fontTools import subset as fts

    source = ROOT / "assets" / "fonts" / "google-sans-flex-latin.woff2"
    if not source.exists():
        raise SystemExit(f"missing source font: {source}")

    options = fts.Options()
    options.flavor = "woff2"
    options.layout_features = ["kern", "liga", "calt"]
    options.desubroutinize = False
    options.retain_gids = False
    options.drop_tables += ["DSIG"]

    font = fts.load_font(str(source), options)
    subsetter = fts.Subsetter(options=options)
    subsetter.populate(text=CHARS)
    subsetter.subset(font)
    FONT.parent.mkdir(parents=True, exist_ok=True)
    fts.save_font(font, str(FONT), options)
    print(f"subset {source.stat().st_size:,}B -> {FONT.stat().st_size:,}B "
          f"({len(CHARS)} chars) at {FONT}")


if __name__ == "__main__":
    subset()
