# cmdimageg.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF, QRectF, QSizeF

from .command import Command
from .token_ import Token
from .factor import pt2iu
from .image import build as image_build

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


def _has_complex_syntax(s: Statement) -> bool:
    return len(s) >= 2 and s[1].typ == Token.OPENBRACKET


@Command.register("imageg")
class CmdImageG(Command):
    """Draw a grayscale image.

    Syntax (simple):
        imageg x y w h K cdata

    Syntax (complex):
        imageg [ dataxywh ] [ paperxywh ] [ W H C ] cdata
    """

    def _usage(self) -> bool:
        return self.error(
            "Usage: imageg x y w h K cdata\n"
            "       imageg [ dataxywh ] [ paperxywh ] [ W H C ] cdata"
        )

    # --- parse ------------------------------------------------------------

    def _parse_complex(self, s: Statement) -> bool:
        id1 = s.next_index(1)
        id2 = s.next_index(id1)
        id3 = s.next_index(id2)

        # BUG FIX: original missing 'return' on all usage() calls here.
        if (not s.is_numeric(1) or not s.is_numeric(id1)
                or not s.is_numeric(id2)):
            return self._usage()
        if not s.is_numeric(id3):
            return self._usage()
        if len(s.data(1)) != 4:       # dataxywh
            return self._usage()
        if len(s.data(id1)) != 4:     # paperxywh
            return self._usage()
        if len(s.data(id2)) != 3:     # size spec (W H C)
            return self._usage()

        size = s.data(id2)
        expected = int(size[0]) * int(size[1]) * int(size[2])
        if len(s.data(id3)) != expected:
            return self._usage()

        return True

    def _parse_simple(self, s: Statement) -> bool:
        if len(s) < 7:
            return self._usage()
        for k in range(1, 6):
            if s[k].typ != Token.NUMBER:
                return self._usage()
        id1 = s.next_index(6)
        if id1 != len(s) or not s.is_numeric(6):
            return self._usage()
        K = int(s[5].num)
        N = len(s.data(6))
        if N % K != 0:
            return self._usage()
        return True

    def parse(self, s: Statement) -> bool:
        if _has_complex_syntax(s):
            return self._parse_complex(s)
        return self._parse_simple(s)

    # --- data_range -------------------------------------------------------

    def data_range(self, s: Statement) -> QRectF:
        if _has_complex_syntax(s):
            # Paper-transformed images don't contribute to range calculations.
            return QRectF()
        minx = s[1].num
        maxx = s[1].num + s[3].num
        miny = s[2].num
        maxy = s[2].num + s[4].num
        return QRectF(QPointF(minx, miny), QPointF(maxx, maxy))

    # --- render -----------------------------------------------------------

    def _render_complex(self, s: Statement, f: Figure,
                        dryrun: bool) -> None:
        i_dataxywh  = 1
        i_paperxywh = s.next_index(i_dataxywh)
        i_sizespec  = s.next_index(i_paperxywh)
        i_data      = s.next_index(i_sizespec)

        X = int(s.data(i_sizespec)[0])
        Y = int(s.data(i_sizespec)[1])
        C = int(s.data(i_sizespec)[2])

        x = s.data(i_dataxywh)[0]
        y = s.data(i_dataxywh)[1]
        w = s.data(i_dataxywh)[2]
        h = s.data(i_dataxywh)[3]

        na_x = math.isnan(x)
        na_y = math.isnan(y)
        if na_x:
            x = 0.0
        if na_y:
            y = 0.0

        d = QRectF(QPointF(x, y), QSizeF(w, h))
        p1 = f.map(d.left(),  d.bottom())
        p2 = f.map(d.right(), d.top())

        if na_x:
            p1.setX(0.0)
            p2.setX(f.x_axis().maprel(w).x())
        if na_y:
            p1.setY(0.0)
            p2.setY(f.y_axis().maprel(h).y())

        paper = s.data(i_paperxywh)
        p1 += QPointF(pt2iu(paper[0]), pt2iu(paper[1]))
        p2 += QPointF(pt2iu(paper[0] + paper[2]),
                      pt2iu(paper[1] + paper[3]))

        bbox = QRectF(p1, p2).normalized()
        f.set_bbox(bbox)

        if dryrun:
            return

        img = image_build(X, Y, C, s.data(i_data))
        f.painter().drawImage(bbox, img)

    def _render_simple(self, s: Statement, f: Figure,
                       dryrun: bool) -> None:
        X = int(s[5].num)
        cdata = s.data(6)
        C = 1                          # grayscale — differs from CmdImage (C=3)
        Y = len(cdata) // C // X

        extent = self.data_range(s)
        p1 = f.map(extent.left(),  extent.top())
        p2 = f.map(extent.right(), extent.bottom())
        bbox = QRectF(p1, p2).normalized()
        f.set_bbox(bbox)

        if dryrun:
            return

        img = image_build(X, Y, C, cdata)
        f.painter().drawImage(bbox, img)

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        if _has_complex_syntax(s):
            self._render_complex(s, f, dryrun)
        else:
            self._render_simple(s, f, dryrun)
