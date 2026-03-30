# cmdpen.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen

from .command import Commandfrom .token_ import Tokenfrom .factor import pt2iufrom .error import Error
if TYPE_CHECKING:
    from .statement import Statement    from .figure import Figure

_PEN_DEFAULT_LENGTH = 3  # pt

_JOIN_STYLE: dict[str, Qt.PenJoinStyle] = {
    "miterjoin": Qt.PenJoinStyle.MiterJoin,
    "beveljoin":  Qt.PenJoinStyle.BevelJoin,
    "roundjoin":  Qt.PenJoinStyle.RoundJoin,
}

_CAP_STYLE: dict[str, Qt.PenCapStyle] = {
    "flatcap":   Qt.PenCapStyle.FlatCap,
    "squarecap": Qt.PenCapStyle.SquareCap,
    "roundcap":  Qt.PenCapStyle.RoundCap,
}


@Command.register("pen")
class CmdPen(Command):
    """Set pen properties.

    Syntax:
        pen [ID] - | color | width | -alpha |
            miterjoin|beveljoin|roundjoin |
            flatcap|squarecap|roundcap |
            solid|none |
            dash [L1 ...] |
            dot L ...
    """

    def _usage(self) -> bool:
        return self.error(
            "Usage: pen [ID] - | color | width | -alpha | "
            "miterjoin|beveljoin|roundjoin | flatcap|squarecap|roundcap | "
            "solid|none | dash [L1 ...] | dot L ..."
        )

    def parse(self, s: Statement) -> bool:
        if len(s) < 2:
            return self._usage()
        k = 1
        while k < len(s):
            tok = s[k]
            if tok.typ == Token.CAPITAL and k == 1:
                pass                                    # named pen choice
            elif tok.typ == Token.DASH:
                pass                                    # reset pen
            elif tok.typ == Token.NUMBER:
                pass                                    # width or alpha
            elif tok.typ == Token.BAREWORD:
                w = tok.str
                if w in _JOIN_STYLE or w in _CAP_STYLE:
                    pass
                elif w in ("solid", "none"):
                    pass
                elif w in ("dash", "dot"):
                    if k + 1 < len(s) and s.is_numeric(k + 1):
                        next_k = s.next_index(k + 1) - 1
                        if next_k > 0:
                            k = next_k
                        else:
                            return self._usage()    # bad vector
                    # else: no vector follows — OK
                elif QColor(w).isValid():
                    pass
                else:
                    return self._usage()
            else:
                return self._usage()
            k += 1
        return True

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        from .figure import Figure as FigureClass  # avoid circular at module level        p = QPen(f.painter().pen())
        named_pen = False

        k = 1
        while k < len(s):
            tok = s[k]

            if tok.typ == Token.CAPITAL and k == 1:
                f.choose_pen(tok.str)
                p = QPen(f.painter().pen())
                named_pen = True

            elif tok.typ == Token.DASH:
                p = FigureClass.default_pen()

            elif tok.typ == Token.NUMBER:
                if tok.num == 0:
                    p.setWidthF(pt2iu(f.hairline()))
                elif tok.num > 0:
                    p.setWidthF(pt2iu(tok.num))
                else:
                    c = QColor(p.color())
                    c.setAlphaF(-tok.num)
                    p.setColor(c)
                if p.style() == Qt.PenStyle.NoPen:
                    p.setStyle(Qt.PenStyle.SolidLine)

            elif tok.typ == Token.BAREWORD:
                w = tok.str

                if w in _JOIN_STYLE:
                    p.setJoinStyle(_JOIN_STYLE[w])

                elif w in _CAP_STYLE:
                    p.setCapStyle(_CAP_STYLE[w])

                elif w == "none":
                    p.setStyle(Qt.PenStyle.NoPen)

                elif w == "solid":
                    p.setStyle(Qt.PenStyle.SolidLine)

                elif w == "dash":
                    pw = p.widthF()
                    if pw == 0:
                        pw = f.dash_scale() / f.painter().transform().m11()
                    pat: list[float] = []
                    flat_cap = p.capStyle() == Qt.PenCapStyle.FlatCap
                    if k + 1 < len(s) and s.is_numeric(k + 1):
                        for x in s.data(k + 1):
                            pat.append((1.0 if flat_cap else 0.001)
                                       if x == 0 else pt2iu(x) / pw)
                        k = s.next_index(k + 1) - 1
                    else:
                        pat.append(pt2iu(_PEN_DEFAULT_LENGTH) / pw)
                    # Duplicate odd-length patterns to make them even
                    if len(pat) & 1:
                        pat = pat + pat
                    p.setDashPattern(pat)

                elif w == "dot":
                    pw = p.widthF()
                    if pw == 0:
                        pw = f.dash_scale() / f.painter().transform().m11()
                    pat = []
                    flat_cap = p.capStyle() == Qt.PenCapStyle.FlatCap
                    if k + 1 < len(s) and s.is_numeric(k + 1):
                        for x in s.data(k + 1):
                            pat.append(1.0 if flat_cap else 0.001)
                            pat.append(pt2iu(x) / pw)
                        k = s.next_index(k + 1) - 1
                    else:
                        pat.append(0.001)
                        pat.append(pt2iu(_PEN_DEFAULT_LENGTH) / pw)
                    p.setDashPattern(pat)

                elif QColor(w).isValid():
                    p.setColor(QColor(w))
                    if p.style() == Qt.PenStyle.NoPen:
                        p.setStyle(Qt.PenStyle.SolidLine)

                else:
                    Error() << "pen render surprise"

            k += 1

        f.painter().setPen(p)
        if named_pen:
            f.store_pen()
