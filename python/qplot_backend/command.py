# command.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Type

from PyQt6.QtCore import QRectF
import re
import importlib

from .error import Error
from .range_ import Range

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure

_aliases = { "garea": "gline",
             "phatch": "hatch",
             "pmark": "mark",
             "patch": "plot",
             "line": "plot",
             "area": "plot",
             "ctext": "text" }

class Command(abc.ABC):
    """Abstract base class for all plot commands.

    Subclasses register themselves under a keyword using the
    @Command.register("keyword") decorator, which mirrors the C++
    CBuilder<X> static-instance self-registration pattern.
    """

    _builders: dict[str, Type[Command]] = {}

    # --- Registration -----------------------------------------------------

    @staticmethod
    def register(keyword: str):
        """Class decorator that registers a Command subclass by keyword.

        Usage:
            @Command.register("plot")
            class CmdPlot(Command):
                ...
        """
        def decorator(cls: Type[Command]) -> Type[Command]:
            Command._builders[keyword] = cls
            return cls
        return decorator

    @staticmethod
    def construct(keyword: str) -> Command | None:
        """Instantiate and return the Command registered under keyword,
        or None if no such command exists."""
        cls = Command._builders.get(keyword)
        if cls:
            return cls()
        if Command._tryload(keyword):
            cls = Command._builders.get(keyword)
            if cls:
                return cls()
        return None

    @staticmethod
    def _tryload(keyword: str) -> bool:
        if not re.fullmatch(r'[a-z]+', keyword):
            return False
        if keyword in _aliases:
            keyword = _aliases[keyword]
        if importlib.import_module(f".cmd{keyword}",
                                   package="qplot_backend"):
            return True
        return False
        

    # --- Abstract interface -----------------------------------------------

    @abc.abstractmethod
    def parse(self, statement: Statement) -> bool:
        """Check whether the statement is valid.
        Returns True if valid, False otherwise."""
        ...

    @abc.abstractmethod
    def render(self, statement: Statement, figure: Figure,
               dryrun: bool) -> None:
        """Plot the statement to the figure.
        You may assume parse() returned True.
        Update figure's bbox unless this command only sets style.
        If dryrun is True, do not draw anything."""
        ...

    # --- Virtual methods with default implementations --------------------

    def data_range(self, statement: Statement) -> QRectF:
        """Return the extent of the data in axes coordinates.
        Override in commands that plot data. Default returns empty rect."""
        return QRectF()

    def xlim(self, statement: Statement) -> Range:
        """Return x-range overriding limits. Only overridden by CmdXLim."""
        return Range()

    def ylim(self, statement: Statement) -> Range:
        """Return y-range overriding limits. Only overridden by CmdYLim."""
        return Range()

    # --- Protected helpers ------------------------------------------------

    def error(self, message: str) -> bool:
        """Emit an error message and return False."""
        Error() << "Command error: " << message
        return False
