// CmdHatch.h

#ifndef CMDHATCH_H

#define CMDHATCH_H

#include "CmdPlot.h"

class CmdHatch: public CmdPlot {
  /* Syntax:
     hatch xdata ydata angle(rad) spacing(points) (offset(points))
  */
public:
  virtual QRectF dataRange(Statement const &);
  virtual bool parse(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
