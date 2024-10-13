// ScrollWidget.cpp - This file is part of QPlot

/* QPlot - Publication quality 2D graphs with dual coordinate systems
   Copyright (C) 2014  Daniel Wagenaar
  
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
  
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
  
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// ScrollWidget.C

#include "ScrollWidget.h"
#include <QWheelEvent>
#include <QMouseEvent>
#include <QKeyEvent>
#include <QDebug>
#include <QScreen>
#include <QCursor>
#include "Factor.h"
#include <math.h>

ScrollWidget::ScrollWidget(QWidget *parent): QWidget(parent) {
  extent_world = QRectF(QPointF(0,0), QPointF(1000,1000));
  tl_world = QPointF(0,0);
  scalefactor = iu2pt(1);
  scaletofit = true;
  dragging = false;
}

ScrollWidget::~ScrollWidget() {
}

void ScrollWidget::setExtent(QRectF const &e) {
  extent_world = e;
  sureScale();
}

void ScrollWidget::scaleToFit() {
  scaletofit = true;
  sureScale();
  update();
}

void ScrollWidget::setTopLeft(QPointF tl) {
  tl_world = tl;
  scaletofit = false;
  update();
}

void ScrollWidget::setScale(double factor) {
  QPointF mousepos = mapFromGlobal(QCursor::pos());
  QPointF mousexy_old = tl_world + (mousepos-tlDest())/scale();
  scalefactor = factor;
  scaletofit = false;
  sureScale();
  QPointF mousexy_new = tl_world + (mousepos-tlDest())/scale();
  tl_world += mousexy_old - mousexy_new;
  surePan();
}

void ScrollWidget::autoSize() {
  tl_world = extent_world.topLeft();
  QSizeF s = extent_world.size();
  s *= scale();
  s *= screen()->logicalDotsPerInch() / 96;
  resize(s.toSize());
  update();
}

QRectF const &ScrollWidget::extent() const {
  return extent_world;
}

QPointF const &ScrollWidget::topLeft() const {
  return tl_world;
}

double ScrollWidget::scale() const {
  return scaletofit ? perfectScale() : scalefactor;
}    

void ScrollWidget::mousePressEvent(QMouseEvent *e) {
  dragging = (!requirectrl) || (e->modifiers() & Qt::ControlModifier);
    
  pos_press = e->pos();
  tl_press = tl_world;
}

void ScrollWidget::mouseMoveEvent(QMouseEvent *e) {
  if (!dragging)
    return;
  
  QPointF pos_now = e->pos();
  tl_world = tl_press - (pos_now - pos_press)/scale();
  surePan();
}

void ScrollWidget::keyPressEvent(QKeyEvent *e) {
  switch (e->key()) {
  case Qt::Key_Plus: case Qt::Key_Equal:
    if (e->modifiers() & Qt::AltModifier)
      setScale(1.05*scale());
    else if (e->modifiers() & Qt::ShiftModifier)
      setScale(2*scale());
    else
      setScale(1.2*scale());
    break;
  case Qt::Key_Minus: case Qt::Key_Underscore:
    if (e->modifiers() & Qt::AltModifier)
      setScale(scale()/1.05);
    else if (e->modifiers() & Qt::ShiftModifier)
      setScale(scale()/2);
    else
      setScale(scale()/1.2);
    break;
  case Qt::Key_1:
    setScale(iu2pt(1));
    break;
  case Qt::Key_0:
    scaleToFit();
    break;
  case Qt::Key_E:
    autoSize();
    break;
  case Qt::Key_Q:
    if (e->modifiers() & Qt::ControlModifier)
      close();
    break;
  default:
    QWidget::keyPressEvent(e);
  }
  
}

double ScrollWidget::perfectScale() const {
  QSizeF viewsize = QSizeF(size());
  QSizeF worldsize = extent_world.size();
  double sx = viewsize.width()/worldsize.width();
  double sy = viewsize.height()/worldsize.height();
  return sx<sy ? sx : sy;
}
 
      
void ScrollWidget::sureScale() {
  //  double s = perfectScale();
  if (scalefactor<.01)
    scalefactor = .01;
  else if (scalefactor>100)
    scalefactor = 100;
  surePan();
}

void ScrollWidget::surePan() {
  QSizeF viewsize = QSizeF(size())/scale();
  QPointF br_now = tl_world + QPointF(viewsize.width(), viewsize.height());

  if (br_now.x() >= extent_world.right())
    tl_world.setX(extent_world.right() - viewsize.width());
  if (br_now.y() >= extent_world.bottom())
    tl_world.setY(extent_world.bottom() - viewsize.height());
  if (tl_world.x() < extent_world.left())
    tl_world.setX(extent_world.left());
  if (tl_world.y() < extent_world.top())
    tl_world.setY(extent_world.top());

  update();
}

QPointF ScrollWidget::tlDest() const {
  QSizeF ws = extent_world.size() * scale();
  double x = (width() - ws.width())/2;
  double y = (height() - ws.height())/2;
  return QPointF(x>0 ? x : 0, y>0 ? y : 0);
}

QPointF ScrollWidget::brDest() const {
  QSizeF ws = extent_world.size() * scale();
  double w = width();
  double h = height();
  double x = (w + ws.width())/2;
  double y = (h + ws.height())/2;
  return QPointF(x<w ? x : w, y<h ? y : h);
}

void ScrollWidget::wheelEvent(QWheelEvent *e) {
  double delta = e->angleDelta().y() / 120.0;
  QPointF mousexy_old = tl_world + (e->position()-tlDest())/scale();
  setScale(scale() * pow(1.2, delta));
  QPointF mousexy_new = tl_world + (e->position()-tlDest())/scale();
  tl_world += mousexy_old - mousexy_new;
  surePan();
}

void ScrollWidget::mouseReleaseEvent(QMouseEvent *) {
  dragging = false;
}

void ScrollWidget::setRequireControl(bool b) {
  requirectrl = b;
}
