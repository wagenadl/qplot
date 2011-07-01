// Text.C

#include "Text.H"
#include <QRegExp>
#include "Factor.H"
#include <QFontMetricsF>
#include <QPainter>

Text::Text() {
  clear();
}

Text::~Text() {
}

void Text::addInterpreted(QString txt) {
  txt.replace("~", " ");
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
      int id1 = txt.indexOf(QRegExp("\\s"),idx+1);
      if (id1<0)
	id1 = txt.size();
      add(bld);
      bld="";
      setSub();
      addInterpreted(txt.mid(idx+1,id1-idx-1));
      restore();
      idx=id1;
    } else if (x=="^") {
      int id1 = txt.indexOf(QRegExp("\\s"),idx+1);
      if (id1<0)
	id1 = txt.size();
      add(bld);
      bld="";
      setSuper();
      addInterpreted(txt.mid(idx+1,id1-idx-1));
      restore();
      idx=id1;
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
  return f;
}

Text &Text::operator<<(QString const &txt) {
  add(txt);
  return *this;
}

void Text::add(QString const &txt) {
  if (txt.isEmpty())
    return;
  State s(stack.last());
  Span span;
  span.startpos = QPointF(nextx, s.baseline);
  span.font = makeFont(s);
  span.text = txt;
  spans.push_back(span);
  QFontMetricsF fm(span.font);
  QRectF r = fm.tightBoundingRect(txt);
  bb |= r.translated(span.startpos);
  nextx += fm.width(txt);
}

QRectF Text::bbox() const {
  return bb;
}

void Text::render(QPainter &p, QPointF const &xy0) {
  foreach (Span const &s, spans) {
    p.setFont(s.font);
    p.drawText(xy0+s.startpos, s.text);
  }
}
