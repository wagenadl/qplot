// CmdFigSize.H

#ifndef CMDFIGSIZE_H

#define CMDFIGSIZE_H

#include "Command.H"

class CmdFigSize: public Command {
  /* Syntax:
       figsize width_pt height_pt
   */
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
