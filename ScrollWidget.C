// ScrollWidget.C

#include "ScrollWidget.H"
#include <QMouseEvent>
#include <QKeyEvent>
#include <QDebug>

ScrollWidget::ScrollWidget(QWidget *parent): QWidget(parent) {
  extent_world = QRectF(QPointF(0,0), QPointF(1000,1000));
  tl_world = QPointF(0,0);
  scalefactor = 1;
  scaletofit = true;
}

ScrollWidget::~ScrollWidget() {
}

void ScrollWidget::setExtent(QRectF const &e) {
  extent_world = e;
  sureScale();
}

void ScrollWidget::scaleToFit() {
  scaletofit = true;
  update();
}

void ScrollWidget::setTopLeft(QPointF tl) {
  tl_world = tl;
  scaletofit = false;
  update();
}

void ScrollWidget::setScale(double factor) {
  scalefactor = factor;
  scaletofit = false;
  sureScale();
}

void ScrollWidget::autoSize() {
  if (scaletofit)
    return;
  tl_world = extent_world.topLeft();
  QSizeF s = extent_world.size();
  s *= scalefactor;
  resize(s.toSize());
  update();
}

QRectF const &ScrollWidget::extent() const {
  return extent_world;
}

QPointF const &ScrollWidget::topLeft() const {
  return tl_world;
}

double ScrollWidget::scale() const {
  return scaletofit ? perfectScale() : scalefactor;
}    

void ScrollWidget::mousePressEvent(QMouseEvent *e) {
  pos_press = e->pos();
  tl_press = tl_world;
}

void ScrollWidget::mouseMoveEvent(QMouseEvent *e) {
  QPointF pos_now = e->pos();
  tl_world = tl_press - (pos_now - pos_press)/scale();
  surePan();
}

void ScrollWidget::keyPressEvent(QKeyEvent *e) {
  switch (e->key()) {
  case Qt::Key_Plus: case Qt::Key_Equal:
    if (e->modifiers() & Qt::AltModifier)
      setScale(1.05*scale());
    else if (e->modifiers() & Qt::ShiftModifier)
      setScale(2*scale());
    else
      setScale(1.2*scale());
    break;
  case Qt::Key_Minus: case Qt::Key_Underscore:
    if (e->modifiers() & Qt::AltModifier)
      setScale(scale()/1.05);
    else if (e->modifiers() & Qt::ShiftModifier)
      setScale(scale()/2);
    else
      setScale(scale()/1.2);
    break;
  case Qt::Key_1:
    setScale(1);
    break;
  case Qt::Key_0:
    scaleToFit();
    break;
  case Qt::Key_E:
    autoSize();
    break;
  case Qt::Key_Q:
    close();
    break;
  }
  
}

double ScrollWidget::perfectScale() const {
  QSizeF viewsize = QSizeF(size());
  QSizeF worldsize = extent_world.size();
  double sx = viewsize.width()/worldsize.width();
  double sy = viewsize.height()/worldsize.height();
  return sx<sy ? sx : sy;
}
 
      
void ScrollWidget::sureScale() {
  //  double s = perfectScale();
  if (scalefactor<.01)
    scalefactor = .01;
  else if (scalefactor>100)
    scalefactor = 100;
  surePan();
}

void ScrollWidget::surePan() {
  QSizeF viewsize = QSizeF(size())/scale();
  QPointF br_now = tl_world + QPointF(viewsize.width(), viewsize.height());

  if (br_now.x() >= extent_world.right())
    tl_world.setX(extent_world.right() - viewsize.width());
  if (br_now.y() >= extent_world.bottom())
    tl_world.setY(extent_world.bottom() - viewsize.height());
  if (tl_world.x() < extent_world.left())
    tl_world.setX(extent_world.left());
  if (tl_world.y() < extent_world.top())
    tl_world.setY(extent_world.top());

  update();
}

QPointF ScrollWidget::tlDest() const {
  QSizeF ws = extent_world.size() * scale();
  double x = (width() - ws.width())/2;
  double y = (height() - ws.height())/2;
  return QPointF(x>0 ? x : 0, y>0 ? y : 0);
}
