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

#include "Text.h"
#include <QRegularExpression>
#include "Factor.h"
#include <QFontMetricsF>
#include <QPainter>
#include <QDebug>

Text::Text() {
  clear();
}

Text::~Text() {
}

bool allWord(QString txt) {
  int L = txt.size();
  if (L==0)
    return false;
  for (int k=0; k<L; k++)
    if (!txt[k].isLetterOrNumber())
      return false;
  return true;
}

static int nextUnprotected(QString const &s, int idx) {
  /* Returns the index of the next unprotected space in the string S,
     starting the search from position IDX.
     If none found, returns the length of the string.
     Spaces are considered protected if they occur inside matching parens
     (such as (), [], {}, or ⟨⟩), or matching quotes («», ‘’, or “”).
     Unpaired parens or quotes do not protect. For instance, the string
     "a{(b, c) d" breaks before "d", because the "{" is not paired,
     as does "a{(b, c} d)" because the {} protect the space before "c".
     Unpaired closing parens cause a break before.
     Backslashes cause an otherwise pairable character to be ignored. Thus,
     "a\{b, c}" breaks before "c", as does "a\{(b, c} d)", (because the "}"
     mismatches the "("), while "a\{(b, c\} d)" doesn't break.
   */
  QString pairs = "()[]{}〈〉⟨⟩«»⟪⟫⟦⟧‘’“”⌊⌋⌈⌉";
  QList<int> starts;
  QSet<int> matchedstart;
  QSet<int> matchedend;
  int L = s.length();

  // first iteration, find matching pairs
  bool backslash = false;
  for (int i=idx; i<L; i++) {
    if (s[i]=='\\') {
      backslash = !backslash;
    } else if (backslash) {
      backslash = false;
      continue;
    }
    int what = pairs.indexOf(s[i]);
    if (what<0) 
      continue;
    if ((what&1)==0) {
      starts << i;
    } else {
      for (int k=starts.size()-1; k>=0; --k) {
        int start = starts[k];
        if (pairs[what & ~1]==s[start]) {
          matchedstart << start;
          matchedend << i;
          while (starts.size()>k)
            starts.takeLast();
          break;
        }
      }
    }
  }
  // second iteration, find unprotected stuff
  QString space = " \t\n\r_^";
  int prot = 0;
  backslash = false;
  for (int i=idx; i<L; i++) {
    if (s[i]=='\\')
      backslash = !backslash;
    if (matchedstart.contains(i)) {
      prot ++;
    } else if (matchedend.contains(i)) {
      prot --;
      if (prot==0)
        return i+1;
    } else if (prot==0) {
      if (space.contains(s[i]))
        return i;
      if (!backslash) {
        int what = pairs.indexOf(s[i]);
        if (what>0 && (what & 1))
          return i;
      }
    }
  }
  return L;
}

void Text::addInterpreted(QString txt) {
  int i=-1;
  while ((i=txt.indexOf('-', i+1), i>=0)) {
    if (i==0 || !txt[i-1].isLetter()) {
      txt.replace(i, 1, QChar(0x2212));
    }
  }
  static QString sups = "²³¹⁰ⁱ⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ";
  static QString supr = "2310i456789+−=()n";
  static QString subs = "ᵢᵣᵤᵥᵦᵧᵨᵩᵪ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₔₕₖₗₘₙₚₛₜⱼ";
  static QString subr = "iruvβγρφχ0123456789+-=()aeoxəhklmnpstj";
  QString bld;
  int idx=0;
  while (idx<txt.size()) {
    QString x = txt.mid(idx,1);
    if (x=="*" || x=="/") {
      int id1 = txt.indexOf(x, idx+1);
      if (id1>=0 && allWord(txt.mid(idx+1, id1-idx-1))) {
	add(bld);
	bld="";
        if (x=="*") {
          toggleBold();
        } else {
          italicCorrect();
          toggleSlant();
        }          
	add(txt.mid(idx+1, id1-idx-1));
        if (x=="/")
          italicCorrect();
	restore();
	idx=id1;
      } else {
	bld += x;
      }
    } else if (x=="_" || x=="^") {
      int id1 = nextUnprotected(txt, idx+1);
      add(bld);
      bld="";
      if (x=="^")
        setSuper();
      else
        setSub();
      QString scrpt = txt.mid(idx+1, id1-idx-1);
      if (scrpt.startsWith("{") && scrpt.endsWith("}"))
        scrpt = scrpt.mid(1, scrpt.size()-2);
      addInterpreted(scrpt);
      restore();
      idx=id1 - 1; // do not eat the unprotected thing
      if (idx+1<txt.size()) {
        QString cls = txt.mid(idx+1,1);
        if ((cls=="_" || cls=="^") && cls!=x) {
          add("\\!");
          add("\\!");
        }
      }
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
	bld += txt.mid(idx+1,1);
        idx++;
      }
    } else if (sups.contains(x)) {
      add(bld);
      bld="";
      setSuper();
      add(supr.mid(sups.indexOf(x), 1));
      restore();
    } else if (subs.contains(x)) {
      add(bld);
      bld="";
      setSub();
      add(subr.mid(subs.indexOf(x), 1));
      restore();
    } else {
      bld += x;
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
  QRectF rscript = QFontMetricsF(makeFont(s)).tightBoundingRect("x");
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

static QString doublespace(QString s) {
  if (s.endsWith(" "))
    return s + " "; // weirdly one space is cut from bbox calc in qt5
  return s;
}

void Text::add(QString txt) {
  QString t0 = txt;
  //  txt.replace(QRegExp("  +")," ");
  txt.replace("~", " ");
  if (txt.isEmpty())
    return;
  /* In Qt5, ZWNJ and ZWSP result in incorrect measurements. I am therefore
     forced to get rid of their use. That doesn't make me happy, because
     I know there was a reason why I put them in. I just cannot remember.
     3/21/23: Probably for italics correction
  */
  //txt = QString(QChar(0x200b)) + txt + QString(QChar(0x200b));
  //txt = QString(QChar(0x200c)) + txt + QString(QChar(0x200c));
  State s(stack.last());
  Span span;
  span.startpos = QPointF(nextx, s.baseline);
  span.font = makeFont(s);
  if (t0 == "\\!") {
    span.text = "";
    QFontMetricsF fm(span.font);
    nextx -= fm.horizontalAdvance("x")/5;
  } else if (t0 == "\\,") {
    span.text = "";
    QFontMetricsF fm(span.font);
    nextx += fm.horizontalAdvance("x")/5;
  } else {
    span.text = txt;
  }
  spans.push_back(span);
  if (span.text != "") {
    QFontMetricsF fm(span.font);
    // QTextOption opt; opt.setFlags(QTextOption::IncludeTrailingSpaces);
    QRectF r = fm.tightBoundingRect(doublespace(span.text)); //, opt);
    bb |= r.translated(span.startpos);
    nextx += fm.horizontalAdvance(span.text);
  }
}

QRectF Text::bbox() const {
  return bb;
}

double Text::width() const {
  return nextx;
}

void Text::render(QPainter &p, QPointF const &xy0) {
  foreach (Span const &s, spans) {
    p.setFont(s.font);
    QString txt = s.text;
    //    qDebug() << "render" << txt << txt.size() << xy0 << s.startpos << p.boundingRect(QRectF(0,0,0,0), Qt::AlignLeft| Qt::AlignBottom, txt);
    p.drawText(xy0+s.startpos, txt);
  }
}

void Text::italicCorrect() {
  if (stack.last().slant && spans.size()) {
    Span const &sp = spans.last();
    if (sp.text.size()) {
      QFontMetricsF fm(makeFont(stack.last()));
      qreal dx = fm.rightBearing(sp.text[sp.text.size()-1]);
      if (dx<0)
        nextx -= dx;
    }
  }
}
