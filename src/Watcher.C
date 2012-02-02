// Watcher.C

#include "Watcher.H"
#include <QFileSystemWatcher>
#include <QFile>
#include <QFileInfo>
#include <QDebug>
#include <QToolTip>
#include <QTimer>
#include <QPushButton>
#include <QTextEdit>

#include "Error.H"

extern void prerender(Program &prog, Figure &fig); // defined in main.C

Watcher::Watcher(QString fn, Program *prog, Figure *fig, QWidget *dest):
  fn(fn), prog(prog), fig(fig), dest(dest) {
  working = false;
  //  warnlabel = new QPushButton(dest);
  warnlabel = new QTextEdit(dest);
  warnlabel->setReadOnly(true);
  QPalette p;
  p.setColor(QPalette::Base, "#dddddd");
  p.setColor(QPalette::Text, "#c00000");
  warnlabel->setPalette(p);
  warnlabel->hide();
  //connectt(warnlabel, SIGNAL(clicked()),
  //  this, SLOT(openDetails()));
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
  timer->stop();
  QFileInfo fi(fn);
  QDateTime newMod = fi.lastModified();
  qint64 newSize = fi.size();
  if (newSize!=lastSize || newMod>lastMod) {
    lastMod = newMod;
    lastSize = newSize;
    timer->start();
    return;
  }
  // So the file hasn't changed in the last interval

  // only report if we've had at least one error before?
  bool report = true; //timer->interval()>150;

  if (reread(report)) {
    // success!
    working = false;
    warnlabel->hide();
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
    QFileInfo fi(fn);
    lastMod = fi.lastModified();
    lastSize = fi.size();
    //timer->setInterval(100);
    timer->start();
  }
}

bool Watcher::reread(bool errorbox) {
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
	//warnlabel->setGeometry(0, dest->height()-32, dest->width(), 32);
	warnlabel->setGeometry(0, 0, dest->width(), dest->height());
	//warnlabel->setToolTip(errors);
	warnlabel->setText("Rendering failed due to errors:\n\n" + errors);
	//int idx = errors.indexOf("\n");
	//QString first = (idx>0) ? errors.left(idx) : errors;
	//	warnlabel->setText("Render errors: Click to see details");
	warnlabel->show();
      }
      return false;
    }
  } else {
    Error() << "Couldn't open file";
    return false;
  }
}

void Watcher::openDetails() {
  QPoint x(warnlabel->mapToGlobal(QPoint(warnlabel->width()/2, warnlabel->height()/2)));
  QString t(warnlabel->toolTip());
  qDebug() << x << t;
  QToolTip::showText(x, t);
}
