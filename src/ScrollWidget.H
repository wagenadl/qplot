// ScrollWidget.H - This file is part of QPlot

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

// ScrollWidget.H

#ifndef SCROLLWIDGET_H

#define SCROLLWIDGET_H

#include <QWidget>

class ScrollWidget: public QWidget {
  Q_OBJECT;
public:
  ScrollWidget(QWidget *parent);
  virtual ~ScrollWidget();
public:
  void setExtent(QRectF const &);
  void autoSize();
  void setTopLeft(QPointF tl);
  void setScale(double factor);
  void scaleToFit();
  QRectF const &extent() const; // world size
  QPointF const &topLeft() const; // world coords of current topleft
  QPointF tlDest() const; // screen coords for tl (=(0,0) except at low zoom)
  double scale() const;
protected:
  void keyPressEvent(QKeyEvent *);
  void mousePressEvent(QMouseEvent *);
  void mouseMoveEvent(QMouseEvent *);
private:
  void surePan();
  void sureScale();
  double perfectScale() const; 
private:
  bool scaletofit;
  QRectF extent_world;
  QPointF tl_world;
  double scalefactor;
  QPointF pos_press;
  QPointF tl_press;
};

#endif
