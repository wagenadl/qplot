// PipeReader.cpp

#include "PipeReader.h"
#include "Error.h"
#include <QDebug>

PipeReader::PipeReader() {
}

PipeReader::~PipeReader() {
  if (isRunning())
    terminate();
}

void PipeReader::run() {
  QFile f;
  if (!f.open(stdin, QFile::ReadOnly)) {
    Error() << "Could not open stdin";
    return;
  }

  int line = 1;
  while (!f.atEnd()) {
    Statement s;
    if (s.read(f)) {
      mutex.lock();
      queue.append(s);
      mutex.unlock();
      emit ready();
    } else {
      if (!f.atEnd())
        Error() << QString("Read error at line %1 of stdin").arg(line);
    }
    line += s.lineCount();
  }
}

QList<Statement> PipeReader::readQueue() {
  mutex.lock();
  QList<Statement> res = queue;
  queue = QList<Statement>();
  mutex.unlock();
  return res;
}
