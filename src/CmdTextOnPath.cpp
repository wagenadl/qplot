// CmdTextOnPath.cpp - This file is part of QPlot

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

// CmdTextOnPath.C

#include "CmdTextOnPath.h"
#include "Rotate.h"
#include "Range.h"
#include <QDebug>
#include <QFontMetricsF>
#include <math.h>

static CBuilder<CmdTextOnPath> cbTextOnPath("textonpath");

bool CmdTextOnPath::usage() {
  return error("Usage: textonpath xdata ydata dxpaper dypaper text");
}

bool CmdTextOnPath::parse(Statement const &s) {
  int id1 = s.nextIndex(1);
  int id2 = s.nextIndex(id1);
  if (s.isNumeric(1) && s.isNumeric(id1)
      && id2==s.length()-3
      && s.data(1).size()==s.data(id1).size()
      && s[id2].typ==Token::NUMBER
      && s[id2+1].typ==Token::NUMBER
      && s[id2+2].typ==Token::STRING)
    return true;
  else
    return usage();
}

static double euclideanLength(QPointF p) {
  return ::sqrt(p.x()*p.x() + p.y()*p.y());
}

static QPair<QPointF, double> interpretAlong(QPolygonF const &pp,
                                             QVector<double> const &eta,
                                             double w) {
  int K = eta.size();
  if (K<2)
    return QPair<QPointF, double>(QPointF(), 0);

  if (w<0) {
    // special case at start
    double ang = atan2(pp[1].y()-pp[0].y(), pp[1].x()-pp[0].x());
    return QPair<QPointF, double>(pp[0] + QPointF(w*cos(ang), w*sin(ang)), ang);
  } else if (w>=eta.last()) {
    // special case at start
    w -= eta.last();
    double ang = atan2(pp[K-1].y()-pp[K-2].y(), pp[K-1].x()-pp[K-2].x());
    return QPair<QPointF, double>(pp.last()
                                  + QPointF(w*cos(ang), w*sin(ang)), ang);
  }
  
  int k = 0;
  while (w>eta[k])
    k++;
  // so now w<=eta[k]
  if (w==eta[k]) {
    double ang = atan2(pp[k+1].y()-pp[k-1].y(), pp[k+1].x()-pp[k-1].x());
    return QPair<QPointF, double>(pp[k], ang);
  } else {
    // between k-1 and k
    double q = (w-eta[k-1]) / (eta[k] - eta[k-1] + 1e-9); // avoid abort
    double ang = atan2(pp[k].y()-pp[k-1].y(), pp[k].x()-pp[k-1].x());
    return QPair<QPointF, double>((1-q)*pp[k-1] + q*pp[k], ang);
  }
}

QRectF CmdTextOnPath::dataRange(Statement const &s) {
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

void CmdTextOnPath::render(Statement const &s, Figure &f, bool dummy) {
  QVector<double> const &xdata = s.data(1);
  int id1 = s.nextIndex(1);
  QVector<double> const &ydata = s.data(id1);
  int id2 = s.nextIndex(id1);

  double dxbase = pt2iu(s[id2].num);
  double dybase = pt2iu(s[id2+1].num);
  QString txt = s[id2+2].str;

  if (xdata.isEmpty()) {
    f.setBBox(QRectF());
    return;
  }

  // build up polygon
  QPolygonF pp(xdata.size());
  for (int k=0; k<xdata.size(); k++)
    pp[k] = f.map(xdata[k],ydata[k]);

  // measure cumulative length along polygon
  QVector<double> eta(xdata.size());
  eta[0] = 0;
  for (int k=1; k<xdata.size(); k++)
    eta[k] = eta[k-1] + euclideanLength(pp[k] - pp[k-1]);

  // measure cumulative length of text
  // Really we should use our fancy interpreted text, but not tonight
  QFontMetricsF fm(f.painter().font());
  QVector<double> xi(txt.length()+1);
  Range textYRange;
  QVector<QRectF> rr(txt.length());
  QVector<double> ww(txt.length());
  xi[0] = 0;
  // QTextOption opt;
  // opt.setFlags(QTextOption::IncludeTrailingSpaces);
  for (int i=0; i<txt.length(); i++) {
    QRectF r = fm.tightBoundingRect(txt.mid(i, 1)); //, opt);
    textYRange.extend(r.top());
    textYRange.extend(r.bottom());
    double w = fm.horizontalAdvance(txt.mid(i, 1));
    ww[i] = w;
    xi[i+1] = xi[i] + w;
    rr[i] = r;
  }
  // xi[i], xi[i+1] is now the position at the left, right end of letter i

  double dy = dybase;
  switch (f.vAlign()) {
  case Align::TOP:
    dy -= textYRange.min();
    break;
  case Align::MIDDLE:
    dy -= textYRange.min()/2 + textYRange.max()/2;
    break;
  case Align::BASE:
    break;
  case Align::BOTTOM:
    dy -= textYRange.max();
    break;
  }
  
  QRectF bb;
  double dxi = dxbase;
  switch (f.hAlign()) {
  case Align::LEFT:
    break; 
  case Align::CENTER:
    dxi += eta.last()/2 - xi.last()/2;
    break;
  case Align::RIGHT:
    dxi += eta.last() - xi.last();
    break;
  }
  
  for (int i=0; i<txt.length(); i++) {
    QPair<QPointF, double> p
      = interpretAlong(pp, eta, (xi[i]+xi[i+1])/2 + dxi);
    QRectF r = ::rotate(rr[i].translated(0, dy), p.second).translated(p.first);
    bb |= r;
    if (!dummy) {
      f.painter().save();
      f.painter().translate(p.first);
      f.painter().rotate(p.second * 180 / 3.14159265);
      f.painter().drawText(-ww[i]/2, dy, txt.mid(i, 1));
      f.painter().restore();
    }
  }
  f.setBBox(bb);
}
