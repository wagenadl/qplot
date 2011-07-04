// CmdGroup.H

#ifndef CMDGROUP_H

#define CMDGROUP_H

#include "Command.H"

class CmdGroup: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
