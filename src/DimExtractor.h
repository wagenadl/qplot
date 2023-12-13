// DimExtractor.h

#ifndef DIMEXTRACTOR_H

#define DIMEXTRACTOR_H

#include "Panel.h"
#include "Axis.h"
#include "Range.h"

class DimExtractor {
public:
  enum class Dim {
    X,
    Y,
  };
public:
  static DimExtractor const &x();
  static DimExtractor const &y();
public:
  DimExtractor(Dim d);
  Axis const &axis(Panel const &p) const;
  Range axisPRange(Axis const &a) const;
  double rectMin(QRectF const &) const;
  double rectMax(QRectF const &) const;
  Range rectRange(QRectF const &) const;
  QRectF rerect(QRectF orig, double newmin, double newmax) const;
private:
  Dim d;
};

#endif
