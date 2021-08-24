// CmdGroup.cpp - This file is part of QPlot

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

// CmdGroup.C

#include "CmdGroup.H"
#include <QDebug>

static CBuilder<CmdGroup> cbGroup("group");

bool CmdGroup::usage() {
  return error("Usage: group\n");
}

bool CmdGroup::parse(Statement const &s) {
  if (s.length()==1)
    return true;
  else
    return usage();
}

void CmdGroup::render(Statement const &, Figure &f, bool) {
  f.startGroup();
}

