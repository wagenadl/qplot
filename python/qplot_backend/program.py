# program.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems

from __future__ import annotations

from PyQt6.QtCore import QRectF

from .statement import Statement
from .command import Command
from .token_ import Token
from .range_ import Range
from .error import Error

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .figure import Figure


class Program:
    """Parses a list of Statements into Commands and renders them."""

    def __init__(self, label: str = "") -> None:
        self._stmt:   list[Statement]       = []
        self._cmds:   list[Command | None]  = []
        self._is_ok:  bool                  = True
        self._label:  str                   = ""
        self._line:   int                   = 1
        self.reset()
        self.set_label(label)

    def reset(self) -> None:
        self._stmt  = []
        self._cmds  = []
        self._is_ok = True
        self._line  = 1

    def set_label(self, lbl: str) -> None:
        self._label = lbl

    # --- Loading ----------------------------------------------------------

    def read(self, statements: list[Statement]) -> None:
        """Parse a list of statements. Updates is_valid()."""
        self.reset()
        for s in statements:
            self.append(s)
            if not self._is_ok:
                return

    def append(self, s: Statement) -> None:
        """Parse and append one statement. Updates is_valid()."""
        if len(s) and s[0].str == "figsize":
            self.reset()
        self._stmt.append(s)
        if not self._parse(s, self._line):
            self._is_ok = False
        self._line += s.line_count()

    def _parse(self, s: Statement, lineno: int) -> bool:
        """Parse one statement; append the resulting Command (or None).
        Returns True on success; errors are reported via Error()."""
        if len(s) == 0:
            self._cmds.append(None)   # maintain 1:1 with statements
            return True

        if s[0].typ != Token.BAREWORD:
            Error() << f'Missing keyword at "{self._label}" line {lineno}'
            self._cmds.append(None)
            return False

        c = Command.construct(s[0].str)
        if c is None:
            Error() << (f'Unknown keyword "{s[0].str}" '
                        f'at "{self._label}" line {lineno}')
            self._cmds.append(None)
            return False

        if not c.parse(s):
            Error() << f'Syntax error at "{self._label}" line {lineno}'
            self._cmds.append(None)
            return False

        self._cmds.append(c)
        return True

    # --- Queries ----------------------------------------------------------

    def is_valid(self) -> bool:
        return self._is_ok

    def __len__(self) -> int:
        return len(self._cmds)

    def __getitem__(self, idx: int) -> Statement:
        if 0 <= idx < len(self._stmt):
            return self._stmt[idx]
        return Statement()

    def command(self, idx: int) -> Command | None:
        """Return the Command at idx, or None for empty/failed statements."""
        if 0 <= idx < len(self._cmds):
            return self._cmds[idx]
        return None

    def panels(self, upto: int = -1) -> set[str]:
        """Return the set of all panel IDs referenced up to statement upto."""
        pp: set[str] = {"-"}
        limit = len(self._cmds) if upto < 0 else upto
        for k in range(limit):
            s = self._stmt[k]
            if len(s) >= 2 and s[0].str == "panel":
                pp.add(s[1].str)
        return pp

    def data_range(self, panel: str = "-", upto: int = -1) -> QRectF:
        """Return the union of data ranges for all commands in panel."""
        r = QRectF()
        in_panel = (panel == "-")
        limit = len(self._cmds) if upto < 0 else upto
        for k in range(limit):
            s = self._stmt[k]
            if len(s) >= 2 and s[0].str == "panel":
                in_panel = (s[1].str == panel)
            if in_panel and self._cmds[k] is not None:
                xl = self._cmds[k].xlim(s)
                if not xl.empty():
                    r.setLeft(xl.min())
                    r.setRight(xl.max())
                    continue
                yl = self._cmds[k].ylim(s)
                if not yl.empty():
                    r.setTop(yl.min())
                    r.setBottom(yl.max())
                    continue
                r1 = self._cmds[k].data_range(s)
                if r1.width() or r1.height():
                    r = r.united(r1)
        return r

    # --- Rendering --------------------------------------------------------

    def render(self, f: Figure, dryrun: bool = False,
               upto: int = -1) -> int:
        """Render the program into figure f.
        Returns the index of the next statement to render."""
        f.reset()
        if not self._is_ok:
            return 0

        limit = len(self._cmds) if upto < 0 else upto
        for l in range(limit):
            if self._cmds[l] is not None:
                self._cmds[l].render(self._stmt[l], f, dryrun)
                if dryrun and f.check_fudged():
                    f.end_groups()
                    f.leave_panel()
                    return l

        f.end_groups()
        f.leave_panel()
        return limit
