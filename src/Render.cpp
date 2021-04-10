// render.cpp

#include "Render.h"
#include "Error.h"

#include <QDebug>
#include <QImage>
#include <QPdfWriter>
#include <QSvgGenerator>
#include <QImage>
#include <cmath>
#include <QFileInfo>
#include <QDir>
#include <QTemporaryFile>

Render::Render(QString ifn): ifn(ifn) {
  if (ifn.isEmpty() || ifn=="-") {
    file.open(stdin,QFile::ReadOnly);
    isok = prog.append(file, "<stdin>");
    if (!isok)
      Error() << "Interpretation error";
  } else {
    isok = read(ifn);
  }
}

void Render::readsome() {
  if (file.isOpen())
    prog.append(file, ifn, false);
}

void Render::loadall() {
  if (file.isOpen())
    prog.append(file, ifn, true);
}

bool Render::read(QString ifn) {
  QFile f(ifn);
  if (f.open(QIODevice::ReadOnly)) {
    if (prog.read(f, ifn))
      return true;
    else
      Error() << "Interpretation failed";
  } else {
    Error() << "Cannot open file";
  }
  return false;
}  


void Render::prerender() {
  QImage img(1,1,QImage::Format_ARGB32);
  fig.setSize(QSizeF(1, 1)); // this may be overridden later
  fig.painter().begin(&img);
  fig.reset();
  foreach (QString p, prog.panels()) {
    QRectF dataExtent = prog.dataRange(p);
    if (p=="-") {
      fig.xAxis().setDataRange(dataExtent.left(), dataExtent.right());
      fig.yAxis().setDataRange(dataExtent.top(), dataExtent.bottom());
    } else {
      fig.panelRef(p).xaxis.setDataRange(dataExtent.left(),
                                         dataExtent.right());
      fig.panelRef(p).yaxis.setDataRange(dataExtent.top(),
                                         dataExtent.bottom());
    }
  }

  int iter = 0;
  while (iter<maxtries) {
    prog.render(fig, true); // render to determine paper bbox & fudge
    if (fig.checkFudged()) {
      //qDebug() << "will reiterate";
    } else {
      //qDebug() << "won't reiterate";
      break;
    }
    iter++;
  } 

  if (iter>=maxtries)
    Error() << QString("“Shrink” failed, even after %1 iterations.").arg(iter);

  fig.painter().end();
}


bool Render::renderSVG(QString ofn) {
  QSvgGenerator img;
  img.setFileName(ofn);
  img.setResolution(90); // anything else seems to be poorly supported
  img.setViewBox(QRectF(QPointF(0,0),
			QSizeF(90./72*iu2pt(fig.extent().width()),
			       90./72*iu2pt(fig.extent().height()))));
  if (!fig.painter().begin(&img))
    return false;
  fig.setHairline(0.25);
  fig.painter().scale(90./72*iu2pt(), 90./72*iu2pt());
  fig.setDashScale(90./72*iu2pt());
  fig.painter().translate(fig.extent().left(),
			  fig.extent().top());
  prog.render(fig);
  fig.painter().end();
  return true;
}


bool Render::renderPDF(QString ofn) {
  QPdfWriter img(ofn);
  img.setPageSizeMM(QSizeF(iu2pt(fig.extent().width())*25.4/72,
			   iu2pt(fig.extent().height())*25.4/72));

  if (!fig.painter().begin(&img))
    return false;
  fig.setHairline(0.25);

  double dpix = img.logicalDpiX();
  double dpiy = img.logicalDpiY();

  fig.painter().translate(-10*dpix/72., -10*dpiy/72.);
  // I don't know why this translation is needed.

  fig.painter().scale(iu2pt()*dpix/72.0,
		      iu2pt()*dpix/72.0);
  fig.setDashScale(iu2pt()*std::sqrt(dpix*dpiy)/72.0);
  fig.painter().translate(-fig.extent().left(),
			  -fig.extent().top());
  prog.render(fig);
  fig.painter().end();
  return true;
}



bool Render::renderImage(QString ofn) {
  QImage img(int(fig.extent().width()),
	     int(fig.extent().height()),
	     QImage::Format_ARGB32);
  img.fill(0xffffffff);
  fig.painter().begin(&img);
  fig.setHairline(0);

  fig.setDashScale(1);
  fig.painter().translate(-fig.extent().left(),
			  -fig.extent().top());
  prog.render(fig);
  fig.painter().end();
  return img.save(ofn, 0, bitmapqual);
}


static bool error(QString const &s) {
  Error() << s;
  return false;
}

static bool error_failtosave(QString const &fn) {
  if (fn.isEmpty())
    return error("Failed to save: no filename");
  QFileInfo fi(fn);
  QDir d(fi.dir());
  QString err = QString("Failed to save as “%1”").arg(fn);
  if (!d.exists())
    err += QString(": The folder “%1” does not exist.").arg(d.path());
  else if (!QFileInfo(d.path()).isWritable())
    err += QString(": The folder “%1” is not writable.").arg(d.path());
  else if (fi.exists() && !fi.isWritable())
    err += ": File exists and is not writable.";
  else
    err += ". (Reason unknown.)";
  return error(err);
}

static bool error_unknownextension(QString const &extn) {
  QString err = "Failed to save";
  if (extn.isEmpty())
    err += ": Filename without an extension.";
  else
    err += QString(": Unknown extension “%1”.").arg(extn);
  return error(err);
}


bool Render::noninteractive(QString ifn, QString ofn) {
  Render render(ifn);
  return render.save(ofn);
}

bool Render::save(QString ofn) {
  if (ofn=="-")
    ofn = "-.pdf";
  
  int idx = ofn.lastIndexOf(".");
  if (idx<0)
    return error("Output file must have an extension");
  QString extn = ofn.mid(idx+1);

  bool extnIsBitmap = extn=="png" || extn=="jpg"
    || extn=="tif" || extn=="tiff";
  if (extnIsBitmap)
    setFACTOR(bitmapres/72);

  QTemporaryFile tmpf;
  bool usetmpf = false;
  if (ofn == "-." + extn) {
    // write to stdout
    if (!tmpf.open())
      return error("Cannot write to temporary file");
    tmpf.close();
    ofn = tmpf.fileName();
    usetmpf = true;
  }

  Figure fig;
  fig.overrideSize(QSizeF(pt2iu(overridewidth),
			  pt2iu(overrideheight)));
  prerender();

  if (extn == "svg") {
    if (!renderSVG(ofn))
      return error_failtosave(ofn);
  } else if (extn == "pdf") {
    if (!renderPDF(ofn))
      return error_failtosave(ofn);
  } else if (extnIsBitmap) {
    if (!renderImage(ofn))
      return error_failtosave(ofn);
  } else {
    if (extn=="eps" || extn=="ps") 
      return error("PostScript output is no longer supported");
    else
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
  return true;
}  


void Render::setMaxTries(int n) {
  maxtries = n;
}

void Render::overrideWidth(double w) {
  overridewidth = w;
}

void Render::overrideHeight(double h) {
  overrideheight =h;
}

void Render::setBitmapResolution(double r) {
  bitmapres = r;
}

void Render::setBitmapQuality(int q) {
  bitmapqual = q;
}

void Render::perhapsSave() {
  CmdSave *cmd = prog.nextSave();
  if (cmd) {
    setBitmapResolution(cmd->resolution());
    setBitmapQuality(cmd->quality());
    save(cmd->filename());
  }
}
