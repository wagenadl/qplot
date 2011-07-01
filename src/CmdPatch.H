// CmdPatch.H

#ifndef CMDPATCH_H

#define CMDPATCH_H

#include "Command.H"

class CmdPatch: public Command {
  /* Syntax:
       patch xdata ydata
   */
public:
  virtual bool parse(Statement const &);
  virtual QRectF dataRange(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
