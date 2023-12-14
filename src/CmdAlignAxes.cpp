// CmdAlignAxes.cpp - This file is part of QPlot

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

// CmdAlignAxes.C

#include "CmdAlignAxes.h"
#include "DimExtractor.h"

#include <QDebug>
#include <math.h>
#include "Error.h"
#include "Range.h"

static CBuilder<CmdAlignAxes> cbAlignAxes("alignaxes");

#define SCALETOLERANCE 1e-3
#define SHIFTTOLERANCE .1
#define MINOVERLAP 5

bool CmdAlignAxes::usage() {
  return error("Usage: alignaxes ID ...\n");
}

bool CmdAlignAxes::parse(Statement const &s) {
  if (s.length()<3)
    return usage(); // we could allow this null case, but that might confuse

  for (int i=1; i<s.length(); i++) 
    if (s[i].typ!=Token::CAPITAL)
      return usage();
  return true;
}


void CmdAlignAxes::render(Statement const &s, Figure &f, bool) {
  QSet<QString> ids;
  for (int i=1; i<s.length(); i++) {
    if (f.hasPanel(s[i].str)) {
      ids.insert(s[i].str);
    } else {
      Error() << "Unknown panel: " << s[i].str;
      return;
    }
  }
  // Now we know that all IDS are actual panels.

  f.leavePanel();

  // Let's find out if we have paper overlap in x, y 
  Range px, py;
  bool first = true;
  foreach (QString id, ids) {
    Panel const &p(f.panelRef(id));
    Range px1(p.desiredExtent.left(), p.desiredExtent.right());
    Range py1(p.desiredExtent.top(), p.desiredExtent.bottom());
    if (first) {
      px = px1;
      py = py1;
      first = false;
    } else {
      px.intersect(px1);
      py.intersect(py1);
    }
  }

  if (px.range() > MINOVERLAP)
    align(f, ids, DimExtractor::x());

  if (py.range() > MINOVERLAP)
    align(f, ids, DimExtractor::y());
}


void CmdAlignAxes::align(Figure &f, QSet<QString> ids, DimExtractor const &de) {
  // Find union of extents
  Range px;
  for (QString id: ids) 
    px.unionize(de.rectRange(f.panelRef(id).desiredExtent));

  // Find min and max represented there
  Range dx;
  for (QString id: ids) {
    Axis const &axis(de.axis(f.panelRef(id)));
    dx.extend(axis.rev(de.repoint(QPointF(0,0), px.min())));
    dx.extend(axis.rev(de.repoint(QPointF(0,0), px.max())));
  }

  /* Now I need to calculate the Placement that will ensure the
     appropriate mapping at the edges.
     I need: a*x0+b = px0   (1)
     a*x1+b = px1   (2)
     Solve for a and b.
     Then use these a and b to set the Placement PX0 and PX1 to
     PX0 = a*X0+b   (3)
     PX1 = a*X1+b   (4)
     where X0 and X1 are the min and max data coord of the Axis.
     Subtract (1) and (2):
     a = (px1-px0) / (x1-x0)
     Then:
     b = px0 - a*x0.
  */
  double x0 = dx.min();
  double x1 = dx.max();

  for (QString id: ids) {
    Axis &axis = de.axis(f.panelRef(id));
    bool rev = de.point(axis.maprel(1)) < 0;
    // rev indicates wheter (d-,d+) -> (p+,p-) or (d-,d+)->(p-,p+)
    double px0 = rev ? px.max() : px.min();
    double px1 = rev ? px.min() : px.max();
    // px0, px1 are paper target for x0, x1; regardless of rev
    double a = (px1-px0) / (x1-x0);
    double b = px0 - a*x0;
    // qDebug() << id << x0 << x1 << px0 << px1 << a << b;
    if (fabs(de.point(axis.map(x0)) - px0) > SHIFTTOLERANCE
        || fabs(de.point(axis.map(x1)) - px1) > SHIFTTOLERANCE) {
      axis.setPlacement(de.repoint(QPointF(), a*axis.min()+b),
                        de.repoint(QPointF(), a*axis.max()+b));
      f.markFudged();
    }
  }
}
