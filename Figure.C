// Figure.C

#include "Figure.H"
#include <math.h>

Figure::Figure() {
  figextent = QRectF(QPointF(0,0), QSizeF(72*6, 72*4));
  halign = CENTER;
  valign = BASE;
  currentPen = "A";
  currentBrush = "A";
  hairline_ = false;
  replaceAxes();
}

void Figure::setHairline(bool h) {
  hairline_ = h;
}

bool Figure::hairline() const {
  return hairline;
}

void Figure::setHAlign(Figure::HAlign a) {
  halign = a;
}

void Figure::setVAlign(Figure::VAlign a) {
  valign = a;
}

Figure::HAlign Figure::hAlign() const {
  return halign;
}

Figure::VAlign Figure::vAlign() const {
  return valign;
}


void Figure::setExtent(QRectF xywh_pt) {
  if (figextent==xywh_pt)
    return;

  figextent = xywh_pt;
  replaceAxes();
}

void Figure::setSize(QSizeF wh_pt) {
  if (figextent.size() == wh_pt)
    return;
  
  figextent.setSize(wh_pt);
  replaceAxes();
}

void Figure::replaceAxes() {
  xax.setPlacement(QPointF(figextent.left(),0),
		   QPointF(figextent.right(),0));
  yax.setPlacement(QPointF(0,figextent.bottom()),
		   QPointF(0,figextent.top()));
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

double Figure::angle(double dx, double dy) const {
  QPointF frm = map(0, 0);
  QPointF to = map(dx, dy);
  QPointF d = to-frm;
  return atan2(d.y(), d.x());
}

void Figure::setAnchor(double x, double y, double dx, double dy) {
  setAnchor(map(x,y), angle(dx,dy));
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

QRectF const &Figure::extent() const {
  return figextent;
}

void Figure::setRefText(QString s) {
  reftxt = s;
}

QString Figure::refText() const {
  return reftxt;
}

void Figure::choosePen(QString s) {
  pens[currentPen] = p.pen();
  p.setPen(pens[currentPen=s]);
}

void Figure::chooseBrush(QString s) {
  brushes[currentBrush] = p.brush();
  p.setBrush(brushes[currentBrush=s]);
}
