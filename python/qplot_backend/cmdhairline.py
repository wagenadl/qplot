# cmdhairline.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems

from __future__ import annotations

from typing import TYPE_CHECKING

from .command import Command
from .token_ import Token

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


@Command.register("hairline")
class CmdHairline(Command):
    """Set the hairline width.

    Syntax:
        hairline 1|0
    """

    def _usage(self) -> bool:
        return self.error("Usage: hairline width")

    def parse(self, s: Statement) -> bool:
        if len(s) == 2 and s[1].typ == Token.NUMBER:
            return True
        return self._usage()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        f.set_hairline(s[1].num)
