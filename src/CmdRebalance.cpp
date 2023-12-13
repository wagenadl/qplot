// CmdRebalance.cpp - This file is part of QPlot

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

// CmdRebalance.C

#include "CmdRebalance.h"

#include <QDebug>
#include <math.h>
#include "Error.h"
#include "Range.h"

static CBuilder<CmdRebalance> cbRebalance("rebalance");

#define SCALETOLERANCE 2e-3
#define MINOVERLAP 5

bool CmdRebalance::usage() {
  return error("Usage: rebalance ID ...\n");
}

static QList<QStringList> idlists(Statement const &s) {
  QList<QStringList> result;
  QStringList current;
  for (int i=1; i<s.length(); i++) {
    if (s[i].typ==Token::CAPITAL) {
      current << s[i].str;
    } else if (s[i].typ==Token::DASH) {
      result << current;
      current = QStringList();
    } else {
      return QList<QStringList>(); // fail if unexpected token
    }
  }
  if (!current.isEmpty())
    result << current; // we tolerate final DASH
  if (result.isEmpty())
    return QList<QStringList>(); // fail if nothing read
  int N = result[0].size();
  if (N<2)
    return QList<QStringList>(); // fail if not at least two IDs in primary list
  for (int i=1; i<result.size(); ++i)
    if (result[i].size() != N)
      return QList<QStringList>(); // fail if length mismatch
  return result;
}
  

bool CmdRebalance::parse(Statement const &s) {
  return idlists(s).isEmpty() ? usage() : true;
}

void CmdRebalance::render(Statement const &s, Figure &f, bool) {
  QList<QStringList> ids = idlists(s);
  for (QStringList ids1: ids) {
    for (QString id: ids1) {
      if (!f.hasPanel(id)) {
        Error() << "Unknown panel: " << id;
        return;
      }
    }
  }
  // Now we know that all IDS are actual panels.

  f.leavePanel();

  // Let's find out if we have paper overlap in x, y 
  Range px, py;
  bool first = true;
  for (QString id: ids[0]) {
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

  if (py.range() > MINOVERLAP) {
    QList<QRectF> rects = scaleX(f, ids[0]);
    if (!rects.isEmpty()) 
      for (int k=1; k<ids.size(); ++k)
        propagateX(f, ids[k], rects);
  }

  if (px.range() > MINOVERLAP) {
    QList<QRectF> rects = scaleY(f, ids[0]);
    if (!rects.isEmpty()) 
      for (int k=1; k<ids.size(); ++k)
        propagateY(f, ids[k], rects);
  }
}

QList<QRectF> CmdRebalance::scaleX(Figure &f, QStringList ids) {
  qDebug() << "rebalance x" << ids;
  // Estimate the common scale
  double scale = 1; // will be overwritten
  int N = 0;
  QRectF fullextent;
  for (QString id: ids) {
    Panel const &p(f.panelRef(id));
    scale *= fabs(p.xaxis.maprel(1).x());
    if (N==0)
      fullextent = p.desiredExtent;
    else
      fullextent |= p.desiredExtent;
    N += 1;
  }
  scale = pow(scale, 1.0/N);

  double fullwidth = fullextent.width();
  qDebug() << "  scale" << scale << "full" << fullwidth;
  
  // Figure out new proposal for sharing space
  bool trivial = true;
  double proposedwidth = 0;
  for (QString id: ids) {
    Panel const &panel(f.panelRef(id));
    Axis const &axis(panel.xaxis);
    double sc1 = fabs(axis.maprel(1).x());
    if (sc1 > scale*(1+SCALETOLERANCE) || sc1 < scale*(1-SCALETOLERANCE))
      trivial = false;
    double desired = (scale/sc1) * panel.desiredExtent.width();
    qDebug() << "  " << id << sc1 << desired << panel.desiredExtent.width();
    proposedwidth += desired;
  }
  if (trivial)
    return QList<QRectF>();

  // Apply the scale to all panels
  QList<QRectF> rects;
  double x0 = fullextent.left();
  for (QString id: ids) {
    Panel const &panel(f.panelRef(id));
    Axis const &axis(panel.xaxis);
    double sc1 = fabs(axis.maprel(1).x());
    double desired = (scale/sc1) * panel.desiredExtent.width();
    QRectF ext(x0, fullextent.top(), desired, fullextent.height());
    rects << ext;
    f.overridePanelExtent(id, ext);
    x0 += desired;
  }
  f.markFudged();
  return rects;
}

void CmdRebalance::propagateX(Figure &f, QStringList ids, QList<QRectF> src) {
  QRectF fullextent;
  for (QString id: ids) {
    Panel const &p(f.panelRef(id));
    if (fullextent.isEmpty())
      fullextent = p.desiredExtent;
    else
      fullextent |= p.desiredExtent;
  }

  for (int n=0; n<ids.size(); n++) {
    Panel const &panel(f.panelRef(ids[n]));
    Axis const &axis(panel.xaxis);
    QRectF r = src[n];
    QRectF ext = QRectF(r.left(), fullextent.top(),
                        r.width(), fullextent.height());
    f.overridePanelExtent(ids[n], ext);
  }  
}


QList<QRectF> CmdRebalance::scaleY(Figure &f, QStringList ids) {
  qDebug() << "rebalance y" << ids;
  // Estimate the common scale
  double scale = 1; // will be overwritten
  int N = 0;
  QRectF fullextent;
  for (QString id: ids) {
    Panel const &p(f.panelRef(id));
    scale *= fabs(p.yaxis.maprel(1).y());
    if (N==0)
      fullextent = p.desiredExtent;
    else
      fullextent |= p.desiredExtent;
    N += 1;
  }
  scale = pow(scale, 1.0/N);

  double fullheight = fullextent.height();
  qDebug() << "  scale" << scale << "full" << fullheight;
  
  // Figure out new proposal for sharing space
  bool trivial = true;
  double proposedheight = 0;
  for (QString id: ids) {
    Panel const &panel(f.panelRef(id));
    Axis const &axis(panel.yaxis);
    double sc1 = fabs(axis.maprel(1).y());
    if (sc1 > scale*(1+SCALETOLERANCE) || sc1 < scale*(1-SCALETOLERANCE))
      trivial = false;
    double desired = (scale/sc1) * panel.desiredExtent.height();
    qDebug() << "  " << id << sc1 << desired << panel.desiredExtent.height();
    proposedheight += desired;
  }
  if (trivial)
    return QList<QRectF>();

  // Apply the scale to all panels
  QList<QRectF> rects;
  double y0 = fullextent.top();
  for (QString id: ids) {
    Panel const &panel(f.panelRef(id));
    Axis const &axis(panel.yaxis);
    double sc1 = fabs(axis.maprel(1).y());
    double desired = (scale/sc1) * panel.desiredExtent.height();
    QRectF ext(fullextent.left(), y0, fullextent.width(), desired);
    rects << ext;
    f.overridePanelExtent(id, ext);
    y0 += desired;
  }
  f.markFudged();
  return rects;
}


void CmdRebalance::propagateY(Figure &f, QStringList ids, QList<QRectF> src) {
  QRectF fullextent;
  for (QString id: ids) {
    Panel const &p(f.panelRef(id));
    if (fullextent.isEmpty())
      fullextent = p.desiredExtent;
    else
      fullextent |= p.desiredExtent;
  }

  for (int n=0; n<ids.size(); n++) {
    Panel const &panel(f.panelRef(ids[n]));
    Axis const &axis(panel.xaxis);
    QRectF r = src[n];
    QRectF ext = QRectF(fullextent.left(), r.top(),
                        fullextent.width(), r.height());
    f.overridePanelExtent(ids[n], ext);
  }  
}
