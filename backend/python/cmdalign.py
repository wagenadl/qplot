# cmdalign.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from .command import Commandfrom .align import Alignfrom .token_ import Token
if TYPE_CHECKING:
    from .statement import Statement    from .figure import Figure

def _halignment(s: str) -> int:
    return {
        "left":   Align.LEFT,
        "right":  Align.RIGHT,
        "center": Align.CENTER,
    }.get(s, -1)


def _valignment(s: str) -> int:
    return {
        "top":    Align.TOP,
        "bottom": Align.BOTTOM,
        "middle": Align.MIDDLE,
        "base":   Align.BASE,
    }.get(s, -1)


@Command.register("align")
class CmdAlign(Command):

    def _usage(self) -> bool:
        return self.error(
            "Usage: align left|right|center|top|bottom|middle|base ..."
        )

    def parse(self, s: Statement) -> bool:
        if len(s) < 2:
            return self._usage()
        for k in range(1, len(s)):
            if s[k].typ == Token.BAREWORD:
                if _valignment(s[k].str) >= 0:
                    continue
                if _halignment(s[k].str) >= 0:
                    continue
            return self._usage()
        return True

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        for k in range(1, len(s)):
            h = _halignment(s[k].str)
            v = _valignment(s[k].str)
            if h >= 0:
                f.set_halign(Align.HAlign(h))
            elif v >= 0:
                f.set_valign(Align.VAlign(v))
