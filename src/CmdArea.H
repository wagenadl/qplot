// CmdArea.H

#ifndef CMDAREA_H

#define CMDAREA_H

#include "Command.H"

class CmdArea: public Command {
  /* Syntax:
       area xdata ydata
     This is like "patch", but specified in paper space
   */
public:
  virtual bool parse(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
