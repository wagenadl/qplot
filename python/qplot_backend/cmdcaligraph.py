# cmdcaligraph.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPolygonF, QBrush

from .command import Command
from .token_ import Token
from .factor import pt2iu

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


@Command.register("caligraph")
class CmdCaligraph(Command):
    """Draw a calligraphic line of variable width.

    Syntax:
        caligraph xdata ydata widthdata
    """

    def _usage(self) -> bool:
        return self.error("Usage: caligraph xdata ydata widthdata")

    def parse(self, s: Statement) -> bool:
        id1 = s.next_index(1)
        id2 = s.next_index(id1)
        id3 = s.next_index(id2)
        if (id3 == len(s)
                and s.is_numeric(1) and s.is_numeric(id1) and s.is_numeric(id2)
                and len(s.data(1)) == len(s.data(id1))
                and len(s.data(1)) == len(s.data(id2))):
            return True
        return self._usage()

    def data_range(self, s: Statement) -> QRectF:
        xdata = s.data(1)
        ydata = s.data(s.next_index(1))
        if not xdata:
            return QRectF()
        return QRectF(
            QPointF(min(xdata), min(ydata)),
            QPointF(max(xdata), max(ydata)),
        )

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        id1 = s.next_index(1)
        id2 = s.next_index(id1)
        xdata = s.data(1)
        ydata = s.data(id1)
        wdata = s.data(id2)

        if not xdata:
            f.set_bbox(QRectF())
            return

        # Each interior point expands to three polygon vertices:
        # two on the outer corner, one on the inner.
        # First and last points expand to two each.
        N = len(xdata)
        L = 3 * N - 2
        poly = [QPointF(0, 0)] * L  # pre-allocate, filled from both ends
        l1 = 0                       # front pointer (outer edge)
        l2 = L                       # back pointer  (inner edge)

        pprev = QPointF()
        pthis = QPointF()
        pnext = QPointF()
        dprev = QPointF()
        dnext = QPointF()
        theta_prev = 0.0
        theta_next = 0.0

        for k in range(N):
            if k > 0:
                pprev = pthis
            if k > 0:
                pthis = pnext
            else:
                pthis = f.map(xdata[k], ydata[k])
            if k < N - 1:
                pnext = f.map(xdata[k + 1], ydata[k + 1])

            if k > 0:
                dprev = dnext
            if k < N - 1:
                dnext = pnext - pthis

            if k > 0:
                theta_prev = theta_next
            if k < N - 1:
                theta_next = math.atan2(dnext.y(), dnext.x())

            w = pt2iu(wdata[k] / 2)

            if k == 0:
                dd = w * QPointF(-math.sin(theta_next), math.cos(theta_next))
                poly[l1] = pthis + dd;  l1 += 1
                l2 -= 1;                poly[l2] = pthis - dd

            elif k == N - 1:
                dd = w * QPointF(-math.sin(theta_prev), math.cos(theta_prev))
                poly[l1] = pthis + dd;  l1 += 1
                l2 -= 1;                poly[l2] = pthis - dd

            else:
                dd_prev = w * QPointF(-math.sin(theta_prev), math.cos(theta_prev))
                dd_next = w * QPointF(-math.sin(theta_next), math.cos(theta_next))

                # Cross product sign determines which side is convex
                if dnext.y() * dprev.x() > dnext.x() * dprev.y():
                    poly[l1] = pthis + dd_prev / 2 + dd_next / 2;  l1 += 1
                    l2 -= 1;  poly[l2] = pthis - dd_prev
                    l2 -= 1;  poly[l2] = pthis - dd_next
                else:
                    poly[l1] = pthis + dd_prev;  l1 += 1
                    poly[l1] = pthis + dd_next;  l1 += 1
                    l2 -= 1;  poly[l2] = pthis - dd_prev / 2 - dd_next / 2

        if l1 != l2:
            import sys
            print("Caligraph: point miscount", file=sys.stderr)

        qpoly = QPolygonF(poly)
        bbox = qpoly.boundingRect()
        f.set_bbox(bbox)

        if dryrun:
            return

        painter = f.painter()
        pen = painter.pen()
        brush = painter.brush()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(pen.color()))
        painter.drawPolygon(qpoly)
        painter.setPen(pen)
        painter.setBrush(brush)
