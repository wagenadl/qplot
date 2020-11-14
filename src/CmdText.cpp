// CmdText.cpp - This file is part of QPlot

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

// CmdText.C

#include "CmdText.h"
#include <QFontMetricsF>
#include "Rotate.h"
#include <QDebug>
#include "Text.h"

static CBuilder<CmdText> cbText("text");
static CBuilder<CmdText> cbCText("ctext");

bool CmdText::usage() {
  return error("Usage: text [dx dy] string");
}

bool CmdText::parse(Statement const &s) {
  if (s.length()==4 && s[1].typ==Token::NUMBER &&
      s[2].typ==Token::NUMBER && s[3].typ==Token::STRING)
    return true;
  else if (s.length()==2 && s[1].typ==Token::STRING)
    return true;
  else
    return usage();
}

void CmdText::render(Statement const &s, Figure &f, bool dummy) {
  double dx;
  double dy;
  QString txt;
  bool shortform;
  if (s.length()==2) {
    dx = 0;
    dy = 0;
    txt = s[1].str;
    shortform = f.textShiftAccum().isActive();
  } else {
    dx = pt2iu(s[1].num);
    dy = pt2iu(s[2].num);
    txt = s[3].str;
    shortform = s[0].str=="ctext" && f.textShiftAccum().isActive();
  }

  Text t;
  t.setFont(f.painter().font());
  t.addInterpreted(txt);

  QRectF r0 = t.bbox();
  QRectF r = r0;

  if (shortform) {
    dx += f.textShiftAccum().x();
    dy += f.textShiftAccum().y();
  } else {
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
  }
  
  // work on bbox: (actual, not ref)
  r = ::rotate(r0.translated(dx, dy), f.anchorAngle());
  r.translate(f.anchor());
  f.setBBox(r);
  f.textShiftAccum().setBase(dx+t.width(), dy);

  if (dummy)
    return;

  f.painter().save();
  f.painter().translate(f.anchor());
  f.painter().rotate(f.anchorAngle() * 180 / 3.14159265);
  t.render(f.painter(), QPointF(dx, dy));
  f.painter().restore();

}
