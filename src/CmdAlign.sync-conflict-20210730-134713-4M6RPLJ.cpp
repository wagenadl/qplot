// CmdAlign.cpp - This file is part of QPlot

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

// CmdAlign.C

#include "CmdAlign.H"
#include "Align.H"

static CBuilder<CmdAlign> cbAlign("align");

bool CmdAlign::usage() {
  return error("Usage: align left|right|center|top|bottom|middle|base ...");
}

static int halignment(QString s) {
  if (s=="left")
    return Align::LEFT;
  else if (s=="right")
    return Align::RIGHT;
  else if (s=="center")
    return Align::CENTER;
  else
    return -1;
}

static int valignment(QString s) {
  if (s=="top")
    return Align::TOP;
  else if (s=="bottom")
    return Align::BOTTOM;
  else if (s=="middle")
    return Align::MIDDLE;
  else if (s=="base")
    return Align::BASE;
  else
    return -1;
}

bool CmdAlign::parse(Statement const &s) {
  if (s.length()<2)
    return usage();
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::BAREWORD) {
      if (valignment(s[k].str)>=0)
	continue;
      else if (halignment(s[k].str)>=0)
	continue;
    }
    return usage();
  }
  return true;
}


void CmdAlign::render(Statement const &s, Figure &f, bool) {
  for (int k=1; k<s.length(); k++) {
    if (halignment(s[k].str)>=0)
      f.setHAlign(Align::HAlign(halignment(s[k].str)));
    else if (valignment(s[k].str)>=0)
      f.setVAlign(Align::VAlign(valignment(s[k].str)));
  }
}
