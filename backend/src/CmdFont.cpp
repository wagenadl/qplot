// CmdFont.cpp - This file is part of QPlot

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

// CmdFont.C

#include "CmdFont.h"


static CBuilder<CmdFont> cbFont("font");

bool CmdFont::usage() {
  return error("Usage: font family [bold] [italic] size");
}

bool CmdFont::parse(Statement const &s) {
  if (s.length()<3 || s.length()>5)
    return usage();
  if (s[1].typ!=Token::BAREWORD)
    return usage();
  if (s[s.length()-1].typ!=Token::NUMBER)
    return usage();
  for (int k=2; k<s.length()-1; k++) {
    if (s[k].typ==Token::BAREWORD) {
      if (s[k].str=="bold")
	continue;
      else if (s[k].str=="italic")
	continue;
    }
    return usage();
  }
  return true;
}


void CmdFont::render(Statement const &s, Figure &f, bool) {
  QFont font(s[1].str);
  //  font.setPointSizeF(pt2iu(s[s.length()-1].num));
  font.setPixelSize(pt2iu(s[s.length()-1].num));
  for (int k=2; k<s.length()-1; k++) {
    if (s[k].str=="bold")
      font.setWeight(QFont::Bold);
    else if (s[k].str=="italic")
      font.setItalic(true);
  }
  f.painter().setFont(font);
}
