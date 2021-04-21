// render.h

#ifndef RENDER_H

#define RENDER_H

#include "Program.h"
#include "Figure.h"
#include <QString>

class Renderer {
public:
  Renderer();
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
private:
  Program prog;
  Figure fig;
  int maxtries = 100;
  double bitmapres = 300;
  int bitmapqual = 95;
  double overridewidth = 0;
  double overrideheight = 0;
};
  
#endif
