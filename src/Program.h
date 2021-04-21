// Program.H - This file is part of QPlot

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

// Program.H

#ifndef PROGRAM_H

#define PROGRAM_H

#include <QFile>
#include "Statement.h"
#include "Command.h"

class Program {
public:
  Program(QString label="");
  virtual ~Program();
  void reset();
  void setLabel(QString);
  void read(QList<Statement> const &); // Updates isOK.
  void append(Statement const &); // Updates isOK.
  bool isValid() const { return isOK; }
  int length() const; // number of statements
  Statement const &operator[](int) const;
  QSet<QString> panels();
  QRectF dataRange(QString panel="-");
  /*:F dataRange
   *:D Returns the full (x0-x1 x y0-y1) range of data in this program.
   *:N This ignores "panels", and will therefore work as expected only if
       there are none.
   */
  void render(Figure &f, bool dryrun=false);
private:
  bool parse(Statement const &s, int lineno); // true if ok. errors are reported through Error()
private:
  QList<Statement> stmt;
  QList<Command *> cmds;
  bool isOK;
  QString label;
  int line;
};

#endif
