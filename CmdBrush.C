// CmdBrush.C

#include "CmdBrush.H"
#include <QDebug>

static CBuilder<CmdBrush> cbBrush("brush");

bool CmdBrush::usage() {
  return error("Usage: brush color|none|opacity ...");
}

bool CmdBrush::parse(Statement const &s) {
  if (s.length()<2)
    return usage();
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::CAPITAL) {
      continue; // OK, this is brush choice
    } else if (s[k].typ==Token::NUMBER) {
      continue; // OK, this is opacity
    } else if (s[k].typ==Token::BAREWORD) {
      QString w = s[k].str;
      if (w=="none")
	continue;
      else if (QColor(w).isValid())
	continue;
      else
	return usage();
    }
  }
  return true;
}

void CmdBrush::render(Statement const &s, Figure &f, bool) {
  QBrush b(f.painter().brush());
  QColor c(b.color());
  double alpha = c.alphaF();
  bool newColor = false;
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::CAPITAL) {
      f.painter().setBrush(b);
      f.chooseBrush(s[k].str);
      b = f.painter().brush();
    } else if (s[k].typ==Token::NUMBER) {
      alpha = s[k].num;
      if (alpha<0)
	alpha=0;
      else if (alpha>1)
	alpha=1;
      newColor = true;
    } else if (s[k].typ==Token::BAREWORD) {
      QString w = s[k].str;
      if (w=="none")
	b.setStyle(Qt::NoBrush);
      else if (QColor(w).isValid()) {
	c = w;
	newColor = true;
      } else
	qDebug() << "brush render surprise";
    }
  }
  if (newColor) {
    c.setAlphaF(alpha);
    b.setColor(c);
    b.setStyle(Qt::SolidPattern);
  }
  f.painter().setBrush(b);
}


