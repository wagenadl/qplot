// Text.cpp - This file is part of QPlot

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

// Text.C

#include "Text.H"
#include <QRegExp>
#include "Factor.H"
#include <QFontMetricsF>
#include <QPainter>
#include <QDebug>

Text::Text() {
  clear();
}

Text::~Text() {
}

void Text::addInterpreted(QString txt) {
  int i=-1;
  while ((i=txt.indexOf('-', i+1), i>=0)) {
    if (i==0 || !txt[i-1].isLetter()) {
      txt.replace(i, 1, QChar(0x2212));
    }
  }

  QString bld;
  QRegExp word("\\w+");
  int idx=0;
  while (idx<txt.size()) {
    QString x = txt.mid(idx,1);
    if (x=="*") {
      int id1 = txt.indexOf("*",idx+1);
      if (id1>=0 && word.exactMatch(txt.mid(idx+1,id1-idx-1))) {
	add(bld);
	bld="";
	toggleBold();
	add(txt.mid(idx+1,id1-idx-1));
	restore();
	idx=id1;
      } else {
	bld+="*";
      }
    } else if (x=="/") {
      int id1 = txt.indexOf("/",idx+1);
      if (id1>=0 && word.exactMatch(txt.mid(idx+1,id1-idx-1))) {
	add(bld);
	bld="";
	toggleSlant();
	add(txt.mid(idx+1,id1-idx-1));
	restore();
	idx=id1;
      } else {
	bld+="/";
      }
    } else if (x=="_") {
      int id1 = txt.indexOf(QRegExp("[ \t\n\r]"),idx+1);
      if (id1<0)
	id1 = txt.size();
      add(bld);
      bld="";
      setSub();
      addInterpreted(txt.mid(idx+1,id1-idx-1));
      restore();
      idx=id1;
    } else if (x=="^") {
      int id1 = txt.indexOf(QRegExp("[ \t\n\r]"),idx+1);
      if (id1<0)
	id1 = txt.size();
      add(bld);
      bld="";
      setSuper();
      addInterpreted(txt.mid(idx+1,id1-idx-1));
      restore();
      idx=id1;
    } else if (x=="\\") {
      if (txt.mid(idx+1,1)=="!") {
	add(bld);
	add("\\!");
	bld="";
	idx++;
      } else if (txt.mid(idx+1,1)==",") {
	add(bld);
	add("\\,");
	bld="";
	idx++;
      } else {
	bld += x;
      }
    } else {
      bld+=x;
    }
    idx++;
  }
  add(bld);
}

void Text::clear() {
  spans.clear();
  nextx = 0;
  bb = QRectF();
  stack.clear();
  State s;
  s.fontfamily = "Helvetica";
  s.fontsize = pt2iu(10);
  s.baseline = 0;
  s.slant = false;
  s.bold = false;
  stack.push_back(s);
}

void Text::setFont(QFont const &f) {
  State s = stack.last();
  s.fontfamily = f.family();
  s.fontsize = f.pixelSize();
  s.slant = f.italic();
  s.bold = f.bold();
  stack.push_back(s);
}

void Text::setFont(QString family, double size) {
  State s = stack.last();
  s.fontfamily = family;
  s.fontsize = size;
  stack.push_back(s);
}

void Text::toggleSlant() {
  State s = stack.last();
  s.slant = !s.slant;
  stack.push_back(s);
}

void Text::toggleBold() {
  State s = stack.last();
  s.bold = !s.bold;
  stack.push_back(s);
}

void Text::restore() {
  if (stack.size()>=2)
    stack.pop_back();
  // else error?
}

#define SCRIPTSIZE 0.75
#define SCRIPTSHIFT 0.75

void Text::setSuper() {
  State s = stack.last();
  QRectF rbase = QFontMetricsF(makeFont(s)).tightBoundingRect("x");
  s.fontsize *= SCRIPTSIZE;
  QRectF rscript = QFontMetricsF(makeFont(s)).tightBoundingRect("0");
  s.baseline += rbase.top() - (1-SCRIPTSHIFT)*rscript.top();
  stack.push_back(s);
}

void Text::setSub() {
  State s = stack.last();
  s.fontsize *= SCRIPTSIZE;
  QRectF rscript = QFontMetricsF(makeFont(s)).tightBoundingRect("0");
  s.baseline -= SCRIPTSHIFT*rscript.top();
  stack.push_back(s);
}

QFont Text::makeFont(Text::State const &s) {
  QFont f;
  f.setFamily(s.fontfamily);
  f.setPixelSize(s.fontsize);
  f.setBold(s.bold);
  f.setItalic(s.slant);
  f.setKerning(true);
  return f;
}

Text &Text::operator<<(QString const &txt) {
  add(txt);
  return *this;
}

void Text::add(QString txt) {
  txt.replace("~", " ");
  txt.replace(QRegExp("  +")," ");
  if (txt.isEmpty())
    return;
  State s(stack.last());
  Span span;
  span.startpos = QPointF(nextx, s.baseline);
  span.font = makeFont(s);
  if (txt == "\\!") {
    span.text = "";
    QFontMetricsF fm(span.font);
    QRectF r = fm.tightBoundingRect("x");
    nextx -= r.width()/5;
  } else if (txt == "\\,") {
    span.text = "";
    QFontMetricsF fm(span.font);
    QRectF r = fm.tightBoundingRect("x");
    nextx += r.width()/5;
  } else {
    span.text = txt;
  }
  spans.push_back(span);
  if (span.text != "") {
    QFontMetricsF fm(span.font);
    QRectF r = fm.tightBoundingRect(txt);
    bb |= r.translated(span.startpos);
    nextx += fm.width(txt);
  }
}

QRectF Text::bbox() const {
  QRectF b(bb);
  b.setRight(nextx);
  return b;
}

double Text::width() const {
  return nextx;
}

void Text::render(QPainter &p, QPointF const &xy0) {
  foreach (Span const &s, spans) {
    p.setFont(s.font);
    QString txt = s.text;
    p.drawText(xy0+s.startpos, txt);
  }
}
