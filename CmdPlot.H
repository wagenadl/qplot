// CmdPlot.H

#ifndef CMDPLOT_H

#define CMDPLOT_H

#include "Command.H"

class CmdPlot: public Command {
  /* Syntax:
       plot xdata ydata
   */
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
