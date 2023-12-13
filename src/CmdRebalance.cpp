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
#include "DimExtractor.h"

static CBuilder<CmdRebalance> cbRebalance("rebalance");

constexpr double SCALETOLERANCE = 2e-3;
constexpr double SPACETOLERANCE = 1; // pt

constexpr double MINOVERLAP = 5; // pt

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
    QList<Range> ranges = scale(f, ids[0], DimExtractor::x());
    if (!ranges.isEmpty()) 
      for (int k=1; k<ids.size(); ++k)
        propagate(f, ids[k], ranges, DimExtractor::x());
  }

  if (px.range() > MINOVERLAP) {
    QList<Range> ranges = scale(f, ids[0], DimExtractor::y());
    if (!ranges.isEmpty()) 
      for (int k=1; k<ids.size(); ++k)
        propagate(f, ids[k], ranges, DimExtractor::y());
  }
}

QList<Range> CmdRebalance::scale(Figure &f, QStringList ids,
                                 DimExtractor const &de) {
  qDebug() << "rebalance" << ids;

  // Get space available
  QRectF fullextent;
  for (QString id: ids) {
    Panel const &p(f.panelRef(id));
    if (fullextent.isEmpty())
      fullextent = p.desiredExtent;
    else
      fullextent |= p.desiredExtent;
  }
  
  // Estimate space needs
  QMap<QString, double> nondatause; // paper coords
  QMap<QString, double> datarange;
  QMap<QString, double> oldwidth;
  for (QString id: ids) {
    Panel const &p(f.panelRef(id));
    Axis const &axis(de.axis(p));
    Range fullbb(de.rectRange(p.fullbbox));
    Range desibb(de.rectRange(p.desiredExtent));
    oldwidth[id] = desibb.range();
    Range databb(de.axisPRange(axis));
    double prespace = databb.min() - fullbb.min();
    double postspace = fullbb.max() - databb.max();
    nondatause[id] = prespace + postspace;
    datarange[id] = fabs(axis.max() - axis.min());
  }
  double totalnondatause = 0;
  for (double dx: nondatause)
    totalnondatause += dx;
  double totaldatarange = 0;
  for (double dx: datarange)
    totaldatarange += dx;

  double fullwidth = de.rectRange(fullextent).range();
  double scale = (fullwidth - totalnondatause) / totaldatarange;
  qDebug() << "  scale" << scale << "full" << fullwidth;
  
  // Figure out new proposal for sharing space
  bool trivial = true;
  QMap<QString, double> propwidth;
  for (QString id: ids) {
    Panel const &panel(f.panelRef(id));
    Axis const &axis(panel.xaxis);
    double desired = nondatause[id] + datarange[id] * scale;
    propwidth[id] = desired;
    qDebug() << "  " << id << nondatause[id] << datarange[id] << oldwidth[id] << propwidth[id];
    if (fabs(desired - oldwidth[id]) > SPACETOLERANCE)
      trivial = false;
  }
  if (trivial)
    return QList<Range>();

  // Apply the scale to all panels
  QList<Range> ranges;
  double x0 = de.rectMin(fullextent);
  for (QString id: ids) {
    Panel const &panel(f.panelRef(id));
    double x1 = x0 + propwidth[id];
    QRectF ext = de.rerect(fullextent, x0, x1);
    ranges << Range(x0, x1);
    f.overridePanelExtent(id, ext);
    x0 = x1;
  }
  qDebug() << "  => " << fullextent << x0;
  f.markFudged();
  return ranges;
}

void CmdRebalance::propagate(Figure &f, QStringList ids, QList<Range> src,
                             DimExtractor const &de) {
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
    Axis const &axis(de.axis(panel));
    QRectF ext = de.rerect(fullextent, src[n].min(), src[n].max());
    f.overridePanelExtent(ids[n], ext);
  }  
}

