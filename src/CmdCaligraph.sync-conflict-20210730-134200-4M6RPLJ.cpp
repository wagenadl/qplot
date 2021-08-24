// CmdCaligraph.cpp - This file is part of QPlot

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

// CmdCaligraph.C

#include "CmdCaligraph.H"
#include "Rotate.H"

#include <QDebug>
#include <math.h>

static CBuilder<CmdCaligraph> cbCaligraph("caligraph");

bool CmdCaligraph::usage() {
  return error("Usage: caligraph xdata ydata widthdata");
}

bool CmdCaligraph::parse(Statement const &s) {
  int id1 = s.nextIndex(1);
  int id2 = s.nextIndex(id1);
  int id3 = s.nextIndex(id2);
  if (id3==s.length()
      && s.isNumeric(1) && s.isNumeric(id1) && s.isNumeric(3)
      && s.data(1).size()==s.data(id1).size() 
      && s.data(1).size()==s.data(id2).size() )
    return true;
  else
    return usage();
}

QRectF CmdCaligraph::dataRange(Statement const &s) {
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
  return QRectF(QPointF(minx,miny), QPointF(maxx,maxy));
}

void CmdCaligraph::render(Statement const &s, Figure &f, bool dryrun) {
  int id1 = s.nextIndex(1);
  int id2 = s.nextIndex(id1);
  QVector<double> const &xdata = s.data(1);
  QVector<double> const &ydata = s.data(id1);
  QVector<double> const &wdata = s.data(id2);
  if (xdata.isEmpty()) {
    f.setBBox(QRectF());
    return;
  }

  /* Each point on the line is replaced by three: two on the outer corner
     and one on the inner, except for the first and last points, which
     get replaced by only two each. */
  int N = xdata.size();
  int L = 3*N-2;
  int l1 = 0;
  int l2 = L;
  QPolygonF poly(L);

  QPointF pprev, pthis, pnext;
  QPointF dprev, dnext;
  double thetaprev = 0; // this value not used unless N=1
  double thetanext = 0; // this value not used unless N=1
  for (int k=0; k<N; k++) {
    if (k>0) 
      pprev = pthis;
    if (k>0)
      pthis = pnext;
    else 
      pthis = f.map(xdata[k],ydata[k]);
    if (k<N-1)
      pnext = f.map(xdata[k+1],ydata[k+1]);

    if (k>0) 
      dprev = dnext;
    if (k<N-1)
      dnext = pnext - pthis;

    if (k>0)
      thetaprev = thetanext;
    if (k<N-1)
      thetanext = atan2(dnext.y(), dnext.x());

    double w = pt2iu(wdata[k]/2);
    if (k==0) {
      QPointF ddnext = w * QPointF(-sin(thetanext), cos(thetanext));
      poly[l1++] = pthis+ddnext;
      poly[--l2] = pthis-ddnext;
    } else if (k==N-1) {
      QPointF ddprev = w * QPointF(-sin(thetaprev), cos(thetaprev));
      poly[l1++] = pthis+ddprev;
      poly[--l2] = pthis-ddprev;
    } else {
      QPointF ddprev = w * QPointF(-sin(thetaprev), cos(thetaprev));
      QPointF ddnext = w * QPointF(-sin(thetanext), cos(thetanext));
      if (dnext.y()*dprev.x() > dnext.x()*dprev.y()) {
	poly[l1++] = pthis+ddprev/2+ddnext/2;
	poly[--l2] = pthis-ddprev;
	poly[--l2] = pthis-ddnext;
      } else {
	poly[l1++] = pthis+ddprev;
	poly[l1++] = pthis+ddnext;
	poly[--l2] = pthis-ddprev/2-ddnext/2;
      }
    }
  }
  if (l1!=l2)
    qDebug() << "Caligraph: point miscount";

  QRectF bbox = poly.boundingRect();
  f.setBBox(bbox);

  if (dryrun)
    return;

  QPen pen = f.painter().pen();
  QBrush brush = f.painter().brush();
  f.painter().setPen(Qt::NoPen);
  f.painter().setBrush(pen.color());
  f.painter().drawPolygon(poly);
  f.painter().setPen(pen);
  f.painter().setBrush(brush);
}
