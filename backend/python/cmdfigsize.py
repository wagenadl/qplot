# cmdfigsize.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QSizeF

from command import Command
from token_ import Token
from factor import pt2iu

if TYPE_CHECKING:
    from statement import Statement
    from figure import Figure


@Command.register("figsize")
class CmdFigSize(Command):
    """Set the figure size in PostScript points.

    Syntax:
        figsize width_pt height_pt
    """

    def _usage(self) -> bool:
        return self.error("Usage: figsize width_pt height_pt")

    def parse(self, s: Statement) -> bool:
        if (len(s) == 3
                and s[1].typ == Token.NUMBER
                and s[2].typ == Token.NUMBER):
            return True
        return self._usage()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        w = pt2iu(s[1].num)
        h = pt2iu(s[2].num)
        f.set_size(QSizeF(w, h))
