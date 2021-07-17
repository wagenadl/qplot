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
  void prerender(int upto=-1);
  bool renderSVG(QString ofn, int upto=-1);
  bool renderPDF(QString ofn, int upto=-1);
  bool renderImage(QString ofn, int upto=-1);
  bool save(QString ofn, int upto=-1);
  void setMaxTries(int);
  void overrideWidth(double w);
  void overrideHeight(double h);
  void setBitmapResolution(double r);
  void setBitmapQuality(int q);
  void dosaves(int start=0, int end=-1); // in terms of command indices
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
