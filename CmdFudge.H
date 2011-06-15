// CmdFudge.H

#ifndef CMDFUDGE_H

#define CMDFUDGE_H

class CmdFudge: public Command {
  /*:C CmdFudge
   *:D "fudge" reduces the placement of axes to attempt to fit inside a figure.
   *:D Syntax:
         fudge
         fudge margin_pt
       Default is 1 pt.
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
