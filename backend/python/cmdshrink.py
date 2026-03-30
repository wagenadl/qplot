# cmdshrink.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF, QRectF

from .command import Command
from .token_ import Token
from .factor import pt2iu
from .error import Error

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure

_SHRINK_DEFAULT = 0.2  # pt


@Command.register("shrink")
class CmdShrink(Command):
    """Reduce axis placement to fit content inside the panel extent.

    Syntax:
        shrink
        shrink margin_pt
        shrink margin_pt ratio

    Default margin is 0.2 pt. Default ratio is unspecified (x and y
    are adjusted independently). Does not work for rotated axes, and
    assumes the y-axis runs up.
    """

    def _usage(self) -> bool:
        return self.error("Usage: shrink [margin_pt] [ratio]\n")

    def parse(self, s: Statement) -> bool:
        if len(s) == 1:
            return True
        if len(s) == 2 and s[1].typ == Token.NUMBER:
            return True
        if (len(s) == 3
                and s[1].typ in (Token.NUMBER, Token.DASH)
                and s[2].typ == Token.NUMBER):
            return True
        return self._usage()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        mrg = pt2iu(_SHRINK_DEFAULT)
        if len(s) >= 2 and s[1].typ == Token.NUMBER:
            mrg = pt2iu(s[1].num)

        has_ratio = len(s) >= 3
        ratio     = s[2].num if has_ratio else 1.0

        actual  = f.full_bbox()   # paper coords of panel content at present
        desired = f.extent()      # desired paper coords of panel

        dleft   = actual.left()   - desired.left()    # +ve means content is inside
        dright  = desired.right() - actual.right()
        dtop    = actual.top()    - desired.top()
        dbottom = desired.bottom()- actual.bottom()

        x0 = QPointF(f.x_axis().minp())   # paper coords of data range
        x1 = QPointF(f.x_axis().maxp())
        y0 = QPointF(f.y_axis().minp())
        y1 = QPointF(f.y_axis().maxp())

        old_dx = x1.x() - x0.x()   # paper width of data area
        old_dy = y1.y() - y0.y()   # paper height of data area

        # Push axes inward wherever content overflows the margin
        if dleft < mrg:
            x0 += QPointF(2 * mrg - dleft, 0)
        if dright < mrg:
            x1 -= QPointF(2 * mrg - dright, 0)
        if dtop < mrg:
            y1 += QPointF(0, 2 * mrg - dtop)
        if dbottom < mrg:
            y0 -= QPointF(0, 2 * mrg - dbottom)

        new_dx = x1.x() - x0.x()
        new_dy = y1.y() - y0.y()

        # Fudge failure: axes have flipped sign (collapsed past zero)
        if new_dx * old_dx < 0 or new_dy * old_dy < 0:
            Error() << (f"Fudge failure ({old_dx},{old_dy}) "
                        f"-> ({new_dx},{new_dy})")
            f.mark_fudge_failure()
            return

        # Optionally enforce an aspect ratio
        if has_ratio:
            dpx  = math.fabs(new_dx)
            dpy  = math.fabs(new_dy)
            xrat = math.fabs(dpx / (f.x_axis().max() - f.x_axis().min()))
            yrat = math.fabs(dpy / (f.y_axis().max() - f.y_axis().min()))
            myrat = yrat / xrat
            if myrat > ratio:           # too tall — shrink height
                adj = 0.5 * dpy * (1 - ratio / myrat)
                y1 += QPointF(0,  adj)
                y0 -= QPointF(0,  adj)
            elif myrat < ratio:         # too wide — shrink width
                adj = 0.5 * dpx * (1 - myrat / ratio)
                x1 -= QPointF(adj, 0)
                x0 += QPointF(adj, 0)

        # Only mark fudged if axes actually moved by more than the margin
        def manhattan(p: QPointF) -> float:
            return math.fabs(p.x()) + math.fabs(p.y())

        if (manhattan(x0 - f.x_axis().minp()) > mrg
                or manhattan(x1 - f.x_axis().maxp()) > mrg
                or manhattan(y0 - f.y_axis().minp()) > mrg
                or manhattan(y1 - f.y_axis().maxp()) > mrg):
            f.x_axis().set_placement(x0, x1)
            f.y_axis().set_placement(y0, y1)
            f.mark_fudged()
