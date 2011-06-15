// CmdPlot.H

#ifndef CMDPLOT_H

#define CMDPLOT_H

#include "Command.H"

class CmdPlot: public Command {
  /* Syntax:
       plot [ xdata ] [ ydata ]
       plot x y
   */
public:
  CmdPlot();
  virtual ~CmdPlot();
  virtual bool parse(Statement const &); 
  virtual QRectF bounds(Statement const &, Figure &);
  virtual void render(Statement const &, Figure &);
private:
  bool usage();
public:
  static Command *construct();
  
};

#endif
