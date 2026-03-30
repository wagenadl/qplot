# cmdalignaxes.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from command import Command
from whichaxis import WhichAxis
from range import Range
from error import Error
from token_ import Token

if TYPE_CHECKING:
    from statement import Statement
    from figure import Figure

from PyQt6.QtCore import QPointF

_SHIFT_TOLERANCE = 0.1


def _usage(self) -> bool:
    return self.error("Usage: alignaxes x|y|xy ID ...\n")


@Command.register("alignaxes")
class CmdAlignAxes(Command):
    """'alignaxes' reduces the placement of axes so that multiple panels
    line up.

    Syntax:
        alignaxes x  ID ...
        alignaxes y  ID ...
        alignaxes xy ID ...

    Note: does not yet work for rotated axes.
    """

    def _usage(self) -> bool:
        return self.error("Usage: alignaxes x|y|xy ID ...\n")

    def parse(self, s: Statement) -> bool:
        if len(s) < 3:
            return self._usage()
        if s[1].typ != Token.BAREWORD:
            return self._usage()
        if s[1].str not in ("x", "y", "xy"):
            return self._usage()
        for i in range(2, len(s)):
            if s[i].typ != Token.CAPITAL:
                return self._usage()
        return True

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        share_x = "x" in s[1].str
        share_y = "y" in s[1].str

        ids: list[str] = []
        for i in range(2, len(s)):
            if f.has_panel(s[i].str):
                ids.append(s[i].str)
            else:
                Error() << "Unknown panel: " << s[i].str
                return

        f.leave_panel()

        if share_x:
            self._align(f, ids, WhichAxis.x())
        if share_y:
            self._align(f, ids, WhichAxis.y())

    def _align(self, f: Figure, ids: list[str],
               de: WhichAxis) -> None:
        groups = de.ordered_groups(f, ids)

        # Find union of extents in each group
        pxx: list[Range] = []
        # Find min and max data coordinates represented in each group
        dxx: list[Range] = []

        for group in groups:
            px = Range()
            for id_ in group:
                px.unionize(de.rect_range(f.panel_ref(id_).desired_extent))
            pxx.append(px)

            dx = Range()
            for id_ in group:
                axis = de.axis(f.panel_ref(id_))
                dx.extend(axis.rev(de.repoint(QPointF(0, 0), px.min())))
                dx.extend(axis.rev(de.repoint(QPointF(0, 0), px.max())))
            dxx.append(dx)

        # Find the smallest scale across all groups
        scale = 1.0
        for k, group in enumerate(groups):
            sc = pxx[k].range() / dxx[k].range()
            if k == 0 or sc < scale:
                scale = sc

        # Calculate the Placement that ensures the appropriate mapping.
        # We need:
        #   a*dx0 + b = px0   (1)
        #   a*dx1 + b = px1   (2)
        # Subtracting: a = (px1-px0) / (dx1-dx0)
        #              b = px0 - a*dx0
        #
        # If changing scale to a' from another group, we still want the
        # centre to match:
        #   a'*(dx0+dx1)/2 + b = (px0+px1)/2
        #   b = (px0+px1)/2 - a'*(dx0+dx1)/2

        for k, group in enumerate(groups):
            dx = dxx[k]
            px = pxx[k]
            x0 = dx.min()
            x1 = dx.max()

            for id_ in group:
                axis = de.axis(f.panel_ref(id_))
                rev = de.point(axis.maprel(1)) < 0
                # rev: (d-, d+) -> (p+, p-)  rather than  (d-, d+) -> (p-, p+)
                px0 = px.max() if rev else px.min()
                px1 = px.min() if rev else px.max()
                a = -scale if rev else scale
                b = (px0 + px1) / 2 - a * (x0 + x1) / 2
                PX0 = a * axis.min() + b
                PX1 = a * axis.max() + b

                if (math.fabs(de.point(axis.minp()) - PX0) > _SHIFT_TOLERANCE
                        or math.fabs(de.point(axis.maxp()) - PX1) > _SHIFT_TOLERANCE):
                    axis.set_placement(de.repoint(QPointF(), PX0),
                                       de.repoint(QPointF(), PX1))
                    f.mark_fudged()
