// CmdReftext.H

#ifndef CMDREFTEXT_H

#define CMDREFTEXT_H

#include "Command.H"

class CmdRefText: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
