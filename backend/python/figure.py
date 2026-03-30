# figure.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math

from PyQt6.QtCore import Qt, QPointF, QRectF, QSizeF
from PyQt6.QtGui import QBrush, QFont, QPainter, QPen, QTransform

from axis import Axis
from panel import Panel
from marker import Marker
from align import Align
from groupdata import GroupData
from textshiftaccum import TextShiftAccum
from factor import pt2iu
from error import Error

_DEFAULT_HAIR = 0.25


class Figure:
    """Central state object for a QPlot figure.

    Holds axes, panels, painter state, markers, anchors, and group stack.
    """

    def __init__(self) -> None:
        # All instance variables declared and typed here.
        # Assigned proper values by hard_reset() / reset() below.
        self._hairline:      float                  = _DEFAULT_HAIR
        self._showbboxes:    bool                   = False
        self._figextent:     QRectF                 = QRectF()
        self._panels:        dict[str, Panel]       = {}
        self._dashscale:     float                  = 1.0
        self._current_panel: str                    = "-"
        self._xax:           Axis                   = Axis()
        self._yax:           Axis                   = Axis()
        self._fullbbox:      QRectF                 = QRectF()
        self._cumulbbox:     QRectF                 = QRectF()
        self._lastbbox:      QRectF                 = QRectF()
        self._pntr:          QPainter               = QPainter()
        self._anch:          QPointF                = QPointF(0, 0)
        self._anchang:       float                  = 0.0
        self._valign:        Align.VAlign           = Align.VAlign.BASE
        self._halign:        Align.HAlign           = Align.HAlign.CENTER
        self._reftxt:        str                    = ""
        self._mrkr:          Marker                 = Marker()
        self._pens:          dict[str, QPen]        = {}
        self._brushes:       dict[str, QBrush]      = {}
        self._current_pen:   str                    = "A"
        self._current_brush: str                    = "A"
        self._groupstack:    list[GroupData]        = []
        self._locations:     dict[str, QPointF]     = {}
        self._fudged:        bool                   = False
        self._fudge_failure: bool                   = False
        self._textshiftaccum: TextShiftAccum        = TextShiftAccum()
        self._override_wh:   QSizeF                 = QSizeF()
        self.hard_reset()

    # --- Reset ------------------------------------------------------------

    def hard_reset(self) -> None:
        """Full reset — equivalent to restarting the program."""
        self._figextent  = QRectF(QPointF(0, 0), QSizeF(72 * 6, 72 * 4))
        self._panels     = {}
        self._dashscale  = 1.0
        self._current_panel = "-"
        self._replace_axes()
        self.reset()

    def reset(self) -> None:
        """Soft reset of style and state, preserving panel geometry."""
        self._halign        = Align.HAlign.CENTER
        self._valign        = Align.VAlign.BASE
        self._current_pen   = "A"
        self._current_brush = "A"
        self._current_panel = "-"
        self._pens          = {}
        self._brushes       = {}
        self._reftxt        = ""
        self._mrkr          = Marker()
        self._anch          = QPointF(0, 0)
        self._anchang       = 0.0
        self.clear_bbox(full=True)
        for p in self._panels.values():
            p.fullbbox  = QRectF()
            p.cumulbbox = QRectF()
            p.lastbbox  = QRectF()
        self._groupstack = []
        if self._pntr.isActive():
            font = QFont("Helvetica")
            font.setPixelSize(int(pt2iu(10)))
            self._pntr.setFont(font)
            self._pntr.setPen(Figure.default_pen())
        self._fudged        = False
        self._fudge_failure = False

    # --- Size and extent --------------------------------------------------

    def set_size(self, wh_pt: QSizeF) -> None:
        owh = self._override_wh
        if not owh.isEmpty():
            wh_pt = owh
        elif owh.width() > 0:
            wh_pt = QSizeF(owh.width(),
                           owh.width() * wh_pt.height() / wh_pt.width())
        elif owh.height() > 0:
            wh_pt = QSizeF(owh.height() * wh_pt.width() / wh_pt.height(),
                           owh.height())
        if self._figextent.size() == wh_pt:
            return
        self._figextent = QRectF(QPointF(0, 0), wh_pt)
        self._replace_axes()

    def override_size(self, wh: QSizeF) -> None:
        self._override_wh = wh

    def set_extent(self, xywh_pt: QRectF) -> None:
        if self._figextent == xywh_pt:
            return
        if not self._figextent.isEmpty():
            return  # avoid overwriting after rebalance
        self._figextent = xywh_pt
        self._replace_axes()

    def extent(self) -> QRectF:
        return self._figextent

    def override_panel_extent(self, s: str, ext: QRectF) -> None:
        if s == self._current_panel:
            self._figextent = ext
            self._replace_axes()
        else:
            self._panels[s].desired_extent = ext

    def _replace_axes(self) -> None:
        self._xax.set_placement(QPointF(self._figextent.left(),  0),
                                QPointF(self._figextent.right(), 0))
        self._yax.set_placement(QPointF(0, self._figextent.bottom()),
                                QPointF(0, self._figextent.top()))

    # --- Axes -------------------------------------------------------------

    def x_axis(self) -> Axis:
        return self._xax

    def y_axis(self) -> Axis:
        return self._yax

    def map(self, x: float, y: float) -> QPointF:
        return self._xax.map(x) + self._yax.map(y)

    def map_point(self, xy: QPointF) -> QPointF:
        return self._xax.map(xy.x()) + self._yax.map(xy.y())

    def maprel(self, dx: float, dy: float) -> QPointF:
        return self._xax.maprel(dx) + self._yax.maprel(dy)

    def xform(self) -> QTransform:
        xf = QTransform(
            self._xax.maprel(1).x(), 0, 0,
            0, self._yax.maprel(1).y(), 0,
            self._xax.map(0).x() + self._yax.map(0).x(),
            self._yax.map(0).y() + self._xax.map(0).y(), 1,
        )
        return xf

    # --- Bounding boxes ---------------------------------------------------

    def clear_bbox(self, full: bool = False) -> None:
        self._lastbbox  = QRectF()
        self._cumulbbox = QRectF()
        if full:
            self._fullbbox = QRectF()

    def set_bbox(self, b: QRectF) -> None:
        self._lastbbox  = b
        self._cumulbbox = self._cumulbbox.united(b)
        self._fullbbox  = self._fullbbox.united(b)

    def force_bbox_x(self, x0: float, x1: float) -> None:
        self._fullbbox.setLeft(x0);   self._fullbbox.setRight(x1)
        self._cumulbbox.setLeft(x0);  self._cumulbbox.setRight(x1)

    def force_bbox_y(self, y0: float, y1: float) -> None:
        self._fullbbox.setTop(y0);    self._fullbbox.setBottom(y1)
        self._cumulbbox.setTop(y0);   self._cumulbbox.setBottom(y1)

    def last_bbox(self) -> QRectF:
        return self._lastbbox

    def cumul_bbox(self) -> QRectF:
        return self._cumulbbox

    def full_bbox(self) -> QRectF:
        return self._fullbbox

    # --- Anchor -----------------------------------------------------------

    def set_anchor(self, x_or_pt, y_or_phi: float = 0,
                   dx: float = 1, dy: float = 0) -> None:
        """set_anchor(QPointF, phi)  or  set_anchor(x, y, dx, dy)."""
        if isinstance(x_or_pt, QPointF):
            self._anch    = x_or_pt
            self._anchang = y_or_phi
        else:
            self._anch    = self.map(x_or_pt, y_or_phi)
            self._anchang = self.angle(dx, dy)
        self._textshiftaccum.reset()

    def anchor(self) -> QPointF:
        return self._anch

    def anchor_angle(self) -> float:
        return self._anchang

    def angle(self, dx: float, dy: float) -> float:
        frm = self.map(0, 0)
        to  = self.map(dx, dy)
        d   = to - frm
        return math.atan2(d.y(), d.x())

    # --- Text shift accumulator -------------------------------------------

    def text_shift_accum(self) -> TextShiftAccum:
        return self._textshiftaccum

    def update_text_shift_accum(self, dx: float, dy: float) -> None:
        self._textshiftaccum.update(dx, dy)

    # --- Alignment --------------------------------------------------------

    def set_halign(self, a: Align.HAlign) -> None:
        self._halign = a

    def set_valign(self, a: Align.VAlign) -> None:
        self._valign = a

    def halign(self) -> Align.HAlign:
        return self._halign

    def valign(self) -> Align.VAlign:
        return self._valign

    # --- Ref text ---------------------------------------------------------

    def set_ref_text(self, s: str) -> None:
        self._reftxt = s

    def ref_text(self) -> str:
        return self._reftxt

    # --- Painter ----------------------------------------------------------

    def painter(self) -> QPainter:
        return self._pntr

    # --- Marker -----------------------------------------------------------

    def marker(self) -> Marker:
        return self._mrkr

    # --- Pen and brush ----------------------------------------------------

    def store_pen(self) -> None:
        self._pens[self._current_pen] = self._pntr.pen()

    def store_brush(self) -> None:
        self._brushes[self._current_brush] = self._pntr.brush()

    def choose_pen(self, s: str) -> None:
        self._current_pen = s
        if s in self._pens:
            self._pntr.setPen(self._pens[s])

    def choose_brush(self, s: str) -> None:
        self._current_brush = s
        if s in self._brushes:
            self._pntr.setBrush(self._brushes[s])

    def hairline(self) -> float:
        return self._hairline

    def set_hairline(self, h: float) -> None:
        self._hairline = h
        if self._pntr.isActive():
            pen = QPen(self._pntr.pen())
            pen.setWidthF(pt2iu(self._hairline))
            self._pntr.setPen(pen)

    def set_dash_scale(self, s: float) -> None:
        self._dashscale = s

    def dash_scale(self) -> float:
        return self._dashscale

    # --- Panels -----------------------------------------------------------

    def choose_panel(self, s: str) -> None:
        if s == self._current_panel:
            return
        if self._groupstack:
            Error() << "Warning: panel change while group stack not empty"
            self._groupstack.clear()

        # Save current state into the outgoing panel
        store = self._panels.setdefault(self._current_panel, Panel())
        store.xaxis          = self._xax
        store.yaxis          = self._yax
        store.desired_extent = self._figextent
        store.fullbbox       = self._fullbbox
        store.cumulbbox      = self._cumulbbox
        store.lastbbox       = self._lastbbox

        self._current_panel = s

        # Restore state from the incoming panel
        src = self._panels.setdefault(self._current_panel, Panel())
        self._xax       = src.xaxis
        self._yax       = src.yaxis
        self._figextent = src.desired_extent
        self._fullbbox  = src.fullbbox
        self._cumulbbox = src.cumulbbox
        self._lastbbox  = src.lastbbox

        self.set_anchor(self._figextent.topLeft())

        if s == "-":
            # Returning to top level: fold last panel's bbox upward
            self._fullbbox  = self._fullbbox.united(store.fullbbox)
            self._cumulbbox = self._cumulbbox.united(store.fullbbox)
            self._lastbbox  = store.fullbbox

    def leave_panel(self) -> None:
        self.choose_panel("-")

    def panel_ref(self, p: str) -> Panel:
        """Return mutable Panel for p, creating a blank one if needed."""
        return self._panels.setdefault(p, Panel())

    def panel(self, p: str) -> Panel:
        """Return Panel for p (read-only intent). Returns blank Panel if unknown."""
        return self._panels.get(p, Panel())

    def has_panel(self, p: str) -> bool:
        return p in self._panels

    def current_panel_name(self) -> str:
        return self._current_panel

    def override_panel_extent(self, s: str, ext: QRectF) -> None:
        if s == self._current_panel:
            self._figextent = ext
            self._replace_axes()
        else:
            self._panels.setdefault(s, Panel()).desired_extent = ext

    # --- Group stack ------------------------------------------------------

    def start_group(self) -> None:
        g = GroupData()
        g.bbox       = self._cumulbbox
        g.pen        = self._pntr.pen()
        g.brush      = self._pntr.brush()
        g.pen_name   = self._current_pen
        g.brush_name = self._current_brush
        g.valign     = self._valign
        g.halign     = self._halign
        g.reftext    = self._reftxt
        g.hairline   = self._hairline
        g.font       = self._pntr.font()
        self._groupstack.append(g)
        self._cumulbbox = QRectF()

    def end_group(self) -> None:
        if not self._groupstack:
            Error() << "Warning: pop from empty group stack"
            return
        self._lastbbox = self._cumulbbox
        g = self._groupstack.pop()
        if self._current_pen != g.pen_name:
            self.choose_pen(g.pen_name)
        self._pntr.setPen(g.pen)
        if self._current_brush != g.brush_name:
            self.choose_brush(g.brush_name)
        self._pntr.setBrush(g.brush)
        self._halign    = g.halign
        self._valign    = g.valign
        self._reftxt    = g.reftext
        self._hairline  = g.hairline
        self._pntr.setFont(g.font)
        self._cumulbbox = g.bbox.united(self._lastbbox)

    def end_groups(self) -> None:
        while self._groupstack:
            self.end_group()

    # --- Locations --------------------------------------------------------

    def set_location(self, id_: str, xy: QPointF) -> None:
        self._locations[id_] = xy

    def get_location(self, id_: str) -> QPointF:
        return self._locations.get(id_, QPointF(0, 0))

    # --- Panel hit-test ---------------------------------------------------

    def panel_at(self, xy: QPointF) -> str:
        """Return the name of whichever panel contains xy, or '' if none."""
        if self._current_panel != "-":
            if self._figextent.contains(xy):
                return self._current_panel
        for p, panel in self._panels.items():
            if p != self._current_panel:
                if panel.desired_extent.contains(xy):
                    return p
        if self._current_panel == "-":
            if self._figextent.contains(xy):
                return "-"
        return ""

    # --- Fudge flags ------------------------------------------------------

    def mark_fudged(self) -> None:
        self._fudged = True

    def check_fudged(self) -> bool:
        return self._fudged

    def mark_fudge_failure(self) -> None:
        self._fudged        = True
        self._fudge_failure = True

    def check_fudge_failure(self) -> bool:
        return self._fudge_failure

    # --- Bounding box display ---------------------------------------------

    def show_bounding_boxes(self, b: bool = True) -> None:
        self._showbboxes = b

    def are_bounding_boxes_shown(self) -> bool:
        return self._showbboxes

    # --- Static -----------------------------------------------------------

    @staticmethod
    def default_pen() -> QPen:
        pen = QPen(Qt.GlobalColor.black)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        pen.setWidthF(pt2iu(0.5))
        pen.setMiterLimit(4)
        return pen
