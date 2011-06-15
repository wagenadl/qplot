// main.C

#include <QApplication>
#include <QWidget>
#include <QDebug>
#include <QImage>
#include <stdio.h>
#include "Program.H"
#include "Figure.H"
#include "Command.H"

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
  f.painter().begin(&img);
  f.setAutoRange(true);
  prog.render(f, true); // render once to determine data ranges. This first time, fudge should be disabled, I think. But I don't have that figured out yet.
  f.setAutoRange(false);
  prog.render(f, true); // render again to determine paper bbox & fudge
  prog.render(f);
  img.save("foo.png");
}
