// CmdPanel.cpp - This file is part of QPlot

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

// CmdPanel.C

#include "CmdPanel.h"


static CBuilder<CmdPanel> cbPanel("panel");

bool CmdPanel::usage() {
  return error("Usage: panel ID [x y w h] | -");
}

bool CmdPanel::parse(Statement const &s) {
  if (s.length()==2 && s[1].typ==Token::DASH)
    return true;
  else if (s.length()==2 &&
	   (s[1].typ==Token::CAPITAL || s[1].typ==Token::BAREWORD))
    return true;
  else if (s.length()==2+4 &&
	   (s[1].typ==Token::CAPITAL || s[1].typ==Token::BAREWORD) &&
	   s[2].typ==Token::NUMBER &&
	   s[3].typ==Token::NUMBER &&
	   s[4].typ==Token::NUMBER &&
	   s[5].typ==Token::NUMBER)
    return true;
  else
    return usage();
}


void CmdPanel::render(Statement const &s, Figure &f, bool dryrun) {
  f.leavePanel();
  if (s[1].typ==Token::DASH)
    return;
  
  QRectF area;
  if (s.length()==6) {
    area = QRectF(pt2iu(s[2].num), pt2iu(s[3].num),
		  pt2iu(s[4].num), pt2iu(s[5].num));
    if (!dryrun)
      f.painter().drawRect(area);
  }
  f.choosePanel(s[1].str);
  if (s.length()==6)
    f.setExtent(area);
}
