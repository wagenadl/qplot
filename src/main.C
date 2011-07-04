// main.C

#include <QApplication>
#include <QWidget>
#include <QDebug>
#include <QImage>
#include <QFile>
#include <QPrinter>
#include <QSvgGenerator>
#include <QFileInfo>

#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

#include "Program.H"
#include "Figure.H"
#include "Command.H"
#include "QPWidget.H"
#include "Watcher.H"
#include "Error.H"
#include "Factor.H"

int error(QString const &s) {
  Error() << s;
  return 1;
}

int usage(int ex=1) {
  Error() << "Usage: qplot   input.txt";
  Error() << "       qplot   input.txt output.pdf|svg|png|.ps";
  return ex;
}

void prerender(Program &prog, Figure &fig) {
  QImage img(1,1,QImage::Format_ARGB32);
  fig.setSize(QSizeF(1, 1)); // this may be overridden later
  fig.painter().begin(&img);
  //fig.painter().scale(iu2pt(), iu2pt());
  fig.reset();
  foreach (QString p, prog.panels()) {
    QRectF dataExtent = prog.dataRange(p);
    //qDebug() << "1" << p << dataExtent;
    if (p=="-") {
      //qDebug() << "xax";
      fig.xAxis().setDataRange(dataExtent.left(), dataExtent.right());
      //qDebug() << "yax";
      fig.yAxis().setDataRange(dataExtent.top(), dataExtent.bottom());
    } else {
      fig.panelRef(p).xaxis.setDataRange(dataExtent.left(), dataExtent.right());
      fig.panelRef(p).yaxis.setDataRange(dataExtent.top(), dataExtent.bottom());
    }
  }
  prog.render(fig, true); // render to determine paper bbox & fudge
  //qDebug() << "2" << prog.dataRange() << fig.xAxis().min() << fig.xAxis().max();
  prog.render(fig, true); // render to determine paper bbox & fudge
  //qDebug() << "3" << prog.dataRange() << fig.xAxis().minp() << fig.xAxis().maxp();
  fig.painter().end();
}

int read(Program &prog, QString ifn) {
  QFile f(ifn);
  if (f.open(QIODevice::ReadOnly)) {
    //QTextStream ts(&f);
    if (prog.read(f, ifn))
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
  int idx = ifn.lastIndexOf('/');
  win.setWindowTitle("qplot: " + ((idx>=0) ? ifn.mid(idx+1) : ifn));
  QObject::connect(&wtch, SIGNAL(ping()), &win, SLOT(raise()));
  QObject::connect(&wtch, SIGNAL(ping()), &win, SLOT(update()));
  win.setContents(&fig, &prog);
  win.setMargin(pt2iu(20), gray);
  win.show();
  win.autoSize();
  wtch.reread(true);
  QFileInfo fi(ifn);
  QString path = fi.path();
  QString leaf = fi.fileName();
  QFile pidfile(path + "/.qp-" + leaf + ".pid");
  pidfile.open(QIODevice::WriteOnly);
  char pid[100];
  snprintf(pid, 100, "%i\n", getpid());
  pidfile.write(pid, strlen(pid));
  pidfile.close();
  int r = app->exec();
  pidfile.remove();
  return r;
}

int noninteractive(QString ifn, QString ofn) {
  Program prog;
  if (ifn.isEmpty()) {
    //QTextStream ts(stdin);
    QFile f; f.open(stdin,QFile::ReadOnly);
    if (!prog.read(f, "<stdin>")) {
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
    img.setResolution(90); // anything else seems to be poorly supported
    img.setViewBox(QRectF(QPointF(0,0),
			  QSizeF(90./72*iu2pt(fig.extent().width()),
				 90./72*iu2pt(fig.extent().height()))));
    fig.painter().begin(&img);
    fig.painter().scale(90./72*iu2pt(), 90./72*iu2pt());
    fig.painter().translate(-iu2pt(fig.extent().left()),
			    -iu2pt(fig.extent().top()));
    prog.render(fig);
    fig.painter().end();
  } else if (extn == "eps") {
    return error("Writing to eps is not supported");
  } else if (extn == "pdf") {
    QPrinter img(QPrinter::ScreenResolution);
    img.setResolution(72);
    img.setPageMargins(0, 0, 0, 0, QPrinter::Point);
    img.setPaperSize(QSizeF(iu2pt(fig.extent().width()),
			    iu2pt(fig.extent().height())),
		     QPrinter::Point);
    img.setOutputFileName(ofn);
    fig.painter().begin(&img);
    fig.painter().scale(iu2pt(), iu2pt());
    fig.painter().translate(-iu2pt(fig.extent().left()),
			    -iu2pt(fig.extent().top()));
    prog.render(fig);
    fig.painter().end();
  } else if (extn=="ps") {
    QSizeF p = papersize();
    QPrinter img(QPrinter::ScreenResolution);
    img.setResolution(72);
    QSizeF imsize(QSizeF(iu2pt(fig.extent().width()),
			 iu2pt(fig.extent().height()))),
    img.setOutputFileName(ofn);
    fig.painter().begin(&img);
    fig.painter().translate((p.width()-imsize.width())/2,
			    (p.height()-imsize.height())/2);
    /* Draw some crop marks? */
    fig.painter().scale(iu2pt(), iu2pt());
    fig.painter().translate(-fig.extent().left(),
			    -fig.extent().top());
    prog.render(fig);
    fig.painter().end();
  } else if (extn=="png" || extn=="jpg" || extn=="tif" || extn=="tiff") {
    QImage img(int(fig.extent().width()),
	       int(fig.extent().height()),
	       QImage::Format_ARGB32);
    img.fill(0xffffffff);
    fig.painter().begin(&img);
    fig.painter().scale(iu2pt(), iu2pt());
    fig.painter().translate(-iu2pt(fig.extent().left()),
			    -iu2pt(fig.extent().top()));
    prog.render(fig);
    fig.painter().end();
    if (!img.save(ofn))
      return error("Failed to save.");
  } else {
    return error("Unknown extension.");
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
