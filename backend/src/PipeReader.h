// PipeReader.h

#ifndef PIPEREADER_H

#define PIPEREADER_H

#include <QThread>

#include "Statement.h"
#include <QList>
#include <QMutex>

class PipeReader: public QThread {
  Q_OBJECT;
public:
  PipeReader();
  virtual ~PipeReader();
  QList<Statement> readQueue();
signals:
  void ready();
protected:
  void run() override;
private:
  QMutex mutex;
  QList<Statement> queue;
};

#endif
