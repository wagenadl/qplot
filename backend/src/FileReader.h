// FileReader.h

#ifndef FILEREADER_H

#define FILEREADER_H

#include <QThread>
#include <QMutex>
#include <QList>
#include <QDateTime>

#include "Statement.h"

class FileReader: public QThread {
  Q_OBJECT;
public:
  struct Contents {
    bool valid;
    QList<Statement> contents;
    QString error;
    Contents() { valid = false; }
  };
public:
  FileReader(QString filename); // reads the program
  // use "exec()" to start thread to re-read program automatically
  virtual ~FileReader();
  Contents contents() const;
signals:
  void ready(); // emitted when program re-read, even if with errors
protected:
  void run() override;
private:
  Contents read(); // true if OK
  void fileChanged();
  void tick();
private:
  QString filename;
  Contents cont;
  mutable QMutex mutex;
  class QFileSystemWatcher *fsw;
  class QTimer *timer;
  QDateTime lastMod;
  qint64 lastSize;
  bool waiting;
};

#endif
