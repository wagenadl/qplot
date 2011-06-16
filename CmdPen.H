// CmdPen.H

#ifndef CMDPEN_H

#define CMDPEN_H

#include "Command.H"

class CmdPen: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
