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

#include <QDebug>
#include <math.h>
#include "Error.h"
#include "Range.h"

static CBuilder<CmdCommonScale> cbCommonScale("commonscale");

#define SCALETOLERANCE 1e-4
#define SHIFTTOLERANCE 1e-3
#define MINOVERLAP 5

bool CmdCommonScale::usage() {
  return error("Usage: commonscale [x|y|xy] ID ...\n");
}

bool CmdCommonScale::parse(Statement const &s) {
  if (s.length()<2)
    return usage(); // we could allow this null case, but that might confuse

  int i0 = 1;
  if (s[1].typ==Token::BAREWORD) {
    if (s[1].str=="x" || s[1].str=="y" || s[1].str=="xy")
      i0 += 1;
    else
      return usage();
  }
  if (s.length() - i0 < 2)
    return usage();
  for (int i=i0; i<s.length(); i++) 
    if (s[i].typ!=Token::CAPITAL)
      return usage();
  return true;
}

void CmdCommonScale::render(Statement const &s, Figure &f, bool) {
  bool shareX = true;
  bool shareY = true;
  QSet<QString> ids;
  int i0 = 1;
  if (s[1].typ==Token::BAREWORD) {
    if (s[1].str=="x")
      shareY = false;
    if (s[1].str=="y")
      shareX = false;
    i0 += 1;
  }
  for (int i=i0; i<s.length(); i++) {
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
    scaleX(f, ids);

  if (shareY) 
    scaleY(f, ids);
}

void CmdCommonScale::scaleX(Figure &f, QSet<QString> ids) {
  // Get the scale
  double scale = 1e99; // will be overwritten
  foreach (QString id, ids) {
    Panel const &p(f.panelRef(id));
    double sc1 = p.xaxis.maprel(1).x();
    if (sc1<scale)
      scale = sc1;
  }

  // Apply the scale to all panels
  for (QString id: ids) {
    Axis &axis(f.panelRef(id).xaxis);
    double sc1 = axis.maprel(1).x();
    if (sc1>scale*(1+SCALETOLERANCE)) { // || sc1<scale*(1-SCALETOLERANCE)) {
      // Let's actually shrink
      double currentWidth = axis.maxp().x() - axis.minp().x();
      double newWidth = currentWidth * scale/sc1;
      double shift = (currentWidth - newWidth)/2;
      axis.setPlacement(QPointF(axis.minp().x() + shift, 0),
                        QPointF(axis.maxp().x() - shift, 0));
      f.markFudged();
    }
  }
}

void CmdCommonScale::scaleY(Figure &f, QSet<QString> ids) {
  // Get the scale
  double scale = 1e99; // will be overwritten
  foreach (QString id, ids) {
    Panel const &p(f.panelRef(id));
    double sc1 = fabs(p.yaxis.maprel(1).y());
    if (sc1<scale)
      scale = sc1;
  }

  // Apply the scale to all panels
  for (QString id: ids) {
    Axis &axis(f.panelRef(id).yaxis);
    double sc1 = fabs(axis.maprel(1).y());
    if (sc1>scale*(1+SCALETOLERANCE)) {
      // Let's actually shrink
      double currentHeight = axis.minp().y() - axis.maxp().y();
      double newHeight = currentHeight * scale/sc1;
      double shift = (currentHeight - newHeight)/2;
      axis.setPlacement(QPointF(0, axis.minp().y()-shift),
                             QPointF(0, axis.maxp().y()+shift));
      f.markFudged();
    }
  }
}

