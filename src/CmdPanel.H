// CmdPanel.H

#ifndef CMDPANEL_H

#define CMDPANEL_H

#include "Command.H"

class CmdPanel: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
