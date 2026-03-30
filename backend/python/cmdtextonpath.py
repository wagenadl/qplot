# cmdtextonpath.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QFontMetricsF, QPolygonF

from .command import Command
from .token_ import Token
from .factor import pt2iu
from .rotate import rotate_rect
from .range_ import Range
from .align import Align

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


def _euclidean_length(p: QPointF) -> float:
    return math.sqrt(p.x() * p.x() + p.y() * p.y())


def _interpret_along(pp: list[QPointF], eta: list[float],
                     w: float) -> tuple[QPointF, float]:
    """Return (position, angle) at arc-length w along polygon pp.
    eta[k] is the cumulative arc length to pp[k].
    Extrapolates linearly beyond the ends."""
    K = len(eta)
    if K < 2:
        return QPointF(), 0.0

    if w < 0:
        ang = math.atan2(pp[1].y() - pp[0].y(), pp[1].x() - pp[0].x())
        return (pp[0] + QPointF(w * math.cos(ang), w * math.sin(ang)),
                ang)

    if w >= eta[-1]:
        w -= eta[-1]
        ang = math.atan2(pp[K-1].y() - pp[K-2].y(),
                         pp[K-1].x() - pp[K-2].x())
        return (pp[-1] + QPointF(w * math.cos(ang), w * math.sin(ang)),
                ang)

    k = 0
    while w > eta[k]:
        k += 1
    # w <= eta[k]

    if w == eta[k]:
        ang = math.atan2(pp[k+1].y() - pp[k-1].y(),
                         pp[k+1].x() - pp[k-1].x())
        return pp[k], ang

    # interpolate between k-1 and k
    q   = (w - eta[k-1]) / (eta[k] - eta[k-1] + 1e-9)
    ang = math.atan2(pp[k].y() - pp[k-1].y(),
                     pp[k].x() - pp[k-1].x())
    pt  = QPointF((1 - q) * pp[k-1].x() + q * pp[k].x(),
                  (1 - q) * pp[k-1].y() + q * pp[k].y())
    return pt, ang


@Command.register("textonpath")
class CmdTextOnPath(Command):
    """Draw text characters individually along a data path.

    Syntax:
        textonpath xdata ydata dxpaper dypaper 'text'
    """

    def _usage(self) -> bool:
        return self.error(
            "Usage: textonpath xdata ydata dxpaper dypaper text")

    def parse(self, s: Statement) -> bool:
        id1 = s.next_index(1)
        id2 = s.next_index(id1)
        if (s.is_numeric(1) and s.is_numeric(id1)
                and id2 == len(s) - 3
                and len(s.data(1)) == len(s.data(id1))
                and s[id2].typ   == Token.NUMBER
                and s[id2+1].typ == Token.NUMBER
                and s[id2+2].typ == Token.STRING):
            return True
        return self._usage()

    def data_range(self, s: Statement) -> QRectF:
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
        return QRectF(QPointF(range_x.min(), range_y.min()),
                      QPointF(range_x.max(), range_y.max()))

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        xdata = s.data(1)
        id1   = s.next_index(1)
        ydata = s.data(id1)
        id2   = s.next_index(id1)

        dxbase = pt2iu(s[id2].num)
        dybase = pt2iu(s[id2+1].num)
        txt    = s[id2+2].str

        if not xdata:
            f.set_bbox(QRectF())
            return

        # Build polygon in paper coordinates
        pp = [f.map(xdata[k], ydata[k]) for k in range(len(xdata))]

        # Cumulative arc lengths along polygon
        eta = [0.0] * len(pp)
        for k in range(1, len(pp)):
            eta[k] = eta[k-1] + _euclidean_length(pp[k] - pp[k-1])

        # Measure each character's bounding rect and advance width
        fm           = QFontMetricsF(f.painter().font())
        text_y_range = Range()
        xi           = [0.0] * (len(txt) + 1)
        rr:  list[QRectF] = []
        ww:  list[float]  = []

        for i, ch in enumerate(txt):
            r = fm.tightBoundingRect(ch)
            text_y_range.extend(r.top())
            text_y_range.extend(r.bottom())
            w = fm.horizontalAdvance(ch)
            ww.append(w)
            xi[i+1] = xi[i] + w
            rr.append(r)

        # Vertical alignment
        dy = dybase
        valign = f.valign()
        if valign == Align.VAlign.TOP:
            dy -= text_y_range.min()
        elif valign == Align.VAlign.MIDDLE:
            dy -= (text_y_range.min() + text_y_range.max()) / 2
        elif valign == Align.VAlign.BOTTOM:
            dy -= text_y_range.max()
        # BASE: dy unchanged

        # Horizontal alignment — offset along the path
        dxi = dxbase
        halign = f.halign()
        if halign == Align.HAlign.CENTER:
            dxi += eta[-1] / 2 - xi[-1] / 2
        elif halign == Align.HAlign.RIGHT:
            dxi += eta[-1] - xi[-1]

        bb = QRectF()
        for i in range(len(txt)):
            pt, ang = _interpret_along(
                pp, eta, (xi[i] + xi[i+1]) / 2 + dxi)
            r = rotate_rect(
                rr[i].translated(0, dy), ang).translated(pt)
            bb = r if bb.isNull() else bb.united(r)

            if not dryrun:
                f.painter().save()
                f.painter().translate(pt)
                f.painter().rotate(ang * 180 / math.pi)
                f.painter().drawText(QPointF(-ww[i] / 2, dy), txt[i])
                f.painter().restore()

        f.set_bbox(bb)
