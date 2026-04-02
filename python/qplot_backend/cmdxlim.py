# cmdxlim.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems

from __future__ import annotations

from typing import TYPE_CHECKING

from .command import Command
from .token_ import Token
from .range_ import Range

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


@Command.register("xlim")
class CmdXLim(Command):
    """Override the x-axis data limits.

    Syntax:
        xlim x0 x1
    """

    def _usage(self) -> bool:
        return self.error("Usage: xlim x0 x1")

    def parse(self, s: Statement) -> bool:
        if (len(s) == 3
                and s[1].typ == Token.NUMBER
                and s[2].typ == Token.NUMBER):
            return True
        return self._usage()

    def xlim(self, s: Statement) -> Range:
        return Range(s[1].num, s[2].num)

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        x0, x1 = s[1].num, s[2].num
        f.force_bbox_x(f.map(x0, 0).x(), f.map(x1, 0).x())
