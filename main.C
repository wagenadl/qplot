// main.C

#include <QApplication>
#include <QWidget>
#include <QDebug>
#include <QImage>
#include <QFile>
#include <QPrinter>
#include <QSvgGenerator>
//#include <QTemporaryFile>
//#include <QProcess>
#include <stdio.h>
#include "Program.H"
#include "Figure.H"
#include "Command.H"
#include "QPWidget.H"
#include "Watcher.H"
#include "Error.H"

int error(QString const &s) {
  Error() << s;
  return 1;
}

int usage(int ex=1) {
  Error() << "Usage: qplot   input.txt";
  Error() << "       qplot   input.txt output.pdf|svg|png";
  return ex;
}

void prerender(Program &prog, Figure &fig) {
  QImage img(1,1,QImage::Format_ARGB32);
  fig.setSize(QSizeF(800, 600));
  fig.painter().begin(&img);
  QRectF dataExtent = prog.dataRange();
  fig.xAxis().setDataRange(dataExtent.left(), dataExtent.right());
  fig.yAxis().setDataRange(dataExtent.top(), dataExtent.bottom());
  prog.render(fig, true); // render to determine paper bbox & fudge
  prog.render(fig, true); // render to determine paper bbox & fudge
  fig.painter().end();
}

int read(Program &prog, QString ifn) {
  QFile f(ifn);
  if (f.open(QIODevice::ReadOnly)) {
    QTextStream ts(&f);
    if (prog.read(ts, ifn))
      return 0;
    Error() << "Interpretation failed";
  } else {
    Error() << "Cannot open file";
  }
  return 1;
}  

int interactive(QString ifn, QApplication *app, bool gray=false) {
  Program prog;
  read(prog, ifn);
  Figure fig;
  prerender(prog, fig);

  Watcher wtch(ifn, &prog, &fig);
  QPWidget win;
  QObject::connect(&wtch, SIGNAL(ping()), &win, SLOT(update()));
  win.setContents(&fig, &prog);
  win.setMargin(20,gray);
  win.show();
  return app->exec();
}

int noninteractive(QString ifn, QString ofn) {
  Program prog;
  if (ifn.isEmpty()) {
    QTextStream ts(stdin);
    if (!prog.read(ts, "<stdin>")) {
      Error() << "Interpretation error";
      return 1;
    }
  } else {
    read(prog, ifn);
  }
  Figure fig;
  prerender(prog, fig);

  int idx = ofn.lastIndexOf(".");
  if (idx<0)
    return error("Output file must have an extension");
  QString extn = ofn.mid(idx+1);
  if (extn == "svg") {
    QSvgGenerator img;
    img.setFileName(ofn);
    img.setResolution(72);
    img.setViewBox(QRectF(QPointF(0,0),fig.extent().size()));
    fig.painter().begin(&img);    
    fig.painter().translate(-fig.extent().left(), -fig.extent().top());
    prog.render(fig);
    fig.painter().end();
  } else if (extn == "pdf") {
    QPrinter img(QPrinter::HighResolution);
    img.setPageMargins(0, 0, 0, 0, QPrinter::Point);
    img.setPaperSize(fig.extent().size(), QPrinter::Point);
    img.setResolution(72*20);
    img.setOutputFileName(ofn);
    fig.painter().begin(&img);
    fig.painter().scale(20, 20);
    fig.painter().translate(-fig.extent().left(), -fig.extent().top());
    prog.render(fig);
    fig.painter().end();
  } else {
    QImage img(int(fig.extent().width()),
	       int(fig.extent().height()),
	       QImage::Format_ARGB32);
    img.fill(0xffffffff);
    fig.painter().begin(&img);
    fig.painter().translate(-fig.extent().left(), -fig.extent().top());
    prog.render(fig);
    fig.painter().end();
    img.save(ofn);
  }
  return 0;
}  

int main(int argc, char **argv) {
  QApplication app(argc, argv);

  if (argc<2 || argc>3)
    return usage();
  if (argc==2) {
    QString ifn = argv[1];
    if (ifn=="-h" || ifn=="--help")
      return usage(0);
    else
      return interactive(ifn, &app);
  } else /* argc==3 */ {
    if (QString(argv[1])=="-gray")
      return interactive(argv[2], &app, true);
    else
      return noninteractive(argv[1], argv[2]);
  } 
}
