// TextShiftAccum.C

#include "TextShiftAccum.H"
#include <QDebug>

TextShiftAccum::TextShiftAccum() {
  reset();
}

void TextShiftAccum::reset() {
  has = 0;
}

void TextShiftAccum::setBase(double x, double y) {
  x_ = x;
  y_ = y;
  has = true;
}

void TextShiftAccum::update(double dx, double dy) {
  if (!has) {
    qDebug() << "Warning: TextShiftAccum: update w/o base";
    setBase(0, 0);
  }
  x_ += dx;
  y_ += dy;
}

double TextShiftAccum::x() {
  return x_;
}

double TextShiftAccum::y() {
  return y_;
}

bool TextShiftAccum::isActive() {
  return has;
}
