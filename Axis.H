// Axis.H

#ifndef AXIS_H

#define AXIS_H

#include <QPointF>

class Axis {
public:
  Axis();
  void setDataRange(double x0, double x1, bool isAuto=false);
  void resetDataRange(); // enables auto ranging
  void fixDataRange(); // disables auto ranging
  bool isAuto() const;
  void expandDataRange(double x0, double x1, bool isAuto=false);
  void setPlacement(QPointF p0_pt, QPointF p1_pt);
  /* For a horizontal axis, normally p0_pt.y=p1_pt.y=0;
     for a vertical axis, normally p0_pt.x=p1_pt.x=0.
     That allows simple addition of the output of map() from a pair of axes.
  */
  double min() const; // data coord
  double max() const; // data coord
  QPointF minp() const; // paper coord (pt)
  QPointF maxp() const; // paper coord (pt)
  QPointF map(double x) const;
private:
  void recalc();
private:
  double x0, x1; // data
  QPointF p0, p1; // paper
  QPointF dp;
  bool isauto;
  bool isempty;
};

#endif
