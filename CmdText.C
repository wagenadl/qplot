// CmdText.C

#include "CmdText.H"
#include <QFontMetricsF>
#include "Rotate.H"
#include <QDebug>

static CBuilder<CmdText> cbText("text");

bool CmdText::usage() {
  return error("Usage: text dx dy string");
}

bool CmdText::parse(Statement const &s) {
  if (s.length()==4 && s[1].typ==Token::NUMBER &&
      s[2].typ==Token::NUMBER && s[3].typ==Token::STRING)
    return true;
  else
    return usage();
}

void CmdText::render(Statement const &s, Figure &f, bool dummy) {
  double dx = pt2iu(s[1].num);
  double dy = pt2iu(s[2].num);
  QString txt = s[3].str;

  QFontMetricsF fm(f.painter().font());
  QString ref = f.refText();
  QRectF r(fm.tightBoundingRect(txt));
  if (!ref.isEmpty()) {
    QRectF rr(fm.tightBoundingRect(ref));
    r.setTop(rr.top());
    r.setBottom(rr.bottom());
  }
  qDebug() << "Text bbox: " << r;
  
  switch (f.hAlign()) {
  case Figure::LEFT:
    dx -= r.left();
    break;
  case Figure::RIGHT:
    dx -= r.right();
    break;
  case Figure::CENTER:
    dx -= r.left()/2 + r.right()/2;
    break;
  }
  switch (f.vAlign()) {
  case Figure::TOP:
    dy -= r.top();
    break;
  case Figure::BOTTOM:
    dy -= r.bottom();
    break;
  case Figure::MIDDLE:
    dy -= r.top()/2 + r.bottom()/2;
    break;
  case Figure::BASE:
    break;
  }

  // work on bbox:
  r.translate(dx, dy);
  r = ::rotate(r, f.anchorAngle());
  r.translate(f.anchor());
  f.setBBox(r);
  
  if (dummy)
    return;

  f.painter().save();
  f.painter().translate(f.anchor());
  f.painter().rotate(f.anchorAngle() * 180 / 3.14159265);
  f.painter().drawText(QPointF(dx,dy), txt);
  f.painter().restore();
}
