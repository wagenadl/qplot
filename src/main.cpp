// main.cpp - This file is part of QPlot

/* QPlot - Publication quality 2D graphs with dual coordinate systems
   Copyright (C) 2014  Daniel Wagenaar
  
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
  
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
  
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// main.C

#include <QApplication>
#include <QWidget>
#include <QDebug>
#include <QImage>
#include <QFile>
#include <QDir>
#include <QPdfWriter>
#include <QSvgGenerator>
#include <QFileInfo>
#include <QTemporaryFile>
#include <QDateTime>
#include <QProcessEnvironment>
#include <QDebug>

#include <math.h>
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

double BITMAPRES = 300;
int BITMAPQUAL = 95;
double OVERRIDEWIDTH = 0;
double OVERRIDEHEIGHT = 0;

#define MAXTRIES_DEFAULT 100
int MAXTRIES = MAXTRIES_DEFAULT;

#undef QPLOT_POSTSCRIPT_SUPPORT

extern void setFACTOR(double); // in Factor.C

int error(QString const &s) {
  Error() << s;
  return 1;
}

int error_failtosave(QString const &fn) {
  if (fn.isEmpty())
    return error("Failed to save: no filename");
  QFileInfo fi(fn);
  QDir d(fi.dir());
  if (!d.exists())
    return error(QString::fromUtf8("Failed to save as “%1”: The folder “%2” does not exist.").arg(fn).arg(d.path()));
  else if (!QFileInfo(d.path()).isWritable())
    return error(QString::fromUtf8("Failed to save as “%1”: The folder “%2” is not writable.").arg(fn).arg(d.path()));
  else if (fi.exists() && !fi.isWritable()) 
    return error(QString::fromUtf8("Failed to save as “%1”: File exists and is not writable.").arg(fn));
  else
    return error(QString::fromUtf8("Failed to save as “%1”. (Reason unknown.)"));
}

int error_unknownextension(QString const &extn) {
  if (extn.isEmpty())
    return error("Failed to save: filename without an extension.");
  else
    return error(QString::fromUtf8("Failed to save. Unknown extension “") + extn
		 + QString::fromUtf8("”."));
}

int usage(int ex=1) {
  Error() << "Usage: qplot input.txt";
  Error() << "       qplot input.txt output.pdf|svg|ps";
  Error() << "       qplot [-rDPI] input.txt output.png|tif|jpg";
  Error() << "       qplot -wWIDTH -hHEIGHT ... overrides output size (pts)";
  Error() << "       qplot --maxtries N ... overrides max tries for shrink";
  Error() << "       qplot --autoraise ... automatically raises the window on update";
  Error() << "";
  Error() << "For noninteractive use, input.txt may be '-' for stdin, and";
  Error() << "output.EXT may be '-.EXT' for stdout.";

  return ex;
}

QSizeF papersize() {
  // right now, just return letter size:
  return QSizeF(8.5*72, 11*72);
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

  int iter = 0;
  while (iter<MAXTRIES) {
    //qDebug() << iter;
    prog.render(fig, true); // render to determine paper bbox & fudge
    if (fig.checkFudged()) {
      //qDebug() << "will reiterate";
    } else {
      //qDebug() << "won't reiterate";
      break;
    }
    iter++;
  } 
  //  qDebug() << "Hello world";
  if (MAXTRIES==MAXTRIES_DEFAULT) {
    if (iter>=MAXTRIES)
      Error() << "Shrink failed";
  } else {
    //qDebug() << "Iterations used: " << iter;
  }

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

static bool autoraise = false;

int interactive(QString ifn, QApplication *app) {
  if (ifn=="-")
    Error() << "Input may not be stdin for interactive use";
  
  Program prog;
  read(prog, ifn);
  Figure fig;
  fig.setHairline(0);
  prerender(prog, fig);

  QPWidget win;
  Watcher wtch(ifn, &prog, &fig, &win);
  int idx = ifn.lastIndexOf('/');
  win.setWindowTitle("qplot: " + ((idx>=0) ? ifn.mid(idx+1) : ifn));
  if (autoraise)
    QObject::connect(&wtch, SIGNAL(ping()), &win, SLOT(raise()));
  QObject::connect(&wtch, SIGNAL(ping()), &win, SLOT(update()));
  win.setContents(&fig, &prog);
  win.setMargin(pt2iu(20));
  win.show();
  win.autoSize();
  wtch.reread(true);
  QFileInfo fi(ifn);
  QString path = fi.path();
  QString leaf = fi.fileName();
  QFile pidfile(path + "/.qp-" + leaf + ".pid");
  QFile fbfile(path + "/.qp-" + leaf + ".fb");
  if (fbfile.exists())
    win.setFeedbackFile(fbfile.fileName());
  pidfile.open(QIODevice::WriteOnly);
  char pid[100];
  snprintf(pid, 100, "%i\n", getpid());
  pidfile.write(pid, strlen(pid));
  pidfile.close();
  int r = app->exec();
  pidfile.remove();
  return r;
}

bool renderSVG(Program &prog, Figure &fig, QString ofn) {
  QSvgGenerator img;
  img.setFileName(ofn);
  img.setResolution(90); // anything else seems to be poorly supported
  img.setViewBox(QRectF(QPointF(0,0),
			QSizeF(90./72*iu2pt(fig.extent().width()),
			       90./72*iu2pt(fig.extent().height()))));
  if (!fig.painter().begin(&img))
    return false;
  fig.painter().scale(90./72*iu2pt(), 90./72*iu2pt());
  fig.setDashScale(90./72*iu2pt());
  fig.painter().translate(fig.extent().left(),
			  fig.extent().top());
  prog.render(fig);
  fig.painter().end();
  return true;
}

bool renderPDF(Program &prog, Figure &fig, QString ofn) {
  QPdfWriter img(ofn);
  img.setPageSizeMM(QSizeF(iu2pt(fig.extent().width())*25.4/72,
			   iu2pt(fig.extent().height())*25.4/72));

  if (!fig.painter().begin(&img))
    return false;

  double dpix = img.logicalDpiX();
  double dpiy = img.logicalDpiY();

  fig.painter().translate(-10*dpix/72., -10*dpiy/72.);
  // I don't know why this translation is needed.

  fig.painter().scale(iu2pt()*dpix/72.0,
		      iu2pt()*dpix/72.0);
  fig.setDashScale(iu2pt()*sqrt(dpix*dpiy)/72.0);
  fig.painter().translate(-fig.extent().left(),
			  -fig.extent().top());
  prog.render(fig);
  fig.painter().end();
  return true;
}

#ifdef QPLOT_POSTSCRIPT_SUPPORT

bool renderPS(Program &prog, Figure &fig, QString ofn, QString ttl="") {
  QSizeF p = papersize();
  QPrinter img(QPrinter::ScreenResolution);
  img.setResolution(72);
  img.setPaperSize(p, QPrinter::Point);
  img.setPageMargins(0, 0, 0, 0, QPrinter::Point);
  QSizeF imsize(QSizeF(iu2pt(fig.extent().width()),
		       iu2pt(fig.extent().height())));
  img.setOutputFileName(ofn);
  img.setOutputFormat(QPrinter::PostScriptFormat);
  if (!fig.painter().begin(&img))
    return false;
  fig.painter().translate((p.width()-imsize.width())/2,
			  (p.height()-imsize.height())/2);

  /* Draw some crop marks */
  fig.painter().save();
  { QPen p; p.setWidth(.5); fig.painter().setPen(p); }
  const int MINX = 5;
  const int MAXX = 20;
  // tl
  fig.painter().drawLine(-MAXX,0,-MINX,0);
  fig.painter().drawLine(0,-MAXX,0,-MINX);
  // bl
  fig.painter().drawLine(-MAXX,imsize.height(),-MINX,imsize.height());
  fig.painter().drawLine(0,imsize.height()+MINX,0,imsize.height()+MAXX);
  // tr
  fig.painter().drawLine(imsize.width()+MINX,0,imsize.width()+MAXX,0);
  fig.painter().drawLine(imsize.width(),-MINX,imsize.width(),-MAXX);
  // tr
  fig.painter().drawLine(imsize.width()+MINX,imsize.height(),
			 imsize.width()+MAXX,imsize.height());
  fig.painter().drawLine(imsize.width(),imsize.height()+MINX,
			 imsize.width(),imsize.height()+MAXX);
  // render title
  fig.painter().setFont(QFont("Helvetica", 10));
  fig.painter().drawText(10, imsize.height()+18, ttl);
  fig.painter().restore();
  /* Done with crop marks */
  fig.painter().scale(iu2pt(), iu2pt());
  fig.setDashScale(iu2pt());
  fig.painter().translate(-fig.extent().left(),
			  -fig.extent().top());
  prog.render(fig);
  fig.painter().end();
  return true;
}

#endif

bool renderImage(Program &prog, Figure &fig, QString ofn) {
  QImage img(int(fig.extent().width()),
	     int(fig.extent().height()),
	     QImage::Format_ARGB32);
  img.fill(0xffffffff);
  fig.painter().begin(&img);
  fig.setHairline(0);
  //  fig.painter().scale(iu2pt(), iu2pt());
  fig.setDashScale(1);
  fig.painter().translate(-fig.extent().left(),
			  -fig.extent().top());
  prog.render(fig);
  fig.painter().end();
  return img.save(ofn, 0, BITMAPQUAL);
}

int noninteractive(QString ifn, QString ofn) {
  if (ofn=="-")
    ofn = "-.ps";
  
  int idx = ofn.lastIndexOf(".");
  if (idx<0)
    return error("Output file must have an extension");
  QString extn = ofn.mid(idx+1);

  bool extnIsBitmap = extn=="png" || extn=="jpg" || extn=="tif" || extn=="tiff";
  if (extnIsBitmap)
    setFACTOR(BITMAPRES/72);

  Program prog;
  if (ifn.isEmpty() || ifn=="-") {
    QFile f; f.open(stdin,QFile::ReadOnly);
    if (!prog.read(f, "<stdin>")) {
      Error() << "Interpretation error";
      return 1;
    }
  } else {
    read(prog, ifn);
  }

  QTemporaryFile tmpf;
  bool usetmpf = false;
  if (ofn == "-."+extn) {
    // write to stdout
    if (!tmpf.open())
      return error("Cannot write to temporary file");
    tmpf.close();
    ofn = tmpf.fileName();
    usetmpf = true;
  }

  Figure fig;
  fig.overrideSize(QSizeF(pt2iu(OVERRIDEWIDTH),
			  pt2iu(OVERRIDEHEIGHT)));
  prerender(prog, fig);

  if (extn == "svg") {
    if (!renderSVG(prog, fig, ofn))
      return error_failtosave(ofn);
   } else if (extn == "eps") {
    return error("Writing to .eps is not supported in this version");
  } else if (extn == "pdf") {
    if (!renderPDF(prog, fig, ofn))
      return error_failtosave(ofn);
  } else if (extn=="ps") {
#ifdef QPLOT_POSTSCRIPT_SUPPORT
    renderPS(prog, fig, ofn, ifn + QString::fromUtf8(" — ")
	     + QDateTime::currentDateTime()
	     .toString(QString::fromUtf8("MM/dd/’yy hh:mm")));
#else
    return error("Writing to .ps is not supported in this version");
#endif
  } else if (extnIsBitmap) {
    if (!renderImage(prog, fig, ofn))
      return error_failtosave(ofn);
  } else {
    return error_unknownextension(extn);
  }

  if (usetmpf) {
    if (!tmpf.open())
      error("Cannot re-read temporary file");
    QFile f;
    if (!f.open(stdout,QFile::WriteOnly))
      error("Cannot write to stdout");
    while (1) {
      QByteArray ba = tmpf.read(1024*1024);
      if (ba.isEmpty())
	break;
      if (f.write(ba)!=ba.size())
	error("Failure to write to stdout");
    }
    if (!tmpf.atEnd())
      error("Error reading from temporary file");
  }
  return 0;
}  

int main(int argc, char **argv) {
  QApplication app(argc, argv);

  QProcessEnvironment env(QProcessEnvironment::systemEnvironment());
  if (env.contains("QPLOT_MAXITER")) {
    MAXTRIES = env.value("QPLOT_MAXITER").toInt();
    qDebug() << "Max shrink iterations set to " << MAXTRIES;
  }

  int argi=1;
  if (argc<2)
    return usage();
  while (argi<argc) {
    QString arg = argv[argi];
    if (arg=="--help") {
      return usage(0);
    } else if (arg=="-r") {
      argi++;
      if (argi>=argc)
	return usage();
      arg = argv[argi];
      bool ok;
      BITMAPRES = arg.toDouble(&ok);
      if (!ok)
	return usage();
      argi++;
    } else if (arg.startsWith("-r")) {
      bool ok;
      BITMAPRES = arg.mid(2).toDouble(&ok);
      if (!ok)
	return usage();
      argi++;
    } else if (arg=="-q") {
      argi++;
      if (argi>=argc)
        return usage();
      arg = argv[argi];
      bool ok;
      BITMAPQUAL = arg.toInt(&ok);
      if (!ok)
        return usage();
      argi++;
    } else if (arg.startsWith("-q")) {
      bool ok;
      BITMAPQUAL = arg.mid(2).toInt(&ok);
      if (!ok)
        return usage();
      argi++;
    } else if (arg=="-w") {
      argi++;
      if (argi>=argc)
	return usage();
      arg = argv[argi];
      bool ok;
      OVERRIDEWIDTH = arg.toDouble(&ok);
      if (!ok)
	return usage();
      argi++;
    } else if (arg.startsWith("-w")) {
      bool ok;
      OVERRIDEWIDTH = arg.mid(2).toDouble(&ok);
      if (!ok)
	return usage();
      argi++;
    } else if (arg=="-h") {
      argi++;
      if (argi>=argc)
	return usage();
      arg = argv[argi];
      bool ok;
      OVERRIDEHEIGHT = arg.toDouble(&ok);
      if (!ok)
	return usage();
      argi++;
    } else if (arg.startsWith("-h")) {
      bool ok;
      OVERRIDEHEIGHT = arg.mid(2).toDouble(&ok);
      if (!ok)
	return usage();
      argi++;
    } else if (arg=="--autoraise") {
      autoraise = true;
      argi++;
    } else if (arg=="--maxtries") {
      argi++;
      if (argi>=argc)
	return usage();
      arg = argv[argi];
      bool ok;
      MAXTRIES = arg.toInt(&ok);
      if (!ok)
	return usage();
      argi++;
    } else if (arg.startsWith("--maxtries=")) {
      argi++;
      bool ok;
      MAXTRIES=arg.mid(QString("--maxtries=").length()).toInt(&ok);
      if (!ok)
	return usage();
    } else {
      break;
    }
  }

  if (argc-argi == 1) 
    return interactive(argv[argi], &app);
  else if (argc-argi == 2) 
    return noninteractive(argv[argi], argv[argi+1]);
  else 
    return usage();
  
}
