# renderer.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
import os
import sys
import tempfile

from PyQt6.QtCore import QPointF, QRectF, QSizeF
from PyQt6.QtGui import QImage, QPainter, QPageSize
from PyQt6.QtSvg import QSvgGenerator
from PyQt6.QtPdf import QPdfWriter

from .program import Programfrom .figure import Figurefrom .factor import pt2iu, iu2pt, set_factorfrom .error import Errorfrom .cmdsave import CmdSave

class Renderer:
    """Orchestrates pre-rendering (fudge loop) and output to SVG/PDF/image."""

    def __init__(self) -> None:
        self._prog:            Program = Program()
        self._fig:             Figure  = Figure()
        self._maxtries:        int     = 1000
        self._bitmapres:       float   = 300.0
        self._bitmapqual:      int     = 95
        self._overridewidth:   float   = 0.0
        self._overrideheight:  float   = 0.0

    # --- Accessors --------------------------------------------------------

    def program(self) -> Program:
        return self._prog

    def figure(self) -> Figure:
        return self._fig

    # --- Pre-render (fudge/shrink iteration loop) -------------------------

    def prerender(self, upto: int = -1) -> None:
        img = QImage(1, 1, QImage.Format.Format_ARGB32)
        self._fig.set_size(QSizeF(1, 1))
        self._fig.painter().begin(img)
        self._fig.hard_reset()

        for p in self._prog.panels(upto):
            data_extent = self._prog.data_range(p, upto)
            if p == "-":
                self._fig.x_axis().set_data_range(
                    data_extent.left(), data_extent.right())
                self._fig.y_axis().set_data_range(
                    data_extent.top(), data_extent.bottom())
            else:
                self._fig.panel_ref(p).xaxis.set_data_range(
                    data_extent.left(), data_extent.right())
                self._fig.panel_ref(p).yaxis.set_data_range(
                    data_extent.top(), data_extent.bottom())

        iter_count:     dict[int, int] = {}
        max_iter_count: dict[int, int] = {}
        fail       = False
        total_iter = 0

        while True:
            line = self._prog.render(self._fig, dryrun=True, upto=upto)
            if self._fig.check_fudge_failure():
                fail = True
                break
            elif self._fig.check_fudged():
                for k in list(iter_count):
                    if k < line:
                        iter_count[k] = 0
                iter_count[line] = iter_count.get(line, 0) + 1
                total_iter += 1
                max_iter_count[line] = max(
                    max_iter_count.get(line, 0), iter_count[line])
                if iter_count[line] >= self._maxtries:
                    Error() << (f"Shrink iterations exceeded at {line}: "
                                f"{iter_count[line]} >= {self._maxtries}")
                    fail = True
                    break
            else:
                break

        if fail:
            Error() << f'"Shrink" failed after {total_iter} iterations'
            print(f"Iteration detail: {iter_count}", file=sys.stderr)
            print(f"Max iteration detail: {max_iter_count}", file=sys.stderr)

        self._fig.painter().end()

    # --- Format-specific renderers ----------------------------------------

    def render_svg(self, ofn: str, upto: int = -1) -> bool:
        img = QSvgGenerator()
        img.setFileName(ofn)
        img.setResolution(90)
        img.setViewBox(QRectF(
            QPointF(0, 0),
            QSizeF(90. / 72 * iu2pt(self._fig.extent().width()),
                   90. / 72 * iu2pt(self._fig.extent().height())),
        ))
        if not self._fig.painter().begin(img):
            return False
        self._fig.set_hairline(0.25)
        self._fig.painter().scale(90. / 72 * iu2pt(),
                                  90. / 72 * iu2pt())
        self._fig.set_dash_scale(90. / 72 * iu2pt())
        self._fig.painter().translate(self._fig.extent().left(),
                                      self._fig.extent().top())
        self._prog.render(self._fig, dryrun=False, upto=upto)
        self._fig.painter().end()
        return True

    def render_pdf(self, ofn: str, upto: int = -1) -> bool:
        img = QPdfWriter(ofn)
        img.setPageSize(QPageSize(
            QSizeF(iu2pt(self._fig.extent().width()),
                   iu2pt(self._fig.extent().height())),
            QPageSize.Unit.Point,
        ))
        if not self._fig.painter().begin(img):
            return False
        self._fig.set_hairline(0.25)
        dpix = img.logicalDpiX()
        dpiy = img.logicalDpiY()
        self._fig.painter().translate(-10 * dpix / 72., -10 * dpiy / 72.)
        self._fig.painter().scale(iu2pt() * dpix / 72.0,
                                  iu2pt() * dpix / 72.0)
        self._fig.set_dash_scale(iu2pt() * math.sqrt(dpix * dpiy) / 72.0)
        self._fig.painter().translate(-self._fig.extent().left(),
                                      -self._fig.extent().top())
        self._prog.render(self._fig, dryrun=False, upto=upto)
        self._fig.painter().end()
        return True

    def render_image(self, ofn: str, upto: int = -1) -> bool:
        img = QImage(
            int(self._fig.extent().width()),
            int(self._fig.extent().height()),
            QImage.Format.Format_ARGB32,
        )
        img.fill(0xFFFFFFFF)
        self._fig.painter().begin(img)
        self._fig.painter().setRenderHint(QPainter.RenderHint.Antialiasing)
        self._fig.painter().setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self._fig.set_hairline(0)
        self._fig.set_dash_scale(1)
        self._fig.painter().translate(-self._fig.extent().left(),
                                      -self._fig.extent().top())
        self._prog.render(self._fig, dryrun=False, upto=upto)
        self._fig.painter().end()
        if ofn.endswith("jpg") or ofn.endswith("jpeg"):
            return img.save(ofn, quality=self._bitmapqual)
        return img.save(ofn)

    # --- Top-level save ---------------------------------------------------

    def save(self, ofn: str, upto: int = -1) -> bool:
        if ofn == "-":
            ofn = "-.pdf"

        idx = ofn.rfind(".")
        if idx < 0:
            return _error("Output file must have an extension")
        extn = ofn[idx + 1:]

        extn_is_bitmap = extn in ("png", "jpg", "tif", "tiff")
        if extn_is_bitmap:
            set_factor(self._bitmapres / 72)

        # Handle stdout output via a temporary file
        use_tmpf = False
        tmpf_path = ""
        if ofn == f"-.{extn}":
            fd, tmpf_path = tempfile.mkstemp(suffix=f".{extn}")
            os.close(fd)
            ofn = tmpf_path
            use_tmpf = True

        self._fig = Figure()
        self._fig.override_size(QSizeF(pt2iu(self._overridewidth),
                                       pt2iu(self._overrideheight)))
        self.prerender(upto)

        ok = False
        if extn == "svg":
            ok = self.render_svg(ofn, upto)
        elif extn == "pdf":
            ok = self.render_pdf(ofn, upto)
        elif extn_is_bitmap:
            ok = self.render_image(ofn, upto)
        elif extn in ("eps", "ps"):
            return _error("PostScript output is no longer supported")
        else:
            return _error_unknown_extension(extn)

        if not ok:
            return _error_fail_to_save(ofn)

        if use_tmpf:
            try:
                with open(tmpf_path, "rb") as f:
                    while True:
                        chunk = f.read(1024 * 1024)
                        if not chunk:
                            break
                        sys.stdout.buffer.write(chunk)
                sys.stdout.buffer.flush()
            except OSError as e:
                _error(f"Failed to write to stdout: {e}")
            finally:
                os.unlink(tmpf_path)

        return True

    # --- Iteration and override controls ----------------------------------

    def set_max_tries(self, n: int) -> None:
        self._maxtries = n

    def override_width(self, w: float) -> None:
        self._overridewidth = w

    def override_height(self, h: float) -> None:
        self._overrideheight = h

    def set_bitmap_resolution(self, r: float) -> None:
        self._bitmapres = r

    def set_bitmap_quality(self, q: int) -> None:
        self._bitmapqual = q

    def dosaves(self, start: int = 0, end: int = -1) -> None:
        """Execute all CmdSave commands in the given range."""
        limit = len(self._prog) if end < 0 else end
        for k in range(start, limit):
            cmd = self._prog.command(k)
            if isinstance(cmd, CmdSave):
                self.set_bitmap_resolution(cmd.resolution())
                self.set_bitmap_quality(cmd.quality())
                self.save(cmd.filename(), k)


# ---------------------------------------------------------------------------
# Module-level error helpers
# ---------------------------------------------------------------------------

def _error(s: str) -> bool:
    Error() << s
    return False


def _error_fail_to_save(fn: str) -> bool:
    if not fn:
        return _error("Failed to save: no filename")
    err = f'Failed to save as \u201c{fn}\u201d'
    d = os.path.dirname(os.path.abspath(fn))
    if not os.path.isdir(d):
        err += f': The folder \u201c{d}\u201d does not exist.'
    elif not os.access(d, os.W_OK):
        err += f': The folder \u201c{d}\u201d is not writable.'
    elif os.path.exists(fn) and not os.access(fn, os.W_OK):
        err += ': File exists and is not writable.'
    else:
        err += '. (Reason unknown.)'
    return _error(err)


def _error_unknown_extension(extn: str) -> bool:
    if not extn:
        return _error('Failed to save: Filename without an extension.')
    return _error(f'Failed to save: Unknown extension \u201c{extn}\u201d.')
