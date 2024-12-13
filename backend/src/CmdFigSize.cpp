// CmdFigSize.cpp - This file is part of QPlot

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

// CmdFigSize.C

#include "CmdFigSize.h"


static CBuilder<CmdFigSize> cbFigSize("figsize");

bool CmdFigSize::usage() {
  return error("Usage: figsize width_pt height_pt");
}

bool CmdFigSize::parse(Statement const &s) {
  if (s.length()==3 && s[1].typ==Token::NUMBER && s[2].typ==Token::NUMBER)
    return true;
  else
    return usage();
}


void CmdFigSize::render(Statement const &s, Figure &f, bool) {
  double w = pt2iu(s[1].num);
  double h = pt2iu(s[2].num);
  f.setSize(QSizeF(w,h));
}
