// Range.H - This file is part of QPlot

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

// Range.H

#ifndef RANGE_H

#define RANGE_H

class Range {
public:
  Range();
  Range(double x);
  Range(double x, double y);
  bool empty() const;
  void extend(double x) {
    if (empty_) {
      min_ = max_ = x;
      empty_ = false;
    } else if (x<min_)
      min_=x;
    else if (x>max_)
      max_=x;
  }
  void unionize(Range const &r);
  void intersect(Range const &r);
  bool contains(double x) const;
  double min() const { return min_; }
  double max() const { return max_; }
  double range() const;
private:
  double min_;
  double max_;
  bool empty_;
};

#endif
