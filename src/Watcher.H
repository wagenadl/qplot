// Watcher.H

#ifndef WATCHER_H

#define WATCHER_H

#include "Program.H"
#include "Figure.H"
#include <QWidget>
#include <QDateTime>

class Watcher: public QObject {
  Q_OBJECT;
public:
  Watcher(QString fn, Program *prog, Figure *fig, QWidget *dest);
  virtual ~Watcher();
  bool reread(bool errorbox);
signals:
  void ping();
private slots:
  void fileChanged(); // file changed
  void tick(); // timer event
  void openDetails();
private:
  QString fn;
  Program *prog;
  Figure *fig;
  class QFileSystemWatcher *fsw;
  class QTimer *timer;
  QWidget *dest;
  class QPushButton *warnlabel;
  bool working;
  QDateTime lastMod;
};

#endif
