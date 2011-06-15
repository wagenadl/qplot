// Axis.C

#include "Axis.H"
#include <QDebug>

Axis::Axis() {
  x0=0;
  x1=1;
  p0 = QPointF(0,0);
  p1 = QPointF(1,0);
  dp = QPointF(1,0);
}

void Axis::setDataRange(double x0_, double x1_) {
  x0 = x0_;
  if (x1<=x0) {
    x1 = x0 + 1;
    qDebug() << "Warning: bad data range";
  }
  x1 = x1_;

  recalc();
}

void Axis::recalc() {
  dp = QPointF((p1.x()-p0.x())/(x1-x0), (p1.y()-p0.y())/(x1-x0));
}

void Axis::setPlacement(QPointF p0_, QPointF p1_) {
  p0 = p0_;
  p1 = p1_;
  recalc();
}

double Axis::min() const {
  return x0;
}

double Axis::max() const {
  return x1;
}

QPointF Axis::minp() const {
  return p0;
}

QPointF Axis::maxp() const {
  return p1;
}

QPointF Axis::map(double x) const {
  return p0 + x*dp;
}
