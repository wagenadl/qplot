// CmdYLim.cpp - This file is part of QPlot

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

// CmdYlim.C

#include "CmdYLim.h"


static CBuilder<CmdYLim> cbYLim("ylim");

bool CmdYLim::usage() {
  return error("Usage: ylim y0 y1");
}

bool CmdYLim::parse(Statement const &s) {
  if (s.length()==3 && s[1].typ==Token::NUMBER && s[2].typ==Token::NUMBER)
    return true;
  else
    return usage();
}

QRectF CmdYLim::dataRange(Statement const &s) {
  double y0 = s[1].num;
  double y1 = s[2].num;
  return QRectF(QPointF(0, y0), QPointF(-1, y1)); // return -ve width rect.
}


void CmdYLim::render(Statement const &s, Figure &f, bool) {
  double y0 = s[1].num;
  double y1 = s[2].num;
  f.forceBBoxY(f.map(0,y0).y(), f.map(0,y1).y());
  //f.yAxis().setDataRange(y0, y1);
}
