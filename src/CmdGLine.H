// CmdGLine.H

#ifndef CMDGLINE_H

#define CMDGLINE_H

#include "Command.H"

class CmdGLine: public Command {
  /* Syntax:
       gline xdata ydata
     This is like "plot", but specified in paper space
   */
public:
  virtual bool parse(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
