# qpwidget.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
import sys

from PyQt6.QtCore import Qt, QPoint, QPointF, QRect, QRectF, QSizeF
from PyQt6.QtGui import (
    QCloseEvent, QColor, QCursor, QFont, QFontMetrics,
    QKeyEvent, QMouseEvent, QPaintEvent, QPainter, QPen,
    QPixmap, QResizeEvent,
)
from PyQt6.QtWidgets import (
    QApplication, QGridLayout, QLabel, QMenu, QMessageBox,
    QSizePolicy, QSpacerItem, QWidget,
)

from .scrollwidget import ScrollWidget
from .figure import Figure
from .program import Program
from .axis import Axis
from .factor import pt2iu, iu2pt

try:
    from config import QPLOT_VERSION
except ImportError:
    QPLOT_VERSION = "(unknown)"

_MARGPIX = 15


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _coordtext_dx(x: float, dx: float) -> str:
    """Format x so that a difference of dx is visually clear."""
    if x == 0:
        return "0"
    if dx <= 0:
        return "\u2014"  # em dash
    k = math.floor(math.log(dx) / math.log(10))
    if k <= 0:
        return f"{x:.{-k}f}".replace("-", "\u2212")
    l = math.floor(math.log(abs(x)) / math.log(10))
    if l < l - k + 2:
        return f"{x:.0f}"
    digits = max(l - k + 1, 1)
    return f"{x:.{digits}e}".replace("-", "\u2212")


def _coordtext(x: float, x0: float, x1: float) -> str:
    return _coordtext_dx(x, 2e-3 * (x1 - x0))


def _sensible_step(range_: float) -> float:
    mx  = range_ / 5
    lg  = math.log10(mx)
    ord_ = math.floor(lg)
    sub = 10 ** (lg - ord_)
    if sub >= 5:
        sub = 5
    elif sub >= 2:
        sub = 2
    else:
        sub = 1
    return sub * 10 ** ord_


# ---------------------------------------------------------------------------
# QPWidget
# ---------------------------------------------------------------------------

class QPWidget(ScrollWidget):
    """Interactive display widget for a QPlot figure.

    Supports zooming/panning (via ScrollWidget), ruler overlay,
    coordinate tracking, crop marks, and a menu button.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._fig:           Figure | None = None
        self._prog:          Program | None = None
        self._marg:          float          = 20.0
        self._worldextent:   QRectF         = QRectF()
        self._winttl:        str            = ""
        self._trackpanel:    str            = "-"
        self._coord:         QLabel         = QLabel(self)
        self._ruler:         bool           = False
        self._brandnew:      bool           = True
        self._menurect:      QRect          = QRect()
        self._showmenu:      bool           = True
        self._showcoords:    bool           = True
        self._showcropmarks: bool           = False
        self._graymargin:    bool           = False

        self._prep_coord()
        self._pick_cursor()
        self.setMouseTracking(True)
        self._place_menu_button()

    # --- Public interface -------------------------------------------------

    def set_margin(self, m: float) -> None:
        self._marg = m
        self.set_extent(
            self._worldextent.adjusted(-m, -m, m, m))

    def set_contents(self, fig: Figure, prog: Program) -> None:
        self._fig  = fig
        self._prog = prog
        if fig:
            self._worldextent = fig.extent()
            self.set_extent(
                self._worldextent.adjusted(
                    -self._marg, -self._marg,
                     self._marg,  self._marg))
        else:
            self.update()

    def setWindowTitle(self, t: str) -> None:  # keep Qt name for framework
        self._winttl = t
        super().setWindowTitle(t)

    def set_ruler(self, r: bool) -> None:
        if r == self._ruler:
            return
        self._ruler = r
        self.update()

    def has_ruler(self) -> bool:
        return self._ruler

    def take_screen_shot(self) -> None:
        if not self._fig or not self._prog:
            return
        coords_seen = self._showcoords
        menu_seen   = self._showmenu
        self._showmenu = False
        self._coord.hide()

        world = self._fig.extent()
        tld   = self.tl_dest()
        s     = self.scale()
        tlw   = self.top_left()
        world.translate(-tlw)
        world = QRectF(world.topLeft() * s, world.size() * s)
        world.translate(tld)
        r = QRectF(QPoint(0, 0), self.size()) & world
        pm = self.grab(r.toRect())
        QApplication.clipboard().setPixmap(pm)

        if coords_seen:
            self._coord.show()
        if menu_seen:
            self._showmenu = True

    # --- Event handlers ---------------------------------------------------

    def paintEvent(self, _: QPaintEvent) -> None:
        if not self._fig or not self._prog:
            return

        if self._fig.extent() != self._worldextent:
            self._worldextent = self._fig.extent()
            self.set_extent(self._worldextent.adjusted(
                -self._marg, -self._marg,
                 self._marg,  self._marg))
            if self._brandnew:
                self.resize((self._worldextent.size() / 20).toSize())
            self._brandnew = False
            self.auto_size()

        p = self._fig.painter()
        p.begin(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        p.setBrush(QColor(200, 200, 200) if self._graymargin
                   else QColor("white"))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(self.rect())

        tld = self.tl_dest()
        p.translate(tld.x(), tld.y())
        s = self.scale()
        p.scale(s, s)
        tlw = self.top_left()
        p.translate(-tlw.x(), -tlw.y())

        self._render_margin(p)
        if self._ruler:
            self._render_ruler(p)

        self._fig.set_hairline(0)
        self._prog.render(self._fig)

        p.end()

        if self._showmenu:
            self._paint_menu_button()

    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        self._place_menu_button()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        key  = e.key()
        mods = e.modifiers()

        if key == Qt.Key.Key_G:
            self._graymargin = not self._graymargin
            self.update()
        elif key == Qt.Key.Key_M:
            self._showcropmarks = not self._showcropmarks
            self.update()
        elif key == Qt.Key.Key_C:
            if mods & Qt.KeyboardModifier.ControlModifier:
                self.take_screen_shot()
            else:
                self._showcoords = not self._showcoords
                self._pick_cursor()
                self._report_track(
                    QPointF(self.mapFromGlobal(QCursor.pos(self.screen()))),
                    0, "move")
        elif key == Qt.Key.Key_R:
            self.set_ruler(not self.has_ruler())
        elif key == Qt.Key.Key_B:
            if self._fig:
                self._fig.show_bounding_boxes(
                    not self._fig.are_bounding_boxes_shown())
            self.update()
        else:
            super().keyPressEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if self._menurect.contains(e.pos()):
            self._click_menu()
            return
        super().mousePressEvent(e)
        if self._fig:
            xy    = QPointF(e.pos())
            world = (xy - self.tl_dest()) / self.scale() + self.top_left()
            tp    = self._fig.panel_at(world)
            if tp != self._trackpanel and self._ruler:
                self.update()
            self._trackpanel = tp
            self._pick_cursor()
            self._report_track(xy, e.button(), "press")

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        super().mouseMoveEvent(e)
        if self._fig:
            xy = QPointF(e.pos())
            if not e.buttons():
                world = (xy - self.tl_dest()) / self.scale() + self.top_left()
                tp    = self._fig.panel_at(world)
                if tp != self._trackpanel:
                    self._trackpanel = tp
                    self._pick_cursor()
                    if self._ruler:
                        self.update()
            self._report_track(xy, e.button(), "move")

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        self._pick_cursor()
        if self._fig:
            self._report_track(QPointF(e.pos()), e.button(), "release")

    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(e)
        if self._fig:
            self._report_track(QPointF(e.pos()), e.button(), "double")

    def closeEvent(self, e: QCloseEvent) -> None:
        super().closeEvent(e)

    def leaveEvent(self, e) -> None:
        super().leaveEvent(e)
        self._coord.hide()

    # --- Private helpers --------------------------------------------------

    def _prep_coord(self) -> None:
        self._coord.hide()
        f = self.font()
        f.setPointSize(14)
        self._coord.setFont(f)
        self._coord.setAutoFillBackground(True)
        p = self._coord.palette()
        p.setColor(p.ColorRole.Window, QColor(255, 255, 255, 200))
        self._coord.setMargin(5)
        self._coord.setPalette(p)

    def _place_menu_button(self) -> None:
        dpi = self.screen().logicalDotsPerInch()
        w = int(24 * dpi / 96)
        h = int(20 * dpi / 96)
        self._menurect = QRect(0, 0, w, h)

    def _paint_menu_button(self) -> None:
        p = QPainter(self)
        dpi = self.screen().logicalDotsPerInch()
        p.setPen(QPen(QColor(100, 100, 100), 2 * dpi / 96))
        w  = self._menurect.width()
        h  = self._menurect.height()
        x0 = self._menurect.left() + w // 4
        y0 = self._menurect.top()  + h // 2
        w  = w // 2
        dy = h // 4
        for k in (-1, 0, 1):
            p.drawLine(x0, y0 + k * dy, x0 + w, y0 + k * dy)

    def _click_menu(self) -> None:
        menu = QMenu()

        about = menu.addAction("&About QPlot\u2026")

        showhide = menu.addMenu("&Show/hide")
        coordinates = showhide.addAction("&Coordinates")
        coordinates.setShortcut(Qt.Key.Key_C)
        coordinates.setCheckable(True)
        coordinates.setChecked(self._showcoords)

        margin_act = showhide.addAction("&Gray margin")
        margin_act.setShortcut(Qt.Key.Key_G)
        margin_act.setCheckable(True)
        margin_act.setChecked(self._graymargin)

        crops = showhide.addAction("Crop &marks")
        crops.setShortcut(Qt.Key.Key_M)
        crops.setCheckable(True)
        crops.setChecked(self._showcropmarks)

        ruler_act = showhide.addAction("&Rulers")
        ruler_act.setShortcut(Qt.Key.Key_R)
        ruler_act.setCheckable(True)
        ruler_act.setChecked(self.has_ruler())

        boxes = showhide.addAction("&Boxes (debug)")
        boxes.setShortcut(Qt.Key.Key_B)
        boxes.setCheckable(True)
        if self._fig:
            boxes.setChecked(self._fig.are_bounding_boxes_shown())

        shot  = menu.addAction("Screensho&t")
        shot.setShortcut(Qt.Key.Key_C)
        close = menu.addAction("&Close")

        menu.move(QCursor.pos(self.screen()))
        act = menu.exec()

        if act == shot:
            self.take_screen_shot()
        elif act == about:
            self._about_action()
        elif act == close:
            self.close()
        elif act == margin_act:
            self._graymargin = margin_act.isChecked()
            self.update()
        elif act == crops:
            self._showcropmarks = crops.isChecked()
            self.update()
        elif act == ruler_act:
            self.set_ruler(ruler_act.isChecked())
        elif act == boxes and self._fig:
            self._fig.show_bounding_boxes(boxes.isChecked())
        elif act == coordinates:
            self._showcoords = coordinates.isChecked()
            self.update()

    def _render_margin(self, p: QPainter) -> None:
        p.save()
        if self._graymargin:
            p.setBrush(QColor("white"))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRect(self._fig.extent())
        if self._showcropmarks:
            self._draw_crop_marks(p)
        p.restore()

    def _draw_crop_marks(self, p: QPainter) -> None:
        world = self._fig.extent()
        dpi   = self.screen().logicalDotsPerInch()
        p.setPen(QPen(QColor("black"), 1 * dpi / 96 / self.scale()))
        yy = [world.top(), world.bottom()]
        xx = [world.left(), world.right()]
        dm  = _MARGPIX / self.scale()
        if dm > 0.25 * self._marg:
            dm = 0.25 * self._marg
        ddm = 0.75 * self._marg
        for k in range(2):
            x = xx[k]
            p.drawLine(QPointF(x, yy[0] - ddm), QPointF(x, yy[0] - dm))
            p.drawLine(QPointF(x, yy[1] + ddm), QPointF(x, yy[1] + dm))
            y = yy[k]
            p.drawLine(QPointF(xx[0] - ddm, y), QPointF(xx[0] - dm, y))
            p.drawLine(QPointF(xx[1] + ddm, y), QPointF(xx[1] + dm, y))

    def _render_ruler(self, p: QPainter) -> None:
        if not self._trackpanel:
            return
        p.save()
        world = self._fig.extent()
        xax   = self._find_x_axis()
        yax   = self._find_y_axis()

        x0 = xax.min();  x1 = xax.max()
        dx = _sensible_step(x1 - x0)
        x0 = math.ceil(x0 / dx) * dx
        x1 = math.floor(x1 / dx) * dx

        y0 = yax.min();  y1 = yax.max()
        dy = _sensible_step(y1 - y0)
        y0 = math.ceil(y0 / dy) * dy
        y1 = math.floor(y1 / dy) * dy

        p.setPen(QPen(QColor(0, 0, 0), 1 / self.scale()))
        ytop_text = world.top()    - pt2iu(1)
        ybot_text = world.bottom() + pt2iu(1)
        xleft_text  = world.left()  - pt2iu(1)
        xright_text = world.right() + pt2iu(1)

        f = QFont("Helvetica")
        f.setPointSize(int(12 / self.scale()))
        p.setFont(f)
        s = 1 / self.scale()

        x = x0
        while x <= x1 + dx / 2:
            xw  = xax.map(x).x()
            txt = _coordtext_dx(x, dx)
            p.drawText(
                QRectF(xw - 200*s, ytop_text - 50*s, 400*s, 50*s),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
                txt)
            p.drawText(
                QRectF(xw - 200*s, ybot_text, 400*s, 100*s),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                txt)
            x += dx

        y = y0
        while y <= y1 + dy / 2:
            yw  = yax.map(y).y()
            txt = _coordtext_dx(y, dy)
            p.drawText(
                QRectF(xleft_text - 400*s, yw - 20*s, 400*s, 40*s),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                txt)
            p.drawText(
                QRectF(xright_text, yw - 20*s, 400*s, 40*s),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                txt)
            y += dy

        p.restore()

    def _find_x_axis(self) -> Axis:
        if self._trackpanel == self._fig.current_panel_name():
            return self._fig.x_axis()
        return self._fig.panel_ref(self._trackpanel).xaxis

    def _find_y_axis(self) -> Axis:
        if self._trackpanel == self._fig.current_panel_name():
            return self._fig.y_axis()
        return self._fig.panel_ref(self._trackpanel).yaxis

    def _pick_cursor(self) -> None:
        if self._trackpanel == "":
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.set_require_control(True)
        elif self._showcoords and not self.is_dragging():
            self.setCursor(Qt.CursorShape.CrossCursor)
            self.set_require_control(True)
        else:
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            self.set_require_control(False)

    def _report_track(self, xy: QPointF, button: Qt.MouseButton,
                      what: str) -> None:
        if not self._fig or self._trackpanel == "" or not self._showcoords:
            self._coord.hide()
            return

        world = (xy - self.tl_dest()) / self.scale() + self.top_left()
        xax   = self._find_x_axis()
        yax   = self._find_y_axis()
        x_str = _coordtext(xax.rev(world), xax.min(), xax.max())
        y_str = _coordtext(yax.rev(world), yax.min(), yax.max())

        c = f"({x_str}, {y_str})".replace("-", "\u2212")
        self._coord.setText(c)
        self._coord.resize(self._coord.sizeHint())

        xc = int(xy.x()) + 10
        if xc + self._coord.width() > self.width() - 5:
            xc = int(xy.x()) - self._coord.width() - 10
        yc = int(xy.y()) + 10
        if yc + self._coord.height() > self.height() - 5:
            yc = int(xy.y()) - self._coord.height() - 10
        self._coord.move(xc, yc)
        self._coord.show()

        if button or what != "move":
            self._feedback(
                f"{what} {self._trackpanel} {x_str} {y_str} {button}")

    def _feedback(self, s: str) -> None:
        sys.stdout.write(s + "\n")
        sys.stdout.flush()

    def _about_action(self) -> None:
        msg = (
            f"<b>QPlot</b> {QPLOT_VERSION}<br>"
            "(C) 2013\u20132024\u2002Daniel A. Wagenaar<br><br>"
            "<b>QPlot</b> is an alternative 2D plotting library for "
            "Python, Matlab, and Octave that facilitates beautiful typography "
            "and precise axis scaling.<br><br>"
            "<b>QPlot</b> is free software: you can redistribute it and/or "
            "modify it under the terms of the GNU General Public License as "
            "published by the Free Software Foundation, either version 3 of "
            "the License, or (at your option) any later version.<br><br>"
            "<b>QPlot</b> is distributed in the hope that it will be useful, "
            "but WITHOUT ANY WARRANTY; without even the implied warranty of "
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU "
            "General Public License for more details.<br><br>"
            "You should have received a copy of the GNU General Public License "
            "along with this program. If not, see "
            "<a href=\"http://www.gnu.org/licenses/gpl-3.0.en.html\">"
            "www.gnu.org/licenses/gpl-3.0.en.html</a>."
        )
        box = QMessageBox()
        box.setWindowTitle("About QPlot")
        box.setTextFormat(Qt.TextFormat.RichText)
        box.setText(msg)
        dpi = self.screen().logicalDotsPerInch()
        icon_w = int(128 * dpi / 96)
        box.setIconPixmap(
            QPixmap(":qplot.png").scaled(
                icon_w, icon_w,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            ))
        layout = box.layout()
        if isinstance(layout, QGridLayout):
            layout.addItem(
                QSpacerItem(int(8 * dpi), 0,
                            QSizePolicy.Policy.Fixed,
                            QSizePolicy.Policy.Expanding),
                layout.rowCount(), 0, 1, layout.columnCount(),
            )
        box.exec()
