// main.C

#include <QApplication>
#include <QWidget>
#include <QDebug>
#include <QImage>
#include <stdio.h>
#include "Program.H"
#include "Figure.H"
#include "Command.H"
#include "QPWidget.H"

int error(QString const &s) {
  qDebug() << s;
  return 1;
}

int main(int argc, char **argv) {
  QApplication app(argc, argv);
  QImage img(800, 600, QImage::Format_RGB32);
  img.fill(-1);

  QTextStream ts(stdin);
  Program prog;
  if (!prog.read(ts, "<stdin>"))
    return 1;

  Figure f;
  f.setSize(QSizeF(800, 600));
  f.painter().begin(&img);
  QRectF dataExtent = prog.dataRange();
  qDebug()<<dataExtent;
  f.xAxis().setDataRange(dataExtent.left(), dataExtent.right());
  f.yAxis().setDataRange(dataExtent.top(), dataExtent.bottom());
  qDebug()<<f.extent();
  qDebug()<<f.fullBBox();
  qDebug()<<f.xAxis().min() << f.xAxis().max() << f.xAxis().minp()<<f.xAxis().maxp();
  qDebug()<<f.yAxis().min() << f.yAxis().max() << f.yAxis().minp()<<f.yAxis().maxp();
  prog.render(f, true); // render to determine paper bbox & fudge
  prog.render(f);
  f.painter().end();
  img.save("foo.png");

  QPWidget w;
  w.setContents(&f,&prog);
  w.show();
  app.exec();
}
