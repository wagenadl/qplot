// PipeReader.cpp

#include "PipeReader.h"
#include "Error.h"
#include <QDebug>
#include <iostream>
#ifdef _WIN32
#include <io.h>
#endif
#include <fcntl.h>

PipeReader::PipeReader() {
}

PipeReader::~PipeReader() {
  if (isRunning())
    terminate();
}

void PipeReader::run() {
  #ifdef _WIN32
  _setmode(_fileno(stdin), _O_BINARY);
  #endif
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
