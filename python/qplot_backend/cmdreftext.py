# cmdreftext.py - This file is part of QPlot

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


@Command.register("reftext")
class CmdRefText(Command):
    """Set the reference text string used by CmdText for alignment.

    Syntax:
        reftext             (clears the reference text)
        reftext 'string'    (sets the reference text)
        reftext '+string'   (appends to the reference text)
    """

    def _usage(self) -> bool:
        return self.error("Usage: reftext [string]")

    def parse(self, s: Statement) -> bool:
        if len(s) == 1:
            return True
        if len(s) == 2 and s[1].typ == Token.STRING:
            return True
        return self._usage()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        if len(s) == 1:
            f.set_ref_text("")
        elif s[1].str.startswith("+"):
            f.set_ref_text(f.ref_text() + s[1].str[1:])
        else:
            f.set_ref_text(s[1].str)
