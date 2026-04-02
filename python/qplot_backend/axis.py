# axis.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems

import math

from PyQt6.QtCore import QPointF


class Axis:
    """Maps between 1D data coordinates and 2D paper coordinates (points).

    For a horizontal axis, normally p0.y == p1.y == 0.
    For a vertical axis, normally p0.x == p1.x == 0.
    This allows the outputs of map() from a pair of axes to be simply added.
    """

    def __init__(self) -> None:
        self._x0: float = 0.0
        self._x1: float = 1.0
        self._p0: QPointF = QPointF(0.0, 0.0)
        self._p1: QPointF = QPointF(1.0, 0.0)
        self._recalc()

    def set_data_range(self, x0: float, x1: float) -> None:
        """Set the data coordinate range. If x1 <= x0, defaults to [0, 1]."""
        if x1 <= x0:
            self._x0 = 0.0
            self._x1 = 1.0
        else:
            self._x0 = x0
            self._x1 = x1
        self._recalc()

    def set_placement(self, p0: QPointF, p1: QPointF) -> None:
        """Set the paper coordinates (pt) corresponding to min and max data."""
        self._p0 = p0
        self._p1 = p1
        self._recalc()

    def min(self) -> float:
        """Minimum data coordinate."""
        return self._x0

    def max(self) -> float:
        """Maximum data coordinate."""
        return self._x1

    def minp(self) -> QPointF:
        """Paper coordinate (pt) of the minimum data value."""
        return self._p0

    def maxp(self) -> QPointF:
        """Paper coordinate (pt) of the maximum data value."""
        return self._p1

    def map(self, x: float) -> QPointF:
        """Map a data coordinate to a paper coordinate."""
        return self._porig + self._dp * x

    def maprel(self, dx: float) -> QPointF:
        """Map a relative data distance to a paper displacement."""
        return self._dp * dx

    def rev(self, p: QPointF) -> float:
        """Map a paper coordinate back to a data coordinate."""
        dp = p - self._p0
        dpa = self._p1 - self._p0
        phi = math.atan2(dpa.y(), dpa.x())
        length = math.sqrt(dpa.x() ** 2 + dpa.y() ** 2)
        dx = (dp.x() * math.cos(phi) + dp.y() * math.sin(phi)) / length
        return dx * (self._x1 - self._x0) + self._x0

    # --- Private ----------------------------------------------------------

    def _recalc(self) -> None:
        """Recompute cached mapping coefficients after any change."""
        scale = 1.0 / (self._x1 - self._x0)
        self._dp = QPointF(
            (self._p1.x() - self._p0.x()) * scale,
            (self._p1.y() - self._p0.y()) * scale,
        )
        self._porig = self._p0 - self._dp * self._x0
