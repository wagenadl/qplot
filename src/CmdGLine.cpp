// CmdGLine.cpp - This file is part of QPlot

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

// CmdGLine.C

#include "CmdGLine.h"
#include "Rotate.h"
#include <math.h>
#include <QDebug>

static CBuilder<CmdGLine> cbGLine("gline");
static CBuilder<CmdGLine> cbGArea("garea");

bool CmdGLine::usage(QString x) {
  if (x.isEmpty())
    return error("Usage: gline|garea ptspec ...");
  else
    return error("gline|garea: " + x);
}

enum GLineKW {
  KW_ERROR,
  KW_absdata,
  KW_abspaper,
  KW_reldata,
  KW_relpaper,
  KW_rotdata,
  KW_rotpaper,
  KW_retract,
  KW_at,
  KW_atx,
  KW_aty,
};

static GLineKW glineKW(QString s) {
  if (s=="absdata")
    return KW_absdata;
  else if (s=="abspaper")
    return KW_abspaper;
  else if (s=="reldata")
    return KW_reldata;
  else if (s=="relpaper")
    return KW_relpaper;
  else if (s=="rotdata")
    return KW_rotdata;
  else if (s=="rotpaper")
    return KW_rotpaper;
  else if (s=="retract")
    return KW_retract;
  else if (s=="at")
    return KW_at;
  else if (s=="atx")
    return KW_atx;
  else if (s=="ayt")
    return KW_aty;
  else  
    return KW_ERROR;
}

static QString got(Statement const &s, int k) {
  return " rather than '" + s[k].str + "' after " + QString::number(k);
}
  
bool CmdGLine::parse(Statement const &s) {
  int k=1;
  while (k<s.length()) {
    if (s[k].typ!=Token::OPENPAREN)
      return usage("expected '('" + got(s,k));
    k++;
    if (k>=s.length())
      usage();
    while (s[k].typ!=Token::CLOSEPAREN) {
      if (s[k].typ!=Token::BAREWORD)
        return usage("expected ')' or keyword" + got(s,k));
      GLineKW kw = glineKW(s[k].str);
      if (kw==KW_ERROR)
        return usage("unknown keyword: '" + s[k].str + "'");
      k++;
      if (k>=s.length())
        usage("missing 1st argument to '" + s[k].str + "'");
      switch (kw) { // checking first number
      case KW_absdata: case KW_abspaper:
        if (s[k].typ!=Token::NUMBER && s[k].typ!=Token::DASH)
	  return usage("expected number or dash after '" + s[k-1].str + "'");
        break;
      case KW_at: case KW_atx: case KW_aty:
	if (s[k].typ!=Token::CAPITAL)
	  return usage("expected ID after '" + s[k-1].str + "'");
	break;
      default:
        if (s[k].typ!=Token::NUMBER)
	  return usage("expected number");
        break;
      }
      k++;
      if (k>=s.length())
        return usage("missing 2nd argument to '" + s[k].str + "'");
      switch (kw) { // checking second number
      case KW_absdata: case KW_abspaper:
        if (s[k].typ!=Token::NUMBER && s[k].typ!=Token::DASH)
	  return usage("expected number or dash after '" + s[k-2].str + "'");
        break;
      case KW_retract:
        if (s[k].typ==Token::CLOSEPAREN)
	  --k; // no second number
        else if (s[k].typ!=Token::NUMBER)
	  return usage("expected ')' or number after 'retract'");
        break;
      case KW_rotpaper: case KW_at: case KW_atx: case KW_aty:
	--k; // no second number
	break;
      default:
        if (s[k].typ!=Token::NUMBER)
	  return usage("expected number after '" + s[k-2].str + "'");
        break;
      }
      k++;
      if (k>=s.length())
        return usage("unexpected end of line");
    }
    k++;
  }

  return true;
}

QRectF CmdGLine::dataRange(Statement const &s) {
  QPolygonF pts;
  int k=1;
  while (k<s.length()) {
    // build a new point
    k++; // we already know we have parentheses
    while (s[k].typ!=Token::CLOSEPAREN) {
      GLineKW kw = glineKW(s[k].str); // we already know keyword is valid
      switch (kw) {
      case KW_absdata:
        if (s[k+1].typ==Token::NUMBER && s[k+2].typ==Token::NUMBER)
          pts << QPointF(s[k+1].num, s[k+2].num);
        break;
      case KW_rotpaper:
        --k; // only one number
        break;
      case KW_at:
	--k;
	break;
      case KW_atx:
	--k;
	break;
      case KW_aty:
	--k;
	break;
      case KW_retract:
        if (s[k+2].typ!=Token::NUMBER) 
	  --k; // only one number
	break;
      }
      k+=3; // skip keyword and both numbers
    }
    k++; // skip close paren
  }
  if (pts.size())
    return pts.boundingRect();
  else
    return QRectF();
}
  

void CmdGLine::render(Statement const &s, Figure &f, bool dryrun) {
  QPolygonF pts;
  QVector<double> retractL;
  QVector<double> retractR;

  int k=1;
  while (k<s.length()) {
    // build a new point
    QPointF p(0,0);
    double phi=0;
    double rL=0, rR=0;
    
    k++; // we already know we have parentheses

    while (s[k].typ!=Token::CLOSEPAREN) {
      GLineKW kw = glineKW(s[k].str); // we already know keyword is valid
      QPointF p1(0, 0); // start at abspaper (0,0)
      switch (kw) {
      case KW_absdata:
        p1 = f.map(s[k+1].typ==Token::NUMBER ? s[k+1].num : f.xAxis().min(),
		   s[k+2].typ==Token::NUMBER ? s[k+2].num : f.yAxis().min());
        if (s[k+1].typ==Token::NUMBER)
	  p.setX(p1.x());
        if (s[k+2].typ==Token::NUMBER)
	  p.setY(p1.y());
        break;
      case KW_abspaper:
        if (s[k+1].typ==Token::NUMBER)
	  p.setX(pt2iu(s[k+1].num));
        if (s[k+2].typ==Token::NUMBER)
	  p.setY(pt2iu(s[k+2].num));
        break;
      case KW_reldata:
        p1 = f.maprel(s[k+1].num, s[k+2].num);
        p.setX(p.x()+p1.x());
        p.setY(p.y()+p1.y());
        break;
      case KW_relpaper:
        p.setX(p.x()+pt2iu(s[k+1].num)*cos(phi) - pt2iu(s[k+2].num)*sin(phi));
        p.setY(p.y()+pt2iu(s[k+1].num)*sin(phi) + pt2iu(s[k+2].num)*cos(phi));
        break;
      case KW_rotdata:
        p1 = f.maprel(s[k+1].num, s[k+2].num);
        phi = atan2(p1.y(), p1.x());
        break;
      case KW_rotpaper:
        phi = s[k+1].num;
        --k; // only one number
        break;
      case KW_at:
	p = f.getLocation(s[k+1].str);
	--k;
	break;
      case KW_atx:
	p.setX(f.getLocation(s[k+1].str).x());
	--k;
	break;
      case KW_aty:
	p.setY(f.getLocation(s[k+1].str).y());
	--k;
	break;
      case KW_retract:
        rL = pt2iu(s[k+1].num);
        if (s[k+2].typ==Token::NUMBER) {
	  rR = pt2iu(s[k+2].num);
        } else {
	  rR = rL;
	  --k; // only one number
        }
	break;
      case KW_ERROR: // cannot happen
        break;
      }
      k+=3; // skip keyword and both numbers
    }
    k++; // skip close paren
    pts.push_back(p);
    retractL.push_back(rL);
    retractR.push_back(rR);
  }

  QList<QPolygonF> ppp;
  QPolygonF pcurrent;
  int N = pts.size();
  for (int n=0; n<N; n++) {
    QPointF p = pts[n];
    if (n>0 && (retractL[n]!=0 || retractR[n]!=0)) {
      // break after this segment
      QPointF dp = p-pts[n-1];
      double phi = atan2(dp.y(), dp.x());
      pcurrent << p - QPointF(cos(phi)*retractL[n], sin(phi)*retractL[n]);
      ppp << pcurrent;
      pcurrent = QPolygonF();
    }
    if (n<N-1 && retractR[n]!=0) {
      QPointF dp = p-pts[n+1];
      double phi = atan2(dp.y(), dp.x());
      p -= QPointF(cos(phi)*retractR[n], sin(phi)*retractR[n]);
    }
    pcurrent << p;
  }
  if (pcurrent.size()>1)
    ppp << pcurrent;


  QRectF bbox;
  foreach (QPolygonF const &p, ppp) {
    if (bbox.isNull())
      bbox = p.boundingRect();
    else
      bbox |= p.boundingRect();
  }

  double w = f.painter().pen().widthF();


  if (w>0)
    bbox.adjust(-w/2, -w/2, w/2, w/2);

  f.setBBox(bbox); // Now GLines do affect shrink. Why would that be bad?
  // QRectF()); // GLines do *not* affect fudge

  if (dryrun)
    return;

  foreach (QPolygonF const &p, ppp) {
    if (s[0].str=="garea")
      f.painter().drawPolygon(p);
    else
      f.painter().drawPolyline(p);
  }

}
