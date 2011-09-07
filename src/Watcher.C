// Watcher.C

#include "Watcher.H"
#include <QFileSystemWatcher>
#include <QFile>
#include <QFileInfo>
#include <QDebug>
#include <QTimer>
#include <QMessageBox>

#include "Error.H"

extern void prerender(Program &prog, Figure &fig); // defined in main.C

Watcher::Watcher(QString fn, Program *prog, Figure *fig):
  fn(fn), prog(prog), fig(fig) {
  working = false;
  qmb = new QMessageBox(0);
  fsw = new QFileSystemWatcher();
  fsw->addPath(fn);
  connect(fsw, SIGNAL(fileChanged(QString const &)),
	  this, SLOT(fileChanged()));
  timer = new QTimer(this);
  timer->setSingleShot(true);
  timer->setInterval(100);
  connect(timer, SIGNAL(timeout()),
	  this, SLOT(tick()));
}

Watcher::~Watcher() {
  delete fsw;
}

void Watcher::tick() {
  QDateTime newMod = QFileInfo(fn).lastModified();
  if (newMod>lastMod) {
    lastMod = newMod;
    timer->start();
    return;
  }

  // So the file hasn't changed in the last interval
  bool report = timer->interval()>150;

  if (reread(report)) {
      // success!
      working = false;
  } else {
    // wait a little longer
    int ival = 2*timer->interval();
    if (ival>1000)
      ival=1000;
    timer->setInterval(ival);
    timer->start();
  }
}

void Watcher::fileChanged() {
  if (!working) {
    working = true;
    lastMod = QFileInfo(fn).lastModified();
    timer->setInterval(100);
    timer->start();
  }
}

bool Watcher::reread(bool errorbox) {
  qmb->hide();
  QFile f(fn);
  if (f.open(QFile::ReadOnly)) {
    QString errors;
    QTextStream ts(&errors, QIODevice::WriteOnly);
    if (errorbox)
      Error::setDestination(&ts);
    bool ok = prog->read(f, fn);
    Error::setDestination(0);
    if (ok) {
      fig->hardReset();
      //qDebug() << "read ok: lines=" << prog->length();
      //if (prog->length()>0)
      //	qDebug() << "last line: " << (*prog)[prog->length()-1][0].str;
      ::prerender(*prog, *fig);
      //qDebug() << "prerendered";
      emit ping();
      //qDebug() << "ping emitted";
      return true;
    } else {
      if (errorbox) {
	qmb->setWindowTitle("qplot " + fn);
	if (errors.size()>1000)
	  errors = errors.left(1000) + " ...";
	qmb->setText(errors);
	qmb->show();
      }
      return false;
    }
  } else {
    Error() << "Couldn't open file";
    return false;
  }
}
