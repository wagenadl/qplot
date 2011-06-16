// Figure.H

#ifndef FIGURE_H

#define FIGURE_H

#include "Axis.H"

#include <QRectF>
#include <QPainter>

class Figure {
public:
  enum HAlign {
    LEFT, CENTER, RIGHT,
  };
  enum VAlign {
    TOP, MIDDLE, BOTTOM, BASE,
  };
public:
  Figure();
  void setSize(QSizeF wh_pt);
  void setExtent(QRectF xywh_pt);
  /*:N Iff this is a genuine change, I will reset axis mapping. Thus, the
       render() of a program can be rerun multiple times without axis reset.
       In particular, that means that results from "fudge" will be preserved.
  */
  QRectF const &extent() const;
  Axis &xAxis();
  Axis &yAxis();
  /*:N Note that the yAxis normally runs up, that is, the minimum of its
       data range has a paper coordinate greater than the maximum of its
       data range. */
  QPointF map(double x, double y) const; // data to paper
  void clearBBox(bool full=false);
  void setBBox(QRectF const &); // sets lastbbox, updates fullbbox and cumulbbox
  void setAnchor(QPointF const &, double phi=0); // in paper coords
  void setAnchor(double x, double y, double dx=1, double dy=0); // in data coords
  QPointF const &anchor() const;
  double const &anchorAngle() const;
  QRectF const &lastBBox() const;
  QRectF const &cumulBBox() const;
  QRectF const &fullBBox() const;
  void setVAlign(VAlign a);
  void setHAlign(HAlign a);
  VAlign vAlign() const;
  HAlign hAlign() const;
  QPainter &painter();
private:
  QRectF figextent;
  Axis xax, yax;
  QRectF fullbbox, cumulbbox, lastbbox;
  QPainter p;
  QPointF anch;
  double anchang;
  VAlign valign;
  HAlign halign;
private:
  void replaceAxes();
};

#endif
