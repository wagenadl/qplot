// CmdShareLim.H

#ifndef CMDSHARELIM_H

#define CMDSHARELIM_H

#include "Command.H"

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
