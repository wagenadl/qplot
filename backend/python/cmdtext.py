# cmdtext.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QColor, QPen

from command import Command
from token_ import Token
from factor import pt2iu
from rotate import rotate_rect
from text import Text
from align import Align

if TYPE_CHECKING:
    from statement import Statement
    from figure import Figure


@Command.register("text")
@Command.register("ctext")
class CmdText(Command):
    """Draw a text string at the current anchor point.

    Syntax:
        text 'string'
        text dx dy 'string'
        ctext 'string'
        ctext dx dy 'string'

    ctext uses the text shift accumulator for continuation positioning.
    """

    def _usage(self) -> bool:
        return self.error("Usage: text [dx dy] string")

    def parse(self, s: Statement) -> bool:
        if (len(s) == 4
                and s[1].typ == Token.NUMBER
                and s[2].typ == Token.NUMBER
                and s[3].typ == Token.STRING):
            return True
        if len(s) == 2 and s[1].typ == Token.STRING:
            return True
        return self._usage()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        if len(s) == 2:
            dx, dy  = 0.0, 0.0
            txt     = s[1].str
            shortform = f.text_shift_accum().is_active()
        else:
            dx  = pt2iu(s[1].num)
            dy  = pt2iu(s[2].num)
            txt = s[3].str
            shortform = (s[0].str == "ctext"
                         and f.text_shift_accum().is_active())

        t = Text()
        t.set_font_from_qfont(f.painter().font())
        t.add_interpreted(txt)

        r0 = t.bbox()
        r  = QRectF(r0)

        if shortform:
            dx += f.text_shift_accum().x()
            dy += f.text_shift_accum().y()
        else:
            ref = f.ref_text()
            if ref:
                tref = Text()
                tref.set_font_from_qfont(f.painter().font())
                tref.add_interpreted(ref)
                rr = tref.bbox()
                r.setTop(rr.top())
                r.setBottom(rr.bottom())

            halign = f.halign()
            if halign == Align.HAlign.LEFT:
                dx -= r.left()
            elif halign == Align.HAlign.RIGHT:
                dx -= r.right()
            elif halign == Align.HAlign.CENTER:
                dx -= (r.left() + r.right()) / 2

            valign = f.valign()
            if valign == Align.VAlign.TOP:
                dy -= r.top()
            elif valign == Align.VAlign.BOTTOM:
                dy -= r.bottom()
            elif valign == Align.VAlign.MIDDLE:
                dy -= (r.top() + r.bottom()) / 2
            # BASE: dy unchanged

        # Compute bbox from union of actual and ref rects, rotated to paper
        union_r = r0.united(r).translated(dx, dy)
        rotated = rotate_rect(union_r, f.anchor_angle())
        rotated.translate(f.anchor())
        f.set_bbox(rotated)
        f.text_shift_accum().set_base(dx + t.width(), dy)

        if dryrun:
            return

        if f.are_bounding_boxes_shown():
            f.painter().save()
            f.painter().setPen(QPen(QColor(255, 0, 0), 8))
            f.painter().setBrush(Qt.BrushStyle.NoBrush)
            f.painter().drawRect(rotated)
            f.painter().restore()

        f.painter().save()
        f.painter().translate(f.anchor())
        f.painter().rotate(f.anchor_angle() * 180 / math.pi)
        t.render(f.painter(), QPointF(dx, dy))
        f.painter().restore()
