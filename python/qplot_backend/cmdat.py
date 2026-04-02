# cmdat.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtCore import Qt

from .command import Command
from .token_ import Token
from .slightly import slightly_less, slightly_more
from .error import Error

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


def _is_abs(s: str) -> bool:
    return s in ("abs", "absolute")


def _hori_align(s: str) -> int:
    # These values are used arithmetically in render(), not just as an enum.
    return {"left": 0, "center": 1, "right": 2}.get(s, -1)


def _vert_align(s: str) -> int:
    return {"top": 0, "middle": 1, "bottom": 2}.get(s, -1)


@Command.register("at")
class CmdAt(Command):
    """Set the current anchor point.

    Syntax:
        at -
        at x y
        at x y phi
        at x y dx dy
        at x y ID
        at ID ...
        at ID ... phi
        at ID ... dx dy
    """

    def _usage(self) -> bool:
        return self.error(
            "Usage: at x y (dx dy)|phi | - | x y ID | ID ... (phi)"
        )

    def parse(self, s: Statement) -> bool:
        if len(s) < 2:
            return self._usage()

        if s[1].typ == Token.CAPITAL:
            # at ID ...
            i1 = 2
            while i1 < len(s) and s[i1].typ == Token.CAPITAL:
                i1 += 1
            di = len(s) - i1
            if di == 0:
                return True                                      # at ID ...
            if di == 1:
                return True if s[i1].typ == Token.NUMBER \
                    else self._usage()                           # at ID ... phi
            if di == 2:
                return True if (s[i1].typ == Token.NUMBER
                                and s[i1 + 1].typ == Token.NUMBER) \
                    else self._usage()                           # at ID ... dx dy
            return self._usage()

        if len(s) == 2:
            return True if s[1].typ == Token.DASH else self._usage()  # at -

        hori_ok = (
            s[1].typ == Token.NUMBER
            or s[1].typ == Token.DASH
            or (s[1].typ == Token.BAREWORD
                and (_hori_align(s[1].str) >= 0 or _is_abs(s[1].str)))
        )
        if not hori_ok:
            return self._usage()

        vert_ok = (
            s[2].typ == Token.NUMBER
            or s[2].typ == Token.DASH
            or (s[2].typ == Token.BAREWORD
                and (_vert_align(s[2].str) >= 0 or _is_abs(s[2].str)))
        )
        if not vert_ok:
            return self._usage()

        if len(s) == 3:
            return True                                          # at x y

        if s[3].typ == Token.CAPITAL and len(s) == 4:
            return True                                          # at x y ID

        if s[3].typ != Token.NUMBER:
            return self._usage()

        if len(s) == 4:
            return True                                          # at x y phi

        if s[4].typ != Token.NUMBER:
            return self._usage()

        return True if len(s) == 5 else self._usage()           # at x y dx dy

    def data_range(self, s: Statement) -> QRectF:
        """Return a tiny bbox around (x, y) if both are numeric, else empty."""
        if len(s) < 3:
            return QRectF()
        if s[1].typ == Token.NUMBER and s[2].typ == Token.NUMBER:
            x, y = s[1].num, s[2].num
            return QRectF(
                QPointF(slightly_less(x), slightly_less(y)),
                QPointF(slightly_more(x), slightly_more(y)),
            )
        return QRectF()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        if s[1].typ == Token.CAPITAL:                           # at ID ...
            i1 = 2
            while i1 < len(s) and s[i1].typ == Token.CAPITAL:
                i1 += 1
            p = QPointF(0, 0)
            for i in range(1, i1):
                p += f.get_location(s[i].str)
            p /= (i1 - 1)
            di = len(s) - i1
            if di == 0:
                f.set_anchor(p)
            elif di == 1:
                f.set_anchor(p, s[i1].num)
            elif di == 2:
                f.set_anchor(p, f.angle(s[i1].num, s[i1 + 1].num))
            return

        if len(s) <= 2:                                         # at -
            f.set_anchor(f.extent().topLeft())
            return

        old_anc = f.anchor()

        x = s[1].num if s[1].typ == Token.NUMBER else f.x_axis().min()
        y = s[2].num if s[2].typ == Token.NUMBER else f.y_axis().min()
        anchor = f.map(x, y)

        if s[1].typ == Token.BAREWORD:
            if _is_abs(s[1].str):
                anchor.setX(f.extent().left())
            else:
                a = _hori_align(s[1].str)
                anchor.setX(f.last_bbox().left()
                            + a * f.last_bbox().width() / 2)
        elif s[1].typ == Token.DASH:
            anchor.setX(old_anc.x())

        if s[2].typ == Token.BAREWORD:
            if _is_abs(s[2].str):
                anchor.setY(f.extent().top())
            else:
                a = _vert_align(s[2].str)
                anchor.setY(f.last_bbox().top()
                            + a * f.last_bbox().height() / 2)
        elif s[2].typ == Token.DASH:
            anchor.setY(old_anc.y())

        n = len(s)
        if n == 3:
            f.set_anchor(anchor)                                # at x y
        elif n == 4:
            if s[3].typ == Token.CAPITAL:
                f.set_location(s[3].str, anchor)               # at x y ID
            else:
                f.set_anchor(anchor, s[3].num)                 # at x y phi
        elif n == 5:
            f.set_anchor(anchor, f.angle(s[3].num, s[4].num))  # at x y dx dy

        if dryrun:
            return
        if not f.are_bounding_boxes_shown():
            return

        painter = f.painter()
        painter.save()
        painter.setPen(QPen(QColor(255, 0, 0), 10))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(anchor, 30, 30)
        painter.restore()
