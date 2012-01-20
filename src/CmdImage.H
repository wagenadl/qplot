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
  bool parse_complex(Statement const &);
  bool parse_simple(Statement const &);
  void render_complex(Statement const &, Figure &, bool);
  void render_simple(Statement const &, Figure &, bool);
};

#endif
