// Figure.H

#ifndef FIGURE_H

#define FIGURE_H

#include "Axis.H"

#include <QRectF>
#include <QPainter>

class Figure {
public:
  Figure();
  void setSize(QSizeF wh_pt);
  QSizeF const &size() const;
  Axis &xAxis();
  Axis &yAxis();
  void clearBBox(bool full=false);
  void setBBox(QRectF const &); // sets lastbbox, updates fullbbox and cumulbbox
  QRectF const &lastBBox() const;
  QRectF const &cumulBBox() const;
  QRectF const &fullBBox() const;
  QPainter &painter();
private:
  QSizeF figsize;
  Axis xax, yax;
  QRectF fullbbox, cumulbbox, lastbbox;
  QPainter p;
};

#endif
