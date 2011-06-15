// Geometry.H

#ifndef GEOMETRY_H

#define GEOMETRY_H

#include <QPointF>
#include <QRectF>
#include <QTransform>

class UnitVector {
public:
  UnitVector();
  explicit UnitVector(QPointF const &xy);
  void set(QPointF const &xy); // angle is atan2(y,x)
  double angle() const; // radians in data space!
  QPointF const &xy() const;
  QTransform const &transform() const;
private:
  QPointF xy_d;
  double ang;
  QTransform xform;
};

extern QTransform rectMapping(QRectF const &src, QRectF const &dst);

class DataOnPaper {
  /*:C DataOnPaper
   *:D Describes the location of a system of data axes in metric space.
   */
public:
  DataOnPaper(QRectF const &dataRect, QRectF const &paperRect);
  void setDataRect(QRectF const &dataRect);
  void setPaperRect(QRectF const &paperRect);
  QRectF const &dataRect() const; // in data coords
  QRectF const &paperRect() const; // in postscript points
  QPointF dataToPaper(QPointF const &dataPt) const;
  QTransform const &transform() const;
private:
  QRectF dataR;
  QRectF paperR;
  QTransform mapper;
};
  

class MetricOnData {
  /*:C MetricOnData
   *:D Attaches a metric coordinate system to a certain data point in a graph.
       This requires that the graph is pinned to the underlying base metric
       space.
       We are thus dealing with three coordinate system:
       - The "base": actual x-y coordinates on paper, measured in points
       - The "data": x-y coordinates in data space
       - The "metric": possibly rotated coordinate system attached to a
         certain point in the data space (the "origin").
   */
public:
  MetricOnData(DataOnMetric const &base);
  MetricOnData(DataOnMetric const &base, QPointF const &xy_data);
  MetricOnData(DataOnMetric const &base, QPointF const &xy_data,
	       UnitVector const &rot_data);
  /*:N The "base" must remain in existence for the lifetime of this object.
    It is not required to remain constant, however. We use it in metricToData()
    and metricToPaper() conversions.
  */
  void setOrigin(QPointF const &xy_data);
  void setRotation(UnitVector const &rot_data);
  QPointF metricToData(QPointF const &xy) const;
  QPointF metricToPaper(QPointF const &xy) const;
  QPointF origin() const;
  UnitVector rotation() const;
private:
  DataOnMetric const &base;
  QPointF orig;
  UnitVector rot;
};

#endif
