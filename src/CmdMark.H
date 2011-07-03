// CmdMark.H

#ifndef CMDMARK_H

#define CMDMARK_H

#include "Command.H"

class CmdMark: public Command {
  /* Syntax:
       mark xdata ydata
   */
public:
  virtual bool parse(Statement const &);
  virtual QRectF dataRange(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
