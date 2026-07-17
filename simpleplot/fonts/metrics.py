"""Helvetica advance-width table (units per 1000 em), AFM-derived.

Only the metric matters for layout: we place ``<text>`` and let the renderer
draw glyphs. ``text_width`` estimates a string's rendered width so labels can be
centered / right-aligned and margins sized.
"""

from __future__ import annotations

# Base widths for punctuation and symbols.
_W = {
    " ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667,
    "'": 191, "(": 333, ")": 333, "*": 389, "+": 584, ",": 278, "-": 333,
    ".": 278, "/": 278, ":": 278, ";": 278, "<": 584, "=": 584, ">": 584,
    "?": 556, "@": 1015, "[": 278, "\\": 278, "]": 278, "^": 469, "_": 556,
    "`": 333, "{": 334, "|": 260, "}": 334, "~": 584,
}
# Digits are all 556 in Helvetica.
for _d in "0123456789":
    _W[_d] = 556
# Uppercase letters.
for _c, _w in zip(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    (667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833,
     722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611),
):
    _W[_c] = _w
# Lowercase letters.
for _c, _w in zip(
    "abcdefghijklmnopqrstuvwxyz",
    (556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833,
     556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500),
):
    _W[_c] = _w

_DEFAULT = 556  # fallback for anything not in the table


def text_width(text: str, font_size: float) -> float:
    """Estimated rendered width of ``text`` in pixels at ``font_size`` px."""
    units = sum(_W.get(ch, _DEFAULT) for ch in text)
    return units / 1000.0 * font_size
