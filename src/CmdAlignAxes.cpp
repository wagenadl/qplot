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

#define SHIFTTOLERANCE .1

bool CmdAlignAxes::usage() {
  return error("Usage: alignaxes x|y ID ...\n");
}

bool CmdAlignAxes::parse(Statement const &s) { 
  if (s.length()<3)
    return usage(); // we could allow this null case, but that might confuse

  if (s[1].typ!=Token::BAREWORD)
    return usage();
  if (!(s[1].str=="x" || s[1].str=="y" || s[1].str=="xy"))
    return usage();
  for (int i=2; i<s.length(); i++) 
    if (s[i].typ!=Token::CAPITAL)
      return usage();
  return true;
}


void CmdAlignAxes::render(Statement const &s, Figure &f, bool) {
  bool shareX = s[1].str.contains("x");
  bool shareY = s[1].str.contains("y");

  QStringList ids;
  for (int i=2; i<s.length(); i++) {
    if (f.hasPanel(s[i].str)) {
      ids << s[i].str;
    } else {
      Error() << "Unknown panel: " << s[i].str;
      return;
    }
  }
  // Now we know that all IDS are actual panels.

  f.leavePanel();

  DimExtractor const &de(shareX ? DimExtractor::x() : DimExtractor::y());
  QList<QStringList> groups = de.orderedGroups(f, ids);
  //  qDebug() << "align" << shareX << shareY << groups;

  // Find union of extents in each groups
  QList<Range> pxx;
  // Find min and max represented there
  QList<Range> dxx;
  for (auto group: groups) {
    Range px;
    for (QString id: group)
      px.unionize(de.rectRange(f.panelRef(id).desiredExtent));
    pxx << px;
    Range dx;
    for (QString id: group) {
      Axis const &axis(de.axis(f.panelRef(id)));
      dx.extend(axis.rev(de.repoint(QPointF(0,0), px.min())));
      dx.extend(axis.rev(de.repoint(QPointF(0,0), px.max())));
    }
    dxx << dx;
  }

  double scale = 1;
  for (int k=0; k<groups.size(); k++) {
    double sc = pxx[k].range() / dxx[k].range();
    // qDebug() << "  grsc" << groups[k] << sc;
    if (k==0 || sc<scale)
      scale = sc;
  }

  // qDebug() << "  align" << scale;
  /* Now I need to calculate the Placement that will ensure the
     appropriate mapping at the edges.
     I need:
     a*dx0+b = px0   (1)
     a*dx1+b = px1   (2)
     Solve for a and b.
     Then use these a and b to set the Placement PX0 and PX1 to
     PX0 = a*X0+b   (3)
     PX1 = a*X1+b   (4)
     where X0 and X1 are the min and max data coord of the Axis.
     Subtract (1) and (2):
     a = (px1-px0) / (dx1-dx0)
     Then:
     b = px0 - a*dx0.
  */
  /* If I am changing the scale to use a' from another group, I
     still want
     a'*(dx0+dx1)/2 + b = (px0+px1)/2
     so b = (px0+px1)/2 - a'*(dx0+dx1)/2
   */
  for (int k=0; k<groups.size(); k++) {
    QStringList const &group(groups[k]);
    Range const &dx(dxx[k]);
    Range const &px(pxx[k]);
    // qDebug() << "  rng " << group << dx.min() << dx.max() << "=>" << px.min() << px.max();
    double x0 = dx.min();
    double x1 = dx.max();
    double sc = px.range() / dx.range();
    for (QString id: group) {
      Axis &axis = de.axis(f.panelRef(id));
      bool rev = de.point(axis.maprel(1)) < 0;
      // rev indicates wheter (d-,d+) -> (p+,p-) or (d-,d+)->(p-,p+)
      double px0 = rev ? px.max() : px.min();
      double px1 = rev ? px.min() : px.max();
      // px0, px1 are paper target for x0, x1; regardless of rev
      double a = rev ? (-scale) : scale;
      double b = (px0+px1)/2 - a * (x0+x1)/2;
      double PX0 = a*axis.min()+b;
      double PX1 = a*axis.max()+b;
      //qDebug() << "  place" << id << a << b
      //         << "|" << axis.min() << axis.max()
      //         << "|" << de.point(axis.minp()) << PX0
      //         << "|" << de.point(axis.maxp()) << PX1;
      // qDebug() << id << x0 << x1 << px0 << px1 << a << b;
      if (fabs(de.point(axis.minp()) - PX0) > SHIFTTOLERANCE
          || fabs(de.point(axis.maxp()) - PX1) > SHIFTTOLERANCE) {
        axis.setPlacement(de.repoint(QPointF(), PX0),
                          de.repoint(QPointF(), PX1));
        f.markFudged();
      }
    }
  }
}
