// CmdCommonScale.cpp - This file is part of QPlot

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

// CmdCommonScale.C

#include "CmdCommonScale.h"
#include "WhichAxis.h"
#include <QDebug>
#include <math.h>
#include "Error.h"
#include "Range.h"

static CBuilder<CmdCommonScale> cbCommonScale("commonscale");

#define SCALETOLERANCE 1e-3

bool CmdCommonScale::usage() {
  return error("Usage: commonscale x|y|xy ID ...\n");
}

bool CmdCommonScale::parse(Statement const &s) {
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

void CmdCommonScale::render(Statement const &s, Figure &f, bool) {
  bool shareX = s[1].str.contains("x");
  bool shareY = s[1].str.contains("y");

  QSet<QString> ids;
  for (int i=2; i<s.length(); i++) {
    if (f.hasPanel(s[i].str)) {
      ids.insert(s[i].str);
    } else {
      Error() << "Unknown panel: " << s[i].str;
      return;
    }
  }
  // Now we know that all IDS are actual panels.

  f.leavePanel();

  if (shareX) 
    scale(f, ids, WhichAxis::x());

  if (shareY) 
    scale(f, ids, WhichAxis::y());
}

void CmdCommonScale::scale(Figure &f, QSet<QString> ids,
                           WhichAxis const &de) {
  // Get the scale
  double scale = -1; // will be overwritten
  foreach (QString id, ids) {
    Panel const &p(f.panelRef(id));
    Axis const &a(de.axis(p));
    double sc1 = fabs(de.point(a.maprel(1)));
    if (scale<0 || sc1<scale)
      scale = sc1;
  }

  // Apply the scale to all panels
  for (QString id: ids) {
    Axis &axis(de.axis(f.panelRef(id)));
    double sc1 = de.point(axis.maprel(1));
    bool rev = sc1<0;
    sc1 = fabs(sc1);
    double px0 = de.point(axis.minp());
    double px1 = de.point(axis.maxp());
    if (sc1>scale*(1+SCALETOLERANCE)) {
      // Let's actually shrink
      double currentWidth = de.axisPRange(axis).range();
      double newWidth = currentWidth * scale/sc1;
      double shift = (currentWidth - newWidth)/2;
      axis.setPlacement(de.repoint(QPointF(), px0 + shift),
                        de.repoint(QPointF(), px1 - shift));
      f.markFudged();
    }
  }
}
