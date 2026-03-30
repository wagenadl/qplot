# cmdylim.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from .command import Command
from .token_ import Token
from .range_ import Range

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


@Command.register("ylim")
class CmdYLim(Command):
    """Override the y-axis data limits.

    Syntax:
        ylim y0 y1
    """

    def _usage(self) -> bool:
        return self.error("Usage: ylim y0 y1")

    def parse(self, s: Statement) -> bool:
        if (len(s) == 3
                and s[1].typ == Token.NUMBER
                and s[2].typ == Token.NUMBER):
            return True
        return self._usage()

    def ylim(self, s: Statement) -> Range:
        return Range(s[1].num, s[2].num)

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        y0, y1 = s[1].num, s[2].num
        f.force_bbox_y(f.map(0, y0).y(), f.map(0, y1).y())
