// CmdYlim.H

#ifndef CMDYLIM_H

#define CMDYLIM_H

#include "Command.H"

class CmdYLim: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
