// DimExtractor.cpp

#include "DimExtractor.h"
#include <algorithm>

DimExtractor::DimExtractor(Dim d): d(d) {
}

Axis const &DimExtractor::axis(Panel const &p) const {
  return d==Dim::X ? p.xaxis : p.yaxis;
}

Axis &DimExtractor::axis(Panel &p) const {
  return d==Dim::X ? p.xaxis : p.yaxis;
}

Range DimExtractor::axisPRange(Axis const &a) const {
  QPointF p1 = a.minp();
  QPointF p2 = a.maxp();
  return d==Dim::X ? Range(p1.x(),p2.x()) : Range(p1.y(), p2.y());
}

double DimExtractor::rectMin(QRectF const &r) const {
  return d==Dim::X ? r.left() : r.top();
}
  
double DimExtractor::rectMax(QRectF const &r) const {
  return d==Dim::X ? r.right() : r.bottom();
}

Range DimExtractor::rectRange(QRectF const &r) const {
  return Range(rectMin(r), rectMax(r));
}

QRectF DimExtractor::rerect(QRectF orig, double newmin, double newmax) const {
  if (d==Dim::X)
    return QRectF(newmin, orig.top(), newmax-newmin, orig.height());
  else
    return QRectF(orig.left(), newmin, orig.width(), newmax-newmin);
}

QPointF DimExtractor::repoint(QPointF orig, double newdim) const {
  if (d==Dim::X)
    return QPointF(newdim, orig.y());
  else
    return QPointF(orig.x(), newdim);
}

double DimExtractor::point(QPointF p) const {
  return d==Dim::X ? p.x() : p.y();
}

DimExtractor const &DimExtractor::x() {
  static DimExtractor de(Dim::X);
  return de;
}

DimExtractor const &DimExtractor::y() {
  static DimExtractor de(Dim::Y);
  return de;
}


QList<QStringList> DimExtractor::orderedGroups(Figure const &f,
                                               QStringList ids) const {
  QList<QStringList> result;
  QMap<QString, double> centerpos;
  QMap<QString, Range> range;
  for (QString id: ids) {
    Panel const &p(f.panel(id));
    Range r = rectRange(p.desiredExtent);
    range[id] = r;
    centerpos[id] = (r.min() + r.max())/2;
  }
  auto key = [centerpos](QString a, QString b) {
    return centerpos[a]<centerpos[b];
  };
  std::sort(ids.begin(), ids.end(), key);
  QStringList now;
  Range r;
  for (QString id: ids) {
    if (r.contains(centerpos[id])) {
      now << id;
    } else {
      if (!now.empty())
        result << now;
      now = QStringList();
      now << id;
      r = range[id];
    }
  }
  if (!now.empty())
    result << now;
  return result;
}
