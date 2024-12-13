// CmdEndGroup.cpp - This file is part of QPlot

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

// CmdEndGroup.C

#include "CmdEndGroup.h"
#include <QDebug>

static CBuilder<CmdEndGroup> cbEndGroup("endgroup");

bool CmdEndGroup::usage() {
  return error("Usage: endgroup\n");
}

bool CmdEndGroup::parse(Statement const &s) {
  if (s.length()==1)
    return true;
  else
    return usage();
}

void CmdEndGroup::render(Statement const &, Figure &f, bool dryrun) {
  f.endGroup();
  if (dryrun)
    return;
  if (!f.areBoundingBoxesShown())
    return;
  f.painter().save();
  f.painter().setBrush(Qt::NoBrush);
  f.painter().setPen(QPen(QColor(0, 180, 0), 8, Qt::DotLine, Qt::RoundCap));
  f.painter().drawRect(f.lastBBox());
  f.painter().restore();
}

