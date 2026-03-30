# marker.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

import enum
from factor import pt2iu


class Marker:
    """Marker style: shape, fill, and radius."""

    class Type(enum.IntEnum):
        CIRCLE        = 0
        SQUARE        = 1
        DIAMOND       = 2
        LEFTTRIANGLE  = 3
        RIGHTTRIANGLE = 4
        UPTRIANGLE    = 5
        DOWNTRIANGLE  = 6
        PENTAGRAM     = 7
        HEXAGRAM      = 8
        PLUS          = 9
        CROSS         = 10
        HBAR          = 11
        VBAR          = 12
        STAR          = 13

    class Fill(enum.IntEnum):
        BRUSH  = 0
        OPEN   = 1
        CLOSED = 2
        SPINE  = 3

    def __init__(self) -> None:
        self.type:   Marker.Type = Marker.Type.CIRCLE
        self.fill:   Marker.Fill = Marker.Fill.CLOSED
        self.radius: float       = pt2iu(3)
