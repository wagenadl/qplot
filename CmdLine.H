// CmdLine.H

#ifndef CMDLINE_H

#define CMDLINE_H

#include "Command.H"

class CmdLine: public Command {
  /* Syntax:
       line xdata ydata
     This is like "plot", but specified in paper space
   */
public:
  virtual bool parse(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
