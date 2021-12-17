// CmdMark.cpp - This file is part of QPlot

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

// CmdMark.C

#include "CmdMark.h"
#include <math.h>
#include <QPolygonF>
#include "Rotate.h"
#include "Slightly.h"
#include "pi.h"
#include <QDebug>

static CBuilder<CmdMark> cbMark("mark");
static CBuilder<CmdMark> cbPMark("pmark");

bool CmdMark::usage() {
  return error("Usage: mark|pmark xdata ydata [rx [ry [1]]]");
}

static void rendermark(QPainter &p, QPointF const &xy,
		       double r, Marker::Type t, bool asSpine) {
  QPolygonF pf;
  switch (t) {
  case Marker::CIRCLE:
    p.drawEllipse(xy, r, r);
    break;
  case Marker::SQUARE:
    r *= sqrt(PI/4);
    if (asSpine) {
      p.drawLine(QPointF(xy)+QPointF(-r,-r), QPointF(xy)+QPointF(r,r));
      p.drawLine(QPointF(xy)+QPointF(-r,r), QPointF(xy)+QPointF(r,-r));
    } else {
      p.drawRect(QRectF(xy + QPointF(-r,-r), QSizeF(2*r, 2*r)));
    }
    break;
  case Marker::DIAMOND: 
    r *= sqrt(2*PI/4);
    pf.resize(4);
    pf[0] = xy + QPointF(-r, 0);
    pf[1] = xy + QPointF(0, -r);
    pf[2] = xy + QPointF(r, 0);
    pf[3] = xy + QPointF(0, r);
    if (asSpine) {
      p.drawLine(pf[0], pf[2]);
      p.drawLine(pf[1], pf[3]);
    } else {
      p.drawConvexPolygon(pf);
    }
    break;
  case Marker::LEFTTRIANGLE:
    r *= 2./3;
    pf.resize(3);
    pf[0] = xy + QPointF(-2*r, 0);
    pf[1] = xy + QPointF(r, -sqrt(3)*r);
    pf[2] = xy + QPointF(r, sqrt(3)*r);
    if (asSpine) {
      p.drawLine(xy, pf[0]);
      p.drawLine(xy, pf[1]);
      p.drawLine(xy, pf[2]);
    } else {
      p.drawConvexPolygon(pf);
    }
    break;
  case Marker::DOWNTRIANGLE:
    r *= 2./3;
    pf.resize(3);
    pf[0] = xy + QPointF(0, 2*r);
    pf[1] = xy + QPointF(-sqrt(3)*r, -r);
    pf[2] = xy + QPointF(sqrt(3)*r, -r);
    if (asSpine) {
      p.drawLine(xy, pf[0]);
      p.drawLine(xy, pf[1]);
      p.drawLine(xy, pf[2]);
    } else {
      p.drawConvexPolygon(pf);
    }
    break;
  case Marker::RIGHTTRIANGLE:
    r *= 2./3;
    pf.resize(3);
    pf[0] = xy + QPointF(2*r, 0);
    pf[1] = xy + QPointF(-r, sqrt(3)*r);
    pf[2] = xy + QPointF(-r, -sqrt(3)*r);
    if (asSpine) {
      p.drawLine(xy, pf[0]);
      p.drawLine(xy, pf[1]);
      p.drawLine(xy, pf[2]);
    } else {
      p.drawConvexPolygon(pf);
    }
    break;
  case Marker::UPTRIANGLE:
    r *= 2./3;
    pf.resize(3);
    pf[0] = xy + QPointF(0, -2*r);
    pf[1] = xy + QPointF(-sqrt(3)*r, r);
    pf[2] = xy + QPointF(sqrt(3)*r, r);
    if (asSpine) {
      p.drawLine(xy, pf[0]);
      p.drawLine(xy, pf[1]);
      p.drawLine(xy, pf[2]);
    } else {
      p.drawConvexPolygon(pf);
    }
    break;
  case Marker::PENTAGRAM: {
    r *= .5 + .5*sqrt(5);
    double r1 = .5*sqrt(5)-.5;
    r1=r1*r1;
    pf.resize(10);
    for (int k=0; k<10; k++) {
      double dy = -r*cos(2*PI*k/10);
      double dx = r*sin(2*PI*k/10);
      if (k&1) {
	dx *= r1;
	dy *= r1;
      }
      pf[k] = xy + QPointF(dx, dy);
    }
    if (asSpine) {
      for (int k=0; k<10; k+=2)
	p.drawLine(xy, pf[k]);
    } else {
      p.drawPolygon(pf);
    }
  } break;
  case Marker::HEXAGRAM: {
    r=r*sqrt(sqrt(3));
    double r1 = 1/sqrt(3);
    pf.resize(12);
    for (int k=0; k<12; k++) {
      double dy = r*cos(2*PI*k/12);
      double dx = -r*sin(2*PI*k/12);
      if (k&1) {
	dx *= r1;
	dy *= r1;
      }
      pf[k] = xy + QPointF(dx, dy);
    }
    if (asSpine) {
      for (int k=0; k<6; k+=2)
	p.drawLine(pf[k], pf[k+6]);
    } else {
      p.drawPolygon(pf);
    }
  } break;
  case Marker::PLUS:
    p.drawLine(xy + QPointF(r,0), xy + QPointF(-r,0));
    p.drawLine(xy + QPointF(0,r), xy + QPointF(0,-r));
    break;
  case Marker::CROSS:
    r /= sqrt(2);
    p.drawLine(xy + QPointF(r,r), xy + QPointF(-r,-r));
    p.drawLine(xy + QPointF(-r,r), xy + QPointF(r,-r));
    break;
  case Marker::HBAR:
    p.drawLine(xy + QPointF(r,0), xy + QPointF(-r,0));
    break;
  case Marker::VBAR:
    p.drawLine(xy + QPointF(0,r), xy + QPointF(0,-r));
    break;
  case Marker::STAR: {
    double rx = 0.5*r; // cos(60)
    double ry = 0.866*r; // sin(60)
    p.drawLine(xy + QPointF(r,0), xy + QPointF(-r,0));
    p.drawLine(xy + QPointF(rx,ry), xy + QPointF(-rx,-ry));
    p.drawLine(xy + QPointF(rx,-ry), xy + QPointF(-rx,ry));
  } break;
  }
}      
      
bool CmdMark::parse(Statement const &s) {
  int id1 = s.nextIndex(1);
  int id2 = s.nextIndex(id1);
  qDebug() << "parse mark" << s.length() << s.data(1).size() << s.data(id1).size();
  if (!s.isNumeric(1) || !s.isNumeric(id1)
      || s.data(1).size()!=s.data(id1).size())
    return usage();
  if (id2==s.length())
    return true;
  if (s[0].str=="pmark")
    return usage();
  if (!s.isNumeric(id2) || s.data(id2).size()!=1) // rx
    return usage();
  int id3 = s.nextIndex(id2);
  if (id3==s.length())
    return true;
  if (!s.isNumeric(id3) || s.data(id3).size()!=1) // ry
    return usage();
  int id4 = s.nextIndex(id3);
  if (id4==s.length())
    return true;
  if (!s.isNumeric(id4) || s.data(id4).size()!=1) // isvert
    return usage();
  int id5 = s.nextIndex(id4);
  if (id5==s.length())
    return true;
  return usage();
}

QRectF CmdMark::dataRange(Statement const &s) {
  if (s[0].str=="pmark")
    return QRectF(); // paper coord -> no data range

  
  QVector<double> const &xdata = s.data(1);
  QVector<double> const &ydata = s.data(s.nextIndex(1));

  if (xdata.isEmpty())
    return QRectF();

  double minx = xdata[0];
  double maxx = xdata[0];
  double miny = ydata[0];
  double maxy = ydata[0];

  for (int k=1; k<xdata.size(); k++)
    if (xdata[k]<minx)
      minx=xdata[k];
    else if (xdata[k]>maxx)
      maxx=xdata[k];
  for (int k=1; k<ydata.size(); k++)
    if (ydata[k]<miny)
      miny=ydata[k];
    else if (ydata[k]>maxy)
      maxy=ydata[k];
  return QRectF(QPointF(Slightly::less(minx), Slightly::less(miny)),
		QPointF(Slightly::more(maxx), Slightly::more(maxy)));
}

QPolygonF avoidCollision(QPolygonF const &in, double rx, double ry, bool ver) {
  QPolygonF out;
  auto sqr = [](double x) { return x*x; };
  double rx2 = sqr(rx);
  double ry2 = sqr(ry);
  auto collides = [&out, rx2, ry2, sqr](QPointF const &p) {
                    for (QPointF const &q: out) {
                      if (sqr(p.x()-q.x())/rx2 + sqr(p.y()-q.y())/ry2 < 1)
                        return true;
                    }
                    return false;
                  };
  for (QPointF const &p: in) {
    double dx = 0;
    while (collides(p + (ver ? QPointF(0,dx) : QPointF(dx,0))))
      if (dx>0)
        dx = -dx;
      else
        dx = -dx + rx;
    out.append(p + (ver ? QPointF(0,dx) : QPointF(dx,0)));
  }
  return out;
}

    

void CmdMark::render(Statement const &s, Figure &f, bool dryrun) {
  QVector<double> const &xdata = s.data(1);
  int idx = s.nextIndex(1);
  QVector<double> const &ydata = s.data(idx);
  if (xdata.isEmpty()) {
    f.setBBox(QRectF());
    return;
  }
  double rx = 0;
  double ry = 0;
  bool hori = false;
  bool vert = false;
  idx = s.nextIndex(idx);
  if (idx < s.length()) {
    hori = true;
    rx = pt2iu(s.data(idx)[0]);
    ry = rx;
    idx = s.nextIndex(idx);
    if (idx < s.length()) {
      ry = pt2iu(s.data(idx)[0]);
      idx = s.nextIndex(idx);
      if (idx < s.length()) {
        vert = s.data(idx)[0]!=0;
        hori = !vert;
      }
    }
  }
  
  QPolygonF pp(xdata.size());

  if (s[0].str=="mark") {
    for (int k=0; k<xdata.size(); k++)
      pp[k] = f.map(xdata[k], ydata[k]);
    if (hori) 
      pp = avoidCollision(pp, rx, ry, false);
    else if (vert)
      pp = avoidCollision(pp, rx, ry, true);
  } else { // pmark
    double a = f.anchorAngle();
    QPointF xy0 = f.anchor();
    for (int k=0; k<xdata.size(); k++) {
      QPointF xy(pt2iu(xdata[k]), pt2iu(ydata[k]));
      if (a)
	xy = ::rotate(xy, a);
      xy += xy0;
      pp[k] = xy;
    }
  }

  QRectF bbox = pp.boundingRect();
  double w = f.painter().pen().widthF();
  if (w>0)
    bbox.adjust(-w/2, -w/2, w/2, w/2);
  double r = f.marker().radius;
  bbox.adjust(-r, -r, r, r);
  f.setBBox(bbox);
  
  if (dryrun)
    return;

  QPainter &ptr(f.painter());
  ptr.save();

  bool asSpine = false;
  switch (f.marker().fill) {
  case Marker::CLOSED:
    ptr.setBrush(ptr.pen().color());
    break;
  case Marker::OPEN:
    ptr.setBrush(QColor("white"));
    break;
  case Marker::BRUSH:
    break;
  case Marker::SPINE:
    asSpine = true;
    break;
  }

  Marker::Type t = f.marker().type;

  for (QPointF const &p: pp)
    rendermark(ptr, p, r, t, asSpine);

  ptr.restore();  
}
