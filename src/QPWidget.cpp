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
#include <QSpacerItem>
#include <QGridLayout>
#include <QScreen>
#include <QKeyEvent>
#include <QLabel>
#include <QIcon>
#include <math.h>
#include <QApplication>
#include <QClipboard>
#include <iostream>
#include <QFont>
#include <QFontMetrics>
#include <QMenu>
#include <QAction>
#include <QMessageBox>
#include "config.h"


#define MARGPIX 15


QPWidget::QPWidget(QWidget *parent): ScrollWidget(parent) {
  brandnew = true;
  fig=0;
  prog=0;
  marg = 20;
  showcropmarks = false;
  graymargin = false;
  prepCoord();
  showcoords = true;
  trackpanel = "-";
  ruler = false;
  pickCursor();
  setMouseTracking(true);
  showmenu = true;
  placeMenuButton();
}

QPWidget::~QPWidget() {
}

void QPWidget::prepCoord() {
  coord = new QLabel(this);
  coord->hide();
  QFont f = font();
  f.setPointSize(14);
  coord->setFont(f);
  QFontMetrics fm(f);
  QRect r = fm.boundingRect("AZ09");
  //  coord->resize(width()/2, r.height() + 5);
  //  coord->move(5, height() - coord->height() - 5);
  coord->setAutoFillBackground(true);
  QPalette p = coord->palette();
  p.setColor(QPalette::Window, QColor(255, 255, 255, 200));
  coord->setMargin(5);
  coord->setPalette(p);
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

void QPWidget::clickMenu() {
  QMenu menu;

  QAction about{"&About QPlot…"};
  menu.addAction(&about);

  QMenu showhide("&Show/hide");
  QAction coordinates{"&Coordinates"};
  coordinates.setShortcut(Qt::Key_C);
  coordinates.setCheckable(true);
  coordinates.setChecked(showcoords);
  showhide.addAction(&coordinates);

  QAction margin{"&Gray margin"};
  margin.setShortcut(Qt::Key_G);
  margin.setCheckable(true);
  margin.setChecked(graymargin);
  showhide.addAction(&margin);
  
  QAction crops{"Crop &marks"};
  crops.setShortcut(Qt::Key_M);
  crops.setCheckable(true);
  crops.setChecked(showcropmarks);
  showhide.addAction(&crops);

  QAction ruler{"&Rulers"};
  ruler.setShortcut(Qt::Key_R);
  ruler.setCheckable(true);
  ruler.setChecked(hasRuler());
  showhide.addAction(&ruler);

  QAction boxes{"&Boxes (debug)"};
  boxes.setShortcut(Qt::Key_B);
  boxes.setCheckable(true);
  boxes.setChecked(fig->areBoundingBoxesShown());
  showhide.addAction(&boxes);
  
  menu.addMenu(&showhide);

  QAction shot({"Screensho&t"});
  shot.setShortcut(Qt::CTRL + Qt::Key_C);
  menu.addAction(&shot);
  
  QAction close{"&Close"};
  menu.addAction(&close);

  menu.move(QCursor::pos(screen()));
  QAction *act = menu.exec();

  if (act==&shot) {
    takeScreenShot();
  } else if (act==&about) {
    aboutAction();
  } else if (act==&close) {
    this->close();
  } else if (act==&margin) {
    graymargin = margin.isChecked();
    update();
  } else if (act==&crops) {
    showcropmarks = crops.isChecked();
    update();
  } else if (act==&ruler) {
    setRuler(ruler.isChecked());
  } else if (act==&boxes) {
    fig->showBoundingBoxes(boxes.isChecked());
  } else if (act==&coordinates) {
    showcoords = coordinates.isChecked();
    update(); // this doesn't actually do it
  }  
}

void QPWidget::paintMenuButton() {
  QPainter p(this);
  float dpi = screen()->logicalDotsPerInch();
  p.setPen(QPen(QColor(100, 100, 100), 2 * dpi/96));
  int w = menurect.width();
  int h = menurect.height();
  int x0 = menurect.left() + w / 4;
  int y0 = menurect.top() + h / 2;
  w = w/2;
  int dy = h / 4;
  for (int k=-1; k<=1; k++)
    p.drawLine(x0, y0 + k*dy, x0+w, y0 + k*dy);
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
  p.setRenderHint(QPainter::Antialiasing);
  p.setRenderHint(QPainter::TextAntialiasing);

  p.setBrush(graymargin ? QColor(200, 200, 200) : QColor("white"));
  p.setPen(Qt::NoPen);
  p.drawRect(rect());
  
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

  if (showmenu)
    paintMenuButton();
 
}

static QString coordtext(double x, double dx) {
  // represents X so that a difference of DX is clear.
  if (x == 0)
    return "0";
  if (dx <= 0)
    return QString::fromUtf8("—");
  int k = floor(log(dx)/log(10));
  if (k <= 0)
    return QString("%1").arg(x, 0, 'f', -k).replace("-", "−");
  int l = floor(log(abs(x))/log(10));
  // I will show l-k digits, with exponentiation (XXXeN where N is l).
  // I could also show just l digits. If that is more compact, I will do it.
  if (l < l-k + 2)
    return QString("%1").arg(x, 0, 'f', 0);
  k = l-k+1;
  if (k<1)
    k=1;
  return QString("%1").arg(x, 0, 'e', k).replace("-", "−");
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
  if (trackpanel=="")
    return;
  
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

  p.setPen(QPen(QColor(0,0,0), 1/scale()));

  //double ytop_near = world.top() - pt2iu(1);
  //double ytop_far = world.top() - pt2iu(4);
  double ytop_text = world.top() - pt2iu(1);
  //double ybot_near = world.bottom() + pt2iu(1);
  //double ybot_far = world.bottom() + pt2iu(4);
  double ybot_text = world.bottom() + pt2iu(1);
  //for (double x=x0; x<=x1+dx/2; x+=dx) {
  //  double xw = xax->map(x).x();
  //  p.drawLine(xw, ytop_near, xw, ytop_far);
  //  p.drawLine(xw, ybot_near, xw, ybot_far);
  //}

  //double xleft_near = world.left() - pt2iu(1);
  //double xleft_far = world.left() - pt2iu(4);
  double xleft_text = world.left() - pt2iu(1);
  //double xright_near = world.right() + pt2iu(1);
  //double xright_far = world.right() + pt2iu(4);
  double xright_text = world.right() + pt2iu(1);
  //for (double y=y0; y<=y1+dy/2; y+=dy) {
  //  double yw = yax->map(y).y();
  //  p.drawLine(xleft_near, yw, xleft_far, yw);
  //  p.drawLine(xright_near, yw, xright_far, yw);
  //}
  
  //  p.setPen("#666666");
  QFont f("Helvetica");
  f.setPointSize(12 / scale());
  p.setFont(f);

  double s = 1/scale();
  for (double x=x0; x<=x1+dx/2; x+=dx) {
    double xw = xax->map(x).x();
    QString txt = coordtext(x, dx);
    p.drawText(QRectF(xw - 200*s, ytop_text - 50*s, 400*s, 50*s),
	       Qt::AlignHCenter | Qt::AlignBottom,
               txt);
    p.drawText(QRectF(xw - 200*s, ybot_text, 400*s, 100*s),
	       Qt::AlignHCenter | Qt::AlignTop,
               txt);
  }
  
  for (double y=y0; y<=y1+dy/2; y+=dy) {
    double yw = yax->map(y).y();
    QString txt = coordtext(y, dy);
    p.drawText(QRectF(xleft_text - 400*s, yw - 20*s, 400*s, 40*s),
	       Qt::AlignRight | Qt::AlignVCenter,
	       txt);
    p.drawText(QRectF(xright_text, yw - 20*s, 400*s, 40*s),
	       Qt::AlignLeft | Qt::AlignVCenter,
	       txt);
  }
  
  p.restore();
}

void QPWidget::renderMargin(QPainter &p) {
  p.save();
  if (graymargin) {
    p.setBrush(QColor("white"));
    p.setPen(Qt::NoPen);
    p.drawRect(fig->extent());
  }
  if (showcropmarks)
    drawCropMarks(p);
  p.restore();
}

void QPWidget::drawCropMarks(QPainter &p) {
  QRectF world = fig->extent();
  float dpi = screen()->logicalDotsPerInch();
  p.setPen(QPen(QColor("black"), 1 * dpi/96 / scale()));
  double yy[]{ world.top(), world.bottom() };
  double xx[]{ world.left(), world.right() };
  double dm = MARGPIX / scale();
  if (dm > .25 * marg)
    dm = .25 * marg;
  double ddm = .75 * marg;
  for (int k=0; k<2; k++) {
    double x = xx[k];
    double y = yy[0];
    p.drawLine(QPointF(x, y - ddm), QPointF(x, y - dm));
    y = yy[1];
    p.drawLine(QPointF(x, y + ddm), QPointF(x, y + dm));
    y = yy[k];
    x = xx[0];
    p.drawLine(QPointF(x - ddm, y), QPointF(x - dm, y));
    x = xx[1];
    p.drawLine(QPointF(x + ddm, y), QPointF(x + dm, y));
  }
}  

void QPWidget::mousePressEvent(QMouseEvent *e) {
  if (menurect.contains(e->pos())) {
    clickMenu();
    return;
  }
      
  ScrollWidget::mousePressEvent(e);
  if (fig) {
    QPointF xy = e->pos();
    QPointF world = (xy-tlDest()) / scale() + topLeft();
    QString tp = fig->panelAt(world);
    if (tp != trackpanel)
      if (ruler)
        update();
    trackpanel = tp;
    pickCursor();
    reportTrack(xy, e->button(), "press");
  }
}

void QPWidget::keyPressEvent(QKeyEvent *e) {
  switch (e->key()) {
  case Qt::Key_G:
    graymargin = !graymargin;
    update();
    break;
  case Qt::Key_M:
    showcropmarks = !showcropmarks;
    update();
    break;
  case Qt::Key_C:
    if (e->modifiers() & Qt::ControlModifier) {
      takeScreenShot();
    } else {
      showcoords = !showcoords;
      pickCursor();
      reportTrack(mapFromGlobal(QCursor::pos(screen())), 0, "move");
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

  bool coordseen = showcoords;
  bool menuseen = showmenu;
  showmenu = false;
  coord->hide();
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
  if (coordseen)
    coord->show();
  if (menuseen)
    showmenu = true;
}

bool QPWidget::hasRuler() const {
  return ruler;
}

void QPWidget::setRuler(bool r) {
  if (r == ruler)
    return;
  ruler = r;
  update();
}

void QPWidget::setWindowTitle(QString t) {
  winttl = t;
  ScrollWidget::setWindowTitle(t);
}

void QPWidget::placeMenuButton() {
  float dpi = screen()->logicalDotsPerInch();
  int w = 24 * dpi / 96;
  int h = 20 * dpi / 96;
  menurect = QRect(0, 0, w, h); // QRect(width() - w, 0, w, h);
}

void QPWidget::resizeEvent(QResizeEvent *e) {
  ScrollWidget::resizeEvent(e);
  //coord->resize(width()/2, 24);
  //coord->move(5, height() - coord->height() - 5);
  placeMenuButton();
}


void QPWidget::mouseMoveEvent(QMouseEvent *e) {
  ScrollWidget::mouseMoveEvent(e);
  if (fig) {
    QPointF xy = e->pos();
    if (e->buttons() == 0) {
      QPointF world = (xy-tlDest()) / scale() + topLeft();
      QString tp = fig->panelAt(world);
      if (tp != trackpanel) {
        trackpanel = tp;
        pickCursor();
        if (ruler)
          update();
      }
    }
    reportTrack(xy, e->button(), "move");
  }
}

void QPWidget::pickCursor() {
  if (trackpanel=="") {
    setCursor(Qt::ArrowCursor);
    setRequireControl(true);
  } else if (showcoords && !isDragging()) {
    setCursor(Qt::CrossCursor);
    setRequireControl(true);
  } else {
    setCursor(Qt::OpenHandCursor);
    setRequireControl(false);
  }
}

void QPWidget::mouseReleaseEvent(QMouseEvent *e) {
  ScrollWidget::mouseReleaseEvent(e);
  pickCursor();
    
  if (fig)
    reportTrack(e->pos(), e->button(), "release");
}

void QPWidget::mouseDoubleClickEvent(QMouseEvent *e) {
  ScrollWidget::mouseDoubleClickEvent(e);
  if (fig) 
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
  if (!fig || trackpanel=="" || !showcoords) {
    coord->hide();
    return;
  }

  QPointF world = (xy - tlDest()) / scale() + topLeft();
  QRectF we = extent();

  Axis *xax = findXAxis();
  Axis *yax = findYAxis();
  QString x = coordtext(xax->rev(world), xax->min(), xax->max());
  QString y = coordtext(yax->rev(world), yax->min(), yax->max());
  
  QString c = QString("(%1, %2)").arg(x).arg(y);
  c.replace("-", "−"); // proper minus sign
  QString tptxt = "";
  if (trackpanel != "-")
    tptxt = "[" + trackpanel + "] ";
  if (trackpanel.length()==2) {
    // simple subplots, interpret pyqplot's AA style naming
    int row = trackpanel[0].unicode() - 'A';
    int col = trackpanel[1].unicode() - 'A';
    if (row >= 0 && row <= 26 && col>=0 && col <= 26)
      tptxt = QString("[%1,%2] ").arg(row).arg(col);
  }
  coord->setText(c);
  coord->resize(coord->sizeHint());
  int xc = xy.x() + 10;
  if (xc + coord->width() > width() - 5)
    xc = xy.x() - coord->width() - 10;
  int yc = xy.y() + 10;
  if (yc + coord->height() > height() - 5)
    yc = xy.y() - coord->height() - 10;
  coord->move(xc, yc);
  coord->show();
  
  if (button || what != "move")
    feedback(QString("%1 %2 %3 %4 %5").
	     arg(what).arg(trackpanel).arg(x).arg(y).arg(button));
}

void QPWidget::feedback(QString s) {
  std::cout << s.toUtf8().data() << "\n";
  std::cout.flush();
}

void QPWidget::leaveEvent(QEvent *e) {
  ScrollWidget::leaveEvent(e);
  coord->hide();
}

void QPWidget::aboutAction() {
  QString msg = "<b>QPlot</b> ";
  msg += QPLOT_VERSION;
  msg += "<br>";
  msg += "(C) 2013–2024  Daniel A. Wagenaar<br><br>";
  msg +=
    "<b>QPlot</b> is is an alternative 2D plotting library for"
    " Python, Matlab, and Octave that facilitates beautiful typography"
    " and precise axis scaling.<br>"
    "<br>"
    "<b>QPlot</b> is free software: you can redistribute it and/or"
    " modify it under the terms of the GNU General Public License as"
    " published by the Free Software Foundation, either version 3 of"
    " the License, or (at your option) any later"
    " version.<br>"
    "<br>"
    "<b>QPlot</b> is distributed in the hope"
    " that it will be useful, but WITHOUT ANY WARRANTY; without even"
    " the implied warranty of MERCHANTABILITY or FITNESS FOR A"
    " PARTICULAR PURPOSE. See the GNU General Public License for"
    " more details.<br>"
    "<br>"
    "You should have received a copy of the GNU"
    " General Public License along with this program. If not, see <a"
    " href=\"http://www.gnu.org/licenses/gpl-3.0.en.html\">www.gnu.org/licenses/gpl-3.0.en.html</a>.";
  
  QMessageBox box;
  box.setWindowTitle("About QPlot");
  box.setTextFormat(Qt::RichText);
  box.setText(msg);
  float dpi = screen()->logicalDotsPerInch();
  int iconwidth = 128 * dpi / 96;
  box.setIconPixmap(QPixmap(":qplot.png")
                    .scaled(QSize(iconwidth, iconwidth),
                            Qt::KeepAspectRatio,
                            Qt::SmoothTransformation));
  QGridLayout *layout = dynamic_cast<QGridLayout *>(box.layout());
  if (layout) 
    layout->addItem(new QSpacerItem(8*dpi, 0,
                                    QSizePolicy::Fixed,
                                    QSizePolicy::Expanding),
                    layout->rowCount(), 0, 1, layout->columnCount());
  box.exec();
}
