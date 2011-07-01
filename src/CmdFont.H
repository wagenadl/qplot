// CmdFont.H

#ifndef CMDFONT_H

#define CMDFONT_H

#include "Command.H"

class CmdFont: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
