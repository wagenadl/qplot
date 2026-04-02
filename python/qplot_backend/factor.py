# factor.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems

_FACTOR: float = 30.0
"""Conversion factor between PostScript points and internal units.
Should only be set by main.py via set_factor()."""


def pt2iu(x_pt: float = 1.0) -> float:
    """Convert PostScript points to internal units."""
    return _FACTOR * x_pt


def iu2pt(x_iu: float = 1.0) -> float:
    """Convert internal units to PostScript points."""
    return x_iu / _FACTOR


def set_factor(x: float) -> None:
    """Set the conversion factor. For use by main.py only."""
    global _FACTOR
    _FACTOR = x
