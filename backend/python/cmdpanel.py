# cmdpanel.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QRectF

from .command import Commandfrom .token_ import Tokenfrom .factor import pt2iu
if TYPE_CHECKING:
    from .statement import Statement    from .figure import Figure

@Command.register("panel")
class CmdPanel(Command):
    """Select or create a panel.

    Syntax:
        panel -               (leave current panel, select none)
        panel ID              (select panel by ID)
        panel ID x y w h      (select panel and set its extent in pt)
    """

    def _usage(self) -> bool:
        return self.error("Usage: panel ID [x y w h] | -")

    def parse(self, s: Statement) -> bool:
        if len(s) == 2 and s[1].typ == Token.DASH:
            return True
        if (len(s) == 2
                and s[1].typ in (Token.CAPITAL, Token.BAREWORD)):
            return True
        if (len(s) == 6
                and s[1].typ in (Token.CAPITAL, Token.BAREWORD)
                and all(s[k].typ == Token.NUMBER for k in range(2, 6))):
            return True
        return self._usage()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        f.leave_panel()
        if s[1].typ == Token.DASH:
            return
        f.choose_panel(s[1].str)
        if len(s) < 6:
            return
        area = QRectF(
            pt2iu(s[2].num), pt2iu(s[3].num),
            pt2iu(s[4].num), pt2iu(s[5].num),
        )
        f.set_extent(area)
