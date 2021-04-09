// Watcher.cpp - This file is part of QPlot

/* QPlot - Publication quality 2D graphs with dual coordinate systems
   Copyright (C) 2014  Daniel Wagenaar
  
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
  
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
  
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// Watcher.C

#include "Watcher.h"
#include "QPWidget.h"
#include <QFileSystemWatcher>
#include <QFile>
#include <QFileInfo>
#include <QDebug>
#include <QToolTip>
#include <QTimer>
#include <QPushButton>
#include <QTextEdit>

#include "Error.h"
#include "Render.h"

Watcher::Watcher(QString fn, Render *render, QPWidget *dest):
  fn(fn), render(render), dest(dest) {
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
    bool ok = render->program()->read(f, fn);
    Error::setDestination(0);
    if (ok) {
      dest->resetFeedbackFile();
      render->figure()->hardReset();
      render->prerender();
      emit ping();
      return true;
    } else {
      if (errorbox) {
	warnlabel->setGeometry(0, 0, dest->width(), dest->height());
	warnlabel->setText("Rendering failed due to errors:\n\n" + errors);
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
