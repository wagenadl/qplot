// Command.H

#ifndef COMMAND_H

#define COMMAND_H

#include "Statement.H"
#include "Figure.H"
#include <QMap>

class Command {
public:
  Command();
  virtual ~Command();
  virtual bool parse(Statement const &)=0;
  /*:F parse
   *:D Should check whether the statement is valid.
   */
  virtual QRectF bounds(Statement const &, Figure &)=0;
  /*:F bounds
   *:D Should calculate the bounding box of the graphics this statement
       would produce.
       You may assume that parse() has returned OK.
       The Figure's Painter may be used to get style information.
  */
  virtual void render(Statement const &, Figure &)=0;
  /*:F render
   *:D Should actually plot the statement to the figure.
       You may assume that parse() has returned OK.
       The output should remain within the bounds returned by bounds().
  */
public:
  static void addBuilder(QString kwd, Command *(*foo)(void));
protected:
  bool error(QString const &);
public:
  static Command *construct(QString kwd);
private:
  static QMap<QString, Command*(*)()> *builders;
  static void ensureBuilders();
};

class CommandBuilder {
public:
  CommandBuilder(QString name, Command *(*builder)());
};

#endif
