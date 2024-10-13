// CmdAt.cpp - This file is part of QPlot

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

// CmdAt.C

#include "CmdAt.h"
#include <QDebug>
#include "Slightly.h"

static CBuilder<CmdAt> cbAt("at");

bool CmdAt::usage() {
  return error("Usage: at x y (dx dy)|phi | - | x y ID | ID ... (phi)");
}

static bool isAbs(QString s) {
  if (s=="abs")
    return true;
  else if (s=="absolute")
    return true;
  else
    return false;
}

static int horiAlign(QString s) {
  // These numbers are actually meaningfully used in calc, not just an enum. 
  if (s=="left")
    return 0;
  else if (s=="center")
    return 1;
  else if (s=="right")
    return 2;
  else
    return -1;
}

static int vertAlign(QString s) {
  if (s=="top")
    return 0;
  else if (s=="middle")
    return 1;
  else if (s=="bottom")
    return 2;
  else
    return -1;
}
  

bool CmdAt::parse(Statement const &s) {
  if (s.length()<2)
    return usage();
  if (s[1].typ==Token::CAPITAL) {
    int i1 = 2;
    while (i1<s.length() && s[i1].typ==Token::CAPITAL)
      i1++;
    int di = s.length() - i1;
    if (di==0)
      return true; // at ID ...
    if (di==1)
      return s[i1].typ==Token::NUMBER ? true : usage(); // at ID ... phi 
    if (di==2)
      return (s[i1].typ==Token::NUMBER && s[i1+1].typ==Token::NUMBER)
	? true : usage(); // at ID ... dx dy
    return usage();
  }
  if (s.length()==2)
    return s[1].typ==Token::DASH ? true : usage(); // at -

  bool horiok =
    s[1].typ==Token::NUMBER
    || s[1].typ==Token::DASH
    || (s[1].typ==Token::BAREWORD && (horiAlign(s[1].str)>=0
                                      || isAbs(s[1].str)));
  if (!horiok)
    return usage();

  bool vertok = 
    s[2].typ==Token::NUMBER
    || s[2].typ==Token::DASH
    ||(s[2].typ==Token::BAREWORD && (vertAlign(s[2].str)>=0
                                     || isAbs(s[2].str)));
  if (!vertok)
    return usage();

  if (s.length()==3)
    return true; // at x y

  if (s[3].typ==Token::CAPITAL && s.length()==4)
    return true; // at x y ID

  if (s[3].typ!=Token::NUMBER)
    return usage();

  if (s.length()==4)
    return true; // at x y phi

  if (s[4].typ!=Token::NUMBER)
    return usage();

  return s.length()==5 ? true : usage(); // at x y dx dy
}

    

QRectF CmdAt::dataRange(Statement const &s) {
  // at x y => bbox around (x,y), else empty
  if (s.length()<3)
    return QRectF();
  
  if (s[1].typ==Token::NUMBER && s[2].typ==Token::NUMBER) {
    double x = s[1].num;
    double y = s[2].num;
    return QRectF(QPointF(Slightly::less(x),Slightly::less(y)),
		  QPointF(Slightly::more(x),Slightly::more(y)));
  } else {
    return QRectF();
  }
}
  
void CmdAt::render(Statement const &s, Figure &f, bool dryrun) {
  if (s[1].typ==Token::CAPITAL) { // at ID ...
    int i1 = 2;
    while (i1<s.length() && s[i1].typ==Token::CAPITAL) 
      i1++;
    QPointF p(0,0);
    for (int i=1; i<i1; i++)
      p += f.getLocation(s[i].str);
    p /= (i1 - 1);
    int di = s.length() - i1;
    if (di==0)
      f.setAnchor(p);
    else if (di==1)
      f.setAnchor(p, s[i1].num);
    else if (di==2)
      f.setAnchor(p, f.angle(s[i1].num, s[i1+1].num));
    // other options excluded by parse()
    return; 
  }

  if (s.length()<=2) { // at -
    f.setAnchor(f.extent().topLeft());
    return;
  }

  QPointF oldAnc = f.anchor();
  
  double x = s[1].typ==Token::NUMBER ? s[1].num : f.xAxis().min(); 
  double y = s[2].typ==Token::NUMBER ? s[2].num : f.yAxis().min(); 
  QPointF anchor = f.map(x,y);

  if (s[1].typ==Token::BAREWORD) {
    // that means x is as yet undefined. no matter:
    if (isAbs(s[1].str)) {
      anchor.setX(f.extent().left());
    } else {
      int a = horiAlign(s[1].str);
      anchor.setX(f.lastBBox().left()
		  + a*f.lastBBox().width()/2);
    }
  } else if (s[1].typ==Token::DASH) {
    anchor.setX(oldAnc.x());
  }
  
  if (s[2].typ==Token::BAREWORD) {
    // that means y is as yet undefined. no matter:
    if (isAbs(s[2].str)) {
      anchor.setY(f.extent().top());
    } else {
      int a = vertAlign(s[2].str);
      anchor.setY(f.lastBBox().top()
		  + a*f.lastBBox().height()/2);
    }
  } else if (s[2].typ==Token::DASH) {
    anchor.setY(oldAnc.y());
  }

  switch (s.length()) {
  case 3: 
    f.setAnchor(anchor); // at x y
    break;
  case 4:
    if (s[3].typ==Token::CAPITAL)
      f.setLocation(s[3].str, anchor); // at x y ID
    else
      f.setAnchor(anchor, s[3].num); // at x y phi
    break;
  case 5:
    f.setAnchor(anchor, f.angle(s[3].num,s[4].num)); // at x y dx dy
    break;
  default:
    qDebug() << "Unexpected syntax in AT";
  }

  if (dryrun)
    return;
  if (!f.areBoundingBoxesShown())
    return;
  f.painter().save();
  f.painter().setPen(QPen(QColor(255, 0, 0), 10));
  f.painter().setBrush(Qt::NoBrush);
  f.painter().drawEllipse(anchor, 30, 30);
  f.painter().restore();
}
