// WhichAxis.h

#ifndef WHICHAXIS_H

#define WHICHAXIS_H

#include "Panel.h"
#include "Axis.h"
#include "Range.h"
#include "Figure.h"

class WhichAxis {
public:
  enum class AxisName {
    X,
    Y,
  };
public:
  static WhichAxis const &x();
  static WhichAxis const &y();
public:
  WhichAxis(AxisName d);
  Axis const &axis(Panel const &p) const;
  Axis &axis(Panel &p) const;
  Range axisPRange(Axis const &a) const;
  double rectMin(QRectF const &) const;
  double rectMax(QRectF const &) const;
  Range rectRange(QRectF const &) const;
  QRectF rerect(QRectF orig, double newmin, double newmax) const;
  QPointF repoint(QPointF p, double newdim) const;
  double point(QPointF p) const;
  QList<QStringList> orderedGroups(Figure const &f, QStringList ids) const;
private:
  AxisName d;
};

#endif
