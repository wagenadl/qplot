// Watcher.C

#include "Watcher.H"
#include <QFileSystemWatcher>
#include <QFile>
#include <QDebug>
#include <QTimer>
#include <QMessageBox>

#include "Error.H"

extern void prerender(Program &prog, Figure &fig); // defined in main.C

Watcher::Watcher(QString fn, Program *prog, Figure *fig):
  fn(fn), prog(prog), fig(fig) {
  qmb = new QMessageBox(0);
  fsw = new QFileSystemWatcher();
  fsw->addPath(fn);
  connect(fsw, SIGNAL(fileChanged(QString const &)),
	  this, SLOT(pong()));
}

Watcher::~Watcher() {
  delete fsw;
}

void Watcher::tick() {
  reread(true);
}

void Watcher::pong() {
  if (!reread(false))
    QTimer::singleShot(1000, this, SLOT(tick()));
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
