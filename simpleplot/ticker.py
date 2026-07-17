"""Tick location and label formatting ("nice numbers" 1-2-5 algorithm)."""

from __future__ import annotations

import math
from typing import List

import numpy as np


def nice_ticks(vmin: float, vmax: float, n: int = 5) -> np.ndarray:
    """Return ~``n`` evenly spaced "nice" tick locations within [vmin, vmax]."""
    if vmin == vmax:
        vmin, vmax = vmin - 0.5, vmax + 0.5
    if not (math.isfinite(vmin) and math.isfinite(vmax)):
        return np.array([vmin, vmax])

    span = vmax - vmin
    raw_step = span / max(n, 1)
    mag = 10 ** math.floor(math.log10(raw_step))
    norm = raw_step / mag
    # Snap to a nice multiple of the magnitude.
    if norm < 1.5:
        step = 1 * mag
    elif norm < 3:
        step = 2 * mag
    elif norm < 7:
        step = 5 * mag
    else:
        step = 10 * mag

    start = math.ceil(vmin / step) * step
    ticks = np.arange(start, vmax + step * 0.5, step)
    # Guard against float dust producing points just outside the range.
    ticks = ticks[(ticks >= vmin - step * 1e-6) & (ticks <= vmax + step * 1e-6)]
    return ticks


def log_ticks(vmin: float, vmax: float) -> np.ndarray:
    """Decade tick locations (powers of 10) spanning [vmin, vmax]."""
    if vmin <= 0:
        vmin = min(vmax / 1000.0, 1e-300) if vmax > 0 else 1e-3
    lo = math.floor(math.log10(vmin))
    hi = math.ceil(math.log10(vmax))
    if hi - lo > 12:  # avoid absurd counts for huge dynamic range
        exps = np.linspace(lo, hi, 12)
    else:
        exps = np.arange(lo, hi + 1)
    return np.power(10.0, exps)


def format_tick(v: float) -> str:
    """Format a tick value compactly (fixed or scientific as appropriate)."""
    if v == 0:
        return "0"
    av = abs(v)
    if av >= 1e5 or av < 1e-3:
        s = f"{v:.1e}"
        # Tidy "1.0e+03" -> "1e3".
        mant, exp = s.split("e")
        mant = mant.rstrip("0").rstrip(".")
        exp = int(exp)
        return f"{mant}e{exp}"
    s = f"{v:.6f}".rstrip("0").rstrip(".")
    return s


def format_ticks(values) -> List[str]:
    return [format_tick(float(v)) for v in values]
