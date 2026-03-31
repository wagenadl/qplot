# cmdsave.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from .command import Command
from .token_ import Token

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure


@Command.register("save")
class CmdSave(Command):
    """Record a filename (and optional resolution/quality) for saving.

    Syntax:
        save filename [resolution [quality]]

    Actual saving is performed by Renderer, which reads back the
    filename(), resolution(), and quality() accessors.
    """

    def __init__(self) -> None:
        super().__init__()
        self._ofn:  str   = ""
        self._reso: float = 300.0
        self._qual: int   = 95

    def _usage(self) -> bool:
        return self.error("Usage: save filename [resolution [quality]]")

    def parse(self, s: Statement) -> bool:
        if 2 <= len(s) <= 4 and s[1].typ == Token.STRING:
            self._ofn = s[1].str
            if len(s) >= 3 and s[2].typ == Token.NUMBER:
                self._reso = s[2].num
            if len(s) >= 4 and s[3].typ == Token.NUMBER:
                self._qual = int(s[3].num)
            return True
        return self._usage()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        pass  # saving is performed by Renderer

    def filename(self) -> str:
        return self._ofn

    def resolution(self) -> float:
        return self._reso

    def quality(self) -> int:
        return self._qual
