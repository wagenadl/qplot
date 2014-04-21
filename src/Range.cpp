// Range.cpp - This file is part of QPlot

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

// Range.C

#include "Range.H"

Range::Range() {
  empty_ = true;
}

Range::Range(double x) {
  min_ = max_ = x;
  empty_ = false;
}

Range::Range(double x, double y) {
  min_ = max_ = x;
  empty_ = false;
  extend(y);
}

bool Range::empty() const {
  return empty_;
}

void Range::extend(double x) {
  if (empty_) {
    min_ = max_ = x;
    empty_ = false;
  } else {
    if (x<min_)
      min_=x;
    if (x>max_)
      max_=x;
  }
}

void Range::unionize(Range const &r) {
  if (r.empty_)
    return;
  if (empty_) {
    min_ = r.min_;
    max_ = r.max_;
    empty_ = false;
  } else {
    if (r.min_<min_)
      min_ = r.min_;
    if (r.max_>max_)
      max_ = r.max_;
  }
}

void Range::intersect(Range const &r) {
  if (empty_)
    return;
  if (r.empty_) {
    empty_ = true;
  } else {
    if (r.min_>min_)
      min_ = r.min_;
    if (r.max_<max_)
      max_ = r.max_;
    if (min_>max_)
      empty_ = true;
  }
}

bool Range::contains(double x) const {
  if (empty_)
    return false;
  else
    return x>=min_ && x<=max_;
}

double Range::range() const {
  if (empty_)
    return 0;
  else
    return max_ - min_;
}
