// Program.H

#ifndef PROGRAM_H

#define PROGRAM_H

#include <QFile>
#include "Statement.H"
#include "Command.H"

class Program {
public:
  Program();
  bool read(QFile &ts, QString label);
  /*:F read
   *:D Reads and parses a program.
   *   Returns true if OK, false if error.
   *   Errors are reported through qDebug.
   */
  virtual ~Program();
  int length() const;
  Statement const &operator[](int) const;
  QSet<QString> panels();
  QRectF dataRange(QString panel="-");
  /*:F dataRange
   *:D Returns the full (x0-x1 x y0-y1) range of data in this program.
   *:N This ignores "panels", and will therefore work as expected only if
       there are none.
   */
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
