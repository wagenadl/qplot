# cmdxzimage.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QTransform

from .command import Commandfrom .token_ import Tokenfrom .image import build as image_build
if TYPE_CHECKING:
    from .statement import Statement    from .figure import Figure
# Token index constants (mirrors the C++ Arg enum)
_X     = 1
_Z     = 2
_W     = 3
_D     = 4
_Y     = 5
_XZ    = 6
_YZ    = 7
_BIGX  = 8
_BIGZ  = 9
_CDATA = 10


@Command.register("xzimage")
class CmdXZImage(Command):
    """Draw an image in a skewed xz-plane coordinate system.

    Syntax:
        xzimage x z w d y xz yz X Z cdata
    """

    def _usage(self) -> bool:
        return self.error("Usage: xzimage x z w d y xz yz X Z cdata\n")

    def parse(self, s: Statement) -> bool:
        if len(s) < _CDATA + 1:
            return self._usage()
        for k in range(_X, _BIGZ + 1):
            if s[k].typ != Token.NUMBER:
                return self._usage()
        id1 = s.next_index(_CDATA)
        if id1 != len(s) or not s.is_numeric(_CDATA):
            return self._usage()
        X = int(s[_BIGX].num)
        Z = int(s[_BIGZ].num)
        N = len(s.data(_CDATA))
        if N % (X * Z) != 0:
            return self._usage()
        C = N // (X * Z)
        if C < 1 or C > 4:
            return self._usage()
        return True

    def data_range(self, s: Statement) -> QRectF:
        minx = s[_X].num
        maxx = s[_X].num + s[_W].num
        minz = s[_Z].num
        maxz = s[_Z].num + s[_D].num
        y    = s[_Y].num
        xz   = s[_XZ].num
        yz   = s[_YZ].num
        r1 = QRectF(QPointF(minx + xz * minz, y + yz * minz),
                    QPointF(maxx + xz * maxz, y + yz * maxz))
        r2 = QRectF(QPointF(maxx + xz * minz, y + yz * minz),
                    QPointF(minx + xz * maxz, y + yz * maxz))
        return r1.united(r2).normalized()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        X     = int(s[_BIGX].num)
        Z     = int(s[_BIGZ].num)
        cdata = s.data(_CDATA)
        C     = len(cdata) // X // Z

        extent = self.data_range(s)
        p1     = f.map(extent.left(),  extent.top())
        p2     = f.map(extent.right(), extent.bottom())
        bbox   = QRectF(p1, p2).normalized()
        f.set_bbox(bbox)

        if dryrun:
            return

        x0 = s[_X].num
        z0 = s[_Z].num
        w  = s[_W].num
        d  = s[_D].num
        y  = s[_Y].num
        xz = s[_XZ].num
        yz = s[_YZ].num

        img = image_build(X, Z, C, cdata)

        f.painter().save()
        data2paper = f.xform()
        img2data   = QTransform(
            w / X,        0,        0,
            xz * d / Z,   yz * d / Z, 0,
            x0 + xz * z0, y + yz * z0, 1,
        )
        f.painter().setTransform(data2paper, True)
        f.painter().setTransform(img2data,   True)
        f.painter().drawImage(QPointF(0, 0), img)
        f.painter().restore()
