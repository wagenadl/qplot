// Program.H

#ifndef PROGRAM_H

#define PROGRAM_H

#include <QTextStream>
#include "Statement.H"
#include "Command.H"

class Program {
public:
  Program();
  bool read(QTextStream &ts, QString label);
  /*:F read
   *:D Reads and parses a program.
   *   Returns true if OK, false if error.
   *   Errors are reported through qDebug.
   */
  ~Program();
  int length() const;
  Statement const &operator[](int) const;
  QRectF dataRange();
  void render(Figure &f, bool dryrun=false);
private:
  bool error(QString const &); // returns false
  bool error(QString const &, int idx); // returns false
private:
  QList<Statement> stmt;
  QList<Command *> cmds;
  bool isOK;
};

#endif
