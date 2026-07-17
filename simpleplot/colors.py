"""Colormaps and normalization for ``pcolormesh`` / mapped scatter.

Colormaps are lookup tables (256x3 uint8). ``viridis`` is stored as a small set
of anchor stops and linearly interpolated to 256 entries at import time to keep
the source compact while staying visually faithful.
"""

from __future__ import annotations

import numpy as np

# Viridis anchor stops at t = 0.0, 0.1, ... 1.0 (RGB 0-255).
_VIRIDIS_ANCHORS = np.array([
    [68, 1, 84], [72, 40, 120], [62, 74, 137], [49, 104, 142],
    [38, 130, 142], [31, 158, 137], [53, 183, 121], [110, 206, 88],
    [181, 222, 43], [221, 227, 24], [253, 231, 37],
], dtype=float)

# Plasma anchor stops.
_PLASMA_ANCHORS = np.array([
    [13, 8, 135], [84, 2, 163], [139, 10, 165], [185, 50, 137],
    [219, 92, 104], [244, 136, 73], [254, 188, 43], [240, 249, 33],
], dtype=float)


def _build_lut(anchors: np.ndarray, n: int = 256) -> np.ndarray:
    """Linearly interpolate anchor stops into an ``(n, 3)`` uint8 LUT."""
    m = anchors.shape[0]
    src = np.linspace(0.0, 1.0, m)
    dst = np.linspace(0.0, 1.0, n)
    lut = np.empty((n, 3), dtype=np.uint8)
    for c in range(3):
        lut[:, c] = np.round(np.interp(dst, src, anchors[:, c])).astype(np.uint8)
    return lut


_GRAY_LUT = np.repeat(np.linspace(0, 255, 256, dtype=np.uint8)[:, None], 3, axis=1)

_COLORMAPS = {
    "viridis": _build_lut(_VIRIDIS_ANCHORS),
    "plasma": _build_lut(_PLASMA_ANCHORS),
    "gray": _GRAY_LUT,
    "grey": _GRAY_LUT,
}


def get_cmap(name) -> np.ndarray:
    """Return a 256x3 uint8 LUT for ``name`` (or pass an LUT through)."""
    if isinstance(name, np.ndarray):
        return name
    try:
        return _COLORMAPS[name]
    except KeyError:
        raise ValueError(
            f"Unknown colormap {name!r}. Available: {sorted(_COLORMAPS)}"
        )


def available_colormaps():
    return sorted(_COLORMAPS)


class Normalize:
    """Linearly map data to [0, 1] using ``vmin``/``vmax``.

    Unset limits are inferred from the data on first use.
    """

    def __init__(self, vmin=None, vmax=None):
        self.vmin = vmin
        self.vmax = vmax

    def autoscale_none(self, A):
        A = np.asarray(A, dtype=float)
        if self.vmin is None:
            self.vmin = float(np.nanmin(A))
        if self.vmax is None:
            self.vmax = float(np.nanmax(A))

    def __call__(self, A):
        A = np.asarray(A, dtype=float)
        self.autoscale_none(A)
        span = self.vmax - self.vmin
        if span == 0:
            span = 1.0
        return (A - self.vmin) / span


def apply_colormap(A, lut, norm: Normalize) -> np.ndarray:
    """Map data array ``A`` to an RGBA uint8 array. NaNs become transparent."""
    normed = norm(A)
    finite = np.isfinite(normed)
    idx = np.clip(np.nan_to_num(normed) * (lut.shape[0] - 1), 0, lut.shape[0] - 1)
    idx = idx.astype(np.intp)
    rgb = lut[idx]
    alpha = np.where(finite, 255, 0).astype(np.uint8)
    return np.concatenate([rgb, alpha[..., None]], axis=-1)
