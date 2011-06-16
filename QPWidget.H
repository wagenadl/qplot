// QPWidget.H

#ifndef QPWIDGET_H

#define QPWIDGET_H

#include <QWidget>
#include "Figure.H"
#include "Program.H"

class QPWidget: public QWidget {
  Q_OBJECT;
public:
  QPWidget(QWidget *parent=0);
  ~QPWidget();
  void setContents(Figure *f, Program *p);
  void autoSize();
  void setPan(QPointF tl);
  void setZoom(double factor);
  void scaleToFit();
  virtual void paintEvent(QPaintEvent *);
private:
  bool scaletofit;
  double scalefactor;
  QPointF panorigin;

  Figure *fig;
  Program *prog;
};

#endif
