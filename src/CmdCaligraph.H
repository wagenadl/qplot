// CmdCaligraph.H

#ifndef CMDCALIGRAPH_H

#define CMDCALIGRAPH_H

#include "Command.H"

class CmdCaligraph: public Command {
  /* Syntax:
       caligraph xdata ydata widthdata
   */
public:
  virtual bool parse(Statement const &);
  virtual QRectF dataRange(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
