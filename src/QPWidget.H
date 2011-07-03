// QPWidget.H

#ifndef QPWIDGET_H

#define QPWIDGET_H

#include "ScrollWidget.H"
#include "Figure.H"
#include "Program.H"

class QPWidget: public ScrollWidget {
  Q_OBJECT;
public:
  QPWidget(QWidget *parent=0);
  ~QPWidget();
  void setContents(Figure *f, Program *p);
  void setMargin(double pix, bool gray);
protected:
  virtual void keyPressEvent(QKeyEvent *);
  virtual void paintEvent(QPaintEvent *);
private:
  Figure *fig;
  Program *prog;
  double marg;
  bool gray;
  QRectF worldextent;
};

#endif
