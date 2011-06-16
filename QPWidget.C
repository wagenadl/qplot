// QPWidget.C

#include "QPWidget.H"

QPWidget::QPWidget(QWidget *parent): QWidget(parent) {
  fig=0;
  prog=0;
  scaletofit = true;
  scalefactor = 1;
  panorigin = QPointF(0,0);
}

QPWidget::~QPWidget() {
}

void QPWidget::setContents(Figure *f, Program *p) {
  fig = f;
  prog = p;
  update();
}

void QPWidget::scaleToFit() {
  scaletofit = true;
  update();
}

void QPWidget::setPan(QPointF tl) {
  panorigin = tl;
  scaletofit = false;
  update();
}

void QPWidget::setZoom(double factor) {
  scalefactor = factor;
  scaletofit = false;
  update();
}

void QPWidget::autoSize() {
  if (!fig)
    return;
  scaletofit = false;
  scalefactor = 1;
  panorigin = fig->extent().topLeft();
  resize(fig->extent().size().toSize());
  update();
}

void QPWidget::paintEvent(QPaintEvent *) {
  if (!fig || !prog)
    return;
  QPainter &p(fig->painter());
  p.begin(this);
  if (scaletofit) {
    double sx = width()/fig->extent().width();
    double sy = height()/fig->extent().height();
    double s = sx<sy ? sx : sy;
    p.scale(s,s);
    p.translate(-fig->extent().left(), -fig->extent().top());
  } else {
    p.scale(scalefactor, scalefactor);
    p.translate(-fig->extent().left()-panorigin.x(),
		-fig->extent().top()-panorigin.y());
  }

  prog->render(*fig);
  p.end();
}
