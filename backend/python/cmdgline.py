# cmdgline.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
import enum
from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QPolygonF

from command import Command
from token_ import Token
from factor import pt2iu

if TYPE_CHECKING:
    from statement import Statement
    from figure import Figure


class _KW(enum.Enum):
    ERROR    = "ERROR"
    absdata  = "absdata"
    abspaper = "abspaper"
    reldata  = "reldata"
    relpaper = "relpaper"
    rotdata  = "rotdata"
    rotpaper = "rotpaper"
    retract  = "retract"
    at       = "at"
    atx      = "atx"
    aty      = "aty"


def _gline_kw(s: str) -> _KW:
    # NOTE: the original C++ had a typo "ayt" instead of "aty" which
    # meant KW_aty was unreachable via keyword lookup. Fixed here.
    try:
        return _KW(s)
    except ValueError:
        return _KW.ERROR


def _got(s: Statement, k: int) -> str:
    return f" rather than '{s[k].str}' after {k}"


@Command.register("gline")
@Command.register("garea")
class CmdGLine(Command):
    """General-purpose line/polygon drawing command.

    Syntax:
        gline ( PT1SPEC ) ( PT2SPEC ) ...
        garea ( PT1SPEC ) ( PT2SPEC ) ...

    where each PTnSPEC is one or more of:
        absdata  X Y       — absolute data coordinates
        abspaper X Y       — absolute paper coordinates (pt)
        reldata  DX DY     — relative data coordinates
        relpaper DX DY     — relative paper coordinates (pt), rotated by phi
        rotdata  XI ETA    — set phi = atan2(eta, xi) in data space
        rotpaper PHI       — set phi directly (radians)
        retract  L [L2]    — retract endpoints along segment
        at  ID             — set point to stored location ID
        atx ID             — set x from stored location ID
        aty ID             — set y from stored location ID
    """

    def _usage(self, x: str = "") -> bool:
        if not x:
            return self.error("Usage: gline|garea ptspec ...")
        return self.error("gline|garea: " + x)

    def parse(self, s: Statement) -> bool:
        k = 1
        while k < len(s):
            if s[k].typ != Token.OPENPAREN:
                return self._usage("expected '('" + _got(s, k))
            k += 1
            if k >= len(s):
                return self._usage()

            while s[k].typ != Token.CLOSEPAREN:
                if s[k].typ != Token.BAREWORD:
                    return self._usage("expected ')' or keyword" + _got(s, k))
                kw = _gline_kw(s[k].str)
                if kw == _KW.ERROR:
                    return self._usage(f"unknown keyword: '{s[k].str}'")
                k += 1
                if k >= len(s):
                    return self._usage(f"missing 1st argument to '{s[k].str}'")

                # Validate first argument
                if kw in (_KW.absdata, _KW.abspaper):
                    if s[k].typ not in (Token.NUMBER, Token.DASH):
                        return self._usage(
                            f"expected number or dash after '{s[k-1].str}'")
                elif kw in (_KW.at, _KW.atx, _KW.aty):
                    if s[k].typ != Token.CAPITAL:
                        return self._usage(
                            f"expected ID after '{s[k-1].str}'")
                else:
                    if s[k].typ != Token.NUMBER:
                        return self._usage("expected number")
                k += 1
                if k >= len(s):
                    return self._usage(f"missing 2nd argument to '{s[k].str}'")

                # Validate second argument (some keywords have only one)
                if kw in (_KW.absdata, _KW.abspaper):
                    if s[k].typ not in (Token.NUMBER, Token.DASH):
                        return self._usage(
                            f"expected number or dash after '{s[k-2].str}'")
                elif kw == _KW.retract:
                    if s[k].typ == Token.CLOSEPAREN:
                        k -= 1  # only one number
                    elif s[k].typ != Token.NUMBER:
                        return self._usage(
                            "expected ')' or number after 'retract'")
                elif kw in (_KW.rotpaper, _KW.at, _KW.atx, _KW.aty):
                    k -= 1  # only one number
                else:
                    if s[k].typ != Token.NUMBER:
                        return self._usage(
                            f"expected number after '{s[k-2].str}'")
                k += 1
                if k >= len(s):
                    return self._usage("unexpected end of line")
            k += 1  # skip CLOSEPAREN
        return True

    def data_range(self, s: Statement) -> QRectF:
        pts: list[QPointF] = []
        k = 1
        while k < len(s):
            k += 1  # skip OPENPAREN
            while s[k].typ != Token.CLOSEPAREN:
                kw = _gline_kw(s[k].str)
                if kw == _KW.absdata:
                    if (s[k+1].typ == Token.NUMBER
                            and s[k+2].typ == Token.NUMBER):
                        pts.append(QPointF(s[k+1].num, s[k+2].num))
                elif kw in (_KW.rotpaper, _KW.at, _KW.atx, _KW.aty):
                    k -= 1  # only one number
                elif kw == _KW.retract:
                    if s[k+2].typ != Token.NUMBER:
                        k -= 1  # only one number
                k += 3  # skip keyword and both number slots
            k += 1  # skip CLOSEPAREN

        if pts:
            poly = QPolygonF(pts)
            return poly.boundingRect()
        return QRectF()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        pts: list[QPointF] = []
        retract_l: list[float] = []
        retract_r: list[float] = []

        k = 1
        while k < len(s):
            p = QPointF(0, 0)
            phi = 0.0
            r_l = r_r = 0.0

            k += 1  # skip OPENPAREN
            while s[k].typ != Token.CLOSEPAREN:
                kw = _gline_kw(s[k].str)

                if kw == _KW.absdata:
                    p1 = f.map(
                        s[k+1].num if s[k+1].typ == Token.NUMBER
                        else f.x_axis().min(),
                        s[k+2].num if s[k+2].typ == Token.NUMBER
                        else f.y_axis().min(),
                    )
                    if s[k+1].typ == Token.NUMBER:
                        p.setX(p1.x())
                    if s[k+2].typ == Token.NUMBER:
                        p.setY(p1.y())

                elif kw == _KW.abspaper:
                    if s[k+1].typ == Token.NUMBER:
                        p.setX(pt2iu(s[k+1].num))
                    if s[k+2].typ == Token.NUMBER:
                        p.setY(pt2iu(s[k+2].num))

                elif kw == _KW.reldata:
                    p1 = f.maprel(s[k+1].num, s[k+2].num)
                    p.setX(p.x() + p1.x())
                    p.setY(p.y() + p1.y())

                elif kw == _KW.relpaper:
                    p.setX(p.x() + pt2iu(s[k+1].num) * math.cos(phi)
                           - pt2iu(s[k+2].num) * math.sin(phi))
                    p.setY(p.y() + pt2iu(s[k+1].num) * math.sin(phi)
                           + pt2iu(s[k+2].num) * math.cos(phi))

                elif kw == _KW.rotdata:
                    p1 = f.maprel(s[k+1].num, s[k+2].num)
                    phi = math.atan2(p1.y(), p1.x())

                elif kw == _KW.rotpaper:
                    phi = s[k+1].num
                    k -= 1  # only one number

                elif kw == _KW.at:
                    p = f.get_location(s[k+1].str)
                    k -= 1

                elif kw == _KW.atx:
                    p.setX(f.get_location(s[k+1].str).x())
                    k -= 1

                elif kw == _KW.aty:
                    p.setY(f.get_location(s[k+1].str).y())
                    k -= 1

                elif kw == _KW.retract:
                    r_l = pt2iu(s[k+1].num)
                    if s[k+2].typ == Token.NUMBER:
                        r_r = pt2iu(s[k+2].num)
                    else:
                        r_r = r_l
                        k -= 1  # only one number

                k += 3  # skip keyword and both number slots
            k += 1  # skip CLOSEPAREN

            pts.append(p)
            retract_l.append(r_l)
            retract_r.append(r_r)

        # Build list of polylines, splitting at retraction points
        ppp: list[QPolygonF] = []
        pcurrent: list[QPointF] = []
        N = len(pts)

        for n in range(N):
            p = pts[n]

            if n > 0 and (retract_l[n] != 0 or retract_r[n] != 0):
                dp = p - pts[n-1]
                phi = math.atan2(dp.y(), dp.x())
                pcurrent.append(
                    p - QPointF(math.cos(phi) * retract_l[n],
                                math.sin(phi) * retract_
