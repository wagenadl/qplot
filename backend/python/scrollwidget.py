# scrollwidget.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math

from PyQt6.QtCore import Qt, QPointF, QRectF, QSizeF
from PyQt6.QtGui import QCursor, QKeyEvent, QMouseEvent, QWheelEvent
from PyQt6.QtWidgets import QWidget

from factor import iu2pt


class ScrollWidget(QWidget):
    """A zoomable, pannable widget base class.

    Subclasses should override paintEvent() and call tlDest()/brDest()
    and scale() to correctly position their content.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._extent_world: QRectF  = QRectF(QPointF(0, 0), QPointF(1000, 1000))
        self._tl_world:     QPointF = QPointF(0, 0)
        self._scalefactor:  float   = iu2pt(1)
        self._scaletofit:   bool    = True
        self._dragging:     bool    = False
        self._requirectrl:  bool    = False
        self._pos_press:    QPointF = QPointF()
        self._tl_press:     QPointF = QPointF()

    # --- Public interface -------------------------------------------------

    def set_require_control(self, b: bool) -> None:
        self._requirectrl = b

    def set_extent(self, e: QRectF) -> None:
        self._extent_world = e
        self._sure_scale()

    def scale_to_fit(self) -> None:
        self._scaletofit = True
        self._sure_scale()
        self.update()

    def set_top_left(self, tl: QPointF) -> None:
        self._tl_world = tl
        self._scaletofit = False
        self.update()

    def set_scale(self, factor: float) -> None:
        mousepos = self.mapFromGlobal(QCursor.pos())
        mousexy_old = self._tl_world + (mousepos - self.tl_dest()) / self.scale()
        self._scalefactor = factor
        self._scaletofit = False
        self._sure_scale()
        mousexy_new = self._tl_world + (mousepos - self.tl_dest()) / self.scale()
        self._tl_world += mousexy_old - mousexy_new
        self._sure_pan()

    def auto_size(self) -> None:
        self._tl_world = self._extent_world.topLeft()
        s = QSizeF(self._extent_world.size())
        s *= self.scale()
        s *= self.screen().logicalDotsPerInch() / 96
        self.resize(s.toSize())
        self.update()

    def extent(self) -> QRectF:
        return self._extent_world

    def top_left(self) -> QPointF:
        return self._tl_world

    def scale(self) -> float:
        return self._perfect_scale() if self._scaletofit else self._scalefactor

    def tl_dest(self) -> QPointF:
        """Screen coordinates of the world top-left (centred when zoomed out)."""
        ws = self._extent_world.size() * self.scale()
        x = (self.width()  - ws.width())  / 2
        y = (self.height() - ws.height()) / 2
        return QPointF(max(x, 0), max(y, 0))

    def br_dest(self) -> QPointF:
        """Screen coordinates of the world bottom-right."""
        ws = self._extent_world.size() * self.scale()
        w = self.width()
        h = self.height()
        x = (w + ws.width())  / 2
        y = (h + ws.height()) / 2
        return QPointF(min(x, w), min(y, h))

    def is_dragging(self) -> bool:
        return self._dragging

    # --- Event handlers ---------------------------------------------------

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self._dragging = (
            not self._requirectrl
            or bool(e.modifiers() & Qt.KeyboardModifier.ControlModifier)
        )
        self._pos_press = QPointF(e.pos())
        self._tl_press  = QPointF(self._tl_world)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if not self._dragging:
            return
        pos_now = QPointF(e.pos())
        self._tl_world = self._tl_press - (pos_now - self._pos_press) / self.scale()
        self._sure_pan()

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self._dragging = False

    def wheelEvent(self, e: QWheelEvent) -> None:
        delta = e.angleDelta().y() / 120.0
        mousexy_old = self._tl_world + (e.position() - self.tl_dest()) / self.scale()
        self.set_scale(self.scale() * math.pow(1.2, delta))
        mousexy_new = self._tl_world + (e.position() - self.tl_dest()) / self.scale()
        self._tl_world += mousexy_old - mousexy_new
        self._sure_pan()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        key  = e.key()
        mods = e.modifiers()

        if key in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):
            if mods & Qt.KeyboardModifier.AltModifier:
                self.set_scale(1.05 * self.scale())
            elif mods & Qt.KeyboardModifier.ShiftModifier:
                self.set_scale(2 * self.scale())
            else:
                self.set_scale(1.2 * self.scale())
        elif key in (Qt.Key.Key_Minus, Qt.Key.Key_Underscore):
            if mods & Qt.KeyboardModifier.AltModifier:
                self.set_scale(self.scale() / 1.05)
            elif mods & Qt.KeyboardModifier.ShiftModifier:
                self.set_scale(self.scale() / 2)
            else:
                self.set_scale(self.scale() / 1.2)
        elif key == Qt.Key.Key_1:
            self.set_scale(iu2pt(1))
        elif key == Qt.Key.Key_0:
            self.scale_to_fit()
        elif key == Qt.Key.Key_E:
            self.auto_size()
        elif key == Qt.Key.Key_Q:
            if mods & Qt.KeyboardModifier.ControlModifier:
                self.close()
        else:
            super().keyPressEvent(e)

    # --- Private helpers --------------------------------------------------

    def _perfect_scale(self) -> float:
        viewsize  = QSizeF(self.size())
        worldsize = self._extent_world.size()
        sx = viewsize.width()  / worldsize.width()
        sy = viewsize.height() / worldsize.height()
        return min(sx, sy)

    def _sure_scale(self) -> None:
        self._scalefactor = max(0.01, min(100.0, self._scalefactor))
        self._sure_pan()

    def _sure_pan(self) -> None:
        viewsize = QSizeF(self.size()) / self.scale()
        br_now   = self._tl_world + QPointF(viewsize.width(), viewsize.height())

        if br_now.x() >= self._extent_world.right():
            self._tl_world.setX(self._extent_world.right()  - viewsize.width())
        if br_now.y() >= self._extent_world.bottom():
            self._tl_world.setY(self._extent_world.bottom() - viewsize.height())
        if self._tl_world.x() < self._extent_world.left():
            self._tl_world.setX(self._extent_world.left())
        if self._tl_world.y() < self._extent_world.top():
            self._tl_world.setY(self._extent_world.top())

        self.update()
