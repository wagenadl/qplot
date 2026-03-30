# groupdata.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QBrush, QFont, QPen

from .align import Align


class GroupData:
    """Style and layout state saved and restored across a group."""

    def __init__(self) -> None:
        self.bbox:       QRectF         = QRectF()
        self.pen:        QPen           = QPen()
        self.pen_name:   str            = ""
        self.brush:      QBrush         = QBrush()
        self.brush_name: str            = ""
        self.font:       QFont          = QFont()
        self.valign:     Align.VAlign   = Align.VAlign.TOP
        self.halign:     Align.HAlign   = Align.HAlign.LEFT
        self.reftext:    str            = ""
        self.hairline:   float          = 0.0
