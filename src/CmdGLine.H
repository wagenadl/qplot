// CmdGLine.H - This file is part of QPlot

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

// CmdGLine.H

#ifndef CMDGLINE_H

#define CMDGLINE_H

#include "Command.H"

class CmdGLine: public Command {
  /* GLINE / GAREA: command for supergeneral line/polygon drawing:
        gline ( PT1SPEC ) ( PT2SPEC ) ...
        garea ( PT1SPEC ) ( PT2SPEC ) ...
     
     where PTnSPEC is:
        COMMAND1 ARGS1 [COMMAND2 ARGS2] ...
     
     where COMMANDs are:
        absdata X Y
        abspaper X Y
        reldata DX DY
        relpaper DX DY
        rotdata XI ETA
        rotpaper PHI
        retract L
        retract L1 L2
   
     ABSDATA and RELDATA are specified in data coordinates.
     ABSPAPER and RELPAPER are specified in paper coordinates
     ROTDATA uses atan2(eta, xi) for its angle. ROTPAPER is directly specified
     in radians.
     Retraction is along the line segment; two numbers may be given for 
     internal points. Distances are specified in postscript points.
   
     For instance,
       gline ( absdata 0 1 relpaper 5 0 ) ( absdata 0 1 relpaper 0 5 )
     draws a line from 5 pt to the right of the point (0,1) in the graph to
     5 pt above the point (1,0) on the graph.
  */
public:
  virtual bool parse(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage(QString x="");
};

#endif
