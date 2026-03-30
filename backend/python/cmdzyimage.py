# cmdzyimage.py - This file is part of QPlot

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
_Z     = 1
_Y     = 2
_D     = 3
_H     = 4
_X     = 5
_XZ    = 6
_YZ    = 7
_BIGZ  = 8
_BIGY  = 9
_CDATA = 10


@Command.register("zyimage")
class CmdZYImage(Command):
    """Draw an image in a skewed zy-plane coordinate system.

    Syntax:
        zyimage z y d h x xz yz Z Y cdata
    """

    def _usage(self) -> bool:
        return self.error("Usage: zyimage z y d h x xz yz Z Y cdata\n")

    def parse(self, s: Statement) -> bool:
        if len(s) < _CDATA + 1:
            return self._usage()
        for k in range(_Z, _BIGY + 1):
            if s[k].typ != Token.NUMBER:
                return self._usage()
        id1 = s.next_index(_CDATA)
        if id1 != len(s) or not s.is_numeric(_CDATA):
            return self._usage()
        Z = int(s[_BIGZ].num)
        Y = int(s[_BIGY].num)
        N = len(s.data(_CDATA))
        if N % (Z * Y) != 0:
            return self._usage()
        C = N // (Z * Y)
        if C < 1 or C > 4:
            return self._usage()
        return True

    def data_range(self, s: Statement) -> QRectF:
        minz = s[_Z].num
        maxz = s[_Z].num + s[_D].num
        miny = s[_Y].num
        maxy = s[_Y].num + s[_H].num
        x    = s[_X].num
        xz   = s[_XZ].num
        yz   = s[_YZ].num
        r1 = QRectF(QPointF(x + xz * minz, miny + yz * minz),
                    QPointF(x + xz * maxz, maxy + yz * maxz))
        r2 = QRectF(QPointF(x + xz * minz, maxy + yz * minz),
                    QPointF(x + xz * maxz, miny + yz * maxz))
        return r1.united(r2).normalized()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        Z     = int(s[_BIGZ].num)
        Y     = int(s[_BIGY].num)   # BUG FIX: C++ used s[ArgZ] here by mistake
        cdata = s.data(_CDATA)
        C     = len(cdata) // Z // Y

        extent = self.data_range(s)
        p1     = f.map(extent.left(),  extent.top())
        p2     = f.map(extent.right(), extent.bottom())
        bbox   = QRectF(p1, p2).normalized()
        f.set_bbox(bbox)

        if dryrun:
            return

        z0 = s[_Z].num
        y0 = s[_Y].num
        d  = s[_D].num
        h  = s[_H].num
        x  = s[_X].num
        xz = s[_XZ].num
        yz = s[_YZ].num

        img = image_build(Z, Y, C, cdata)

        f.painter().save()
        data2paper = f.xform()
        img2data   = QTransform(
            xz * d / Z,  yz * d / Z, 0,
            0,            h / Y,      0,
            x + xz * z0, y0 + yz * z0, 1,
        )
        f.painter().setTransform(data2paper, True)
        f.painter().setTransform(img2data,   True)
        f.painter().drawImage(QPointF(0, 0), img)
        f.painter().restore()
