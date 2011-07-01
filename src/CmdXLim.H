// CmdXLim.H

#ifndef CMDXLIM_H

#define CMDXLIM_H

#include "Command.H"

class CmdXLim: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
