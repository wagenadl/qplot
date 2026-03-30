# rotate.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

import math
from PyQt6.QtCore import QPointF, QRectF


def rotate_point(p: QPointF, phi_rad: float) -> QPointF:
    c, s = math.cos(phi_rad), math.sin(phi_rad)
    return QPointF(
        p.x() * c - p.y() * s,
        p.y() * c + p.x() * s,
    )


def rotate_rect(r: QRectF, phi_rad: float) -> QRectF:
    x1 = rotate_point(r.topLeft(),     phi_rad)
    x2 = rotate_point(r.bottomLeft(),  phi_rad)
    x3 = rotate_point(r.topRight(),    phi_rad)
    x4 = rotate_point(r.bottomRight(), phi_rad)

    return QRectF(x1, x3).united(QRectF(x2, x4))
