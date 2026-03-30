# pipereader.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import sys

from PyQt6.QtCore import QMutex, QMutexLocker, QThread, pyqtSignal

from .statement import Statementfrom .error import Error

class PipeReader(QThread):
    """Reads QPlot statements from stdin on a background thread.

    Emits ready() each time a statement is successfully read.
    Callers drain the queue with read_queue().
    """

    ready: pyqtSignal = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._mutex: QMutex           = QMutex()
        self._queue: list[Statement]  = []

    def __del__(self) -> None:
        if self.isRunning():
            self.terminate()

    # --- QThread entry point ----------------------------------------------

    def run(self) -> None:
        source = sys.stdin.buffer   # binary stdin, cross-platform
        line = 1
        while True:
            s = Statement()
            n = s.read(source)
            if n:
                self._mutex.lock()
                self._queue.append(s)
                self._mutex.unlock()
                self.ready.emit()
            else:
                if source.read(0) == b"" and source.readable():
                    # EOF — check by attempting a zero-byte read
                    pass
                try:
                    peek = source.peek(1) if hasattr(source, 'peek') else b"x"
                except Exception:
                    peek = b""
                if not peek:
                    Error() << "EOF"
                    break
                else:
                    Error() << f"Read error at line {line} of stdin"
            line += s.line_count()

    # --- Public interface -------------------------------------------------

    def read_queue(self) -> list[Statement]:
        """Atomically drain and return all queued statements."""
        locker = QMutexLocker(self._mutex)
        result = self._queue
        self._queue = []
        return result
