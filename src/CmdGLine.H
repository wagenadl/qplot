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
