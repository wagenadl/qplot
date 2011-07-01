// CmdHairline.H

#ifndef CMDHAIRLINE_H

#define CMDHAIRLINE_H

#include "Command.H"

class CmdHairline: public Command {
  /* Syntax:
       hairline 1|0
   */
public:
  virtual bool parse(Statement const &); 
  virtual void render(Statement const &, Figure &, bool);
private:
  bool usage();
};

#endif
