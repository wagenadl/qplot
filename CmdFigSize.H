// CmdFigSize.H

#ifndef CMDFIGSIZE_H

#define CMDFIGSIZE_H

class CmdFigSize: public Command {
  /* Syntax:
       figsize width_pt height_pt
   */
public:
  virtual bool parse(Statement const &); 
  virtual QRectF bounds(Statement const &, Figure &);
  virtual void render(Statement const &, Figure &);
private:
  bool usage();
};

#endif
