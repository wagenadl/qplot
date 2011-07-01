// CmdAt.H

#ifndef CMDAT_H

#define CMDAT_H

#include "Command.H"

class CmdAt: public Command {
public:
  virtual bool parse(Statement const &); 
  virtual QRectF dataRange(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
