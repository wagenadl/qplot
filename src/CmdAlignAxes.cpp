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

#include <QDebug>
#include <math.h>
#include "Error.h"
#include "Range.h"

static CBuilder<CmdAlignAxes> cbAlignAxes("alignaxes");

#define SCALETOLERANCE 1e-4
#define SHIFTTOLERANCE 1e-3
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
    alignX(f, ids);

  if (py.range() > MINOVERLAP)
    alignY(f, ids);
}


void CmdAlignAxes::alignX(Figure &f, QSet<QString> ids) {
  // Find union of extents
  Range px;
  for (QString id: ids) {
    Panel const &p(f.panelRef(id));
    px.unionize(Range(p.desiredExtent.left(), p.desiredExtent.right()));
  }
  // Find min and max represented there
  /* Note that I am assuming the axis has negative values on the left.
     I think I make that assumption throughout the program, probably
     to my ultimate detriment.
  */      
  double x0 = 1e99;
  double x1 = -1e99;
  for (QString id: ids) {
    Axis const &axis(f.panelRef(id).xaxis);
    double x0a = axis.rev(QPointF(px.min(), 0));
    double x1a = axis.rev(QPointF(px.max(), 0));
    if (x0a<x0)
      x0 = x0a;
    if (x1a>x1)
      x1 = x1a;
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
  double a = (px.max()-px.min()) / (x1-x0);
  double b = px.min() - a*x0;

  for (QString id: ids) {
    Axis &axis = f.panelRef(id).xaxis;
    if (axis.map(x0).x()<px.min()-SHIFTTOLERANCE ||
        axis.map(x1).x()>px.max()+SHIFTTOLERANCE)  {
      axis.setPlacement(QPointF(a*axis.min()+b, 0),
                     QPointF(a*axis.max()+b, 0));
      f.markFudged();
    }
  }
}


void CmdAlignAxes::alignY(Figure &f, QSet<QString> ids) {
  // Find union of extents
  Range py;
  for (QString id: ids) {
    Panel const &p(f.panelRef(id));
    py.unionize(Range(p.desiredExtent.top(), p.desiredExtent.bottom()));
  }
  // Find min and max represented there
  /* Note that I am assuming the axis has negative values on the bottom.
     I think I make that assumption throughout the program, probably
     to my ultimate detriment.
  */      
  double y0 = 1e99;
  double y1 = -1e99;
  for (QString id: ids) {
    Axis const &axis(f.panelRef(id).yaxis);
    double y0a = axis.rev(QPointF(0, py.max()));
    double y1a = axis.rev(QPointF(0, py.min()));
    if (y0a<y0)
      y0 = y0a;
    if (y1a>y1)
      y1 = y1a;
  }
  /* Now I need to calculate the Placement that will ensure the
     appropriate mapping at the edges.
     I need: a*y0+b = py0   (1)
     a*y1+b = py1   (2)
     Solve for a and b.
     Then use these a and b to set the Placement PY0 and PY1 to
     PY0 = a*Y0+b   (3)
     PY1 = a*Y1+b   (4)
     where Y0 and Y1 are the min and max data coord of the Axis.
     Subtract (1) and (2):
     a = (py1-py0) / (y1-y0)
     Then:
     b = py0 - a*y0.
  */
  double a = (py.min()-py.max()) / (y1-y0);
  double b = py.max() - a*y0;

  for (QString id: ids) {
    Axis &axis(f.panelRef(id).yaxis);
    if (axis.map(y1).y()<py.min()-SHIFTTOLERANCE ||
        axis.map(y0).y()>py.max()+SHIFTTOLERANCE) {
      axis.setPlacement(QPointF(0, a*axis.min()+b),
                        QPointF(0, a*axis.max()+b));
      f.markFudged();
    }
  }
}
