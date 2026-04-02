# range.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems

import math


class Range:
    """Tracks the min/max extent of a set of values.
    An empty Range has no values added yet."""

    def __init__(self, x: float = None, y: float = None):
        if x is None:
            self._empty = True
            self._min = self._max = 0.0
        else:
            self._empty = False
            self._min = self._max = x
            if y is not None:
                self.extend(y)

    def empty(self) -> bool:
        return self._empty

    def min(self) -> float:
        return self._min

    def max(self) -> float:
        return self._max

    def extend(self, x: float) -> None:
        """Expand the range to include x. NaN values are ignored."""
        if math.isnan(x):
            return
        if self._empty:
            self._min = self._max = x
            self._empty = False
        elif x < self._min:
            self._min = x
        elif x > self._max:
            self._max = x

    def unionize(self, other: "Range") -> None:
        """Expand this range to also cover other."""
        if other._empty:
            return
        if self._empty:
            self._min = other._min
            self._max = other._max
            self._empty = False
        else:
            if other._min < self._min:
                self._min = other._min
            if other._max > self._max:
                self._max = other._max

    def intersect(self, other: "Range") -> None:
        """Shrink this range to only the overlap with other."""
        if self._empty:
            return
        if other._empty:
            self._empty = True
        else:
            if other._min > self._min:
                self._min = other._min
            if other._max < self._max:
                self._max = other._max
            if self._min > self._max:
                self._empty = True

    def contains(self, x: float) -> bool:
        if self._empty:
            return False
        return self._min <= x <= self._max

    def range(self) -> float:
        """Returns the span (max - min), or 0 for an empty range."""
        if self._empty:
            return 0.0
        return self._max - self._min
