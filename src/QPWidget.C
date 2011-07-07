// QPWidget.C

#include "QPWidget.H"
#include <QDebug>
#include <QKeyEvent>
#include <QLabel>
#include <math.h>
#define MARGPIX 15

QPWidget::QPWidget(QWidget *parent): ScrollWidget(parent) {
  fig=0;
  prog=0;
  marg = 20;
  margindecor = NONE;
  coord = new QLabel(this);
  coord->hide();
  coord->resize(200,18);
  coord->move(5, height()-coord->height()-3);
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

  prog->render(*fig);
  p.end();
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
    setMouseTracking(!hasMouseTracking());
    qDebug() << hasMouseTracking();
    if (hasMouseTracking())
      coord->show();
    else
      coord->hide();
    break;
  default:
    ScrollWidget::keyPressEvent(e);
  }
}

void QPWidget::setWindowTitle(QString t) {
  winttl = t;
  ScrollWidget::setWindowTitle(t);
}

void QPWidget::resizeEvent(QResizeEvent *e) {
  ScrollWidget::resizeEvent(e);
  coord->move(5, height()-coord->height()-3);
}

static QString coordtext(double x, double x0, double x1) {
  double dx = 2e-3*(x1-x0);
  // represents X so that a difference of DX is clear.
  if (x==0)
    return 0;
  if (dx<=0)
    return QString::fromUtf8("–");
  int k = floor(log(dx)/log(10));
  if (k<=0)
    return QString("%1").arg(x, 0, 'f', -k);
  int l = floor(log(abs(x))/log(10));
  // I will show l-k digits, and e(l-k).
  // I could also show just l digits.
  if (l-k + 2 > l)
    return QString("%1").arg(x, 0, 'f', -k);
  k = l-k+1;
  if (k<1)
    k=1;
  return QString("%1").arg(x, 0, 'e', k);
}


void QPWidget::mouseMoveEvent(QMouseEvent *e) {
  ScrollWidget::mouseMoveEvent(e);
  if (e->buttons())
    return;
  if (!fig)
    return;

  QPointF xy = e->pos();
  QPointF world = (xy-tlDest()) / scale() + topLeft();
  QString pnl = fig->currentPanelName();
  QString x = coordtext(fig->xAxis().rev(world),
			fig->xAxis().min(), fig->xAxis().max());
  QString y = coordtext(fig->yAxis().rev(world),
			fig->yAxis().min(), fig->yAxis().max());
  QRectF we = extent();
  if (world.x()<we.left()+marg || world.x()>we.right()-marg)
    x = QString::fromUtf8("–");
  if (world.y()<we.top()+marg || world.y()>we.bottom()-marg)
    y = QString::fromUtf8("–");

  QString c = QString("(%1, %2)").arg(x).arg(y);
  if (pnl != "")
    c = "[" + pnl + "] " + c;
  coord->setText(c);
}
