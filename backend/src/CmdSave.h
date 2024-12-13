// CmdSave.H - This file is part of QPlot

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

// CmdSave.H

#ifndef CMDSAVE_H

#define CMDSAVE_H

#include "Command.h"

class CmdSave: public Command {
public:
  virtual bool parse(Statement const &);
  virtual void render(Statement const &, Figure &, bool) {}
  QString filename() const { return ofn; }
  double resolution() const { return reso; }
  int quality() const { return qual; }
private:
  bool usage();
  QString ofn;
  double reso=300;
  int qual=95;
};

#endif
