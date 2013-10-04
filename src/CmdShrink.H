// CmdShrink.H

#ifndef CMDSHRINK_H

#define CMDSHRINK_H

#include "Command.H"

class CmdShrink: public Command {
  /*:C CmdShrink
   *:D "shrink" reduces the placement of axes to attempt to fit inside a figure.
   *:D Syntax:
         shrink
         shrink margin_pt
         shrink margin_pt ratio
       Default margin is 1 pt.
       Default ratio is unspecified (x and y independent).
   *:N This does not yet work for rotated axes, and it assumes that
       the y-axis runs up.
   *:N The logic is: if we are a full margin within bounds, we don't do
       anything. Otherwise, we adjust the axes to 2x the margin
   */
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
