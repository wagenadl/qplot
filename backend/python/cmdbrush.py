# cmdbrush.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor

from .command import Commandfrom .token_ import Token
if TYPE_CHECKING:
    from .statement import Statement    from .figure import Figure

@Command.register("brush")
class CmdBrush(Command):

    def _usage(self) -> bool:
        return self.error("Usage: brush [ID] color|none|opacity ...")

    def parse(self, s: Statement) -> bool:
        if len(s) < 2:
            return self._usage()
        for k in range(1, len(s)):
            if s[k].typ == Token.CAPITAL and k == 1:
                continue                             # named brush choice
            elif s[k].typ == Token.NUMBER:
                continue                             # opacity
            elif s[k].typ == Token.BAREWORD:
                w = s[k].str
                if w == "none":
                    continue
                elif QColor(w).isValid():
                    continue
                else:
                    return self._usage()
            else:
                return self._usage()
        return True

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        b = QBrush(f.painter().brush())
        c = QColor(b.color())
        alpha = c.alphaF()
        new_color = False
        named_brush = False

        for k in range(1, len(s)):
            if s[k].typ == Token.CAPITAL and k == 1:
                f.choose_brush(s[k].str)
                b = QBrush(f.painter().brush())
                c = QColor(b.color())
                alpha = c.alphaF()
                named_brush = True

            elif s[k].typ == Token.NUMBER:
                alpha = max(0.0, min(1.0, s[k].num))
                new_color = True

            elif s[k].typ == Token.BAREWORD:
                w = s[k].str
                if w == "none":
                    b.setColor(QColor("black"))
                    b.setStyle(Qt.BrushStyle.NoBrush)
                elif QColor(w).isValid():
                    c = QColor(w)
                    new_color = True

        if new_color:
            c.setAlphaF(alpha)
            b.setColor(c)
            b.setStyle(Qt.BrushStyle.SolidPattern)

        f.painter().setBrush(b)
        if named_brush:
            f.store_brush()
