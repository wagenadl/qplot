// Rotate.cpp - This file is part of QPlot

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

// Rotate.C

#include "Rotate.h"
#include <math.h>

QPointF rotate(QPointF const &p, double phirad) {
  return QPointF(p.x()*cos(phirad)-p.y()*sin(phirad),
		 p.y()*cos(phirad)+p.x()*sin(phirad));
}

QRectF rotate(QRectF const &r, double phirad) {
  QPointF x1 = rotate(r.topLeft(),phirad);
  QPointF x2 = rotate(r.bottomLeft(),phirad);
  QPointF x3 = rotate(r.topRight(),phirad);
  QPointF x4 = rotate(r.bottomRight(),phirad);
  return QRectF(x1,x3) | QRectF(x2,x4);
}
