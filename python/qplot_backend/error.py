# error.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

import sys
from PyQt6.QtCore import QTextStream, QIODevice
from PyQt6.QtCore import QFile

class Error:
    """Accumulates a message and writes it to stderr (or a custom destination)
    when the object is destroyed."""

    _dest: QTextStream | None = None

    def __init__(self):
        self._parts: list[str] = []

    def __lshift__(self, value: object) -> "Error":
        self._parts.append(str(value))
        return self

    def __del__(self):
        msg = "".join(self._parts)
        if Error._dest is not None:
            Error._dest << msg << "\n"
            Error._dest.flush()
        else:
            print(msg, file=sys.stderr)


    @staticmethod
    def set_destination(dest: QTextStream | None) -> None:
        Error._dest = dest
