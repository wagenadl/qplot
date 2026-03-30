# cmdendgroup.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen

from .command import Command

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


@Command.register("endgroup")
class CmdEndGroup(Command):

    def _usage(self) -> bool:
        return self.error("Usage: endgroup\n")

    def parse(self, s: Statement) -> bool:
        return True if len(s) == 1 else self._usage()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        f.end_group()
        if dryrun:
            return
        if not f.are_bounding_boxes_shown():
            return
        painter = f.painter()
        painter.save()
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(
            QColor(0, 180, 0),
            8,
            Qt.PenStyle.DotLine,
            Qt.PenCapStyle.RoundCap,
        ))
        painter.drawRect(f.last_bbox())
        painter.restore()
