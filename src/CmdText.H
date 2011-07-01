// CmdText.H

#ifndef CMDTEXT_H

#define CMDTEXT_H

#include "Command.H"

class CmdText: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
