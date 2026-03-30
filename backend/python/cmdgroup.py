# cmdgroup.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from typing import TYPE_CHECKING

from command import Command

if TYPE_CHECKING:
    from statement import Statement
    from figure import Figure


@Command.register("group")
class CmdGroup(Command):

    def _usage(self) -> bool:
        return self.error("Usage: group\n")

    def parse(self, s: Statement) -> bool:
        return True if len(s) == 1 else self._usage()

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        f.start_group()
