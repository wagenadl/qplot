// QPWidget.H - This file is part of QPlot

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

// QPWidget.H

#ifndef QPWIDGET_H

#define QPWIDGET_H

#include "ScrollWidget.h"
#include "Figure.h"
#include "Program.h"
#include <QFile>

class QPWidget: public ScrollWidget {
  Q_OBJECT;
public:
  QPWidget(QWidget *parent=0);
  virtual ~QPWidget();
  void setContents(Figure *f, Program *p);
  void setMargin(double pix);
  virtual void setWindowTitle(QString s);
  void setRuler(bool);
  bool hasRuler() const;
  void takeScreenShot();
protected:
  virtual void keyPressEvent(QKeyEvent *);
  virtual void paintEvent(QPaintEvent *);
  virtual void resizeEvent(QResizeEvent *);
  virtual void mouseReleaseEvent(QMouseEvent *);
  virtual void mouseMoveEvent(QMouseEvent *);
  virtual void mousePressEvent(QMouseEvent *);
  virtual void mouseDoubleClickEvent(QMouseEvent *);
  virtual void closeEvent(QCloseEvent *);
private:
  void reportTrack(QPointF xy, int button, QString what);
  void renderMargin(QPainter &);
  void renderRuler(QPainter &);
  void pickCursor();
  Axis *findXAxis();
  Axis *findYAxis();
  void feedback(QString);
private:
  Figure *fig;
  Program *prog;
  double marg;
  enum MarginDecor {
    NONE,
    GRAY,
    CROP,
  } margindecor;
  QRectF worldextent;
  QString winttl;
  QString trackpanel;
  class QLabel *coord;
  bool ruler;
  bool coords;
  bool brandnew;
};

#endif
