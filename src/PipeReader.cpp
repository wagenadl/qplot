// PipeReader.cpp

#include "PipeReader.h"
#include "Error.h"
#include <QDebug>
#include <iostream>

PipeReader::PipeReader() {
}

PipeReader::~PipeReader() {
  if (isRunning())
    terminate();
}

void PipeReader::run() {
  int line = 1;
  while (!std::cin.eof()) {
    Statement s;
    if (s.read(std::cin)) {
      mutex.lock();
      queue.append(s);
      mutex.unlock();
      emit ready();
    } else {
      if (!std::cin.eof())
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
