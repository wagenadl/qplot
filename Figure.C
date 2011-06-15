// Figure.C

#include "Figure.H"

Figure::Figure() {
  figsize = QSizeF(72*6, 72*4);
  xax.setPlacement(QPointF(0,0), QPointF(figsize.width(),0));
  yax.setPlacement(QPointF(0,0), QPointF(0,figsize.height()));
}

void Figure::setSize(QSizeF wh_pt) {
  figsize = wh_pt;
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

QPainter &Figure::painter() {
  return p;
}
