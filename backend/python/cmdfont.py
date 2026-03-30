# cmdfont.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtGui import QFont

from .command import Commandfrom .token_ import Tokenfrom .factor import pt2iu
if TYPE_CHECKING:
    from .statement import Statement    from .figure import Figure

@Command.register("font")
class CmdFont(Command):
    """Set the current font.

    Syntax:
        font family [bold] [italic] size_pt
    """

    def _usage(self) -> bool:
        return self.error("Usage: font family [bold] [italic] size")

    def parse(self, s: Statement) -> bool:
        if not (3 <= len(s) <= 5):
            return self._usage()
        if s[1].typ != Token.BAREWORD:
            return self._usage()
        if s[len(s) - 1].typ != Token.NUMBER:
            return self._usage()
        for k in range(2, len(s) - 1):
            if s[k].typ == Token.BAREWORD and s[k].str in ("bold", "italic"):
                continue
            return self._usage()
        return True

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        font = QFont(s[1].str)
        font.setPixelSize(int(pt2iu(s[len(s) - 1].num)))
        for k in range(2, len(s) - 1):
            if s[k].str == "bold":
                font.setWeight(QFont.Weight.Bold)
            elif s[k].str == "italic":
                font.setItalic(True)
        f.painter().setFont(font)
