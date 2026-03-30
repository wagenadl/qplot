# cmdmark.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt, QPointF, QRectF, QSizeF
from PyQt6.QtGui import QPainter, QPolygonF, QColor

from .command import Commandfrom .token_ import Tokenfrom .factor import pt2iufrom .rotate import rotate_pointfrom .slightly import slightly_less, slightly_morefrom .marker import Marker
if TYPE_CHECKING:
    from .statement import Statement    from .figure import Figure

# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _render_mark(p: QPainter, xy: QPointF, r: float,
                 t: Marker.Type, as_spine: bool) -> None:
    """Draw a single marker of type t, centred at xy with radius r."""
    pf: list[QPointF]

    if t == Marker.Type.CIRCLE:
        p.drawEllipse(xy, r, r)

    elif t == Marker.Type.SQUARE:
        r *= math.sqrt(math.pi / 4)
        if as_spine:
            p.drawLine(xy + QPointF(-r, -r), xy + QPointF(r,  r))
            p.drawLine(xy + QPointF(-r,  r), xy + QPointF(r, -r))
        else:
            p.drawRect(QRectF(xy + QPointF(-r, -r), QSizeF(2*r, 2*r)))

    elif t == Marker.Type.DIAMOND:
        r *= math.sqrt(2 * math.pi / 4)
        pf = [
            xy + QPointF(-r,  0),
            xy + QPointF( 0, -r),
            xy + QPointF( r,  0),
            xy + QPointF( 0,  r),
        ]
        if as_spine:
            p.drawLine(pf[0], pf[2])
            p.drawLine(pf[1], pf[3])
        else:
            p.drawConvexPolygon(QPolygonF(pf))

    elif t == Marker.Type.LEFTTRIANGLE:
        r *= 2.0 / 3
        s3r = math.sqrt(3) * r
        pf = [
            xy + QPointF(-2*r,   0),
            xy + QPointF(   r, -s3r),
            xy + QPointF(   r,  s3r),
        ]
        if as_spine:
            for v in pf:
                p.drawLine(xy, v)
        else:
            p.drawConvexPolygon(QPolygonF(pf))

    elif t == Marker.Type.DOWNTRIANGLE:
        r *= 2.0 / 3
        s3r = math.sqrt(3) * r
        pf = [
            xy + QPointF(   0, 2*r),
            xy + QPointF(-s3r,  -r),
            xy + QPointF( s3r,  -r),
        ]
        if as_spine:
            for v in pf:
                p.drawLine(xy, v)
        else:
            p.drawConvexPolygon(QPolygonF(pf))

    elif t == Marker.Type.RIGHTTRIANGLE:
        r *= 2.0 / 3
        s3r = math.sqrt(3) * r
        pf = [
            xy + QPointF( 2*r,   0),
            xy + QPointF(  -r,  s3r),
            xy + QPointF(  -r, -s3r),
        ]
        if as_spine:
            for v in pf:
                p.drawLine(xy, v)
        else:
            p.drawConvexPolygon(QPolygonF(pf))

    elif t == Marker.Type.UPTRIANGLE:
        r *= 2.0 / 3
        s3r = math.sqrt(3) * r
        pf = [
            xy + QPointF(   0, -2*r),
            xy + QPointF(-s3r,    r),
            xy + QPointF( s3r,    r),
        ]
        if as_spine:
            for v in pf:
                p.drawLine(xy, v)
        else:
            p.drawConvexPolygon(QPolygonF(pf))

    elif t == Marker.Type.PENTAGRAM:
        r *= 0.5 + 0.5 * math.sqrt(5)
        r1 = (0.5 * math.sqrt(5) - 0.5) ** 2
        pf = []
        for k in range(10):
            dy = -r * math.cos(2 * math.pi * k / 10)
            dx =  r * math.sin(2 * math.pi * k / 10)
            if k & 1:
                dx *= r1
                dy *= r1
            pf.append(xy + QPointF(dx, dy))
        if as_spine:
            for k in range(0, 10, 2):
                p.drawLine(xy, pf[k])
        else:
            p.drawPolygon(QPolygonF(pf))

    elif t == Marker.Type.HEXAGRAM:
        r = r * math.sqrt(math.sqrt(3))
        r1 = 1.0 / math.sqrt(3)
        pf = []
        for k in range(12):
            dy =  r * math.cos(2 * math.pi * k / 12)
            dx = -r * math.sin(2 * math.pi * k / 12)
            if k & 1:
                dx *= r1
                dy *= r1
            pf.append(xy + QPointF(dx, dy))
        if as_spine:
            for k in range(0, 6, 2):
                p.drawLine(pf[k], pf[k + 6])
        else:
            p.drawPolygon(QPolygonF(pf))

    elif t == Marker.Type.PLUS:
        p.drawLine(xy + QPointF( r, 0), xy + QPointF(-r,  0))
        p.drawLine(xy + QPointF( 0, r), xy + QPointF( 0, -r))

    elif t == Marker.Type.CROSS:
        r /= math.sqrt(2)
        p.drawLine(xy + QPointF( r,  r), xy + QPointF(-r, -r))
        p.drawLine(xy + QPointF(-r,  r), xy + QPointF( r, -r))

    elif t == Marker.Type.HBAR:
        p.drawLine(xy + QPointF(r, 0), xy + QPointF(-r, 0))

    elif t == Marker.Type.VBAR:
        p.drawLine(xy + QPointF(0, r), xy + QPointF(0, -r))

    elif t == Marker.Type.STAR:
        rx = 0.5   * r   # cos(60°)
        ry = 0.866 * r   # sin(60°)
        p.drawLine(xy + QPointF( r,   0), xy + QPointF(-r,   0))
        p.drawLine(xy + QPointF( rx,  ry), xy + QPointF(-rx, -ry))
        p.drawLine(xy + QPointF( rx, -ry), xy + QPointF(-rx,  ry))


def _avoid_collision(pts: list[QPointF], rx: float, ry: float,
                     vertical: bool) -> list[QPointF]:
    """Displace points horizontally (or vertically) to avoid overlap."""
    out: list[QPointF] = []
    rx2 = rx * rx
    ry2 = ry * ry

    def collides(p: QPointF) -> bool:
        for q in out:
            dx = p.x() - q.x()
            dy = p.y() - q.y()
            if dx*dx / rx2 + dy*dy / ry2 < 1:
                return True
        return False

    for p in pts:
        dx = 0.0
        offset = QPointF(0, dx) if vertical else QPointF(dx, 0)
        while collides(p + offset):
            if dx > 0:
                dx = -dx
            else:
                dx = -dx + rx
            offset = QPointF(0, dx) if vertical else QPointF(dx, 0)
        out.append(p + offset)

    return out


# ---------------------------------------------------------------------------
# Command class
# ---------------------------------------------------------------------------

@Command.register("mark")
@Command.register("pmark")
class CmdMark(Command):
    """Draw markers at data or paper coordinates.

    Syntax:
        mark  xdata ydata
        mark  xdata ydata rx [ry [1]]   (displace to avoid crowding)
        pmark xdata ydata
    """

    def _usage(self) -> bool:
        return self.error("Usage: mark|pmark xdata ydata [rx [ry [1]]]")

    def parse(self, s: Statement) -> bool:
        id1 = s.next_index(1)
        id2 = s.next_index(id1)
        if (not s.is_numeric(1) or not s.is_numeric(id1)
                or len(s.data(1)) != len(s.data(id1))):
            return self._usage()
        if id2 == len(s):
            return True
        if s[0].str == "pmark":
            return self._usage()
        if not s.is_numeric(id2) or len(s.data(id2)) != 1:  # rx
            return self._usage()
        id3 = s.next_index(id2)
        if id3 == len(s):
            return True
        if not s.is_numeric(id3) or len(s.data(id3)) != 1:  # ry
            return self._usage()
        id4 = s.next_index(id3)
        if id4 == len(s):
            return True
        if not s.is_numeric(id4) or len(s.data(id4)) != 1:  # isvert
            return self._usage()
        id5 = s.next_index(id4)
        if id5 == len(s):
            return True
        return self._usage()

    def data_range(self, s: Statement) -> QRectF:
        if s[0].str == "pmark":
            return QRectF()  # paper coordinates — no data range

        xdata = s.data(1)
        ydata = s.data(s.next_index(1))
        if not xdata:
            return QRectF()

        return QRectF(
            QPointF(slightly_less(min(xdata)), slightly_less(min(ydata))),
            QPointF(slightly_more(max(xdata)), slightly_more(max(ydata))),
        )

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        xdata = s.data(1)
        idx = s.next_index(1)
        ydata = s.data(idx)

        if not xdata:
            f.set_bbox(QRectF())
            return

        rx = ry = 0.0
        hori = vert = False
        idx = s.next_index(idx)

        if idx < len(s):
            hori = True
            rx = pt2iu(s.data(idx)[0])
            ry = rx
            idx = s.next_index(idx)
            if idx < len(s):
                ry = pt2iu(s.data(idx)[0])
                idx = s.next_index(idx)
                if idx < len(s):
                    vert = s.data(idx)[0] != 0
                    hori = not vert

        if s[0].str == "mark":
            pp = [f.map(xdata[k], ydata[k]) for k in range(len(xdata))]
            if hori:
                pp = _avoid_collision(pp, rx, ry, vertical=False)
            elif vert:
                pp = _avoid_collision(pp, rx, ry, vertical=True)
        else:  # pmark
            a = f.anchor_angle()
            xy0 = f.anchor()
            pp = []
            for k in range(len(xdata)):
                xy = QPointF(pt2iu(xdata[k]), pt2iu(ydata[k]))
                if a:
                    xy = rotate_point(xy, a)
                xy += xy0
                pp.append(xy)

        qpp = QPolygonF(pp)
        bbox = qpp.boundingRect()
        w = f.painter().pen().widthF()
        if w > 0:
            bbox.adjust(-w/2, -w/2, w/2, w/2)
        r = f.marker().radius
        bbox.adjust(-r, -r, r, r)
        f.set_bbox(bbox)

        if dryrun:
            return

        CmdMark.draw(qpp, f)

    @staticmethod
    def draw(pp: QPolygonF, f: Figure) -> None:
        """Draw markers at the given paper-coordinate points.
        Called by CmdHatch as well as by render()."""
        ptr = f.painter()
        ptr.save()

        as_spine = False
        fill = f.marker().fill

        if fill == Marker.Fill.CLOSED:
            ptr.setBrush(ptr.pen().color())
        elif fill == Marker.Fill.OPEN:
            ptr.setBrush(QColor("white"))
        elif fill == Marker.Fill.BRUSH:
            pass  # use current brush as-is
        elif fill == Marker.Fill.SPINE:
            as_spine = True

        t = f.marker().type
        r = f.marker().radius

        if t == Marker.Type.CIRCLE and as_spine:
            ptr.setBrush(Qt.BrushStyle.NoBrush)

        for p in pp:
            _render_mark(ptr, p, r, t, as_spine)

        ptr.restore()
