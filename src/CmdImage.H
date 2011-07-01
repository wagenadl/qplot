// CmdImage.H

#ifndef CMDIMAGE_H

#define CMDIMAGE_H

#include "Command.H"

class CmdImage: public Command {
public:
  virtual bool parse(Statement const &);
  virtual QRectF dataRange(Statement const &);
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
