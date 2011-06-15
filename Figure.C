// Figure.C

#include "Figure.H"
#include <math.h>

Figure::Figure() {
  figsize = QSizeF(72*6, 72*4);
  xax.setPlacement(QPointF(0,0), QPointF(figsize.width(),0));
  yax.setPlacement(QPointF(0,figsize.height()), QPointF(0,0));
}

void Figure::setSize(QSizeF wh_pt) {
  if (figsize == wh_pt)
    return;
  
  figsize = wh_pt;
  xax.setPlacement(QPointF(0,0), QPointF(figsize.width(),0));
  yax.setPlacement(QPointF(0,figsize.height()), QPointF(0,0));
}

QSizeF const &Figure::size() const {
  return figsize;
}

Axis &Figure::xAxis() {
  return xax;
}

Axis &Figure::yAxis() {
  return yax;
}

QPointF Figure::map(double x, double y) const {
  return xax.map(x) + yax.map(y);
}

void Figure::clearBBox(bool full) {
  lastbbox = QRectF();
  cumulbbox = QRectF();
  if (full)
    fullbbox = QRectF();
}

void Figure::setBBox(QRectF const &b) {
  lastbbox = b;
  cumulbbox |= b;
  fullbbox |= b;
}

QRectF const &Figure::lastBBox() const {
  return lastbbox;
}

QRectF const &Figure::cumulBBox() const {
  return cumulbbox;
}

QRectF const &Figure::fullBBox() const {
  return fullbbox;
}

void Figure::setAnchor(double x, double y, double dx, double dy) {
  QPointF frm = map(0, 0);
  QPointF to = map(dx, dy);
  QPointF d = to-frm;
  setAnchor(map(x,y), atan2(d.y(), d.x()));
}

void Figure::setAnchor(QPointF const &x, double a) {
  anch = x;
  anchang = a;
}

QPointF const &Figure::anchor() const {
  return anch;
}

double const &Figure::anchorAngle() const {
  return anchang;
}

QPainter &Figure::painter() {
  return p;
}

void Figure::setAutoRange(bool au) {
  if (au) {
    xax.resetDataRange();
    yax.resetDataRange();    
  } else {
    xax.fixDataRange();
    yax.fixDataRange();    
  }
}
