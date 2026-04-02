# slightly.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems

import math


def slightly_less(x: float) -> float:
    """Return the largest representable float strictly less than x."""
    return math.nextafter(x, -math.inf)


def slightly_more(x: float) -> float:
    """Return the smallest representable float strictly greater than x."""
    return math.nextafter(x, math.inf)
