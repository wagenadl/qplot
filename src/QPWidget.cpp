// QPWidget.cpp - This file is part of QPlot

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

// QPWidget.C

#include "QPWidget.h"
#include <QDebug>
#include <QKeyEvent>
#include <QLabel>
#include <math.h>
#include <QApplication>
#include <QClipboard>
#include <iostream>

#define MARGPIX 15

QPWidget::QPWidget(QWidget *parent): ScrollWidget(parent) {
  brandnew = true;
  fig=0;
  prog=0;
  marg = 20;
  margindecor = NONE;
  coord = new QLabel(this);
  coord->hide();
  coord->resize(width()/2, 24);
  coord->move(5, height() - coord->height() - 5);
  trackpanel = "-";
  ruler = false;
}

QPWidget::~QPWidget() {
}

void QPWidget::setMargin(double m) {
  marg = m;
  setExtent(worldextent.adjusted(-marg, -marg, marg, marg));
}

void QPWidget::setContents(Figure *f, Program *p) {
  fig = f;
  prog = p;
  if (fig) {
    worldextent = fig->extent();
    setExtent(worldextent.adjusted(-marg, -marg, marg, marg));
  } else {
    update();
  }
}


void QPWidget::paintEvent(QPaintEvent *) {
  if (!fig || !prog)
    return;

  if (fig->extent()!=worldextent) {
    worldextent = fig->extent();
    setExtent(worldextent.adjusted(-marg, -marg, marg, marg));
    if (brandnew)
      resize((worldextent.size()/20).toSize());
    brandnew = false;
    autoSize();
  }    
  
  QPainter &p(fig->painter());
  p.begin(this); // resets state of pen

  if (margindecor!=GRAY) {
    p.save();
    p.setBrush(QColor("white"));
    p.setPen(Qt::NoPen);
    p.drawRect(rect());
    p.restore();
  }
  
  QPointF tld = tlDest();
  p.translate(tld.x(), tld.y());
  double s = scale();
  p.scale(s, s);
  QPointF tlw = topLeft();
  p.translate(-tlw.x(), -tlw.y());

  renderMargin(p);
  if (ruler)
    renderRuler(p);

  fig->setHairline(0);
  prog->render(*fig);
  
  p.end();
}

static QString coordtext(double x, double dx) {
  // represents X so that a difference of DX is clear.
  if (x==0)
    return "0";
  if (dx<=0)
    return QString::fromUtf8("–");
  int k = floor(log(dx)/log(10));
  if (k<=0)
    return QString("%1").arg(x, 0, 'f', -k);
  int l = floor(log(abs(x))/log(10));
  // I will show l-k digits, with exponentiation (XXXeN where N is l).
  // I could also show just l digits. If that is more compact, I will do it.
  if (l < l-k + 2)
    return QString("%1").arg(x, 0, 'f', 0);
  k = l-k+1;
  if (k<1)
    k=1;
  return QString("%1").arg(x, 0, 'e', k);
}

static QString coordtext(double x, double x0, double x1) {
  return coordtext(x, 2e-3*(x1-x0));
}


static double sensibleStep(double range) {
  double mx = range/5;
  double lg = log10(mx);
  double ord = floor(lg);
  double sub = pow(10, lg-ord);
  if (sub>=5)
    sub=5;
  else if (sub>=2)
    sub=2;
  else
    sub=1;
  return sub * pow(10,ord);
}

void QPWidget::renderRuler(QPainter &p) {
  p.save();

  QRectF world = fig->extent();
  Axis *xax = findXAxis();
  Axis *yax = findYAxis();

  double x0 = xax->min();
  double x1 = xax->max();
  double dx = sensibleStep(x1-x0);
  x0 = ceil(x0/dx)*dx;
  x1 = floor(x1/dx)*dx;

  double y0 = yax->min();
  double y1 = yax->max();
  double dy = sensibleStep(y1-y0);
  y0 = ceil(y0/dy)*dy;
  y1 = floor(y1/dy)*dy;

  p.setPen("#aaaaaa");

  for (double x=x0; x<=x1+dx/2; x+=dx) {
    double xw = xax->map(x).x();
    p.drawLine(xw, world.top()-pt2iu(2), xw, world.top()-pt2iu(5));
    p.drawLine(xw, world.bottom()+pt2iu(2), xw, world.bottom()+pt2iu(5));
  }

  for (double y=y0; y<=y1+dy/2; y+=dy) {
    double yw = yax->map(y).y();
    p.drawLine(world.left()-pt2iu(2), yw, world.left()-pt2iu(5), yw);
    p.drawLine(world.right()+pt2iu(2), yw, world.right()+pt2iu(5), yw);
  }
  
  p.setPen("#666666");
  QFont f("Helvetica");
  f.setPointSize(10/scale());
  p.setFont(f);

  double s = 1/scale();
  for (double x=x0; x<=x1+dx/2; x+=dx) {
    double xw = xax->map(x).x();
    p.drawText(QRectF(xw-200*s, world.top()-50*s,
		      400*s, 50*s),
	       Qt::AlignHCenter | Qt::AlignBottom,
	       coordtext(x, dx));
    p.drawText(QRectF(xw-200*s, world.bottom(),
		      400*s, 50*s),
	       Qt::AlignCenter | Qt::AlignTop,
	       coordtext(x, dx));
  }
  
  for (double y=y0; y<=y1+dy/2; y+=dy) {
    double yw = yax->map(y).y();
    p.drawText(QRectF(world.left()-400*s, yw-20*s,
		      400*s, 40*s), 
	       Qt::AlignRight | Qt::AlignVCenter,
	       coordtext(y, dy) + "  ");
    p.drawText(QRectF(world.right(), yw-20*s,
		      400*s, 40*s),
	       Qt::AlignLeft | Qt::AlignVCenter,
	       "  " + coordtext(y, dy));
  }
  
  
  p.restore();
}

void QPWidget::renderMargin(QPainter &p) {
  p.save();
  QRectF world = fig->extent();
  if (margindecor==GRAY) {
    // draw background
    p.setBrush(QColor("white"));
    p.setPen(Qt::NoPen);
    p.drawRect(world);
  } else if (margindecor==CROP) {
    // draw crop marks
    p.setPen(QColor("black"));
    double yy[] = { world.top(), world.bottom() };
    double xx[] = { world.left(), world.right() };
    double dm = MARGPIX/scale();
    if (dm>.25*marg)
      dm = .25*marg;
    double ddm = .75*marg;
    for (int k=0; k<2; k++) {
      double x = xx[k];
      double y = yy[0];
      p.drawLine(QPointF(x,y-ddm), QPointF(x,y-dm));
      y = yy[1];
      p.drawLine(QPointF(x,y+ddm), QPointF(x,y+dm));
      y = yy[k];
      x = xx[0];
      p.drawLine(QPointF(x-ddm,y), QPointF(x-dm,y));
      x = xx[1];
      p.drawLine(QPointF(x+ddm,y), QPointF(x+dm,y));
    }
  }
  p.restore();
}  

void QPWidget::mousePressEvent(QMouseEvent *e) {
  ScrollWidget::mousePressEvent(e);
  if (fig) {
    QPointF xy = e->pos();
    QPointF world = (xy-tlDest()) / scale() + topLeft();
    trackpanel = fig->panelAt(world);
    reportTrack(xy, e->button(), "press");
  }
}

void QPWidget::keyPressEvent(QKeyEvent *e) {
  switch (e->key()) {
  case Qt::Key_G:
    switch (margindecor) {
    case NONE:
      margindecor = CROP;
      break;
    case CROP:
      margindecor = GRAY;
      break;
    case GRAY:
      margindecor = NONE;
      break;
    }
    update();
    break;
  case Qt::Key_C:
    if (e->modifiers() & Qt::ControlModifier) {
      takeScreenShot();
    } else {
      setMouseTracking(!hasMouseTracking());
      if (hasMouseTracking())
	coord->show();
      else
	coord->hide();
    }
    break;
  case Qt::Key_R:
    setRuler(!hasRuler());
    break;
  case Qt::Key_B:
    if (fig)
      fig->showBoundingBoxes(!fig->areBoundingBoxesShown());
    update();
    break;
  default:
    ScrollWidget::keyPressEvent(e);
  }
}

void QPWidget::takeScreenShot() {
  if (!fig || !prog)
    return;

  QRect r0(QPoint(0,0), size());
  QRectF world = fig->extent();
  QPointF tld = tlDest();
  double s = scale();
  QPointF tlw = topLeft();
  world.translate(-tlw);
  world = QRectF(world.topLeft()*s, world.size()*s);
  world.translate(tld);
  QRectF r = r0;
  r &= world;
  QPixmap pm = grab(r.toRect());
  QClipboard *cb = QApplication::clipboard();
  cb->setPixmap(pm);
}

bool QPWidget::hasRuler() const {
  return ruler;
}

void QPWidget::setRuler(bool r) {
  if (r==ruler)
    return;
  ruler=r;
  update();
}

void QPWidget::setWindowTitle(QString t) {
  winttl = t;
  ScrollWidget::setWindowTitle(t);
}

void QPWidget::resizeEvent(QResizeEvent *e) {
  ScrollWidget::resizeEvent(e);
  coord->resize(width()/2, 24);
  coord->move(5, height() - coord->height() - 5);
}


void QPWidget::mouseMoveEvent(QMouseEvent *e) {
  ScrollWidget::mouseMoveEvent(e);
  reportTrack(e->pos(), e->buttons(), "move");
}

void QPWidget::mouseReleaseEvent(QMouseEvent *e) {
  ScrollWidget::mouseReleaseEvent(e);
  reportTrack(e->pos(), e->button(), "release");
}

void QPWidget::mouseDoubleClickEvent(QMouseEvent *e) {
  ScrollWidget::mouseDoubleClickEvent(e);
  reportTrack(e->pos(), e->button(), "double");
}

void QPWidget::closeEvent(QCloseEvent *e) {
  ScrollWidget::closeEvent(e);
}

Axis *QPWidget::findXAxis() {
  if (trackpanel == fig->currentPanelName())
    return &fig->xAxis();
  else
    return &fig->panelRef(trackpanel).xaxis;
}

Axis *QPWidget::findYAxis() {
  if (trackpanel == fig->currentPanelName())
    return &fig->yAxis();
  else
    return &fig->panelRef(trackpanel).yaxis;
}

void QPWidget::reportTrack(QPointF xy, int button, QString what) {
  if (!fig)
    return;
  QPointF world = (xy-tlDest()) / scale() + topLeft();
  Axis *xax = findXAxis();
  Axis *yax = findYAxis();
  
  QString x = coordtext(xax->rev(world), xax->min(), xax->max());
  QString y = coordtext(yax->rev(world), yax->min(), yax->max());
  QRectF we = extent();
  if (world.x()<we.left()+marg || world.x()>we.right()-marg)
    x = QString::fromUtf8("–");
  if (world.y()<we.top()+marg || world.y()>we.bottom()-marg)
    y = QString::fromUtf8("–");

  QString c = QString("(%1, %2)").arg(x).arg(y);
  if (trackpanel != "-")
    c = "[" + trackpanel + "] " + c;
  coord->setText(c);
  if (button || what!="move")
    feedback(QString("%1 %2 %3 %4 %5").
	     arg(what).arg(trackpanel).arg(x).arg(y).arg(button));
}

void QPWidget::feedback(QString s) {
  std::cout << s.toUtf8().data() << "\n";
  std::cout.flush();
}
