# panel.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs withdul coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from PyQt6.QtCore import QRectF

from .axis import Axis


class Panel:
    """Holds the two axes and bounding boxes for one plot panel."""

    def __init__(self) -> None:
        self.xaxis:        Axis   = Axis()
        self.yaxis:        Axis   = Axis()
        self.desired_extent: QRectF = QRectF()
        self.fullbbox:     QRectF = QRectF()
        self.cumulbbox:    QRectF = QRectF()
        self.lastbbox:     QRectF = QRectF()
