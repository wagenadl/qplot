# cmdhatch.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QPolygonF, QPainterPath

from .command import Command
from .cmdplot import CmdPlot
from .cmdmark import CmdMark
from .rotate import rotate_point
from .token_ import Token
from .factor import pt2iu

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


@Command.register("hatch")
@Command.register("phatch")
class CmdHatch(CmdPlot):
    """Draw hatching inside a polygon.

    Syntax:
        hatch  xdata ydata angle(rad) spacing(pt) [offset(pt)]
        phatch xdata ydata angle(rad) spacing(pt) [offset(pt)]

    phatch uses paper coordinates rather than data coordinates.
    angle may also be '*' (hex grid), ':' (rect grid), or '%' (diagonal grid).
    """

    def _usage(self) -> bool:
        return self.error(
            "Usage: hatch|phatch xdata ydata angle spacing (offset)")

    def data_range(self, s: Statement) -> QRectF:
        if s[0].str == "phatch":
            return QRectF()
        return super().data_range(s)

    def parse(self, s: Statement) -> bool:
        idx_x = 1
        idx_y = s.next_index(idx_x)
        idx_a = s.next_index(idx_y)
        idx_s = s.next_index(idx_a)
        idx_o = s.next_index(idx_s)
        idx_end = s.next_index(idx_o)

        angle_tok = s.token(idx_a)
        angle_ok = (angle_tok.typ == Token.NUMBER
                    or (angle_tok.typ == Token.STRING
                        and angle_tok.str in ("*", ":", "%")))

        if (s.is_numeric(idx_x) and s.is_numeric(idx_y)
                and len(s.data(idx_x)) == len(s.data(idx_y))
                and angle_ok
                and s.token(idx_s).typ == Token.NUMBER
                and (idx_o == len(s) or s.token(idx_o).typ == Token.NUMBER)
                and (idx_o == len(s) or idx_end == len(s))
                and s.token(idx_s).num > 0):
            return True
        return self._usage()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        idx_x = 1
        idx_y = s.next_index(idx_x)
        idx_a = s.next_index(idx_y)
        idx_s = s.next_index(idx_a)
        idx_o = s.next_index(idx_s)

        xdata = s.data(idx_x)
        ydata = s.data(idx_y)
        angle_tok = s.token(idx_a)
        angle = angle_tok.num  # 0.0 if not a number, safe default
        is_hex  = angle_tok.typ == Token.STRING and angle_tok.str == "*"
        is_rect = angle_tok.typ == Token.STRING and angle_tok.str == ":"
        is_diag = angle_tok.typ == Token.STRING and angle_tok.str == "%"
        spacing = pt2iu(s.token(idx_s).num)
        if is_diag:
            spacing /= math.sqrt(2)
        # safe even with no offset token — num==0 for missing tokens
        offset = pt2iu(s.token(idx_o).num)

        # Convert (xdata, ydata) to polygons in paper space.
        # NaNs in the data separate individual polygons.
        polygons: list[QPolygonF] = []
        current: list[QPointF] = []
        is_paper = s[0].str == "phatch"
        at_angle = f.anchor_angle()
        at_xy = f.anchor()

        for k in range(len(xdata)):
            if math.isnan(xdata[k]) or math.isnan(ydata[k]):
                if current:
                    polygons.append(QPolygonF(current))
                current = []
            else:
                if is_paper:
                    pt = (rotate_point(
                              QPointF(pt2iu(xdata[k]), pt2iu(ydata[k])),
                              at_angle)
                          + at_xy)
                else:
                    pt = f.map(xdata[k], ydata[k])
                current.append(pt)
        if current:
            polygons.append(QPolygonF(current))

        if not polygons:
            f.set_bbox(QRectF())
            return

        bbox = polygons[0].boundingRect()
        for poly in polygons[1:]:
            bbox = bbox.united(poly.boundingRect())
        f.set_bbox(bbox)  # lines don't protrude by w/2 because of clipping

        if dryrun:
            return

        # Strategy: rotate all polygons by -angle into grid space (XI, ETA),
        # find the grid lines that cover the bbox, rotate them back, and draw.
        # OFFSET is relative to the centroid of all polygon centroids.
        antirotated: list[QPolygonF] = []
        for poly in polygons:
            rot = [rotate_point(p, -angle) for p in poly]
            antirotated.append(QPolygonF(rot))

        anticenter = QPointF(0, 0)
        for poly in antirotated:
            ac1 = QPointF(0, 0)
            for p in poly:
                ac1 += p
            ac1 /= poly.count()
            anticenter += ac1
        anticenter /= len(antirotated)
        anticenter.setX(anticenter.x() + offset)

        for k, poly in enumerate(polygons):
            clip = QPainterPath()
            clip.addPolygon(poly)
            clip.closeSubpath()
            f.painter().setClipPath(clip)

            ar = antirotated[k]
            ab = ar.boundingRect()
            xi0  = ab.left()
            xi1  = ab.right()
            eta0 = ab.top()
            eta1 = ab.bottom()
            xi0 = (math.floor((xi0 - anticenter.x()) / spacing)
                   * spacing + anticenter.x())

            if is_hex:
                y_space = 1.732 * spacing  # sqrt(3)
                eta0 = (math.floor((eta0 - anticenter.y()) / y_space)
                        * y_space + anticenter.y())
                pp: list[QPointF] = []
                eta = eta0
                while eta < eta1:
                    xi = xi0
                    while xi < xi1:
                        pp.append(rotate_point(QPointF(xi, eta), angle))
                        xi += spacing
                    xi = xi0 + spacing / 2
                    while xi < xi1:
                        pp.append(rotate_point(
                            QPointF(xi, eta + y_space / 2), angle))
                        xi += spacing
                    eta += y_space
                CmdMark.draw(QPolygonF(pp), f)

            elif is_rect:
                eta0 = (math.floor((eta0 - anticenter.y()) / spacing)
                        * spacing + anticenter.y())
                pp = []
                eta = eta0
                while eta < eta1:
                    xi = xi0
                    while xi < xi1:
                        pp.append(rotate_point(QPointF(xi, eta), angle))
                        xi += spacing
                    eta += spacing
                CmdMark.draw(QPolygonF(pp), f)

            elif is_diag:
                pp = []
                eta = eta0
                while eta < eta1:
                    xi = xi0
                    while xi < xi1:
                        pp.append(rotate_point(QPointF(xi, eta), angle))
                        xi += 2 * spacing
                    eta += spacing
                    if eta < eta1:
                        xi = xi0 + spacing
                        while xi < xi1:
                            pp.append(rotate_point(QPointF(xi, eta), angle))
                            xi += 2 * spacing
                        eta += spacing
                CmdMark.draw(QPolygonF(pp), f)

            else:
                xi = xi0
                while xi < xi1:
                    f.painter().drawLine(
                        rotate_point(QPointF(xi, eta0), angle),
                        rotate_point(QPointF(xi, eta1), angle))
                    xi += spacing

            f.painter().setClipping(False)
