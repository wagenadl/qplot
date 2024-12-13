// renderer.cpp

#include "Renderer.h"
#include "Error.h"
#include "CmdSave.h"

#include <QDebug>
#include <QImage>
#include <QPdfWriter>
#include <QSvgGenerator>
#include <QImage>
#include <cmath>
#include <QFileInfo>
#include <QDir>
#include <QTemporaryFile>

Renderer::Renderer() {
  maxtries = 1000;
  bitmapres = 300;
  bitmapqual = 95;
  overridewidth = 0;
  overrideheight = 0;
}

void Renderer::prerender(int upto) {
  //  qDebug() << "prerender" << upto;
  QImage img(1,1,QImage::Format_ARGB32);
  fig.setSize(QSizeF(1, 1)); // this may be overridden later
  fig.painter().begin(&img);
  fig.hardReset();
  foreach (QString p, prog.panels(upto)) {
    QRectF dataExtent = prog.dataRange(p, upto);
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

  QMap<int, int> itercount; // organize by line number
  QMap<int, int> maxitercount; // organize by line number
  bool fail = false;
  int totaliter = 0;
  while (true) {
    int line = prog.render(fig, true, upto);
    // renderer to determine paper bbox & fudge
    if (fig.checkFudgeFailure()) {
      fail = true;
      break;
    } else if (fig.checkFudged()) {
      for (auto it=itercount.begin(); it!=itercount.end(); ++it)
        if (it.key()<line)
          it.value() = 0;
      itercount[line] += 1;
      totaliter += 1;
      if (itercount[line] > maxitercount[line])
        maxitercount[line] = itercount[line];
      if (itercount[line] >= maxtries) {
        Error() << QString("Shrink iterations exceeded at %1: %2 >= %3")
          .arg(line).arg(itercount[line]).arg(maxtries);
        fail = true;
        break;
      }
    } else {
      break;
    }
  } 


  if (fail) {
    Error() << QString("\"Shrink\" failed after %1 iterations").arg(totaliter);
    qDebug() << "Iteration detail: " << itercount;
    qDebug() << "Max iteration detail: " << maxitercount;
  }

  fig.painter().end();
}


bool Renderer::renderSVG(QString ofn, int upto) {
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
  prog.render(fig, false, upto);
  fig.painter().end();
  return true;
}


bool Renderer::renderPDF(QString ofn, int upto) {
  QPdfWriter img(ofn);
  img.setPageSize(QPageSize(QSizeF(iu2pt(fig.extent().width()),
				            iu2pt(fig.extent().height())), 
							QPageSize::Point));

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
  prog.render(fig, false, upto);
  fig.painter().end();
  return true;
}



bool Renderer::renderImage(QString ofn, int upto) {
  QImage img(int(fig.extent().width()),
	     int(fig.extent().height()),
	     QImage::Format_ARGB32);
  img.fill(0xffffffff);
  fig.painter().begin(&img);
  fig.painter().setRenderHint(QPainter::Antialiasing);
  fig.painter().setRenderHint(QPainter::TextAntialiasing);
  fig.setHairline(0);

  fig.setDashScale(1);
  fig.painter().translate(-fig.extent().left(),
			  -fig.extent().top());
  prog.render(fig, false, upto); 
  fig.painter().end();
  if (ofn.endsWith("jpg") || ofn.endsWith("jpeg"))
    return img.save(ofn, 0, bitmapqual);
  else
    return img.save(ofn);
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


bool Renderer::save(QString ofn, int upto) {
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
  prerender(upto);

  if (extn == "svg") {
    if (!renderSVG(ofn, upto))
      return error_failtosave(ofn);
  } else if (extn == "pdf") {
    if (!renderPDF(ofn, upto))
      return error_failtosave(ofn);
  } else if (extnIsBitmap) {
    if (!renderImage(ofn, upto))
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
    if (!f.open(stdout, QFile::WriteOnly))
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


void Renderer::setMaxTries(int n) {
  //  qDebug() << "setmaxtries" << n;
  maxtries = n;
}

void Renderer::overrideWidth(double w) {
  overridewidth = w;
}

void Renderer::overrideHeight(double h) {
  overrideheight =h;
}

void Renderer::setBitmapResolution(double r) {
  bitmapres = r;
}

void Renderer::setBitmapQuality(int q) {
  bitmapqual = q;
}

//void Renderer::perhapsSave() {
//  CmdSave *cmd = prog.nextSave();
//  if (cmd) {
//    setBitmapResolution(cmd->resolution());
//    setBitmapQuality(cmd->quality());
//    save(cmd->filename());
//  }
//}

void Renderer::dosaves(int start, int end) {
  if (end<0)
    end = prog.length();
  for (int k=start; k<end; k++) {
    CmdSave const *cmd = dynamic_cast<CmdSave const *>(prog.command(k));
    if (cmd) {
      setBitmapResolution(cmd->resolution());
      setBitmapQuality(cmd->quality());
      save(cmd->filename(), k);
    }
  }
}
