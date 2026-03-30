# filereader.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from dataclasses import dataclass, field

from PyQt6.QtCore import (
    QDateTime, QFileInfo, QMutex, QMutexLocker,
    QThread, QTimer, pyqtSignal,
)
from PyQt6.QtCore import QFileSystemWatcher

from statement import Statement


# ---------------------------------------------------------------------------
# Contents — result of a read attempt
# ---------------------------------------------------------------------------

@dataclass
class Contents:
    valid:    bool            = False
    contents: list[Statement] = field(default_factory=list)
    error:    str             = ""


# ---------------------------------------------------------------------------
# FileReader
# ---------------------------------------------------------------------------

class FileReader(QThread):
    """Reads a QPlot program file, and re-reads it automatically when it
    changes on disk (when run as a thread via exec()).

    Emits ready() whenever the file has been re-read, even with errors.
    """

    ready: pyqtSignal = pyqtSignal()

    def __init__(self, filename: str) -> None:
        super().__init__()
        self._filename:  str       = filename
        self._cont:      Contents  = Contents()
        self._mutex:     QMutex    = QMutex()
        self._fsw:       QFileSystemWatcher | None = None
        self._timer:     QTimer | None             = None
        self._last_mod:  QDateTime = QDateTime()
        self._last_size: int       = 0
        self._waiting:   bool      = False

        self._cont = self._read()

    def __del__(self) -> None:
        if self.isRunning():
            self.terminate()

    # --- QThread entry point ----------------------------------------------

    def run(self) -> None:
        self._fsw = QFileSystemWatcher()
        self._fsw.addPath(self._filename)
        self._waiting = False

        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.setInterval(100)
        self._timer.timeout.connect(self._tick)
        self._fsw.fileChanged.connect(self._file_changed)

        # Run the thread's event loop until the thread is stopped
        from PyQt6.QtCore import QEventLoop
        loop = QEventLoop()
        loop.exec()

        self._fsw = None
        self._timer = None

    # --- File change handling ---------------------------------------------

    def _file_changed(self) -> None:
        if not self._waiting:
            self._waiting = True
            fi = QFileInfo(self._filename)
            self._last_mod  = fi.lastModified()
            self._last_size = fi.size()
            self._timer.start()

    def _tick(self) -> None:
        self._timer.stop()
        fi = QFileInfo(self._filename)
        new_mod  = fi.lastModified()
        new_size = fi.size()

        if new_size != self._last_size or new_mod > self._last_mod:
            # File changed again while we were waiting — restart timer
            self._last_mod  = new_mod
            self._last_size = new_size
            self._timer.start()
            return

        c = self._read()
        self._mutex.lock()
        self._cont = c
        self._mutex.unlock()
        self.ready.emit()

        if c.valid:
            self._waiting = False
            self._timer.setInterval(100)
        else:
            # Back off exponentially to avoid flooding errors
            ival = min(self._timer.interval() * 2, 1000)
            self._timer.setInterval(ival)
            self._timer.start()

    # --- Public interface -------------------------------------------------

    def contents(self) -> Contents:
        """Return a snapshot of the most recently read contents."""
        locker = QMutexLocker(self._mutex)
        return Contents(
            valid=self._cont.valid,
            contents=list(self._cont.contents),
            error=self._cont.error,
        )

    # --- Internal read ----------------------------------------------------

    def _read(self) -> Contents:
        """Read and parse the file. Returns a Contents with valid=True on success."""
        import sys
        c = Contents()

        if self._filename in ("-", ""):
            source = sys.stdin.buffer
        else:
            try:
                source = open(self._filename, "rb")
            except OSError:
                c.error = f"Could not open '{self._filename}'"
                return c

        line = 1
        try:
            while True:
                s = Statement()
                n = s.read(source)
                if n == 0:
                    break
                c.contents.append(s)
                line += s.line_count()
        except Exception as exc:
            c.error = f"Read error at line {line} of "{self._filename}": {exc}"
            return c
        finally:
            if self._filename not in ("-", ""):
                source.close()

        c.valid = True
        return c
