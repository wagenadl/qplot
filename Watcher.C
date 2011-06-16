// Watcher.C

#include "Watcher.H"
#include <QFileSystemWatcher>
#include <QFile>
#include <QDebug>
#include "Error.H"

extern void prerender(Program &prog, Figure &fig); // defined in main.C

Watcher::Watcher(QString fn, Program *prog, Figure *fig):
  fn(fn), prog(prog), fig(fig) {
  fsw = new QFileSystemWatcher();
  fsw->addPath(fn);
  connect(fsw, SIGNAL(fileChanged(QString const &)),
	  this, SLOT(pong()));
}

Watcher::~Watcher() {
  delete fsw;
}

void Watcher::timerEvent(QTimerEvent *) {
  if (tid)
    killTimer(tid);
  tid=0;
  reread();
}

void Watcher::pong() {
  if (!reread()) xxxxxxxxxxxx
    tid = startTimer(500);
}

bool Watcher::reread() {
  QFile f(fn);
  if (f.open(QFile::ReadOnly)) {
    QTextStream ts(&f);
    if (prog->read(ts, fn)) {
      ::prerender(*prog, *fig);
      Error() << "Reread file";
      emit ping();
      return true;
    } else {
      Error() << "Parsing error";
      return false;
    }
  } else {
    Error() << "Couldn't open file";
    return false;
  }
}
