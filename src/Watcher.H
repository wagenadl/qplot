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
  bool reread(bool errorbox);
signals:
  void ping();
private slots:
  void pong(); // file changed
  void tick(); // timer event
private:
  QString fn;
  Program *prog;
  Figure *fig;
  class QFileSystemWatcher *fsw;
  class QMessageBox *qmb;
};

#endif
