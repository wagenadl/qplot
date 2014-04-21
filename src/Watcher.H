// Watcher.H - This file is part of QPlot

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
  //class QPushButton *warnlabel;
  class QTextEdit *warnlabel;
  bool working;
  QDateTime lastMod;
  qint64 lastSize;
};

#endif
