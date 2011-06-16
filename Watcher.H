// Watcher.H

#ifndef WATCHER_H

#define WATCHER_H

#include "Program.H"
#include "Figure.H"
#include <QWidget>

class Watcher: public QObject {
  Q_OBJECT;
public:
  Watcher(QString fn, Program *prog, Figure *fig);
  virtual ~Watcher();
signals:
  void ping();
private slots:
  void pong();
private:
  bool reread();
protected:
  void timerEvent(QTimerEvent *);
private:
  QString fn;
  Program *prog;
  Figure *fig;
  class QFileSystemWatcher *fsw;
  int tid;
};

#endif
