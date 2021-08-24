// CmdBrush.cpp - This file is part of QPlot

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

// CmdBrush.C

#include "CmdBrush.H"
#include <QDebug>

static CBuilder<CmdBrush> cbBrush("brush");

bool CmdBrush::usage() {
  return error("Usage: brush [ID] color|none|opacity ...");
}

bool CmdBrush::parse(Statement const &s) {
  if (s.length()<2)
    return usage();
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::CAPITAL && k==1) {
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
    } else
      return usage();
  }
  return true;
}

void CmdBrush::render(Statement const &s, Figure &f, bool) {
  QBrush b(f.painter().brush());
  QColor c(b.color());
  double alpha = c.alphaF();
  bool newColor = false;
  bool namedBrush = false;
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::CAPITAL && k==1) {
      // f.painter().setBrush(b);
      f.chooseBrush(s[k].str);
      b = f.painter().brush();
      c = b.color();
      alpha = c.alphaF();
      namedBrush = true;
    } else if (s[k].typ==Token::NUMBER) {
      alpha = s[k].num;
      if (alpha<0)
	alpha=0;
      else if (alpha>1)
	alpha=1;
      newColor = true;
    } else if (s[k].typ==Token::BAREWORD) {
      QString w = s[k].str;
      if (w=="none") {
	b.setColor("black");
	b.setStyle(Qt::NoBrush);
      } else if (QColor(w).isValid()) {
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
  if (namedBrush)
    f.storeBrush();
}


