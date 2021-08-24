// TextShiftAccum.cpp - This file is part of QPlot

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
