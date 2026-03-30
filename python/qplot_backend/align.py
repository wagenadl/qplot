# align.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

import enum


class Align:
    class HAlign(enum.IntEnum):
        LEFT   = 0
        CENTER = 1
        RIGHT  = 2

    class VAlign(enum.IntEnum):
        TOP    = 0
        MIDDLE = 1
        BOTTOM = 2
        BASE   = 3
