// QPWidget.C

#include "QPWidget.H"
#include <QDebug>
#include <QKeyEvent>

#define MARGPIX 10

QPWidget::QPWidget(QWidget *parent): ScrollWidget(parent) {
  fig=0;
  prog=0;
  marg = 20;
  gray = false;
}

QPWidget::~QPWidget() {
}

void QPWidget::setMargin(double m, bool g) {
  marg = m;
  gray = g;
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

  if (!gray) {
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
  if (gray) {
    // draw background
    p.setBrush(QColor("white"));
    p.setPen(Qt::NoPen);
    p.drawRect(world);
  } else {
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
    gray = !gray;
    update();
    break;
  default:
    ScrollWidget::keyPressEvent(e);
  }
}
