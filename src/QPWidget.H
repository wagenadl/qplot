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
  virtual ~QPWidget();
  void setContents(Figure *f, Program *p);
  void setMargin(double pix);
  virtual void setWindowTitle(QString s);
protected:
  virtual void keyPressEvent(QKeyEvent *);
  virtual void paintEvent(QPaintEvent *);
  virtual void resizeEvent(QResizeEvent *);
  virtual void mouseMoveEvent(QMouseEvent *);
private:
  Figure *fig;
  Program *prog;
  double marg;
  enum MarginDecor {
    NONE,
    GRAY,
    CROP,
  } margindecor;
  QRectF worldextent;
  QString winttl;
  class QLabel *coord;
};

#endif
