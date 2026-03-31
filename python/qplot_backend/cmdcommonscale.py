# cmdcommonscale.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF

from .command import Command
from .whichaxis import WhichAxis
from .error import Error
from .token_ import Token

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure

_SCALE_TOLERANCE = 1e-3


@Command.register("commonscale")
class CmdCommonScale(Command):
    """'commonscale' reduces the placement of axes so that multiple panels
    have the same data scale.

    Syntax:
        commonscale x  ID ...
        commonscale y  ID ...
        commonscale xy ID ...

    Note: does not yet work for rotated axes, and assumes y-axis runs up.
    """

    def _usage(self) -> bool:
        return self.error("Usage: commonscale x|y|xy ID ...\n")

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

        ids: set[str] = set()
        for i in range(2, len(s)):
            if f.has_panel(s[i].str):
                ids.add(s[i].str)
            else:
                Error() << "Unknown panel: " << s[i].str
                return

        f.leave_panel()

        if share_x:
            self._scale(f, ids, WhichAxis.x())
        if share_y:
            self._scale(f, ids, WhichAxis.y())

    def _scale(self, f: Figure, ids: set[str], de: WhichAxis) -> None:
        # Find the smallest scale across all panels
        scale = -1.0
        for id_ in ids:
            p = f.panel_ref(id_)
            a = de.axis(p)
            sc1 = math.fabs(de.point(a.maprel(1)))
            if scale < 0 or sc1 < scale:
                scale = sc1

        # Apply that scale to all panels, shrinking any that are too large
        for id_ in ids:
            axis = de.axis(f.panel_ref(id_))
            sc1 = de.point(axis.maprel(1))
            rev = sc1 < 0
            sc1 = math.fabs(sc1)
            px0 = de.point(axis.minp())
            px1 = de.point(axis.maxp())

            if sc1 > scale * (1 + _SCALE_TOLERANCE):
                current_width = de.axis_p_range(axis).range()
                new_width = current_width * scale / sc1
                shift = (current_width - new_width) / 2
                if rev:
                    shift = -shift
                axis.set_placement(de.repoint(QPointF(), px0 + shift),
                                   de.repoint(QPointF(), px1 - shift))
                f.mark_fudged()
