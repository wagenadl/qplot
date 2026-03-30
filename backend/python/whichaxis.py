# whichaxis.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF, QRectF

from range import Range

if TYPE_CHECKING:
    from axis import Axis
    from panel import Panel
    from figure import Figure


class AxisName(enum.Enum):
    X = "X"
    Y = "Y"


class WhichAxis:

    def __init__(self, d: AxisName) -> None:
        self._d = d

    # --- Singleton accessors (mirrors C++ static methods) -----------------

    _x_instance: WhichAxis | None = None
    _y_instance: WhichAxis | None = None

    @staticmethod
    def x() -> WhichAxis:
        if WhichAxis._x_instance is None:
            WhichAxis._x_instance = WhichAxis(AxisName.X)
        return WhichAxis._x_instance

    @staticmethod
    def y() -> WhichAxis:
        if WhichAxis._y_instance is None:
            WhichAxis._y_instance = WhichAxis(AxisName.Y)
        return WhichAxis._y_instance

    # --- Axis selection ---------------------------------------------------

    def axis(self, p: Panel) -> Axis:
        return p.xaxis if self._d == AxisName.X else p.yaxis

    # --- Range helpers ----------------------------------------------------

    def axis_p_range(self, a: Axis) -> Range:
        p1 = a.minp()
        p2 = a.maxp()
        return Range(p1.x(), p2.x()) if self._d == AxisName.X \
            else Range(p1.y(), p2.y())

    def rect_min(self, r: QRectF) -> float:
        return r.left() if self._d == AxisName.X else r.top()

    def rect_max(self, r: QRectF) -> float:
        return r.right() if self._d == AxisName.X else r.bottom()

    def rect_range(self, r: QRectF) -> Range:
        return Range(self.rect_min(r), self.rect_max(r))

    # --- Geometry manipulation --------------------------------------------

    def rerect(self, orig: QRectF, newmin: float, newmax: float) -> QRectF:
        if self._d == AxisName.X:
            return QRectF(newmin, orig.top(), newmax - newmin, orig.height())
        else:
            return QRectF(orig.left(), newmin, orig.width(), newmax - newmin)

    def repoint(self, orig: QPointF, newdim: float) -> QPointF:
        if self._d == AxisName.X:
            return QPointF(newdim, orig.y())
        else:
            return QPointF(orig.x(), newdim)

    def point(self, p: QPointF) -> float:
        return p.x() if self._d == AxisName.X else p.y()

    # --- Group ordering ---------------------------------------------------

    def ordered_groups(self, f: Figure, ids: list[str]) -> list[list[str]]:
        """Sort panel ids by their centre position along this axis,
        then group overlapping ones together."""
        center_pos: dict[str, float] = {}
        range_map: dict[str, Range] = {}

        for id_ in ids:
            p = f.panel(id_)
            r = self.rect_range(p.desired_extent)
            range_map[id_] = r
            center_pos[id_] = (r.min() + r.max()) / 2

        sorted_ids = sorted(ids, key=lambda a: center_pos[a])

        result: list[list[str]] = []
        now: list[str] = []
        r = Range()

        for id_ in sorted_ids:
            if r.contains(center_pos[id_]):
                now.append(id_)
            else:
                if now:
                    result.append(now)
                now = [id_]
                r = range_map[id_]

        if now:
            result.append(now)

        return result
