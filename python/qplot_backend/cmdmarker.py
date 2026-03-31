# cmdmarker.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from .command import Command
from .token_ import Token
from .factor import pt2iu
from .marker import Marker

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


_FILL_STYLE: dict[str, Marker.Fill] = {
    "open":  Marker.Fill.OPEN,
    "solid": Marker.Fill.CLOSED,
    "brush": Marker.Fill.BRUSH,
    "spine": Marker.Fill.SPINE,
}

_MARKER_TYPE: dict[str, Marker.Type] = {
    "circle":  Marker.Type.CIRCLE,
    "square":  Marker.Type.SQUARE,
    "diamond": Marker.Type.DIAMOND,
    "left":    Marker.Type.LEFTTRIANGLE,
    "right":   Marker.Type.RIGHTTRIANGLE,
    "up":      Marker.Type.UPTRIANGLE,
    "down":    Marker.Type.DOWNTRIANGLE,
    "penta":   Marker.Type.PENTAGRAM,
    "hexa":    Marker.Type.HEXAGRAM,
    "hbar":    Marker.Type.HBAR,
    "vbar":    Marker.Type.VBAR,
    "plus":    Marker.Type.PLUS,
    "cross":   Marker.Type.CROSS,
    "star":    Marker.Type.STAR,
}


@Command.register("marker")
class CmdMarker(Command):
    """Set marker style properties.

    Syntax:
        marker size|open|solid|brush|spine|
               circle|square|diamond|left|right|up|down|
               penta|hexa|hbar|vbar|plus|cross|star ...
    """

    def _usage(self) -> bool:
        return self.error(
            "Usage: marker size|open|solid|white|brush|circle|square|"
            "diamond|left|right|up|down|penta|hexa|hbar|vbar|plus|cross|star"
        )

    def parse(self, s: Statement) -> bool:
        if len(s) < 2:
            return self._usage()
        for k in range(1, len(s)):
            if s[k].typ == Token.NUMBER:
                continue                          # size
            elif s[k].typ == Token.BAREWORD:
                w = s[k].str
                if w in _MARKER_TYPE or w in _FILL_STYLE:
                    continue
                return self._usage()
            else:
                return self._usage()
        return True

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        for k in range(1, len(s)):
            if s[k].typ == Token.NUMBER:
                f.marker().radius = pt2iu(s[k].num) / 2
            elif s[k].typ == Token.BAREWORD:
                w = s[k].str
                if w in _MARKER_TYPE:
                    f.marker().type = _MARKER_TYPE[w]
                elif w in _FILL_STYLE:
                    f.marker().fill = _FILL_STYLE[w]
