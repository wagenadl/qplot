// PipeReader.cpp

#include "PipeReader.h"
#include "Error.h"
#include <QDebug>
#include <iostream>
#include <io.h>
#include <fcntl.h>

PipeReader::PipeReader() {
}

PipeReader::~PipeReader() {
  if (isRunning())
    terminate();
}

void PipeReader::run() {
  _setmode(_fileno(stdin), _O_BINARY);
  int line = 1;
  while (std::cin) {
    Statement s;
    if (s.read(std::cin)) {
      mutex.lock();
      queue.append(s);
      mutex.unlock();
      emit ready();
    } else {
      if (std::cin.eof()) {
        Error() << "EOF";
        break;
      } else {
        Error() << QString("Read error at line %1 of stdin").arg(line);
      }
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
