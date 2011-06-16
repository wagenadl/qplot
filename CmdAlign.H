// CmdAlign.H

#ifndef CMDALIGN_H

#define CMDALIGN_H

#include "Command.H"

class CmdAlign: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
