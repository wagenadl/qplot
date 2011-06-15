// Command.C

#include "Command.H"
#include <QDebug>

QMap<QString, Command*(*)()> *Command::builders = 0;

void Command::ensureBuilders() {
  if (!builders)
    builders = new QMap<QString, Command*(*)()>();
}

Command::Command() {
}

Command::~Command() {
}

bool Command::error(QString const &s) {
  qDebug() << "Command error: " << s;
  return false;
}

void Command::addBuilder(QString kwd, Command*(*foo)()) {
  ensureBuilders();
  (*builders)[kwd] = foo;
}

Command *Command::construct(QString kwd) {
  if (builders->contains(kwd))
    return (*(*builders)[kwd])();
  else
    return 0;
}

CommandBuilder::CommandBuilder(QString name, Command *(*builder)()) {
  Command::addBuilder(name, builder);
}
