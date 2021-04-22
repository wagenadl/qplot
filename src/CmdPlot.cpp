// CmdPlot.cpp - This file is part of QPlot

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

// CmdPlot.C

#include "CmdPlot.h"
#include "Rotate.h"
#include "Range.h"
#include <QDebug>
#include <cmath>

static CBuilder<CmdPlot> cbPlot("plot");
static CBuilder<CmdPlot> cbPatch("patch");
static CBuilder<CmdPlot> cbLine("line");
static CBuilder<CmdPlot> cbArea("area");

bool CmdPlot::usage() {
  return error("Usage: plot|patch|line|area xdata ydata");
}

bool CmdPlot::parse(Statement const &s) {
  int id1 = s.nextIndex(1);
  int id2 = s.nextIndex(id1);
  if (id2==s.length() && s.isNumeric(1) && s.isNumeric(id1) &&
      s.data(1).size()==s.data(id1).size())
    return true;
  else
    return usage();
}

QRectF CmdPlot::dataRange(Statement const &s) {
  if (s[0].str=="line" || s[0].str=="area")
    return QRectF();
  
  QVector<double> const &xdata = s.data(1);
  QVector<double> const &ydata = s.data(s.nextIndex(1));

  if (xdata.isEmpty())
    return QRectF();

  Range rangex, rangey;
  foreach (double x, xdata)
    rangex.extend(x);
  foreach (double y, ydata)
    rangey.extend(y);
  return QRectF(QPointF(rangex.min(),rangey.min()),
                QPointF(rangex.max(),rangey.max()));
}

void CmdPlot::render(Statement const &s, Figure &f, bool dryrun) {
  QVector<double> const &xdata = s.data(1);
  QVector<double> const &ydata = s.data(s.nextIndex(1));
  if (xdata.isEmpty()) {
    f.setBBox(QRectF());
    return;
  }

  QPainterPath p;
  bool lastnan = true;
  
  if (s[0].str=="plot" || s[0].str=="patch") {
    for (int k=0; k<xdata.size(); k++) {
      if (std::isnan(xdata[k]) || std::isnan(ydata[k])) {
        lastnan = true;
      } else {
        if (lastnan)
          p.moveTo(f.map(xdata[k],ydata[k]));
        else
          p.lineTo(f.map(xdata[k],ydata[k]));
        lastnan = false;
      }
    }
  } else {
    double a = f.anchorAngle();
    QPointF xy0 = f.anchor();
    for (int k=0; k<xdata.size(); k++) {
      if (std::isnan(xdata[k]) || std::isnan(ydata[k])) {
        lastnan = true;
      } else {
        QPointF xy(pt2iu(xdata[k]), pt2iu(ydata[k]));
        if (a)
          xy = ::rotate(xy, a);
        xy += xy0;
        if (lastnan)
          p.moveTo(xy);
        else
          p.lineTo(xy);
        lastnan = false;
      }
    }
  }

  if (s[0].str=="patch" || s[0].str=="area")
    p.closeSubpath();
  
  QRectF bbox = p.boundingRect();
  double w = f.painter().pen().widthF();
  if (w>0)
    bbox.adjust(-w/2, -w/2, w/2, w/2);
  /* Adjust for line width.
     This does not take protruding miters into account.
  */
  f.setBBox(bbox);

  if (dryrun)
    return;

  QBrush b = f.painter().brush();
  if (s[0].str=="plot" || s[0].str=="line")
    f.painter().setBrush(QBrush(Qt::NoBrush));

  f.painter().drawPath(p);

  if (s[0].str=="plot" || s[0].str=="line")
    f.painter().setBrush(b);
}
