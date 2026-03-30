# cmdplot.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QBrush, QPainterPath

from .command import Command
from .token_ import Token
from .factor import pt2iu
from .range_ import Range
from .rotate import rotate_point

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


@Command.register("plot")
@Command.register("patch")
@Command.register("line")
@Command.register("area")
class CmdPlot(Command):
    """Draw a line, filled polygon, or paper-space path.

    Syntax:
        plot  xdata ydata    — data-space polyline
        patch xdata ydata    — data-space closed polygon
        line  xdata ydata    — paper-space polyline (relative to anchor)
        area  xdata ydata    — paper-space closed polygon
    """

    def _usage(self) -> bool:
        return self.error("Usage: plot|patch|line|area xdata ydata")

    def parse(self, s: Statement) -> bool:
        id1 = s.next_index(1)
        id2 = s.next_index(id1)
        if (id2 == len(s)
                and s.is_numeric(1) and s.is_numeric(id1)
                and len(s.data(1)) == len(s.data(id1))):
            return True
        return self._usage()

    def data_range(self, s: Statement) -> QRectF:
        if s[0].str in ("line", "area"):
            return QRectF()  # paper-space commands have no data range

        xdata = s.data(1)
        ydata = s.data(s.next_index(1))
        if not xdata:
            return QRectF()

        range_x = Range()
        range_y = Range()
        for x in xdata:
            range_x.extend(x)
        for y in ydata:
            range_y.extend(y)
        return QRectF(
            QPointF(range_x.min(), range_y.min()),
            QPointF(range_x.max(), range_y.max()),
        )

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        xdata = s.data(1)
        ydata = s.data(s.next_index(1))

        if not xdata:
            f.set_bbox(QRectF())
            return

        path = QPainterPath()
        last_nan = True
        cmd = s[0].str

        if cmd in ("plot", "patch"):
            for k in range(len(xdata)):
                if math.isnan(xdata[k]) or math.isnan(ydata[k]):
                    last_nan = True
                else:
                    pt = f.map(xdata[k], ydata[k])
                    if last_nan:
                        path.moveTo(pt)
                    else:
                        path.lineTo(pt)
                    last_nan = False

        else:  # line / area — paper space, relative to anchor
            a = f.anchor_angle()
            xy0 = f.anchor()
            for k in range(len(xdata)):
                if math.isnan(xdata[k]) or math.isnan(ydata[k]):
                    last_nan = True
                else:
                    xy = QPointF(pt2iu(xdata[k]), pt2iu(ydata[k]))
                    if a:
                        xy = rotate_point(xy, a)
                    xy += xy0
                    if last_nan:
                        path.moveTo(xy)
                    else:
                        path.lineTo(xy)
                    last_nan = False

        if cmd in ("patch", "area"):
            path.closeSubpath()

        bbox = path.boundingRect()
        w = f.painter().pen().widthF()
        if w > 0:
            bbox.adjust(-w/2, -w/2, w/2, w/2)
        # Note: does not account for protruding miters.
        f.set_bbox(bbox)

        if dryrun:
            return

        brush = f.painter().brush()
        if cmd in ("plot", "line"):
            f.painter().setBrush(QBrush(Qt.BrushStyle.NoBrush))

        f.painter().drawPath(path)

        if cmd in ("plot", "line"):
            f.painter().setBrush(brush)
