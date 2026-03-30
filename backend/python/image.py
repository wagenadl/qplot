# image.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

import numpy as np
from PyQt6.QtGui import QImage


def _to_byte(v: np.ndarray) -> np.ndarray:
    """Clamp float values in [0,1] and convert to uint8."""
    return np.clip(v * 255.999, 0, 255).astype(np.uint8)


def build(X: int, Y: int, C: int, cdata: list[float]) -> QImage:
    """Build a QImage from normalised float data in [0.0, 1.0].

    Args:
        X:     image width in pixels
        Y:     image height in pixels
        C:     number of channels (1=grey, 2=grey+alpha, 3=RGB, 4=RGBA)
        cdata: flat list of floats, length X*Y*C, in row-major order

    Returns:
        QImage in ARGB32 format
    """
    assert len(cdata) == X * Y * C

    src = np.array(cdata, dtype=np.float64).reshape(Y, X, C)

    # Output buffer: Y rows, X cols, 4 bytes per pixel (B, G, R, A)
    dst = np.empty((Y, X, 4), dtype=np.uint8)

    if C == 1:
        grey = _to_byte(src[:, :, 0])
        dst[:, :, 0] = grey   # B
        dst[:, :, 1] = grey   # G
        dst[:, :, 2] = grey   # R
        dst[:, :, 3] = 255    # A

    elif C == 2:
        grey = _to_byte(src[:, :, 0])
        dst[:, :, 0] = grey                      # B
        dst[:, :, 1] = grey                      # G
        dst[:, :, 2] = grey                      # R
        dst[:, :, 3] = _to_byte(src[:, :, 1])   # A

    elif C == 3:
        dst[:, :, 0] = _to_byte(src[:, :, 2])   # B ← channel 2
        dst[:, :, 1] = _to_byte(src[:, :, 1])   # G ← channel 1
        dst[:, :, 2] = _to_byte(src[:, :, 0])   # R ← channel 0
        dst[:, :, 3] = 255                       # A

    elif C == 4:
        dst[:, :, 0] = _to_byte(src[:, :, 2])   # B ← channel 2
        dst[:, :, 1] = _to_byte(src[:, :, 1])   # G ← channel 1
        dst[:, :, 2] = _to_byte(src[:, :, 0])   # R ← channel 0
        dst[:, :, 3] = _to_byte(src[:, :, 3])   # A ← channel 3

    else:
        raise ValueError(f"Unsupported channel count: {C}")

    raw = dst.tobytes()
    return QImage(raw, X, Y, 4 * X, QImage.Format.Format_ARGB32)
