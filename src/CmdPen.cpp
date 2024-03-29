// CmdPen.cpp - This file is part of QPlot

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

// CmdPen.C

#include "CmdPen.h"
#include <QDebug>

#include "Error.h"

static CBuilder<CmdPen> cbPen("pen");

#define PEN_DEFAULTLENGTH 3

bool CmdPen::usage() {
  return error("Usage: pen [ID] - | color | width | -alpha | miterjoin|beveljoin|roundjoin | flatcap|squarecap|roundcap | solid|none | dash [L1 ...] | dot L ...");
}

static int joinstyle(QString s) {
  if (s=="miterjoin")
    return Qt::MiterJoin;
  else if (s=="beveljoin")
    return Qt::BevelJoin;
  else if (s=="roundjoin")
    return Qt::RoundJoin;
  else
    return -1;
}

static int capstyle(QString s) {
  if (s=="flatcap")
    return Qt::FlatCap;
  else if (s=="squarecap")
    return Qt::SquareCap;
  else if (s=="roundcap")
    return Qt::RoundCap;
  else
    return -1;
}

bool CmdPen::parse(Statement const &s) {
  if (s.length()<2)
    return usage();
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::CAPITAL && k==1) {
      continue; // OK, this is pen choice
    } else if (s[k].typ==Token::DASH) {
      continue; // OK, this resets pen
    } else if (s[k].typ==Token::NUMBER) {
      continue; // OK, this is width or alpha
    } else if (s[k].typ==Token::BAREWORD) {
      QString w = s[k].str;
      if (joinstyle(w)>=0)
	continue;
      else if (capstyle(w)>=0)
	continue;
      else if (w=="solid" || w=="none")
	continue;
      else if (w=="dash" || w=="dot") {
	if (k+1<s.length() && s.isNumeric(k+1)) {
	  k=s.nextIndex(k+1)-1;
	  if (k>0)
	    continue;
	  else
	    return usage(); // Bad vector is not OK
	} else {
	  continue; // OK if no vector follows
	}
      } else if (QColor(w).isValid())
	continue;
      else
	return usage();
    } else
      return usage();
  }
  return true;
}

void CmdPen::render(Statement const &s, Figure &f, bool) {
  QPen p(f.painter().pen());
  bool namedPen = false;
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::CAPITAL && k==1) {
      f.choosePen(s[k].str);
      p = f.painter().pen();
      namedPen = true;
    } else if (s[k].typ==Token::DASH) {
      // reset pen
      p = Figure::defaultPen();
    } else if (s[k].typ==Token::NUMBER) {
      if (s[k].num==0)
	p.setWidthF(pt2iu(f.hairline()));
      else if (s[k].num>0)
	p.setWidthF(pt2iu(s[k].num));
      else {
	QColor c = p.color();
	c.setAlphaF(-s[k].num);
	p.setColor(c);
      }
      if (p.style()==Qt::NoPen)
	p.setStyle(Qt::SolidLine);
    } else if (s[k].typ==Token::BAREWORD) {
      QString w = s[k].str;
      if (joinstyle(w)>=0)
	p.setJoinStyle(Qt::PenJoinStyle(joinstyle(w)));
      else if (capstyle(w)>=0)
	p.setCapStyle(Qt::PenCapStyle(capstyle(w)));
      else if (w=="none")
	p.setStyle(Qt::NoPen);
      else if (w=="solid")
	p.setStyle(Qt::SolidLine);
      else if (w=="dash") {
	double w = p.widthF();
	if (w==0)
	  w = f.dashScale()/f.painter().transform().m11();
	QVector<qreal> pat;
	bool flatcap = p.capStyle()==Qt::FlatCap;
	if (k+1<s.length() && s.isNumeric(k+1)) {
	  foreach (double x, s.data(k+1)) {
	    if (x==0) 
	      pat.push_back(flatcap ? 1 : .001);
	    else 
	      pat.push_back(pt2iu(x)/w);
	  }
	  k = s.nextIndex(k+1)-1;
	} else {
	  pat.push_back(pt2iu(PEN_DEFAULTLENGTH)/w);
	}
	int L = pat.size();
	if (L&1)
	  for (int l=0; l<L; l++)
	    pat.push_back(pat[l]);
	p.setDashPattern(pat);
      } else if (w=="dot") {
	double w = p.widthF();
	if (w==0)
	  w = f.dashScale()/f.painter().transform().m11();
	QVector<qreal> pat;
	bool flatcap = p.capStyle()==Qt::FlatCap;
	if (k+1<s.length() && s.isNumeric(k+1)) {
	  foreach (double x, s.data(k+1)) {
	    pat.push_back(flatcap ? 1 : 0.001);
	    pat.push_back(pt2iu(x)/w);
	  }
	  k = s.nextIndex(k+1)-1;
	} else {
	  pat.push_back(0.001);
	  pat.push_back(pt2iu(PEN_DEFAULTLENGTH)/w);
	}
	p.setDashPattern(pat);	
      } else if (QColor(w).isValid()) {
	p.setColor(w);
	if (p.style()==Qt::NoPen)
	  p.setStyle(Qt::SolidLine);
      } else {
	Error() << "pen render surprise";
      }
    }
  }
  f.painter().setPen(p);
  if (namedPen)
    f.storePen();
}


