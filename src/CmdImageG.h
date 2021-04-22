// CmdImageG.H - This file is part of QPlot

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

// CmdImageG.H

#ifndef CMDIMAGEG_H

#define CMDIMAGEG_H

#include "Command.h"

class CmdImageG: public Command {
public:
  virtual bool parse(Statement const &);
  virtual QRectF dataRange(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
  bool parse_complex(Statement const &);
  bool parse_simple(Statement const &);
  void render_complex(Statement const &, Figure &, bool);
  void render_simple(Statement const &, Figure &, bool);
};

#endif