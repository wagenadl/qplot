// CmdBrush.H

#ifndef CMDBRUSH_H

#define CMDBRUSH_H

#include "Command.H"

class CmdBrush: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
