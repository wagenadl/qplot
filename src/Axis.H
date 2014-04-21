// Axis.H - This file is part of QPlot

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

// Axis.H

#ifndef AXIS_H

#define AXIS_H

#include <QPointF>

class Axis {
public:
  Axis();
  void setDataRange(double x0, double x1);
  void setPlacement(QPointF p0_pt, QPointF p1_pt);
  /* For a horizontal axis, normally p0_pt.y=p1_pt.y=0;
     for a vertical axis, normally p0_pt.x=p1_pt.x=0.
     That allows simple addition of the output of map() from a pair of axes.
  */
  double min() const; // data coord
  double max() const; // data coord
  QPointF minp() const; // paper coord (pt)
  QPointF maxp() const; // paper coord (pt)
  QPointF map(double x) const;
  QPointF maprel(double dx) const;
  double rev(QPointF p) const;
private:
  void recalc();
private:
  double x0, x1; // data
  QPointF p0, p1; // paper
  QPointF porig, dp;
};

#endif
