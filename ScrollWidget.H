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
