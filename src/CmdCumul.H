// CmdCumul.H

#ifndef CMDCUMUL_H

#define CMDCUMUL_H

#include "Command.H"

class CmdCumul: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
