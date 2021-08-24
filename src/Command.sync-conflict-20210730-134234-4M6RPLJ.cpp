// Command.cpp - This file is part of QPlot

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

// Command.C

#include "Command.H"
#include <QDebug>
#include "Error.H"

QMap<QString, CBuilder_ *> *Command::builders = 0;

void Command::addBuilder(QString x, class CBuilder_ *b) {
  if (!builders)
    builders = new QMap<QString, CBuilder_ *>();
  (*builders)[x] = b;
}

bool Command::error(QString const &s) {
  Error() << "Command error: " << s;
  return false;
}

Command *Command::construct(QString kwd) {
  if (builders && builders->contains(kwd))
    return (*builders)[kwd]->build();
  else
    return 0;
}

QRectF Command::dataRange(Statement const &) {
  return QRectF();
}
