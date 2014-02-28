// Command.C

#include "Command.H"
#include <QDebug>
#include "Error.H"

QMap<QString, CBuilder_ *> *Command::builders = 0;

void Command::addBuilder(QString x, class CBuilder_ *b) {
  if (!builders)
    builders = new QMap<QString, CBuilder_ *>();
  (*builders)[x] = b;
}

bool Command::error(QString const &s) {
  Error() << "Command error: " << s;
  return false;
}

Command *Command::construct(QString kwd) {
  if (builders && builders->contains(kwd))
    return (*builders)[kwd]->build();
  else
    return 0;
}

QRectF Command::dataRange(Statement const &) {
  return QRectF();
}