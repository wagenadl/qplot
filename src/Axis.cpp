// Axis.cpp - This file is part of QPlot

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

// Axis.C

#include "Axis.h"
#include <QDebug>
#include "Error.h"
#include <math.h>

Axis::Axis() {
  x0=0;
  x1=1;
  p0 = QPointF(0,0);
  p1 = QPointF(1,0);
  recalc();
}

void Axis::setDataRange(double x0_, double x1_) {
  if (x1_ <= x0_) {
    x0 = 0;
    x1 = 1;
  } else {
    x0 = x0_;
    x1 = x1_;
  }
  recalc();
}

void Axis::recalc() {
  dp = QPointF((p1.x()-p0.x())/(x1-x0), (p1.y()-p0.y())/(x1-x0));
  porig = p0 - dp*x0;
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
  return porig + x*dp;
}

QPointF Axis::maprel(double x) const {
  return x*dp;
}

double Axis::rev(QPointF p) const {
  QPointF dp = p-p0;
  QPointF dpa = p1-p0;
  double phi = atan2(dpa.y(), dpa.x());
  double dx = (dp.x()*cos(phi) + dp.y()*sin(phi)) /
    sqrt(dpa.x()*dpa.x() + dpa.y()*dpa.y());;
  return dx*(x1-x0) + x0;
}
