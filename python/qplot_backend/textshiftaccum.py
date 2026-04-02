# textshiftaccum.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems

import sys


class TextShiftAccum:
    """Accumulates incremental text position shifts from a base point."""

    def __init__(self) -> None:
        self._x:   float = 0.0
        self._y:   float = 0.0
        self._has: bool  = False
        self.reset()

    def reset(self) -> None:
        self._has = False

    def set_base(self, x: float, y: float) -> None:
        self._x = x
        self._y = y
        self._has = True

    def update(self, dx: float, dy: float) -> None:
        if not self._has:
            print("Warning: TextShiftAccum: update w/o base", file=sys.stderr)
            self.set_base(0.0, 0.0)
        self._x += dx
        self._y += dy

    def x(self) -> float:
        return self._x

    def y(self) -> float:
        return self._y

    def is_active(self) -> bool:
        return self._has
