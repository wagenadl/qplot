// CmdMarker.H

#ifndef CMDMARKER_H

#define CMDMARKER_H

#include "Command.H"

class CmdMarker: public Command {
public:
  virtual bool parse(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
