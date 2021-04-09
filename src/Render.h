// render.h

#ifndef RENDER_H

#define RENDER_H

#include "Program.h"
#include "Figure.h"
#include <QString>

class Render {
public:
  Render(QString ifn);
  QString inputFilename() { return ifn; }
  bool read(QString ifn);
  Program *program() { return &prog; }
  Figure *figure() { return &fig; }
  void prerender();
  bool renderSVG(QString ofn);
  bool renderPDF(QString ofn);
  bool renderImage(QString ofn);
  bool save(QString ofn);
  void setMaxTries(int);
  void overrideWidth(double w);
  void overrideHeight(double h);
  void setBitmapResolution(double r);
  void setBitmapQuality(int q);
  static bool noninteractive(QString ifn, QString ofn);
  bool valid() const { return isok; }
private:
  QString ifn;
  bool isok;
  Program prog;
  Figure fig;
  int maxtries = 100;
  double bitmapres = 300;
  int bitmapqual = 95;
  double overridewidth = 0;
  double overrideheight = 0;
};
  
#endif
