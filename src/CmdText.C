// CmdText.C

#include "CmdText.H"
#include <QFontMetricsF>
#include "Rotate.H"
#include <QDebug>
#include "Text.H"

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

  Text t;
  t.setFont(f.painter().font());
  t.addInterpreted(txt);

  QRectF r0 = t.bbox();
  QRectF r = r0;

  QString ref = f.refText();
  if (!ref.isEmpty()) {
    Text tref;
    tref.setFont(f.painter().font());
    tref.addInterpreted(ref);
    QRectF rr = tref.bbox();
    r.setTop(rr.top());
    r.setBottom(rr.bottom());
  }
  
  switch (f.hAlign()) {
  case Align::LEFT:
    dx -= r.left();
    break;
  case Align::RIGHT:
    dx -= r.right();
    break;
  case Align::CENTER:
    dx -= r.left()/2 + r.right()/2;
    break;
  }
  switch (f.vAlign()) {
  case Align::TOP:
    dy -= r.top();
    break;
  case Align::BOTTOM:
    dy -= r.bottom();
    break;
  case Align::MIDDLE:
    dy -= r.top()/2 + r.bottom()/2;
    break;
  case Align::BASE:
    break;
  }

  // work on bbox: (actual, not ref)
  r = ::rotate(r0.translated(dx, dy), f.anchorAngle());
  r.translate(f.anchor());
  f.setBBox(r);
  
  if (dummy)
    return;

  f.painter().save();
  f.painter().translate(f.anchor());
  f.painter().rotate(f.anchorAngle() * 180 / 3.14159265);
  t.render(f.painter(), QPointF(dx, dy));
  f.painter().restore();
}
