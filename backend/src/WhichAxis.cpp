// WhichAxis.cpp

#include "WhichAxis.h"
#include <algorithm>

WhichAxis::WhichAxis(AxisName d): d(d) {
}

Axis const &WhichAxis::axis(Panel const &p) const {
  return d==AxisName::X ? p.xaxis : p.yaxis;
}

Axis &WhichAxis::axis(Panel &p) const {
  return d==AxisName::X ? p.xaxis : p.yaxis;
}

Range WhichAxis::axisPRange(Axis const &a) const {
  QPointF p1 = a.minp();
  QPointF p2 = a.maxp();
  return d==AxisName::X ? Range(p1.x(),p2.x()) : Range(p1.y(), p2.y());
}

double WhichAxis::rectMin(QRectF const &r) const {
  return d==AxisName::X ? r.left() : r.top();
}
  
double WhichAxis::rectMax(QRectF const &r) const {
  return d==AxisName::X ? r.right() : r.bottom();
}

Range WhichAxis::rectRange(QRectF const &r) const {
  return Range(rectMin(r), rectMax(r));
}

QRectF WhichAxis::rerect(QRectF orig, double newmin, double newmax) const {
  if (d==AxisName::X)
    return QRectF(newmin, orig.top(), newmax-newmin, orig.height());
  else
    return QRectF(orig.left(), newmin, orig.width(), newmax-newmin);
}

QPointF WhichAxis::repoint(QPointF orig, double newdim) const {
  if (d==AxisName::X)
    return QPointF(newdim, orig.y());
  else
    return QPointF(orig.x(), newdim);
}

double WhichAxis::point(QPointF p) const {
  return d==AxisName::X ? p.x() : p.y();
}

WhichAxis const &WhichAxis::x() {
  static WhichAxis de(AxisName::X);
  return de;
}

WhichAxis const &WhichAxis::y() {
  static WhichAxis de(AxisName::Y);
  return de;
}


QList<QStringList> WhichAxis::orderedGroups(Figure const &f,
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
