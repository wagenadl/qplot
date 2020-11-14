// CmdShareLim.H - This file is part of QPlot

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

// CmdShareLim.H

#ifndef CMDSHARELIM_H

#define CMDSHARELIM_H

#include "Command.h"

class CmdShareLim: public Command {
  /*:C CmdShareLim
   *:D "sharelim" reduces the placement of axes so that multiple panels
       line up.
   *:D Syntax:
         sharelim ID...
         sharelim x ID...
         sharelim y ID...
   *:D This links the current panel with the named panels in a symmetric
       fashion.
   *:N This does not yet work for rotated axes, and it assumes that
       the y-axis runs up.
   */
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
