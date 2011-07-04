// CmdEndGroup.H

#ifndef CMDENDGROUP_H

#define CMDENDGROUP_H

#include "Command.H"

class CmdEndGroup: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
