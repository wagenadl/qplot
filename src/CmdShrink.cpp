// CmdShrink.cpp - This file is part of QPlot

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

// CmdShrink.C

#include "CmdShrink.h"
#include <QDebug>
#include <math.h>
#include "Error.h"

static CBuilder<CmdShrink> cbShrink("shrink");

#define SHRINK_DEFAULT 0.2

bool CmdShrink::usage() {
  return error("Usage: shrink [margin_pt] [ratio]\n");
}

bool CmdShrink::parse(Statement const &s) {
  if (s.length()==1)
    return true;
  else if (s.length()==2 && s[1].typ==Token::NUMBER)
    return true;
  else if (s.length()==3 && (s[1].typ==Token::NUMBER || s[1].typ==Token::DASH)
	   && (s[2].typ==Token::NUMBER))
    return true;
  else
    return usage();
}

void CmdShrink::render(Statement const &s, Figure &f, bool) {
  double mrg = pt2iu(SHRINK_DEFAULT);
  if (s.length()>=2 && s[1].typ==Token::NUMBER)
    mrg = pt2iu(s[1].num);
  bool hasRatio = s.length()>=3;
  double ratio = hasRatio ? s[2].num : 1;
  QRectF actual = f.fullBBox();
  QRectF desired = f.extent();

  double dleft = actual.left() - desired.left(); // +ve means it's OK
  double dright = desired.right() - actual.right();
  double dtop =  actual.top() - desired.top();
  double dbottom = desired.bottom() - actual.bottom();

  QPointF x0 = f.xAxis().minp();
  QPointF x1 = f.xAxis().maxp();
  QPointF y0 = f.yAxis().minp();
  QPointF y1 = f.yAxis().maxp();

  double olddx = x1.x()-x0.x();
  double olddy = y1.y()-y0.y();
  
  if (dleft<mrg)
    x0 += QPointF(2*mrg-dleft, 0);
  if (dright<mrg)
    x1 -= QPointF(2*mrg-dright, 0);
  if (dtop<mrg)
    y1 += QPointF(0, 2*mrg-dtop);
  if (dbottom<mrg)
    y0 -= QPointF(0, 2*mrg-dbottom);

  double newdx = x1.x()-x0.x();
  double newdy = y1.y()-y0.y();

  if (newdx*olddx<0 || newdy*olddy<0) {
    f.markFudged();
    //    qDebug() << "Shrink at " << s.label() << " did work";
    return;
  }

  if (hasRatio) {
    double dpx = fabs(x1.x() - x0.x());
    double dpy = fabs(y1.y() - y0.y());
    double xrat = fabs(dpx / (f.xAxis().max() - f.xAxis().min()));
    double yrat = fabs(dpy / (f.yAxis().max() - f.yAxis().min()));
    double myrat = yrat/xrat;
    if (myrat>ratio) {
      // I am too tall
      y1 += QPointF(0, .5*dpy*(1-ratio/myrat));
      y0 -= QPointF(0, .5*dpy*(1-ratio/myrat));
    } else if (myrat<ratio) {
      // I am too wide
      x1 -= QPointF(.5*dpx*(1-myrat/ratio), 0);
      x0 += QPointF(.5*dpx*(1-myrat/ratio), 0);
    }
  }      

  if ((x0 - f.xAxis().minp()).manhattanLength()>mrg ||
      (x1 - f.xAxis().maxp()).manhattanLength()>mrg ||
      (y0 - f.yAxis().minp()).manhattanLength()>mrg ||
      (y1 - f.yAxis().maxp()).manhattanLength()>mrg) {
    f.xAxis().setPlacement(x0, x1);
    f.yAxis().setPlacement(y0, y1);
    f.markFudged();
    //qDebug() << "Shrink at " << s.label() << " did work";
  }
}

