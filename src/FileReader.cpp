// FileReader.cpp

#include "FileReader.h"
#include <QFileSystemWatcher>
#include <QTimer>
#include <QMutexLocker>
#include <QFileInfo>
#include <QDebug>
#include <QEventLoop>

FileReader::FileReader(QString filename): filename(filename) {
  cont = read();
}

FileReader::~FileReader() {
  if (isRunning())
    terminate();
}

void FileReader::run() {
  fsw = new QFileSystemWatcher();
  fsw->addPath(filename);
  waiting = false;

  timer = new QTimer();
  timer->setSingleShot(true);
  timer->setInterval(100);

  connect(timer, &QTimer::timeout,
          [this]() { tick(); }); // this lambda slot runs in thread
  connect(fsw, &QFileSystemWatcher::fileChanged,
          [this]() { fileChanged(); }); // ditto

  QEventLoop loop;
  loop.exec();

  delete fsw;
  delete timer;
}

void FileReader::tick() {
  timer->stop();
  QFileInfo fi(filename);
  QDateTime newMod = fi.lastModified();
  qint64 newSize = fi.size();
  if (newSize!=lastSize || newMod>lastMod) { // has the file changed again?
    lastMod = newMod;
    lastSize = newSize;
    timer->start();
    return;
  }

  // read the file
  Contents c = read();
  mutex.lock();
  cont = c;
  mutex.unlock();
  emit ready(); // even if program incomplete

  if (c.valid) {
    waiting = false;
    timer->setInterval(100); // for next time
  } else {
    // wait a little longer so we don't produce infinitely many errors
    int ival = 2*timer->interval();
    if (ival>1000)
      ival=1000;
    timer->setInterval(ival);
    timer->start();
  }
}

void FileReader::fileChanged() {
  if (!waiting) {
    waiting = true;
    QFileInfo fi(filename);
    lastMod = fi.lastModified();
    lastSize = fi.size();
    timer->start();
  }
}

FileReader::Contents FileReader::contents() const {
  QMutexLocker locker(&mutex);
  Contents c = cont;
  return c;
}

FileReader::Contents FileReader::read() {
  Contents c;

  QFile f(filename);
  
  bool opened = false;
  if (filename=="-" || filename=="") 
    opened = f.open(stdin, QFile::ReadOnly);
  else
    opened = f.open(QFile::ReadOnly);
  
  if (!opened) {
    c.error = QString("Could not open “%2”").arg(filename);
    return c;
  }

  int line = 1;
  while (!f.atEnd()) {
    Statement s;
    if (s.read(f)) {
      c.contents.append(s);
      line += s.lineCount();
    } else {
      c.error = QString("Read error at line %1 of “%2”")
        .arg(line).arg(filename);
      return c;
    }
  }
  c.valid = true;
  return c;
}
